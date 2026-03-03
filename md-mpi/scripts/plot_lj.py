#!/usr/bin/env python3
"""
plot_lj.py — Generate Lennard-Jones / Argon validation plots (Results 2).

Produces:
  1. Energy conservation: E_kin, E_pot, E_total vs time for Verlet and Euler
  2. Temperature vs time
  3. Raw NVE vs equilibrated NVE energy comparison
  4. g(r) vs r/sigma

Usage:
  python3 scripts/plot_lj.py
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUT_DIR = "out"
LJ_DIR = "out/lj"
PLOT_DIR = "out/plots"

SIGMA = 3.4e-10
EPSILON_OVER_KB = 120.0
KB = 1.380649e-23
EPSILON = KB * EPSILON_OVER_KB


def load_csv(filepath):
    """Load CSV with headers."""
    return np.genfromtxt(filepath, delimiter=',', names=True)


def plot_energy_conservation():
    """Plot E_kin, E_pot, E_total vs time for Verlet and Euler."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    configs = [
        ("verlet_864_100", "Velocity-Verlet (NVE)", "#2ecc71"),
        ("euler_864_100", "Euler (AMM Eqn 4.27)", "#e74c3c"),
    ]

    for idx, (fname, label, color) in enumerate(configs):
        fpath = f"{LJ_DIR}/{fname}.csv"
        if not os.path.exists(fpath):
            print(f"Warning: {fpath} not found, skipping")
            continue

        data = load_csv(fpath)
        t = data['time'] * 1e12  # ps
        ekin = data['E_kin'] / EPSILON
        epot = data['E_pot'] / EPSILON
        etot = data['E_total'] / EPSILON

        ax = axes[idx, 0]
        ax.plot(t, ekin, label=r'$E_{kin}$', color='#e74c3c', linewidth=1.5)
        ax.plot(t, epot, label=r'$E_{pot}$', color='#3498db', linewidth=1.5)
        ax.plot(t, etot, label=r'$E_{total}$', color='#2c3e50', linewidth=2)
        ax.set_xlabel('Time [ps]')
        ax.set_ylabel(r'Energy [$\varepsilon$]')
        ax.set_title(f'{label}: Energy vs Time')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Relative deviation
        ax2 = axes[idx, 1]
        e0 = etot[0]
        rel_dev = (etot - e0) / abs(e0) if abs(e0) > 1e-30 else etot - e0
        ax2.plot(t, rel_dev, color=color, linewidth=1.5)
        ax2.set_xlabel('Time [ps]')
        ax2.set_ylabel(r'$(E_{total} - E_0) / |E_0|$')
        ax2.set_title(f'{label}: Relative Energy Deviation')
        ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_energy.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_energy.png")


def plot_temperature():
    """Plot temperature vs time."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    configs = [
        ("verlet_864_100", "Velocity-Verlet", "#2ecc71"),
        ("euler_864_100", "Euler (AMM 4.27)", "#e74c3c"),
    ]

    for fname, label, color in configs:
        fpath = f"{LJ_DIR}/{fname}.csv"
        if not os.path.exists(fpath):
            continue

        data = load_csv(fpath)
        t = data['time'] * 1e12
        T = data['temperature']
        ax.plot(t, T, label=label, color=color, linewidth=1.5)

    ax.axhline(y=94.4, color='k', linestyle='--', alpha=0.5, label='T = 94.4 K')
    ax.set_xlabel('Time [ps]')
    ax.set_ylabel('Temperature [K]')
    ax.set_title('Temperature vs Time (N=864, NVE)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_temperature.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_temperature.png")


def plot_equilibrated_comparison():
    """Compare raw NVE vs equilibrated NVE energy deviation."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # --- Left panel: full trajectories ---
    configs = [
        ("verlet_864_100", "Raw NVE (100 steps)", "#e74c3c", '-'),
        ("verlet_864_200_equilibrated", "Equilibrated (rescale→100, NVE→200)", "#2ecc71", '-'),
    ]

    for fname, label, color, ls in configs:
        fpath = f"{LJ_DIR}/{fname}.csv"
        if not os.path.exists(fpath):
            print(f"  {fpath} not found, skipping")
            continue

        data = load_csv(fpath)
        step = data['step']
        etot = data['E_total'] / EPSILON
        e0 = etot[0]
        rel_dev = (etot - e0) / abs(e0)

        ax1.plot(step, rel_dev, color=color, label=label, linewidth=1.5, linestyle=ls)

    ax1.set_xlabel('Step')
    ax1.set_ylabel(r'$(E_{total} - E_0) / |E_0|$')
    ax1.set_title('Energy Deviation: Full Trajectories')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # --- Right panel: NVE-only phase comparison ---
    # Raw NVE: all 100 steps
    fpath_raw = f"{LJ_DIR}/verlet_864_100.csv"
    fpath_eq = f"{LJ_DIR}/verlet_864_200_equilibrated.csv"

    if os.path.exists(fpath_raw):
        data = load_csv(fpath_raw)
        etot = data['E_total'] / EPSILON
        e0 = etot[0]
        nve_steps = np.arange(len(etot))
        ax2.plot(nve_steps, (etot - e0) / abs(e0), color='#e74c3c', linewidth=1.5,
                 label=f'Raw NVE (drift={abs(etot[-1]-e0)/abs(e0)*100:.2f}%)')

    if os.path.exists(fpath_eq):
        data = load_csv(fpath_eq)
        # NVE phase starts after step 100
        nve_mask = data['step'] > 100
        if np.any(nve_mask):
            etot_nve = data['E_total'][nve_mask] / EPSILON
            e0_nve = etot_nve[0]
            nve_steps = np.arange(len(etot_nve))
            ax2.plot(nve_steps, (etot_nve - e0_nve) / abs(e0_nve), color='#2ecc71', linewidth=1.5,
                     label=f'Post-equilibration NVE (drift={abs(etot_nve[-1]-e0_nve)/abs(e0_nve)*100:.2f}%)')

    ax2.set_xlabel('NVE Step')
    ax2.set_ylabel(r'$(E_{total} - E_0) / |E_0|$')
    ax2.set_title('NVE Energy Conservation Comparison')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_equilibrated_comparison.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_equilibrated_comparison.png")


def plot_rdf():
    """Plot g(r) radial distribution function."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fpath = f"{OUT_DIR}/gr.csv"
    if not os.path.exists(fpath):
        print("No g(r) data found. Skipping RDF plot.")
        return

    data = np.genfromtxt(fpath, delimiter=',', names=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(data['r_sigma'], data['gr'], '-', color='#2c3e50', linewidth=1.5)
    ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.3, label='g(r) = 1')
    ax.set_xlabel(r'$r / \sigma$', fontsize=14)
    ax.set_ylabel(r'$g(r)$', fontsize=14)
    ax.set_title('Radial Distribution Function (Liquid Argon, T=94.4 K)')
    ax.set_xlim(0, 5)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Annotate first peak
    peak_idx = np.argmax(data['gr'])
    ax.annotate(f"Peak: g({data['r_sigma'][peak_idx]:.2f}σ) = {data['gr'][peak_idx]:.2f}",
                xy=(data['r_sigma'][peak_idx], data['gr'][peak_idx]),
                xytext=(2.5, 2.5), fontsize=10,
                arrowprops=dict(arrowstyle='->', color='gray'))

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_rdf.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_rdf.png")


if __name__ == "__main__":
    plot_energy_conservation()
    plot_temperature()
    plot_equilibrated_comparison()
    plot_rdf()
