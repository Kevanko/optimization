from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence

import matplotlib.pyplot as plt


def _ensure_graphs_dir(graphs_dir: str = "graphs") -> Path:
    path = Path(graphs_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def plot_time_complexity(
    m_values: Sequence[int],
    series: Mapping[str, Sequence[float]],
    *,
    graphs_dir: str = "graphs",
    filename: str = "time_complexity.png",
) -> None:
    out_dir = _ensure_graphs_dir(graphs_dir)
    plt.figure(figsize=(9, 5))
    markers = ["o", "s", "^", "d", "x", "*"]
    for idx, (label, values) in enumerate(series.items()):
        plt.plot(m_values, values, marker=markers[idx % len(markers)], label=label)
    plt.xlabel("m (number of tasks)")
    plt.ylabel("Runtime, seconds")
    plt.title("Time Complexity: NFDH vs FFDH for Different n")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / filename, dpi=150)
    plt.close()


def plot_accuracy(
    m_values: Sequence[int],
    nfdh_mean: Sequence[float],
    nfdh_std: Sequence[float],
    ffdh_mean: Sequence[float],
    ffdh_std: Sequence[float],
    *,
    graphs_dir: str = "graphs",
    filename: str = "stats.png",
    title: str = "Epsilon Statistics",
) -> None:
    out_dir = _ensure_graphs_dir(graphs_dir)

    plt.figure(figsize=(9, 5))
    plt.errorbar(m_values, nfdh_mean, yerr=nfdh_std, marker="o", capsize=4, label="NFDH")
    plt.errorbar(m_values, ffdh_mean, yerr=ffdh_std, marker="s", capsize=4, label="FFDH")
    plt.xlabel("m (number of tasks)")
    plt.ylabel("epsilon")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / filename, dpi=150)
    plt.close()
