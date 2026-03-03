#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# ai/pack_results.sh — Bundles all critical production CSV data into a 
# single markdown file so it can be easily uploaded to an LLM context.
#
# Very large trajectories (thousands of lines) are truncated to their 
# head/tail to prevent blowing up the LLM context window.
# ──────────────────────────────────────────────────────────────────

set -euo pipefail
cd "$(dirname "$0")/.."

OUTFILE="ai/results_bundle.md"
DATADIR="out"

mkdir -p ai
echo "# MD Solver Production Data Bundle" > "$OUTFILE"
echo "Generated: $(date)" >> "$OUTFILE"
echo "" >> "$OUTFILE"
echo "This file contains the raw CSV outputs from the production runs." >> "$OUTFILE"
echo "Long trajectory files are truncated to the first 10 and last 5 lines." >> "$OUTFILE"
echo "" >> "$OUTFILE"

# Helper function to append a full CSV
append_full_csv() {
    local file="$1"
    local title="$2"
    if [ -f "$file" ]; then
        echo "## $title" >> "$OUTFILE"
        echo '```csv' >> "$OUTFILE"
        cat "$file" >> "$OUTFILE"
        echo '```' >> "$OUTFILE"
        echo "" >> "$OUTFILE"
    fi
}

# Helper function to append a truncated CSV
append_trunc_csv() {
    local file="$1"
    local title="$2"
    if [ -f "$file" ]; then
        echo "## $title (Truncated)" >> "$OUTFILE"
        echo '```csv' >> "$OUTFILE"
        head -n 10 "$file" >> "$OUTFILE"
        echo "..." >> "$OUTFILE"
        tail -n 5 "$file" >> "$OUTFILE"
        echo '```' >> "$OUTFILE"
        echo "" >> "$OUTFILE"
    fi
}

# 1. SCALING DATA (Full)
append_full_csv "$DATADIR/scaling_strong.csv" "Strong Scaling (N=2048, P=1..32)"
append_full_csv "$DATADIR/scaling_size.csv" "Size Scaling (P=16, N=108..2048)"

# 2. RADIAL DISTRIBUTION FUNCTION (Full)
if [ -f "$DATADIR/gr_smooth.csv" ]; then
    append_full_csv "$DATADIR/gr_smooth.csv" "Radial Distribution Function g(r) [25500 steps]"
else
    append_full_csv "$DATADIR/gr.csv" "Radial Distribution Function g(r)"
fi

# 3. LENNARD-JONES TRAJECTORIES (Truncated)
append_trunc_csv "$DATADIR/lj/verlet_864_100.csv" "LJ Velocity-Verlet Raw NVE (N=864, 100 steps)"
append_trunc_csv "$DATADIR/lj/euler_864_100.csv" "LJ Euler Raw NVE (N=864, 100 steps)"
append_trunc_csv "$DATADIR/lj/verlet_864_200_equilibrated.csv" "LJ Velocity-Verlet Equilibrated NVE (N=864, 200 steps)"
append_trunc_csv "$DATADIR/lj/verlet_864_100_rescaled.csv" "LJ Velocity-Verlet with pure thermostat rescaling (N=864, 100 steps)"

# 4. HARMONIC OSCILLATOR CONVERGENCE (Truncated representations for dt=0.01)
append_trunc_csv "$DATADIR/ho/euler_dt0.01.csv" "HO Euler trajectory (dt=0.01)"
append_trunc_csv "$DATADIR/ho/verlet_dt0.01.csv" "HO Velocity-Verlet trajectory (dt=0.01)"
append_trunc_csv "$DATADIR/ho/rk4_dt0.01.csv" "HO RK4 trajectory (dt=0.01)"

echo "Results successfully bundled into $OUTFILE"
