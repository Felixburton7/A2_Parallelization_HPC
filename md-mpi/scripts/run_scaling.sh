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
#   out/scaling_strong_raw.csv
#   out/scaling_size_raw.csv
#   out/scaling_strong_stats.csv
#   out/scaling_size_stats.csv
#   out/scaling_meta.txt
# ──────────────────────────────────────────────────────────────────

set -euo pipefail

SOLVER="./md_solver"
OUTDIR="out"
STRONG_STEPS=1000
SIZE_STEPS=5000
INTEGRATOR="verlet"
REPS=31

mkdir -p "$OUTDIR"

if [ $((REPS % 2)) -eq 0 ]; then
    echo "ERROR: REPS must be odd for an unambiguous median-by-sample selection (got REPS=$REPS)." >&2
    exit 1
fi

# Helper: from a sorted [rep wall comm] temp file, emit robust wall-time spread stats.
# Prints CSV fields:
# reps,median_rep,median_wall_s,median_comm_s,q1_wall_s,q3_wall_s,iqr_wall_s,min_wall_s,max_wall_s
summarize_sorted_samples() {
    local sorted_file="$1"
    local n
    n=$(wc -l < "$sorted_file" | tr -d ' ')

    if [ "$n" -le 0 ]; then
        return 1
    fi

    local mid q1 q3
    mid=$(( n / 2 + 1 ))
    q1=$(( (n + 1) / 4 ))
    q3=$(( (3 * n + 3) / 4 ))

    local median_line q1_line q3_line min_line max_line
    median_line=$(sed -n "${mid}p" "$sorted_file")
    q1_line=$(sed -n "${q1}p" "$sorted_file")
    q3_line=$(sed -n "${q3}p" "$sorted_file")
    min_line=$(sed -n "1p" "$sorted_file")
    max_line=$(sed -n "${n}p" "$sorted_file")

    local median_rep median_wall median_comm q1_wall q3_wall min_wall max_wall iqr_wall
    median_rep=$(echo "$median_line" | awk '{print $1}')
    median_wall=$(echo "$median_line" | awk '{print $2}')
    median_comm=$(echo "$median_line" | awk '{print $3}')
    q1_wall=$(echo "$q1_line" | awk '{print $2}')
    q3_wall=$(echo "$q3_line" | awk '{print $2}')
    min_wall=$(echo "$min_line" | awk '{print $2}')
    max_wall=$(echo "$max_line" | awk '{print $2}')
    iqr_wall=$(awk -v q1="$q1_wall" -v q3="$q3_wall" 'BEGIN{printf "%.6f", q3 - q1}')

    echo "$n,$median_rep,$median_wall,$median_comm,$q1_wall,$q3_wall,$iqr_wall,$min_wall,$max_wall"
}

# ─── Strong Scaling: N=2048, vary P ──────────────────────────────
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_strong.csv"
echo "kind,P,N,rep,wall_s,comm_s" > "$OUTDIR/scaling_strong_raw.csv"
echo "P,N,reps,median_rep,median_wall_s,median_comm_s,q1_wall_s,q3_wall_s,iqr_wall_s,min_wall_s,max_wall_s" > "$OUTDIR/scaling_strong_stats.csv"

N_STRONG=2048
for P in 1 2 4 8 16 24 32; do
    TMP_SAMPLES=$(mktemp)
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np "$P" "$SOLVER" \
            --mode lj --integrator "$INTEGRATOR" \
            --N "$N_STRONG" --steps "$STRONG_STEPS" --timing 2>&1)

        WALL=$(awk '/Wall time/ {print $3; exit}' <<< "$OUTPUT")
        COMM=$(awk '/Comm time/ {print $3; exit}' <<< "$OUTPUT")
        if [ -z "$WALL" ]; then
            echo "ERROR: failed to parse wall time for strong scaling (P=$P, rep=$REP)." >&2
            echo "$OUTPUT" >&2
            rm -f "$TMP_SAMPLES"
            exit 1
        fi
        # P=1 has no comm line
        if [ -z "$COMM" ]; then COMM="0.000000"; fi
        COMM=$(awk -v w="$WALL" -v c="$COMM" 'BEGIN{if (c > w) print w; else print c}')

        echo "$REP $WALL $COMM" >> "$TMP_SAMPLES"
        echo "strong,$P,$N_STRONG,$REP,$WALL,$COMM" >> "$OUTDIR/scaling_strong_raw.csv"
        echo "  P=$P rep=$REP wall=$WALL comm=$COMM"
    done

    SORTED_SAMPLES=$(mktemp)
    sort -n -k2 "$TMP_SAMPLES" > "$SORTED_SAMPLES"
    STATS=$(summarize_sorted_samples "$SORTED_SAMPLES")
    rm -f "$TMP_SAMPLES" "$SORTED_SAMPLES"

    REPS_OUT=$(echo "$STATS" | cut -d, -f1)
    MEDIAN_REP=$(echo "$STATS" | cut -d, -f2)
    MED_WALL=$(echo "$STATS" | cut -d, -f3)
    MED_COMM=$(echo "$STATS" | cut -d, -f4)
    Q1_WALL=$(echo "$STATS" | cut -d, -f5)
    Q3_WALL=$(echo "$STATS" | cut -d, -f6)
    IQR_WALL=$(echo "$STATS" | cut -d, -f7)
    MIN_WALL=$(echo "$STATS" | cut -d, -f8)
    MAX_WALL=$(echo "$STATS" | cut -d, -f9)

    echo "$P,$N_STRONG,$MED_WALL,$MED_COMM" >> "$OUTDIR/scaling_strong.csv"
    echo "$P,$N_STRONG,$REPS_OUT,$MEDIAN_REP,$MED_WALL,$MED_COMM,$Q1_WALL,$Q3_WALL,$IQR_WALL,$MIN_WALL,$MAX_WALL" >> "$OUTDIR/scaling_strong_stats.csv"
    echo ">> P=$P MEDIAN: wall=$MED_WALL comm=$MED_COMM"
