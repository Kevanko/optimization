"""Frequency-method formulas for mean time between failures (Θ) and
mean recovery time (T) of a distributed computing system with structural redundancy.

System parameters:
  N — total number of elementary machines (EM)
  n — number of EMs in the base (active) subsystem; n in [1, N]
  λ — failure rate of any EM  (1/hours)
  μ — recovery rate of one repair unit  (1/hours)
  m — number of repair units

Repair-rate function:
  μ_l = (N − l) · μ   if  (N − m) ≤ l ≤ N
  μ_l = m · μ         if  0 ≤ l < (N − m)

Formulas (frequency method):

  Θ = 1/(n·λ) + Σ_{j=n+1}^{N} [ 1/(j·λ) · Π_{l=n}^{j-1} μ_l/(l·λ) ]

  T = 1/μ_0 · Π_{l=1}^{n-1} (l·λ/μ_l)
    + Σ_{j=1}^{n-1} [ 1/(j·λ) · Π_{l=j}^{n-1} (l·λ/μ_l) ]   (n > 1)

  T = 1/μ_0                                                      (n = 1)

Both functions use O(max(N-n, n)) time with a single pass and log-space arithmetic
for Θ (avoids overflow) and an iterative product for T (handles underflow gracefully).
"""

import math


def _mu_l(l: int, N: int, m: int, mu: float) -> float:
    """Effective repair rate when l machines are currently failed."""
    if (N - m) <= l <= N:
        return (N - l) * mu
    return m * mu


def compute_theta(n: int, N: int, lam: float, mu: float, m: int) -> float:
    """Compute mean time between failures Θ.

    O(N - n) time. Uses log-space arithmetic to prevent overflow.
    """
    theta = 1.0 / (n * lam)

    # Incrementally build log_prod = log( Π_{l=n}^{j-1} μ_l / (l·λ) )
    log_prod = 0.0
    for j in range(n + 1, N + 1):
        mu_val = _mu_l(j - 1, N, m, mu)
        if mu_val == 0.0:
            break
        log_prod += math.log(mu_val) - math.log((j - 1) * lam)
        # term_j = exp(log_prod) / (j·λ)
        theta += math.exp(log_prod - math.log(j * lam))

    return theta


def compute_T(n: int, N: int, lam: float, mu: float, m: int) -> float:
    """Compute mean recovery time T.

    O(n) time using an iterative single-pass product.

    Key identity:  term_j = (1/(j·λ)) · Π_{l=j}^{n-1} (l·λ/μ_l)
                           = (1/μ_j) · Π_{l=j+1}^{n-1} (l·λ/μ_l)
                           = (1/μ_j) · P_{j+1}

    Iterate j from n-1 down to 1, maintaining P_{j+1}:
      T_sum  += P_{j+1} / μ_j
      P_j     = P_{j+1} · (j·λ / μ_j)

    After the loop P_1 = Π_{l=1}^{n-1} (l·λ/μ_l), needed for the first term.
    Underflow of P to 0 is harmless: those terms are negligible.
    """
    mu0 = _mu_l(0, N, m, mu)
    if mu0 == 0.0:
        return float("inf")

    if n == 1:
        return 1.0 / mu0

    T = 0.0
    P = 1.0   # P_{n} = empty product = 1

    for j in range(n - 1, 0, -1):
        mu_j = _mu_l(j, N, m, mu)
        if mu_j == 0.0:
            return float("inf")
        # term_j = P_{j+1} / μ_j
        T += P / mu_j
        # P_{j} = (j·λ / μ_j) · P_{j+1}
        P *= (j * lam) / mu_j

    # First term: 1/μ_0 · Π_{l=1}^{n-1} (l·λ/μ_l)  =  P_1 / μ_0
    T += P / mu0
    return T
