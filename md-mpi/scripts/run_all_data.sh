#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# run_all_data.sh — Generate ALL production data for the report
#
# Designed for shared HPC clusters (cerberus1). Uses median-of-5
# repetitions for scaling benchmarks to filter contention noise.
#
# Usage:
#   bash scripts/run_all_data.sh
# ──────────────────────────────────────────────────────────────────

SOLVER="./md_solver"
OUTDIR="out"

mkdir -p "$OUTDIR/ho" "$OUTDIR/lj"

echo "=========================================="
echo "  FULL DATA GENERATION — $(date)"
echo "=========================================="

# Helper: compute median of 5 values
median5() {
    echo "$@" | tr ' ' '\n' | sort -g | sed -n '3p'
}

# ── 0. Parallel Consistency Check ──
echo ""
echo "=== PARALLEL CONSISTENCY CHECK ==="
mpirun -np 1 $SOLVER --mode lj --N 108 --steps 10 2>/dev/null | grep "^[0-9]" > /tmp/d1.txt
mpirun -np 2 $SOLVER --mode lj --N 108 --steps 10 2>/dev/null | grep "^[0-9]" > /tmp/d2.txt
if diff -q /tmp/d1.txt /tmp/d2.txt > /dev/null 2>&1; then
    echo "  P=1 vs P=2 data: MATCH ✅"
else
    echo "  P=1 vs P=2 data: MISMATCH ❌"
fi

# ── 1. Results 1: HO Convergence ──
echo ""
echo "=== RESULTS 1: HO CONVERGENCE ==="
# dt values and corresponding steps (T_final = 10 for all)
# Using shell arithmetic to avoid python3 dependency
DT_LIST="1.0:10 0.5:20 0.1:100 0.05:200 0.01:1000 0.005:2000 0.001:10000 0.0005:20000"
for INT in euler verlet rk4; do
    for ENTRY in $DT_LIST; do
        DT=$(echo $ENTRY | cut -d: -f1)
        STEPS=$(echo $ENTRY | cut -d: -f2)
        mpirun -np 1 $SOLVER --mode ho --integrator $INT --N 1 --steps $STEPS --dt $DT 2>/dev/null
        SRCFILE="$OUTDIR/ho_${INT}.csv"
        DSTFILE="$OUTDIR/ho/${INT}_dt${DT}.csv"
        if [ -s "$SRCFILE" ]; then
            cp "$SRCFILE" "$DSTFILE"
            LINES=$(wc -l < "$DSTFILE")
            echo "  $INT dt=$DT steps=$STEPS -> $DSTFILE ($LINES lines)"
        else
            echo "  $INT dt=$DT steps=$STEPS -> FAILED (no output file)"
        fi
    done
done

# ── 2. Results 2: LJ Production ──
echo ""
echo "=== RESULTS 2: LJ PRODUCTION ==="

echo "  Verlet N=864 100 steps..."
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 --steps 100 2>/dev/null
if [ -s "$OUTDIR/lj_verlet.csv" ]; then
    cp "$OUTDIR/lj_verlet.csv" "$OUTDIR/lj/verlet_864_100.csv"
    echo "  -> lj/verlet_864_100.csv ($(wc -l < "$OUTDIR/lj/verlet_864_100.csv") lines) ✅"
fi

echo "  Euler N=864 100 steps..."
mpirun -np 4 $SOLVER --mode lj --integrator euler --N 864 --steps 100 2>/dev/null
if [ -s "$OUTDIR/lj_euler.csv" ]; then
    cp "$OUTDIR/lj_euler.csv" "$OUTDIR/lj/euler_864_100.csv"
    echo "  -> lj/euler_864_100.csv ($(wc -l < "$OUTDIR/lj/euler_864_100.csv") lines) ✅"
fi

# ── 3. g(r) Production Run ──
echo ""
echo "=== g(r) PRODUCTION RUN ==="
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 --steps 5000 \
    --rescale-freq 10 --rescale-end 500 --gr --gr-discard 500 --gr-interval 10 2>/dev/null
if [ -s "$OUTDIR/gr.csv" ]; then
    echo "  g(r) done: $(wc -l < "$OUTDIR/gr.csv") lines ✅"
else
    echo "  g(r) FAILED ❌"
fi

# ── 4. Strong Scaling (median of 5) ──
echo ""
echo "=== RESULTS 3: STRONG SCALING (5 reps, N=2048, 200 steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_strong.csv"

for P in 1 2 4 8 16 24 32; do
    WALLS=""
    COMMS=""
    for REP in 1 2 3 4 5; do
        OUTPUT=$(mpirun -np $P $SOLVER --mode lj --N 2048 --steps 200 --timing 2>/dev/null)
        W=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
        C=$(echo "$OUTPUT" | grep "Comm time" | awk '{print $3}')
        [ -z "$C" ] && C="0.0"
        WALLS="$WALLS $W"
        COMMS="$COMMS $C"
        echo "    P=$P rep=$REP wall=$W comm=$C"
    done
    MEDIAN_W=$(median5 $WALLS)
    MEDIAN_C=$(median5 $COMMS)
    echo "$P,2048,$MEDIAN_W,$MEDIAN_C" >> "$OUTDIR/scaling_strong.csv"
    echo "  >> P=$P MEDIAN: wall=$MEDIAN_W comm=$MEDIAN_C"
done

# ── 5. Size Scaling (median of 5) ──
echo ""
echo "=== RESULTS 3: SIZE SCALING (5 reps, P=16, 200 steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_size.csv"

for N in 108 256 500 864 1372 2048; do
    WALLS=""
    COMMS=""
    for REP in 1 2 3 4 5; do
        OUTPUT=$(mpirun -np 16 $SOLVER --mode lj --N $N --steps 200 --timing 2>/dev/null)
        W=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
        C=$(echo "$OUTPUT" | grep "Comm time" | awk '{print $3}')
        [ -z "$C" ] && C="0.0"
        WALLS="$WALLS $W"
        COMMS="$COMMS $C"
        echo "    N=$N rep=$REP wall=$W comm=$C"
    done
    MEDIAN_W=$(median5 $WALLS)
    MEDIAN_C=$(median5 $COMMS)
    echo "16,$N,$MEDIAN_W,$MEDIAN_C" >> "$OUTDIR/scaling_size.csv"
    echo "  >> N=$N MEDIAN: wall=$MEDIAN_W comm=$MEDIAN_C"
done

# ── Summary ──
echo ""
echo "=========================================="
echo "  ALL DONE — $(date)"
echo "=========================================="
echo ""
echo "=== FILE INVENTORY ==="
echo "HO convergence files:"
ls -la "$OUTDIR/ho/" 2>/dev/null | grep csv
echo ""
echo "LJ production files:"
ls -la "$OUTDIR/lj/" 2>/dev/null | grep csv
echo ""
echo "g(r):"
ls -la "$OUTDIR/gr.csv" 2>/dev/null
echo ""
echo "Strong scaling:"
cat "$OUTDIR/scaling_strong.csv"
echo ""
echo "Size scaling:"
cat "$OUTDIR/scaling_size.csv"
