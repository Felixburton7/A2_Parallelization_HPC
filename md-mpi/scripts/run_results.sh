#!/bin/bash
# Run end-to-end Results data generation and plotting.
# Usage:
#   bash scripts/run_results.sh [--skip-scaling]

set -euo pipefail
cd "$(dirname "$0")/.."

bash scripts/run_all_data.sh "$@"
python3 scripts/plot_ho.py
python3 scripts/plot_lj.py
python3 scripts/plot_scaling.py
