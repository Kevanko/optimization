#!/usr/bin/env bash
# П.4: сравнительный анализ на наборах в стиле протоколов (m=500, 1000, 1500), n=1024.
# Создаёт data/workload_500.txt, workload_1000.txt, workload_1500.txt (синтетика или из лога)
# и пишет results/epsilon_workload.csv.

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
BIN="./schedule"
N=1024
mkdir -p results data

# Синтетические наборы в стиле нагрузок (если нет реальных логов LLNL)
if [[ ! -f data/workload_500.txt ]]; then
    echo "Generating workload-style sets (m=500,1000,1500)..."
    for m in 500 1000 1500; do
        python3 workload_to_tasks.py --synthetic $m $N $m > "data/workload_${m}.txt"
    done
fi

OUT="results/epsilon_workload.csv"
echo "m,n,alg,epsilon" > "$OUT"
for m in 500 1000 1500; do
    f="data/workload_${m}.txt"
    [[ -f "$f" ]] || continue
    for alg in NFDH FFDH; do
        eps=$("$BIN" "$f" "$N" "$alg" 2>/dev/null | awk -F= '/^epsilon=/ {print $2}')
        [[ -n "$eps" ]] && echo "${m},${N},${alg},${eps}" >> "$OUT"
    done
done
echo "Wrote $OUT (п.4)"
