#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# ai/make_results.sh — Generate ai/results.md from existing out/ data
#
# Usage (from repo root):
#   bash ai/make_results.sh
#
# Never regenerates data. Only summarises what exists.
# ──────────────────────────────────────────────────────────────────

set -euo pipefail
cd "$(dirname "$0")/.."

OUT="ai/results.md"
mkdir -p ai

TMP_PREFACE="$(mktemp ai/results.preface.tmp.XXXXXX)"
TMP_BODY="$(mktemp ai/results.body.tmp.XXXXXX)"
TMP_ERR="$(mktemp ai/results.err.tmp.XXXXXX)"
trap 'rm -f "$TMP_PREFACE" "$TMP_BODY" "$TMP_ERR"' EXIT

GEN_SUCCEEDED=true
GEN_STATUS="confirmed"
GEN_NOTE="Report-writing oriented analysis generated from current manifest-linked outputs."

: > "$TMP_BODY"

if [ ! -f out/manifest.json ]; then
    GEN_SUCCEEDED=false
    GEN_STATUS="potential issue"
    GEN_NOTE="Manifest missing; generated only partial guidance."
    {
        echo "**Manifest check:** potential issue"
        echo ""
        echo "- Missing file: \`out/manifest.json\`"
        echo "- To regenerate data artifacts, run:"
        echo '```bash'
        echo "bash scripts/run_all_data.sh"
        echo '```'
        echo ""
    } >> "$TMP_BODY"
else
    if python3 ai/report_writer_context.py >> "$TMP_BODY" 2>> "$TMP_ERR"; then
        :
    else
        GEN_SUCCEEDED=false
        GEN_STATUS="potential issue"
        GEN_NOTE="Report-writing pack generation reported an execution error; diagnostics captured."
    fi
    {
        echo "## Generated Result Summaries (Detailed)"
        echo ""
        echo "The section below is the detailed verbatim analyzer output from \`ai/analyse_results.py\`."
        echo ""
    } >> "$TMP_BODY"
    if python3 ai/analyse_results.py all >> "$TMP_BODY" 2>> "$TMP_ERR"; then
        :
    else
        GEN_SUCCEEDED=false
        GEN_STATUS="potential issue"
        GEN_NOTE="Analyzer reported an execution error; diagnostics captured."
    fi
fi

{
    echo ""
    echo "## Diagnostics / Warnings (Results Generator)"
    echo ""
    if [ -s "$TMP_ERR" ]; then
        echo "- Status: potential issue"
        echo "- Analyzer stderr output captured below:"
        echo '```'
        cat "$TMP_ERR"
        echo '```'
    else
        echo "- Status: confirmed"
        echo "- No stderr warnings were emitted during results analysis generation."
    fi
    echo ""
    echo "## Potentially Stale or Informational Items (Results View)"
    echo ""
    echo "- informational: This file summarizes existing outputs and does not regenerate simulation data."
    echo "- informational: For raw artifact payloads and longer CSV context, also read \`ai/results_bundle.md\`."
    echo "- informational: For executable build/test traces and source snapshots, also read \`ai/audit_output.md\`."
    echo ""
} >> "$TMP_BODY"

python3 ai/context_report.py preface \
    --doc results \
    --generation-status "$GEN_STATUS" \
    --generation-succeeded "$GEN_SUCCEEDED" \
    --generation-note "$GEN_NOTE" \
    --preface-mode full > "$TMP_PREFACE"

{
    cat "$TMP_PREFACE"
    echo ""
    cat "$TMP_BODY"
} > "$OUT"

echo "results.md written to $OUT"
