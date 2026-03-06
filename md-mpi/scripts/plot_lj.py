#!/usr/bin/env python3
"""
plot_lj.py — Generate Lennard-Jones / Argon validation plots (Results 2).

Produces:
  - out/plots/results2_lj_brief_energy_100step_production.png
  - out/plots/results2_lj_extended_energy_stability.png
  - out/plots/results2_lj_brief_temperature_100step_production.png
  - out/plots/results2_lj_extended_temperature_stability.png
  - out/plots/results2_lj_rdf_comparison_rahman1964.png
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


def divergence_crop_limit(div_time_ps, max_time_ps):
    if div_time_ps is None or not np.isfinite(div_time_ps):
        return None
    pad = max(0.15, 0.1 * div_time_ps)
    return float(min(max_time_ps, div_time_ps + pad))


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
    euler_divergence_time_ps = None
    max_time_ps = 0.0

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
        if np.any(np.isfinite(t)):
            max_time_ps = max(max_time_ps, float(np.nanmax(t)))
        ekin = series["ekin_eps"]
        epot = series["epot_eps"]
        etot = series["etot_eps"]
        meta = series["meta"]

        ref_idx = first_finite_prod_index(steps, etot, 0)
        if ref_idx is None:
            rel_dev = np.full_like(etot, np.nan)
        else:
            e0 = etot[ref_idx]
            if np.isfinite(e0) and abs(e0) > 1e-30:
                rel_dev = (etot - e0) / abs(e0)
            else:
                rel_dev = etot - e0

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
        ax_d.set_ylabel("Relative Energy Deviation")
        ax_d.set_title(f"{label_plot}: Relative Energy Deviation")
        apply_major_grid(ax_d)
        disable_offset_text(ax_d)

        divergence_step = series.get("divergence_step")
        divergence_time_ps = series.get("divergence_time_ps")
        divergence_reason = series.get("divergence_reason")
        if divergence_step is not None and "Euler" in label and divergence_time_ps is not None:
            if euler_divergence_time_ps is None or divergence_time_ps < euler_divergence_time_ps:
                euler_divergence_time_ps = divergence_time_ps
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

    if config.get("crop_to_euler_divergence", False):
        x_max = divergence_crop_limit(euler_divergence_time_ps, max_time_ps)
        if x_max is not None:
            for row in range(2):
                for col in range(2):
                    axes[row, col].set_xlim(0.0, x_max)

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
    euler_divergence_time_ps = None
    max_time_ps = 0.0
    target_temp_k = config.get("target_temperature_k")

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
        if np.any(np.isfinite(t)):
            max_time_ps = max(max_time_ps, float(np.nanmax(t)))
        temp = series["temperature"]
        meta = series["meta"]
        label_plot = label
        if series["has_nonfinite"]:
            label_plot = f"{label} (divergent tail omitted)"

        ax.plot(t, temp, label=label_plot, color=color, linestyle=linestyle, linewidth=linewidth)
        plotted_series.append(
            {
                "t": t,
                "temp": temp,
                "color": color,
                "linestyle": linestyle,
                "linewidth": linewidth,
                "style_key": integrator.get("style_key", ""),
            }
        )

        divergence_step = series.get("divergence_step")
        divergence_time_ps = series.get("divergence_time_ps")
        divergence_reason = series.get("divergence_reason")
        if divergence_step is not None and "Euler" in label and divergence_time_ps is not None:
            if euler_divergence_time_ps is None or divergence_time_ps < euler_divergence_time_ps:
                euler_divergence_time_ps = divergence_time_ps
            ax.axvline(divergence_time_ps, color=color, linestyle="--", linewidth=1.2, alpha=0.8)
            note = f"Euler diverged at step {divergence_step}"
            if divergence_reason:
                note += f" ({divergence_reason})"
            ax.text(
                0.58,
                0.92,
                note,
                transform=ax.transAxes,
                fontsize=8,
                bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"},
            )

        production_start = get_meta_value(meta, "production_start_step", "production_start", 0)
        dt = parse_float_meta(meta, "dt", float("nan"))
        if target_temp_k is None:
            target_temp_candidate = parse_float_meta(meta, "target_temperature", float("nan"))
            if np.isfinite(target_temp_candidate):
                target_temp_k = float(target_temp_candidate)
        if production_start > 0 and np.isfinite(dt) and not drew_prod_line:
            ax.axvline(
                x=production_start * dt * 1e12,
                color="gray",
                linestyle=":",
                linewidth=1.5,
                alpha=0.8,
                label="production starts",
            )
            drew_prod_line = True

    if not any_data:
        plt.close(fig)
        print(f"Warning: no usable data for {run_key}; skipped {out_name}")
        return

    ax.set_xlabel("Time [ps]")
    ax.set_ylabel("Temperature [K]")
    ax.set_title(config["temperature_title"])
    apply_major_grid(ax)
    disable_offset_text(ax)
    if target_temp_k is None:
        target_temp_k = 94.4
    if np.isfinite(target_temp_k):
        ax.axhline(
            y=target_temp_k,
            color="#7a7a7a",
            linestyle="--",
            linewidth=1.4,
            alpha=0.55,
            zorder=0,
            label=f"Target T = {target_temp_k:.1f} K",
        )

    ax.legend(loc=config.get("legend_loc", "best"))

    zoom_cfg = config.get("zoom_inset")
    if zoom_cfg and plotted_series:
        inset_kwargs = {
            "width": zoom_cfg.get("width", "30%"),
            "height": zoom_cfg.get("height", "34%"),
            "loc": zoom_cfg.get("loc", "lower right"),
            "borderpad": zoom_cfg.get("borderpad", 0.8),
        }
        if "bbox_to_anchor" in zoom_cfg:
            inset_kwargs["bbox_to_anchor"] = zoom_cfg["bbox_to_anchor"]
            inset_kwargs["bbox_transform"] = ax.transAxes

        axins = inset_axes(ax, **inset_kwargs)
        for series_plot in plotted_series:
            plot_kwargs = {
                "color": series_plot["color"],
                "linestyle": series_plot["linestyle"],
                "linewidth": max(1.2, 0.9 * series_plot["linewidth"]),
            }
            # Show discrete samples for Verlet in the inset so short-time variation
            # reads less like an over-smoothed curve.
            if series_plot["style_key"] == "verlet":
                plot_kwargs.update(
                    {
                        "linewidth": 1.0,
                        "marker": "o",
                        "markersize": 2.0,
                        "markevery": 1,
                        "markeredgewidth": 0.0,
                        "antialiased": False,
                    }
                )
            axins.plot(series_plot["t"], series_plot["temp"], **plot_kwargs)
        if "xlim" in zoom_cfg:
            axins.set_xlim(*zoom_cfg["xlim"])
        if "ylim" in zoom_cfg:
            axins.set_ylim(*zoom_cfg["ylim"])
        if np.isfinite(target_temp_k):
            axins.axhline(
                y=target_temp_k,
                color="#7a7a7a",
                linestyle="--",
                linewidth=1.0,
                alpha=0.5,
                zorder=0,
            )
        axins.set_title(zoom_cfg.get("title", "Zoom"), fontsize=9, pad=4)
        axins.patch.set_facecolor(zoom_cfg.get("facecolor", "white"))
        axins.patch.set_alpha(zoom_cfg.get("alpha", 0.96))
        spine_color = zoom_cfg.get("spine_color", "#333333")
        spine_width = zoom_cfg.get("spine_width", 1.0)
        for spine in axins.spines.values():
            spine.set_color(spine_color)
            spine.set_linewidth(spine_width)
        apply_major_grid(axins)
        disable_offset_text(axins)
        axins.tick_params(axis="both", which="major", labelsize=8)

    if config.get("crop_to_euler_divergence", False):
        x_max = divergence_crop_limit(euler_divergence_time_ps, max_time_ps)
        if x_max is not None:
            ax.set_xlim(0.0, x_max)

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

    r_sigma = finite_or_nan(np.asarray(data["r_sigma"], dtype=float))
    gr = finite_or_nan(np.asarray(data["gr"], dtype=float))
    rahman_r_sigma = RAHMAN_R_A / SIGMA_ANGSTROM
    rahman_r_smooth, rahman_g_smooth = cubic_spline_interpolate(rahman_r_sigma, RAHMAN_G, n_points=300)
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
    ax.scatter(rahman_r_sigma, RAHMAN_G, color=COLOR_EULER, s=22, zorder=2, label="Rahman (1964) Fig. 2")
    ax.plot(r_sigma, gr, color="k", linewidth=2.0, zorder=3, label="Present Work (Verlet, NVE)")
    ax.axhline(y=1.0, color=COLOR_REFERENCE, linestyle="--", linewidth=1.2)

    title = "RDF: Present Work vs Rahman (1964)"

    ax.set_title(title)
    ax.set_xlabel(r"Distance $r/\sigma$")
    ax.set_ylabel("g(r)")
    xmax = np.nanmax(np.concatenate([r_sigma[np.isfinite(r_sigma)], rahman_r_sigma])) if np.any(np.isfinite(r_sigma)) else np.max(rahman_r_sigma)
    ax.set_xlim(0.0, max(3.3, 1.05 * float(xmax)))
    ax.set_ylim(bottom=0.0)
    secax = ax.secondary_xaxis(
        "top",
        functions=(lambda x: x * SIGMA_ANGSTROM, lambda x: x / SIGMA_ANGSTROM),
    )
    secax.set_xlabel("Distance r (Å)")
    apply_major_grid(ax)
    disable_offset_text(ax)
    ax.legend(loc="best")

    out_path = f"{PLOT_DIR}/results2_lj_rdf_comparison_rahman1964.png"
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
        "temperature_title": "Argon LJ (required run): Temperature vs Time (100-step NVE production)",
        "production_only_note": False,
    }
    extended_cfg = {
        "integrators": [
            {"series_key": "verlet_600", "label": "Velocity-Verlet", "style_key": "verlet"},
            {"series_key": "euler_600", "label": "Forward Euler", "style_key": "euler"},
        ],
        "energy_title": "Argon LJ (extended optional): Energy vs Time",
        "temperature_title": "Argon LJ (extended optional): Temperature vs Time",
        "crop_to_euler_divergence": True,
        "production_only_note": False,
        "legend_loc": "upper left",
        "zoom_inset": {
            "xlim": (0.0, 1.15),
            "ylim": (75.0, 130.0),
            "title": "Zoom near start (75-130 K)",
            "width": "36%",
            "height": "38%",
            "loc": "center left",
            "bbox_to_anchor": (0.06, 0.0, 1.0, 1.0),
            "borderpad": 1.0,
            "facecolor": "#fcfcfc",
            "alpha": 0.97,
            "spine_color": "#2f2f2f",
            "spine_width": 1.0,
        },
    }

    safe_plot(
        "brief energy",
        plot_energy_for_run,
        manifest,
        "lj_brief",
        brief_cfg,
        "results2_lj_brief_energy_100step_production.png",
    )
    safe_plot(
        "brief temperature",
        plot_temperature_for_run,
        manifest,
        "lj_brief",
        brief_cfg,
        "results2_lj_brief_temperature_100step_production.png",
    )

    safe_plot(
        "extended energy",
        plot_energy_for_run,
        manifest,
        "lj_extended",
        extended_cfg,
        "results2_lj_extended_energy_stability.png",
    )
    safe_plot(
        "extended temperature",
        plot_temperature_for_run,
        manifest,
        "lj_extended",
        extended_cfg,
        "results2_lj_extended_temperature_stability.png",
    )

    safe_plot("rdf", plot_rdf, manifest)


if __name__ == "__main__":
    main()
