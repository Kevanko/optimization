#!/usr/bin/env bash
# Lab 2: run NFDH/FFDH on generated sets; output CSV for timing and epsilon.
# Usage: ./run_experiments.sh [n]  # n = 1024 or 4096 (default 1024)

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
BIN="./schedule"
N="${1:-1024}"
mkdir -p results data

# Generate if missing
if [[ ! -f data/tasks_500_n1024.txt ]]; then
    echo "Generating task sets..."
    make generate
fi

# Timing: m=500..5000, 10 sets, n=1024 and n=4096
run_timing() {
    local n=$1
    local out="results/time_n${n}.csv"
    echo "m,n,alg,time_sec" > "$out"
    for m in 500 1000 1500 2000 2500 3000 3500 4000 4500 5000; do
        local f="data/tasks_${m}_n${n}.txt"
        [[ -f "$f" ]] || continue
        for alg in NFDH FFDH; do
            local t
            t=$("$BIN" "$f" "$n" "$alg" 2>/dev/null | awk -F= '/^time=/ {print $2}')
            [[ -n "$t" ]] && echo "${m},${n},${alg},${t}" >> "$out"
        done
    done
    echo "Wrote $out"
}

# Epsilon (quality): m=500..5000, n=1024, 10 sets
run_epsilon() {
    local out="results/epsilon_n1024.csv"
    echo "m,n,alg,epsilon" > "$out"
    for m in 500 1000 1500 2000 2500 3000 3500 4000 4500 5000; do
        local f="data/tasks_${m}_n1024.txt"
        [[ -f "$f" ]] || continue
        for alg in NFDH FFDH; do
            local eps
            eps=$("$BIN" "$f" 1024 "$alg" 2>/dev/null | awk -F= '/^epsilon=/ {print $2}')
            [[ -n "$eps" ]] && echo "${m},1024,${alg},${eps}" >> "$out"
        done
    done
    echo "Wrote $out"
}

[[ -x "$BIN" ]] || make
run_timing 1024
run_timing 4096
run_epsilon
echo "Done. Results in results/"
