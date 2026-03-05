#!/usr/bin/env python3
"""
plot_lj.py — Generate Lennard-Jones / Argon validation plots (Results 2).

Produces:
  - out/plots/lj_energy_brief.png
  - out/plots/lj_energy_extended.png
  - out/plots/lj_temperature_brief.png
  - out/plots/lj_temperature_extended.png
  - out/plots/lj_rdf.png
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from plot_style import (
    COLOR_ACCENT,
    COLOR_EULER,
    COLOR_REFERENCE,
    COLOR_VERLET,
    INTEGRATOR_STYLE,
    apply_major_grid,
    apply_plot_style,
    disable_offset_text,
    save_figure,
)

OUT_DIR = "out"
PLOT_DIR = "out/plots"

EPSILON_OVER_KB = 120.0
KB = 1.380649e-23
EPSILON = KB * EPSILON_OVER_KB
SIGMA_ANGSTROM = 3.4
TEMP_DIVERGENCE_K = 1.0e4

RAHMAN_R_A = np.array([3.0, 3.7, 5.2, 7.0, 8.5, 10.4], dtype=float)
RAHMAN_G = np.array([0.00, 2.85, 0.65, 1.25, 0.90, 1.05], dtype=float)


def load_manifest():
    manifest_path = f"{OUT_DIR}/manifest.json"
    if not os.path.exists(manifest_path):
        print(f"Warning: manifest not found at {manifest_path}")
        return {}
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        print(f"Warning: failed to parse manifest JSON: {exc}")
        return {}


def nested_get(obj, dotted, default=""):
    cur = obj
    for key in dotted.split("."):
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def load_csv(filepath):
    """Load CSV with headers, skipping comment lines."""

    def filter_comments(handle):
        for line in handle:
            if line.strip() and not line.startswith("#"):
                yield line

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = list(filter_comments(f))
    if not lines:
        return None
    data = np.genfromtxt(lines, delimiter=",", names=True)
    if data is None:
        return None
    if getattr(data, "shape", ()) == ():
        data = np.array([data], dtype=data.dtype)
    return data


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


def parse_float_meta(meta, key, default):
    if key not in meta:
        return default
    try:
        return float(meta[key])
    except ValueError:
        return default


def get_meta_value(meta, preferred_key, fallback_key, default):
    if preferred_key in meta:
        return parse_int_meta(meta, preferred_key, default)
    if fallback_key in meta:
        return parse_int_meta(meta, fallback_key, default)
    return default


def finite_or_nan(arr):
    arr = np.asarray(arr, dtype=float)
    return np.where(np.isfinite(arr), arr, np.nan)


def cubic_spline_interpolate(x, y, n_points=300):
    """Natural cubic spline interpolation without external dependencies."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    if n < 3:
        x_dense = np.linspace(x[0], x[-1], n_points)
        y_dense = np.interp(x_dense, x, y)
        return x_dense, y_dense

    h = np.diff(x)
    if np.any(h <= 0):
        x_dense = np.linspace(np.min(x), np.max(x), n_points)
        y_dense = np.interp(x_dense, x, y)
        return x_dense, y_dense

    alpha = np.zeros(n, dtype=float)
    for i in range(1, n - 1):
        alpha[i] = (3.0 / h[i]) * (y[i + 1] - y[i]) - (3.0 / h[i - 1]) * (y[i] - y[i - 1])

    l = np.ones(n, dtype=float)
    mu = np.zeros(n, dtype=float)
    z = np.zeros(n, dtype=float)

    for i in range(1, n - 1):
        l[i] = 2.0 * (x[i + 1] - x[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]

    c = np.zeros(n, dtype=float)
    b = np.zeros(n - 1, dtype=float)
    d = np.zeros(n - 1, dtype=float)

    for j in range(n - 2, -1, -1):
        c[j] = z[j] - mu[j] * c[j + 1]
        b[j] = (y[j + 1] - y[j]) / h[j] - (h[j] * (c[j + 1] + 2.0 * c[j])) / 3.0
        d[j] = (c[j + 1] - c[j]) / (3.0 * h[j])

    x_dense = np.linspace(x[0], x[-1], n_points)
    seg = np.searchsorted(x, x_dense, side="right") - 1
    seg = np.clip(seg, 0, n - 2)
    dx = x_dense - x[seg]
    y_dense = y[seg] + b[seg] * dx + c[seg] * dx * dx + d[seg] * dx * dx * dx
    return x_dense, y_dense


def first_nonfinite_index(*arrays):
    if not arrays:
        return None
    invalid = np.zeros(len(arrays[0]), dtype=bool)
    for arr in arrays:
        invalid |= ~np.isfinite(arr)
    idx = np.where(invalid)[0]
    return int(idx[0]) if idx.size > 0 else None


def first_exceed_index(arr, threshold):
    idx = np.where(np.abs(arr) > threshold)[0]
    return int(idx[0]) if idx.size > 0 else None


def first_finite_prod_index(steps, etot, production_start):
    for i in range(len(steps)):
        if steps[i] >= production_start and np.isfinite(etot[i]):
            return i
    for i in range(len(steps)):
        if np.isfinite(etot[i]):
            return i
    return None


def load_series(filepath):
    data = load_csv(filepath)
    if data is None or len(data) == 0:
        return None
    names = set(data.dtype.names or [])
    required = {"time", "E_kin", "E_pot", "E_total", "temperature"}
    if not required.issubset(names):
        print(f"Warning: missing required columns in {filepath}; skipping")
        return None

    meta = parse_csv_metadata(filepath)
    steps = np.asarray(data["step"], dtype=float) if "step" in names else np.arange(len(data), dtype=float)
    time_ps = np.asarray(data["time"], dtype=float) * 1e12

    ekin_raw = np.asarray(data["E_kin"], dtype=float) / EPSILON
    epot_raw = np.asarray(data["E_pot"], dtype=float) / EPSILON
    etot_raw = np.asarray(data["E_total"], dtype=float) / EPSILON
    temp_raw = np.asarray(data["temperature"], dtype=float)

    divergence_idx_nonfinite = first_nonfinite_index(ekin_raw, epot_raw, etot_raw, temp_raw)
    divergence_idx_temp = first_exceed_index(temp_raw, TEMP_DIVERGENCE_K)

    divergence_candidates = [idx for idx in [divergence_idx_nonfinite, divergence_idx_temp] if idx is not None]
    divergence_idx = min(divergence_candidates) if divergence_candidates else None
    divergence_reason = None
    if divergence_idx is not None:
        if divergence_idx_nonfinite is not None and divergence_idx == divergence_idx_nonfinite:
            divergence_reason = "non-finite values"
        else:
            divergence_reason = f"|T| > {TEMP_DIVERGENCE_K:.0e} K"

    # Equivalent to DataFrame.replace([np.inf, -np.inf], np.nan) without pandas.
    ekin = finite_or_nan(ekin_raw)
    epot = finite_or_nan(epot_raw)
    etot = finite_or_nan(etot_raw)
    temp = finite_or_nan(temp_raw)

    # If divergence starts, keep only the finite prefix for plotting clarity.
    if divergence_idx is not None:
        ekin[divergence_idx:] = np.nan
        epot[divergence_idx:] = np.nan
        etot[divergence_idx:] = np.nan
        temp[divergence_idx:] = np.nan

    divergence_step = int(steps[divergence_idx]) if divergence_idx is not None else None
    divergence_time_ps = float(time_ps[divergence_idx]) if divergence_idx is not None else None

    return {
        "meta": meta,
        "steps": steps,
        "time_ps": finite_or_nan(time_ps),
        "ekin_eps": ekin,
        "epot_eps": epot,
        "etot_eps": etot,
        "temperature": temp,
        "has_nonfinite": divergence_idx is not None,
        "divergence_step": divergence_step,
        "divergence_time_ps": divergence_time_ps,
        "divergence_reason": divergence_reason,
    }


def plot_energy_for_run(manifest, run_key, config, out_name):
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), sharex="col", constrained_layout=True)
    any_data = False

    for row, integrator in enumerate(config["integrators"]):
        series_key = integrator["series_key"]
        label = integrator["label"]
        style = INTEGRATOR_STYLE[integrator["style_key"]]
        color = style["color"]
        linestyle = style["linestyle"]
        linewidth = style["linewidth"]

        fpath = nested_get(manifest, f"{run_key}.{series_key}")
        if not fpath or not os.path.exists(fpath):
            print(f"Warning: missing {run_key}.{series_key}; skipping")
            continue

        series = load_series(fpath)
        if series is None:
            continue
        any_data = True

        steps = series["steps"]
        t = series["time_ps"]
        ekin = series["ekin_eps"]
        epot = series["epot_eps"]
        etot = series["etot_eps"]
        meta = series["meta"]

        production_start = parse_int_meta(meta, "production_start", 0)
        ref_idx = first_finite_prod_index(steps, etot, production_start)
        if ref_idx is None:
            rel_dev = np.full_like(etot, np.nan)
            ref_text = "no finite reference"
        else:
            e0 = etot[ref_idx]
            if np.isfinite(e0) and abs(e0) > 1e-30:
                rel_dev = (etot - e0) / abs(e0)
            else:
                rel_dev = etot - e0
            # Drift is meaningful only in production (post-rescaling) window.
            rel_dev = np.where(steps >= production_start, rel_dev, np.nan)
            ref_text = f"E0 at step {int(steps[ref_idx])}"

        label_plot = label
        if series["has_nonfinite"]:
            label_plot = f"{label} (divergent tail omitted)"

        ax_e = axes[row, 0]
        ax_e.plot(t, ekin, label=r"$E_{kin}$", color=COLOR_ACCENT, linewidth=1.6)
        ax_e.plot(t, epot, label=r"$E_{pot}$", color=COLOR_VERLET, linewidth=1.6)
        ax_e.plot(t, etot, label=r"$E_{total}$", color="k", linewidth=2.0)
        ax_e.set_ylabel(r"Energy [$\varepsilon$]")
        ax_e.set_title(f"{label_plot}: Energy vs Time")
        apply_major_grid(ax_e)
        disable_offset_text(ax_e)
        ax_e.legend(loc="best")

        ax_d = axes[row, 1]
        ax_d.plot(t, rel_dev, color=color, linestyle=linestyle, linewidth=linewidth)
        ax_d.axhline(y=0.0, color=COLOR_REFERENCE, linestyle="--", linewidth=1.0, alpha=0.7)
        ax_d.set_ylabel(r"$\Delta E / |E_{0,\mathrm{prod}}|$")
        ax_d.set_title(f"{label_plot}: Relative Energy Deviation in Production ({ref_text})")
        apply_major_grid(ax_d)
        disable_offset_text(ax_d)

        divergence_step = series.get("divergence_step")
        divergence_time_ps = series.get("divergence_time_ps")
        divergence_reason = series.get("divergence_reason")
        if divergence_step is not None and "Euler" in label and divergence_time_ps is not None:
            ax_e.axvline(divergence_time_ps, color=color, linestyle="--", linewidth=1.2, alpha=0.8)
            ax_d.axvline(divergence_time_ps, color=color, linestyle="--", linewidth=1.2, alpha=0.8)
            note = f"Euler diverged at step {divergence_step}"
            if divergence_reason:
                note += f" ({divergence_reason})"
            ax_e.text(
                0.02,
                0.93,
                note,
                transform=ax_e.transAxes,
                fontsize=8,
                bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"},
            )
            ax_d.text(
                0.02,
                0.93,
                note,
                transform=ax_d.transAxes,
                fontsize=8,
                bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"},
            )

    if not any_data:
        plt.close(fig)
        print(f"Warning: no usable data for {run_key}; skipped {out_name}")
        return

    axes[1, 0].set_xlabel("Time [ps]")
    axes[1, 1].set_xlabel("Time [ps]")
    fig.suptitle(config["energy_title"], fontsize=13)

    out_path = f"{PLOT_DIR}/{out_name}"
    save_figure(fig, out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


def plot_temperature_for_run(manifest, run_key, config, out_name):
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
    any_data = False
    drew_prod_line = False
    plotted_series = []

    for integrator in config["integrators"]:
        series_key = integrator["series_key"]
        label = integrator["label"]
        style = INTEGRATOR_STYLE[integrator["style_key"]]
        color = style["color"]
        linestyle = style["linestyle"]
        linewidth = style["linewidth"]

        fpath = nested_get(manifest, f"{run_key}.{series_key}")
        if not fpath or not os.path.exists(fpath):
            continue
        series = load_series(fpath)
        if series is None:
            continue

        any_data = True
        t = series["time_ps"]
        temp = series["temperature"]
        meta = series["meta"]
        label_plot = label
        if series["has_nonfinite"]:
            label_plot = f"{label} (divergent tail omitted)"

        ax.plot(t, temp, label=label_plot, color=color, linestyle=linestyle, linewidth=linewidth)
        plotted_series.append((t, temp, color, linestyle, linewidth))

        divergence_step = series.get("divergence_step")
        divergence_time_ps = series.get("divergence_time_ps")
        divergence_reason = series.get("divergence_reason")
        if divergence_step is not None and "Euler" in label and divergence_time_ps is not None:
            ax.axvline(divergence_time_ps, color=color, linestyle="--", linewidth=1.2, alpha=0.8)
            note = f"Euler diverged at step {divergence_step}"
            if divergence_reason:
                note += f" ({divergence_reason})"
            ax.text(
                0.02,
                0.92,
                note,
                transform=ax.transAxes,
                fontsize=8,
                bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"},
            )

        production_start = parse_int_meta(meta, "production_start", 0)
        dt = parse_float_meta(meta, "dt", float("nan"))
        if production_start >= 0 and np.isfinite(dt) and not drew_prod_line:
            ax.axvline(
                x=production_start * dt * 1e12,
                color="gray",
                linestyle=":",
                linewidth=1.5,
                alpha=0.8,
                label=f"production start (step {production_start})",
            )
            drew_prod_line = True

    if not any_data:
        plt.close(fig)
        print(f"Warning: no usable data for {run_key}; skipped {out_name}")
        return

    ax.axhline(y=94.4, color="k", linestyle="--", alpha=0.6, label="T = 94.4 K")
    ax.set_xlabel("Time [ps]")
    ax.set_ylabel("Temperature [K]")
    ax.set_title(config["temperature_title"])
    apply_major_grid(ax)
    disable_offset_text(ax)
    ax.legend(loc="best")

    zoom_cfg = config.get("zoom_inset")
    if zoom_cfg and plotted_series:
        axins = inset_axes(
            ax,
            width=zoom_cfg.get("width", "42%"),
            height=zoom_cfg.get("height", "46%"),
            loc=zoom_cfg.get("loc", "upper left"),
            borderpad=1.2,
        )
        for t, temp, color, linestyle, linewidth in plotted_series:
            axins.plot(t, temp, color=color, linestyle=linestyle, linewidth=linewidth)
        axins.axhline(y=94.4, color="k", linestyle="--", alpha=0.6, linewidth=1.0)
        if "xlim" in zoom_cfg:
            axins.set_xlim(*zoom_cfg["xlim"])
        if "ylim" in zoom_cfg:
            axins.set_ylim(*zoom_cfg["ylim"])
        axins.set_title(zoom_cfg.get("title", "Zoom"), fontsize=9)
        apply_major_grid(axins)
        disable_offset_text(axins)
        axins.tick_params(axis="both", which="major", labelsize=8)

    out_path = f"{PLOT_DIR}/{out_name}"
    save_figure(fig, out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


def plot_rdf(manifest):
    os.makedirs(PLOT_DIR, exist_ok=True)

    gr_path = nested_get(manifest, "lj_rdf.verlet_long")
    if not gr_path or not os.path.exists(gr_path):
        print("No RDF data found at manifest key lj_rdf.verlet_long. Skipping RDF plot.")
        return

    data = load_csv(gr_path)
    if data is None or len(data) == 0:
        print("RDF CSV is empty. Skipping RDF plot.")
        return

    names = set(data.dtype.names or [])
    if "r_sigma" not in names or "gr" not in names:
        print("RDF CSV missing r_sigma/gr columns. Skipping RDF plot.")
        return

    r_a = finite_or_nan(np.asarray(data["r_sigma"], dtype=float) * SIGMA_ANGSTROM)
    gr = finite_or_nan(np.asarray(data["gr"], dtype=float))
    rahman_r_smooth, rahman_g_smooth = cubic_spline_interpolate(RAHMAN_R_A, RAHMAN_G, n_points=300)
    rahman_g_smooth = np.clip(rahman_g_smooth, 0.0, None)
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    ax.plot(
        rahman_r_smooth,
        rahman_g_smooth,
        color=COLOR_EULER,
        linestyle="--",
        linewidth=1.8,
        alpha=0.9,
        zorder=1,
    )
    ax.scatter(RAHMAN_R_A, RAHMAN_G, color=COLOR_EULER, s=22, zorder=2, label="Rahman (1964) Fig. 2")
    ax.plot(r_a, gr, color="k", linewidth=2.0, zorder=3, label="Present Work (Verlet, NVE)")
    ax.axhline(y=1.0, color=COLOR_REFERENCE, linestyle="--", linewidth=1.2)

    title = "RDF: Present Work vs Rahman (1964)"

    ax.set_title(title)
    ax.set_xlabel("Distance r (Å)")
    ax.set_ylabel("g(r)")
    xmax = np.nanmax(np.concatenate([r_a[np.isfinite(r_a)], RAHMAN_R_A])) if np.any(np.isfinite(r_a)) else np.max(RAHMAN_R_A)
    ax.set_xlim(0.0, max(11.0, 1.05 * float(xmax)))
    ax.set_ylim(bottom=0.0)
    apply_major_grid(ax)
    disable_offset_text(ax)
    ax.legend(loc="best")

    out_path = f"{PLOT_DIR}/lj_rdf.png"
    save_figure(fig, out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


def safe_plot(name, fn, *args):
    try:
        fn(*args)
    except Exception as exc:
        print(f"Warning: {name} failed: {exc}")


def main():
    apply_plot_style()
    manifest = load_manifest()

    brief_cfg = {
        "integrators": [
            {"series_key": "verlet", "label": "Velocity-Verlet", "style_key": "verlet"},
            {"series_key": "euler", "label": "Forward Euler", "style_key": "euler"},
        ],
        "energy_title": "Brief (required): Energy vs Time",
        "temperature_title": "Brief (required): Temperature vs Time",
    }
    extended_cfg = {
        "integrators": [
            {"series_key": "verlet_600", "label": "Velocity-Verlet", "style_key": "verlet"},
            {"series_key": "euler_600", "label": "Forward Euler", "style_key": "euler"},
        ],
        "energy_title": "Extended (optional): Energy vs Time",
        "temperature_title": "Extended (optional): Temperature vs Time",
        "zoom_inset": {"xlim": (0.0, 6.0), "ylim": (70.0, 110.0), "title": "Zoom: 70-110 K"},
    }

    safe_plot("brief energy", plot_energy_for_run, manifest, "lj_brief", brief_cfg, "lj_energy_brief.png")
    safe_plot(
        "brief temperature",
        plot_temperature_for_run,
        manifest,
        "lj_brief",
        brief_cfg,
        "lj_temperature_brief.png",
    )

    safe_plot(
        "extended energy",
        plot_energy_for_run,
        manifest,
        "lj_extended",
        extended_cfg,
        "lj_energy_extended.png",
    )
    safe_plot(
        "extended temperature",
        plot_temperature_for_run,
        manifest,
        "lj_extended",
        extended_cfg,
        "lj_temperature_extended.png",
    )

    safe_plot("rdf", plot_rdf, manifest)


if __name__ == "__main__":
    main()
