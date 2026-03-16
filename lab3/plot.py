"""Plot algorithm runtime vs number of machines n for Lab 3."""

import time
import argparse
import os
import matplotlib.pyplot as plt
import numpy as np

from matrix import build_payment_matrix
from brown import brown_method


def measure_runtime(n_values: list, c1: float, c2: float, c3: float,
                    epsilon: float, repeats: int = 3) -> list:
    """Measure average runtime of Brown's method for each n in n_values."""
    times = []
    for n in n_values:
        C = build_payment_matrix(n, c1, c2, c3)
        elapsed = []
        for _ in range(repeats):
            t0 = time.perf_counter()
            brown_method(C, epsilon)
            elapsed.append(time.perf_counter() - t0)
        times.append(min(elapsed))
        print(f"  n={n:3d}  t={times[-1]:.4f}s")
    return times


def main():
    parser = argparse.ArgumentParser(description="Plot Brown's method runtime vs n")
    parser.add_argument("-c1", type=float, default=1.0)
    parser.add_argument("-c2", type=float, default=4.0)
    parser.add_argument("-c3", type=float, default=5.0)
    parser.add_argument("-e", "--epsilon", type=float, default=0.01)
    parser.add_argument("--n-max", type=int, default=50, help="Max n value (default 50)")
    parser.add_argument("--n-min", type=int, default=2, help="Min n value (default 2)")
    parser.add_argument("--step", type=int, default=2, help="Step between n values (default 2)")
    parser.add_argument("--output", type=str, default="plots/runtime_vs_n.png")
    args = parser.parse_args()

    n_values = list(range(args.n_min, args.n_max + 1, args.step))
    print(f"Measuring runtime for n in [{args.n_min}, {args.n_max}] step={args.step}")
    print(f"Parameters: c1={args.c1}, c2={args.c2}, c3={args.c3}, ε={args.epsilon}\n")

    times = measure_runtime(n_values, args.c1, args.c2, args.c3, args.epsilon)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(n_values, times, marker="o", linewidth=1.5, markersize=4, color="#2563eb")
    ax.set_xlabel("Number of machines n", fontsize=12)
    ax.set_ylabel("Runtime (seconds)", fontsize=12)
    ax.set_title(
        f"Brown's method runtime vs n\n"
        f"(c1={args.c1}, c2={args.c2}, c3={args.c3}, ε={args.epsilon})",
        fontsize=12,
    )
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_xlim(n_values[0], n_values[-1])
    fig.tight_layout()
    fig.savefig(args.output, dpi=150)
    print(f"\nPlot saved to {args.output}")


if __name__ == "__main__":
    main()
