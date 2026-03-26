"""Frequency-method calculations for Lab 5.

Lab 5 studies a survivable distributed computing system and requires
components of the vectors:

  theta = {theta_n, theta_{n+1}, ..., theta_N}
  T     = {T_n,     T_{n+1},     ..., T_N}

For a fixed admissible number k of working machines, the component formulas
match the frequency-method formulas already used in Lab 4. Here k plays the
role of the current minimal acceptable number of healthy machines.
"""

from __future__ import annotations

import math


def _mu_l(l: int, N: int, m: int, mu: float) -> float:
    """Effective repair rate when l machines are currently failed."""
    if (N - m) <= l <= N:
        return (N - l) * mu
    return m * mu


def compute_theta_component(k: int, N: int, lam: float, mu: float, m: int) -> float:
    """Compute one component theta_k.

    The formula is the same frequency-method expression as in Lab 4,
    evaluated for the admissible threshold k.
    """
    theta = 1.0 / (k * lam)
    log_prod = 0.0

    for j in range(k + 1, N + 1):
        mu_val = _mu_l(j - 1, N, m, mu)
        if mu_val == 0.0:
            break
        log_prod += math.log(mu_val) - math.log((j - 1) * lam)
        theta += math.exp(log_prod - math.log(j * lam))

    return theta


def compute_T_component(k: int, N: int, lam: float, mu: float, m: int) -> float:
    """Compute one component T_k."""
    mu0 = _mu_l(0, N, m, mu)
    if mu0 == 0.0:
        return float("inf")

    if k == 1:
        return 1.0 / mu0

    total = 0.0
    prod = 1.0

    for j in range(k - 1, 0, -1):
        mu_j = _mu_l(j, N, m, mu)
        if mu_j == 0.0:
            return float("inf")
        total += prod / mu_j
        prod *= (j * lam) / mu_j

    total += prod / mu0
    return total


def compute_theta_vector(n_start: int, N: int, lam: float, mu: float, m: int) -> list[tuple[int, float]]:
    """Return [(k, theta_k), ...] for k in [n_start, N]."""
    return [
        (k, compute_theta_component(k, N, lam, mu, m))
        for k in range(n_start, N + 1)
    ]


def compute_T_vector(n_start: int, N: int, lam: float, mu: float, m: int) -> list[tuple[int, float]]:
    """Return [(k, T_k), ...] for k in [n_start, N]."""
    return [
        (k, compute_T_component(k, N, lam, mu, m))
        for k in range(n_start, N + 1)
    ]
