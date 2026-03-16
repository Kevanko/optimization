"""Lab 4: Generate data files for gnuplot graphs of Θ(n) and T(n).

All 6 datasets from the task are generated and written to data/*.dat files.
Each .dat file has two columns: n  value
Multiple series are written to the same file separated by blank lines (gnuplot index blocks),
or as separate columns depending on the gnuplot script requirements.

For gnuplot compatibility, each series is a separate file:
  data/theta_mu.dat      — 2.1: Θ(n) for μ ∈ {1, 10, 100, 1000}
  data/theta_lam.dat     — 2.2: Θ(n) for λ ∈ {1e-5..1e-9}
  data/theta_m.dat       — 2.3: Θ(n) for m ∈ {1, 2, 3, 4}
  data/T_mu.dat          — 3.1: T(n) for μ ∈ {1, 2, 4, 6}
  data/T_lam.dat         — 3.2: T(n) for λ ∈ {1e-5..1e-9}
  data/T_m.dat           — 3.3: T(n) for m ∈ {1, 2, 3, 4}

Within each file, columns are: n  series1  series2  ...
"""

import os
import sys
from compute import compute_theta, compute_T


def write_dat(path: str, n_range: range, columns: list, header: str = ""):
    """Write a .dat file with columns [n, col1, col2, ...].

    columns is a list of (label, list_of_values) pairs.
    """
    col_labels = "  ".join(c[0] for c in columns)
    with open(path, "w") as f:
        if header:
            f.write(f"# {header}\n")
        f.write(f"# n  {col_labels}\n")
        ns = list(n_range)
        for idx, n in enumerate(ns):
            vals = "  ".join(f"{c[1][idx]:.6e}" for c in columns)
            f.write(f"{n}  {vals}\n")
    print(f"  Written: {path}  ({len(ns)} rows, {len(columns)} series)")


def compute_series(n_range, func, **kwargs):
    """Compute a series of values for each n."""
    return [func(**{**kwargs, "n": n}) for n in n_range]


def main():
    os.makedirs("data", exist_ok=True)

    # ── 2.1: Θ(n), N=65536, λ=1e-5, m=1, μ ∈ {1, 10, 100, 1000} ──────────────
    print("2.1 Θ(n) varying μ ...")
    N, lam, m_val = 65536, 1e-5, 1
    n_range = range(N - 9, N + 1)   # 65527..65536
    mus = [1, 10, 100, 1000]
    cols = [(f"mu={mu}", compute_series(n_range, compute_theta, N=N, lam=lam, mu=mu, m=m_val))
            for mu in mus]
    write_dat("data/theta_mu.dat", n_range, cols,
              f"Theta(n), N={N}, lambda={lam}, m={m_val}")

    # ── 2.2: Θ(n), N=65536, μ=1, m=1, λ ∈ {1e-5..1e-9} ────────────────────────
    print("2.2 Θ(n) varying λ ...")
    mu_val = 1.0
    lams = [1e-5, 1e-6, 1e-7, 1e-8, 1e-9]
    cols = [(f"lam={lam}", compute_series(n_range, compute_theta, N=N, lam=lam, mu=mu_val, m=m_val))
            for lam in lams]
    write_dat("data/theta_lam.dat", n_range, cols,
              f"Theta(n), N={N}, mu={mu_val}, m={m_val}")

    # ── 2.3: Θ(n), N=65536, μ=1, λ=1e-5, m ∈ {1,2,3,4} ────────────────────────
    print("2.3 Θ(n) varying m ...")
    lam_fix = 1e-5
    ms = [1, 2, 3, 4]
    cols = [(f"m={m}", compute_series(n_range, compute_theta, N=N, lam=lam_fix, mu=mu_val, m=m))
            for m in ms]
    write_dat("data/theta_m.dat", n_range, cols,
              f"Theta(n), N={N}, lambda={lam_fix}, mu={mu_val}")

    # ── 3.1: T(n), N=1000, λ=1e-3, m=1, μ ∈ {1,2,4,6} ─────────────────────────
    print("3.1 T(n) varying μ ...")
    N2, lam2, m2 = 1000, 1e-3, 1
    n_range2 = range(900, N2 + 1, 10)   # 900, 910, ..., 1000
    mus2 = [1, 2, 4, 6]
    cols = [(f"mu={mu}", compute_series(n_range2, compute_T, N=N2, lam=lam2, mu=mu, m=m2))
            for mu in mus2]
    write_dat("data/T_mu.dat", n_range2, cols,
              f"T(n), N={N2}, lambda={lam2}, m={m2}")

    # ── 3.2: T(n), N=8192, μ=1, m=1, λ ∈ {1e-5..1e-9} ─────────────────────────
    print("3.2 T(n) varying λ ...")
    N3, mu3, m3 = 8192, 1.0, 1
    n_range3 = range(N3 - 100, N3 + 1, 10)   # 8092, 8102, ..., 8192
    lams3 = [1e-5, 1e-6, 1e-7, 1e-8, 1e-9]
    cols = [(f"lam={lam}", compute_series(n_range3, compute_T, N=N3, lam=lam, mu=mu3, m=m3))
            for lam in lams3]
    write_dat("data/T_lam.dat", n_range3, cols,
              f"T(n), N={N3}, mu={mu3}, m={m3}")

    # ── 3.3: T(n), N=8192, μ=1, λ=1e-5, m ∈ {1,2,3,4} ─────────────────────────
    print("3.3 T(n) varying m ...")
    lam3_fix = 1e-5
    ms3 = [1, 2, 3, 4]
    cols = [(f"m={m}", compute_series(n_range3, compute_T, N=N3, lam=lam3_fix, mu=mu3, m=m))
            for m in ms3]
    write_dat("data/T_m.dat", n_range3, cols,
              f"T(n), N={N3}, lambda={lam3_fix}, mu={mu3}")

    print("\nAll data files written to data/")


if __name__ == "__main__":
    main()
