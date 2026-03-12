from __future__ import annotations

import argparse
import time
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from algorithms import ffdh, nfdh
from data_handler import generate_random_tasks, parse_llnl_logs, parse_tasks_file
from metrics import get_epsilon, get_lower_bound, get_stats
from plotter import plot_accuracy, plot_time_complexity

Task = Tuple[int, int]  # (r_j, t_j)
Schedule = List[Dict[str, object]]


def _run_one_dataset(tasks: Sequence[Task], n: int) -> Dict[str, float]:
    t0 = time.perf_counter()
    _, nfdh_t = nfdh(tasks, n)
    nfdh_runtime = time.perf_counter() - t0

    t1 = time.perf_counter()
    _, ffdh_t = ffdh(tasks, n)
    ffdh_runtime = time.perf_counter() - t1

    t_prime = get_lower_bound(tasks, n)
    return {
        "nfdh_runtime": nfdh_runtime,
        "ffdh_runtime": ffdh_runtime,
        "nfdh_eps": get_epsilon(nfdh_t, t_prime),
        "ffdh_eps": get_epsilon(ffdh_t, t_prime),
    }


def experiment_time_complexity(m_values: Sequence[int], n_values: Sequence[int]) -> None:
    series: "OrderedDict[str, List[float]]" = OrderedDict()
    for n in n_values:
        series[f"NFDH (n={n})"] = []
        series[f"FFDH (n={n})"] = []

    for m in m_values:
        for n in n_values:
            tasks = generate_random_tasks(m, n, seed=1000 + m + n)
            result = _run_one_dataset(tasks, n)
            series[f"NFDH (n={n})"].append(result["nfdh_runtime"])
            series[f"FFDH (n={n})"].append(result["ffdh_runtime"])

    plot_time_complexity(m_values, series, filename="time_complexity.png")


def experiment_random_stats(m_values: Sequence[int], n: int, runs: int = 10) -> None:
    nfdh_mean: List[float] = []
    nfdh_std: List[float] = []
    ffdh_mean: List[float] = []
    ffdh_std: List[float] = []

    for m in m_values:
        nfdh_eps_list: List[float] = []
        ffdh_eps_list: List[float] = []
        for run_idx in range(runs):
            tasks = generate_random_tasks(m, n, seed=10_000 + m * 100 + run_idx)
            result = _run_one_dataset(tasks, n)
            nfdh_eps_list.append(result["nfdh_eps"])
            ffdh_eps_list.append(result["ffdh_eps"])

        m1, s1 = get_stats(nfdh_eps_list)
        m2, s2 = get_stats(ffdh_eps_list)
        nfdh_mean.append(m1)
        nfdh_std.append(s1)
        ffdh_mean.append(m2)
        ffdh_std.append(s2)

    plot_accuracy(
        m_values,
        nfdh_mean,
        nfdh_std,
        ffdh_mean,
        ffdh_std,
        filename="random_stats.png",
        title="Случайные задачи: среднее и стандартное отклонение epsilon",
    )


def experiment_llnl_stats(m_values: Sequence[int], n: int, log_path: Path, runs: int = 10) -> None:
    if not log_path.exists():
        print(f"LLNL file not found, skipping experiment: {log_path}")
        return

    nfdh_mean: List[float] = []
    nfdh_std: List[float] = []
    ffdh_mean: List[float] = []
    ffdh_std: List[float] = []

    for m in m_values:
        nfdh_eps_list: List[float] = []
        ffdh_eps_list: List[float] = []
        for run_idx in range(runs):
            # Use different contiguous slices of the log per run.
            tasks = parse_llnl_logs(log_path, m, offset=run_idx * m, max_width=n)
            if len(tasks) < m:
                break
            result = _run_one_dataset(tasks, n)
            nfdh_eps_list.append(result["nfdh_eps"])
            ffdh_eps_list.append(result["ffdh_eps"])

        if not nfdh_eps_list:
            print(f"No valid LLNL tasks for m={m}, stopping LLNL experiment.")
            break

        m1, s1 = get_stats(nfdh_eps_list)
        m2, s2 = get_stats(ffdh_eps_list)
        nfdh_mean.append(m1)
        nfdh_std.append(s1)
        ffdh_mean.append(m2)
        ffdh_std.append(s2)

    valid_m = list(m_values)[: len(nfdh_mean)]
    if valid_m:
        plot_accuracy(
            valid_m,
            nfdh_mean,
            nfdh_std,
            ffdh_mean,
            ffdh_std,
            filename="llnl_stats.png",
            title="Логи LLNL: среднее и стандартное отклонение epsilon",
        )


def _format_schedule(schedule: Schedule) -> str:
    rows: List[str] = []
    current_time = 0
    for idx, level in enumerate(schedule, start=1):
        height = int(level["height"])
        remaining = int(level["remaining"])
        tasks = level["tasks"]
        rows.append(
            f"level={idx}, start={current_time}, end={current_time + height}, "
            f"height={height}, remaining={remaining}, tasks={tasks}"
        )
        current_time += height
    return "\n".join(rows)


def run_single_instance(input_file: Path, n: int, algorithm: str) -> None:
    tasks = parse_tasks_file(input_file)
    if not tasks:
        raise ValueError("Input file has no tasks")

    algorithm_key = algorithm.upper()
    t0 = time.perf_counter()
    if algorithm_key == "NFDH":
        schedule, t_s = nfdh(tasks, n)
    elif algorithm_key == "FFDH":
        schedule, t_s = ffdh(tasks, n)
    else:
        raise ValueError("algorithm must be NFDH or FFDH")
    runtime = time.perf_counter() - t0

    t_prime = get_lower_bound(tasks, n)
    epsilon = get_epsilon(t_s, t_prime)

    print(f"Algorithm: {algorithm_key}")
    print(f"Input file: {input_file}")
    print(f"n: {n}")
    print("S:")
    print(_format_schedule(schedule))
    print(f"T(S): {t_s}")
    print(f"T': {t_prime:.6f}")
    print(f"epsilon: {epsilon:.6f}")
    print(f"time_seconds: {runtime:.6f}")


def run_experiments() -> None:
    n = 1024
    n_values_time = [1024, 4096]
    m_values = list(range(500, 5001, 500))
    m_values_llnl = [500, 1000, 1500]
    llnl_path = Path("data/LLNL-UBGL-2006-2.swf")

    Path("data").mkdir(exist_ok=True)
    Path("graphs").mkdir(exist_ok=True)

    experiment_time_complexity(m_values, n_values_time)
    experiment_random_stats(m_values, n, runs=10)
    experiment_llnl_stats(m_values_llnl, n, llnl_path, runs=10)

    print("Done. Graphs saved to graphs/")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lab 2 strip packing runner.")
    parser.add_argument(
        "--mode",
        choices=["experiments", "single"],
        default="experiments",
        help="Run full experiments or a single file/algorithm instance.",
    )
    parser.add_argument(
        "--input-file",
        type=Path,
        default=None,
        help="Path to tasks file for --mode single.",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1024,
        help="Machine count n. For --mode single this value is required in practice.",
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        choices=["NFDH", "FFDH", "nfdh", "ffdh"],
        default="NFDH",
        help="Algorithm for --mode single.",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.mode == "single":
        if args.input_file is None:
            parser.error("--input-file is required for --mode single")
        run_single_instance(args.input_file, args.n, args.algorithm)
        return

    run_experiments()


if __name__ == "__main__":
    main()
