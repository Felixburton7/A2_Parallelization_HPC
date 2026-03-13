#!/bin/bash
# ai/generate_all_context.sh — One command to regenerate all context files
set -euo pipefail
cd "$(dirname "$0")/.."

echo "=== Step 1/4: Audit ==="
bash ai/audit.sh

echo "=== Step 2/4: Results bundle ==="
bash ai/pack_results.sh

echo "=== Step 3/4: Results analysis ==="
bash ai/make_results.sh

echo "=== Step 4/4: Pack context ==="
bash ai/pack_context.sh

echo ""
echo "=== Context generation complete ==="
echo "Files to upload to LLM:"
echo "  1. ai/audit_output.md   ($(wc -c < ai/audit_output.md | tr -d ' ') bytes)"
echo "  2. ai/results.md        ($(wc -c < ai/results.md | tr -d ' ') bytes)"
echo "  3. ai/results_bundle.md ($(wc -c < ai/results_bundle.md | tr -d ' ') bytes)"
echo ""
echo "Combined context tarball:"
echo "  ai/context_bundle.tar.gz ($(du -h ai/context_bundle.tar.gz | cut -f1))"
