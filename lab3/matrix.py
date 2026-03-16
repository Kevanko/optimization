"""Payment matrix construction for the Dispatcher-VC game.

The VC (computing center) chooses how many machines to keep active (strategy i, 0..n).
The Dispatcher assigns i tasks to the system (strategy j, 0..n).

Cost formula derived from the model [Evreinov, Khoroshevsky, p.187]:
  c[i][j] = c2*(i-j) + c1*j  if i >= j  (i machines active, j tasks: j run at c1 each, i-j idle at c2 each)
  c[i][j] = c3*(j-i) + c2*i  if i < j   (i machines active, j tasks: i run at c2 each, j-i wait at c3 each)
"""

import numpy as np


def build_payment_matrix(n: int, c1: float, c2: float, c3: float) -> np.ndarray:
    """Build (n+1)x(n+1) payment matrix for the Dispatcher-VC game."""
    size = n + 1
    C = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            if i >= j:
                C[i][j] = c2 * (i - j) + c1 * j
            else:
                C[i][j] = c3 * (j - i) + c2 * i
    return C


def print_matrix(C: np.ndarray) -> None:
    for row in C:
        print("  " + "  ".join(f"{v:6.2f}" for v in row))
