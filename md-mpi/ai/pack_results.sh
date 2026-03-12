#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# ai/pack_results.sh — Bundle project-wide raw artifacts into ai/results_bundle.md
# for LLM context ingestion with controlled truncation.
# ──────────────────────────────────────────────────────────────────

set -euo pipefail
cd "$(dirname "$0")/.."

OUTFILE="ai/results_bundle.md"
DATADIR="out"

mkdir -p ai

TMP_PREFACE="$(mktemp ai/results_bundle.preface.tmp.XXXXXX)"
TMP_BODY="$(mktemp ai/results_bundle.body.tmp.XXXXXX)"
TMP_WARN="$(mktemp ai/results_bundle.warn.tmp.XXXXXX)"
trap 'rm -f "$TMP_PREFACE" "$TMP_BODY" "$TMP_WARN"' EXIT

GEN_SUCCEEDED=true
GEN_STATUS="confirmed"
GEN_NOTE="Raw bundle assembled from current manifest-linked project artifacts."

warn() {
    echo "$1" >> "$TMP_WARN"
}

# Helper function to append a code snippet with line numbers
append_code_snippet() {
    local file="$1"
    local title="$2"
    local fence="$3"
    local start_line="$4"
    local end_line="$5"
    if [ -f "$file" ]; then
        echo "## $title" >> "$TMP_BODY"
        echo "" >> "$TMP_BODY"
        echo "Source: \`$file:$start_line-$end_line\`" >> "$TMP_BODY"
        echo '```'"$fence" >> "$TMP_BODY"
        nl -ba "$file" | sed -n "${start_line},${end_line}p" >> "$TMP_BODY"
        echo '```' >> "$TMP_BODY"
        echo "" >> "$TMP_BODY"
    else
        warn "missing expected code file for section '$title': $file"
    fi
}

# Helper function to append a full CSV
append_full_csv() {
    local file="$1"
    local title="$2"
    if [ -f "$file" ]; then
        echo "## $title" >> "$TMP_BODY"
        echo '```csv' >> "$TMP_BODY"
        cat "$file" >> "$TMP_BODY"
        echo '```' >> "$TMP_BODY"
        echo "" >> "$TMP_BODY"
    else
        warn "missing expected CSV for section '$title': $file"
    fi
}

# Helper function to append a truncated CSV
append_trunc_csv() {
    local file="$1"
    local title="$2"
    if [ -f "$file" ]; then
        echo "## $title (Truncated)" >> "$TMP_BODY"
        echo '```csv' >> "$TMP_BODY"
        head -n 10 "$file" >> "$TMP_BODY"
        echo "..." >> "$TMP_BODY"
        tail -n 5 "$file" >> "$TMP_BODY"
        echo '```' >> "$TMP_BODY"
        echo "" >> "$TMP_BODY"
    else
        warn "missing expected CSV for truncated section '$title': $file"
    fi
}

# Helper function to append plain text/markdown/json sidecars
append_text_file() {
    local file="$1"
    local title="$2"
    local fence="${3:-}"
    if [ -f "$file" ]; then
        echo "## $title" >> "$TMP_BODY"
        if [ -n "$fence" ]; then
            echo '```'"$fence" >> "$TMP_BODY"
            cat "$file" >> "$TMP_BODY"
            echo '```' >> "$TMP_BODY"
        else
            cat "$file" >> "$TMP_BODY"
        fi
        echo "" >> "$TMP_BODY"
    else
        warn "missing expected text artifact for section '$title': $file"
    fi
}

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
try:
    cur = json.loads(mpath.read_text(encoding="utf-8"))
except json.JSONDecodeError:
    sys.exit(0)
for part in key.split("."):
    if not isinstance(cur, dict) or part not in cur:
        sys.exit(0)
    cur = cur[part]
if isinstance(cur, str):
    print(cur)
PY
}

