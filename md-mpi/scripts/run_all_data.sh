#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# run_all_data.sh — Generate ALL production data for the report
#
# Designed for shared HPC clusters (cerberus1). Uses median-of-20
# paired (wall, comm) repetitions for scaling benchmarks to filter contention noise.
# ──────────────────────────────────────────────────────────────────

set -euo pipefail

SOLVER="./md_solver"
OUTDIR="out"
SKIP_SCALING=0
for arg in "$@"; do
  [ "$arg" = "--skip-scaling" ] && SKIP_SCALING=1
done

rm -f "$OUTDIR/manifest.json"
mkdir -p "$OUTDIR/runs"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "=========================================="
echo "  FULL DATA GENERATION — $(date)"
echo "=========================================="

# Helper: given parallel arrays of wall and comm times, pick the
# median by wall time and return the paired (wall, comm).
pick_median_pair() {
    local walls=($1)
    local comms=($2)
    local n=${#walls[@]}
    local tmpfile
    tmpfile=$(mktemp)
    for i in $(seq 0 $((n-1))); do
        echo "${walls[$i]} ${comms[$i]}"
    done | sort -n -k1 > "$tmpfile"
    local mid=$(( (n - 1) / 2 ))
    local line
    line=$(sed -n "$((mid+1))p" "$tmpfile")
    rm -f "$tmpfile"
    echo "$line"
}

# ── 0. Parallel Consistency Check ──
echo ""
echo "=== PARALLEL CONSISTENCY CHECK ==="
D1="$OUTDIR/runs/lj_N108_P1_test_${TIMESTAMP}"
D2="$OUTDIR/runs/lj_N108_P2_test_${TIMESTAMP}"
mkdir -p "$D1" "$D2"
mpirun -np 1 $SOLVER --mode lj --integrator verlet --N 108 --steps 10 --outdir "$D1"
mpirun -np 2 $SOLVER --mode lj --integrator verlet --N 108 --steps 10 --outdir "$D2"
if python3 scripts/check_tolerance.py "$D1/lj_verlet.csv" "$D2/lj_verlet.csv" > /dev/null 2>&1; then
    echo "  P=1 vs P=2 data: MATCH ✅"
else
    echo "  P=1 vs P=2 data: MISMATCH ❌"
fi

# ── 1. Results 1: HO Convergence ──
echo ""
echo "=== RESULTS 1: HO CONVERGENCE ==="
DT_LIST="1.0:10 0.5:20 0.1:100 0.05:200 0.01:1000 0.005:2000 0.001:10000 0.0005:20000"
for INT in euler verlet rk4; do
    for ENTRY in $DT_LIST; do
        DT=$(echo $ENTRY | cut -d: -f1)
        STEPS=$(echo $ENTRY | cut -d: -f2)
        RUNDIR="$OUTDIR/runs/ho_N1_${INT}_dt${DT}_${TIMESTAMP}"
        mkdir -p "$RUNDIR"
        # Exam validation requires HO to run with N=1.
        mpirun -np 1 $SOLVER --mode ho --integrator $INT --N 1 --steps $STEPS --dt $DT --outdir "$RUNDIR" > /dev/null
        DSTFILE="$RUNDIR/ho_${INT}.csv"
        if [ -s "$DSTFILE" ]; then
            python3 scripts/append_manifest.py "ho_convergence.${INT}_dt${DT//./_}" "$DSTFILE"
            echo "  $INT dt=$DT steps=$STEPS -> $DSTFILE ✅"
        else
            echo "  $INT dt=$DT steps=$STEPS -> FAILED"
        fi
    done
done

# ── 2. Results 2: LJ Production ──
echo ""
echo "=== RESULTS 2: LJ PRODUCTION ==="
RUNDIR_V="$OUTDIR/runs/lj_N864_P4_verlet_100_${TIMESTAMP}"
mkdir -p "$RUNDIR_V"
echo "  Verlet N=864 100 steps..."
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 --steps 100 --dt 1e-14 --rescale-step 10 --outdir "$RUNDIR_V" > /dev/null
if [ -s "$RUNDIR_V/lj_verlet.csv" ]; then
    python3 scripts/append_manifest.py "lj_production.verlet_100" "$RUNDIR_V/lj_verlet.csv"
    echo "  -> output saved to manifest ✅"
fi

RUNDIR_E="$OUTDIR/runs/lj_N864_P4_euler_100_${TIMESTAMP}"
mkdir -p "$RUNDIR_E"
echo "  Euler N=864 100 steps..."
mpirun -np 4 $SOLVER --mode lj --integrator euler --N 864 --steps 100 --dt 1e-14 --rescale-step 10 --outdir "$RUNDIR_E" > /dev/null
if [ -s "$RUNDIR_E/lj_euler.csv" ]; then
    python3 scripts/append_manifest.py "lj_production.euler_100" "$RUNDIR_E/lj_euler.csv"
    echo "  -> output saved to manifest ✅"
fi

# ── Equilibrated NVE comparison ──
RUNDIR_EQ="$OUTDIR/runs/lj_N864_P4_verlet_200_eq_${TIMESTAMP}"
mkdir -p "$RUNDIR_EQ"
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 \
    --steps 200 --rescale-step 100 --outdir "$RUNDIR_EQ" > /dev/null
python3 scripts/append_manifest.py "lj_production.verlet_200_equilibrated" "$RUNDIR_EQ/lj_verlet.csv"

# ── 3. g(r) Production Run ──
echo ""
echo "=== g(r) PRODUCTION RUN ==="
RUNDIR_GR="$OUTDIR/runs/lj_N864_P4_gr_${TIMESTAMP}"
mkdir -p "$RUNDIR_GR"
# With relative --gr-discard semantics (post-production-start), keep absolute
# g(r) sampling start at step 500 by setting discard=500-10=490.
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 --steps 25500 \
    --rescale-step 10 --gr --gr-discard 490 --gr-interval 10 --outdir "$RUNDIR_GR" > /dev/null
if [ -s "$RUNDIR_GR/gr.csv" ]; then
    python3 scripts/append_manifest.py "lj_gr" "$RUNDIR_GR/gr.csv"
    python3 scripts/append_manifest.py "lj_gr_energy" "$RUNDIR_GR/lj_verlet.csv"
    echo "  g(r) done, output saved to manifest ✅"
else
    echo "  g(r) FAILED ❌"
fi

# ── 4. Strong/Size Scaling ──
if [ "$SKIP_SCALING" = "1" ]; then
  echo ""
  echo "=== SKIPPING SCALING (--skip-scaling) ==="
  # Re-register existing files in manifest if they exist
  [ -f "$OUTDIR/scaling_strong.csv" ] && python3 scripts/append_manifest.py "scaling.strong" "$OUTDIR/scaling_strong.csv"
  [ -f "$OUTDIR/scaling_size.csv" ]   && python3 scripts/append_manifest.py "scaling.size"   "$OUTDIR/scaling_size.csv"
else
echo ""
echo "=== RESULTS 3: STRONG SCALING (20 reps, N=2048, 200 steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_strong.csv"
python3 scripts/append_manifest.py "scaling.strong" "$OUTDIR/scaling_strong.csv"

REPS=20
for P in 1 2 4 8 16 24 32; do
    WALLS=""
    COMMS=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np $P $SOLVER --mode lj --integrator verlet --N 2048 --steps 200 --timing 2>/dev/null)
        W=$(awk '/Wall time/ {print $3; exit}' <<< "$OUTPUT")
        C=$(awk '/Comm time/ {print $3; exit}' <<< "$OUTPUT")
        [ -z "$C" ] && C="0.0"
        C=$(awk -v w="$W" -v c="$C" 'BEGIN{if (c > w) print w; else print c}')
        WALLS="$WALLS $W"
        COMMS="$COMMS $C"
        echo "    P=$P rep=$REP wall=$W comm=$C"
    done
    PAIR=$(pick_median_pair "$WALLS" "$COMMS")
    MEDIAN_W=$(echo "$PAIR" | awk '{print $1}')
    MEDIAN_C=$(echo "$PAIR" | awk '{print $2}')
    echo "$P,2048,$MEDIAN_W,$MEDIAN_C" >> "$OUTDIR/scaling_strong.csv"
    echo "  >> P=$P MEDIAN: wall=$MEDIAN_W comm=$MEDIAN_C"
