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
STRONG_STEPS=200
# Use longer runs for size scaling so fixed overhead is less dominant at small N.
SIZE_STEPS=2000

LJ_DT="1e-14"
LJ_TARGET_T=94.4
LJ_BRIEF_EQUIL=50
LJ_BRIEF_PROD_STEPS=100
LJ_BRIEF_FRAMES=$((LJ_BRIEF_PROD_STEPS + 1))
LJ_EXTENDED_EQUIL=$LJ_BRIEF_EQUIL
LJ_EXTENDED_PROD_STEPS=600
LJ_EXTENDED_FRAMES=$((LJ_EXTENDED_PROD_STEPS + 1))
LJ_RDF_EQUIL=$LJ_BRIEF_EQUIL
LJ_RDF_PROD_STEPS=20000
LJ_RDF_FRAMES=$((LJ_RDF_PROD_STEPS + 1))
LJ_GR_DISCARD_STEPS=200
LJ_GR_SAMPLE_EVERY=5
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
mpirun -np 1 $SOLVER --mode lj --integrator verlet --N 108 \
    --equilibration-steps 0 --production-steps 10 \
    --target-temperature $LJ_TARGET_T --final-rescale-before-production --outdir "$D1"
mpirun -np 2 $SOLVER --mode lj --integrator verlet --N 108 \
    --equilibration-steps 0 --production-steps 10 \
    --target-temperature $LJ_TARGET_T --final-rescale-before-production --outdir "$D2"
if python3 scripts/check_tolerance.py "$D1/lj_verlet.csv" "$D2/lj_verlet.csv" > /dev/null 2>&1; then
    echo "  P=1 vs P=2 data: MATCH ✅"
else
    echo "  P=1 vs P=2 data: MISMATCH ❌"
fi

echo ""
echo "=== RDF PARALLEL CONSISTENCY CHECK ==="
DGR1="$OUTDIR/runs/lj_gr_N108_P1_test_${TIMESTAMP}"
DGR2="$OUTDIR/runs/lj_gr_N108_P2_test_${TIMESTAMP}"
mkdir -p "$DGR1" "$DGR2"
mpirun -np 1 $SOLVER --mode lj --integrator verlet --N 108 --dt 1e-14 \
    --equilibration-steps 20 --production-steps 400 \
    --target-temperature $LJ_TARGET_T --final-rescale-before-production \
    --gr --gr-discard-steps 20 --gr-sample-every 2 --outdir "$DGR1" > /dev/null
mpirun -np 2 $SOLVER --mode lj --integrator verlet --N 108 --dt 1e-14 \
    --equilibration-steps 20 --production-steps 400 \
    --target-temperature $LJ_TARGET_T --final-rescale-before-production \
    --gr --gr-discard-steps 20 --gr-sample-every 2 --outdir "$DGR2" > /dev/null
if python3 scripts/check_gr_tolerance.py "$DGR1/gr.csv" "$DGR2/gr.csv" > /dev/null 2>&1; then
    echo "  g(r) P=1 vs P=2 data: MATCH ✅"
else
    echo "  g(r) P=1 vs P=2 data: MISMATCH ❌"
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

# ── 2. Results 2: LJ Brief + Extended ──
echo ""
echo "=== RESULTS 2: LJ BRIEF + EXTENDED ==="
echo "  Convention: startup is configured by --equilibration-steps, production by --production-steps."
echo "  CSV output reports production trajectory only: step 0 is the production initial frame."

# Brief run (required by brief): exactly 100-step NVE production at dt=1e-14 s.
RUNDIR_BRIEF_V="$OUTDIR/runs/lj_brief_N864_P4_verlet_prod${LJ_BRIEF_PROD_STEPS}_eq${LJ_BRIEF_EQUIL}_dt1e-14_${TIMESTAMP}"
mkdir -p "$RUNDIR_BRIEF_V"
echo "  Brief (required) Verlet: equilibration=${LJ_BRIEF_EQUIL}, production=${LJ_BRIEF_PROD_STEPS}, frames=${LJ_BRIEF_FRAMES}, dt=${LJ_DT}, target_T=${LJ_TARGET_T} K..."
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 \
    --dt $LJ_DT --target-temperature $LJ_TARGET_T \
    --equilibration-steps $LJ_BRIEF_EQUIL \
    --production-steps $LJ_BRIEF_PROD_STEPS \
    --final-rescale-before-production \
    --outdir "$RUNDIR_BRIEF_V" > /dev/null
if [ -s "$RUNDIR_BRIEF_V/lj_verlet.csv" ]; then
    python3 scripts/append_manifest.py "lj_brief.verlet" "$RUNDIR_BRIEF_V/lj_verlet.csv"
    echo "  -> brief Verlet output saved to manifest ✅"
fi

RUNDIR_BRIEF_E="$OUTDIR/runs/lj_brief_N864_P4_euler_prod${LJ_BRIEF_PROD_STEPS}_eq${LJ_BRIEF_EQUIL}_dt1e-14_${TIMESTAMP}"
mkdir -p "$RUNDIR_BRIEF_E"
echo "  Brief (required) Euler: equilibration=${LJ_BRIEF_EQUIL}, production=${LJ_BRIEF_PROD_STEPS}, frames=${LJ_BRIEF_FRAMES}, dt=${LJ_DT}, target_T=${LJ_TARGET_T} K..."
mpirun -np 4 $SOLVER --mode lj --integrator euler --N 864 \
    --dt $LJ_DT --target-temperature $LJ_TARGET_T \
    --equilibration-steps $LJ_BRIEF_EQUIL \
    --production-steps $LJ_BRIEF_PROD_STEPS \
    --final-rescale-before-production \
    --outdir "$RUNDIR_BRIEF_E" > /dev/null
