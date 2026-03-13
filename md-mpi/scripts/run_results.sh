#!/bin/bash
# Generate the data and plots used in the report.
# Usage:
#   bash scripts/run_results.sh [--skip-scaling] [--live-scaling] [--reference-scaling] [--bind-to-core|--no-bind-to-core]

set -euo pipefail
cd "$(dirname "$0")/.."

# Remove old output so this run starts from a clean tree.
rm -rf out
mkdir -p out

bash scripts/run_all_data.sh "$@"

# Keep only the report figure files.
mkdir -p out/plots
find out/plots -maxdepth 1 -type f ! -name 'results*' -delete

python3 scripts/plot_ho.py
python3 scripts/plot_lj.py
python3 scripts/plot_scaling.py

# Remove internal helper outputs after plotting.
rm -f out/manifest.json
rm -rf out/summary out/plots/metadata
rm -f out/scaling_meta.txt out/scaling_strong_raw.csv out/scaling_size_raw.csv
rm -f out/scaling_strong_stats.csv out/scaling_size_stats.csv