done

# ── 5. Size Scaling (median of 20 paired samples) ──
echo ""
echo "=== RESULTS 3: SIZE SCALING (20 reps, P=16, 500 steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_size.csv"
python3 scripts/append_manifest.py "scaling.size" "$OUTDIR/scaling_size.csv"

for N in 108 256 500 864 1372 2048; do
    WALLS=""
    COMMS=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np 16 $SOLVER --mode lj --integrator verlet --N $N --steps 500 --timing 2>/dev/null)
        W=$(awk '/Wall time/ {print $3; exit}' <<< "$OUTPUT")
        C=$(awk '/Comm time/ {print $3; exit}' <<< "$OUTPUT")
        [ -z "$C" ] && C="0.0"
        C=$(awk -v w="$W" -v c="$C" 'BEGIN{if (c > w) print w; else print c}')
        WALLS="$WALLS $W"
        COMMS="$COMMS $C"
        echo "    N=$N rep=$REP wall=$W comm=$C"
    done
    PAIR=$(pick_median_pair "$WALLS" "$COMMS")
    MEDIAN_W=$(echo "$PAIR" | awk '{print $1}')
    MEDIAN_C=$(echo "$PAIR" | awk '{print $2}')
    echo "16,$N,$MEDIAN_W,$MEDIAN_C" >> "$OUTDIR/scaling_size.csv"
    echo "  >> N=$N MEDIAN: wall=$MEDIAN_W comm=$MEDIAN_C"
done

fi  # end --skip-scaling check

{
  echo "hostname: $(hostname)"
  if command -v lscpu &>/dev/null; then
    echo "cpu: $(lscpu | grep 'Model name' | sed 's/.*: *//')"
  else
    echo "cpu: $(head -1 /proc/cpuinfo | sed 's/.*: *//')"
  fi
  echo "compiler: $(mpicxx --version | head -1)"
  echo "mpi: $(mpirun --version | head -1)"
  echo "date: $(date -Iseconds)"
} > "$OUTDIR/scaling_meta.txt"

# ── Validate manifest integrity before downstream plotting/analysis ──
if [ "$SKIP_SCALING" = "1" ]; then
  python3 scripts/validate_manifest.py --skip-scaling
else
  python3 scripts/validate_manifest.py
fi

# ── Summary ──
echo ""
echo "=========================================="
echo "  ALL DONE — $(date)"
echo "=========================================="
echo "Manifest written to: $OUTDIR/manifest.json"
