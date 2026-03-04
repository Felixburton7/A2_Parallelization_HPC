#!/usr/bin/env python3
"""
plot_ho.py — Generate Harmonic Oscillator verification plots (Results 1).

Produces:
  1. Position & velocity vs time for all three integrators (with exact overlay)
  2. Phase-space (v vs x) diagrams
  3. Log-log convergence: |x_num(T) - x_exact(T)| vs dt with fitted slopes
  4. Energy conservation comparison

Usage:
  python3 scripts/plot_ho.py           # plot from existing data in out/ho/
  python3 scripts/plot_ho.py --run     # run simulations first, then plot
"""

import os
import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt

# ── Configuration ──
INTEGRATORS = ["euler", "verlet", "rk4"]
INTEGRATOR_LABELS = {"euler": "Forward Euler", "rk4": "RK4", "verlet": "Velocity-Verlet"}
INTEGRATOR_COLORS = {"euler": "#e74c3c", "rk4": "#3498db", "verlet": "#2ecc71"}
INTEGRATOR_ORDERS = {"euler": 1, "rk4": 4, "verlet": 2}

DT_VALUES = [1.0, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005]
DT_STEPS = {1.0: 10, 0.5: 20, 0.1: 100, 0.05: 200, 0.01: 1000,
            0.005: 2000, 0.001: 10000, 0.0005: 20000}
OMEGA = 1.0
T_FINAL = 10.0
TRAJ_DT = 0.01  # dt used for trajectory/phase-space plots

OUT_DIR = "out"
HO_DIR = "out/ho"
PLOT_DIR = "out/plots"


def exact_solution(t, omega=OMEGA):
    """Exact HO solution: x(t) = cos(wt), v(t) = -w*sin(wt)."""
    x = np.cos(omega * t)
    v = -omega * np.sin(omega * t)
    return x, v


def run_ho_simulations():
    """Run HO simulations for all integrators and dt values."""
    os.makedirs(HO_DIR, exist_ok=True)
    for integ in INTEGRATORS:
        for dt in DT_VALUES:
            steps = DT_STEPS[dt]
            cmd = [
                "mpirun", "-np", "1", "./md_solver",
                "--mode", "ho", "--integrator", integ,
                "--dt", str(dt), "--steps", str(steps), "--N", "1"
            ]
            print(f"Running: {integ} dt={dt} steps={steps}")
            subprocess.run(cmd, check=True, capture_output=True)
            src = f"{OUT_DIR}/ho_{integ}.csv"
            dst = f"{HO_DIR}/{integ}_dt{dt}.csv"
            if os.path.exists(src):
                os.rename(src, dst)
    print("All HO simulations complete.")


import json
import csv

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
        # np.genfromtxt has trouble with Python generators, so read to list
        lines = list(filter_comments(f))
    return np.genfromtxt(lines, delimiter=',', names=True)


