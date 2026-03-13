#!/usr/bin/env python3
"""
check_gr_tolerance.py - Compare two g(r) CSV files with tolerances.

Usage:
  python3 scripts/check_gr_tolerance.py <gr_p1.csv> <gr_p2.csv>
"""

import csv
import sys


ABS_TOL = 1e-6
REL_TOL = 1e-5


def filter_comments(handle):
    for line in handle:
        if line.strip() and not line.startswith("#"):
            yield line


def as_rows(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return list(csv.DictReader(filter_comments(f)))


def close_enough(a, b):
    diff = abs(a - b)
    if diff <= ABS_TOL:
        return True
    return diff / (abs(a) + 1e-18) <= REL_TOL


def main():
    if len(sys.argv) != 3:
        print("Usage: check_gr_tolerance.py <gr_p1.csv> <gr_p2.csv>")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]
    try:
        rows1 = as_rows(file1)
        rows2 = as_rows(file2)
    except Exception as exc:
        print(f"Error reading g(r) files: {exc}")
        sys.exit(1)

    if len(rows1) != len(rows2):
        print(f"Length mismatch: {len(rows1)} vs {len(rows2)}")
        sys.exit(1)

    for i, (r1, r2) in enumerate(zip(rows1, rows2)):
        try:
            x1 = float(r1["r_sigma"])
            x2 = float(r2["r_sigma"])
            g1 = float(r1["gr"])
            g2 = float(r2["gr"])
        except Exception as exc:
            print(f"Malformed row {i}: {exc}")
            sys.exit(1)

        if not close_enough(x1, x2):
            print(f"Mismatch at row {i}, col r_sigma: {x1} vs {x2}")
            sys.exit(1)
        if not close_enough(g1, g2):
            print(f"Mismatch at row {i}, col gr: {g1} vs {g2}")
            sys.exit(1)

    print("MATCH")
    sys.exit(0)


if __name__ == "__main__":
    main()
