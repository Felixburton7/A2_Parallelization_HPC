#!/usr/bin/env python3
"""
plot_scaling.py - Generate scaling plots for Results 3.
"""

import os
import json
import glob
import numpy as np
import matplotlib.pyplot as plt

from plot_style import (
    COLOR_EULER,
    COLOR_REFERENCE,
    COLOR_RK4,
    COLOR_VERLET,
    apply_major_grid,
    apply_plot_style,
    disable_offset_text,
    save_figure,
)

PLOT_DIR = "out/plots"
FIG9_AB_PNG = "results3_figure9ab.png"
FIG10_ABC_PNG = "results3_figure10abc.png"
FIG11_AB_WEAK_PNG = "results3_figure11ab_weak.png"
RESULTS3_INTEGRATOR = "verlet"
RESULTS3_TIMESTEP_S = 1.0e-14
RESULTS3_SEED = 42
RESULTS3_REPETITIONS = 11
RESULTS3_STRONG_FIXED_N = 2048
RESULTS3_STRONG_TIMED_STEPS = 500
RESULTS3_SIZE_FIXED_P = 16
RESULTS3_SIZE_TIMED_STEPS = 2000
RESULTS3_PROTOCOL_SOURCE = "scripts/run_all_data.sh"
STALE_RESULTS3_PATTERNS = [
    # Legacy pre-results3 naming pattern; no longer part of report outputs.
    f"{PLOT_DIR}/scaling_*.png",
]


def load_manifest():
    manifest_path = "out/manifest.json"
    if not os.path.exists(manifest_path):
        print(f"Warning: manifest not found at {manifest_path}")
        return {}
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)
def add_panel_label(ax, label: str, x: float = -0.1, y: float = 1.05):
    ax.text(
        x,
        y,
        f"{label})",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=11,
        fontweight="bold",
        color="black",
    )


def set_panel_title(ax, title: str):
    # Keep panel titles aligned with panel labels and slightly lifted from the plot area.
    ax.set_title(title, loc="left", y=1.05, pad=3)


def remove_old_results3_files():
    for pattern in STALE_RESULTS3_PATTERNS:
        for path in glob.glob(pattern):
            os.remove(path)
            print(f"Removed old file {path}")


def load_scaling_csv(manifest, key):
    path = manifest.get("scaling", {}).get(key, "")
    if not os.path.exists(path):
        return None, path, False
    data = np.genfromtxt(path, delimiter=',', names=True, encoding=None)
    names = getattr(getattr(data, "dtype", None), "names", None)
    if names and "P" in names and "wall_s" in names:
        return data, path, False

    # Fallback: tolerate headerless CSVs ("P,N,wall_s,comm_max_s" missing).
    raw = np.genfromtxt(path, delimiter=',', encoding=None)
    if raw is None:
        return None, path, False
    if raw.ndim == 1:
        raw = np.array([raw])
    if raw.shape[1] < 4:
        return None, path, False
    out = np.zeros(raw.shape[0], dtype=[("P", float), ("N", float), ("wall_s", float), ("comm_max_s", float)])
    out["P"] = raw[:, 0]
    out["N"] = raw[:, 1]
    out["wall_s"] = raw[:, 2]
    out["comm_max_s"] = raw[:, 3]
    print(f"Warning: {path} missing header; parsed as a 4-column table.")
    return out, path, True


def amdahl(P, f):
    """Amdahl's Law: S(P) = 1 / (f + (1-f)/P)."""
    return 1.0 / (f + (1.0 - f) / P)