def plot_trajectories():
    """Plot x(t), v(t), phase space for all integrators at dt=0.01."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    t_exact = np.linspace(0, T_FINAL, 1000)
    x_exact, v_exact = exact_solution(t_exact)

    manifest = load_manifest()
    
    for integ in INTEGRATORS:
        dt_key = str(TRAJ_DT).replace('.', '_')
        fpath = manifest.get("ho_convergence", {}).get(f"{integ}_dt{dt_key}", "")
        if not os.path.exists(fpath):
            print(f"Warning: {fpath} not found, skipping {integ}")
            continue

        data = load_csv(fpath)
        t = data['time']
        x = data['x']
        v = data['v']

        color = INTEGRATOR_COLORS[integ]
        label = INTEGRATOR_LABELS[integ]

        axes[0].plot(t, x, color=color, label=label, linewidth=1.5, alpha=0.8)
        axes[1].plot(t, v, color=color, label=label, linewidth=1.5, alpha=0.8)
        axes[2].plot(x, v, color=color, label=label, linewidth=1.2, alpha=0.8)

    # Exact overlays
    axes[0].plot(t_exact, x_exact, 'k--', linewidth=1, alpha=0.5, label='Exact')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Position x')
    axes[0].set_title('Position vs Time')
    axes[0].legend(fontsize=9)
    axes[0].grid(True)

    axes[1].plot(t_exact, v_exact, 'k--', linewidth=1, alpha=0.5, label='Exact')
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Velocity v')
    axes[1].set_title('Velocity vs Time')
    axes[1].legend(fontsize=9)
    axes[1].grid(True)

    x_ep, v_ep = exact_solution(np.linspace(0, 2 * np.pi / OMEGA, 500))
    axes[2].plot(x_ep, v_ep, 'k--', linewidth=1, alpha=0.5, label='Exact')
    axes[2].set_xlabel('Position x')
    axes[2].set_ylabel('Velocity v')
    axes[2].set_title('Phase Space (v vs x)')
    axes[2].legend(fontsize=9)
    axes[2].set_aspect('equal')
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/ho_trajectories.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_trajectories.png")


def plot_convergence():
    """Log-log convergence plot with fitted slopes."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))

    x_ex_final, _ = exact_solution(T_FINAL)

    manifest = load_manifest()

    for integ in INTEGRATORS:
        errors = []
        dts = []

        for dt in DT_VALUES:
            dt_key = str(dt).replace('.', '_')
            try:
                fpath = manifest.get("ho_convergence", {}).get(f"{integ}_dt{dt_key}", "")
            except Exception:
                fpath = ""
            if not os.path.exists(fpath):
                continue

            data = load_csv(fpath)
            x_num_final = data['x'][-1]
            err = abs(x_num_final - x_ex_final)

            if err > 1e-16:  # skip if at machine epsilon
                errors.append(err)
                dts.append(dt)

        if len(dts) < 2:
            print(f"Warning: not enough data for {integ} convergence")
            continue

        dts = np.array(dts)
        errors = np.array(errors)

        log_dt = np.log10(dts)
        log_err = np.log10(errors)
        slope, intercept = np.polyfit(log_dt, log_err, 1)

        color = INTEGRATOR_COLORS[integ]
        expected = INTEGRATOR_ORDERS[integ]
        label = f"{INTEGRATOR_LABELS[integ]} (slope={slope:.2f}, expected {expected})"

        ax.loglog(dts, errors, 'o-', color=color, label=label,
                  linewidth=2, markersize=6)

        # Reference slope line
        dt_ref = np.array([min(dts), max(dts)])
        err_ref = errors[0] * (dt_ref / dts[0]) ** expected
        ax.loglog(dt_ref, err_ref, '--', color=color, alpha=0.4, linewidth=1)

    ax.set_xlabel(r'$\Delta t$')
    ax.set_ylabel(r'$|x_{num}(T) - x_{exact}(T)|$')
    ax.set_title('Convergence: Position Error vs Timestep')
    ax.legend(fontsize=10)
    ax.grid(True, which='both')

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/ho_convergence.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_convergence.png")


def plot_energy_conservation():
    """Energy conservation comparison for all integrators."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    manifest = load_manifest()
    
    for integ in INTEGRATORS:
        dt_key = str(TRAJ_DT).replace('.', '_')
        fpath = manifest.get("ho_convergence", {}).get(f"{integ}_dt{dt_key}", "")
        if not os.path.exists(fpath):
            continue

        data = load_csv(fpath)
        t = data['time']
        E = data['E_total']

        color = INTEGRATOR_COLORS[integ]
        label = INTEGRATOR_LABELS[integ]

        E0 = E[0]
        rel_dev = (E - E0) / abs(E0) if abs(E0) > 1e-30 else E - E0
        ax.plot(t, rel_dev, color=color, label=label, linewidth=1.5)

    ax.set_xlabel('Time')
    ax.set_ylabel(r'$(E - E_0) / |E_0|$')
    ax.set_title('HO Energy Conservation (dt=0.01)')
    ax.legend(fontsize=10)
    ax.grid(True)

    # Add zoomed inset to show VV vs RK4 near zero
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    axins = inset_axes(ax, width="40%", height="30%", loc="lower right", borderpad=2)
    
    for integ in INTEGRATORS:
        if integ == "euler": continue # Skip Euler for inset
        dt_key = str(TRAJ_DT).replace('.', '_')
        fpath = manifest.get("ho_convergence", {}).get(f"{integ}_dt{dt_key}", "")
        if not os.path.exists(fpath): continue
        data = load_csv(fpath)
        t = data['time']
        E = data['E_total']
        E0 = E[0]
        rel_dev = (E - E0) / abs(E0) if abs(E0) > 1e-30 else E - E0
        axins.plot(t, rel_dev, color=INTEGRATOR_COLORS[integ], linewidth=1.5)
    
    axins.set_title('Zoom: VV vs RK4')
    axins.grid(True)
    axins.tick_params(axis='both', which='major', labelsize=8)
    
    # Optional: adjust y-limits of inset manually if needed
    # (Leaving it auto-scaled, which usually captures the O(1e-4) VV vs O(1e-15) RK4 nicely.)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/ho_energy.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_energy.png")


if __name__ == "__main__":
    if "--run" in sys.argv:
        run_ho_simulations()

    plot_trajectories()
    plot_convergence()
    plot_energy_conservation()
