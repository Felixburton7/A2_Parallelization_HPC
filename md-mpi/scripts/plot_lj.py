#!/usr/bin/env python3
"""
plot_lj.py — Generate Lennard-Jones / Argon validation plots (Results 2).

Produces:
  - out/plots/results2_lj_brief_energy_100step_production.png
  - out/plots/results2_lj_brief_temperature_100step_production.png
  - out/plots/results2_lj_rdf_comparison_rahman1964.png
"""

import csv
import json
import os
import shutil
from datetime import datetime, timezone

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
PLOT_META_DIR = "out/plots/metadata"
SUMMARY_DIR = "out/summary/results2"
RAHMAN_SOURCE_FILE = "scripts/data/rahman1964_fig2_manual_anchors.csv"
RAHMAN_OUT_FILE = f"{SUMMARY_DIR}/rahman1964_fig2_manual_anchors.csv"
RESULTS2_TABLE_MD = f"{SUMMARY_DIR}/results2_quantitative_summary_table.md"
RESULTS2_TABLE_CSV = f"{SUMMARY_DIR}/results2_quantitative_summary_table.csv"
RESULTS2_TABLE_JSON = f"{SUMMARY_DIR}/results2_quantitative_summary_table.json"
RESULTS2_REPORT_NOTE = f"{SUMMARY_DIR}/results2_report_note.md"
RESULTS2_RECOMMENDED_FIGURES = f"{SUMMARY_DIR}/results2_recommended_figure_set.md"
RESULTS2_RAHMAN_EXTRACTION_NOTE = f"{SUMMARY_DIR}/results2_rahman_extraction_note.md"
RESULTS2_CHANGE_NOTE = f"{SUMMARY_DIR}/results2_what_changed_and_why.md"
REMOVED_RESULTS2_FILES = [
    f"{PLOT_DIR}/results2_lj_extended_energy_stability.png",
    f"{PLOT_DIR}/results2_lj_extended_temperature_stability.png",
    f"{PLOT_META_DIR}/results2_lj_extended_energy_stability.json",
    f"{PLOT_META_DIR}/results2_lj_extended_temperature_stability.json",
]

EPSILON_OVER_KB = 120.0
KB = 1.380649e-23
EPSILON = KB * EPSILON_OVER_KB
SIGMA_ANGSTROM = 3.4
TEMP_DIVERGENCE_K = 1.0e4


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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
    os.makedirs(PLOT_META_DIR, exist_ok=True)
    payload = {
        "generated_utc": utc_now(),
        "figure_filename": plot_png_name,
        "plot_file_png": f"{PLOT_DIR}/{plot_png_name}",
        "section": section,
        "missing_provenance": [],
    }
    payload.update(extra)
    payload["missing_provenance"] = unique_preserve_order(payload.get("missing_provenance", []))
    sidecar = f"{PLOT_META_DIR}/{os.path.splitext(plot_png_name)[0]}.json"
    with open(sidecar, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
    print(f"Saved {sidecar}")


def write_text_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content.rstrip() + "\n")
    print(f"Saved {path}")


def write_json_file(path, payload):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"Saved {path}")


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


def sync_rahman_anchor_dataset(source_path, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    shutil.copy2(source_path, out_path)
    print(f"Copied {source_path} -> {out_path}")


def update_manifest_with_results2_outputs(manifest_update):
    manifest_path = f"{OUT_DIR}/manifest.json"
    if not os.path.exists(manifest_path):
        return
    try:
        with open(manifest_path, "r", encoding="utf-8") as handle:
            manifest = json.load(handle)
    except json.JSONDecodeError:
        print("Warning: manifest JSON invalid; skipping results2_outputs manifest update")
        return

    # Extended Results 2 run keys are intentionally removed from the active
    # report-facing manifest package.
    manifest.pop("lj_extended", None)
    manifest["results2_outputs"] = manifest_update
    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=False)
        handle.write("\n")
    print(f"Updated {manifest_path} with results2_outputs")


