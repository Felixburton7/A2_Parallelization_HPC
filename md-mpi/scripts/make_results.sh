#!/bin/bash
# Thin compatibility wrapper.
# Use --generate-data to run production data generation before writing results.

set -euo pipefail
cd "$(dirname "$0")/.."

if [ "${1:-}" = "--generate-data" ]; then
  shift
  bash scripts/run_all_data.sh "$@"
fi

bash ai/make_results.sh
