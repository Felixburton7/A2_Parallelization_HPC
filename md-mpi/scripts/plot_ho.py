#!/usr/bin/env python3
"""
plot_ho.py — Results 1 harmonic oscillator plotting package.

Main figures (brief-facing):
  1) out/plots/results1_ho_figure1_trajectories_dt0p01.png
  2) out/plots/results1_ho_figure2_phase_space_dt0p01.png
  3) out/plots/results1_ho_figure3_small_vs_large_dt.png
  4) out/plots/results1_ho_figure4_convergence_combined.png

Optional supporting figure:
  5) out/plots/results1_ho_figure5_energy_diagnostic.png

Generated artifacts:
  - out/summary/results1/results1_ho_small_large_summary.(csv|md)
  - out/summary/results1/results1_ho_convergence_summary.(csv|md)
  - out/summary/results1/results1_ho_endpoint_values.(csv|md)
  - out/summary/results1/results1_ho_caption_notes.md

Each figure gets a JSON metadata sidecar in:
  out/plots/metadata/<figure_name>.json
"""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from plot_style import (
    INTEGRATOR_STYLE,
    apply_major_grid,
    apply_plot_style,
    disable_offset_text,
    save_figure,
)

# Configuration
INTEGRATORS = ["euler", "verlet", "rk4"]
INTEGRATOR_LABELS = {"euler": "Forward Euler", "verlet": "Velocity-Verlet", "rk4": "RK4"}
INTEGRATOR_ORDERS = {"euler": 1, "verlet": 2, "rk4": 4}

DT_VALUES = [1.0, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005]
DT_STEPS = {
    1.0: 10,
    0.5: 20,
    0.1: 100,
    0.05: 200,
    0.01: 1000,
    0.005: 2000,
    0.001: 10000,
    0.0005: 20000,
}
DT_SMALL = 0.01
DT_LARGE = 0.5
TRAJ_DT = DT_SMALL

OMEGA = 1.0
X0 = 1.0
V0 = 0.0
T_FINAL = 10.0

OUT_DIR = "out"
PLOT_DIR = "out/plots"
PLOT_META_DIR = "out/plots/metadata"
SUMMARY_DIR = "out/summary"
SUMMARY_RESULTS1_DIR = "out/summary/results1"

FIG1_PNG = "results1_ho_figure1_trajectories_dt0p01.png"
FIG2_PNG = "results1_ho_figure2_phase_space_dt0p01.png"
FIG3_PNG = "results1_ho_figure3_small_vs_large_dt.png"
FIG4_PNG = "results1_ho_figure4_convergence_combined.png"
FIG5_PNG = "results1_ho_figure5_energy_diagnostic.png"

R1_SMALL_LARGE_CSV = f"{SUMMARY_RESULTS1_DIR}/results1_ho_small_large_summary.csv"
R1_SMALL_LARGE_MD = f"{SUMMARY_RESULTS1_DIR}/results1_ho_small_large_summary.md"
R1_CONVERGENCE_CSV = f"{SUMMARY_RESULTS1_DIR}/results1_ho_convergence_summary.csv"
R1_CONVERGENCE_MD = f"{SUMMARY_RESULTS1_DIR}/results1_ho_convergence_summary.md"
R1_ENDPOINT_VALUES_CSV = f"{SUMMARY_RESULTS1_DIR}/results1_ho_endpoint_values.csv"
R1_ENDPOINT_VALUES_MD = f"{SUMMARY_RESULTS1_DIR}/results1_ho_endpoint_values.md"
R1_CAPTION_NOTES_MD = f"{SUMMARY_RESULTS1_DIR}/results1_ho_caption_notes.md"
R1_SECTION_NOTES_MD = f"{SUMMARY_RESULTS1_DIR}/results1_results_section_notes.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def dt_key(dt: float) -> str:
    return str(dt).replace(".", "_")


def format_dt(dt: float) -> str:
    return f"{dt:g}"


def exact_solution(t: np.ndarray | float, omega: float = OMEGA, x0: float = X0, v0: float = V0):
    """
    Authoritative exact HO solution used throughout.
    x(t) = x0 cos(omega t) + (v0/omega) sin(omega t)
    v(t) = -x0 omega sin(omega t) + v0 cos(omega t)
    """
    t_arr = np.asarray(t, dtype=float)
    if abs(omega) < 1e-15:
        x = x0 + v0 * t_arr
        v = np.full_like(t_arr, v0, dtype=float)
        return x, v

    wt = omega * t_arr
    x = x0 * np.cos(wt) + (v0 / omega) * np.sin(wt)
    v = -x0 * omega * np.sin(wt) + v0 * np.cos(wt)
    return x, v


def exact_phase_curve(num_points: int = 1200, t_final: float = T_FINAL):
    t = np.linspace(0.0, t_final, num_points, dtype=float)
    return exact_solution(t)


def load_manifest():
    manifest_path = f"{OUT_DIR}/manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(filepath: str):
    """Load CSV with header, skipping comment lines."""

    def non_comment_lines(handle):
        for line in handle:
            if line.strip() and not line.startswith("#"):
                yield line

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = list(non_comment_lines(f))
    if not lines:
        return None

    data = np.genfromtxt(lines, delimiter=",", names=True)
    if data is None:
        return None
    if getattr(data, "shape", ()) == ():
        data = np.array([data], dtype=data.dtype)
    return data


def write_csv(path: str, fieldnames: List[str], rows: List[Dict[str, object]]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"Saved {path}")


def markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def fmt_sci(x: float, digits: int = 3) -> str:
    if not np.isfinite(x):
        return "nan"
    return f"{x:.{digits}e}"


def fmt_pct_from_ratio(x: float, digits: int = 4) -> str:
    if not np.isfinite(x):
        return "nan"
    pct = 100.0 * x
    if abs(pct) < 10 ** (-digits):
        return f"{pct:.2e}%"
    return f"{pct:.{digits}f}%"


