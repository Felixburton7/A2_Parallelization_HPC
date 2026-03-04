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


import json

def load_manifest():
    with open("out/manifest.json", "r") as f:
        return json.load(f)

def load_csv(filepath):
    """Load CSV with headers, skipping comment lines."""
    def filter_comments(f):
        for line in f:
            if line.strip() and not line.startswith('#'):
                yield line
    with open(filepath, 'r') as f:
        lines = list(filter_comments(f))
    return np.genfromtxt(lines, delimiter=',', names=True)


def parse_csv_metadata(filepath):
    """Parse first metadata comment line '# key: value, ...'."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not line.startswith("#"):
                break
            s = line.lstrip("#").strip()
            parts = [p.strip() for p in s.split(",")]
            meta = {}
            for part in parts:
                if ":" not in part:
                    continue
                k, v = part.split(":", 1)
                meta[k.strip()] = v.strip()
            if meta:
                return meta
    return {}


def parse_int_meta(meta, key, default):
    if key not in meta:
        return default
    try:
        return int(float(meta[key]))
    except ValueError:
        return default


def first_prod_index(steps, production_start):
    idx = np.where(steps >= production_start)[0]
    return int(idx[0]) if idx.size > 0 else 0


def plot_energy_conservation():
    """Plot E_kin, E_pot, E_total vs time for Verlet and Euler."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    configs = [
        ("verlet_100", "Velocity-Verlet (NVE)", "#2ecc71"),
        ("euler_100", "Forward Euler", "#e74c3c"),
    ]

    manifest = load_manifest()
    
    for idx, (key, label, color) in enumerate(configs):
        fpath = manifest.get("lj_production", {}).get(key, "")
        if not os.path.exists(fpath):
            print(f"Warning: {fpath} not found, skipping")
            continue

        data = load_csv(fpath)
        meta = parse_csv_metadata(fpath)
        production_start = parse_int_meta(meta, "production_start", 0)

        t = data['time'] * 1e12  # ps
        steps = data['step'] if 'step' in data.dtype.names else np.arange(len(t))
        ekin = data['E_kin'] / EPSILON
        epot = data['E_pot'] / EPSILON
        etot = data['E_total'] / EPSILON

        ax = axes[idx, 0]
        ax.plot(t, ekin, label=r'$E_{kin}$', color='tab:red', linewidth=1.5)
        ax.plot(t, epot, label=r'$E_{pot}$', color='tab:blue', linewidth=1.5)
        ax.plot(t, etot, label=r'$E_{total}$', color='k', linewidth=2)
        ax.set_xlabel('Time [ps]')
        ax.set_ylabel(r'Energy [$\varepsilon$]')
        ax.set_title(f'{label}: Energy vs Time')
        ax.legend()
        ax.grid(True)

        # Relative deviation
        ax2 = axes[idx, 1]
        i0 = first_prod_index(steps, production_start)
        e0 = etot[i0]
        rel_dev = (etot - e0) / abs(e0) if abs(e0) > 1e-30 else etot - e0
        ax2.plot(t, rel_dev, color=color, linewidth=1.5)
        ax2.set_xlabel('Time [ps]')
        ax2.set_ylabel(r'$\Delta E / |E_{0,\mathrm{prod}}|$')
        ax2.set_title(f'{label}: Relative Energy Deviation (E0 at step {production_start})')
        ax2.grid(True)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_energy.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_energy.png")