resolve_rdf_gr_path() {
    local path=""
    path="$(manifest_get "lj_rdf.verlet_long")"
    [ -n "$path" ] || path="$(manifest_get "lj_rdf.verlet")"
    [ -n "$path" ] || path="$(manifest_get "results2_outputs.rdf_csv")"
    [ -n "$path" ] || path="$(manifest_get "results2_outputs.rdf_gr_csv")"
    if [ -z "$path" ]; then
        path="$(ls -1t out/runs/lj_rdf_*/gr.csv out/runs/lj_rdf*/gr.csv 2>/dev/null | head -n 1 || true)"
    fi
    echo "$path"
}

resolve_rdf_energy_path() {
    local gr_path="$1"
    local path=""
    path="$(manifest_get "lj_rdf.verlet_long_energy")"
    [ -n "$path" ] || path="$(manifest_get "lj_rdf.verlet_energy")"
    [ -n "$path" ] || path="$(manifest_get "results2_outputs.rdf_energy_csv")"
    if [ -z "$path" ] && [ -n "$gr_path" ]; then
        local sibling
        sibling="$(dirname "$gr_path")/lj_verlet.csv"
        if [ -f "$sibling" ]; then
            path="$sibling"
        fi
    fi
    if [ -z "$path" ]; then
        path="$(ls -1t out/runs/lj_rdf_*/lj_verlet.csv out/runs/lj_rdf*/lj_verlet.csv 2>/dev/null | head -n 1 || true)"
    fi
    echo "$path"
}

{
    echo "## Raw Artifact Bundle (Verbatim / Truncated)"
    echo ""
    echo "This section preserves raw artifact payloads (with explicit truncation for long trajectories)."
    echo ""
} > "$TMP_BODY"

# Append manifest.json
if [ -f "$DATADIR/manifest.json" ]; then
    echo "## out/manifest.json" >> "$TMP_BODY"
    echo '```json' >> "$TMP_BODY"
    cat "$DATADIR/manifest.json" >> "$TMP_BODY"
    echo '```' >> "$TMP_BODY"
    echo "" >> "$TMP_BODY"
else
    GEN_SUCCEEDED=false
    GEN_STATUS="potential issue"
    GEN_NOTE="Manifest missing; bundle generated with partial content only."
    warn "required manifest missing: $DATADIR/manifest.json"
fi

# Package ordering (project-wide, not only Results 2)
{
    echo "## Current Package Ordering (Core Evidence First)"
    echo ""
    echo "1. out/manifest.json"
    echo "2. out/summary/results1/results1_ho_convergence_summary.csv"
    echo "3. out/summary/results2/results2_quantitative_summary_table.md"
    echo "4. out/plots/results2_figure6_lj_brief_energy_100step_production.png"
    echo "5. out/plots/results2_figure7_lj_brief_temperature_100step_production.png"
    echo "6. out/plots/results2_figure8_lj_rdf_comparison_rahman1964.png"
    echo "7. out/plots/results3_figure9ab_problem_size_scaling_fixed_p16.png"
    echo "8. out/plots/results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.png"
    echo "9. out/scaling_strong.csv"
    echo "10. out/scaling_size.csv"
    echo ""
} >> "$TMP_BODY"

{
    echo "## Report-Writing Notes and Plot Metadata"
    echo ""
    echo "This section pulls in the short human-readable notes and figure metadata sidecars that are most useful while drafting the Results section."
    echo ""
} >> "$TMP_BODY"

append_text_file "out/summary/results1/results1_ho_convergence_summary.md" "Results 1 HO Convergence Summary (Markdown)" "markdown"
append_full_csv "out/summary/results1/results1_ho_convergence_summary.csv" "Results 1 HO Convergence Summary (CSV)"
append_text_file "out/summary/results1/results1_ho_small_large_summary.md" "Results 1 Small-vs-Large Timestep Summary (Markdown)" "markdown"
append_full_csv "out/summary/results1/results1_ho_small_large_summary.csv" "Results 1 Small-vs-Large Timestep Summary (CSV)"
append_text_file "out/summary/results1/results1_ho_endpoint_values.md" "Results 1 Endpoint Values (Markdown)" "markdown"
append_full_csv "out/summary/results1/results1_ho_endpoint_values.csv" "Results 1 Endpoint Values (CSV)"
append_text_file "out/summary/results1/results1_results_section_notes.md" "Results 1 Results-Section Notes" "markdown"
append_text_file "out/summary/results1/results1_ho_caption_notes.md" "Results 1 Figure Caption Notes" "markdown"

