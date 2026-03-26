"""Matplotlib fallback for all 6 Lab 5 graphs."""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("plots", exist_ok=True)


def load(path):
    return np.loadtxt(path, comments="#")


def save(fig, path):
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {path}")


d = load("data/theta_mu.dat")
fig, ax = plt.subplots(figsize=(9, 5.5))
labels = ["μ = 1 1/ч", "μ = 10 1/ч", "μ = 100 1/ч", "μ = 1000 1/ч"]
markers = ["+", "x", "*", "s"]
for i, (lbl, mk) in enumerate(zip(labels, markers)):
    ax.semilogy(d[:, 0], d[:, i + 1], label=lbl, marker=mk, markersize=6, linewidth=1.2)
ax.set_title("Компоненты вектора θ_k (N = 65536, λ = 10⁻⁵ 1/ч, m = 1)")
ax.set_xlabel("Число работоспособных машин k")
ax.set_ylabel("θ_k (часы)")
ax.grid(True, which="both", linestyle="--", alpha=0.5)
ax.legend()
save(fig, "plots/theta_mu.png")

d = load("data/theta_lam.dat")
fig, ax = plt.subplots(figsize=(9, 5.5))
labels = ["λ = 10⁻⁵ 1/ч", "λ = 10⁻⁶ 1/ч", "λ = 10⁻⁷ 1/ч"]
markers = ["+", "x", "*"]
for i, (lbl, mk) in enumerate(zip(labels, markers)):
    ax.semilogy(d[:, 0], d[:, i + 1], label=lbl, marker=mk, markersize=6, linewidth=1.2)
ax.set_title("Компоненты вектора θ_k (N = 65536, μ = 1 1/ч, m = 1)")
ax.set_xlabel("Число работоспособных машин k")
ax.set_ylabel("θ_k (часы)")
ax.grid(True, which="both", linestyle="--", alpha=0.5)
ax.legend()
save(fig, "plots/theta_lam.png")

d = load("data/theta_m.dat")
fig, ax = plt.subplots(figsize=(9, 5.5))
labels = ["m = 1", "m = 2", "m = 3"]
markers = ["+", "x", "*"]
for i, (lbl, mk) in enumerate(zip(labels, markers)):
    ax.semilogy(d[:, 0], d[:, i + 1], label=lbl, marker=mk, markersize=6, linewidth=1.2)
ax.set_title("Компоненты вектора θ_k (N = 65536, λ = 10⁻⁵ 1/ч, μ = 1 1/ч)")
ax.set_xlabel("Число работоспособных машин k")
ax.set_ylabel("θ_k (часы)")
ax.grid(True, which="both", linestyle="--", alpha=0.5)
ax.legend()
save(fig, "plots/theta_m.png")

d = load("data/T_mu.dat")
fig, ax = plt.subplots(figsize=(9, 5.5))
labels = ["μ = 1 1/ч", "μ = 10 1/ч", "μ = 100 1/ч", "μ = 1000 1/ч"]
markers = ["+", "x", "*", "s"]
for i, (lbl, mk) in enumerate(zip(labels, markers)):
    ax.semilogy(d[:, 0], d[:, i + 1], label=lbl, marker=mk, markersize=6, linewidth=1.2)
ax.set_title("Компоненты вектора T_k (N = 65536, λ = 10⁻⁵ 1/ч, m = 1)")
ax.set_xlabel("Число работоспособных машин k")
ax.set_ylabel("T_k (часы)")
ax.grid(True, which="both", linestyle="--", alpha=0.5)
ax.legend()
save(fig, "plots/T_mu.png")

d = load("data/T_lam.dat")
fig, ax = plt.subplots(figsize=(9, 5.5))
labels = ["λ = 10⁻⁵ 1/ч", "λ = 10⁻⁶ 1/ч", "λ = 10⁻⁷ 1/ч"]
markers = ["+", "x", "*"]
for i, (lbl, mk) in enumerate(zip(labels, markers)):
    ax.plot(d[:, 0], d[:, i + 1], label=lbl, marker=mk, markersize=6, linewidth=1.2)
ax.set_title("Компоненты вектора T_k (N = 65536, μ = 1 1/ч, m = 1)")
ax.set_xlabel("Число работоспособных машин k")
ax.set_ylabel("T_k (часы)")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
save(fig, "plots/T_lam.png")

d = load("data/T_m.dat")
fig, ax = plt.subplots(figsize=(9, 5.5))
labels = ["m = 1", "m = 2", "m = 3"]
markers = ["+", "x", "*"]
for i, (lbl, mk) in enumerate(zip(labels, markers)):
    ax.plot(d[:, 0], d[:, i + 1], label=lbl, marker=mk, markersize=6, linewidth=1.2)
ax.set_title("Компоненты вектора T_k (N = 65536, λ = 10⁻⁵ 1/ч, μ = 1 1/ч)")
ax.set_xlabel("Число работоспособных машин k")
ax.set_ylabel("T_k (часы)")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
save(fig, "plots/T_m.png")

print("\nAll Lab 5 plots saved to plots/")
