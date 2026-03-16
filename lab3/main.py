"""Lab 3: Dispatcher-VC game theory solver.

Usage:
  python main.py -n 10 -c1 1 -c2 4 -c3 5 -e 0.01
  python main.py --input input.txt
  python main.py --input input.txt -e 0.01

Input file format (one value per line):
  n
  c1
  c2
  c3

Constraints:
  c1 in {1, 2, 3}
  c2, c3 in {4, 5, 6}
  c1 < max(c2, c3)
"""

import argparse
import sys

from matrix import build_payment_matrix, print_matrix
from brown import brown_method


def parse_args():
    parser = argparse.ArgumentParser(description="Dispatcher-VC game solver (Brown's method)")
    parser.add_argument("--input", type=str, default=None, help="Path to input file")
    parser.add_argument("-n", type=int, default=None, help="Number of machines")
    parser.add_argument("-c1", type=float, default=None, help="Cost c1")
    parser.add_argument("-c2", type=float, default=None, help="Cost c2")
    parser.add_argument("-c3", type=float, default=None, help="Cost c3")
    parser.add_argument("-e", "--epsilon", type=float, default=0.01, help="Convergence threshold (default 0.01)")
    return parser.parse_args()


def load_from_file(path: str):
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    if len(lines) < 4:
        sys.exit(f"Input file must contain 4 values: n, c1, c2, c3. Got {len(lines)}.")
    return int(lines[0]), float(lines[1]), float(lines[2]), float(lines[3])


def validate(n, c1, c2, c3):
    if n < 1:
        sys.exit("n must be >= 1")
    if c1 not in {1.0, 2.0, 3.0}:
        print(f"Warning: c1={c1} is outside the recommended set {{1, 2, 3}}")
    if c2 not in {4.0, 5.0, 6.0} or c3 not in {4.0, 5.0, 6.0}:
        print(f"Warning: c2={c2}, c3={c3} should be in {{4, 5, 6}} for the actual lab")
    if c1 >= max(c2, c3):
        print(f"Warning: constraint c1 < max(c2, c3) violated (c1={c1}, max={max(c2,c3)})")


def main():
    args = parse_args()

    if args.input:
        n, c1, c2, c3 = load_from_file(args.input)
    elif all(v is not None for v in [args.n, args.c1, args.c2, args.c3]):
        n, c1, c2, c3 = args.n, args.c1, args.c2, args.c3
    else:
        sys.exit("Provide either --input file or all of -n, -c1, -c2, -c3")

    epsilon = args.epsilon
    validate(n, c1, c2, c3)

    print(f"n = {n},  c1 = {c1},  c2 = {c2},  c3 = {c3},  ε = {epsilon}\n")

    C = build_payment_matrix(n, c1, c2, c3)
    print("Payment matrix C:")
    print_matrix(C)

    result = brown_method(C, epsilon)

    strat_vc = result["strategy_vc"]
    strat_dp = result["strategy_dp"]
    alpha = result["alpha"]
    beta = result["beta"]
    approx_value = (alpha + beta) / 2

    print(f"\nNumber of iterations l = {result['iterations']}")
    print(f"Game value V = {result['game_value']:.3f}  "
          f"(convergence gap β−α; approximate payoff ≈ {approx_value:.3f})")

    print("\nOptimal mixed strategies (VC):")
    print("  " + "  ".join(f"{v:.2f}" for v in strat_vc))

    print("\nOptimal mixed strategies (Dispatcher):")
    print("  " + "  ".join(f"{v:.2f}" for v in strat_dp))

    print("\n--- Interpretation ---")
    dominant_vc = int(strat_vc.argmax())
    dominant_dp = int(strat_dp.argmax())
    print(f"VC should most often keep {dominant_vc} machine(s) active "
          f"(strategy {dominant_vc}, weight {strat_vc[dominant_vc]:.2f}).")
    print(f"Dispatcher should most often assign {dominant_dp} task(s) "
          f"(strategy {dominant_dp}, weight {strat_dp[dominant_dp]:.2f}).")
    print(f"Approximate equilibrium payoff ≈ {approx_value:.3f}.")


if __name__ == "__main__":
    main()
