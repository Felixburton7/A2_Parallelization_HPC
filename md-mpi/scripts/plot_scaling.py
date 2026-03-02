#!/usr/bin/env python3
"""
plot_scaling.py — Generate scaling analysis plots (Results 3).

Produces:
  1. Strong scaling: Speedup S(P) with Amdahl's Law fit
  2. Efficiency E(P) = S(P)/P
  3. Size scaling: Compute time vs N (expect ~N^2 behaviour)

Usage:
  python3 scripts/plot_scaling.py

Prerequisites:
  Scaling data in out/scaling_strong.csv and out/scaling_size.csv
  Format: P,time or N,time (one header row)
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
    """Plot speedup and efficiency vs number of processes."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fpath = f"{OUT_DIR}/scaling_strong.csv"
    if not os.path.exists(fpath):
        print(f"Warning: {fpath} not found. Skipping strong scaling plot.")
        return

    data = np.genfromtxt(fpath, delimiter=',', names=True)
    P = data['P'].astype(int)
    times = data['time']

    # Compute speedup and efficiency
    t1 = times[0]  # serial time (P=1)
    speedup = t1 / times
    efficiency = speedup / P

    # Fit Amdahl's Law
    try:
        popt, pcov = curve_fit(amdahl, P, speedup, p0=[0.01], bounds=(0, 1))
        f_fit = popt[0]
        P_fit = np.linspace(1, max(P) * 1.1, 100)
        S_fit = amdahl(P_fit, f_fit)
    except Exception as e:
        print(f"Warning: Amdahl fit failed: {e}")
        f_fit = None

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Speedup plot
    ax1.plot(P, speedup, 'o-', color='#2ecc71', linewidth=2, markersize=8, label='Measured')
    ax1.plot(P, P.astype(float), 'k--', alpha=0.5, linewidth=1.5, label='Ideal (S=P)')
    if f_fit is not None:
        ax1.plot(P_fit, S_fit, '-', color='#e74c3c', linewidth=1.5,
                 label=f'Amdahl fit (f={f_fit:.4f})')
    ax1.set_xlabel('Number of Processes P', fontsize=12)
    ax1.set_ylabel('Speedup S(P)', fontsize=12)
    ax1.set_title('Strong Scaling: Speedup', fontsize=14)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)

    # Efficiency plot
    ax2.plot(P, efficiency, 'o-', color='#3498db', linewidth=2, markersize=8)
    ax2.axhline(y=1.0, color='k', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Number of Processes P', fontsize=12)
    ax2.set_ylabel('Efficiency E(P) = S(P)/P', fontsize=12)
    ax2.set_title('Strong Scaling: Efficiency', fontsize=14)
    ax2.set_ylim(0, 1.1)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/scaling_strong.png", dpi=150)
    plt.close()
    print(f"Saved {PLOT_DIR}/scaling_strong.png")

    if f_fit is not None:
        print(f"Amdahl serial fraction f = {f_fit:.6f}")
        print(f"Maximum theoretical speedup = {1.0/f_fit:.2f}")


def plot_size_scaling():
    """Plot compute time vs N (expect ~N^2)."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fpath = f"{OUT_DIR}/scaling_size.csv"
    if not os.path.exists(fpath):
        print(f"Warning: {fpath} not found. Skipping size scaling plot.")
        return

    data = np.genfromtxt(fpath, delimiter=',', names=True)
    N = data['N']
    times = data['time']

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.loglog(N, times, 'o-', color='#2ecc71', linewidth=2, markersize=8, label='Measured')

    # Reference N^2 line
    N_ref = np.array([min(N), max(N)])
    t_ref = times[0] * (N_ref / N[0])**2
    ax.loglog(N_ref, t_ref, 'k--', alpha=0.5, linewidth=1.5, label=r'$\sim N^2$ reference')

    ax.set_xlabel('Number of Particles N', fontsize=12)
    ax.set_ylabel('Wall Time [s]', fontsize=12)
    ax.set_title('Size Scaling: Compute Time vs N', fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, which='both', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/scaling_size.png", dpi=150)
    plt.close()
    print(f"Saved {PLOT_DIR}/scaling_size.png")


if __name__ == "__main__":
    plot_strong_scaling()
    plot_size_scaling()
