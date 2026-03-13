#!/usr/bin/env python3
"""
plot_lj.py - Generate Lennard-Jones / Argon validation plots (Results 2).

Produces:
  - out/plots/results2_figure6.png
  - out/plots/results2_figure7.png
  - out/plots/results2_figure8.png
"""

import csv
import json
import os
import glob

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from plot_style import (
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
RAHMAN_SOURCE_FILE = "scripts/data/rahman1964_fig2_manual_anchors.csv"
STALE_RESULTS2_PATTERNS = [
    # Removed extended-results2 outputs:
    f"{PLOT_DIR}/results2_lj_extended_*.png",
    # Legacy pre-results2 naming:
    f"{PLOT_DIR}/lj_*.png",
]

EPSILON_OVER_KB = 120.0
KB = 1.380649e-23
EPSILON = KB * EPSILON_OVER_KB
SIGMA_ANGSTROM = 3.4
TEMP_DIVERGENCE_K = 1.0e4

FIG6_ENERGY_PNG = "results2_figure6.png"
FIG7_TEMPERATURE_PNG = "results2_figure7.png"
FIG8_RDF_PNG = "results2_figure8.png"


def unique_preserve_order(items):
    out = []
    seen = set()
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def parse_scalar(raw):
    if isinstance(raw, (int, float, bool)):
        return raw
    s = str(raw).strip()
    lower = s.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    try:
        if any(c in s for c in [".", "e", "E"]):
            return float(s)
        return int(s)
    except ValueError:
        return s


def typed_meta(meta):
    return {k: parse_scalar(v) for k, v in meta.items()}


def run_identifier_from_path(path):
    if not path:
        return ""
    parent = os.path.basename(os.path.dirname(path))
    return parent or ""


def extract_series_parameters(meta_typed):
    keys = [
        "mode",
        "integrator",
        "N",
        "P",
        "dt",
        "target_temperature",
        "equilibration_steps",
        "production_steps",
        "production_start_step",
        "n_steps",
        "n_frames",
        "total_steps_executed",
        "L",
        "rcut",
        "production_nve",
        "final_rescale_before_production",
        "final_rescale_applied",
        "startup_temperature_before_final_rescale",
        "startup_temperature_after_final_rescale",
        "gr_discard_steps",
        "gr_sample_every",
        "gr_start",
        "timestamp",
    ]
    out = {}
    for key in keys:
        if key in meta_typed:
            out[key] = meta_typed[key]
    return out


def write_plot_metadata(plot_png_name, section, extra):
    return


def add_panel_label(ax, label: str, x: float = -0.1, y: float = 1.05):
    ax.text(
        x,
        y,
        f"{label})",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=11,
        fontweight="bold",
        color="black",
    )


def load_rahman_anchor_points(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Rahman anchor dataset not found: {path}")

    points = []
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "point_id",
            "r_angstrom",
            "r_over_sigma",
            "g_value",
            "point_type",
            "source_note",
            "uncertainty_note",
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Rahman anchor dataset missing columns: {sorted(missing)}")

        for row in reader:
            if not row:
                continue
            point = {
                "point_id": int(row["point_id"]),
                "r_angstrom": float(row["r_angstrom"]),
                "r_over_sigma": float(row["r_over_sigma"]),
                "g_value": float(row["g_value"]),
                "point_type": row["point_type"].strip(),
                "source_note": row["source_note"].strip(),
                "uncertainty_note": row["uncertainty_note"].strip(),
            }
            points.append(point)

    points.sort(key=lambda item: item["point_id"])
    if not points:
        raise ValueError("Rahman anchor dataset is empty")
    return points


def remove_old_results2_files():
    for pattern in STALE_RESULTS2_PATTERNS:
        for path in glob.glob(pattern):
            os.remove(path)
            print(f"Removed old file {path}")


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
    meta_typed = typed_meta(meta)
    production_start = get_meta_value(meta, "production_start_step", "production_start", 0)
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
        "meta_typed": meta_typed,
        "filepath": filepath,
        "run_identifier": run_identifier_from_path(filepath),
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
        "production_start_step": production_start,
    }


def plot_energy_for_run(manifest, run_key, config, out_name):
    os.makedirs(PLOT_DIR, exist_ok=True)
    fig, axes = plt.subplots(
        2,
        1,
        figsize=(9.4, 7.2),
        sharex=True,
        constrained_layout=True,
    )
    any_data = False
    euler_divergence_time_ps = None
    max_time_ps = 0.0
    x_max = None
    source_data_files = []
    source_manifest_keys = []
    simulation_run_identifiers = []
    per_integrator_summary = []
    series_parameters = {}
    missing_provenance = []

    for row, integrator in enumerate(config["integrators"]):
        series_key = integrator["series_key"]
        label = integrator["label"]
        style_key = integrator["style_key"]
        manifest_key = f"{run_key}.{series_key}"
        style = INTEGRATOR_STYLE[integrator["style_key"]]
        color = style["color"]
        linestyle = style["linestyle"]
        linewidth = style["linewidth"]

        fpath = nested_get(manifest, manifest_key)
        if not fpath or not os.path.exists(fpath):
            print(f"Warning: missing {manifest_key}; skipping")
            missing_provenance.append(f"manifest/data file missing for {manifest_key}")
            continue

        series = load_series(fpath)
        if series is None:
            missing_provenance.append(f"series unreadable or missing required columns for {manifest_key}")
            continue
        any_data = True

        steps = series["steps"]
        t = series["time_ps"]
        if np.any(np.isfinite(t)):
            max_time_ps = max(max_time_ps, float(np.nanmax(t)))
        etot = series["etot_eps"]
        meta_typed = series["meta_typed"]
        source_data_files.append(fpath)
        source_manifest_keys.append(manifest_key)
        simulation_run_identifiers.append(series["run_identifier"])
        series_parameters[style_key] = extract_series_parameters(meta_typed)

        production_start = series["production_start_step"]
        ref_idx = first_finite_prod_index(steps, etot, production_start)
        if ref_idx is None:
            rel_dev_pct = np.full_like(etot, np.nan)
            rel_dev_ref_step = None
            e0 = np.nan
        else:
            e0 = etot[ref_idx]
            if np.isfinite(e0) and abs(e0) > 1e-30:
                rel_dev_pct = 100.0 * (etot - e0) / abs(e0)
            else:
                rel_dev_pct = np.full_like(etot, np.nan)
            rel_dev_ref_step = int(steps[ref_idx])

        finite_etot = etot[np.isfinite(etot)]
        ax_d = axes[row]
        row_label = label
        ax_d.plot(t, rel_dev_pct, color=color, linestyle=linestyle, linewidth=max(2.2, linewidth), label=row_label)
        ax_d.set_ylabel(r"$\Delta E / E_0$ [%]")
        ax_d.axhline(0.0, color=COLOR_REFERENCE, linestyle="--", linewidth=1.0, alpha=0.6)
        apply_major_grid(ax_d)
        disable_offset_text(ax_d)

        add_panel_label(ax_d, chr(ord("a") + row))
        ax_d.legend(
            loc="upper left",
            bbox_to_anchor=(0.02, 0.95),
            fontsize=9,
            frameon=True,
            facecolor="white",
            edgecolor="none",
            framealpha=0.86,
        )


        divergence_step = series.get("divergence_step")
        divergence_time_ps = series.get("divergence_time_ps")
        divergence_reason = series.get("divergence_reason")
        finite_rel_pct = rel_dev_pct[np.isfinite(rel_dev_pct)]
        max_abs_rel_pct = float(np.nanmax(np.abs(finite_rel_pct))) if finite_rel_pct.size else None
        mean_abs_rel_pct = float(np.nanmean(np.abs(finite_rel_pct))) if finite_rel_pct.size else None
        final_rel_pct = float(finite_rel_pct[-1]) if finite_rel_pct.size else None
        per_integrator_summary.append(
            {
                "integrator": style_key,
                "label": label,
                "manifest_key": manifest_key,
                "source_file": fpath,
                "run_identifier": series["run_identifier"],
                "points_plotted": int(np.count_nonzero(np.isfinite(etot))),
                "reference_step_for_relative_deviation": rel_dev_ref_step,
                "max_abs_relative_energy_deviation_percent": max_abs_rel_pct,
                "mean_abs_relative_energy_deviation_percent": mean_abs_rel_pct,
                "final_relative_energy_deviation_percent": final_rel_pct,
                "mean_total_energy_eps": float(np.nanmean(finite_etot)) if finite_etot.size else None,
                "divergent_tail_omitted": bool(series["has_nonfinite"]),
                "divergence_step": divergence_step,
                "divergence_time_ps": divergence_time_ps,
                "divergence_reason": divergence_reason,
            }
        )
        if max_abs_rel_pct is not None and final_rel_pct is not None:
            ann_lines = [
                f"max |ΔE/E0| = {max_abs_rel_pct:.3f}%",
                f"final ΔE/E0 = {final_rel_pct:.3f}%",
            ]
            if mean_abs_rel_pct is not None:
                ann_lines.append(f"mean |ΔE/E0| = {mean_abs_rel_pct:.3f}%")
            ax_d.text(
                0.98,
                0.06,
                "\n".join(ann_lines),
                transform=ax_d.transAxes,
                ha="right",
                va="bottom",
                fontsize=8.5,
                bbox={"facecolor": "white", "alpha": 0.82, "edgecolor": "none"},
            )
        if divergence_step is not None and "Euler" in label and divergence_time_ps is not None:
            if euler_divergence_time_ps is None or divergence_time_ps < euler_divergence_time_ps:
                euler_divergence_time_ps = divergence_time_ps

    if not any_data:
        plt.close(fig)
        print(f"Warning: no usable data for {run_key}; skipped {out_name}")
        return None

    if config.get("crop_to_euler_divergence", False):
        x_max = divergence_crop_limit(euler_divergence_time_ps, max_time_ps)
    if x_max is None and np.isfinite(max_time_ps) and max_time_ps > 0:
        x_max = float(max_time_ps)
    if x_max is not None:
        for row in range(2):
            axes[row].set_xlim(0.0, x_max)

    axes[1].set_xlabel("Time [ps]")
    if config.get("include_required_run_note", False):
        fig.set_constrained_layout_pads(h_pad=0.12, w_pad=0.03, hspace=0.08, wspace=0.08)
        fig.text(
            0.5,
            0.003,
            "Required production run: 100 steps (1 ps), after startup/equilibration. "
            "CSV step 0 is the production initial frame; final startup->production rescale applied.",
            ha="center",
            fontsize=9,
        )

    out_path = f"{PLOT_DIR}/{out_name}"
    save_figure(fig, out_path)
    plt.close(fig)
    print(f"Saved {out_path}")

    any_tail_omitted = any(row.get("divergent_tail_omitted") for row in per_integrator_summary)
    energy_caveats = [
        "Relative drift is computed from total energy with E0 taken at the first finite production frame.",
        "LJ uses a hard cutoff without potential shifting; small energy discontinuities can occur when pairs cross r_cut.",
        "For required-run interpretation, startup/equilibration is completed before this production trajectory.",
    ]
    if any_tail_omitted:
        energy_caveats.append("Divergent non-finite tails are omitted only where the raw series becomes non-finite.")

    write_plot_metadata(
        out_name,
        "results2",
        {
            "figure_number": config.get("figure_number_energy"),
            "panels": config.get("panels_energy", ["a)", "b)"]),
            "source_data_files": unique_preserve_order(source_data_files),
            "source_manifest_keys": unique_preserve_order(source_manifest_keys),
            "simulation_run_identifiers": unique_preserve_order([r for r in simulation_run_identifiers if r]),
            "key_parameters": {
                "integrators_compared": [integrator["style_key"] for integrator in config["integrators"]],
                "energy_units": "epsilon",
                "temperature_divergence_threshold_k": TEMP_DIVERGENCE_K,
                "figure_layout": {
                    "rows": ["Velocity-Verlet", "Forward Euler"],
                    "columns": ["signed relative total-energy deviation ΔE/E0 [%] vs time [ps]"],
                },
                "drift_only_figure": True,
                "panel_content": "signed relative total-energy deviation only (ΔE/E0 [%])",
                "series_parameters": series_parameters,
                "run_semantics": {
                    "required_production_steps": 100 if run_key == "lj_brief" else None,
                    "required_production_time_ps": 1.0 if run_key == "lj_brief" else None,
                    "startup_precedes_production": True,
                    "final_rescale_before_production_expected": True,
                    "step_0_semantics": "step 0 in CSV is the production initial frame",
                },
            },
            "fit_or_truncation": {
                "relative_deviation_reference": "first finite E_total point at or after production_start_step",
                "divergent_tail_handling": (
                    "non-finite values or |T| > threshold are omitted from plotted tail"
                    if any_tail_omitted
                    else "no tail omitted; full available production window is plotted"
                ),
                "crop_to_euler_divergence": bool(config.get("crop_to_euler_divergence", False)),
                "applied_xlim_ps": [0.0, float(x_max)] if x_max is not None else None,
                "drift_only": True,
            },
            "key_quantitative_summary": {
                "max_time_ps_in_source": float(max_time_ps),
                "euler_divergence_time_ps": euler_divergence_time_ps,
                "per_integrator": per_integrator_summary,
            },
            "caveats": energy_caveats,
            "missing_provenance": missing_provenance,
        },
    )
    return {
        "plot_file": out_path,
        "per_integrator": per_integrator_summary,
        "series_parameters": series_parameters,
        "xlim_ps": [0.0, float(x_max)] if x_max is not None else None,
    }


def plot_temperature_for_run(manifest, run_key, config, out_name):
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=config.get("figsize", (10, 5)), constrained_layout=True)
    any_data = False
    plotted_series = []
    euler_divergence_time_ps = None
    max_time_ps = 0.0
    x_max = None
    target_temp_k = config.get("target_temperature_k")
    source_data_files = []
    source_manifest_keys = []
    simulation_run_identifiers = []
    per_integrator_summary = []
    series_parameters = {}
    missing_provenance = []
    production_start_line_ps = None
    divergence_marker_labeled = False

    for integrator in config["integrators"]:
        series_key = integrator["series_key"]
        label = integrator["label"]
        style_key = integrator["style_key"]
        manifest_key = f"{run_key}.{series_key}"
        style = INTEGRATOR_STYLE[integrator["style_key"]]
        color = style["color"]
        linestyle = style["linestyle"]
        linewidth = max(2.0, style["linewidth"])

        fpath = nested_get(manifest, manifest_key)
        if not fpath or not os.path.exists(fpath):
            missing_provenance.append(f"manifest/data file missing for {manifest_key}")
            continue
        series = load_series(fpath)
        if series is None:
            missing_provenance.append(f"series unreadable or missing required columns for {manifest_key}")
            continue

        any_data = True
        t = series["time_ps"]
        if np.any(np.isfinite(t)):
            max_time_ps = max(max_time_ps, float(np.nanmax(t)))
        temp = series["temperature"]
        meta = series["meta"]
        meta_typed = series["meta_typed"]
        source_data_files.append(fpath)
        source_manifest_keys.append(manifest_key)
        simulation_run_identifiers.append(series["run_identifier"])
        series_parameters[style_key] = extract_series_parameters(meta_typed)
        ax.plot(t, temp, label=label, color=color, linestyle=linestyle, linewidth=linewidth)
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
        finite_temp = temp[np.isfinite(temp)]
        per_integrator_summary.append(
            {
                "integrator": style_key,
                "label": label,
                "manifest_key": manifest_key,
                "source_file": fpath,
                "run_identifier": series["run_identifier"],
                "points_plotted": int(np.count_nonzero(np.isfinite(temp))),
                "mean_temperature_k": float(np.nanmean(finite_temp)) if finite_temp.size else None,
                "std_temperature_k": float(np.nanstd(finite_temp)) if finite_temp.size else None,
                "min_temperature_k": float(np.nanmin(finite_temp)) if finite_temp.size else None,
                "max_temperature_k": float(np.nanmax(finite_temp)) if finite_temp.size else None,
                "divergent_tail_omitted": bool(series["has_nonfinite"]),
                "divergence_step": series.get("divergence_step"),
                "divergence_time_ps": series.get("divergence_time_ps"),
                "divergence_reason": series.get("divergence_reason"),
            }
        )
        divergence_step = series.get("divergence_step")
        divergence_time_ps = series.get("divergence_time_ps")
        divergence_reason = series.get("divergence_reason")
        if divergence_step is not None and "Euler" in label and divergence_time_ps is not None:
            if euler_divergence_time_ps is None or divergence_time_ps < euler_divergence_time_ps:
                euler_divergence_time_ps = divergence_time_ps
            vline_label = None
            if not divergence_marker_labeled:
                vline_label = "Euler divergence point"
                divergence_marker_labeled = True
            ax.axvline(
                divergence_time_ps,
                color=color,
                linestyle="--",
                linewidth=1.2,
                alpha=0.8,
                label=vline_label,
            )

        production_start = get_meta_value(meta, "production_start_step", "production_start", 0)
        dt = parse_float_meta(meta, "dt", float("nan"))
        if target_temp_k is None:
            target_temp_candidate = parse_float_meta(meta, "target_temperature", float("nan"))
            if np.isfinite(target_temp_candidate):
                target_temp_k = float(target_temp_candidate)
        if production_start > 0 and np.isfinite(dt) and production_start_line_ps is None:
            production_start_line_ps = float(production_start * dt * 1e12)
            ax.axvline(
                x=production_start_line_ps,
                color="gray",
                linestyle=":",
                linewidth=1.5,
                alpha=0.8,
                label="production starts",
            )

    if not any_data:
        plt.close(fig)
        print(f"Warning: no usable data for {run_key}; skipped {out_name}")
        return None

    ax.set_xlabel("Time [ps]")
    ax.set_ylabel("Temperature [K]")
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
            label=f"Target temperature ({target_temp_k:.1f} K)",
        )

    legend_kwargs = {
        "loc": config.get("legend_loc", "upper left"),
        "frameon": True,
        "facecolor": "white",
        "framealpha": 0.94,
        "edgecolor": "#BDBDBD",
        "borderpad": 0.45,
        "labelspacing": 0.35,
    }
    if "legend_bbox_to_anchor" in config:
        legend_kwargs["bbox_to_anchor"] = config["legend_bbox_to_anchor"]
    ax.legend(**legend_kwargs)

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

    if config.get("include_required_run_note", False):
        fig.text(
            0.5,
            0.01,
            "Required production run: 100 steps (1 ps), after startup/equilibration. "
            "Temperature evidence complements the energy-stability and RDF comparison results.",
            ha="center",
            fontsize=9,
        )

    out_path = f"{PLOT_DIR}/{out_name}"
    save_figure(fig, out_path)
    plt.close(fig)
    print(f"Saved {out_path}")

    write_plot_metadata(
        out_name,
        "results2",
        {
            "figure_number": config.get("figure_number_temperature"),
            "panels": config.get("panels_temperature", ["a)"]),
            "source_data_files": unique_preserve_order(source_data_files),
            "source_manifest_keys": unique_preserve_order(source_manifest_keys),
            "simulation_run_identifiers": unique_preserve_order([r for r in simulation_run_identifiers if r]),
            "key_parameters": {
                "integrators_compared": [integrator["style_key"] for integrator in config["integrators"]],
                "target_temperature_k": float(target_temp_k) if target_temp_k is not None and np.isfinite(target_temp_k) else None,
                "temperature_divergence_threshold_k": TEMP_DIVERGENCE_K,
                "series_parameters": series_parameters,
                "run_semantics": {
                    "required_production_steps": 100 if run_key == "lj_brief" else None,
                    "required_production_time_ps": 1.0 if run_key == "lj_brief" else None,
                    "startup_precedes_production": True,
                    "final_rescale_before_production_expected": True,
                    "step_0_semantics": "step 0 in CSV is the production initial frame",
                },
            },
            "fit_or_truncation": {
                "divergent_tail_handling": "non-finite values or |T| > threshold are omitted from plotted tail",
                "crop_to_euler_divergence": bool(config.get("crop_to_euler_divergence", False)),
                "applied_xlim_ps": [0.0, float(x_max)] if x_max is not None else None,
                "production_start_line_ps": production_start_line_ps,
                "zoom_inset": config.get("zoom_inset", None),
            },
            "key_quantitative_summary": {
                "max_time_ps_in_source": float(max_time_ps),
                "euler_divergence_time_ps": euler_divergence_time_ps,
                "per_integrator": per_integrator_summary,
            },
            "caveats": [
                "Temperature is shown only for finite values; divergent tails are omitted.",
                "Target temperature line is a reference, not a fitted value.",
                "Temperature evidence is complementary and should be interpreted with the energy and RDF results.",
            ],
            "missing_provenance": missing_provenance,
        },
    )
    return {
        "plot_file": out_path,
        "per_integrator": per_integrator_summary,
        "series_parameters": series_parameters,
        "xlim_ps": [0.0, float(x_max)] if x_max is not None else None,
    }


