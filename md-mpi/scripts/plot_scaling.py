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

Prerequisites:
  out/scaling_strong.csv  (columns: P,N,wall_s,comm_s)
  out/scaling_size.csv    (columns: P,N,wall_s,comm_s)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

OUT_DIR = "out"
PLOT_DIR = "out/plots"


def amdahl(P, f):
    """Amdahl's Law: S(P) = 1 / (f + (1-f)/P)."""
    return 1.0 / (f + (1.0 - f) / P)


def plot_strong_scaling():
    """Plot speedup, efficiency, and compute/comm breakdown."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fpath = f"{OUT_DIR}/scaling_strong.csv"
    if not os.path.exists(fpath):
        print(f"Warning: {fpath} not found. Skipping strong scaling.")
        return

    data = np.genfromtxt(fpath, delimiter=',', names=True)
    P = data['P'].astype(int)
    wall = data['wall_s']
    comm = data['comm_s']
    compute = wall - comm

    t1 = wall[0]
    speedup = t1 / wall
    efficiency = speedup / P

    # Fit Amdahl's Law
    f_fit = None
    try:
        popt, _ = curve_fit(amdahl, P, speedup, p0=[0.01], bounds=(0, 1))
        f_fit = popt[0]
        P_fit = np.linspace(1, max(P) * 1.1, 100)
        S_fit = amdahl(P_fit, f_fit)
    except Exception as e:
        print(f"Warning: Amdahl fit failed: {e}")

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # --- Panel 1: Speedup ---
    ax1 = axes[0]
    ax1.plot(P, speedup, 'o-', color='#2ecc71', linewidth=2, markersize=8, label='Measured')
    ax1.plot(P, P.astype(float), 'k--', alpha=0.5, linewidth=1.5, label='Ideal (S=P)')
    if f_fit is not None:
        ax1.plot(P_fit, S_fit, '-', color='#e74c3c', linewidth=1.5,
                 label=f'Amdahl fit (f={f_fit:.4f})')
    ax1.set_xlabel('Number of Processes P', fontsize=12)
    ax1.set_ylabel('Speedup S(P)', fontsize=12)
    ax1.set_title('Strong Scaling: Speedup', fontsize=13)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # --- Panel 2: Efficiency ---
    ax2 = axes[1]
    ax2.plot(P, efficiency, 'o-', color='#3498db', linewidth=2, markersize=8)
    ax2.axhline(y=1.0, color='k', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Number of Processes P', fontsize=12)
    ax2.set_ylabel('Efficiency E(P) = S(P)/P', fontsize=12)
    ax2.set_title('Strong Scaling: Efficiency', fontsize=13)
    ax2.set_ylim(0, 1.15)
    ax2.grid(True, alpha=0.3)

    # --- Panel 3: Stacked bar — Compute vs Communication ---
    ax3 = axes[2]
    x_pos = np.arange(len(P))
    bar_width = 0.6

    # Clamp negative compute to zero for display
    compute_display = np.maximum(compute, 0)

    ax3.bar(x_pos, compute_display, bar_width, label='Compute', color='#2ecc71', alpha=0.8)
    ax3.bar(x_pos, comm, bar_width, bottom=compute_display, label='Communication', color='#e74c3c', alpha=0.8)

    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([str(p) for p in P])
    ax3.set_xlabel('Number of Processes P', fontsize=12)
    ax3.set_ylabel('Wall Time [s]', fontsize=12)
    ax3.set_title('Compute vs Communication Time', fontsize=13)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/scaling_strong.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/scaling_strong.png")

    if f_fit is not None:
        print(f"  Amdahl serial fraction f = {f_fit:.6f}")
        print(f"  Maximum theoretical speedup = {1.0/f_fit:.1f}x")


def plot_size_scaling():
    """Plot wall time and compute time vs N."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fpath = f"{OUT_DIR}/scaling_size.csv"
    if not os.path.exists(fpath):
        print(f"Warning: {fpath} not found. Skipping size scaling.")
        return

    data = np.genfromtxt(fpath, delimiter=',', names=True)
    N = data['N']
    wall = data['wall_s']
    comm = data['comm_s']
    compute = wall - comm

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # --- Panel 1: Wall time vs N ---
    ax1.loglog(N, wall, 'o-', color='#2ecc71', linewidth=2, markersize=8, label='Wall time')
    ax1.loglog(N, comm, 's--', color='#e74c3c', linewidth=1.5, markersize=6, label='Comm time', alpha=0.7)

    # N² reference (normalised to largest N)
    N_ref = np.array([min(N), max(N)])
    t_ref = wall[-1] * (N_ref / N[-1]) ** 2
    ax1.loglog(N_ref, t_ref, 'k--', alpha=0.4, linewidth=1.5, label=r'$\sim N^2$ reference')

    ax1.set_xlabel('Number of Particles N', fontsize=12)
    ax1.set_ylabel('Time [s]', fontsize=12)
    ax1.set_title('Size Scaling (P=16)', fontsize=13)
    ax1.legend(fontsize=10)
    ax1.grid(True, which='both', alpha=0.3)

    # --- Panel 2: Communication fraction vs N ---
    comm_frac = comm / wall * 100
    ax2.plot(N, comm_frac, 'o-', color='#e74c3c', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Particles N', fontsize=12)
    ax2.set_ylabel('Communication Fraction [%]', fontsize=12)
    ax2.set_title('Communication Overhead vs Problem Size', fontsize=13)
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=50, color='k', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/scaling_size.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/scaling_size.png")


if __name__ == "__main__":
    plot_strong_scaling()
    plot_size_scaling()
