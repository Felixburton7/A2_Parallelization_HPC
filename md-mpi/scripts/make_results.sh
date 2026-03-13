#!/bin/bash
# Keep the older script name working by forwarding to run_results.sh.

set -euo pipefail
cd "$(dirname "$0")/.."

# Older flag kept so existing commands still work; data generation already runs here.
if [ "${1:-}" = "--generate-data" ]; then
  shift
fi

exec bash scripts/run_results.sh "$@"
