#!/usr/bin/env python3
"""
validate_manifest.py — Ensure out/manifest.json has expected keys and valid paths.
"""

import argparse
import json
import sys
from pathlib import Path


DT_KEYS = ["1_0", "0_5", "0_1", "0_05", "0_01", "0_005", "0_001", "0_0005"]
INTEGRATORS = ["euler", "verlet", "rk4"]


def nested_get(obj, dotted):
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def require_file(manifest, key, errors):
    value = nested_get(manifest, key)
    if not value:
        errors.append(f"missing key: {key}")
        return
    p = Path(value)
    if not p.exists():
        errors.append(f"missing file for {key}: {value}")


def check_scaling_header(path, errors):
    p = Path(path)
    if not p.exists():
        errors.append(f"missing scaling file: {path}")
        return
    try:
        first = p.read_text(encoding="utf-8", errors="replace").splitlines()[0].strip()
    except IndexError:
        first = ""
    if first != "P,N,wall_s,comm_s":
        errors.append(
            f"bad header in {path}: '{first}' (expected 'P,N,wall_s,comm_s')"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="out/manifest.json")
    parser.add_argument("--skip-scaling", action="store_true")
    args = parser.parse_args()

    mpath = Path(args.manifest)
    if not mpath.exists():
        print(f"ERROR: missing manifest: {args.manifest}", file=sys.stderr)
        sys.exit(1)

    try:
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid manifest JSON: {e}", file=sys.stderr)
        sys.exit(1)

    errors = []

    for integ in INTEGRATORS:
        for dt in DT_KEYS:
            require_file(manifest, f"ho_convergence.{integ}_dt{dt}", errors)

    require_file(manifest, "lj_production.verlet_100", errors)
    require_file(manifest, "lj_production.euler_100", errors)
    require_file(manifest, "lj_production.verlet_200_equilibrated", errors)
    require_file(manifest, "lj_gr", errors)
    require_file(manifest, "lj_gr_energy", errors)

    if not args.skip_scaling:
        require_file(manifest, "scaling.strong", errors)
        require_file(manifest, "scaling.size", errors)
        strong = nested_get(manifest, "scaling.strong")
        size = nested_get(manifest, "scaling.size")
        if strong:
            check_scaling_header(strong, errors)
        if size:
            check_scaling_header(size, errors)

    if errors:
        print("Manifest validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("Manifest validation OK")


if __name__ == "__main__":
    main()
