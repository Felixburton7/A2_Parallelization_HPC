#!/usr/bin/env python3
"""
plot_scaling.py — Generate scaling analysis plots (Results 3).

Produces:
  1. Strong scaling: Speedup S(P) with Amdahl's Law fit
  2. Efficiency E(P) = S(P)/P
  3. Stacked bar chart: Compute vs Communication time
  4. Size scaling: Wall time vs N with O(N²) reference

Usage:
  python3 scripts/plot_scaling.py

Prerequisites (from manifest.json):
  scaling.strong -> out/scaling_strong.csv  (columns: P,N,wall_s,comm_s)
  scaling.size   -> out/scaling_size.csv    (columns: P,N,wall_s,comm_s)
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt

PLOT_DIR = "out/plots"


def load_manifest():
    with open("out/manifest.json", "r") as f:
        return json.load(f)


def load_scaling_csv(key):
    manifest = load_manifest()
    path = manifest.get("scaling", {}).get(key, "")
    if not os.path.exists(path):
        return None
    data = np.genfromtxt(path, delimiter=',', names=True, encoding=None)
    names = getattr(getattr(data, "dtype", None), "names", None)
    if names and "P" in names and "wall_s" in names:
        return data

    # Fallback: tolerate headerless CSVs ("P,N,wall_s,comm_s" missing).
    raw = np.genfromtxt(path, delimiter=',', encoding=None)
    if raw is None:
        return None
    if raw.ndim == 1:
        raw = np.array([raw])
    if raw.shape[1] < 4:
        return None
    out = np.zeros(raw.shape[0], dtype=[("P", float), ("N", float), ("wall_s", float), ("comm_s", float)])
    out["P"] = raw[:, 0]
    out["N"] = raw[:, 1]
    out["wall_s"] = raw[:, 2]
    out["comm_s"] = raw[:, 3]
    print(f"Warning: {path} missing header; parsed as 4-column numeric fallback.")
    return out


def amdahl(P, f):
    """Amdahl's Law: S(P) = 1 / (f + (1-f)/P)."""
    return 1.0 / (f + (1.0 - f) / P)