append_text_file "out/summary/results2/results2_quantitative_summary_table.md" "Results 2 Quantitative Summary Table (Markdown)"
append_full_csv "out/summary/results2/results2_quantitative_summary_table.csv" "Results 2 Quantitative Summary Table (CSV)"
append_text_file "out/summary/results2/rahman1964_fig2_manual_anchors.csv" "Rahman Fig. 2 Manual Anchor Dataset" "csv"
append_text_file "out/summary/results2/results2_report_note.md" "Results 2 Report Note" "markdown"
append_text_file "out/summary/results2/results2_rahman_extraction_note.md" "Rahman Extraction Note" "markdown"
append_text_file "out/summary/results2/results2_recommended_figure_set.md" "Results 2 Recommended Figure Set" "markdown"
append_text_file "out/summary/results2/results2_what_changed_and_why.md" "Results 2 What Changed and Why" "markdown"

append_text_file "out/plots/metadata/results1_figure1ab_trajectories_dt0p01.json" "Plot Metadata: Results 1 Figure 1(a,b) Trajectories" "json"
append_text_file "out/plots/metadata/results1_figure1c_phase_space_dt0p01.json" "Plot Metadata: Results 1 Figure 1(c) Phase Space" "json"
append_text_file "out/plots/metadata/results1_figure2_small_vs_large_dt.json" "Plot Metadata: Results 1 Figure 2 Small-vs-Large dt" "json"
append_text_file "out/plots/metadata/results1_figure3_convergence_combined.json" "Plot Metadata: Results 1 Figure 3 Convergence" "json"
append_text_file "out/plots/metadata/results1_figure4_energy_diagnostic.json" "Plot Metadata: Results 1 Figure 4 Energy Diagnostic" "json"
append_text_file "out/plots/metadata/results2_figure6_lj_brief_energy_100step_production.json" "Plot Metadata: Results 2 Figure 6 Energy Drift" "json"
append_text_file "out/plots/metadata/results2_figure7_lj_brief_temperature_100step_production.json" "Plot Metadata: Results 2 Figure 7 Temperature" "json"
append_text_file "out/plots/metadata/results2_figure8_lj_rdf_comparison_rahman1964.json" "Plot Metadata: Results 2 Figure 8 RDF vs Rahman" "json"
append_text_file "out/plots/metadata/results3_figure9ab_problem_size_scaling_fixed_p16.json" "Plot Metadata: Results 3 Figure 9 Size Scaling" "json"
append_text_file "out/plots/metadata/results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.json" "Plot Metadata: Results 3 Figure 10 Strong Scaling" "json"

# Radial distribution function (full)
GR_PATH="$(resolve_rdf_gr_path)"
if [ -n "$GR_PATH" ]; then
    append_full_csv "$GR_PATH" "Radial Distribution Function g(r) (Long RDF production run)"
else
    warn "RDF g(r) path missing from expected manifest keys (lj_rdf.verlet_long/lj_rdf.verlet/results2_outputs.*) and no run-file fallback found"
fi

# LJ brief trajectories (truncated)
LJ_BRIEF_VERLET="$(manifest_get "lj_brief.verlet")"
LJ_BRIEF_EULER="$(manifest_get "lj_brief.euler")"
if [ -n "$LJ_BRIEF_VERLET" ]; then
    append_trunc_csv "$LJ_BRIEF_VERLET" "LJ Brief (required) — Velocity-Verlet (100 steps)"
else
    warn "manifest key missing or empty: lj_brief.verlet"
