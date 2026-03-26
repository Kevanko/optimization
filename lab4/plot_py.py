"""Matplotlib fallback for generating all 6 lab graphs.

Use this if gnuplot is not available:
  python3 plot_py.py

Produces the same PNG files in plots/ as the gnuplot scripts.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("plots", exist_ok=True)


def load(path):
    """Load a .dat file, skipping comment lines. Returns (n_col, *data_cols)."""
    data = np.loadtxt(path, comments="#")
    return data


def save(fig, path):
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {path}")


# ── 2.1: Θ(n) varying μ ────────────────────────────────────────────────────────
d = load("data/theta_mu.dat")
fig, ax = plt.subplots(figsize=(9, 5.5))
labels = ["μ = 1 1/ч", "μ = 10 1/ч", "μ = 100 1/ч", "μ = 1000 1/ч"]
markers = ["+", "x", "*", "s"]
for i, (lbl, mk) in enumerate(zip(labels, markers)):
    ax.semilogy(d[:, 0], d[:, i + 1], label=lbl, marker=mk, markersize=6, linewidth=1.2)
ax.set_title("Среднее время наработки до отказа (N = 65536, λ = 10⁻⁵ 1/ч, m = 1)")
ax.set_xlabel("Число машин n в основной подсистеме")
ax.set_ylabel("Среднее время до отказа (часы)")
ax.grid(True, which="both", linestyle="--", alpha=0.5)
ax.legend()
save(fig, "plots/theta_mu.png")

# ── 2.2: Θ(n) varying λ ────────────────────────────────────────────────────────
d = load("data/theta_lam.dat")
fig, ax = plt.subplots(figsize=(9, 5.5))
labels = ["λ = 10⁻⁵ 1/ч", "λ = 10⁻⁶ 1/ч", "λ = 10⁻⁷ 1/ч",
          "λ = 10⁻⁸ 1/ч", "λ = 10⁻⁹ 1/ч"]
markers = ["+", "x", "*", "s", "D"]
for i, (lbl, mk) in enumerate(zip(labels, markers)):
    ax.semilogy(d[:, 0], d[:, i + 1], label=lbl, marker=mk, markersize=6, linewidth=1.2)
ax.set_title("Среднее время наработки до отказа (N = 65536, μ = 1 1/ч, m = 1)")
ax.set_xlabel("Число машин n в основной подсистеме")
ax.set_ylabel("Среднее время до отказа (часы)")
ax.grid(True, which="both", linestyle="--", alpha=0.5)
ax.legend()
save(fig, "plots/theta_lam.png")

# ── 2.3: Θ(n) varying m ────────────────────────────────────────────────────────
d = load("data/theta_m.dat")
fig, ax = plt.subplots(figsize=(9, 5.5))
labels = ["m = 1", "m = 2", "m = 3", "m = 4"]
markers = ["+", "x", "*", "s"]
for i, (lbl, mk) in enumerate(zip(labels, markers)):
    ax.semilogy(d[:, 0], d[:, i + 1], label=lbl, marker=mk, markersize=6, linewidth=1.2)
ax.set_title("Среднее время наработки до отказа (N = 65536, λ = 10⁻⁵ 1/ч, μ = 1 1/ч)")
ax.set_xlabel("Число машин n в основной подсистеме")
ax.set_ylabel("Среднее время до отказа (часы)")
ax.grid(True, which="both", linestyle="--", alpha=0.5)
ax.legend()
save(fig, "plots/theta_m.png")

# ── 3.1: T(n) varying μ ────────────────────────────────────────────────────────
d = load("data/T_mu.dat")
fig, ax = plt.subplots(figsize=(9, 5.5))
labels = ["μ = 1 1/ч", "μ = 2 1/ч", "μ = 4 1/ч", "μ = 6 1/ч"]
markers = ["+", "x", "*", "s"]
for i, (lbl, mk) in enumerate(zip(labels, markers)):
    ax.semilogy(d[:, 0], d[:, i + 1], label=lbl, marker=mk, markersize=6, linewidth=1.2)
ax.set_title("Среднее время восстановления (N = 1000, λ = 10⁻³ 1/ч, m = 1)")
ax.set_xlabel("Число машин n в основной подсистеме")
ax.set_ylabel("Среднее время восстановления (часы)")
ax.grid(True, which="both", linestyle="--", alpha=0.5)
ax.legend()
save(fig, "plots/T_mu.png")

# ── 3.2: T(n) varying λ ────────────────────────────────────────────────────────
d = load("data/T_lam.dat")
fig, ax = plt.subplots(figsize=(9, 5.5))
labels = ["λ = 10⁻⁵ 1/ч", "λ = 10⁻⁶ 1/ч", "λ = 10⁻⁷ 1/ч",
          "λ = 10⁻⁸ 1/ч", "λ = 10⁻⁹ 1/ч"]
markers = ["+", "x", "*", "s", "D"]
for i, (lbl, mk) in enumerate(zip(labels, markers)):
    ax.plot(d[:, 0], d[:, i + 1], label=lbl, marker=mk, markersize=6, linewidth=1.2)
ax.set_title("Среднее время восстановления (N = 8192, μ = 1 1/ч, m = 1)")
ax.set_xlabel("Число машин n в основной подсистеме")
ax.set_ylabel("Среднее время восстановления (часы)")
ax.set_ylim(0.99, 1.20)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
save(fig, "plots/T_lam.png")

# ── 3.3: T(n) varying m ────────────────────────────────────────────────────────
d = load("data/T_m.dat")
fig, ax = plt.subplots(figsize=(9, 5.5))
labels = ["m = 1", "m = 2", "m = 3", "m = 4"]
markers = ["+", "x", "*", "s"]
for i, (lbl, mk) in enumerate(zip(labels, markers)):
    ax.plot(d[:, 0], d[:, i + 1], label=lbl, marker=mk, markersize=6, linewidth=1.2)
ax.set_title("Среднее время восстановления (N = 8192, λ = 10⁻⁵ 1/ч, μ = 1 1/ч)")
ax.set_xlabel("Число машин n в основной подсистеме")
ax.set_ylabel("Среднее время восстановления (часы)")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
save(fig, "plots/T_m.png")

print("\nAll plots saved to plots/")