def plot_strong_scaling():
    """Plot speedup, efficiency, and compute/comm breakdown."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    data = load_scaling_csv("strong")
    if data is None:
        print("Warning: scaling/strong not found in manifest. Skipping strong scaling.")
        return

    P = data['P'].astype(int)
    wall = data['wall_s']
    comm = data['comm_s']
    compute = np.maximum(wall - comm, 1e-9)  # floor to avoid log(0) at small N

    t1 = wall[0]
    speedup = t1 / wall
    efficiency = speedup / P

    # Fit Amdahl's Law using pure NumPy two-pass grid search
    def fit_amdahl(P_arr, S_obs):
        """Fit Amdahl serial fraction f by minimising SSE in S-space.
        Two-pass grid search: coarse (1e-3 resolution) then refined (1e-5).
        Uses pure NumPy — no SciPy dependency, for cluster portability."""
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
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # --- Panel 1: Speedup ---
    ax1 = axes[0]
    ax1.plot(P, speedup, 'o-', color='tab:green', linewidth=2, markersize=8, label='Measured')
    ax1.plot(P, P.astype(float), 'k--', alpha=0.5, linewidth=1.5, label='Ideal (S=P)')
    if f_fit is not None:
        ax1.plot(P_fit, S_fit, '-', color='tab:red', linewidth=1.5,
                 label=f'Amdahl fit (f={f_fit:.4f})')
    ax1.set_xlabel('Number of Processes P')
    ax1.set_ylabel('Speedup S(P)')
    ax1.set_title('Strong Scaling: Speedup')
    ax1.legend(fontsize=10)
    ax1.grid(True)

    # --- Panel 2: Efficiency ---
    ax2 = axes[1]
    ax2.plot(P, efficiency, 'o-', color='tab:blue', linewidth=2, markersize=8)
    ax2.axhline(y=1.0, color='k', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Number of Processes P')
    ax2.set_ylabel('Efficiency E(P) = S(P)/P')
    ax2.set_title('Strong Scaling: Efficiency')
    ax2.set_ylim(0, 1.15)
    ax2.grid(True)

    # --- Panel 3: Stacked bar — Compute vs Communication ---
    ax3 = axes[2]
    x_pos = np.arange(len(P))
    bar_width = 0.6
    compute_display = np.maximum(compute, 0)
    ax3.bar(x_pos, compute_display, bar_width, label='Compute', color='tab:green', alpha=0.8)
    ax3.bar(x_pos, comm, bar_width, bottom=compute_display, label='Communication',
            color='tab:red', alpha=0.8)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([str(p) for p in P])
    ax3.set_xlabel('Number of Processes P')
    ax3.set_ylabel('Wall Time [s]')
    ax3.set_title('Compute vs Communication Time')
    ax3.legend(fontsize=10)
    ax3.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/scaling_strong.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/scaling_strong.png")

    if f_fit is not None:
        print(f"  Amdahl serial fraction f = {f_fit:.6f}")
        print(f"  Maximum theoretical speedup = {1.0/f_fit:.1f}x")


def plot_size_scaling():
    """Plot wall time and compute time vs N."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    data = load_scaling_csv("size")
    if data is None:
        print("Warning: scaling/size not found in manifest. Skipping size scaling.")
        return

    N = data['N']
    wall = data['wall_s']
    comm = data['comm_s']
    compute = np.maximum(wall - comm, 1e-9)  # floor to avoid log(0) at small N

    # Fit power law to compute time (wall - comm) for N >= 500
    mask = N >= 500
    slope_comp, intercept_comp = None, None
    slope_wall, intercept_wall = None, None
    if np.sum(mask) >= 2:
        log_N = np.log10(N[mask])
        log_comp = np.log10(np.maximum(compute[mask], 1e-10))
        slope_comp, intercept_comp = np.polyfit(log_N, log_comp, 1)
        
        log_wall = np.log10(wall[mask])
        slope_wall, intercept_wall = np.polyfit(log_N, log_wall, 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    wall_label = 'Wall time'
    if slope_wall is not None:
        wall_label += f' (O(N^{slope_wall:.2f}))'
    ax1.loglog(N, wall, 'o-', color='tab:green', linewidth=2, markersize=8, label=wall_label)
    
    comp_label = 'Compute time'
    if slope_comp is not None:
        comp_label += f' (O(N^{slope_comp:.2f}))'
    ax1.loglog(N, compute, '^-', color='tab:orange', linewidth=2, markersize=8, label=comp_label)

    ax1.loglog(N, comm, 's--', color='tab:red', linewidth=1.5, markersize=6,
               label='Comm time', alpha=0.7)
    N_ref = np.array([min(N), max(N)])
    t_ref = wall[-1] * (N_ref / N[-1]) ** 2
    ax1.loglog(N_ref, t_ref, 'k--', alpha=0.4, linewidth=1.5, label=r'$\sim N^2$ reference')
    ax1.set_xlabel('Number of Particles N')
    ax1.set_ylabel('Time [s]')
    ax1.set_title('Size Scaling (P=16)')
    ax1.legend(fontsize=10)
    ax1.grid(True, which='both')

    comm_frac = comm / wall * 100
    ax2.plot(N, comm_frac, 'o-', color='tab:red', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Particles N')
    ax2.set_ylabel('Communication Fraction [%]')
    ax2.set_title('Communication Overhead vs Problem Size')
    ax2.set_ylim(0, 100)
    ax2.grid(True)
    ax2.axhline(y=50, color='k', linestyle='--')

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/scaling_size.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/scaling_size.png")


if __name__ == "__main__":
    plot_strong_scaling()
    plot_size_scaling()