fi
if [ -n "$LJ_BRIEF_EULER" ]; then
    append_trunc_csv "$LJ_BRIEF_EULER" "LJ Brief (required) — Euler (100 steps)"
else
    warn "manifest key missing or empty: lj_brief.euler"
fi

# HO convergence endpoint snapshot
echo "## HO Convergence Summary (all dt values, final step only)" >> "$TMP_BODY"
echo '```csv' >> "$TMP_BODY"
echo "integrator,dt,x_final,v_final,E_total_final" >> "$TMP_BODY"
python3 - <<'PY' >> "$TMP_BODY"
import csv
import json
from pathlib import Path

manifest_path = Path("out/manifest.json")
if not manifest_path.exists():
    raise SystemExit(0)

try:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
except json.JSONDecodeError:
    raise SystemExit(0)

for key, fpath in sorted(manifest.get("ho_convergence", {}).items()):
    parts = key.split("_dt")
    if len(parts) != 2:
        continue
    integ = parts[0]
    dt = parts[1].replace("_", ".")
    csv_path = Path(fpath)
    if not csv_path.exists():
        continue
    with csv_path.open("r", encoding="utf-8") as csvf:
        lines = [line for line in csvf if line.strip() and not line.startswith("#")]
    if not lines:
        continue
    reader = csv.DictReader(lines)
    rows = list(reader)
    if not rows:
        continue
    final = rows[-1]
    print(f"{integ},{dt},{final.get('x','')},{final.get('v','')},{final.get('E_total','')}")
PY
echo '```' >> "$TMP_BODY"
echo "" >> "$TMP_BODY"

# LJ RDF companion trajectory (truncated)
LJ_RDF_ENERGY="$(resolve_rdf_energy_path "$GR_PATH")"
if [ -n "$LJ_RDF_ENERGY" ]; then
    append_trunc_csv "$LJ_RDF_ENERGY" "LJ RDF long run trajectory (energy/temperature)"
else
    warn "RDF companion trajectory path missing from expected manifest keys and run-file fallbacks"
fi

echo "## Results 3 Scaling Evidence Bundle" >> "$TMP_BODY"
echo "" >> "$TMP_BODY"
echo "This section makes Results 3 explicit: benchmark inputs, derived metadata, and the code path that turns timed MPI runs into the scaling claims used in the report." >> "$TMP_BODY"
echo "" >> "$TMP_BODY"

append_text_file "out/scaling_meta.txt" "Results 3 Hardware / Environment Snapshot" "text"
append_text_file "out/plots/metadata/results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.json" "Results 3 Strong Scaling Figure Metadata" "json"
append_text_file "out/plots/metadata/results3_figure9ab_problem_size_scaling_fixed_p16.json" "Results 3 Size Scaling Figure Metadata" "json"

# Scaling data (full/truncated)
STRONG_PATH="$(manifest_get "scaling.strong")"
SIZE_PATH="$(manifest_get "scaling.size")"
if [ -n "$STRONG_PATH" ]; then
    append_full_csv "$STRONG_PATH" "Results 3 Strong Scaling (median paired timings)"
else
    warn "manifest key missing or empty: scaling.strong"
fi
if [ -f "out/scaling_strong_stats.csv" ]; then
    append_full_csv "out/scaling_strong_stats.csv" "Results 3 Strong Scaling Spread Statistics"
else
    warn "missing expected scaling stats file: out/scaling_strong_stats.csv"
fi
if [ -f "out/scaling_strong_raw.csv" ]; then
    append_trunc_csv "out/scaling_strong_raw.csv" "Results 3 Strong Scaling Raw Repetition Samples"
else
    warn "missing expected scaling raw file: out/scaling_strong_raw.csv"
fi

if [ -n "$SIZE_PATH" ]; then
    append_full_csv "$SIZE_PATH" "Results 3 Size Scaling (median paired timings)"
else
    warn "manifest key missing or empty: scaling.size"
fi
if [ -f "out/scaling_size_stats.csv" ]; then
    append_full_csv "out/scaling_size_stats.csv" "Results 3 Size Scaling Spread Statistics"
