#!/usr/bin/env bash
# Run bandwidth experiments for three levels: memory, qpi, network.
# Output: results/<cluster>_<level>.csv with lines "level,m_bytes,t_sec".
# Usage: ./run_experiments.sh [cluster]   # cluster: pine | oak | numa | smp (default: pine)
# Requires: benchmark binary in ., MPIRUN (e.g. mpirun or mpiexec), optional NUMACTL.
# На кластере Pine уровень network снимайте через SLURM: sbatch task_pine.job

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

BENCHMARK="${BENCHMARK:-./benchmark}"
MPIRUN="${MPIRUN:-mpirun}"
NUMACTL="${NUMACTL:-numactl}"
N_ITER="${N_ITER:-100}"
CLUSTER="${1:-pine}"

# Message sizes: from 4KB to 8MB (bytes)
SIZES="4096 16384 65536 262144 1048576 2097152 4194304 8388608"

mkdir -p results
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
RESULTS_DIR="results"

run_one() {
    local level="$1"
    local m="$2"
    local opts="$3"
    local out
    out=$("$MPIRUN" $opts -np 2 "$BENCHMARK" "$m" "$N_ITER" 2>/dev/null | head -1)
    if [[ -n "$out" ]]; then
        echo "${level},${out}"
    fi
}

# Level: memory — two processes on one node, same NUMA node (one socket)
run_level_memory() {
    local level="memory"
    local outfile="${RESULTS_DIR}/${CLUSTER}_${level}.csv"
    echo "level,m_bytes,t_sec" > "$outfile"
    for m in $SIZES; do
        # Both ranks on same node; same socket preferred for "memory" (use numactl to bind to one node)
        if command -v "$NUMACTL" &>/dev/null; then
            out=$(numactl --cpunodebind=0 --membind=0 "$MPIRUN" -np 2 "$BENCHMARK" "$m" "$N_ITER" 2>/dev/null | head -1)
        else
            out=$("$MPIRUN" -np 2 --map-by ppr:2:node "$BENCHMARK" "$m" "$N_ITER" 2>/dev/null | head -1)
        fi
        [[ -n "$out" ]] && echo "${level},${out}" >> "$outfile"
    done
    echo "Wrote $outfile"
}

# Level: qpi — two processes on one node, different NUMA nodes (two sockets)
run_level_qpi() {
    local level="qpi"
    local outfile="${RESULTS_DIR}/${CLUSTER}_${level}.csv"
    echo "level,m_bytes,t_sec" > "$outfile"
    for m in $SIZES; do
        # Two sockets on one node: Open MPI --map-by ppr:1:socket
        out=$("$MPIRUN" -np 2 --map-by ppr:1:socket "$BENCHMARK" "$m" "$N_ITER" 2>/dev/null | head -1)
        # MPICH/MVAPICH2: try -bind-to socket or leave to default (may need hostfile with one host)
        [[ -z "$out" ]] && out=$("$MPIRUN" -np 2 "$BENCHMARK" "$m" "$N_ITER" 2>/dev/null | head -1)
        [[ -n "$out" ]] && echo "${level},${out}" >> "$outfile"
    done
    echo "Wrote $outfile"
}

# Level: network — two processes on two different nodes
run_level_network() {
    local level="network"
    local outfile="${RESULTS_DIR}/${CLUSTER}_${level}.csv"
    echo "level,m_bytes,t_sec" > "$outfile"
    for m in $SIZES; do
        # Two nodes: --map-by ppr:1:node or use hostfile with two hosts
        out=$("$MPIRUN" -np 2 --map-by ppr:1:node "$BENCHMARK" "$m" "$N_ITER" 2>/dev/null | head -1)
        [[ -z "$out" ]] && out=$("$MPIRUN" -np 2 "$BENCHMARK" "$m" "$N_ITER" 2>/dev/null | head -1)
        [[ -n "$out" ]] && echo "${level},${out}" >> "$outfile"
    done
    echo "Wrote $outfile"
}

if [[ ! -x "$BENCHMARK" ]]; then
    echo "Build benchmark first: make"
    exit 1
fi

run_level_memory
run_level_qpi
run_level_network

echo "Done. Results in ${RESULTS_DIR}/"