def plot_temperature():
    """Plot temperature vs time."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    configs = [
        ("verlet_100", "Velocity-Verlet", "#2ecc71"),
        ("euler_100", "Forward Euler", "#e74c3c"),
    ]

    manifest = load_manifest()
    drew_prod_line = False

    for key, label, color in configs:
        fpath = manifest.get("lj_production", {}).get(key, "")
        if not os.path.exists(fpath):
            continue

        data = load_csv(fpath)
        meta = parse_csv_metadata(fpath)
        t = data['time'] * 1e12
        T = data['temperature']
        ax.plot(t, T, label=label, color=color, linewidth=1.5)

        rescale_step = parse_int_meta(meta, "rescale_step", -1)
        dt = float(meta.get("dt", "nan")) if meta else float("nan")
        if rescale_step >= 0 and np.isfinite(dt):
            t_prod_ps = rescale_step * dt * 1e12
            if not drew_prod_line:
                ax.axvline(
                    x=t_prod_ps,
                    color='gray',
                    linestyle=':',
                    linewidth=1.5,
                    alpha=0.8,
                    label='production start',
                )
                drew_prod_line = True

    ax.axhline(y=94.4, color='k', linestyle='--', alpha=0.5, label='T = 94.4 K')
    ax.set_xlabel('Time [ps]')
    ax.set_ylabel('Temperature [K]')
    ax.set_title('Temperature vs Time [K] (Time in ps)')
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_temperature.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_temperature.png")


def plot_equilibrated_comparison():
    """Compare raw NVE vs equilibrated NVE energy deviation."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # --- Left panel: full trajectories ---
    configs = [
        ("verlet_100", "Raw NVE (100 steps)", "#e74c3c", '-'),
        ("verlet_200_equilibrated", "Equilibrated (rescale→100, NVE→200)", "#2ecc71", '-'),
    ]

    manifest = load_manifest()

    for key, label, color, ls in configs:
        fpath = manifest.get("lj_production", {}).get(key, "")
        if not os.path.exists(fpath):
            print(f"  {fpath} not found, skipping")
            continue

        data = load_csv(fpath)
        meta = parse_csv_metadata(fpath)
        production_start = parse_int_meta(meta, "production_start", 0)
        step = data['step']
        etot = data['E_total'] / EPSILON
        i0 = first_prod_index(step, production_start)
        e0 = etot[i0]
        rel_dev = (etot - e0) / abs(e0)

        ax1.plot(step, rel_dev, color=color, label=label, linewidth=1.5, linestyle=ls)
        ax1.axvline(x=production_start, color=color, linestyle=':', linewidth=1.0, alpha=0.6)

    ax1.set_xlabel('Step')
    ax1.set_ylabel(r'$\Delta E / |E_{0,\mathrm{prod}}|$')
    ax1.set_title('Energy Deviation: Full Trajectories')
    ax1.legend(fontsize=9)
    ax1.grid(True)

    # --- Right panel: NVE-only phase comparison ---
    # Raw NVE: all 100 steps
    fpath_raw = manifest.get("lj_production", {}).get("verlet_100", "")
    fpath_eq = manifest.get("lj_production", {}).get("verlet_200_equilibrated", "")

    if os.path.exists(fpath_raw):
        data = load_csv(fpath_raw)
        meta = parse_csv_metadata(fpath_raw)
        production_start = parse_int_meta(meta, "production_start", 0)
        step = data['step']
        mask = step >= production_start
        if np.any(mask):
            etot = data['E_total'][mask] / EPSILON
            e0 = etot[0]
            nve_steps = np.arange(len(etot))
            drift = abs(etot[-1] - e0) / abs(e0) * 100.0
            ax2.plot(
                nve_steps,
                (etot - e0) / abs(e0),
                color='tab:red',
                linewidth=1.5,
                label=f'Raw NVE (from step {production_start}, drift={drift:.2f}%)',
            )

    if os.path.exists(fpath_eq):
        data = load_csv(fpath_eq)
        meta = parse_csv_metadata(fpath_eq)
        production_start = parse_int_meta(meta, "production_start", 0)
        nve_mask = data['step'] >= production_start
        if np.any(nve_mask):
            etot_nve = data['E_total'][nve_mask] / EPSILON
            e0_nve = etot_nve[0]
            nve_steps = np.arange(len(etot_nve))
            drift = abs(etot_nve[-1] - e0_nve) / abs(e0_nve) * 100.0
            ax2.plot(
                nve_steps,
                (etot_nve - e0_nve) / abs(e0_nve),
                color='tab:green',
                linewidth=1.5,
                label=f'Post-equilibration NVE (from step {production_start}, drift={drift:.2f}%)',
            )

    ax2.set_xlabel('Production Step Index')
    ax2.set_ylabel(r'$\Delta E / |E_{0,\mathrm{prod}}|$')
    ax2.set_title('Production-Window Energy Conservation Comparison')
    ax2.legend(fontsize=9)
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_equilibrated_comparison.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_equilibrated_comparison.png")


def plot_rdf():
    """Plot g(r) radial distribution function."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    manifest = load_manifest()
    fpath = manifest.get("lj_gr", "")
    if not os.path.exists(fpath):
        print("No g(r) data found. Skipping RDF plot.")
        return

    data = load_csv(fpath)
    meta_gr = parse_csv_metadata(fpath)
    gr_start = parse_int_meta(
        meta_gr,
        "gr_start",
        parse_int_meta(meta_gr, "production_start", 0) + parse_int_meta(meta_gr, "gr_discard", 0),
    )
    gr_interval = parse_int_meta(meta_gr, "gr_interval", 1)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(data['r_sigma'], data['gr'], '-', color='k', linewidth=1.5)
    ax.axhline(y=1.0, color='k', linestyle='--', label='g(r) = 1')
    ax.set_xlabel(r'$r / \sigma$')
    ax.set_ylabel(r'$g(r)$')

    try:
        fpath_energy = manifest.get("lj_gr_energy", "")
        if os.path.exists(fpath_energy):
            energy_data = load_csv(fpath_energy)
            gr_mask = energy_data['step'] >= gr_start
            if np.any(gr_mask):
                T_mean = np.mean(energy_data['temperature'][gr_mask])
                ax.set_title(
                    rf'Radial Distribution Function (Liquid Argon, '
                    rf'$\langle T \rangle$ = {T_mean:.0f} K, start={gr_start}, every {gr_interval})'
                )
            else:
                ax.set_title(r'Radial Distribution Function (Liquid Argon)')
        else:
            ax.set_title(r'Radial Distribution Function (Liquid Argon)')
    except Exception as e:
        print(f"Warning: could not compute T_mean for title: {e}")
        ax.set_title(r'Radial Distribution Function (Liquid Argon)')

    ax.set_xlim(0, 5)
    ax.legend()
    ax.grid(True)

    # Annotate first peak
    peak_idx = np.argmax(data['gr'])
    ax.annotate(f"Peak: g({data['r_sigma'][peak_idx]:.2f}σ) = {data['gr'][peak_idx]:.2f}",
                xy=(data['r_sigma'][peak_idx], data['gr'][peak_idx]),
                xytext=(2.5, 2.5),
                arrowprops=dict(arrowstyle='->', color='gray'))

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_rdf.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_rdf.png")


if __name__ == "__main__":
    plot_energy_conservation()
    plot_temperature()
    plot_equilibrated_comparison()
    plot_rdf()