def plot_strong_scaling():
    """Plot speedup, efficiency, and critical-path comm breakdown."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    manifest = load_manifest()
    data, strong_path, used_fallback = load_scaling_csv(manifest, "strong")
    if data is None:
        print("Warning: scaling/strong not found in manifest. Skipping strong scaling.")
        return

    names = getattr(getattr(data, "dtype", None), "names", ()) or ()
    has_n_column = "N" in names

    P = data['P'].astype(int)
    wall = data['wall_s']
    comm_col = "comm_max_s" if "comm_max_s" in names else "comm_s"
    comm_max = data[comm_col]
    compute_overhead = np.maximum(wall - comm_max, 0.0)
    # Some exported strong-scaling tables omit N; Results 3 strong scaling uses fixed N=2048.
    N_values = data["N"].astype(int) if has_n_column else np.full(len(P), 2048, dtype=int)

    t1 = wall[0]
    speedup = t1 / wall
    efficiency = speedup / P

    # Fit Amdahl's Law using pure NumPy two-pass grid search
    def fit_amdahl(P_arr, S_obs):
        """Fit Amdahl serial fraction f by minimising SSE in S-space.
        Two-pass grid search: coarse (1e-3 resolution) then refined (1e-5).
        Uses pure NumPy, so no SciPy dependency is required."""
        best_f, best_sse = 0.0, 1e30
        # Coarse pass
        for f_trial in np.linspace(0.001, 0.999, 1000):
            S_model = 1.0 / (f_trial + (1.0 - f_trial) / P_arr)
            sse = np.sum((S_obs - S_model) ** 2)
            if sse < best_sse:
                best_f, best_sse = f_trial, sse
        # Refined pass around coarse optimum
        lo = max(0.0001, best_f - 0.002)
        hi = min(0.9999, best_f + 0.002)
        for f_trial in np.linspace(lo, hi, 10000):
            S_model = 1.0 / (f_trial + (1.0 - f_trial) / P_arr)
            sse = np.sum((S_obs - S_model) ** 2)
            if sse < best_sse:
                best_f, best_sse = f_trial, sse
        return best_f

    P_data = P[P > 1].astype(float)
    S_data = speedup[P > 1]
    f_fit = fit_amdahl(P_data, S_data) if len(P_data) > 0 else None

    if f_fit is not None:
        P_fit = np.linspace(1, max(P) * 1.1, 100)
        S_fit = amdahl(P_fit, f_fit)
    
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.8), constrained_layout=True)

    # --- Panel 1: Speedup ---
    ax1 = axes[0]
    ax1.plot(P, speedup, "o-", color=COLOR_VERLET, linewidth=2.0, markersize=6, label="Measured")
    ax1.plot(P, P.astype(float), "--", color=COLOR_REFERENCE, alpha=0.9, linewidth=1.5, label="Ideal (S=P)")
    if f_fit is not None:
        ax1.plot(P_fit, S_fit, "-", color=COLOR_EULER, linewidth=1.6, label=f"Amdahl fit (f={f_fit:.4f})")
    ax1.set_xlabel("Number of Processes P")
    ax1.set_ylabel("Speedup S(P)")
    set_panel_title(ax1, "Strong Scaling: Speedup")
    add_panel_label(ax1, "a")
    ax1.legend(loc="best")
    apply_major_grid(ax1)
    disable_offset_text(ax1)

    # --- Panel 2: Efficiency ---
    ax2 = axes[1]
    ax2.plot(P, efficiency, "o-", color=COLOR_RK4, linewidth=2.0, markersize=6, label="Measured efficiency")
    ax2.axhline(y=1.0, color=COLOR_REFERENCE, linestyle="--", alpha=0.9, linewidth=1.3, label="Ideal (E=1)")
    ax2.set_xlabel("Number of Processes P")
    ax2.set_ylabel("Efficiency E(P) = S(P)/P")
    set_panel_title(ax2, "Strong Scaling: Efficiency")
    add_panel_label(ax2, "b")
    ax2.set_ylim(0, 1.15)
    ax2.legend(loc="best")
    apply_major_grid(ax2)
    disable_offset_text(ax2)

    # Panel 3: stacked bar chart for remaining runtime and critical-path communication
    ax3 = axes[2]
    x_pos = np.arange(len(P))
    bar_width = 0.6
    remaining_display = np.maximum(compute_overhead, 0.0)
    ax3.bar(
        x_pos,
        remaining_display,
        bar_width,
        label="Remaining runtime (wall - comm_max)",
        color=COLOR_VERLET,
        alpha=0.85,
    )
    ax3.bar(
        x_pos,
        comm_max,
        bar_width,
        bottom=remaining_display,
        label="Communication (critical-path max)",
        color=COLOR_EULER,
        alpha=0.85,
    )
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([str(p) for p in P])
    ax3.set_xlabel("Number of Processes P")
    ax3.set_ylabel("Wall Time [s]")
    set_panel_title(ax3, "Critical-Path Communication vs Remaining Runtime")
    add_panel_label(ax3, "c")
    ax3.legend(loc="best")
    apply_major_grid(ax3, axis="y")
    disable_offset_text(ax3)

    save_figure(fig, f"{PLOT_DIR}/{FIG10_ABC_PNG}")
    plt.close()
    print(f"Saved {PLOT_DIR}/{FIG10_ABC_PNG}")

    if f_fit is not None:
        print(f"  Amdahl serial fraction f = {f_fit:.6f}")
        print(f"  Maximum theoretical speedup = {1.0/f_fit:.1f}x")


def plot_size_scaling():
    """Plot wall time and wall-minus-comm_max runtime vs N."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    manifest = load_manifest()
    data, size_path, used_fallback = load_scaling_csv(manifest, "size")
    if data is None:
        print("Warning: scaling/size not found in manifest. Skipping size scaling.")
        return
    names = getattr(getattr(data, "dtype", None), "names", ()) or ()
    if "N" not in names:
        print("Warning: scaling/size is missing N column. Skipping size scaling plot.")
        return

    N = data['N']
    wall = data['wall_s']
    comm_col = "comm_max_s" if "comm_max_s" in names else "comm_s"
    comm_max = data[comm_col]
    remaining_runtime = np.maximum(wall - comm_max, 1e-9)  # floor to avoid log(0)

    # Fit power law to wall-minus-comm_max runtime for N >= 500
    mask = N >= 500
    slope_remaining, intercept_remaining = None, None
    slope_wall, intercept_wall = None, None
    if np.sum(mask) >= 2:
        log_N = np.log10(N[mask])
        log_remaining = np.log10(np.maximum(remaining_runtime[mask], 1e-10))
        slope_remaining, intercept_remaining = np.polyfit(log_N, log_remaining, 1)
        
        log_wall = np.log10(wall[mask])
        slope_wall, intercept_wall = np.polyfit(log_N, log_wall, 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 4.8), constrained_layout=True)

    wall_label = 'Wall time'
    if slope_wall is not None:
        wall_label += f' (O(N^{slope_wall:.2f}))'
    ax1.loglog(N, wall, "o-", color=COLOR_VERLET, linewidth=2.0, markersize=6, label=wall_label)
    
    rem_label = 'Remaining runtime (wall - comm_max)'
    if slope_remaining is not None:
        rem_label += f' (O(N^{slope_remaining:.2f}))'
    ax1.loglog(N, remaining_runtime, "^-", color=COLOR_RK4, linewidth=2.0, markersize=6, label=rem_label)

    ax1.loglog(
        N,
        comm_max,
        "s--",
        color=COLOR_EULER,
        linewidth=1.5,
        markersize=5,
        label="Comm time (max)",
        alpha=0.9,
    )
    N_ref = np.array([min(N), max(N)])
    t_ref = wall[-1] * (N_ref / N[-1]) ** 2
    ax1.loglog(N_ref, t_ref, "--", color=COLOR_REFERENCE, alpha=0.9, linewidth=1.5, label=r"$\sim N^2$ reference")
    ax1.set_xlabel("Number of Particles N")
    ax1.set_ylabel("Time [s]")
    set_panel_title(ax1, "Size Scaling (P=16)")
    add_panel_label(ax1, "a")
    ax1.legend(loc="best")
    apply_major_grid(ax1)

    comm_frac = comm_max / wall * 100
    ax2.plot(N, comm_frac, "o-", color=COLOR_EULER, linewidth=2.0, markersize=6)
    ax2.set_xlabel("Number of Particles N")
    ax2.set_ylabel("Communication Fraction [%]")
    set_panel_title(ax2, "Communication Overhead vs Problem Size")
    add_panel_label(ax2, "b")
    ax2.set_ylim(0, 100)
    apply_major_grid(ax2)
    ax2.axhline(y=50, color=COLOR_REFERENCE, linestyle="--", linewidth=1.2, label="50% reference")
    ax2.legend(loc="best")
    disable_offset_text(ax2)

    save_figure(fig, f"{PLOT_DIR}/{FIG9_AB_PNG}")
    plt.close()
    print(f"Saved {PLOT_DIR}/{FIG9_AB_PNG}")


