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
from matplotlib.ticker import FuncFormatter

from plot_style import (
    INTEGRATOR_STYLE,
    apply_major_grid,
    apply_plot_style,
    disable_offset_text,
    save_figure,
)

# ── Configuration ──
INTEGRATORS = ["euler", "verlet", "rk4"]
INTEGRATOR_LABELS = {"euler": "Forward Euler", "rk4": "RK4", "verlet": "Velocity-Verlet"}
INTEGRATOR_COLORS = {k: INTEGRATOR_STYLE[k]["color"] for k in ["euler", "rk4", "verlet"]}
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

def load_manifest():
    with open("out/manifest.json", "r", encoding="utf-8") as f:
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

    fig, axes = plt.subplots(1, 3, figsize=(18, 5), constrained_layout=True)

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

        style = INTEGRATOR_STYLE[integ]
        color = style["color"]
        label = INTEGRATOR_LABELS[integ]

        axes[0].plot(
            t,
            x,
            color=color,
            linestyle=style["linestyle"],
            label=label,
            linewidth=style["linewidth"],
        )
        axes[1].plot(
            t,
            v,
            color=color,
            linestyle=style["linestyle"],
            label=label,
            linewidth=style["linewidth"],
        )
        axes[2].plot(
            x,
            v,
            color=color,
            linestyle=style["linestyle"],
            label=label,
            linewidth=style["linewidth"],
        )

    # Exact overlays
    exact_style = INTEGRATOR_STYLE["exact"]
    axes[0].plot(
        t_exact,
        x_exact,
        color=exact_style["color"],
        linestyle=exact_style["linestyle"],
        linewidth=exact_style["linewidth"],
        alpha=0.9,
        label="Exact",
    )
    axes[0].set_xlabel(r'Time $[1/\omega]$')
    axes[0].set_ylabel('Position x [arb.]')
    axes[0].set_title('Position vs Time (Reduced Units)')
    axes[0].legend(loc="upper right")
    apply_major_grid(axes[0])
    disable_offset_text(axes[0])

    axes[1].plot(
        t_exact,
        v_exact,
        color=exact_style["color"],
        linestyle=exact_style["linestyle"],
        linewidth=exact_style["linewidth"],
        alpha=0.9,
        label="Exact",
    )
    axes[1].set_xlabel(r'Time $[1/\omega]$')
    axes[1].set_ylabel('Velocity v [arb.]')
    axes[1].set_title('Velocity vs Time (Reduced Units)')
    axes[1].legend(loc="upper right")
    apply_major_grid(axes[1])
    disable_offset_text(axes[1])

    x_ep, v_ep = exact_solution(np.linspace(0, 2 * np.pi / OMEGA, 500))
    axes[2].plot(
        x_ep,
        v_ep,
        color=exact_style["color"],
        linestyle=exact_style["linestyle"],
        linewidth=exact_style["linewidth"],
        alpha=0.9,
        label="Exact",
    )
    axes[2].set_xlabel('Position x [arb.]')
    axes[2].set_ylabel('Velocity v [arb.]')
    axes[2].set_title('Phase Space (v vs x, Reduced Units)')
    axes[2].legend(loc="upper right")
    axes[2].set_aspect("equal", "box")
    apply_major_grid(axes[2])
    disable_offset_text(axes[2])

    save_figure(fig, f"{PLOT_DIR}/ho_trajectories.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_trajectories.png")


def plot_convergence():
    """Log-log convergence plot with fitted slopes."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True)

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

        style = INTEGRATOR_STYLE[integ]
        color = style["color"]
        expected = INTEGRATOR_ORDERS[integ]
        label = f"{INTEGRATOR_LABELS[integ]} (slope={slope:.2f}, expected {expected})"

        ax.loglog(
            dts,
            errors,
            marker="o",
            linestyle=style["linestyle"],
            color=color,
            label=label,
            linewidth=style["linewidth"],
        )

        # Reference slope line
        dt_ref = np.array([min(dts), max(dts)])
        err_ref = errors[0] * (dt_ref / dts[0]) ** expected
        ax.loglog(dt_ref, err_ref, "--", color=color, alpha=0.45, linewidth=1.2)

    ax.set_xlabel(r'$\Delta t\ [1/\omega]$')
    ax.set_ylabel(r'$|x_{num}(T) - x_{exact}(T)|$')
    ax.set_title('Convergence: Position Error vs Timestep (Reduced Units)')
    ax.legend(loc="best")
    apply_major_grid(ax)

    save_figure(fig, f"{PLOT_DIR}/ho_convergence.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_convergence.png")


def plot_energy_conservation():
    """Energy conservation comparison for all integrators."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)

    manifest = load_manifest()
    
    for integ in INTEGRATORS:
        dt_key = str(TRAJ_DT).replace('.', '_')
        fpath = manifest.get("ho_convergence", {}).get(f"{integ}_dt{dt_key}", "")
        if not os.path.exists(fpath):
            continue

        data = load_csv(fpath)
        t = data['time']
        E = data['E_total']

        style = INTEGRATOR_STYLE[integ]
        color = style["color"]
        label = INTEGRATOR_LABELS[integ]

        E0 = E[0]
        rel_dev = (E - E0) / abs(E0) if abs(E0) > 1e-30 else E - E0
        ax.plot(
            t,
            rel_dev,
            color=color,
            linestyle=style["linestyle"],
            label=label,
            linewidth=style["linewidth"],
        )

    ax.set_xlabel(r'Time $[1/\omega]$')
    ax.set_ylabel(r'$(E - E_0) / |E_0|$')
    ax.set_title('HO Energy Conservation (Reduced Units, dt=0.01)')
    ax.legend(loc="best")
    apply_major_grid(ax)
    disable_offset_text(ax)

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
        style = INTEGRATOR_STYLE[integ]
        axins.plot(
            t,
            rel_dev,
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=style["linewidth"],
        )
    
    axins.set_title("Zoom: VV vs RK4", fontsize=9)
    axins.tick_params(axis="both", which="major", labelsize=8)
    axins.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.1e}"))
    apply_major_grid(axins)
    disable_offset_text(axins)

    save_figure(fig, f"{PLOT_DIR}/ho_energy.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_energy.png")


if __name__ == "__main__":
    apply_plot_style()
    if "--run" in sys.argv:
        run_ho_simulations()

    plot_trajectories()
    plot_convergence()
    plot_energy_conservation()
