from __future__ import annotations

import math
from typing import Iterable, Sequence, Tuple

Task = Tuple[int, int]  # (r_j, t_j)


def get_lower_bound(tasks: Sequence[Task], n: int) -> float:
    """
    Lower bound for strip scheduling:
      T' = max(max_j t_j, (sum_j r_j * t_j) / n)
    """
    if not tasks:
        return 0.0
    if n <= 0:
        raise ValueError("n must be positive")

    max_height = max(t for _, t in tasks)
    area_bound = sum(r * t for r, t in tasks) / n
    return float(max(max_height, area_bound))


def get_epsilon(t_s: float, t_prime: float) -> float:
    """Relative error epsilon = (T(S) - T') / T'."""
    if t_prime <= 0:
        return 0.0
    return (t_s - t_prime) / t_prime


def get_stats(values: Iterable[float]) -> Tuple[float, float]:
    """Return mean and standard deviation (population)."""
    data = list(values)
    if not data:
        return 0.0, 0.0

    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return mean, math.sqrt(variance)
