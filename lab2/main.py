from __future__ import annotations

import time
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from algorithms import ffdh, nfdh
from data_handler import generate_random_tasks, parse_llnl_logs
from metrics import get_epsilon, get_lower_bound, get_stats
from plotter import plot_accuracy, plot_time_complexity

Task = Tuple[int, int]  # (r_j, t_j)


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


def experiment_time_complexity(m_values: Sequence[int], n: int) -> None:
    nfdh_times: List[float] = []
    ffdh_times: List[float] = []

    for m in m_values:
        tasks = generate_random_tasks(m, n, seed=1000 + m)
        result = _run_one_dataset(tasks, n)
        nfdh_times.append(result["nfdh_runtime"])
        ffdh_times.append(result["ffdh_runtime"])

    plot_time_complexity(m_values, nfdh_times, ffdh_times, filename="time_complexity.png")


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
        title="Random Tasks: Epsilon Mean and Std",
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
        base_tasks = parse_llnl_logs(log_path, m)
        if not base_tasks:
            print(f"No valid LLNL tasks for m={m}, stopping LLNL experiment.")
            break

        # For "runs", reuse same data as deterministic baseline.
        nfdh_eps_list: List[float] = []
        ffdh_eps_list: List[float] = []
        for _ in range(runs):
            result = _run_one_dataset(base_tasks, n)
            nfdh_eps_list.append(result["nfdh_eps"])
            ffdh_eps_list.append(result["ffdh_eps"])

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
            title="LLNL Logs: Epsilon Mean and Std",
        )


def main() -> None:
    n = 1024
    m_values = list(range(500, 5001, 500))
    llnl_path = Path("data/LLNL-UBGL-2006-2.swf")

    Path("data").mkdir(exist_ok=True)
    Path("graphs").mkdir(exist_ok=True)

    experiment_time_complexity(m_values, n)
    experiment_random_stats(m_values, n, runs=10)
    experiment_llnl_stats(m_values, n, llnl_path, runs=10)

    print("Done. Graphs saved to graphs/")


if __name__ == "__main__":
    main()