def write_plot_metadata(plot_png_name: str, extra: Dict[str, object]) -> None:
    os.makedirs(PLOT_META_DIR, exist_ok=True)
    payload = {
        "generated_utc": utc_now(),
        "plot_file_png": f"{PLOT_DIR}/{plot_png_name}",
        "parameters": {
            "omega": OMEGA,
            "x0": X0,
            "v0": V0,
            "t_final": T_FINAL,
            "dt_small": DT_SMALL,
            "dt_large": DT_LARGE,
            "exact_solution": "x(t)=x0 cos(omega t)+(v0/omega) sin(omega t); v(t)=-x0 omega sin(omega t)+v0 cos(omega t)",
        },
    }
    payload.update(extra)
    sidecar_name = f"{os.path.splitext(plot_png_name)[0]}.json"
    sidecar = f"{PLOT_META_DIR}/{sidecar_name}"
    with open(sidecar, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
    print(f"Saved {sidecar}")


def save_plot_pair(fig, png_name: str, metadata: Dict[str, object]) -> None:
    os.makedirs(PLOT_DIR, exist_ok=True)
    png_path = f"{PLOT_DIR}/{png_name}"
    save_figure(fig, png_path)
    print(f"Saved {png_path}")
    write_plot_metadata(png_name, metadata)


def run_ho_simulations():
    """Optional helper: rerun HO sweep and refresh manifest entries."""
    os.makedirs(f"{OUT_DIR}/runs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for integ in INTEGRATORS:
        for dt in DT_VALUES:
            steps = DT_STEPS[dt]
            run_dir = f"{OUT_DIR}/runs/ho_N1_{integ}_dt{dt}_{timestamp}"
            os.makedirs(run_dir, exist_ok=True)
            cmd = [
                "mpirun",
                "-np",
                "1",
                "./md_solver",
                "--mode",
                "ho",
                "--integrator",
                integ,
                "--dt",
                str(dt),
                "--steps",
                str(steps),
                "--N",
                "1",
                "--outdir",
                run_dir,
            ]
            print(f"Running: {integ} dt={dt} steps={steps}")
            subprocess.run(cmd, check=True)
            dst = f"{run_dir}/ho_{integ}.csv"
            if os.path.exists(dst):
                subprocess.run(
                    [sys.executable, "scripts/append_manifest.py", f"ho_convergence.{integ}_dt{dt_key(dt)}", dst],
                    check=True,
                )
    print("All HO simulations complete and manifest updated.")


def collect_ho_data(manifest) -> Tuple[Dict[str, Dict[float, Dict[str, object]]], List[str]]:
    datasets: Dict[str, Dict[float, Dict[str, object]]] = {integ: {} for integ in INTEGRATORS}
    warnings: List[str] = []
    ho_map = manifest.get("ho_convergence", {})
    for integ in INTEGRATORS:
        for dt in DT_VALUES:
            key = f"{integ}_dt{dt_key(dt)}"
            path = ho_map.get(key, "")
            if not path or not os.path.exists(path):
                warnings.append(f"missing data file for {key}: {path or '(empty manifest path)'}")
                continue
            data = load_csv(path)
            if data is None or len(data) == 0:
                warnings.append(f"empty or unreadable CSV for {key}: {path}")
                continue
            datasets[integ][dt] = {"path": path, "data": data}
    return datasets, warnings


def compute_metrics_for_dataset(integ: str, dt: float, dataset: Dict[str, object]) -> Dict[str, object]:
    data = dataset["data"]
    path = dataset["path"]
    names = set(data.dtype.names or [])
    required = {"time", "x", "v"}
    if not required.issubset(names):
        raise ValueError(f"{path} missing required columns {sorted(required - names)}")

    t = np.asarray(data["time"], dtype=float)
    x = np.asarray(data["x"], dtype=float)
    v = np.asarray(data["v"], dtype=float)
    if len(t) == 0:
        raise ValueError(f"{path} has no trajectory rows")

    x_exact, v_exact = exact_solution(t)
    endpoint_x_error = float(abs(x[-1] - x_exact[-1]))
    endpoint_v_error = float(abs(v[-1] - v_exact[-1]))

    phase_dist = np.sqrt((x - x_exact) ** 2 + (v - v_exact) ** 2)
    finite_phase = np.isfinite(phase_dist)
    rms_phase_error = float(np.sqrt(np.mean(phase_dist[finite_phase] ** 2))) if np.any(finite_phase) else float("nan")

    max_relative_energy_drift = float("nan")
    if "E_total" in names:
        E = np.asarray(data["E_total"], dtype=float)
        finite_E = np.isfinite(E)
        if np.any(finite_E):
            E = E[finite_E]
            E0 = E[0]
            if abs(E0) > 1e-30:
                max_relative_energy_drift = float(np.max(np.abs((E - E0) / abs(E0))))
            else:
                max_relative_energy_drift = float(np.max(np.abs(E - E0)))

    return {
        "integrator": integ,
        "integrator_label": INTEGRATOR_LABELS[integ],
        "dt": float(dt),
        "path": path,
        "final_time": float(t[-1]),
        "x_num_final": float(x[-1]),
        "v_num_final": float(v[-1]),
        "x_exact_final": float(x_exact[-1]),
        "v_exact_final": float(v_exact[-1]),
        "endpoint_position_error": endpoint_x_error,
        "endpoint_velocity_error": endpoint_v_error,
        "rms_phase_space_error": rms_phase_error,
        "max_relative_energy_drift": max_relative_energy_drift,
    }


def compute_metrics(datasets: Dict[str, Dict[float, Dict[str, object]]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for integ in INTEGRATORS:
        for dt in DT_VALUES:
            ds = datasets.get(integ, {}).get(dt)
            if ds is None:
                continue
            rows.append(compute_metrics_for_dataset(integ, dt, ds))
    return rows


def integrator_rank(name: str) -> int:
    try:
        return INTEGRATORS.index(name)
    except ValueError:
        return len(INTEGRATORS)


def sorted_metrics(metrics: List[Dict[str, object]]) -> List[Dict[str, object]]:
    return sorted(metrics, key=lambda r: (integrator_rank(str(r["integrator"])), -float(r["dt"])))


def metrics_index(metrics: List[Dict[str, object]]) -> Dict[Tuple[str, float], Dict[str, object]]:
    return {(str(r["integrator"]), float(r["dt"])): r for r in metrics}


def select_fit_points(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    fit_pts = [(dt, err) for dt, err in points if dt <= 0.1]
    if len(fit_pts) < 3:
        fit_pts = sorted(points)[: max(3, len(points) // 2)]
    return sorted(fit_pts)


def fit_loglog(points: List[Tuple[float, float]]) -> Tuple[float, float]:
    x = np.log10(np.asarray([p[0] for p in points], dtype=float))
    y = np.log10(np.asarray([p[1] for p in points], dtype=float))
    slope, intercept = np.polyfit(x, y, 1)
    return float(slope), float(intercept)


def build_fit_summary(
    metrics: List[Dict[str, object]],
    metric_key: str,
    epsilon: float,
    metric_name: str,
) -> Dict[str, Dict[str, object]]:
    out: Dict[str, Dict[str, object]] = {}
    for integ in INTEGRATORS:
        raw = []
        for row in metrics:
            if row["integrator"] != integ:
                continue
            err = float(row[metric_key])
            if np.isfinite(err) and err > epsilon:
                raw.append((float(row["dt"]), err))
        raw = sorted(raw)
        if len(raw) < 2:
            continue
        fit_pts = select_fit_points(raw)
        if len(fit_pts) < 2:
            continue
        slope, intercept = fit_loglog(fit_pts)
        fit_dts = [float(dt) for dt, _ in fit_pts]
        excluded = [float(dt) for dt, _ in raw if not any(abs(dt - fdt) < 1e-15 for fdt in fit_dts)]
        out[integ] = {
            "metric": metric_name,
            "integrator": integ,
            "integrator_label": INTEGRATOR_LABELS[integ],
            "expected_order": INTEGRATOR_ORDERS[integ],
            "slope": slope,
            "intercept": intercept,
            "fit_dts": fit_dts,
            "excluded_dts": excluded,
            "n_points": len(raw),
        }
    return out


def row_for(metrics_idx: Dict[Tuple[str, float], Dict[str, object]], integ: str, dt: float):
    return metrics_idx.get((integ, dt))


def merge_fit_info(endpoint_fit: Dict[str, Dict[str, object]], rms_fit: Dict[str, Dict[str, object]]):
    merged = {}
    for integ in INTEGRATORS:
        ep = endpoint_fit.get(integ)
        rm = rms_fit.get(integ)
        if ep is None or rm is None:
            continue
        excluded_union = sorted(set([float(x) for x in ep["excluded_dts"]] + [float(x) for x in rm["excluded_dts"]]))
        merged[integ] = {
            "integrator_label": INTEGRATOR_LABELS[integ],
            "endpoint_slope": float(ep["slope"]),
            "rms_slope": float(rm["slope"]),
            "expected_order": INTEGRATOR_ORDERS[integ],
            "endpoint_fit_dt_values": [float(v) for v in ep["fit_dts"]],
            "rms_fit_dt_values": [float(v) for v in rm["fit_dts"]],
            "excluded_coarse_dt_values": excluded_union,
        }
    return merged


def add_reference_slope(ax, dts: np.ndarray, errs: np.ndarray, expected: int, color: str) -> None:
    anchor_idx = len(dts) // 2
    dt_anchor = dts[anchor_idx]
    err_anchor = errs[anchor_idx]
    dt_ref = np.array([np.min(dts), np.max(dts)], dtype=float)
    err_ref = err_anchor * (dt_ref / dt_anchor) ** expected
    ax.loglog(dt_ref, err_ref, "--", color=color, alpha=0.45, linewidth=1.2)


def _window_yrange(series: List[Tuple[np.ndarray, np.ndarray]], t0: float, t1: float, pad_frac: float = 0.20) -> Tuple[float, float]:
    vals: List[np.ndarray] = []
    for t, y in series:
        tt = np.asarray(t, dtype=float)
        yy = np.asarray(y, dtype=float)
        mask = (tt >= t0) & (tt <= t1)
        if np.any(mask):
            vals.append(yy[mask])
    if not vals:
        y0 = np.asarray(series[0][1], dtype=float)
        return float(np.min(y0)), float(np.max(y0))
    stacked = np.concatenate(vals)
    ymin = float(np.nanmin(stacked))
    ymax = float(np.nanmax(stacked))
    span = ymax - ymin
    if span <= 1e-14:
        span = max(abs(ymax) * 0.1, 1e-3)
    return ymin - pad_frac * span, ymax + pad_frac * span


def plot_figure1_trajectories(datasets: Dict[str, Dict[float, Dict[str, object]]]) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(9.2, 7.6), sharex=True, constrained_layout=False)
    t_exact = np.linspace(0.0, T_FINAL, 2000, dtype=float)
    x_exact, v_exact = exact_solution(t_exact)
    exact_style = INTEGRATOR_STYLE["exact"]
    zoom_t0, zoom_t1 = 9.0, 10.0
    plot_series = {
        "x": [("exact", t_exact, x_exact)],
        "v": [("exact", t_exact, v_exact)],
    }

    for integ in INTEGRATORS:
        ds = datasets.get(integ, {}).get(TRAJ_DT)
        if ds is None:
            print(f"Warning: {integ} dt={TRAJ_DT:g} missing for Figure 1.")
            continue
        data = ds["data"]
        style = INTEGRATOR_STYLE[integ]
        lw = float(style["linewidth"])
        alpha = 0.95
        if integ == "euler":
            lw = 2.3
            alpha = 0.98
        elif integ in ("verlet", "rk4"):
            lw = 2.0
            alpha = 0.93
        axes[0].plot(
            data["time"],
            data["x"],
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=lw,
            alpha=alpha,
            zorder=3,
            label=INTEGRATOR_LABELS[integ],
        )
        axes[1].plot(
            data["time"],
            data["v"],
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=lw,
            alpha=alpha,
            zorder=3,
            label=INTEGRATOR_LABELS[integ],
        )
        t_num = np.asarray(data["time"], dtype=float)
        plot_series["x"].append((integ, t_num, np.asarray(data["x"], dtype=float)))
        plot_series["v"].append((integ, t_num, np.asarray(data["v"], dtype=float)))

    axes[0].plot(
        t_exact,
        x_exact,
        color=exact_style["color"],
        linestyle=exact_style["linestyle"],
        linewidth=2.0,
        alpha=0.90,
        zorder=6,
        label="Exact",
    )
    axes[1].plot(
        t_exact,
        v_exact,
        color=exact_style["color"],
        linestyle=exact_style["linestyle"],
        linewidth=2.0,
        alpha=0.90,
        zorder=6,
        label="Exact",
    )

    # Keep full context and stable axis limits across reruns.
    axes[1].set_xlim(0.0, T_FINAL)
    # Subtle source-window highlight for the endpoint zoom.
    for ax in axes:
        ax.axvspan(zoom_t0, zoom_t1, color="#9a9a9a", alpha=0.08, zorder=0)

    inset_meta: Dict[str, object] = {}
    panel_specs = [("x", axes[0], "x"), ("v", axes[1], "v")]
    for panel_key, ax, ykey in panel_specs:
        series = [(t, y) for _, t, y in plot_series[ykey]]
        axins = inset_axes(ax, width="20%", height="24%", loc="upper right", borderpad=0.95)
        inset_meta[panel_key] = {"used": True, "placement": "inside-upper right", "time_window": [zoom_t0, zoom_t1]}

        for integ, t, y in plot_series[ykey]:
            if integ == "exact":
                st = exact_style
                lw = 1.8
                alpha = 0.88
            else:
                st = INTEGRATOR_STYLE[str(integ)]
                lw = 2.1 if integ == "euler" else 1.8
                alpha = 0.96 if integ == "euler" else 0.92
            axins.plot(t, y, color=st["color"], linestyle=st["linestyle"], linewidth=lw, alpha=alpha, zorder=3)

        yz0, yz1 = _window_yrange(series, zoom_t0, zoom_t1, pad_frac=0.22)
        axins.set_xlim(zoom_t0, zoom_t1)
        axins.set_ylim(yz0, yz1)
        apply_major_grid(axins)
        disable_offset_text(axins)
        axins.tick_params(axis="both", which="major", labelsize=7)

    axes[0].set_title("(a) Position x(t)", loc="left")
    axes[1].set_title("(b) Velocity v(t)", loc="left")
    axes[0].set_ylabel("Position x [reduced units]")
    axes[1].set_ylabel("Velocity v [reduced units]")
    axes[1].set_xlabel(r"Time $[1/\omega]$")
    for ax in axes:
        apply_major_grid(ax)
        disable_offset_text(ax)
        # Add top headroom so inset bottoms clear nearby curves.
        ymin, ymax = ax.get_ylim()
        span = ymax - ymin
        if span > 0:
            ax.set_ylim(ymin, ymax + 0.10 * span)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 0.965))
    fig.suptitle(r"Harmonic oscillator trajectories ($\Delta t=0.01$)", fontsize=13, y=0.995)
    fig.subplots_adjust(top=0.88, bottom=0.10, left=0.10, right=0.98, hspace=0.24)

    save_plot_pair(
        fig,
        FIG1_PNG,
        {
            "kind": "main_results1_figure",
            "figure_number": 1,
            "claim": "Shows position and velocity trajectories at dt=0.01 for Euler, Velocity-Verlet, RK4 versus exact.",
            "panels": ["(a) x(t)", "(b) v(t)"],
            "insets": inset_meta,
            "zoom_window": [zoom_t0, zoom_t1],
            "endpoint_note": "Near-overlap is expected at small Δt; endpoint errors still rank Euler > Velocity-Verlet > RK4.",
            "shared_legend": True,
        },
    )
    plt.close(fig)


def plot_figure2_phase_space(datasets: Dict[str, Dict[float, Dict[str, object]]]) -> None:
    fig, ax = plt.subplots(figsize=(6.7, 6.5), constrained_layout=False)
    exact_style = INTEGRATOR_STYLE["exact"]
    series = {}

    for integ in INTEGRATORS:
        ds = datasets.get(integ, {}).get(TRAJ_DT)
        if ds is None:
            print(f"Warning: {integ} dt={TRAJ_DT:g} missing for Figure 2.")
            continue
        data = ds["data"]
        series[integ] = data
        style = INTEGRATOR_STYLE[integ]
        ax.plot(
            data["x"],
            data["v"],
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=style["linewidth"],
            alpha=0.96,
            zorder=3,
            label=INTEGRATOR_LABELS[integ],
        )

    x_exact, v_exact = exact_phase_curve(num_points=2200, t_final=T_FINAL)
    ax.plot(
        x_exact,
        v_exact,
        color=exact_style["color"],
        linestyle=exact_style["linestyle"],
        linewidth=2.4,
        alpha=0.98,
        zorder=6,
        label="Exact",
    )

    ax.set_title(r"Phase-space trajectories ($\Delta t=0.01$)")
    ax.set_xlabel("Position x [reduced units]")
    ax.set_ylabel("Velocity v [reduced units]")
    ax.set_aspect("equal", "box")
    apply_major_grid(ax)
    disable_offset_text(ax)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False, borderaxespad=0.0)

    # Place zoom outside the main axes, under the external legend.
    axins = inset_axes(
        ax,
        width="24%",
        height="24%",
        bbox_to_anchor=(1.10, 0.07, 0.98, 0.98),
        bbox_transform=ax.transAxes,
        loc="lower left",
        borderpad=0.0,
    )
    # Inset: local final-time sector with all methods; endpoint markers reveal near-coincidence.
    zoom_t_start = 8.8
    zx_all: List[float] = []
    zv_all: List[float] = []
    marker_map = {"euler": "o", "verlet": "s", "rk4": "^"}
    for integ in INTEGRATORS:
        data = series.get(integ)
        if data is None:
            continue
        style = INTEGRATOR_STYLE[integ]
        tt = np.asarray(data["time"], dtype=float)
        xx = np.asarray(data["x"], dtype=float)
        vv = np.asarray(data["v"], dtype=float)
        mask = tt >= zoom_t_start
        if np.any(mask):
            xloc = xx[mask]
            vloc = vv[mask]
            axins.plot(
                xloc,
                vloc,
                color=style["color"],
                linestyle=style["linestyle"],
                linewidth=style["linewidth"],
                alpha=0.98,
                zorder=3,
            )
            axins.plot(xloc[-1], vloc[-1], marker=marker_map.get(integ, "o"), markersize=4.0, color=style["color"], zorder=4)
            zx_all.extend(xloc.tolist())
            zv_all.extend(vloc.tolist())
    tz = np.linspace(zoom_t_start, T_FINAL, 400, dtype=float)
    xz, vz = exact_solution(tz)
    axins.plot(xz, vz, color=exact_style["color"], linestyle=":", linewidth=1.6, alpha=0.85, zorder=2)
    axins.plot(xz[-1], vz[-1], marker="D", markersize=4.0, color=exact_style["color"], zorder=4)
    zx_all.extend(xz.tolist())
    zv_all.extend(vz.tolist())
    if zx_all and zv_all:
        xmin, xmax = min(zx_all), max(zx_all)
        ymin, ymax = min(zv_all), max(zv_all)
        xpad = max(0.01, 0.22 * (xmax - xmin))
        ypad = max(0.01, 0.22 * (ymax - ymin))
        axins.set_xlim(xmin - xpad, xmax + xpad)
        axins.set_ylim(ymin - ypad, ymax + ypad)
    axins.set_title(r"Zoom near $t\approx T$", fontsize=7.8, pad=2)
    axins.tick_params(axis="both", which="major", labelsize=7)
    apply_major_grid(axins)
    disable_offset_text(axins)
    fig.subplots_adjust(left=0.12, right=0.74, top=0.91, bottom=0.11)

    save_plot_pair(
        fig,
        FIG2_PNG,
        {
            "kind": "main_results1_figure",
            "figure_number": 2,
            "claim": "Shows phase-space geometry at dt=0.01 and qualitative orbit preservation differences.",
            "panel": "v_vs_x",
            "shared_legend": True,
        },
    )
    plt.close(fig)


def _plot_small_large_series(ax, x_data, y_data, exact_x, exact_y, method_color, include_coarse: bool = True):
    # Keep exact clearly distinct from coarse/fine numerical styles in this comparison panel.
    exact_style = INTEGRATOR_STYLE["exact"]
    ax.plot(
        exact_x,
        exact_y,
        color=exact_style["color"],
        linestyle=":",
        linewidth=max(2.0, float(exact_style["linewidth"])),
        alpha=0.95,
    )
    if include_coarse:
        ax.plot(
            x_data["coarse"],
            y_data["coarse"],
            color=method_color,
            linestyle="-.",
            linewidth=1.9,
            alpha=0.92,
        )
    ax.plot(x_data["fine"], y_data["fine"], color=method_color, linestyle="-", linewidth=2.2, alpha=0.92)


def plot_figure3_small_vs_large(
    datasets: Dict[str, Dict[float, Dict[str, object]]],
    metrics_idx: Dict[Tuple[str, float], Dict[str, object]],
) -> None:
    fig, axes = plt.subplots(len(INTEGRATORS), 2, figsize=(12.8, 11.1), constrained_layout=False)
    t_exact = np.linspace(0.0, T_FINAL, 2400, dtype=float)
    x_exact, v_exact = exact_solution(t_exact)

    for row_idx, integ in enumerate(INTEGRATORS):
        ax_traj = axes[row_idx, 0]
        ax_phase = axes[row_idx, 1]
        color = INTEGRATOR_STYLE[integ]["color"]

        ds_large = datasets.get(integ, {}).get(DT_LARGE)
        ds_small = datasets.get(integ, {}).get(DT_SMALL)
        if ds_large is None or ds_small is None:
            print(f"Warning: missing dt={DT_LARGE:g} or dt={DT_SMALL:g} for {integ} in Figure 3.")
            continue
        d_large = ds_large["data"]
        d_small = ds_small["data"]

        _plot_small_large_series(
            ax_traj,
            {"coarse": d_large["time"], "fine": d_small["time"]},
            {"coarse": d_large["x"], "fine": d_small["x"]},
            t_exact,
            x_exact,
            color,
        )
        _plot_small_large_series(
            ax_phase,
            {"coarse": d_large["x"], "fine": d_small["x"]},
            {"coarse": d_large["v"], "fine": d_small["v"]},
            x_exact,
            v_exact,
            color,
        )

        ax_traj.set_xlim(0.0, T_FINAL)
        ax_phase.set_aspect("equal", "box")
        ax_traj.set_ylabel(f"{INTEGRATOR_LABELS[integ]}\nPosition x")
        ax_phase.set_ylabel("Velocity v")
        if row_idx == len(INTEGRATORS) - 1:
            ax_traj.set_xlabel(r"Time $[1/\omega]$")
            ax_phase.set_xlabel("Position x")
        apply_major_grid(ax_traj)
        apply_major_grid(ax_phase)
        disable_offset_text(ax_traj)
        disable_offset_text(ax_phase)

    axes[0, 0].set_title("x(t) vs time", loc="left")
    axes[0, 1].set_title("phase space v(x)", loc="left")

    legend_handles = [
        Line2D(
            [0],
            [0],
            color=INTEGRATOR_STYLE["exact"]["color"],
            linestyle=":",
            linewidth=max(2.0, float(INTEGRATOR_STYLE["exact"]["linewidth"])),
            label="Exact",
        ),
        Line2D([0], [0], color="black", linestyle="-.", linewidth=2.0, label=f"Coarse dt={DT_LARGE:g}"),
        Line2D([0], [0], color="black", linestyle="-", linewidth=2.2, label=f"Fine dt={DT_SMALL:g}"),
    ]
    fig.legend(legend_handles, [h.get_label() for h in legend_handles], loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.972))
    fig.suptitle("Small vs Large Timestep Comparison", fontsize=13, y=0.995)
    fig.subplots_adjust(top=0.92, bottom=0.07, left=0.09, right=0.98, hspace=0.18, wspace=0.08)

    per_integrator = {}
    for integ in INTEGRATORS:
        m_large = row_for(metrics_idx, integ, DT_LARGE)
        m_small = row_for(metrics_idx, integ, DT_SMALL)
        if m_large is None or m_small is None:
            continue
        per_integrator[integ] = {
            "coarse": {
                "dt": DT_LARGE,
                "endpoint_position_error": float(m_large["endpoint_position_error"]),
                "endpoint_velocity_error": float(m_large["endpoint_velocity_error"]),
            },
            "fine": {
                "dt": DT_SMALL,
                "endpoint_position_error": float(m_small["endpoint_position_error"]),
                "endpoint_velocity_error": float(m_small["endpoint_velocity_error"]),
            },
        }

    save_plot_pair(
        fig,
        FIG3_PNG,
        {
            "kind": "main_results1_figure",
            "figure_number": 3,
            "claim": "Direct small-vs-large timestep comparison with full-range coarse behaviour retained; quantitative error values are reported in summary tables.",
            "layout": {"rows": INTEGRATORS, "columns": ["x(t)", "v(x)"]},
            "shared_legend": True,
            "error_annotations": per_integrator,
            "insets": {"euler_trajectory_zoom": False, "euler_phase_zoom": False},
        },
    )
    plt.close(fig)


def _plot_convergence_panel(
    ax,
    metrics: List[Dict[str, object]],
    fit_summary: Dict[str, Dict[str, object]],
    metric_key: str,
    epsilon: float,
    ylabel: str,
    panel_title: str,
):
    method_handles: List[Line2D] = []
    for integ in INTEGRATORS:
        rows = [
            (float(r["dt"]), float(r[metric_key]))
            for r in metrics
            if r["integrator"] == integ and np.isfinite(float(r[metric_key])) and float(r[metric_key]) > epsilon
        ]
        rows = sorted(rows)
        if len(rows) < 2:
            continue
        dts = np.asarray([p[0] for p in rows], dtype=float)
        errs = np.asarray([p[1] for p in rows], dtype=float)
        style = INTEGRATOR_STYLE[integ]
        expected = INTEGRATOR_ORDERS[integ]
        fit_info = fit_summary.get(integ, {})
        slope = fit_info.get("slope", float("nan"))
        label = f"{INTEGRATOR_LABELS[integ]} (s={float(slope):.2f}, exp {expected})"
        line = ax.loglog(
            dts,
            errs,
            linestyle=style["linestyle"],
            color=style["color"],
            linewidth=style["linewidth"],
            alpha=0.95,
            label=label,
        )[0]
        method_handles.append(line)

        fit_dts = [float(v) for v in fit_info.get("fit_dts", [])]
        if fit_dts:
            inc_mask = np.array([any(abs(dt - fd) <= 1e-12 * max(1.0, abs(dt), abs(fd)) for fd in fit_dts) for dt in dts], dtype=bool)
        else:
            inc_mask = np.ones_like(dts, dtype=bool)
        exc_mask = ~inc_mask

        ax.scatter(dts[inc_mask], errs[inc_mask], marker="o", s=40, facecolors=style["color"], edgecolors=style["color"], linewidths=0.8, zorder=4)
        if np.any(exc_mask):
            ax.scatter(dts[exc_mask], errs[exc_mask], marker="o", s=40, facecolors="white", edgecolors=style["color"], linewidths=1.3, zorder=4)

        if fit_dts and np.isfinite(float(fit_info.get("intercept", float("nan")))):
            dt_fit = np.asarray(sorted(fit_dts), dtype=float)
            dt_fit_line = np.array([np.min(dt_fit), np.max(dt_fit)], dtype=float)
            err_fit_line = (10.0 ** float(fit_info["intercept"])) * (dt_fit_line ** float(fit_info["slope"]))
            ax.loglog(dt_fit_line, err_fit_line, ":", color=style["color"], alpha=0.85, linewidth=1.7)

    ax.set_xlabel(r"$\Delta t\ [1/\omega]$")
    ax.set_ylabel(ylabel)
    ax.set_title(panel_title, loc="left")
    apply_major_grid(ax)
    disable_offset_text(ax)
    ax.legend(handles=method_handles, loc="best", frameon=False)


def plot_figure4_convergence_combined(
    metrics: List[Dict[str, object]],
    endpoint_fit: Dict[str, Dict[str, object]],
    rms_fit: Dict[str, Dict[str, object]],
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.0), constrained_layout=False)

    _plot_convergence_panel(
        axes[0],
        metrics=metrics,
        fit_summary=endpoint_fit,
        metric_key="endpoint_position_error",
        epsilon=1e-14,
        ylabel=r"$|x_{\mathrm{num}}(T)-x_{\mathrm{exact}}(T)|$",
        panel_title=r"(a) Endpoint position error at $T=10$",
    )
    _plot_convergence_panel(
        axes[1],
        metrics=metrics,
        fit_summary=rms_fit,
        metric_key="rms_phase_space_error",
        epsilon=1e-16,
        ylabel=r"$\mathrm{RMS}_t \sqrt{(x-x_{ex})^2 + (v-v_{ex})^2}$",
        panel_title=r"(b) RMS phase-space error over $0\leq t\leq 10$",
    )

    fig.suptitle(
        r"Convergence to the exact solution (expected orders: Euler 1, Velocity-Verlet 2, RK4 4)",
        fontsize=12.8,
        y=0.995,
    )
    fig.subplots_adjust(top=0.84, bottom=0.17, left=0.08, right=0.98, wspace=0.27)
    fig.text(
        0.5,
        0.040,
        r"Filled markers: used in slope fit ($\Delta t \leq 0.1$). Open markers: coarse points shown for context.",
        ha="center",
        va="center",
        fontsize=9,
    )

    meta_fits = {
        "endpoint_position_error": {
            integ: {
                "fitted_slope": float(info["slope"]),
                "expected_order": int(info["expected_order"]),
                "fit_dt_values": [float(v) for v in info["fit_dts"]],
                "excluded_dt_values": [float(v) for v in info["excluded_dts"]],
            }
            for integ, info in endpoint_fit.items()
        },
        "rms_phase_space_error": {
            integ: {
                "fitted_slope": float(info["slope"]),
                "expected_order": int(info["expected_order"]),
                "fit_dt_values": [float(v) for v in info["fit_dts"]],
                "excluded_dt_values": [float(v) for v in info["excluded_dts"]],
            }
            for integ, info in rms_fit.items()
        },
    }

    save_plot_pair(
        fig,
        FIG4_PNG,
        {
            "kind": "main_results1_figure",
            "figure_number": 4,
            "claim": "Demonstrates first-, second-, and fourth-order convergence using endpoint and RMS phase-space metrics.",
            "panels": ["(a) endpoint_position_error", "(b) rms_phase_space_error"],
            "fit_rule": "dt <= 0.1; fallback to smallest half if fewer than 3 points",
            "fits": meta_fits,
            "coarse_points_retained_on_plot": True,
        },
    )
    plt.close(fig)


def plot_figure5_energy_diagnostic(
    datasets: Dict[str, Dict[float, Dict[str, object]]],
    metrics_idx: Dict[Tuple[str, float], Dict[str, object]],
) -> None:
    fig, ax = plt.subplots(figsize=(8.6, 5.3), constrained_layout=False)

    for integ in INTEGRATORS:
        ds = datasets.get(integ, {}).get(TRAJ_DT)
        if ds is None:
            continue
        data = ds["data"]
        if "E_total" not in set(data.dtype.names or []):
            continue
        t = np.asarray(data["time"], dtype=float)
        E = np.asarray(data["E_total"], dtype=float)
        finite = np.isfinite(E)
        if not np.any(finite):
            continue
        t = t[finite]
        E = E[finite]
        E0 = E[0]
        rel = (E - E0) / abs(E0) if abs(E0) > 1e-30 else (E - E0)
        style = INTEGRATOR_STYLE[integ]
        ax.plot(
            t,
            rel,
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=style["linewidth"],
            label=INTEGRATOR_LABELS[integ],
        )

    ax.set_xlabel(r"Time $[1/\omega]$")
    ax.set_ylabel(r"$(E-E_0)/|E_0|$ (dimensionless)")
    ax.set_title(r"Energy drift at $\Delta t=0.01$")
    apply_major_grid(ax)
    disable_offset_text(ax)
    ax.legend(loc="upper right", bbox_to_anchor=(0.995, 0.60), frameon=False)

    summary_lines = []
    for integ in INTEGRATORS:
        row = row_for(metrics_idx, integ, TRAJ_DT)
        if row is None:
            continue
        summary_lines.append((integ, INTEGRATOR_LABELS[integ], fmt_pct_from_ratio(float(row["max_relative_energy_drift"]), 4)))
    if summary_lines:
        ax.text(
            0.02,
            0.985,
            "Max relative energy drift",
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=8.7,
            fontweight="semibold",
            bbox={"facecolor": "white", "alpha": 0.90, "edgecolor": "none", "pad": 0.25},
        )
        y = 0.952
        for integ, label, drift_text in summary_lines:
            ax.text(
                0.02,
                y,
                label,
                transform=ax.transAxes,
                va="top",
                ha="left",
                fontsize=8.2,
                color=INTEGRATOR_STYLE[integ]["color"],
                fontweight="semibold",
                bbox={"facecolor": "white", "alpha": 0.90, "edgecolor": "none", "pad": 0.15},
            )
            ax.text(
                0.20,
                y,
                f"max |ΔE/E0| = {drift_text}",
                transform=ax.transAxes,
                va="top",
                ha="left",
                fontsize=8.2,
                color="#222222",
                bbox={"facecolor": "white", "alpha": 0.90, "edgecolor": "none", "pad": 0.15},
            )
            y -= 0.038

    axins = inset_axes(
        ax,
        width="31%",
        height="27%",
        bbox_to_anchor=(0.0, 0.05, 1.0, 1.0),
        bbox_transform=ax.transAxes,
        loc="lower right",
        borderpad=2.0,
    )
    for integ in ("verlet", "rk4"):
        ds = datasets.get(integ, {}).get(TRAJ_DT)
        if ds is None:
            continue
        data = ds["data"]
        if "E_total" not in set(data.dtype.names or []):
            continue
        t = np.asarray(data["time"], dtype=float)
        E = np.asarray(data["E_total"], dtype=float)
        finite = np.isfinite(E)
        if not np.any(finite):
            continue
        t = t[finite]
        E = E[finite]
        E0 = E[0]
        rel = (E - E0) / abs(E0) if abs(E0) > 1e-30 else (E - E0)
        style = INTEGRATOR_STYLE[integ]
        axins.plot(t, rel, color=style["color"], linestyle=style["linestyle"], linewidth=style["linewidth"])
    axins.set_title("Zoom: VV vs RK4", fontsize=8.5, pad=2)
    axins.tick_params(axis="both", which="major", labelsize=7)
    axins.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.1e}"))
    apply_major_grid(axins)
    disable_offset_text(axins)

    # Keep lower area clean for publication readability; no extra sentence below inset.
    fig.subplots_adjust(top=0.90, bottom=0.12, left=0.10, right=0.98)

    save_plot_pair(
        fig,
        FIG5_PNG,
        {
            "kind": "supporting_results1_figure",
            "figure_number": 5,
            "claim": "Supporting diagnostic: Euler shows strong drift, Velocity-Verlet bounded oscillatory error, RK4 tiny drift on this interval.",
            "note": "RK4 is not symplectic.",
        },
    )
    plt.close(fig)


