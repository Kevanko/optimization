"""Brown's iterative method (fictitious play) for solving matrix games.

Reference: Evreinov, Khoroshevsky, p.192.

Both players alternate best responses:
  - Player 1 (VC, maximizer): picks the row with the highest cumulative column score.
  - Player 2 (Dispatcher, minimizer): picks the column with the lowest cumulative row score.

Convergence criterion: beta - alpha < epsilon, where
  alpha = min_j row_score[j] / l1   — lower bound on game value (Player 1's guarantee)
  beta  = max_i col_score[i] / l2   — upper bound on game value (Player 2's best-response limit)

l1 = number of rows chosen by Player 1 (starts with one extra initial move)
l2 = number of columns chosen by Player 2 (= total loop iterations)

The approximate game value is taken as (alpha + beta) / 2, while
beta - alpha is the residual convergence gap of the iterative process.
"""

import numpy as np


def brown_method(C: np.ndarray, epsilon: float) -> dict:
    """Run Brown's iterative method on payment matrix C.

    Returns a dict with keys:
      iterations            — total loop iteration count (= l2 = col_counts.sum())
      approx_game_value     — midpoint (alpha + beta) / 2
      convergence_gap       — residual gap (beta - alpha) at convergence
      strategy_vc           — optimal mixed strategy for Player 1 (VC), shape (n+1,)
      strategy_dp           — optimal mixed strategy for Player 2 (Dispatcher), shape (n+1,)
    """
    n = C.shape[0]

    row_counts = np.zeros(n, dtype=np.int64)
    col_counts = np.zeros(n, dtype=np.int64)

    # row_score[j] = sum of C[chosen_row][j] over all Player 1's moves
    # col_score[i] = sum of C[i][chosen_col] over all Player 2's moves
    row_score = np.zeros(n)
    col_score = np.zeros(n)

    # Player 1 makes the initial move (arbitrary: row 0)
    i_cur = 0
    row_counts[i_cur] += 1
    row_score += C[i_cur, :]
    l1 = 1
    l2 = 0

    while True:
        # Player 2 (minimizer): pick column that minimises cumulative row score
        j_cur = int(np.argmin(row_score))
        col_counts[j_cur] += 1
        col_score += C[:, j_cur]
        l2 += 1

        # Player 1 (maximizer): pick row that maximises cumulative column score
        i_cur = int(np.argmax(col_score))
        row_counts[i_cur] += 1
        row_score += C[i_cur, :]
        l1 += 1

        # Separate denominators: Player 1 made l1 moves, Player 2 made l2 moves
        alpha = np.min(row_score) / l1   # lower bound on game value
        beta = np.max(col_score) / l2    # upper bound on game value

        if beta - alpha < epsilon:
            break

    convergence_gap = beta - alpha
    approx_game_value = (alpha + beta) / 2

    strategy_vc = row_counts / row_counts.sum()
    strategy_dp = col_counts / col_counts.sum()

    return {
        "iterations": l2,
        "approx_game_value": approx_game_value,
        "convergence_gap": convergence_gap,
        "strategy_vc": strategy_vc,
        "strategy_dp": strategy_dp,
        "alpha": alpha,
        "beta": beta,
    }