def plot_weak_scaling():
    os.makedirs(PLOT_DIR, exist_ok=True)

    weak_path = "out/scaling_weak.csv"
    if not os.path.exists(weak_path):
        print(f"Warning: {weak_path} not found. Skipping weak scaling.")
        return

    data = np.genfromtxt(weak_path, delimiter=",", names=True, encoding=None)
    names = getattr(getattr(data, "dtype", None), "names", None)
    if not names or "P" not in names or "wall_s" not in names:
        raw = np.genfromtxt(weak_path, delimiter=",", encoding=None)
        if raw is None:
            print(f"Warning: {weak_path} is empty. Skipping weak scaling.")
            return
        if raw.ndim == 1:
            raw = np.array([raw])
        if raw.shape[1] < 4:
            print(f"Warning: {weak_path} does not have 4 columns. Skipping weak scaling.")
            return
        data = np.zeros(raw.shape[0], dtype=[("P", float), ("N", float), ("wall_s", float), ("comm_max_s", float)])
        data["P"] = raw[:, 0]
        data["N"] = raw[:, 1]
        data["wall_s"] = raw[:, 2]
        data["comm_max_s"] = raw[:, 3]
        names = data.dtype.names

    data = np.atleast_1d(data)
    P = data["P"].astype(int)
    wall = data["wall_s"].astype(float)
    comm_col = "comm_max_s" if "comm_max_s" in names else "comm_s"
    comm_max = data[comm_col].astype(float)

    order = np.argsort(P)
    P = P[order]
    wall = wall[order]
    comm_max = comm_max[order]

    baseline_wall = wall[0]
    p1_mask = P == 1
    if np.any(p1_mask):
        baseline_wall = wall[p1_mask][0]

    comm_frac = np.where(wall > 0.0, (comm_max / wall) * 100.0, 0.0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 4.8), constrained_layout=True)

    ax1.plot(P, wall, "o-", color=COLOR_VERLET, linewidth=2.0, markersize=6, label="Wall time")
    ax1.axhline(
        y=baseline_wall,
        color=COLOR_REFERENCE,
        linestyle="--",
        alpha=0.9,
        linewidth=1.5,
        label="Baseline compute time (P=1)",
    )
    ax1.set_xlabel("Number of Processes P")
    ax1.set_ylabel("Wall Time [s]")
    ax1.set_xticks(P)
    add_panel_label(ax1, "a")
    ax1.legend(loc="best")
    apply_major_grid(ax1)
    disable_offset_text(ax1)

    ax2.plot(P, comm_frac, "o-", color=COLOR_EULER, linewidth=2.0, markersize=6)
    ax2.set_xlabel("Number of Processes P")
    ax2.set_ylabel("Communication Fraction [%]")
    ax2.set_xticks(P)
    add_panel_label(ax2, "b")
    apply_major_grid(ax2)
    disable_offset_text(ax2)

    save_figure(fig, f"{PLOT_DIR}/{FIG11_AB_WEAK_PNG}")
    plt.close()
    print(f"Saved {PLOT_DIR}/{FIG11_AB_WEAK_PNG}")


if __name__ == "__main__":
    apply_plot_style()
    remove_old_results3_files()
    plot_strong_scaling()
    plot_size_scaling()
    plot_weak_scaling()
