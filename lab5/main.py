"""Lab 5: generate vectors, tables and graph datasets for survivable systems."""

from __future__ import annotations

import csv
import os

from compute import (
    compute_T_component,
    compute_T_vector,
    compute_theta_component,
    compute_theta_vector,
)

N = 65536
LAMBDAS = [1e-6, 1e-7, 1e-5]
MUS = [1, 10, 100, 1000]
MS = [1, 2, 3]
N_START_VALUES = list(range(N - 9, N + 1))  # 65527..65536
GRAPH_N_START = N - 9
GRAPH_K_VALUES = list(range(GRAPH_N_START, N + 1))


def ensure_dirs() -> None:
    os.makedirs("data", exist_ok=True)


def write_vectors_csv(path: str) -> None:
    """Write the full normalized table of vector components."""
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["lambda", "mu", "m", "n_start", "k", "theta_k", "T_k"])
        for lam in LAMBDAS:
            for mu in MUS:
                for m in MS:
                    for n_start in N_START_VALUES:
                        theta_vec = dict(compute_theta_vector(n_start, N, lam, mu, m))
                        T_vec = dict(compute_T_vector(n_start, N, lam, mu, m))
                        for k in range(n_start, N + 1):
                            writer.writerow([
                                f"{lam:.0e}",
                                mu,
                                m,
                                n_start,
                                k,
                                f"{theta_vec[k]:.6e}",
                                f"{T_vec[k]:.6e}",
                            ])
    print(f"  Written: {path}")


def write_dat(path: str, k_values: list[int], columns: list[tuple[str, list[float]]], header: str = "") -> None:
    """Write graph data with columns [k, series1, series2, ...]."""
    labels = "  ".join(label for label, _ in columns)
    with open(path, "w") as f:
        if header:
            f.write(f"# {header}\n")
        f.write(f"# k  {labels}\n")
        for idx, k in enumerate(k_values):
            values = "  ".join(f"{series[idx]:.6e}" for _, series in columns)
            f.write(f"{k}  {values}\n")
    print(f"  Written: {path}  ({len(k_values)} rows, {len(columns)} series)")


def component_series_theta(k_values: list[int], *, lam: float, mu: float, m: int) -> list[float]:
    return [compute_theta_component(k, N, lam, mu, m) for k in k_values]


def component_series_T(k_values: list[int], *, lam: float, mu: float, m: int) -> list[float]:
    return [compute_T_component(k, N, lam, mu, m) for k in k_values]


def main() -> None:
    ensure_dirs()

    print("Writing full vectors table ...")
    write_vectors_csv("data/vectors.csv")

    print("Preparing graph datasets ...")

    theta_mu_cols = [
        (f"mu={mu}", component_series_theta(GRAPH_K_VALUES, lam=1e-5, mu=mu, m=1))
        for mu in MUS
    ]
    write_dat(
        "data/theta_mu.dat",
        GRAPH_K_VALUES,
        theta_mu_cols,
        f"theta_k, N={N}, lambda=1e-5, m=1, n_start={GRAPH_N_START}",
    )

    theta_lam_cols = [
        (f"lam={lam}", component_series_theta(GRAPH_K_VALUES, lam=lam, mu=1.0, m=1))
        for lam in [1e-5, 1e-6, 1e-7]
    ]
    write_dat(
        "data/theta_lam.dat",
        GRAPH_K_VALUES,
        theta_lam_cols,
        f"theta_k, N={N}, mu=1, m=1, n_start={GRAPH_N_START}",
    )

    theta_m_cols = [
        (f"m={m}", component_series_theta(GRAPH_K_VALUES, lam=1e-5, mu=1.0, m=m))
        for m in MS
    ]
    write_dat(
        "data/theta_m.dat",
        GRAPH_K_VALUES,
        theta_m_cols,
        f"theta_k, N={N}, lambda=1e-5, mu=1, n_start={GRAPH_N_START}",
    )

    T_mu_cols = [
        (f"mu={mu}", component_series_T(GRAPH_K_VALUES, lam=1e-5, mu=mu, m=1))
        for mu in MUS
    ]
    write_dat(
        "data/T_mu.dat",
        GRAPH_K_VALUES,
        T_mu_cols,
        f"T_k, N={N}, lambda=1e-5, m=1, n_start={GRAPH_N_START}",
    )

    T_lam_cols = [
        (f"lam={lam}", component_series_T(GRAPH_K_VALUES, lam=lam, mu=1.0, m=1))
        for lam in [1e-5, 1e-6, 1e-7]
    ]
    write_dat(
        "data/T_lam.dat",
        GRAPH_K_VALUES,
        T_lam_cols,
        f"T_k, N={N}, mu=1, m=1, n_start={GRAPH_N_START}",
    )

    T_m_cols = [
        (f"m={m}", component_series_T(GRAPH_K_VALUES, lam=1e-5, mu=1.0, m=m))
        for m in MS
    ]
    write_dat(
        "data/T_m.dat",
        GRAPH_K_VALUES,
        T_m_cols,
        f"T_k, N={N}, lambda=1e-5, mu=1, n_start={GRAPH_N_START}",
    )

    print("\nAll Lab 5 datasets written to data/")


if __name__ == "__main__":
    main()
