#!/usr/bin/env python3
"""
plot_lj.py — Generate Lennard-Jones / Argon validation plots (Results 2).

Produces:
  1. Energy conservation: E_kin, E_pot, E_total vs time for Verlet and Euler
  2. Temperature vs time
  3. g(r) vs r/sigma (if extended run data available)

Usage:
  python3 scripts/plot_lj.py

Prerequisites:
  Run LJ simulations first. Output CSV files expected in out/ directory.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUT_DIR = "out"
PLOT_DIR = "out/plots"

SIGMA = 3.4e-10  # m
EPSILON_OVER_KB = 120.0  # K
KB = 1.380649e-23  # J/K
EPSILON = KB * EPSILON_OVER_KB


def load_csv(filepath):
    """Load CSV with headers."""
    return np.genfromtxt(filepath, delimiter=',', names=True)


def plot_energy_conservation():
    """Plot E_kin, E_pot, E_total vs time for Verlet and Euler."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    configs = [
        ("verlet", "Velocity-Verlet", "#2ecc71"),
        ("euler", "Euler (AMM Eqn 4.27)", "#e74c3c"),
    ]

    for idx, (integ, label, color) in enumerate(configs):
        fpath = f"{OUT_DIR}/lj_{integ}.csv"
        if not os.path.exists(fpath):
            print(f"Warning: {fpath} not found, skipping {integ}")
            continue

        data = load_csv(fpath)
        t = data['time'] * 1e12  # convert to ps
        ekin = data['E_kin'] / EPSILON  # normalise by epsilon
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

        # Energy conservation: relative deviation
        ax2 = axes[idx, 1]
        e0 = etot[0]
        if abs(e0) > 1e-30:
            rel_dev = (etot - e0) / abs(e0)
        else:
            rel_dev = etot - e0
        ax2.plot(t, rel_dev, color=color, linewidth=1.5)
        ax2.set_xlabel('Time [ps]')
        ax2.set_ylabel(r'$(E_{total} - E_0) / |E_0|$')
        ax2.set_title(f'{label}: Relative Energy Deviation')
        ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_energy.png", dpi=150)
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_energy.png")


def plot_temperature():
    """Plot temperature vs time."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    configs = [
        ("verlet", "Velocity-Verlet", "#2ecc71"),
        ("euler", "Euler (AMM Eqn 4.27)", "#e74c3c"),
    ]

    for integ, label, color in configs:
        fpath = f"{OUT_DIR}/lj_{integ}.csv"
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
    plt.savefig(f"{PLOT_DIR}/lj_temperature.png", dpi=150)
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_temperature.png")


def plot_rdf():
    """Plot g(r) if data available."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fpath = f"{OUT_DIR}/gr.csv"
    if not os.path.exists(fpath):
        print("No g(r) data found (out/gr.csv). Skipping RDF plot.")
        return

    data = np.genfromtxt(fpath, delimiter=',', names=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(data['r_sigma'], data['gr'], 'b-', linewidth=1.5)
    ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.3)
    ax.set_xlabel(r'$r / \sigma$', fontsize=14)
    ax.set_ylabel(r'$g(r)$', fontsize=14)
    ax.set_title('Radial Distribution Function (Liquid Argon)')
    ax.set_xlim(0, 5)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_rdf.png", dpi=150)
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_rdf.png")


if __name__ == "__main__":
    plot_energy_conservation()
    plot_temperature()
    plot_rdf()
