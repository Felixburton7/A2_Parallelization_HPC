#!/usr/bin/env python3
"""
plot_ho.py — Generate Harmonic Oscillator verification plots (Results 1).

Produces:
  1. Position vs time for all three integrators (with exact solution overlay)
  2. Velocity vs time
  3. Phase-space (v vs x) diagrams
  4. Log-log convergence: |x_num(T) - x_exact(T)| vs dt with fitted slopes

Usage:
  python3 scripts/plot_ho.py           # just plot from existing data
  python3 scripts/plot_ho.py --run     # run simulations first, then plot

Prerequisites:
  HO CSV files in out/ directory with columns: step,time,x,v,E_kin,E_pot,E_total
"""

import os
import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# ── Configuration ──
INTEGRATORS = ["euler", "rk4", "verlet"]
INTEGRATOR_LABELS = {"euler": "Euler (AMM Eqn 4.27)", "rk4": "RK4", "verlet": "Velocity-Verlet"}
INTEGRATOR_COLORS = {"euler": "#e74c3c", "rk4": "#3498db", "verlet": "#2ecc71"}
INTEGRATOR_ORDERS = {"euler": 1, "rk4": 4, "verlet": 2}

DT_VALUES = [0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]
OMEGA = 1.0
T_FINAL = 10.0  # final time for convergence test
N_PARTICLES = 1

# Initial conditions: x(0) = 1.0, v(0) = 0.0
X0 = 1.0
V0 = 0.0

OUT_DIR = "out"
PLOT_DIR = "out/plots"


def exact_solution(t, omega=OMEGA, x0=X0, v0=V0):
    """Exact HO solution: x(t) = x0*cos(wt) + (v0/w)*sin(wt)."""
    x = x0 * np.cos(omega * t) + (v0 / omega) * np.sin(omega * t)
    v = -x0 * omega * np.sin(omega * t) + v0 * np.cos(omega * t)
    return x, v


def run_ho_simulations():
    """Run HO simulations for all integrators and dt values."""
    os.makedirs(OUT_DIR, exist_ok=True)

    for integ in INTEGRATORS:
        # Single run with moderate dt for trajectory plots
        dt_traj = 0.01
        steps_traj = int(T_FINAL / dt_traj)
        cmd = [
            "mpirun", "-np", "1", "./md_solver",
            "--mode", "ho", "--integrator", integ,
            "--dt", str(dt_traj), "--steps", str(steps_traj),
            "--N", str(N_PARTICLES), "--omega", str(OMEGA)
        ]
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

        # Rename output for trajectory
        src = f"{OUT_DIR}/ho_{integ}.csv"
        dst = f"{OUT_DIR}/ho_{integ}_traj.csv"
        if os.path.exists(src):
            os.rename(src, dst)

        # Convergence sweep
        for dt in DT_VALUES:
            steps = int(T_FINAL / dt)
            cmd = [
                "mpirun", "-np", "1", "./md_solver",
                "--mode", "ho", "--integrator", integ,
                "--dt", str(dt), "--steps", str(steps),
                "--N", str(N_PARTICLES), "--omega", str(OMEGA)
            ]
            print(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)

            # Rename with dt label
            src = f"{OUT_DIR}/ho_{integ}.csv"
            dst = f"{OUT_DIR}/ho_{integ}_dt{dt}.csv"
            if os.path.exists(src):
                os.rename(src, dst)


def load_csv(filepath):
    """Load CSV file with headers."""
    return np.genfromtxt(filepath, delimiter=',', names=True)


