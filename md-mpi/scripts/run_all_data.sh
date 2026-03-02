#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# run_all_data.sh — Generate ALL production data for the report
#
# Designed for shared HPC clusters (cerberus1). Uses median-of-5
# repetitions for scaling benchmarks to filter contention noise.
#
# Usage:
#   bash scripts/run_all_data.sh
#
# Produces:
#   out/ho/     HO convergence CSVs (per integrator, per dt)
#   out/lj/     LJ production CSVs (Euler + Verlet)
#   out/gr.csv  Radial distribution function
#   out/scaling_strong.csv  Strong scaling (median wall + comm times)
#   out/scaling_size.csv    Size scaling (median wall + comm times)
# ──────────────────────────────────────────────────────────────────

set -euo pipefail

SOLVER="./md_solver"
OUTDIR="out"

mkdir -p "$OUTDIR/ho" "$OUTDIR/lj"

echo "=========================================="
echo "  FULL DATA GENERATION — $(date)"
echo "=========================================="

# Helper: compute median of 5 values (sorts and picks middle)
median5() {
    echo "$@" | tr ' ' '\n' | sort -g | sed -n '3p'
}

# ── 0. Parallel Consistency Check ──
echo ""
echo "=== PARALLEL CONSISTENCY CHECK ==="
mpirun -np 1 $SOLVER --mode lj --N 108 --steps 10 2>/dev/null > /tmp/p1_full.txt
mpirun -np 2 $SOLVER --mode lj --N 108 --steps 10 2>/dev/null > /tmp/p2_full.txt
# Compare only CSV data lines (skip header with P= and wall time)
grep "^[0-9]" /tmp/p1_full.txt > /tmp/d1.txt || true
grep "^[0-9]" /tmp/p2_full.txt > /tmp/d2.txt || true
if diff -q /tmp/d1.txt /tmp/d2.txt > /dev/null 2>&1; then
    echo "  P=1 vs P=2 data: MATCH ✅"
else
    echo "  P=1 vs P=2 data: MISMATCH ❌ — CHECK MANUALLY"
fi

# ── 1. Results 1: HO Convergence ──
echo ""
echo "=== RESULTS 1: HO CONVERGENCE ==="
for INT in euler verlet rk4; do
    for DT in 1.0 0.5 0.1 0.05 0.01 0.005 0.001 0.0005; do
        STEPS=$(python3 -c "print(int(10.0/$DT))")
        mpirun -np 1 $SOLVER --mode ho --integrator $INT --N 1 --steps $STEPS --dt $DT 2>/dev/null
        # Code writes to out/ho_{integrator}.csv — copy immediately before next run overwrites
        cp "$OUTDIR/ho_${INT}.csv" "$OUTDIR/ho/${INT}_dt${DT}.csv"
        echo "  $INT dt=$DT steps=$STEPS -> ho/${INT}_dt${DT}.csv"
    done
done

# ── 2. Results 2: LJ Production (100 steps, NVE) ──
echo ""
echo "=== RESULTS 2: LJ PRODUCTION ==="

echo "  Verlet N=864 100 steps..."
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 --steps 100 2>/dev/null
cp "$OUTDIR/lj_verlet.csv" "$OUTDIR/lj/verlet_864_100.csv"

echo "  Euler N=864 100 steps..."
mpirun -np 4 $SOLVER --mode lj --integrator euler --N 864 --steps 100 2>/dev/null
cp "$OUTDIR/lj_euler.csv" "$OUTDIR/lj/euler_864_100.csv"

echo "  LJ production done ✅"

# ── 3. g(r) Production Run ──
echo ""
echo "=== g(r) PRODUCTION RUN ==="
echo "  N=864, 5000 steps, rescale-freq=10, rescale-end=500, 451 frames..."
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 --steps 5000 \
    --rescale-freq 10 --rescale-end 500 --gr --gr-discard 500 --gr-interval 10 2>/dev/null
echo "  g(r) done: $(wc -l < "$OUTDIR/gr.csv") lines ✅"

# ── 4. Results 3: Strong Scaling (median of 5 reps) ──
echo ""
echo "=== RESULTS 3: STRONG SCALING (median of 5 reps, N=2048, 200 steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_strong.csv"

N_STRONG=2048
for P in 1 2 4 8 16 24 32; do
    WALLS=""
    COMMS=""
    for REP in 1 2 3 4 5; do
        OUTPUT=$(mpirun -np $P $SOLVER --mode lj --N $N_STRONG --steps 200 --timing 2>/dev/null)
        W=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
        C=$(echo "$OUTPUT" | grep "Comm time" | awk '{print $3}')
        WALLS="$WALLS $W"
        COMMS="$COMMS $C"
        echo "    P=$P rep=$REP wall=$W comm=$C"
    done
    MEDIAN_W=$(median5 $WALLS)
    MEDIAN_C=$(median5 $COMMS)
    echo "$P,$N_STRONG,$MEDIAN_W,$MEDIAN_C" >> "$OUTDIR/scaling_strong.csv"
    echo "  P=$P MEDIAN: wall=$MEDIAN_W comm=$MEDIAN_C"
done

# ── 5. Results 3: Size Scaling (median of 5 reps) ──
echo ""
echo "=== RESULTS 3: SIZE SCALING (median of 5 reps, P=16, 200 steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_size.csv"

P_SIZE=16
for N in 108 256 500 864 1372 2048; do
    WALLS=""
    COMMS=""
    for REP in 1 2 3 4 5; do
        OUTPUT=$(mpirun -np $P_SIZE $SOLVER --mode lj --N $N --steps 200 --timing 2>/dev/null)
        W=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
        C=$(echo "$OUTPUT" | grep "Comm time" | awk '{print $3}')
        WALLS="$WALLS $W"
        COMMS="$COMMS $C"
        echo "    N=$N rep=$REP wall=$W comm=$C"
    done
    MEDIAN_W=$(median5 $WALLS)
    MEDIAN_C=$(median5 $COMMS)
    echo "$P_SIZE,$N,$MEDIAN_W,$MEDIAN_C" >> "$OUTDIR/scaling_size.csv"
    echo "  N=$N MEDIAN: wall=$MEDIAN_W comm=$MEDIAN_C"
done

# ── Summary ──
echo ""
echo "=========================================="
echo "  ALL DONE — $(date)"
echo "=========================================="
echo ""
echo "Output files:"
echo "  HO convergence:"
ls -l "$OUTDIR/ho/"
echo ""
echo "  LJ production:"
ls -l "$OUTDIR/lj/"
echo ""
echo "  g(r):"
ls -l "$OUTDIR/gr.csv"
echo ""
echo "  Scaling (medians):"
echo "  Strong:"
cat "$OUTDIR/scaling_strong.csv"
echo ""
echo "  Size:"
cat "$OUTDIR/scaling_size.csv"