if [ -s "$RUNDIR_BRIEF_E/lj_euler.csv" ]; then
    python3 scripts/append_manifest.py "lj_brief.euler" "$RUNDIR_BRIEF_E/lj_euler.csv"
    echo "  -> brief Euler output saved to manifest ✅"
fi

# Extended run (optional): longer trajectories for diagnostics/statistics.
RUNDIR_EXT_V="$OUTDIR/runs/lj_extended_N864_P4_verlet_prod${LJ_EXTENDED_PROD_STEPS}_eq${LJ_EXTENDED_EQUIL}_dt1e-14_${TIMESTAMP}"
mkdir -p "$RUNDIR_EXT_V"
echo "  Extended (optional) Verlet: equilibration=${LJ_EXTENDED_EQUIL}, production=${LJ_EXTENDED_PROD_STEPS}, frames=${LJ_EXTENDED_FRAMES}, dt=${LJ_DT}, target_T=${LJ_TARGET_T} K..."
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 \
    --dt $LJ_DT --target-temperature $LJ_TARGET_T \
    --equilibration-steps $LJ_EXTENDED_EQUIL \
    --production-steps $LJ_EXTENDED_PROD_STEPS \
    --final-rescale-before-production \
    --outdir "$RUNDIR_EXT_V" > /dev/null
if [ -s "$RUNDIR_EXT_V/lj_verlet.csv" ]; then
    python3 scripts/append_manifest.py "lj_extended.verlet_600" "$RUNDIR_EXT_V/lj_verlet.csv"
    echo "  -> extended Verlet output saved to manifest ✅"
fi

RUNDIR_EXT_E="$OUTDIR/runs/lj_extended_N864_P4_euler_prod${LJ_EXTENDED_PROD_STEPS}_eq${LJ_EXTENDED_EQUIL}_dt1e-14_${TIMESTAMP}"
mkdir -p "$RUNDIR_EXT_E"
echo "  Extended (optional) Euler: equilibration=${LJ_EXTENDED_EQUIL}, production=${LJ_EXTENDED_PROD_STEPS}, frames=${LJ_EXTENDED_FRAMES}, dt=${LJ_DT}, target_T=${LJ_TARGET_T} K..."
mpirun -np 4 $SOLVER --mode lj --integrator euler --N 864 \
    --dt $LJ_DT --target-temperature $LJ_TARGET_T \
    --equilibration-steps $LJ_EXTENDED_EQUIL \
    --production-steps $LJ_EXTENDED_PROD_STEPS \
    --final-rescale-before-production \
    --outdir "$RUNDIR_EXT_E" > /dev/null
if [ -s "$RUNDIR_EXT_E/lj_euler.csv" ]; then
    python3 scripts/append_manifest.py "lj_extended.euler_600" "$RUNDIR_EXT_E/lj_euler.csv"
    echo "  -> extended Euler output saved to manifest ✅"
fi

# ── 3. g(r) Production Run (extended long) ──
echo ""
echo "=== g(r) PRODUCTION RUN (EXTENDED LONG) ==="
echo "  RDF long run: equilibration=${LJ_RDF_EQUIL}, production=${LJ_RDF_PROD_STEPS}, frames=${LJ_RDF_FRAMES}, discard_steps=${LJ_GR_DISCARD_STEPS}, sample_every=${LJ_GR_SAMPLE_EVERY}"
RUNDIR_GR="$OUTDIR/runs/lj_rdf_N864_P4_verlet_prod${LJ_RDF_PROD_STEPS}_eq${LJ_RDF_EQUIL}_dt1e-14_${TIMESTAMP}"
mkdir -p "$RUNDIR_GR"
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 \
    --dt $LJ_DT \
    --target-temperature $LJ_TARGET_T \
    --equilibration-steps $LJ_RDF_EQUIL \
    --production-steps $LJ_RDF_PROD_STEPS \
    --final-rescale-before-production \
    --gr \
    --gr-discard-steps $LJ_GR_DISCARD_STEPS \
    --gr-sample-every $LJ_GR_SAMPLE_EVERY \
    --outdir "$RUNDIR_GR" > /dev/null
if [ -s "$RUNDIR_GR/gr.csv" ]; then
    python3 scripts/append_manifest.py "lj_rdf.verlet_long" "$RUNDIR_GR/gr.csv"
    python3 scripts/append_manifest.py "lj_rdf.verlet_long_energy" "$RUNDIR_GR/lj_verlet.csv"
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
echo "=== RESULTS 3: STRONG SCALING (20 reps, N=2048, ${STRONG_STEPS} steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_strong.csv"
python3 scripts/append_manifest.py "scaling.strong" "$OUTDIR/scaling_strong.csv"

REPS=20
for P in 1 2 4 8 16 24 32; do
    WALLS=""
    COMMS=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np $P $SOLVER --mode lj --integrator verlet --N 2048 --steps $STRONG_STEPS --timing 2>/dev/null)
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
echo "=== RESULTS 3: SIZE SCALING (20 reps, P=16, ${SIZE_STEPS} steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_size.csv"
python3 scripts/append_manifest.py "scaling.size" "$OUTDIR/scaling_size.csv"

for N in 108 256 500 864 1372 2048; do
    WALLS=""
    COMMS=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np 16 $SOLVER --mode lj --integrator verlet --N $N --steps $SIZE_STEPS --timing 2>/dev/null)
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
