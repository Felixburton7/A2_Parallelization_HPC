#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# ai/pack_context.sh — Bundle raw project artefacts for external sharing
#
# Usage (from repo root):
#   bash ai/pack_context.sh
#
# Produces ai/context_bundle.tar.gz containing:
#   out/manifest.json
#   out/plots/*.png
#   selected CSVs referenced by the manifest
#   organised summary artefacts under out/summary/
# ──────────────────────────────────────────────────────────────────

set -euo pipefail
cd "$(dirname "$0")/.."

BUNDLE="ai/context_bundle.tar.gz"
FILELIST=$(mktemp)
trap 'rm -f "$FILELIST"' EXIT

# Include manifest
if [ -f out/manifest.json ]; then
    echo "out/manifest.json" >> "$FILELIST"
else
    echo "WARNING: out/manifest.json not found" >&2
fi

# Include current report plots only (avoid stale legacy PNGs).
for p in \
    out/plots/results1_figure1ab_trajectories_dt0p01.png \
    out/plots/results1_figure1c_phase_space_dt0p01.png \
    out/plots/results1_figure2_small_vs_large_dt.png \
    out/plots/results1_figure3_convergence_combined.png \
    out/plots/results1_figure4_energy_diagnostic.png \
    out/plots/results2_figure6_lj_brief_energy_100step_production.png \
    out/plots/results2_figure7_lj_brief_temperature_100step_production.png \
    out/plots/results2_figure8_lj_rdf_comparison_rahman1964.png \
    out/plots/results3_figure9ab_problem_size_scaling_fixed_p16.png \
    out/plots/results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.png
do
    if [ -f "$p" ]; then
        echo "$p" >> "$FILELIST"
    fi
done

# Include CSVs referenced by manifest (parse with Python)
if [ -f out/manifest.json ]; then
    python3 -c "
import json, os, sys
def walk(obj):
    if isinstance(obj, str) and obj.endswith('.csv'):
        if os.path.exists(obj):
            print(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            walk(v)
with open('out/manifest.json') as f:
    walk(json.load(f))
" >> "$FILELIST"
fi

# Include scaling CSVs explicitly (they may not be in manifest via nested path)
for f in out/scaling_strong.csv out/scaling_size.csv; do
    if [ -f "$f" ]; then
        echo "$f" >> "$FILELIST"
    fi
done

# Include generated summary/note artifacts (organized outputs).
if [ -d out/summary ]; then
    find out/summary -type f ! -path "out/summary/results1/legacy_root_migrated/*" | sort >> "$FILELIST"
fi

# Deduplicate
sort -u "$FILELIST" -o "$FILELIST"

# Create the archive
tar -czf "$BUNDLE" -T "$FILELIST"

echo "Created $BUNDLE containing:"
cat "$FILELIST" | sed 's/^/  /'
echo ""
echo "Total files: $(wc -l < "$FILELIST" | tr -d ' ')"
echo "Archive size: $(du -h "$BUNDLE" | cut -f1)"
