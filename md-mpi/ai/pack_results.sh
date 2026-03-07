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

# Helper function to append plain text/markdown/json sidecars
append_text_file() {
    local file="$1"
    local title="$2"
    local fence="${3:-}"
    if [ -f "$file" ]; then
        echo "## $title" >> "$OUTFILE"
        if [ -n "$fence" ]; then
            echo '```'"$fence" >> "$OUTFILE"
            cat "$file" >> "$OUTFILE"
            echo '```' >> "$OUTFILE"
        else
            cat "$file" >> "$OUTFILE"
        fi
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

manifest_get() {
    local key="$1"
    python3 - "$key" <<'PY'
import json
import sys
from pathlib import Path

key = sys.argv[1]
mpath = Path("out/manifest.json")
if not mpath.exists():
    sys.exit(0)
cur = json.loads(mpath.read_text(encoding="utf-8"))
for part in key.split("."):
    if not isinstance(cur, dict) or part not in cur:
        sys.exit(0)
    cur = cur[part]
if isinstance(cur, str):
    print(cur)
PY
}

# 1. RESULTS 2 PACKAGE ORDER
echo "## Results 2 Package Ordering" >> "$OUTFILE"
echo "Main/core evidence:" >> "$OUTFILE"
echo "1. out/plots/results2_lj_brief_energy_100step_production.png" >> "$OUTFILE"
echo "2. out/plots/results2_lj_brief_temperature_100step_production.png" >> "$OUTFILE"
echo "3. out/plots/results2_lj_rdf_comparison_rahman1964.png" >> "$OUTFILE"
echo "4. out/summary/results2/results2_quantitative_summary_table.md" >> "$OUTFILE"
echo "" >> "$OUTFILE"

append_text_file "out/summary/results2/results2_quantitative_summary_table.md" "Results 2 Quantitative Summary Table (Markdown)"
append_full_csv "out/summary/results2/results2_quantitative_summary_table.csv" "Results 2 Quantitative Summary Table (CSV)"
append_text_file "out/summary/results2/rahman1964_fig2_manual_anchors.csv" "Rahman Fig. 2 Manual Anchor Dataset" "csv"
append_text_file "out/summary/results2/results2_report_note.md" "Results 2 Report Note" "markdown"
append_text_file "out/summary/results2/results2_rahman_extraction_note.md" "Rahman Extraction Note" "markdown"

# 2. RADIAL DISTRIBUTION FUNCTION (Full)
GR_PATH=$(manifest_get "lj_rdf.verlet_long")
if [ -n "$GR_PATH" ]; then
    append_full_csv "$GR_PATH" "Radial Distribution Function g(r) (Long RDF production run)"
fi

# 3. LENNARD-JONES TRAJECTORIES (Truncated, from manifest keys)
LJ_BRIEF_VERLET=$(manifest_get "lj_brief.verlet")
LJ_BRIEF_EULER=$(manifest_get "lj_brief.euler")
if [ -n "$LJ_BRIEF_VERLET" ]; then append_trunc_csv "$LJ_BRIEF_VERLET" "LJ Brief (required) — Velocity-Verlet (100 steps)"; fi
if [ -n "$LJ_BRIEF_EULER" ]; then append_trunc_csv "$LJ_BRIEF_EULER" "LJ Brief (required) — Euler (100 steps)"; fi

# 4. SCALING DATA (Full)
append_full_csv "$(manifest_get "scaling.strong")" "Strong Scaling (median paired timings)"
append_full_csv "$(manifest_get "scaling.size")" "Size Scaling (median paired timings)"

# 5. HARMONIC OSCILLATOR CONVERGENCE SUMMARY
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

# 6. LJ RDF companion trajectory (if present)
LJ_RDF_ENERGY=$(manifest_get "lj_rdf.verlet_long_energy")
if [ -n "$LJ_RDF_ENERGY" ]; then
    append_trunc_csv "$LJ_RDF_ENERGY" "LJ RDF long run trajectory (energy/temperature)"
fi

echo "Results successfully bundled into $OUTFILE"