def extract_rdf_feature(r_vals, g_vals, rmin, rmax, mode):
    mask = np.isfinite(r_vals) & np.isfinite(g_vals) & (r_vals >= rmin) & (r_vals <= rmax)
    if not np.any(mask):
        return None, None
    rr = r_vals[mask]
    gg = g_vals[mask]
    idx = int(np.argmax(gg)) if mode == "max" else int(np.argmin(gg))
    return float(rr[idx]), float(gg[idx])


def smooth_curve_pchip(x_vals, y_vals, samples_per_segment=40):
    x = np.asarray(x_vals, dtype=float)
    y = np.asarray(y_vals, dtype=float)
    valid = np.isfinite(x) & np.isfinite(y)
    x = x[valid]
    y = y[valid]
    if x.size < 2:
        return x, y

    order = np.argsort(x)
    x = x[order]
    y = y[order]
    x, unique_idx = np.unique(x, return_index=True)
    y = y[unique_idx]

    n = x.size
    if n == 2:
        xx = np.linspace(x[0], x[1], samples_per_segment + 1)
        yy = np.interp(xx, x, y)
        return xx, yy

    h = np.diff(x)
    delta = np.diff(y) / h
    d = np.zeros(n, dtype=float)

    def endpoint_slope(h0, h1, delta0, delta1):
        slope = ((2.0 * h0 + h1) * delta0 - h0 * delta1) / (h0 + h1)
        if np.sign(slope) != np.sign(delta0):
            return 0.0
        if np.sign(delta0) != np.sign(delta1) and abs(slope) > abs(3.0 * delta0):
            return 3.0 * delta0
        return slope

    d[0] = endpoint_slope(h[0], h[1], delta[0], delta[1])
    d[-1] = endpoint_slope(h[-1], h[-2], delta[-1], delta[-2])

    for k in range(1, n - 1):
        if delta[k - 1] == 0.0 or delta[k] == 0.0 or np.sign(delta[k - 1]) != np.sign(delta[k]):
            d[k] = 0.0
        else:
            w1 = 2.0 * h[k] + h[k - 1]
            w2 = h[k] + 2.0 * h[k - 1]
            d[k] = (w1 + w2) / (w1 / delta[k - 1] + w2 / delta[k])

    x_dense_parts = []
    y_dense_parts = []
    for i in range(n - 1):
        t = np.linspace(0.0, 1.0, samples_per_segment, endpoint=False)
        hi = h[i]
        x_seg = x[i] + t * hi
        h00 = 2.0 * t**3 - 3.0 * t**2 + 1.0
        h10 = t**3 - 2.0 * t**2 + t
        h01 = -2.0 * t**3 + 3.0 * t**2
        h11 = t**3 - t**2
        y_seg = h00 * y[i] + h10 * hi * d[i] + h01 * y[i + 1] + h11 * hi * d[i + 1]
        x_dense_parts.append(x_seg)
        y_dense_parts.append(y_seg)

    x_dense_parts.append(np.array([x[-1]]))
    y_dense_parts.append(np.array([y[-1]]))
    return np.concatenate(x_dense_parts), np.concatenate(y_dense_parts)


