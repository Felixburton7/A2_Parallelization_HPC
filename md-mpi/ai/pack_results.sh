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

# Append manifest.json
if [ -f "$DATADIR/manifest.json" ]; then
    echo "## out/manifest.json" >> "$OUTFILE"
    echo '```json' >> "$OUTFILE"
    cat "$DATADIR/manifest.json" >> "$OUTFILE"
    echo '```' >> "$OUTFILE"
    echo "" >> "$OUTFILE"
fi

get_latest_file() {
    ls -1t $1 2>/dev/null | head -n 1
}

# 1. SCALING DATA (Full)
append_full_csv "$DATADIR/scaling_strong.csv" "Strong Scaling (N=2048, P=1..32)"
append_full_csv "$DATADIR/scaling_size.csv" "Size Scaling (P=16, N=108..2048)"

# 2. RADIAL DISTRIBUTION FUNCTION (Full)
GR_LATEST=$(get_latest_file "$DATADIR/runs/lj_*_gr_*/gr.csv")
if [ -n "$GR_LATEST" ]; then
    append_full_csv "$GR_LATEST" "Radial Distribution Function g(r) (Latest)"
fi

# 3. LENNARD-JONES TRAJECTORIES (Truncated)
LJ_VERLET=$(get_latest_file "$DATADIR/runs/lj_N864_*_verlet_100_*/lj_verlet.csv")
LJ_EULER=$(get_latest_file "$DATADIR/runs/lj_N864_*_euler_100_*/lj_euler.csv")
if [ -n "$LJ_VERLET" ]; then append_trunc_csv "$LJ_VERLET" "LJ Velocity-Verlet NVE (N=864, 100 steps)"; fi
if [ -n "$LJ_EULER" ]; then append_trunc_csv "$LJ_EULER" "LJ Euler NVE (N=864, 100 steps)"; fi

# 4. HARMONIC OSCILLATOR CONVERGENCE SUMMARY
echo "## HO Convergence Summary (all dt values, final step only)" >> "$OUTFILE"
echo '```csv' >> "$OUTFILE"
echo "integrator,dt,x_final,v_final,E_total_final" >> "$OUTFILE"
python3 -c "
import json, csv
with open('out/manifest.json') as f:
    m = json.load(f)
for key, fpath in sorted(m.get('ho_convergence', {}).items()):
    parts = key.split('_dt')
    if len(parts) != 2:
        continue
    integ = parts[0]
    dt = parts[1].replace('_', '.')
    try:
        with open(fpath) as csvf:
            lines = [l for l in csvf if l.strip() and not l.startswith('#')]
            reader = csv.DictReader(lines)
            rows = list(reader)
            if rows:
                r = rows[-1]
                print(f\"{integ},{dt},{r['x']},{r['v']},{r['E_total']}\")
    except:
        pass
" >> "$OUTFILE"
echo '```' >> "$OUTFILE"
echo "" >> "$OUTFILE"

# 5. LJ EQUILIBRATED RUNS (if present)
for f in $(find "$DATADIR/runs" -name "lj_verlet.csv" -path "*_gr_*" -o -name "lj_verlet.csv" -path "*25500*" 2>/dev/null | head -3); do
    append_trunc_csv "$f" "LJ Equilibrated Run ($(dirname $f | xargs basename))"
done

# 6. MPI CONSISTENCY DATA
for P in 1 2 4; do
    if [ -f "$DATADIR/audit_p${P}/lj_verlet.csv" ]; then
        append_full_csv "$DATADIR/audit_p${P}/lj_verlet.csv" "MPI Consistency P=$P (N=108, 5 steps)"
    fi
done

echo "Results successfully bundled into $OUTFILE"