def remove_stale_results2_extended_artifacts():
    for path in REMOVED_RESULTS2_FILES:
        if os.path.exists(path):
            os.remove(path)
            print(f"Removed stale artifact {path}")


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
        2,
        figsize=(13.2, 8.2),
        sharex="col",
        constrained_layout=True,
        gridspec_kw={"width_ratios": [1.0, 1.28]},
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
    energy_component_ranges = {}

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
        ekin = series["ekin_eps"]
        epot = series["epot_eps"]
        etot = series["etot_eps"]
        meta = series["meta"]
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
        else:
            e0 = etot[ref_idx]
            if np.isfinite(e0) and abs(e0) > 1e-30:
                rel_dev_pct = 100.0 * (etot - e0) / abs(e0)
            else:
                rel_dev_pct = np.full_like(etot, np.nan)
            rel_dev_ref_step = int(steps[ref_idx])

        ax_e = axes[row, 0]
        ax_e.plot(t, ekin, label=r"$E_{kin}$", color=COLOR_ACCENT, linewidth=1.6, alpha=0.95)
        ax_e.plot(t, epot, label=r"$E_{pot}$", color=COLOR_VERLET, linewidth=1.6, alpha=0.95)
        ax_e.plot(t, etot, label=r"$E_{total}$", color="k", linewidth=2.1, alpha=0.98)
        finite_energy = np.concatenate(
            [
                ekin[np.isfinite(ekin)],
                epot[np.isfinite(epot)],
                etot[np.isfinite(etot)],
            ]
        )
        if finite_energy.size:
            energy_component_ranges[row] = (float(np.nanmin(finite_energy)), float(np.nanmax(finite_energy)))
        ax_e.set_ylabel(r"Energy [$\varepsilon$]")
        apply_major_grid(ax_e)
        disable_offset_text(ax_e)
        if row == 0:
            ax_e.set_title("Energy Components")
            ax_e.legend(loc="best")
        row_label = label
        if style_key == "verlet":
            row_label += " (stable)"
        if style_key == "euler":
            row_label += " (strong drift)"
        ax_e.text(
            0.02,
            0.92,
            row_label,
            transform=ax_e.transAxes,
            fontsize=9,
            bbox={"facecolor": "white", "alpha": 0.86, "edgecolor": "none"},
        )

        ax_d = axes[row, 1]
        ax_d.plot(t, rel_dev_pct, color=color, linestyle=linestyle, linewidth=max(2.2, linewidth))
        ax_d.set_ylabel(r"$\Delta E / E_0$ [%]")
        ax_d.axhline(0.0, color=COLOR_REFERENCE, linestyle="--", linewidth=1.0, alpha=0.5)
        if row == 0:
            ax_d.set_title("Relative Total-Energy Deviation")
        apply_major_grid(ax_d)
        disable_offset_text(ax_d)

        divergence_step = series.get("divergence_step")
        divergence_time_ps = series.get("divergence_time_ps")
        divergence_reason = series.get("divergence_reason")
        finite_rel_pct = rel_dev_pct[np.isfinite(rel_dev_pct)]
        finite_etot = etot[np.isfinite(etot)]
        max_abs_rel_pct = float(np.nanmax(np.abs(finite_rel_pct))) if finite_rel_pct.size else None
        mean_abs_rel_pct = float(np.nanmean(np.abs(finite_rel_pct))) if finite_rel_pct.size else None
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
                "final_relative_energy_deviation_percent": (
                    float(finite_rel_pct[-1]) if finite_rel_pct.size else None
                ),
                "mean_total_energy_eps": float(np.nanmean(finite_etot)) if finite_etot.size else None,
                "divergent_tail_omitted": bool(series["has_nonfinite"]),
                "divergence_step": divergence_step,
                "divergence_time_ps": divergence_time_ps,
                "divergence_reason": divergence_reason,
            }
        )
        if max_abs_rel_pct is not None:
            ax_d.text(
                0.02,
                0.90,
                f"max |ΔE/E0| = {max_abs_rel_pct:.3f}%",
                transform=ax_d.transAxes,
                ha="left",
                fontsize=8.5,
                bbox={"facecolor": "white", "alpha": 0.82, "edgecolor": "none"},
            )
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
        return None

    if config.get("crop_to_euler_divergence", False):
        x_max = divergence_crop_limit(euler_divergence_time_ps, max_time_ps)
        if x_max is not None:
            for row in range(2):
                for col in range(2):
                    axes[row, col].set_xlim(0.0, x_max)
    if config.get("energy_per_row_autoscale", True):
        energy_pad_lower_frac = float(config.get("energy_pad_lower_frac", 0.08))
        energy_pad_upper_frac = float(config.get("energy_pad_upper_frac", 0.14))
        for row in range(2):
            if row not in energy_component_ranges:
                continue
            ymin, ymax = energy_component_ranges[row]
            span = ymax - ymin
            if not np.isfinite(span):
                continue
            if span < 1e-9:
                center = 0.5 * (ymin + ymax)
                pad_low = max(1.0, 0.05 * max(abs(center), 1.0))
                pad_high = pad_low
            else:
                pad_low = energy_pad_lower_frac * span
                pad_high = energy_pad_upper_frac * span
            axes[row, 0].set_ylim(ymin - pad_low, ymax + pad_high)
    energy_ylim = config.get("energy_ylim")
    if energy_ylim is not None:
        for row in range(2):
            axes[row, 0].set_ylim(float(energy_ylim[0]), float(energy_ylim[1]))
    else:
        energy_ymax = config.get("energy_ymax")
        if energy_ymax is not None:
            for row in range(2):
                axes[row, 0].set_ylim(top=float(energy_ymax))

    axes[1, 0].set_xlabel("Time [ps]")
    axes[1, 1].set_xlabel("Time [ps]")
    fig.suptitle(config["energy_title"], fontsize=13)
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

    write_plot_metadata(
        out_name,
        "results2",
        {
            "purpose": config["energy_purpose"],
            "intended_claim": config["energy_claim"],
            "audience_tier": config["audience_tier"],
            "source_data_files": unique_preserve_order(source_data_files),
            "source_manifest_keys": unique_preserve_order(source_manifest_keys),
            "simulation_run_identifiers": unique_preserve_order([r for r in simulation_run_identifiers if r]),
            "key_parameters": {
                "integrators_compared": [integrator["style_key"] for integrator in config["integrators"]],
                "energy_units": "epsilon",
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
                "relative_deviation_reference": "first finite E_total point at or after production_start_step",
                "divergent_tail_handling": "non-finite values or |T| > threshold are omitted from plotted tail",
                "crop_to_euler_divergence": bool(config.get("crop_to_euler_divergence", False)),
                "applied_xlim_ps": [0.0, float(x_max)] if x_max is not None else None,
            },
            "key_quantitative_summary": {
                "max_time_ps_in_source": float(max_time_ps),
                "euler_divergence_time_ps": euler_divergence_time_ps,
                "per_integrator": per_integrator_summary,
            },
            "caveats": [
                "Energy curves are shown in reduced units (E/epsilon).",
                "Divergent tails are intentionally omitted to keep the stable regime readable.",
                "For required-run interpretation, startup/equilibration is completed before this production trajectory.",
            ],
            "missing_provenance": missing_provenance,
        },
    )
    return {
        "plot_file": out_path,
        "metadata_file": f"{PLOT_META_DIR}/{os.path.splitext(out_name)[0]}.json",
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
            "Required production run: 100 steps (1 ps), after startup/equilibration and final rescale. "
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
            "purpose": config["temperature_purpose"],
            "intended_claim": config["temperature_claim"],
            "audience_tier": config["audience_tier"],
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
        "metadata_file": f"{PLOT_META_DIR}/{os.path.splitext(out_name)[0]}.json",
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


def plot_rdf(manifest, rahman_points):
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

    fig, ax = plt.subplots(figsize=(8.4, 5.1), constrained_layout=True)
    ax.plot(r_sigma, gr, color="k", linewidth=2.2, zorder=4, label="Present work (Velocity-Verlet, NVE)")
    ax.plot(
        rahman_r_sigma,
        rahman_g,
        color=COLOR_EULER,
        linestyle=(0, (4, 3)),
        linewidth=1.6,
        alpha=0.72,
        zorder=5,
        label="Rahman guide (manual anchors)",
    )
    ax.scatter(
        rahman_r_sigma[shape_mask],
        rahman_g[shape_mask],
        s=30,
        facecolors="white",
        edgecolors=COLOR_EULER,
        linewidths=1.4,
        zorder=6,
        label="Rahman shape anchors (approx.)",
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
    paper_annotation_offsets = [(30, 4), (30, 8), (26, 10)]
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

    ax.set_title("Argon RDF Comparison: Present Work vs Rahman (1964)")
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

    out_name = "results2_lj_rdf_comparison_rahman1964.png"
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
            "purpose": (
                "Core brief-facing structural evidence: compare present-work Argon RDF against "
                "a transparent manually extracted Rahman (1964) Fig. 2 anchor guide."
            ),
            "intended_claim": (
                "The present Velocity-Verlet RDF reproduces liquid-argon shell structure "
                "(first peak, first minimum, second shell, long-range trend) with qualitative/"
                "semi-quantitative agreement to Rahman (1964), while peak heights are somewhat reduced."
            ),
            "audience_tier": "main-report-core",
            "source_data_files": unique_preserve_order(
                [
                    gr_path,
                    nested_get(manifest, "lj_rdf.verlet_long_energy", ""),
                    RAHMAN_OUT_FILE if os.path.exists(RAHMAN_OUT_FILE) else RAHMAN_SOURCE_FILE,
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
                    "source_file": RAHMAN_OUT_FILE if os.path.exists(RAHMAN_OUT_FILE) else RAHMAN_SOURCE_FILE,
                    "model": "two-tier manual anchor set (paper_anchored + shape_anchor)",
                    "paper_anchored_x_angstrom": [3.7, 7.0, 10.4],
                    "paper_sigma_angstrom": SIGMA_ANGSTROM,
                    "n_points_total": len(rahman_points),
                    "n_points_paper_anchored": int(np.count_nonzero(paper_mask)),
                    "n_points_shape_anchor": int(np.count_nonzero(shape_mask)),
                },
            },
            "fit_or_truncation": {
                "reference_guide": "piecewise-linear dashed guide connecting manual anchor points",
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
        "metadata_file": f"{PLOT_META_DIR}/{os.path.splitext(out_name)[0]}.json",
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


def integrator_map(summary_dict):
    out = {}
    if not summary_dict:
        return out
    for row in summary_dict.get("per_integrator", []):
        out[row.get("integrator")] = row
    return out


def write_results2_quantitative_summary(energy_brief_summary, temp_brief_summary, rdf_summary):
    os.makedirs(SUMMARY_DIR, exist_ok=True)

    energy_by_int = integrator_map(energy_brief_summary or {})
    temp_by_int = integrator_map(temp_brief_summary or {})

    rows_a = []
    for integrator, label in [("verlet", "Velocity-Verlet"), ("euler", "Euler")]:
        e_row = energy_by_int.get(integrator, {})
        t_row = temp_by_int.get(integrator, {})
        prod_steps = (
            (temp_brief_summary or {}).get("series_parameters", {}).get(integrator, {}).get("production_steps")
        )
        rows_a.append(
            {
                "Integrator": label,
                "Production steps": prod_steps if prod_steps is not None else "n/a",
                "Mean T [K]": format_float(t_row.get("mean_temperature_k"), 2),
                "Std T [K]": format_float(t_row.get("std_temperature_k"), 2),
                "Max |ΔE/E0| [%]": format_float(e_row.get("max_abs_relative_energy_deviation_percent"), 3),
                "Mean |ΔE/E0| [%]": format_float(e_row.get("mean_abs_relative_energy_deviation_percent"), 3),
                "Comment": (
                    "Bounded drift; near target state."
                    if integrator == "verlet"
                    else "Strong drift/heating over required run; not a stable NVE trajectory."
                ),
            }
        )

    present_features = (rdf_summary or {}).get("present_features", {})
    rahman_features = (rdf_summary or {}).get("rahman_features", {})
    rows_b = []
    feature_rows = [
        ("first_peak", "First peak", "Broadly correct location; present peak height is lower."),
        ("first_minimum", "First minimum", "Minimum position and depth are broadly consistent."),
        ("second_peak", "Second peak", "Second-shell position is consistent; present peak is lower."),
        ("tail", "Tail", "Long-range trend returns toward g(r)=1."),
    ]
    for key, label, comment in feature_rows:
        present = present_features.get(key, {})
        rahman = rahman_features.get(key, None)
        if rahman:
            provenance = (
                "paper_anchored x (y approx.)"
                if rahman.get("point_type") == "paper_anchored"
                else "shape_anchor (manual approx.)"
            )
            rahman_r = format_float(rahman.get("r_over_sigma"), 3)
            rahman_g = format_float(rahman.get("g_value"), 3)
        else:
            provenance = "n/a"
            rahman_r = "n/a"
            rahman_g = "n/a"

        rows_b.append(
            {
                "Feature": label,
                "Present work r/sigma": format_float(present.get("r_over_sigma"), 3),
                "Present work g(r)": format_float(present.get("g_value"), 3),
                "Rahman reference r/sigma": rahman_r,
                "Rahman reference g(r)": rahman_g,
                "Reference provenance": provenance,
                "Comment": comment,
            }
        )

    md_lines = [
        "# Results 2 Quantitative Summary Table",
        "",
        "## Section A: Required 100-step production run",
        "",
        "| Integrator | Production steps | Mean T [K] | Std T [K] | Max |ΔE/E0| [%] | Mean |ΔE/E0| [%] | Comment |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows_a:
        md_lines.append(
            f"| {row['Integrator']} | {row['Production steps']} | {row['Mean T [K]']} | "
            f"{row['Std T [K]']} | {row['Max |ΔE/E0| [%]']} | {row['Mean |ΔE/E0| [%]']} | {row['Comment']} |"
        )

    md_lines.extend(
        [
            "",
            "## Section B: RDF structural comparison",
            "",
            "| Feature | Present work r/sigma | Present work g(r) | Rahman reference r/sigma | Rahman reference g(r) | Reference provenance | Comment |",
            "|---|---:|---:|---:|---:|---|---|",
        ]
    )
    for row in rows_b:
        md_lines.append(
            f"| {row['Feature']} | {row['Present work r/sigma']} | {row['Present work g(r)']} | "
            f"{row['Rahman reference r/sigma']} | {row['Rahman reference g(r)']} | "
            f"{row['Reference provenance']} | {row['Comment']} |"
        )

    md_lines.extend(
        [
            "",
            "Notes:",
            "- Required run metrics are derived from manifest-linked `lj_brief` production CSV files (100 steps, 101 frames).",
            "- RDF values are from manifest-linked long Verlet RDF run; Rahman values are manual figure anchors (not tabulated exact data).",
        ]
    )

    write_text_file(RESULTS2_TABLE_MD, "\n".join(md_lines))

    csv_lines = [
        "section,Integrator/Feature,Production steps,Mean T [K],Std T [K],Max |ΔE/E0| [%],Mean |ΔE/E0| [%],Present work r/sigma,Present work g(r),Rahman reference r/sigma,Rahman reference g(r),Reference provenance,Comment"
    ]
    for row in rows_a:
        csv_lines.append(
            f"A,{row['Integrator']},{row['Production steps']},{row['Mean T [K]']},{row['Std T [K]']},"
            f"{row['Max |ΔE/E0| [%]']},{row['Mean |ΔE/E0| [%]']},,,,,,{row['Comment']}"
        )
    for row in rows_b:
        csv_lines.append(
            f"B,{row['Feature']},,,,,,{row['Present work r/sigma']},{row['Present work g(r)']},"
            f"{row['Rahman reference r/sigma']},{row['Rahman reference g(r)']},"
            f"{row['Reference provenance']},{row['Comment']}"
        )
    write_text_file(RESULTS2_TABLE_CSV, "\n".join(csv_lines))

    write_json_file(
        RESULTS2_TABLE_JSON,
        {
            "generated_utc": utc_now(),
            "section_a_required_run": rows_a,
            "section_b_rdf_comparison": rows_b,
            "sources": {
                "energy_temperature_summary": "out/plots/metadata/results2_lj_brief_energy_100step_production.json + out/plots/metadata/results2_lj_brief_temperature_100step_production.json",
                "rdf_summary": "out/plots/metadata/results2_lj_rdf_comparison_rahman1964.json",
            },
        },
    )

    return {
        "markdown": RESULTS2_TABLE_MD,
        "csv": RESULTS2_TABLE_CSV,
        "json": RESULTS2_TABLE_JSON,
        "rows_a": rows_a,
        "rows_b": rows_b,
    }


def write_results2_notes():
    write_text_file(
        RESULTS2_REPORT_NOTE,
        """# Results 2 Report Note

The Lennard-Jones Argon test case follows the Rahman-style state point at 94.4 K with N=864 atoms in a periodic box, using dt = 1e-14 s.

For the brief-required production run (100 steps, 1 ps), startup/equilibration is performed first, then a final startup->production temperature rescale is applied before production. In the saved production CSV, step 0 is the production initial frame (n_frames = 101).

Across this required production window, Velocity-Verlet remains near the target state and shows small bounded energy drift. Forward Euler shows strong energy drift and substantial temperature growth over the same window, so it is not suitable for a stable NVE Argon trajectory here.

For structure, the Velocity-Verlet RDF from a longer production run reproduces the expected liquid-argon shell pattern (first peak, first minimum, second shell, and long-range return toward g(r)=1), with broad agreement to Rahman (1964).

The Rahman comparison is based on a manually extracted approximate guide from Rahman Fig. 2. Sigma = 3.4 Å is paper-supported; the x-positions 3.7 Å, 7.0 Å, and 10.4 Å are directly anchored to annotated figure positions; remaining points are approximate shape anchors read from the printed curve.

This comparison should be stated as qualitative / semi-quantitative rather than exact, especially for peak heights (present-work peaks are somewhat reduced).
""",
    )

    write_text_file(
        RESULTS2_RECOMMENDED_FIGURES,
        """# Recommended Final Results 2 Figure Set

Main report figures (core evidence, in order):
1. `out/plots/results2_lj_brief_energy_100step_production.png`
2. `out/plots/results2_lj_brief_temperature_100step_production.png`
3. `out/plots/results2_lj_rdf_comparison_rahman1964.png`
4. `out/summary/results2/results2_quantitative_summary_table.md` (compact quantitative table)
Rationale: this set directly answers the brief-required 100-step Verlet-vs-Euler comparison and Rahman structural comparison with no extra non-deliverable figures.
""",
    )

    write_text_file(
        RESULTS2_RAHMAN_EXTRACTION_NOTE,
        """# Rahman Data Extraction Note (Fig. 2)

Reference file: `scripts/data/rahman1964_fig2_manual_anchors.csv` (copied to `out/summary/results2/rahman1964_fig2_manual_anchors.csv` during plotting).

Exactly paper-supported elements used:
- sigma = 3.4 Å (used for the top-axis conversion and r/sigma conversion)
- Fig. 2 annotated x-positions at 3.7 Å, 7.0 Å, and 10.4 Å

Approximate elements (manual extraction from printed curve):
- all Rahman g(r) values
- all non-annotated x positions used as shape anchors

Interpretation rule:
- this anchor set is a transparent visual guide only; it is not exact tabulated truth and should not be over-interpreted.
""",
    )

    write_text_file(
        RESULTS2_CHANGE_NOTE,
        """# Results 2: What Changed and Why

1. Removed extended 600-step Results 2 figures from the active workflow and report package.
2. Kept only the three brief-facing Results 2 figures plus a compact quantitative table.
3. Replaced old sparse hard-coded Rahman points with a transparent 9-point two-tier anchor dataset (paper_anchored + shape_anchor) stored in machine-readable CSV.
4. Updated RDF figure and metadata to make provenance explicit and to avoid implying exact Rahman tabulated data.
5. Tightened required-run energy/temperature metadata to explicitly state startup/equilibration, final rescale, and step-0 production semantics.
6. Added automatic Results 2 quantitative summary table generation (Markdown + CSV + JSON).
7. Added report-ready claim-safe notes and explicit final Results 2 figure ordering.
""",
    )


def summarize_results2_outputs(energy_brief, temp_brief, rdf_summary, table_files):
    main_figures = [
        f"{PLOT_DIR}/results2_lj_brief_energy_100step_production.png",
        f"{PLOT_DIR}/results2_lj_brief_temperature_100step_production.png",
        f"{PLOT_DIR}/results2_lj_rdf_comparison_rahman1964.png",
    ]
    update_manifest_with_results2_outputs(
        {
            "generated_utc": utc_now(),
            "main_report_figures": main_figures,
            "main_report_tables": [table_files["markdown"], table_files["csv"], table_files["json"]],
            "rahman_reference_dataset": RAHMAN_OUT_FILE if os.path.exists(RAHMAN_OUT_FILE) else RAHMAN_SOURCE_FILE,
            "notes": [
                RESULTS2_REPORT_NOTE,
                RESULTS2_RECOMMENDED_FIGURES,
                RESULTS2_RAHMAN_EXTRACTION_NOTE,
                RESULTS2_CHANGE_NOTE,
            ],
            "plot_metadata_files": [
                energy_brief.get("metadata_file") if energy_brief else None,
                temp_brief.get("metadata_file") if temp_brief else None,
                rdf_summary.get("metadata_file") if rdf_summary else None,
            ],
        }
    )


def main():
    apply_plot_style()
    manifest = load_manifest()
    os.makedirs(SUMMARY_DIR, exist_ok=True)
    remove_stale_results2_extended_artifacts()
    rahman_points = load_rahman_anchor_points(RAHMAN_SOURCE_FILE)
    sync_rahman_anchor_dataset(RAHMAN_SOURCE_FILE, RAHMAN_OUT_FILE)

    brief_cfg = {
        "integrators": [
            {"series_key": "verlet", "label": "Velocity-Verlet", "style_key": "verlet"},
            {"series_key": "euler", "label": "Forward Euler", "style_key": "euler"},
        ],
        "energy_title": "Argon LJ Required Run (100 Steps, 1 ps): Energy Stability",
        "temperature_title": "Argon LJ Required Run (100 Steps, 1 ps): Temperature",
        "energy_purpose": (
            "Core brief-facing evidence for the required 100-step production run: "
            "Velocity-Verlet remains bounded while Forward Euler drifts strongly."
        ),
        "energy_claim": (
            "At the required run length, Velocity-Verlet gives a physically meaningful bounded "
            "NVE trajectory; Forward Euler shows strong drift and is unreliable."
        ),
        "temperature_purpose": (
            "Core brief-facing evidence for the required 100-step production run temperature response."
        ),
        "temperature_claim": (
            "Velocity-Verlet remains close to the target state while Forward Euler heats strongly "
            "over the same required window."
        ),
        "audience_tier": "main-report-core",
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
        "results2_lj_brief_energy_100step_production.png",
    )
    brief_temperature = safe_plot(
        "brief temperature",
        plot_temperature_for_run,
        manifest,
        "lj_brief",
        brief_cfg,
        "results2_lj_brief_temperature_100step_production.png",
    )

    rdf_summary = safe_plot("rdf", plot_rdf, manifest, rahman_points)

    table_files = write_results2_quantitative_summary(brief_energy, brief_temperature, rdf_summary)
    write_results2_notes()
    summarize_results2_outputs(
        brief_energy,
        brief_temperature,
        rdf_summary,
        table_files,
    )


if __name__ == "__main__":
    main()
