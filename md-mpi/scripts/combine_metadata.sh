#!/usr/bin/env bash
set -euo pipefail

metadata_dir="out/plots/metadata"
output_file="$metadata_dir/all_metadata.txt"

if [ ! -d "$metadata_dir" ]; then
  echo "Metadata directory not found: $metadata_dir" >&2
  exit 1
fi

tmp_file="$(mktemp)"
trap 'rm -f "$tmp_file"' EXIT

find "$metadata_dir" -maxdepth 1 -type f -name '*.json' | sort | while IFS= read -r file; do
  printf '===== %s =====\n' "$(basename "$file")" >> "$tmp_file"
  cat "$file" >> "$tmp_file"
  printf '\n\n' >> "$tmp_file"
done

mv "$tmp_file" "$output_file"
trap - EXIT

printf 'Wrote %s\n' "$output_file"
