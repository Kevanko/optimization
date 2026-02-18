#!/usr/bin/env python3
"""
Generate random task files for Lab 2.
Each line: r_j t_j (r_j in [1, n], t_j in [1, 100], uniform).
Usage: python3 generate_tasks.py <m> <n> [seed] > tasks.txt
"""
import sys
import random

def main():
    if len(sys.argv) < 3:
        print("Usage: generate_tasks.py <m> <n> [seed] > tasks.txt", file=sys.stderr)
        sys.exit(1)
    m = int(sys.argv[1])
    n = int(sys.argv[2])
    if len(sys.argv) >= 4:
        random.seed(int(sys.argv[3]))
    for _ in range(m):
        r = random.randint(1, n)
        t = random.randint(1, 100)
        print(r, t)

if __name__ == "__main__":
    main()
