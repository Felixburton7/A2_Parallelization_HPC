#!/usr/bin/env python3
"""
plot_ho.py — Generate Harmonic Oscillator verification plots (Results 1).

Produces:
  1. out/plots/results1_ho_position_velocity_trajectories.png
  2. out/plots/results1_ho_phase_space_trajectories.png
  3. out/plots/results1_ho_convergence_endpoint_position_error.png
  4. out/plots/results1_ho_energy_conservation.png
  5. out/plots/results1_ho_convergence_rms_phase_space_error.png

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
    """Plot x(t), v(t) for all integrators at dt=0.01."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, axes = plt.subplots(2, 1, figsize=(9, 8), constrained_layout=True)

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
    axes[0].set_ylabel('Position x [reduced units]')
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
    axes[1].set_ylabel('Velocity v [reduced units]')
    axes[1].set_title('Velocity vs Time (Reduced Units)')
    axes[1].legend(loc="upper right")
    apply_major_grid(axes[1])
    disable_offset_text(axes[1])

    save_figure(fig, f"{PLOT_DIR}/results1_ho_position_velocity_trajectories.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/results1_ho_position_velocity_trajectories.png")


def plot_phase_space():
    """Plot phase-space trajectory in a dedicated figure."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6.5, 6.2), constrained_layout=True)
    manifest = load_manifest()

    for integ in INTEGRATORS:
        dt_key = str(TRAJ_DT).replace(".", "_")
        fpath = manifest.get("ho_convergence", {}).get(f"{integ}_dt{dt_key}", "")
        if not os.path.exists(fpath):
            continue
        data = load_csv(fpath)
        style = INTEGRATOR_STYLE[integ]
        ax.plot(
            data["x"],
            data["v"],
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=style["linewidth"],
            label=INTEGRATOR_LABELS[integ],
        )

    x_ep, v_ep = exact_solution(np.linspace(0, 2 * np.pi / OMEGA, 500))
    exact_style = INTEGRATOR_STYLE["exact"]
    ax.plot(
        x_ep,
        v_ep,
        color=exact_style["color"],
        linestyle=exact_style["linestyle"],
        linewidth=exact_style["linewidth"],
        alpha=0.9,
        label="Exact",
    )

    ax.set_xlabel("Position x [reduced units]")
    ax.set_ylabel("Velocity v [reduced units]")
    ax.set_title("Phase Space (v vs x, Reduced Units)")
    ax.set_aspect("equal", "box")
    apply_major_grid(ax)
    disable_offset_text(ax)
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), borderaxespad=0.0)

    save_figure(fig, f"{PLOT_DIR}/results1_ho_phase_space_trajectories.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/results1_ho_phase_space_trajectories.png")


def plot_convergence():
    """Log-log convergence plot with fitted slopes."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True)

    x_ex_final, _ = exact_solution(T_FINAL)

    manifest = load_manifest()

    def select_fit_points(points):
        fit_pts = [(dt, err) for dt, err in points if dt <= 0.1]
        if len(fit_pts) < 3:
            fit_pts = sorted(points)[: max(3, len(points) // 2)]
        return sorted(fit_pts)

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

            if err > 1e-14:  # skip if at/near machine epsilon
                errors.append(err)
                dts.append(dt)

        if len(dts) < 2:
            print(f"Warning: not enough data for {integ} convergence")
            continue

        dts = np.array(dts, dtype=float)
        errors = np.array(errors, dtype=float)
        raw_pts = sorted([(float(dt), float(err)) for dt, err in zip(dts, errors)])
        fit_pts = select_fit_points(raw_pts)
        if len(fit_pts) < 2:
            print(f"Warning: not enough asymptotic-fit points for {integ} convergence")
            continue

        fit_dts = np.array([p[0] for p in fit_pts], dtype=float)
        fit_errs = np.array([p[1] for p in fit_pts], dtype=float)
        log_dt = np.log10(fit_dts)
        log_err = np.log10(fit_errs)
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

    save_figure(fig, f"{PLOT_DIR}/results1_ho_convergence_endpoint_position_error.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/results1_ho_convergence_endpoint_position_error.png")


def phase_space_error_metric(data, metric):
    """Whole-trajectory phase-space error metrics against exact x(t), v(t)."""
    t = np.asarray(data["time"], dtype=float)
    x = np.asarray(data["x"], dtype=float)
    v = np.asarray(data["v"], dtype=float)
    x_exact, v_exact = exact_solution(t)
    e = np.sqrt((x - x_exact) ** 2 + (v - v_exact) ** 2)
    finite = np.isfinite(e)
    if not np.any(finite):
        return np.nan
    e = e[finite]
    if metric == "max":
        return float(np.max(e))
    if metric == "rms":
        return float(np.sqrt(np.mean(e ** 2)))
    raise ValueError(f"Unknown phase-space error metric: {metric}")


def plot_phase_error_convergence(metric, out_name, y_label, title):
    """Log-log convergence plot for a whole-trajectory phase-space error metric."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True)
    manifest = load_manifest()
    slopes = {}

    def select_fit_points(points):
        fit_pts = [(dt, err) for dt, err in points if dt <= 0.1]
        if len(fit_pts) < 3:
            fit_pts = sorted(points)[: max(3, len(points) // 2)]
        return sorted(fit_pts)

    for integ in INTEGRATORS:
        errors = []
        dts = []

        for dt in DT_VALUES:
            dt_key = str(dt).replace(".", "_")
            fpath = manifest.get("ho_convergence", {}).get(f"{integ}_dt{dt_key}", "")
            if not os.path.exists(fpath):
                continue

            data = load_csv(fpath)
            err = phase_space_error_metric(data, metric)
            if np.isfinite(err) and err > 1e-16:
                errors.append(err)
                dts.append(dt)

        if len(dts) < 2:
            print(f"Warning: not enough data for {integ} {metric} convergence")
            continue

        dts = np.array(dts, dtype=float)
        errors = np.array(errors, dtype=float)
        raw_pts = sorted([(float(dt), float(err)) for dt, err in zip(dts, errors)])
        fit_pts = select_fit_points(raw_pts)
        if len(fit_pts) < 2:
            print(f"Warning: not enough asymptotic-fit points for {integ} {metric} convergence")
            continue

        fit_dts = np.array([p[0] for p in fit_pts], dtype=float)
        fit_errs = np.array([p[1] for p in fit_pts], dtype=float)
        log_dt = np.log10(fit_dts)
        log_err = np.log10(fit_errs)
        slope, _intercept = np.polyfit(log_dt, log_err, 1)
        slopes[integ] = slope

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

        dt_ref = np.array([min(dts), max(dts)])
        err_ref = errors[0] * (dt_ref / dts[0]) ** expected
        ax.loglog(dt_ref, err_ref, "--", color=color, alpha=0.45, linewidth=1.2)

    ax.set_xlabel(r"$\Delta t\ [1/\omega]$")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend(loc="best")
    apply_major_grid(ax)

    save_figure(fig, f"{PLOT_DIR}/{out_name}")
    plt.close()
    print(f"Saved {PLOT_DIR}/{out_name}")
    if slopes:
        ordered = ", ".join(f"{k}={slopes[k]:.2f}" for k in INTEGRATORS if k in slopes)
        print(f"Fitted slopes ({metric}): {ordered}")


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
    ax.set_ylabel(r'$(E - E_0) / |E_0|$ (dimensionless; $E$ in CSV is SI J)')
    ax.set_title('HO Energy Conservation (relative drift, dt=0.01)')
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

    save_figure(fig, f"{PLOT_DIR}/results1_ho_energy_conservation.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/results1_ho_energy_conservation.png")


if __name__ == "__main__":
    apply_plot_style()
    if "--run" in sys.argv:
        run_ho_simulations()

    plot_trajectories()
    plot_phase_space()
    plot_convergence()
    plot_phase_error_convergence(
        metric="rms",
        out_name="results1_ho_convergence_rms_phase_space_error.png",
        y_label=r"$\mathrm{RMS}_t \sqrt{(x_{num}-x_{exact})^2 + (v_{num}-v_{exact})^2}$",
        title="Convergence: RMS Phase-Space Error vs Timestep (Reduced Units)",
    )
    plot_energy_conservation()
