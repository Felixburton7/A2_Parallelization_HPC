#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# run_scaling.sh — Batch scaling benchmarks with comm breakdown
#
# Usage:
#   bash scripts/run_scaling.sh
#
# Produces:
#   out/scaling_strong.csv   (P,N,wall_s,comm_s)  — median of REPS
#   out/scaling_size.csv     (P,N,wall_s,comm_s)  — median of REPS
# ──────────────────────────────────────────────────────────────────

set -euo pipefail

SOLVER="./md_solver"
OUTDIR="out"
STEPS=100
INTEGRATOR="verlet"
REPS=5

mkdir -p "$OUTDIR"

# Helper: extract median from an array of values
get_median() {
    echo "$@" | tr ' ' '\n' | sort -n | awk '{a[NR]=$1} END {
        if (NR%2==1) print a[(NR+1)/2];
        else print (a[NR/2]+a[NR/2+1])/2
    }'
}

# ─── Strong Scaling: N=2048, vary P ──────────────────────────────
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_strong.csv"

N_STRONG=2048
for P in 1 2 4 8 16 24 32; do
    WALLS=()
    COMMS=()
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np "$P" "$SOLVER" \
            --mode lj --integrator "$INTEGRATOR" \
            --N "$N_STRONG" --steps "$STEPS" --timing 2>&1)

        WALL=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
        COMM=$(echo "$OUTPUT" | grep "Comm time" | awk '{print $3}')
        # P=1 has no comm line
        if [ -z "$COMM" ]; then COMM="0.000000"; fi

        WALLS+=("$WALL")
        COMMS+=("$COMM")
        echo "  P=$P rep=$REP wall=$WALL comm=$COMM"
    done

    MED_WALL=$(get_median "${WALLS[@]}")
    MED_COMM=$(get_median "${COMMS[@]}")
    echo "$P,$N_STRONG,$MED_WALL,$MED_COMM" >> "$OUTDIR/scaling_strong.csv"
    echo ">> P=$P MEDIAN: wall=$MED_WALL comm=$MED_COMM"
done

echo ""

# ─── Size Scaling: P=16, vary N ──────────────────────────────────
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_size.csv"

P_SIZE=16
for N in 108 256 500 864 1372 2048; do
    WALLS=()
    COMMS=()
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np "$P_SIZE" "$SOLVER" \
            --mode lj --integrator "$INTEGRATOR" \
            --N "$N" --steps "$STEPS" --timing 2>&1)

        WALL=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
        COMM=$(echo "$OUTPUT" | grep "Comm time" | awk '{print $3}')
        if [ -z "$COMM" ]; then COMM="0.000000"; fi

        WALLS+=("$WALL")
        COMMS+=("$COMM")
        echo "  N=$N rep=$REP wall=$WALL comm=$COMM"
    done

    MED_WALL=$(get_median "${WALLS[@]}")
    MED_COMM=$(get_median "${COMMS[@]}")
    echo "$P_SIZE,$N,$MED_WALL,$MED_COMM" >> "$OUTDIR/scaling_size.csv"
    echo ">> N=$N MEDIAN: wall=$MED_WALL comm=$MED_COMM"
done

echo ""
echo "Done. Results in $OUTDIR/scaling_strong.csv and $OUTDIR/scaling_size.csv"
