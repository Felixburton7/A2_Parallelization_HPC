#!/usr/bin/env python3
"""
append_manifest.py — Safely append/update a key path in out/manifest.json.

Usage:
  python3 scripts/append_manifest.py <key.path> <file_path>
"""

import json
import os
import sys
import tempfile
from pathlib import Path


def set_nested(data, key_path, value):
    keys = key_path.split(".")
    d = data
    for k in keys[:-1]:
        if k not in d or not isinstance(d[k], dict):
            d[k] = {}
        d = d[k]
    d[keys[-1]] = value


def load_manifest(path: Path):
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in {path}: {e}", file=sys.stderr)
        return None


def atomic_write(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def main():
    if len(sys.argv) != 3:
        print("Usage: append_manifest.py <key.path> <file_path>", file=sys.stderr)
        sys.exit(1)

    key_path = sys.argv[1]
    file_path = sys.argv[2]
    manifest_path = Path("out/manifest.json")

    data = load_manifest(manifest_path)
    if data is None:
        sys.exit(2)

    set_nested(data, key_path, file_path)
    atomic_write(manifest_path, data)


if __name__ == "__main__":
    main()
