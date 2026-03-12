#!/bin/bash
# Run end-to-end Results data generation and plotting.
# Usage:
#   bash scripts/run_results.sh [--skip-scaling] [--live-scaling] [--reference-scaling] [--bind-to-core|--no-bind-to-core]

set -euo pipefail
cd "$(dirname "$0")/.."

# Start from a clean output tree to avoid mixing stale and fresh artifacts.
rm -rf out
mkdir -p out

bash scripts/run_all_data.sh "$@"

# Keep only canonical report plot artifacts (results*.png + results*.json metadata).
mkdir -p out/plots out/plots/metadata
find out/plots -maxdepth 1 -type f ! -name 'results*' -delete
find out/plots/metadata -maxdepth 1 -type f -name '*.json' ! -name 'results*.json' -delete

python3 scripts/plot_ho.py
python3 scripts/plot_lj.py
python3 scripts/plot_scaling.py
