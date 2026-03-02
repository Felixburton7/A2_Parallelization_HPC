#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# run_scaling.sh — Batch execution for scaling benchmarks on cerberus1
#
# Usage:
#   bash scripts/run_scaling.sh
#
# Produces:
#   out/scaling_strong.csv   (P, time)
#   out/scaling_size.csv     (N, time)
# ──────────────────────────────────────────────────────────────────

set -euo pipefail

SOLVER="./md_solver"
OUTDIR="out"
STEPS=100
INTEGRATOR="verlet"

mkdir -p "$OUTDIR"

# ─── Strong Scaling: N=2048, vary P ──────────────────────────────
echo "P,time" > "$OUTDIR/scaling_strong.csv"

N_STRONG=2048
for P in 1 2 4 8 16 24 32; do
    echo "Strong scaling: N=$N_STRONG, P=$P"
    OUTPUT=$(mpirun -np "$P" "$SOLVER" \
        --mode lj --integrator "$INTEGRATOR" \
        --N "$N_STRONG" --steps "$STEPS" --timing 2>&1)

    # Extract wall time from output: "Wall time: X.XXXXXX s ..."
    TIME=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
    echo "$P,$TIME" >> "$OUTDIR/scaling_strong.csv"
    echo "  -> $TIME s"
done

echo ""

# ─── Size Scaling: P=16, vary N ──────────────────────────────────
echo "N,time" > "$OUTDIR/scaling_size.csv"

P_SIZE=16
for N in 108 256 500 864 1372 2048; do
    echo "Size scaling: N=$N, P=$P_SIZE"
    OUTPUT=$(mpirun -np "$P_SIZE" "$SOLVER" \
        --mode lj --integrator "$INTEGRATOR" \
        --N "$N" --steps "$STEPS" --timing 2>&1)

    TIME=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
    echo "$N,$TIME" >> "$OUTDIR/scaling_size.csv"
    echo "  -> $TIME s"
done

echo ""
echo "Done. Results in $OUTDIR/scaling_strong.csv and $OUTDIR/scaling_size.csv"
