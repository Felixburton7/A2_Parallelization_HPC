#!/bin/bash
# Generate the data used in the report.
# By default, Results 3 uses the reference scaling tables in
# scripts/data/reference_scaling/.

set -euo pipefail

SOLVER="./md_solver"
OUTDIR="out"
SKIP_SCALING=0
LIVE_SCALING=0
STRONG_STEPS=500
SIZE_STEPS=2000
SCALING_REPS=11
SCALING_BIND_TO_CORE=1
SCALING_REF_DIR="scripts/data/reference_scaling"

LJ_DT="1e-14"
LJ_TARGET_T=94.4
LJ_BRIEF_EQUIL=50
LJ_BRIEF_PROD_STEPS=100
LJ_BRIEF_FRAMES=$((LJ_BRIEF_PROD_STEPS + 1))
LJ_RDF_EQUIL=$LJ_BRIEF_EQUIL
LJ_RDF_PROD_STEPS=20000
LJ_RDF_FRAMES=$((LJ_RDF_PROD_STEPS + 1))
LJ_GR_DISCARD_STEPS=200
LJ_GR_SAMPLE_EVERY=5
for arg in "$@"; do
  case "$arg" in
    --skip-scaling) SKIP_SCALING=1 ;;
    --live-scaling) LIVE_SCALING=1 ;;
    --reference-scaling) LIVE_SCALING=0 ;;
    --bind-to-core) SCALING_BIND_TO_CORE=1 ;;
    --no-bind-to-core) SCALING_BIND_TO_CORE=0 ;;
    *)
      echo "ERROR: unknown argument '$arg'" >&2
      echo "Usage: bash scripts/run_all_data.sh [--skip-scaling] [--live-scaling] [--reference-scaling] [--bind-to-core|--no-bind-to-core]" >&2
      exit 1
      ;;
  esac
done

rm -f "$OUTDIR/manifest.json"
mkdir -p "$OUTDIR/runs"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "=========================================="
echo "  DATA GENERATION - $(date)"
echo "=========================================="

# 0. Parallel consistency check
echo ""
echo "=== PARALLEL CONSISTENCY CHECK ==="
# This uses zero equilibration for a quick MPI consistency test.
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
    echo "  P=1 vs P=2 data: match"
else
    echo "  P=1 vs P=2 data: mismatch"
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
    echo "  g(r) P=1 vs P=2 data: match"
else
    echo "  g(r) P=1 vs P=2 data: mismatch"
fi

# 1. Results 1: HO convergence
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
            echo "  $INT dt=$DT steps=$STEPS -> saved to $DSTFILE"
        else
            echo "  $INT dt=$DT steps=$STEPS -> FAILED"
        fi
    done
done

# 2. Results 2: LJ brief run
echo ""
echo "=== RESULTS 2: LJ BRIEF ==="
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
    echo "  -> brief Verlet output saved in manifest"
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
    echo "  -> brief Euler output saved in manifest"
fi

# 3. g(r) production run
echo ""
echo "=== g(r) PRODUCTION RUN (LONG) ==="
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
    echo "  g(r) complete; output saved in manifest"
else
    echo "  g(r) FAILED"
fi

# 4. Strong and size scaling
if [ "$SKIP_SCALING" = "1" ]; then
  echo ""
  echo "=== SKIPPING SCALING (--skip-scaling) ==="
  # Re-register existing files in manifest if they exist
  [ -f "$OUTDIR/scaling_strong.csv" ] && python3 scripts/append_manifest.py "scaling.strong" "$OUTDIR/scaling_strong.csv"
  [ -f "$OUTDIR/scaling_size.csv" ]   && python3 scripts/append_manifest.py "scaling.size"   "$OUTDIR/scaling_size.csv"
else
echo ""
if [ "$LIVE_SCALING" = "1" ]; then
  echo "=== RESULTS 3: LIVE SCALING (reps=${SCALING_REPS}, strong_steps=${STRONG_STEPS}, size_steps=${SIZE_STEPS}, bind_to_core=${SCALING_BIND_TO_CORE}) ==="
  REPS="$SCALING_REPS" \
  SOLVER="$SOLVER" \
  OUTDIR="$OUTDIR" \
  STRONG_STEPS="$STRONG_STEPS" \
  SIZE_STEPS="$SIZE_STEPS" \
  BIND_TO_CORE="$SCALING_BIND_TO_CORE" \
  INTEGRATOR="verlet" \
    bash scripts/run_scaling.sh
else
  echo "=== RESULTS 3: REFERENCE SCALING DATA ==="
  for f in \
    scaling_strong.csv \
    scaling_size.csv
  do
    SRC="$SCALING_REF_DIR/$f"
    if [ ! -s "$SRC" ]; then
      echo "ERROR: missing reference scaling file $SRC" >&2
      exit 1
    fi
    cp "$SRC" "$OUTDIR/$f"
  done
fi

python3 scripts/append_manifest.py "scaling.strong" "$OUTDIR/scaling_strong.csv"
python3 scripts/append_manifest.py "scaling.size" "$OUTDIR/scaling_size.csv"

fi  # end --skip-scaling check

# Validate manifest before plotting.
if [ "$SKIP_SCALING" = "1" ]; then
  python3 scripts/validate_manifest.py --skip-scaling
else
  python3 scripts/validate_manifest.py
fi

# Summary
echo ""
echo "=========================================="
echo "  FINISHED - $(date)"
echo "=========================================="
echo "Run data written under: $OUTDIR/"