def plot_trajectories():
    """Plot x(t), v(t), phase space for all integrators."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Exact solution
    t_exact = np.linspace(0, T_FINAL, 1000)
    x_exact, v_exact = exact_solution(t_exact)

    for integ in INTEGRATORS:
        fpath = f"{OUT_DIR}/ho_{integ}_traj.csv"
        if not os.path.exists(fpath):
            print(f"Warning: {fpath} not found, skipping {integ}")
            continue

        data = load_csv(fpath)
        t = data['time']
        x = data['x']
        v = data['v']

        color = INTEGRATOR_COLORS[integ]
        label = INTEGRATOR_LABELS[integ]

        # Position vs time
        axes[0].plot(t, x, color=color, label=label, linewidth=1.5, alpha=0.8)

        # Velocity vs time
        axes[1].plot(t, v, color=color, label=label, linewidth=1.5, alpha=0.8)

        # Phase space: v vs x
        axes[2].plot(x, v, color=color, label=label, linewidth=1.2, alpha=0.8)

    # Exact overlays
    axes[0].plot(t_exact, x_exact, 'k--', linewidth=1, alpha=0.5, label='Exact')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Position x')
    axes[0].set_title('Position vs Time')
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(t_exact, v_exact, 'k--', linewidth=1, alpha=0.5, label='Exact')
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Velocity v')
    axes[1].set_title('Velocity vs Time')
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)

    x_ex_phase, v_ex_phase = exact_solution(np.linspace(0, 2*np.pi/OMEGA, 500))
    axes[2].plot(x_ex_phase, v_ex_phase, 'k--', linewidth=1, alpha=0.5, label='Exact')
    axes[2].set_xlabel('Position x')
    axes[2].set_ylabel('Velocity v')
    axes[2].set_title('Phase Space (v vs x)')
    axes[2].legend(fontsize=9)
    axes[2].set_aspect('equal')
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/ho_trajectories.png", dpi=150)
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_trajectories.png")


def plot_convergence():
    """Plot log-log convergence: |x_num(T) - x_exact(T)| vs dt with fitted slopes."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Exact position at T_FINAL
    x_ex_final, _ = exact_solution(T_FINAL)

    for integ in INTEGRATORS:
        errors = []
        dts = []

        for dt in DT_VALUES:
            fpath = f"{OUT_DIR}/ho_{integ}_dt{dt}.csv"
            if not os.path.exists(fpath):
                continue

            data = load_csv(fpath)

            # Position error: |x_num(T) - x_exact(T)| (charter §A3)
            x_num_final = data['x'][-1]
            err = abs(x_num_final - x_ex_final)

            if err > 0:
                errors.append(err)
                dts.append(dt)

        if len(dts) < 2:
            print(f"Warning: not enough data for {integ} convergence")
            continue

        dts = np.array(dts)
        errors = np.array(errors)

        # Linear regression on log-log data
        log_dt = np.log10(dts)
        log_err = np.log10(errors)
        slope, intercept, r_value, _, _ = linregress(log_dt, log_err)

        color = INTEGRATOR_COLORS[integ]
        expected = INTEGRATOR_ORDERS[integ]
        label = f"{INTEGRATOR_LABELS[integ]} (fitted p={slope:.2f}, expected {expected})"

        ax.loglog(dts, errors, 'o-', color=color, label=label,
                  linewidth=2, markersize=6)

        # Reference slope line
        dt_ref = np.array([min(dts), max(dts)])
        err_ref = errors[0] * (dt_ref / dts[0])**expected
        ax.loglog(dt_ref, err_ref, '--', color=color, alpha=0.4, linewidth=1)

    ax.set_xlabel(r'$\Delta t$', fontsize=14)
    ax.set_ylabel(r'$|x_{num}(T) - x_{exact}(T)|$', fontsize=14)
    ax.set_title('Convergence: Position Error vs Timestep', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, which='both', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/ho_convergence.png", dpi=150)
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_convergence.png")


def plot_energy_conservation():
    """Plot energy conservation comparison for all integrators."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    for integ in INTEGRATORS:
        fpath = f"{OUT_DIR}/ho_{integ}_traj.csv"
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
    ax.set_title('HO Energy Conservation')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/ho_energy.png", dpi=150)
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_energy.png")


if __name__ == "__main__":
    if "--run" in sys.argv:
        run_ho_simulations()

    plot_trajectories()
    plot_convergence()
    plot_energy_conservation()