def plot_rdf(manifest, rahman_points, out_name=FIG8_RDF_PNG):
    os.makedirs(PLOT_DIR, exist_ok=True)

    gr_path = nested_get(manifest, "lj_rdf.verlet_long")
    if not gr_path or not os.path.exists(gr_path):
        print("No RDF data found at manifest key lj_rdf.verlet_long. Skipping RDF plot.")
        return None

    data = load_csv(gr_path)
    if data is None or len(data) == 0:
        print("RDF CSV is empty. Skipping RDF plot.")
        return None

    names = set(data.dtype.names or [])
    if "r_sigma" not in names or "gr" not in names:
        print("RDF CSV missing r_sigma/gr columns. Skipping RDF plot.")
        return None
    gr_meta_typed = typed_meta(parse_csv_metadata(gr_path))
    run_identifier = run_identifier_from_path(gr_path)

    r_sigma = finite_or_nan(np.asarray(data["r_sigma"], dtype=float))
    gr = finite_or_nan(np.asarray(data["gr"], dtype=float))

    rahman_r_sigma = np.array([p["r_over_sigma"] for p in rahman_points], dtype=float)
    rahman_r_angstrom = np.array([p["r_angstrom"] for p in rahman_points], dtype=float)
    rahman_g = np.array([p["g_value"] for p in rahman_points], dtype=float)
    rahman_types = [p["point_type"] for p in rahman_points]
    paper_mask = np.array([pt == "paper_anchored" for pt in rahman_types], dtype=bool)
    shape_mask = ~paper_mask
    paper_points = [p for p in rahman_points if p["point_type"] == "paper_anchored"]
    rahman_guide_r, rahman_guide_g = smooth_curve_pchip(rahman_r_sigma, rahman_g, samples_per_segment=40)

    fig, ax = plt.subplots(figsize=(8.4, 5.1), constrained_layout=True)
    ax.plot(r_sigma, gr, color="k", linewidth=2.2, zorder=4, label="Present work (Velocity-Verlet, NVE)")
    ax.plot(
        rahman_guide_r,
        rahman_guide_g,
        color=COLOR_EULER,
        linestyle=(0, (4, 3)),
        linewidth=1.6,
        alpha=0.72,
        zorder=5,
        label="Rahman guide (derived manual anchors)",
    )
    ax.scatter(
        rahman_r_sigma[paper_mask],
        rahman_g[paper_mask],
        s=42,
        marker="X",
        color=COLOR_EULER,
        edgecolors="white",
        linewidths=0.9,
        zorder=7,
        label="Rahman paper-anchored X points",
    )
    paper_annotation_offsets = [(22, -4), (22, 0), (18, 2)]
    annotation_fontsize = plt.rcParams.get("legend.fontsize", 10)
    for idx, point in enumerate(paper_points):
        dx, dy = paper_annotation_offsets[idx] if idx < len(paper_annotation_offsets) else (24, 8)
        anchor_x = float(point["r_over_sigma"])
        anchor_y = float(point["g_value"])
        label = (
            f"r={point['r_angstrom']:.1f} Å (r/σ={anchor_x:.3f})\n"
            f"g(r)≈{anchor_y:.2f}"
        )
        ax.annotate(
            label,
            xy=(anchor_x, anchor_y),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=annotation_fontsize,
            color="black",
            ha="left",
            va="bottom",
            arrowprops={
                "arrowstyle": "->",
                "color": "black",
                "lw": 0.9,
                "shrinkA": 2,
                "shrinkB": 9,
                "alpha": 0.9,
            },
            bbox={"facecolor": "white", "alpha": 0.78, "edgecolor": "none", "pad": 1.3},
            zorder=5,
        )
    ax.axhline(y=1.0, color=COLOR_REFERENCE, linestyle=(0, (3, 3)), linewidth=1.0, alpha=0.65, label="g(r) = 1")

    ax.set_xlabel(r"Distance $r/\sigma$")
    ax.set_ylabel("g(r)")
    finite_r = r_sigma[np.isfinite(r_sigma)]
    xmax = np.nanmax(np.concatenate([finite_r, rahman_r_sigma])) if finite_r.size else np.max(rahman_r_sigma)
    ax.set_xlim(0.0, max(3.6, 1.03 * float(xmax)))
    ax.set_ylim(bottom=0.0)
    secax = ax.secondary_xaxis(
        "top",
        functions=(lambda x: x * SIGMA_ANGSTROM, lambda x: x / SIGMA_ANGSTROM),
    )
    secax.set_xlabel("Distance r (Å)")
    apply_major_grid(ax)
    disable_offset_text(ax)
    ax.legend(loc="upper right")

    out_path = f"{PLOT_DIR}/{out_name}"
    save_figure(fig, out_path)
    plt.close(fig)
    print(f"Saved {out_path}")

    finite_mask = np.isfinite(r_sigma) & np.isfinite(gr)
    r_plot = r_sigma[finite_mask]
    g_plot = gr[finite_mask]

    first_peak_r, first_peak_g = extract_rdf_feature(r_plot, g_plot, 0.95, 1.30, mode="max")
    first_min_r, first_min_g = extract_rdf_feature(r_plot, g_plot, 1.30, 1.80, mode="min")
    second_peak_r, second_peak_g = extract_rdf_feature(r_plot, g_plot, 1.80, 2.40, mode="max")
    tail_mask = r_plot >= 4.0
    tail_mean = float(np.nanmean(g_plot[tail_mask])) if np.any(tail_mask) else None

    write_plot_metadata(
        out_name,
        "results2",
        {
            "figure_number": 8,
            "panels": ["a)"],
            "source_data_files": unique_preserve_order(
                [
                    gr_path,
                    nested_get(manifest, "lj_rdf.verlet_long_energy", ""),
                    RAHMAN_SOURCE_FILE,
                ]
            ),
            "source_manifest_keys": ["lj_rdf.verlet_long", "lj_rdf.verlet_long_energy"],
            "simulation_run_identifiers": [run_identifier] if run_identifier else [],
            "key_parameters": {
                "present_work_series": extract_series_parameters(gr_meta_typed),
                "distance_units": {
                    "main_axis": "r/sigma",
                    "secondary_axis": "angstrom",
                    "sigma_angstrom": SIGMA_ANGSTROM,
                },
                "reference_dataset": {
                    "source_file": RAHMAN_SOURCE_FILE,
                    "model": "two-tier manual anchor set (paper_anchored + shape_anchor)",
                    "paper_anchored_x_angstrom": [3.7, 7.0, 10.4],
                    "paper_sigma_angstrom": SIGMA_ANGSTROM,
                    "n_points_total": len(rahman_points),
                    "n_points_paper_anchored": int(np.count_nonzero(paper_mask)),
                    "n_points_shape_anchor": int(np.count_nonzero(shape_mask)),
                },
            },
            "fit_or_truncation": {
                "reference_guide": "shape-preserving cubic dashed guide through manual anchor points",
                "present_work_truncation": "none",
            },
            "key_quantitative_summary": {
                "present_work_first_peak_r_over_sigma": first_peak_r,
                "present_work_first_peak_g": first_peak_g,
                "present_work_first_minimum_r_over_sigma": first_min_r,
                "present_work_first_minimum_g": first_min_g,
                "present_work_second_peak_r_over_sigma": second_peak_r,
                "present_work_second_peak_g": second_peak_g,
                "present_work_long_range_mean_g_for_r_over_sigma_ge_4": tail_mean,
                "rahman_anchor_points": rahman_points,
            },
            "caveats": [
                "Rahman comparison uses a manually extracted approximate reference guide from printed Fig. 2.",
                "Sigma = 3.4 Å is paper-supported; x-positions 3.7 Å, 7.0 Å, and 10.4 Å are paper-anchored figure annotations.",
                "All Rahman g(r) values and all non-anchored x-values are approximate manual reads from the printed plot.",
                "No error bars are shown; comparison is qualitative/semi-quantitative rather than exact.",
            ],
            "missing_provenance": [],
        },
    )

    rahman_feature_map = {
        "first_peak": next((p for p in rahman_points if p["point_id"] == 2), None),
        "first_minimum": next((p for p in rahman_points if p["point_id"] == 4), None),
        "second_peak": next((p for p in rahman_points if p["point_id"] == 5), None),
        "tail": next((p for p in rahman_points if p["point_id"] == 9), None),
    }

    return {
        "plot_file": out_path,
        "present_features": {
            "first_peak": {"r_over_sigma": first_peak_r, "g_value": first_peak_g},
            "first_minimum": {"r_over_sigma": first_min_r, "g_value": first_min_g},
            "second_peak": {"r_over_sigma": second_peak_r, "g_value": second_peak_g},
            "tail": {"r_over_sigma": ">=4.0 (mean)", "g_value": tail_mean},
        },
        "rahman_features": rahman_feature_map,
        "rahman_points": rahman_points,
    }


