#!/usr/bin/env python3
"""
Plot t(m) and bandwidth m/t from lab1 results.
Reads CSV from results/ (format: level,m_bytes,t_sec) and saves plots to plots/.
Usage: python3 plot_results.py [cluster]   # cluster: pine | oak | all (default: pine)
  all — строит графики по каждому кластеру и сводные сравнения Pine vs OAK.
"""

import csv
import sys
from pathlib import Path

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except ImportError:
    sys.exit("Install matplotlib: pip install matplotlib")

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = SCRIPT_DIR / "results"
PLOTS_DIR = SCRIPT_DIR / "plots"

# Подписи по заданию: три уровня коммуникационной среды
LEVEL_LABELS = {
    "memory": "Оперативная память узла (NUMA/SMP)",
    "qpi": "Шина Intel QPI (между процессорами NUMA-узла)",
    "network": "Сеть между ЭМ (InfiniBand QDR / Gigabit Ethernet)",
}

LEVEL_LABELS_EN = {
    "memory": "Memory (same node)",
    "qpi": "QPI (2 sockets)",
    "network": "Network (between nodes)",
}


def load_results(cluster: str):
    """Load all level CSVs for cluster into {level: [(m_bytes, t_sec), ...]}."""
    data = {}
    for level in ("memory", "qpi", "network"):
        p = RESULTS_DIR / f"{cluster}_{level}.csv"
        if not p.exists():
            continue
        points = []
        with open(p) as f:
            r = csv.DictReader(f)
            for row in r:
                try:
                    m = int(row["m_bytes"])
                    t = float(row["t_sec"])
                    points.append((m, t))
                except (KeyError, ValueError):
                    continue
        if points:
            data[level] = sorted(points)
    return data


def plot_t_vs_m(data: dict, cluster: str, lang: str = "ru"):
    """График зависимости t(m) — время передачи сообщения размером m байт (п.3 задания)."""
    labels = LEVEL_LABELS if lang == "ru" else LEVEL_LABELS_EN
    fig, ax = plt.subplots()
    for level, points in data.items():
        if not points:
            continue
        m_vals = [p[0] for p in points]
        t_vals = [p[1] for p in points]
        ax.plot(m_vals, t_vals, "o-", label=labels.get(level, level))
    ax.set_xlabel("m, байт" if lang == "ru" else "Message size (bytes)")
    ax.set_ylabel("t, с" if lang == "ru" else "Time (s)")
    ax.set_title("Зависимость времени передачи t от размера сообщения m" if lang == "ru" else f"Transfer time t(m) — {cluster.upper()} cluster")
    ax.legend()
    ax.grid(True, alpha=0.3)
    if max(m for points in data.values() for m, _ in points) > 1e6:
        ax.set_xscale("log")
    fig.tight_layout()
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        out = PLOTS_DIR / f"t_vs_m_{cluster}.{ext}"
        fig.savefig(out)
        print(f"Saved {out}")
    plt.close()


def plot_bandwidth(data: dict, cluster: str, lang: str = "ru"):
    """Пропускная способность (МБ/с) от размера сообщения m."""
    labels = LEVEL_LABELS if lang == "ru" else LEVEL_LABELS_EN
    fig, ax = plt.subplots()
    for level, points in data.items():
        if not points:
            continue
        m_vals = [p[0] for p in points]
        bw_mbs = [p[0] / (1024 * 1024) / p[1] if p[1] > 0 else 0 for p in points]
        ax.plot(m_vals, bw_mbs, "o-", label=labels.get(level, level))
    ax.set_xlabel("m, байт" if lang == "ru" else "Message size (bytes)")
    ax.set_ylabel("МБ/с" if lang == "ru" else "Bandwidth (MB/s)")
    ax.set_title("Пропускная способность от размера сообщения m" if lang == "ru" else f"Bandwidth vs message size — {cluster.upper()}")
    ax.legend()
    ax.grid(True, alpha=0.3)
    if max(m for points in data.values() for m, _ in points) > 1e6:
        ax.set_xscale("log")
    fig.tight_layout()
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        out = PLOTS_DIR / f"bandwidth_vs_m_{cluster}.{ext}"
        fig.savefig(out)
        print(f"Saved {out}")
    plt.close()