def _write_markdown(path: str, lines: List[str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Saved {path}")


def generate_table_outputs(
    metrics: List[Dict[str, object]],
    endpoint_fit: Dict[str, Dict[str, object]],
    rms_fit: Dict[str, Dict[str, object]],
    sanity_warnings: List[str],
) -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(SUMMARY_RESULTS1_DIR, exist_ok=True)
    ordered = sorted_metrics(metrics)
    idx = metrics_index(metrics)

    # 1) Small-vs-large summary
    small_large_rows = []
    for integ in INTEGRATORS:
        for dt in [DT_LARGE, DT_SMALL]:
            row = row_for(idx, integ, dt)
            if row is None:
                continue
            small_large_rows.append(
                {
                    "integrator": integ,
                    "integrator_label": INTEGRATOR_LABELS[integ],
                    "dt": float(dt),
                    "endpoint_position_error": float(row["endpoint_position_error"]),
                    "endpoint_velocity_error": float(row["endpoint_velocity_error"]),
                    "rms_phase_space_error": float(row["rms_phase_space_error"]),
                    "max_relative_energy_drift": float(row["max_relative_energy_drift"]),
                }
            )
    write_csv(
        R1_SMALL_LARGE_CSV,
        [
            "integrator",
            "integrator_label",
            "dt",
            "endpoint_position_error",
            "endpoint_velocity_error",
            "rms_phase_space_error",
            "max_relative_energy_drift",
        ],
        small_large_rows,
    )
    small_large_md = [
        "# Results 1 HO Small-vs-Large Timestep Summary",
        "",
        f"Generated: {utc_now()}",
        "",
        markdown_table(
            [
                "Integrator",
                "dt",
                "abs(x(T)-x_exact(T))",
                "abs(v(T)-v_exact(T))",
                "RMS phase-space error",
                "max abs(E-E0)/abs(E0)",
            ],
            [
                [
                    INTEGRATOR_LABELS[str(r["integrator"])],
                    format_dt(float(r["dt"])),
                    fmt_sci(float(r["endpoint_position_error"]), 3),
                    fmt_sci(float(r["endpoint_velocity_error"]), 3),
                    fmt_sci(float(r["rms_phase_space_error"]), 3),
                    fmt_sci(float(r["max_relative_energy_drift"]), 3),
                ]
                for r in small_large_rows
            ],
        ),
    ]
    _write_markdown(R1_SMALL_LARGE_MD, small_large_md)

    # 2) Convergence summary
    merged_fit = merge_fit_info(endpoint_fit, rms_fit)
    convergence_rows = []
    for integ in INTEGRATORS:
        info = merged_fit.get(integ)
        if info is None:
            continue
        convergence_rows.append(
            {
                "integrator": integ,
                "integrator_label": info["integrator_label"],
                "endpoint_position_slope": info["endpoint_slope"],
                "rms_phase_space_slope": info["rms_slope"],
                "endpoint_fit_dt_values": ";".join(format_dt(float(v)) for v in info["endpoint_fit_dt_values"]),
                "rms_fit_dt_values": ";".join(format_dt(float(v)) for v in info["rms_fit_dt_values"]),
                "excluded_coarse_dt_values": ";".join(format_dt(float(v)) for v in info["excluded_coarse_dt_values"]),
            }
        )
    write_csv(
        R1_CONVERGENCE_CSV,
        [
            "integrator",
            "integrator_label",
            "endpoint_position_slope",
            "rms_phase_space_slope",
            "endpoint_fit_dt_values",
            "rms_fit_dt_values",
            "excluded_coarse_dt_values",
        ],
        convergence_rows,
    )
    conv_md = [
        "# Results 1 HO Convergence Summary",
        "",
        f"Generated: {utc_now()}",
        "",
        markdown_table(
            [
                "Integrator",
                "Endpoint slope",
                "RMS slope",
                "Endpoint fit dt values",
                "RMS fit dt values",
                "Excluded coarse dt values",
            ],
            [
                [
                    str(r["integrator_label"]),
                    f"{float(r['endpoint_position_slope']):.2f}",
                    f"{float(r['rms_phase_space_slope']):.2f}",
                    str(r["endpoint_fit_dt_values"]),
                    str(r["rms_fit_dt_values"]),
                    str(r["excluded_coarse_dt_values"]) if str(r["excluded_coarse_dt_values"]) else "-",
                ]
                for r in convergence_rows
            ],
        ),
    ]
    _write_markdown(R1_CONVERGENCE_MD, conv_md)

    # 3) Endpoint values table (selected dt)
    selected_dts = [0.5, 0.1, 0.01]
    endpoint_rows = []
    for integ in INTEGRATORS:
        for dt in selected_dts:
            row = row_for(idx, integ, dt)
            if row is None:
                continue
            endpoint_rows.append(
                {
                    "integrator": integ,
                    "integrator_label": INTEGRATOR_LABELS[integ],
                    "dt": dt,
                    "x_num_final": float(row["x_num_final"]),
                    "x_exact_final": float(row["x_exact_final"]),
                    "endpoint_position_error": float(row["endpoint_position_error"]),
                    "v_num_final": float(row["v_num_final"]),
                    "v_exact_final": float(row["v_exact_final"]),
                    "endpoint_velocity_error": float(row["endpoint_velocity_error"]),
                }
            )
    write_csv(
        R1_ENDPOINT_VALUES_CSV,
        [
            "integrator",
            "integrator_label",
            "dt",
            "x_num_final",
            "x_exact_final",
            "endpoint_position_error",
            "v_num_final",
            "v_exact_final",
            "endpoint_velocity_error",
        ],
        endpoint_rows,
    )
    endpoint_md = [
        "# Results 1 HO Endpoint Values (Selected dt)",
        "",
        f"Generated: {utc_now()}",
        "",
        markdown_table(
            [
                "Integrator",
                "dt",
                "x_num(T)",
                "x_exact(T)",
                "abs(Δx(T))",
                "v_num(T)",
                "v_exact(T)",
                "abs(Δv(T))",
            ],
            [
                [
                    str(r["integrator_label"]),
                    format_dt(float(r["dt"])),
                    fmt_sci(float(r["x_num_final"]), 6),
                    fmt_sci(float(r["x_exact_final"]), 6),
                    fmt_sci(float(r["endpoint_position_error"]), 3),
                    fmt_sci(float(r["v_num_final"]), 6),
                    fmt_sci(float(r["v_exact_final"]), 6),
                    fmt_sci(float(r["endpoint_velocity_error"]), 3),
                ]
                for r in endpoint_rows
            ],
        ),
    ]
    _write_markdown(R1_ENDPOINT_VALUES_MD, endpoint_md)

    # 4) Caption/helper notes
    fig3_bits = []
    for integ in INTEGRATORS:
        coarse = row_for(idx, integ, DT_LARGE)
        fine = row_for(idx, integ, DT_SMALL)
        if coarse is None or fine is None:
            continue
        fig3_bits.append(
            f"{INTEGRATOR_LABELS[integ]} coarse/fine endpoint x-error ratio = "
            f"{float(coarse['endpoint_position_error']) / max(float(fine['endpoint_position_error']), 1e-300):.2f}"
        )

    notes = [
        "# Results 1 Figure Caption Notes (Auto-Generated)",
        "",
        f"Generated: {utc_now()}",
        "",
        f"Figure 1 (trajectories): Verifies x(t) and v(t) behaviour for all three methods against the exact solution at dt={format_dt(TRAJ_DT)}; Euler remains the visibly largest deviation while RK4 is nearly exact on this horizon.",
        "Figure 2 (phase space): Shows geometric orbit quality at dt=0.01, with Euler clearly outside the closed exact orbit and a dedicated final-sector zoom showing all methods with endpoint markers.",
        "Figure 3 (small vs large dt): Directly demonstrates timestep sensitivity with dt=0.5 and dt=0.01 for each method, retaining full coarse-range behaviour without dense in-panel text; quantitative values are provided in the summary tables; "
        + "; ".join(fig3_bits)
        + ".",
        f"Figure 4 (combined convergence): Fitted slopes are Euler {endpoint_fit['euler']['slope']:.2f}/{rms_fit['euler']['slope']:.2f}, Velocity-Verlet {endpoint_fit['verlet']['slope']:.2f}/{rms_fit['verlet']['slope']:.2f}, RK4 {endpoint_fit['rk4']['slope']:.2f}/{rms_fit['rk4']['slope']:.2f} (endpoint/RMS), consistent with orders 1/2/4; filled markers denote fit-included points and open markers denote coarse points shown for context.",
        "Figure 5 (energy diagnostic): At dt=0.01, Euler exhibits strong secular drift, Velocity-Verlet shows bounded oscillatory error, and RK4 drift is tiny on this interval; RK4 remains non-symplectic.",
    ]
    if sanity_warnings:
        notes.append("")
        notes.append("Sanity warnings:")
        for warning in sanity_warnings:
            notes.append(f"- WARNING: {warning}")
    _write_markdown(R1_CAPTION_NOTES_MD, notes)

    # Keep one compact machine summary for compatibility with downstream note workflows.
    legacy_notes = [
        "# Results 1 Auto-Summary Notes",
        "",
        f"Generated: {utc_now()}",
        "",
        f"Endpoint slopes: Euler {endpoint_fit['euler']['slope']:.2f}, Velocity-Verlet {endpoint_fit['verlet']['slope']:.2f}, RK4 {endpoint_fit['rk4']['slope']:.2f}.",
        f"RMS slopes: Euler {rms_fit['euler']['slope']:.2f}, Velocity-Verlet {rms_fit['verlet']['slope']:.2f}, RK4 {rms_fit['rk4']['slope']:.2f}.",
    ]
    _write_markdown(R1_SECTION_NOTES_MD, legacy_notes)


def run_sanity_checks(
    endpoint_fit: Dict[str, Dict[str, object]],
    rms_fit: Dict[str, Dict[str, object]],
    metrics_idx: Dict[Tuple[str, float], Dict[str, object]],
) -> List[str]:
    warnings: List[str] = []

    for integ in INTEGRATORS:
        expected = INTEGRATOR_ORDERS[integ]
        efit = endpoint_fit.get(integ)
        if efit is None:
            warnings.append(f"missing endpoint-position fit for {integ}")
        else:
            slope = float(efit["slope"])
            if abs(slope - expected) > 0.35:
                warnings.append(f"endpoint-position slope for {integ} is {slope:.2f}, far from expected {expected}")

        rfit = rms_fit.get(integ)
        if rfit is None:
            warnings.append(f"missing RMS phase-space fit for {integ}")
        else:
            slope = float(rfit["slope"])
            if abs(slope - expected) > 0.35:
                warnings.append(f"RMS phase-space slope for {integ} is {slope:.2f}, far from expected {expected}")

    for integ in INTEGRATORS:
        coarse = row_for(metrics_idx, integ, DT_LARGE)
        fine = row_for(metrics_idx, integ, DT_SMALL)
        if coarse is None or fine is None:
            warnings.append(f"cannot compare coarse vs fine dt for {integ}")
            continue
        if float(coarse["endpoint_position_error"]) <= float(fine["endpoint_position_error"]):
            warnings.append(f"coarse dt position error is not larger than fine dt for {integ} ({DT_LARGE:g} vs {DT_SMALL:g})")
        if float(coarse["endpoint_velocity_error"]) <= float(fine["endpoint_velocity_error"]):
            warnings.append(f"coarse dt velocity error is not larger than fine dt for {integ} ({DT_LARGE:g} vs {DT_SMALL:g})")

    euler = row_for(metrics_idx, "euler", DT_SMALL)
    verlet = row_for(metrics_idx, "verlet", DT_SMALL)
    if euler is not None and verlet is not None:
        if float(euler["max_relative_energy_drift"]) <= float(verlet["max_relative_energy_drift"]):
            warnings.append("Euler energy drift is not larger than Velocity-Verlet at dt=0.01")
    else:
        warnings.append("missing dt=0.01 energy-drift rows for Euler and/or Velocity-Verlet")

    return warnings


def main():
    apply_plot_style()

    if "--run" in sys.argv:
        run_ho_simulations()

    manifest = load_manifest()
    datasets, data_warnings = collect_ho_data(manifest)
    for warning in data_warnings:
        print(f"Warning: {warning}")

    required_missing = []
    for integ in INTEGRATORS:
        for dt in [DT_SMALL, DT_LARGE]:
            if dt not in datasets.get(integ, {}):
                required_missing.append(f"{integ} dt={dt:g}")
    if required_missing:
        raise RuntimeError("Missing required HO datasets for small-vs-large comparison: " + ", ".join(required_missing))

    metrics = compute_metrics(datasets)
    if not metrics:
        raise RuntimeError("No HO metrics could be computed from manifest datasets.")
    m_idx = metrics_index(metrics)

    endpoint_fit = build_fit_summary(
        metrics=metrics,
        metric_key="endpoint_position_error",
        epsilon=1e-14,
        metric_name="endpoint_position_error",
    )
    rms_fit = build_fit_summary(
        metrics=metrics,
        metric_key="rms_phase_space_error",
        epsilon=1e-16,
        metric_name="rms_phase_space_error",
    )

    plot_figure1_trajectories(datasets)
    plot_figure2_phase_space(datasets)
    plot_figure3_small_vs_large(datasets, m_idx)
    plot_figure4_convergence_combined(metrics, endpoint_fit, rms_fit)
    plot_figure5_energy_diagnostic(datasets, m_idx)

    sanity_warnings = run_sanity_checks(endpoint_fit, rms_fit, m_idx)
    generate_table_outputs(metrics, endpoint_fit, rms_fit, sanity_warnings)

    if sanity_warnings:
        print("=== SANITY CHECK WARNINGS ===")
        for warning in sanity_warnings:
            print(f"WARNING: {warning}")
    else:
        print("All numerical sanity checks passed.")


if __name__ == "__main__":
    main()