def safe_plot(name, fn, *args):
    try:
        return fn(*args)
    except Exception as exc:
        print(f"Warning: {name} failed: {exc}")
        return None


def format_float(value, digits=3):
    if value is None:
        return "n/a"
    if isinstance(value, str):
        return value
    if not np.isfinite(value):
        return "n/a"
    return f"{value:.{digits}f}"


def main():
    apply_plot_style()
    manifest = load_manifest()
    remove_old_results2_files()
    rahman_points = load_rahman_anchor_points(RAHMAN_SOURCE_FILE)

    brief_cfg = {
        "integrators": [
            {"series_key": "verlet", "label": "Velocity-Verlet", "style_key": "verlet"},
            {"series_key": "euler", "label": "Forward Euler", "style_key": "euler"},
        ],
        "energy_title": "Lennard-Jones argon, required 1 ps NVE run: total-energy drift",
        "temperature_title": "Lennard-Jones argon, required 1 ps NVE run: temperature",
        "figure_number_energy": 6,
        "figure_number_temperature": 7,
        "panels_energy": ["a)", "b)"],
        "panels_temperature": ["a)"],
        "include_required_run_note": False,
        "energy_per_row_autoscale": True,
        "legend_loc": "upper left",
        "figsize": (9.8, 4.8),
    }

    brief_energy = safe_plot(
        "brief energy",
        plot_energy_for_run,
        manifest,
        "lj_brief",
        brief_cfg,
        FIG6_ENERGY_PNG,
    )
    brief_temperature = safe_plot(
        "brief temperature",
        plot_temperature_for_run,
        manifest,
        "lj_brief",
        brief_cfg,
        FIG7_TEMPERATURE_PNG,
    )

    rdf_summary = safe_plot("rdf", plot_rdf, manifest, rahman_points, FIG8_RDF_PNG)


if __name__ == "__main__":
    main()
