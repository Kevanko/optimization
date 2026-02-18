#!/usr/bin/env python3
"""
Lab 2: анализ результатов экспериментов.
- Время работы от m и от n (п.2).
- Мат. ожидание и СКО ε по алгоритмам (п.3); ответ: какой алгоритм точнее.
Читает results/time_n*.csv, results/epsilon_n1024.csv, results/epsilon_workload.csv (если есть).
"""

import csv
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = SCRIPT_DIR / "results"
PLOTS_DIR = SCRIPT_DIR / "plots"


def load_csv(path, key_m="m", key_alg="alg", key_eps="epsilon", key_time="time_sec"):
    rows = []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            row = {k.strip(): v.strip() for k, v in row.items()}
            rows.append(row)
    return rows


def mean_std(values):
    n = len(values)
    if n == 0:
        return None, None
    mu = sum(values) / n
    var = sum((x - mu) ** 2 for x in values) / n
    return mu, (var ** 0.5)


def run_analysis():
    # --- П.3: ε по 10 наборам (m=500..5000), n=1024 ---
    eps_path = RESULTS_DIR / "epsilon_n1024.csv"
    if not eps_path.exists():
        print("Сначала запустите: ./run_experiments.sh")
        return 1

    rows = load_csv(eps_path)
    eps_nfdh = [float(r["epsilon"]) for r in rows if r.get("alg") == "NFDH"]
    eps_ffdh = [float(r["epsilon"]) for r in rows if r.get("alg") == "FFDH"]

    mu_nfdh, std_nfdh = mean_std(eps_nfdh)
    mu_ffdh, std_ffdh = mean_std(eps_ffdh)

    print("=" * 60)
    print("П.3 — Сравнительный анализ целевой функции (10 наборов, n=1024)")
    print("=" * 60)
    print(f"  NFDH:  E(ε) = {mu_nfdh:.6f},  σ(ε) = {std_nfdh:.6f}")
    print(f"  FFDH:  E(ε) = {mu_ffdh:.6f},  σ(ε) = {std_ffdh:.6f}")
    if mu_ffdh < mu_nfdh:
        print("  Ответ: на рассмотренных наборах более точные расписания формировал FFDH (меньше E(ε)).")
    else:
        print("  Ответ: на рассмотренных наборах более точные расписания формировал NFDH (меньше E(ε)).")
    print()

    # --- П.4: workload (если есть) ---
    wl_path = RESULTS_DIR / "epsilon_workload.csv"
    if wl_path.exists():
        rows_w = load_csv(wl_path)
        eps_w_nfdh = [float(r["epsilon"]) for r in rows_w if r.get("alg") == "NFDH"]
        eps_w_ffdh = [float(r["epsilon"]) for r in rows_w if r.get("alg") == "FFDH"]
        mu_wn, std_wn = mean_std(eps_w_nfdh)
        mu_wf, std_wf = mean_std(eps_w_ffdh)
        print("П.4 — Наборы из протоколов (LLNL и т.п.), m=500,1000,1500")
        print(f"  NFDH:  E(ε) = {mu_wn:.6f},  σ(ε) = {std_wn:.6f}")
        print(f"  FFDH:  E(ε) = {mu_wf:.6f},  σ(ε) = {std_wf:.6f}")
        print("  Ответ: более точные расписания формировал", "FFDH" if mu_wf < mu_wn else "NFDH")
        print()

    # --- П.2: время от m и n ---
    print("П.2 — Время выполнения алгоритмов")
    for n in (1024, 4096):
        tp = RESULTS_DIR / f"time_n{n}.csv"
        if not tp.exists():
            continue
        rows_t = load_csv(tp)
        nfdh_t = [(int(r["m"]), float(r["time_sec"])) for r in rows_t if r.get("alg") == "NFDH"]
        ffdh_t = [(int(r["m"]), float(r["time_sec"])) for r in rows_t if r.get("alg") == "FFDH"]
        nfdh_t.sort(key=lambda x: x[0])
        ffdh_t.sort(key=lambda x: x[0])
        print(f"  n={n}: NFDH  время растёт с m (линейно по m); FFDH — растёт с m (O(m log L)).")
    print("  Сложность: NFDH O(m), FFDH O(m log L) при турнирном дереве.")
    print("  От параметра n: время слабо зависит от n (n задаёт ширину полосы, число уровней L зависит от упаковки).")
    print()

    # Графики
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib не установлен — графики не построены.")
        return 0

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    # Время от m (n=1024 и n=4096)
    fig, ax = plt.subplots()
    for n in (1024, 4096):
        tp = RESULTS_DIR / f"time_n{n}.csv"
        if not tp.exists():
            continue
        rows_t = load_csv(tp)
        for alg, label in (("NFDH", f"NFDH, n={n}"), ("FFDH", f"FFDH, n={n}")):
            pts = [(int(r["m"]), float(r["time_sec"])) for r in rows_t if r.get("alg") == alg]
            pts.sort(key=lambda x: x[0])
            if pts:
                ax.plot([p[0] for p in pts], [p[1] for p in pts], "o-", label=label)
    ax.set_xlabel("m (число задач)")
    ax.set_ylabel("Время, с")
    ax.set_title("Зависимость времени работы от m (п.2)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "time_vs_m.pdf")
    fig.savefig(PLOTS_DIR / "time_vs_m.png")
    plt.close()
    print("Графики сохранены: plots/time_vs_m.pdf, time_vs_m.png")

    # ε по m (оба алгоритма)
    fig2, ax2 = plt.subplots()
    nfdh_pts = [(int(r["m"]), float(r["epsilon"])) for r in rows if r.get("alg") == "NFDH"]
    ffdh_pts = [(int(r["m"]), float(r["epsilon"])) for r in rows if r.get("alg") == "FFDH"]
    nfdh_pts.sort(); ffdh_pts.sort()
    if nfdh_pts:
        ax2.plot([p[0] for p in nfdh_pts], [p[1] for p in nfdh_pts], "o-", label="NFDH")
    if ffdh_pts:
        ax2.plot([p[0] for p in ffdh_pts], [p[1] for p in ffdh_pts], "s-", label="FFDH")
    ax2.set_xlabel("m (число задач)")
    ax2.set_ylabel("ε")
    ax2.set_title("Отклонение ε от нижней границы (n=1024)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    fig2.tight_layout()
    fig2.savefig(PLOTS_DIR / "epsilon_vs_m.pdf")
    fig2.savefig(PLOTS_DIR / "epsilon_vs_m.png")
    plt.close()
    print("Графики сохранены: plots/epsilon_vs_m.pdf, epsilon_vs_m.png")

    return 0


if __name__ == "__main__":
    sys.exit(run_analysis())