done

echo ""

# ─── Size Scaling: P=16, vary N ──────────────────────────────────
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_size.csv"
echo "kind,P,N,rep,wall_s,comm_s" > "$OUTDIR/scaling_size_raw.csv"
echo "P,N,reps,median_rep,median_wall_s,median_comm_s,q1_wall_s,q3_wall_s,iqr_wall_s,min_wall_s,max_wall_s" > "$OUTDIR/scaling_size_stats.csv"

P_SIZE=16
for N in 108 256 500 864 1372 2048; do
    TMP_SAMPLES=$(mktemp)
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np "$P_SIZE" "$SOLVER" \
            --mode lj --integrator "$INTEGRATOR" \
            --N "$N" --steps "$SIZE_STEPS" --timing 2>&1)

        WALL=$(awk '/Wall time/ {print $3; exit}' <<< "$OUTPUT")
        COMM=$(awk '/Comm time/ {print $3; exit}' <<< "$OUTPUT")
        if [ -z "$WALL" ]; then
            echo "ERROR: failed to parse wall time for size scaling (N=$N, rep=$REP)." >&2
            echo "$OUTPUT" >&2
            rm -f "$TMP_SAMPLES"
            exit 1
        fi
        if [ -z "$COMM" ]; then COMM="0.000000"; fi
        COMM=$(awk -v w="$WALL" -v c="$COMM" 'BEGIN{if (c > w) print w; else print c}')

        echo "$REP $WALL $COMM" >> "$TMP_SAMPLES"
        echo "size,$P_SIZE,$N,$REP,$WALL,$COMM" >> "$OUTDIR/scaling_size_raw.csv"
        echo "  N=$N rep=$REP wall=$WALL comm=$COMM"
    done

    SORTED_SAMPLES=$(mktemp)
    sort -n -k2 "$TMP_SAMPLES" > "$SORTED_SAMPLES"
    STATS=$(summarize_sorted_samples "$SORTED_SAMPLES")
    rm -f "$TMP_SAMPLES" "$SORTED_SAMPLES"

    REPS_OUT=$(echo "$STATS" | cut -d, -f1)
    MEDIAN_REP=$(echo "$STATS" | cut -d, -f2)
    MED_WALL=$(echo "$STATS" | cut -d, -f3)
    MED_COMM=$(echo "$STATS" | cut -d, -f4)
    Q1_WALL=$(echo "$STATS" | cut -d, -f5)
    Q3_WALL=$(echo "$STATS" | cut -d, -f6)
    IQR_WALL=$(echo "$STATS" | cut -d, -f7)
    MIN_WALL=$(echo "$STATS" | cut -d, -f8)
    MAX_WALL=$(echo "$STATS" | cut -d, -f9)

    echo "$P_SIZE,$N,$MED_WALL,$MED_COMM" >> "$OUTDIR/scaling_size.csv"
    echo "$P_SIZE,$N,$REPS_OUT,$MEDIAN_REP,$MED_WALL,$MED_COMM,$Q1_WALL,$Q3_WALL,$IQR_WALL,$MIN_WALL,$MAX_WALL" >> "$OUTDIR/scaling_size_stats.csv"
    echo ">> N=$N MEDIAN: wall=$MED_WALL comm=$MED_COMM"
done

{
  echo "hostname: $(hostname)"
  if command -v lscpu &>/dev/null; then
    echo "cpu: $(lscpu | grep 'Model name' | sed 's/.*: *//')"
  elif [ -r /proc/cpuinfo ]; then
    echo "cpu: $(grep -m1 'model name' /proc/cpuinfo | sed 's/.*: *//')"
  else
    echo "cpu: unknown"
  fi
  if command -v mpicxx &>/dev/null; then
    echo "compiler: $(mpicxx --version | head -1)"
  else
    echo "compiler: unknown"
  fi
  if command -v mpirun &>/dev/null; then
    echo "mpi: $(mpirun --version | head -1)"
  else
    echo "mpi: unknown"
  fi
  echo "date: $(date -Iseconds)"
} > "$OUTDIR/scaling_meta.txt"

echo ""
echo "Done. Results in:"
echo "  $OUTDIR/scaling_strong.csv"
echo "  $OUTDIR/scaling_size.csv"
echo "  $OUTDIR/scaling_strong_raw.csv"
echo "  $OUTDIR/scaling_size_raw.csv"
echo "  $OUTDIR/scaling_strong_stats.csv"
echo "  $OUTDIR/scaling_size_stats.csv"
echo "  $OUTDIR/scaling_meta.txt"