else
    warn "missing expected scaling stats file: out/scaling_size_stats.csv"
fi
if [ -f "out/scaling_size_raw.csv" ]; then
    append_trunc_csv "out/scaling_size_raw.csv" "Results 3 Size Scaling Raw Repetition Samples"
else
    warn "missing expected scaling raw file: out/scaling_size_raw.csv"
fi

echo "## Important Code Snippets" >> "$TMP_BODY"
echo "" >> "$TMP_BODY"
echo "These excerpts are included so the bundle carries the implementation context behind the figures, not only the output tables." >> "$TMP_BODY"
echo "" >> "$TMP_BODY"

append_code_snippet "include/md/integrators.hpp" "Integrator Implementations Compared in Results 1/2" "cpp" 27 135
append_code_snippet "src/main.cpp" "MPI Position Exchange and Force Refresh Path" "cpp" 341 367
append_code_snippet "src/main.cpp" "Timed Production Loop and Max-Reduction Timing Output" "cpp" 430 505
append_code_snippet "scripts/run_all_data.sh" "Results 3 Benchmark Collection (20 Paired Repetitions, Median Pair Retained)" "bash" 203 253
append_code_snippet "scripts/plot_ho.py" "Results 1 Fit-Point Selection and Slope Construction" "python" 370 443
append_code_snippet "scripts/plot_ho.py" "Results 1 Convergence Figure and Metadata Generation" "python" 938 1015
append_code_snippet "scripts/plot_ho.py" "Results 1 Summary Table Generation" "python" 1136 1235
append_code_snippet "scripts/plot_lj.py" "Results 2 CSV Metadata Parsing and Production-Step Semantics" "python" 303 377
append_code_snippet "scripts/plot_lj.py" "Results 2 Energy Drift Extraction and Per-Integrator Summary" "python" 455 569
append_code_snippet "scripts/plot_lj.py" "Results 2 RDF Feature Extraction and Metadata Packaging" "python" 975 1230
append_code_snippet "scripts/plot_lj.py" "Results 2 Quantitative Summary Table Generation" "python" 1280 1355
append_code_snippet "scripts/plot_scaling.py" "Results 3 Strong Scaling Derivations (Speedup, Efficiency, Amdahl Fit)" "python" 140 255
append_code_snippet "scripts/plot_scaling.py" "Results 3 Size Scaling Derivations (Power-Law Fit and Communication Fraction)" "python" 345 445

{
    echo "## Diagnostics / Warnings (Bundle Generator)"
    echo ""
    if [ -s "$TMP_WARN" ]; then
        echo "- Status: potential issue"
        echo "- Generator warnings captured below:"
        echo '```'
        cat "$TMP_WARN"
        echo '```'
        GEN_STATUS="potential issue"
        if [ "$GEN_SUCCEEDED" = true ]; then
            GEN_NOTE="Bundle generated with warnings; review missing/empty artifact keys."
        fi
    else
        echo "- Status: confirmed"
        echo "- No bundle-generation warnings were emitted."
    fi
    echo ""
    echo "## Potentially Stale or Informational Items (Bundle View)"
    echo ""
    echo "- informational: Long trajectory files are intentionally truncated (head 10 + tail 5) for context size control."
    echo '- informational: Read `ai/results.md` for interpreted conclusions and confidence statements.'
    echo '- informational: Read `ai/audit_output.md` for executable build/test/smoke traces.'
    echo ""
} >> "$TMP_BODY"

python3 ai/context_report.py preface \
    --doc bundle \
    --generation-status "$GEN_STATUS" \
    --generation-succeeded "$GEN_SUCCEEDED" \
    --generation-note "$GEN_NOTE" \
    --preface-mode stub > "$TMP_PREFACE"

{
    cat "$TMP_PREFACE"
    echo ""
    cat "$TMP_BODY"
} > "$OUTFILE"

echo "Results successfully bundled into $OUTFILE"