def plot_t_vs_m_comparison(clusters_data: dict, lang: str = "ru"):
    """Сводный график t(m): Pine и OAK на одних осях (по уровням)."""
    labels = LEVEL_LABELS if lang == "ru" else LEVEL_LABELS_EN
    fig, ax = plt.subplots()
    for cluster, data in clusters_data.items():
        for level, points in data.items():
            if not points:
                continue
            m_vals = [p[0] for p in points]
            t_vals = [p[1] for p in points]
            ax.plot(m_vals, t_vals, "o-", label=f"{cluster.upper()} — {labels.get(level, level)}")
    ax.set_xlabel("m, байт" if lang == "ru" else "Message size (bytes)")
    ax.set_ylabel("t, с" if lang == "ru" else "Time (s)")
    ax.set_title("Время передачи t(m): сравнение Pine и OAK" if lang == "ru" else "Transfer time t(m) — Pine vs OAK")
    ax.legend()
    ax.grid(True, alpha=0.3)
    all_m = [m for data in clusters_data.values() for points in data.values() for m, _ in points]
    if all_m and max(all_m) > 1e6:
        ax.set_xscale("log")
    fig.tight_layout()
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        out = PLOTS_DIR / "t_vs_m_pine_vs_oak." + ext
        fig.savefig(out)
        print(f"Saved {out}")
    plt.close()


def plot_bandwidth_comparison(clusters_data: dict, lang: str = "ru"):
    """Сводный график пропускной способности: Pine и OAK на одних осях."""
    labels = LEVEL_LABELS if lang == "ru" else LEVEL_LABELS_EN
    fig, ax = plt.subplots()
    for cluster, data in clusters_data.items():
        for level, points in data.items():
            if not points:
                continue
            m_vals = [p[0] for p in points]
            bw_mbs = [p[0] / (1024 * 1024) / p[1] if p[1] > 0 else 0 for p in points]
            ax.plot(m_vals, bw_mbs, "o-", label=f"{cluster.upper()} — {labels.get(level, level)}")
    ax.set_xlabel("m, байт" if lang == "ru" else "Message size (bytes)")
    ax.set_ylabel("МБ/с" if lang == "ru" else "Bandwidth (MB/s)")
    ax.set_title("Пропускная способность: сравнение Pine и OAK" if lang == "ru" else "Bandwidth — Pine vs OAK")
    ax.legend()
    ax.grid(True, alpha=0.3)
    all_m = [m for data in clusters_data.values() for points in data.values() for m, _ in points]
    if all_m and max(all_m) > 1e6:
        ax.set_xscale("log")
    fig.tight_layout()
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        out = PLOTS_DIR / "bandwidth_vs_m_pine_vs_oak." + ext
        fig.savefig(out)
        print(f"Saved {out}")
    plt.close()


def main():
    cluster = sys.argv[1] if len(sys.argv) > 1 else "pine"
    if cluster == "all":
        clusters_data = {}
        for c in ("pine", "oak"):
            d = load_results(c)
            if d:
                clusters_data[c] = d
                plot_t_vs_m(d, c, lang="ru")
                plot_bandwidth(d, c, lang="ru")
        if len(clusters_data) >= 2:
            plot_t_vs_m_comparison(clusters_data, lang="ru")
            plot_bandwidth_comparison(clusters_data, lang="ru")
        elif not clusters_data:
            print(f"No results in {RESULTS_DIR}. Run sbatch task_pine.job and/or task_oak.job on clusters.")
            sys.exit(1)
        return
    data = load_results(cluster)
    if not data:
        print(f"No results found in {RESULTS_DIR} for cluster '{cluster}'")
        print("Run sbatch task_pine.job (on Pine) and/or task_oak.job (on OAK), then copy results/.")
        sys.exit(1)
    plot_t_vs_m(data, cluster, lang="ru")
    plot_bandwidth(data, cluster, lang="ru")


if __name__ == "__main__":
    main()
