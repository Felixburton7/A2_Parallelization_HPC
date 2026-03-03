#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# run_scaling.sh — Batch scaling benchmarks with comm breakdown
#
# Uses PAIRED observations: for each rep, records (wall, comm) as a pair.
# The median is selected by wall time, and the comm from THAT SAME rep
# is reported. This guarantees comm <= wall for every data point.
#
# Usage:
#   bash scripts/run_scaling.sh
#
# Produces:
#   out/scaling_strong.csv   (P,N,wall_s,comm_s)
#   out/scaling_size.csv     (P,N,wall_s,comm_s)
# ──────────────────────────────────────────────────────────────────

set -euo pipefail

SOLVER="./md_solver"
OUTDIR="out"
STEPS=100
INTEGRATOR="verlet"
REPS=5

mkdir -p "$OUTDIR"

# Helper: given parallel arrays of wall and comm times, pick the
# median by wall time and return the paired (wall, comm).
# Usage: pick_median_pair "w1 w2 w3 w4 w5" "c1 c2 c3 c4 c5"
# Prints: wall_median comm_from_same_rep
pick_median_pair() {
    local walls=($1)
    local comms=($2)
    local n=${#walls[@]}

    # Create index-sorted-by-wall array using a temp file
    local tmpfile
    tmpfile=$(mktemp)
    for i in $(seq 0 $((n-1))); do
        echo "${walls[$i]} ${comms[$i]}"
    done | sort -n -k1 > "$tmpfile"

    # Pick the middle row (0-indexed: row (n-1)/2 for odd n)
    local mid=$(( (n - 1) / 2 ))
    local line
    line=$(sed -n "$((mid+1))p" "$tmpfile")
    rm -f "$tmpfile"

    echo "$line"
}

# ─── Strong Scaling: N=2048, vary P ──────────────────────────────
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_strong.csv"

N_STRONG=2048
for P in 1 2 4 8 16 24 32; do
    WALLS=""
    COMMS=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun --oversubscribe -np "$P" "$SOLVER" \
            --mode lj --integrator "$INTEGRATOR" \
            --N "$N_STRONG" --steps "$STEPS" --timing 2>&1)

        WALL=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
        COMM=$(echo "$OUTPUT" | grep "Comm time" | awk '{print $3}')
        # P=1 has no comm line
        if [ -z "$COMM" ]; then COMM="0.000000"; fi

        WALLS="$WALLS $WALL"
        COMMS="$COMMS $COMM"
        echo "  P=$P rep=$REP wall=$WALL comm=$COMM"
    done

    PAIR=$(pick_median_pair "$WALLS" "$COMMS")
    MED_WALL=$(echo "$PAIR" | awk '{print $1}')
    MED_COMM=$(echo "$PAIR" | awk '{print $2}')
    echo "$P,$N_STRONG,$MED_WALL,$MED_COMM" >> "$OUTDIR/scaling_strong.csv"
    echo ">> P=$P MEDIAN: wall=$MED_WALL comm=$MED_COMM"
done

echo ""

# ─── Size Scaling: P=16, vary N ──────────────────────────────────
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_size.csv"

P_SIZE=16
for N in 108 256 500 864 1372 2048; do
    WALLS=""
    COMMS=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun --oversubscribe -np "$P_SIZE" "$SOLVER" \
            --mode lj --integrator "$INTEGRATOR" \
            --N "$N" --steps "$STEPS" --timing 2>&1)

        WALL=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
        COMM=$(echo "$OUTPUT" | grep "Comm time" | awk '{print $3}')
        if [ -z "$COMM" ]; then COMM="0.000000"; fi

        WALLS="$WALLS $WALL"
        COMMS="$COMMS $COMM"
        echo "  N=$N rep=$REP wall=$WALL comm=$COMM"
    done

    PAIR=$(pick_median_pair "$WALLS" "$COMMS")
    MED_WALL=$(echo "$PAIR" | awk '{print $1}')
    MED_COMM=$(echo "$PAIR" | awk '{print $2}')
    echo "$P_SIZE,$N,$MED_WALL,$MED_COMM" >> "$OUTDIR/scaling_size.csv"
    echo ">> N=$N MEDIAN: wall=$MED_WALL comm=$MED_COMM"
done

echo ""
echo "Done. Results in $OUTDIR/scaling_strong.csv and $OUTDIR/scaling_size.csv"
