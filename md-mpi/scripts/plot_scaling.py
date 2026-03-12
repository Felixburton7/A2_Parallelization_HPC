#!/usr/bin/env python3
"""
plot_scaling.py — Generate scaling analysis plots (Results 3).

Produces:
  1. Strong scaling: Speedup S(P) with Amdahl's Law fit
  2. Efficiency E(P) = S(P)/P
  3. Stacked bar chart: Critical-path communication vs remaining runtime
  4. Size scaling: Wall time vs N with O(N²) reference

Usage:
  python3 scripts/plot_scaling.py

Prerequisites (from manifest.json):
  scaling.strong -> out/scaling_strong.csv  (columns: P,N,wall_s,comm_max_s)
  scaling.size   -> out/scaling_size.csv    (columns: P,N,wall_s,comm_max_s)
"""

import os
import json
import glob
from datetime import datetime, timezone
import numpy as np
import matplotlib.pyplot as plt

from plot_style import (
    COLOR_EULER,
    COLOR_REFERENCE,
    COLOR_RK4,
    COLOR_VERLET,
    apply_major_grid,
    apply_plot_style,
    disable_offset_text,
    save_figure,
)

PLOT_DIR = "out/plots"
PLOT_META_DIR = "out/plots/metadata"
FIG9_AB_PNG = "results3_figure9ab.png"
FIG10_ABC_PNG = "results3_figure10abc.png"
RESULTS3_INTEGRATOR = "verlet"
RESULTS3_TIMESTEP_S = 1.0e-14
RESULTS3_SEED = 42
RESULTS3_REPETITIONS = 11
RESULTS3_STRONG_FIXED_N = 2048
RESULTS3_STRONG_TIMED_STEPS = 2000
RESULTS3_SIZE_FIXED_P = 16
RESULTS3_SIZE_TIMED_STEPS = 2000
RESULTS3_PROTOCOL_SOURCE = "scripts/run_all_data.sh"
STALE_RESULTS3_PATTERNS = [
    # Legacy pre-results3 naming pattern; no longer part of report outputs.
    f"{PLOT_DIR}/scaling_*.png",
]


def load_manifest():
    manifest_path = "out/manifest.json"
    if not os.path.exists(manifest_path):
        print(f"Warning: manifest not found at {manifest_path}")
        return {}
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


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


def results3_protocol(kind):
    protocol = {
        "integrator": RESULTS3_INTEGRATOR,
        "timestep_s": RESULTS3_TIMESTEP_S,
        "seed": RESULTS3_SEED,
        "repetitions_per_configuration": RESULTS3_REPETITIONS,
        "output_mode": "timing mode with file output disabled",
        "aggregation": "median paired (wall_s, comm_max_s) sample",
        "protocol_source": RESULTS3_PROTOCOL_SOURCE,
        "separation_from_results2": (
            "Results 3 timing benchmarks are separate from the Results 2 brief-mandated 100-step argon validation run."
        ),
        "reporting_convention": (
            "Reported times are raw measured wall-clock seconds from the benchmark windows; no per-100-step normalization is applied."
        ),
    }
    if kind == "strong":
        protocol.update(
            {
                "benchmark_type": "strong_scaling",
                "fixed_particle_count_N": RESULTS3_STRONG_FIXED_N,
                "timed_steps": RESULTS3_STRONG_TIMED_STEPS,
                "design_rationale": (
                    "Use a longer timing window at fixed N=2048 to reduce measurement noise while keeping the single-rank baseline tractable."
                ),
            }
        )
    elif kind == "size":
        protocol.update(
            {
                "benchmark_type": "size_scaling",
                "fixed_process_count_P": RESULTS3_SIZE_FIXED_P,
                "timed_steps": RESULTS3_SIZE_TIMED_STEPS,
                "design_rationale": (
                    "Use a longer timing window at small N so fixed overhead and timer granularity contaminate the size-scaling trend less strongly."
                ),
            }
        )
    else:
        raise ValueError(f"Unknown Results 3 protocol kind: {kind}")
    return protocol


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


def set_panel_title(ax, title: str):
    # Keep panel titles aligned with panel labels and slightly lifted from the plot area.
    ax.set_title(title, loc="left", y=1.05, pad=3)


def remove_stale_results3_artifacts():
    for pattern in STALE_RESULTS3_PATTERNS:
        for path in glob.glob(pattern):
            os.remove(path)
            print(f"Removed stale artifact {path}")


def load_scaling_csv(manifest, key):
    path = manifest.get("scaling", {}).get(key, "")
    if not os.path.exists(path):
        return None, path, False
    data = np.genfromtxt(path, delimiter=',', names=True, encoding=None)
    names = getattr(getattr(data, "dtype", None), "names", None)
    if names and "P" in names and "wall_s" in names:
        return data, path, False

    # Fallback: tolerate headerless CSVs ("P,N,wall_s,comm_max_s" missing).
    raw = np.genfromtxt(path, delimiter=',', encoding=None)
    if raw is None:
        return None, path, False
    if raw.ndim == 1:
        raw = np.array([raw])
    if raw.shape[1] < 4:
        return None, path, False
    out = np.zeros(raw.shape[0], dtype=[("P", float), ("N", float), ("wall_s", float), ("comm_max_s", float)])
    out["P"] = raw[:, 0]
    out["N"] = raw[:, 1]
    out["wall_s"] = raw[:, 2]
    out["comm_max_s"] = raw[:, 3]
    print(f"Warning: {path} missing header; parsed as 4-column numeric fallback.")
    return out, path, True


def amdahl(P, f):
    """Amdahl's Law: S(P) = 1 / (f + (1-f)/P)."""
    return 1.0 / (f + (1.0 - f) / P)


def plot_strong_scaling():
    """Plot speedup, efficiency, and critical-path comm breakdown."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    manifest = load_manifest()
    data, strong_path, used_fallback = load_scaling_csv(manifest, "strong")
    if data is None:
        print("Warning: scaling/strong not found in manifest. Skipping strong scaling.")
        return

    names = getattr(getattr(data, "dtype", None), "names", ()) or ()
    has_n_column = "N" in names

    P = data['P'].astype(int)
    wall = data['wall_s']
    comm_col = "comm_max_s" if "comm_max_s" in names else "comm_s"
    comm_max = data[comm_col]
    compute_overhead = np.maximum(wall - comm_max, 0.0)
    # Some exported strong-scaling tables omit N; Results 3 strong scaling uses fixed N=2048.
    N_values = data["N"].astype(int) if has_n_column else np.full(len(P), 2048, dtype=int)

    t1 = wall[0]
    speedup = t1 / wall
    efficiency = speedup / P

    # Fit Amdahl's Law using pure NumPy two-pass grid search
    def fit_amdahl(P_arr, S_obs):
        """Fit Amdahl serial fraction f by minimising SSE in S-space.
        Two-pass grid search: coarse (1e-3 resolution) then refined (1e-5).
        Uses pure NumPy — no SciPy dependency, for cluster portability."""
        best_f, best_sse = 0.0, 1e30
        # Coarse pass
        for f_trial in np.linspace(0.001, 0.999, 1000):
            S_model = 1.0 / (f_trial + (1.0 - f_trial) / P_arr)
            sse = np.sum((S_obs - S_model) ** 2)
            if sse < best_sse:
                best_f, best_sse = f_trial, sse
        # Refined pass around coarse optimum
        lo = max(0.0001, best_f - 0.002)
        hi = min(0.9999, best_f + 0.002)
        for f_trial in np.linspace(lo, hi, 10000):
            S_model = 1.0 / (f_trial + (1.0 - f_trial) / P_arr)
            sse = np.sum((S_obs - S_model) ** 2)
            if sse < best_sse:
                best_f, best_sse = f_trial, sse
        return best_f

    P_data = P[P > 1].astype(float)
    S_data = speedup[P > 1]
    f_fit = fit_amdahl(P_data, S_data) if len(P_data) > 0 else None

    if f_fit is not None:
        P_fit = np.linspace(1, max(P) * 1.1, 100)
        S_fit = amdahl(P_fit, f_fit)
    
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.8), constrained_layout=True)

    # --- Panel 1: Speedup ---
    ax1 = axes[0]
    ax1.plot(P, speedup, "o-", color=COLOR_VERLET, linewidth=2.0, markersize=6, label="Measured")
    ax1.plot(P, P.astype(float), "--", color=COLOR_REFERENCE, alpha=0.9, linewidth=1.5, label="Ideal (S=P)")
    if f_fit is not None:
        ax1.plot(P_fit, S_fit, "-", color=COLOR_EULER, linewidth=1.6, label=f"Amdahl fit (f={f_fit:.4f})")
    ax1.set_xlabel("Number of Processes P")
    ax1.set_ylabel("Speedup S(P)")
    set_panel_title(ax1, "Strong Scaling: Speedup")
    add_panel_label(ax1, "a")
    ax1.legend(loc="best")
    apply_major_grid(ax1)
    disable_offset_text(ax1)

    # --- Panel 2: Efficiency ---
    ax2 = axes[1]
    ax2.plot(P, efficiency, "o-", color=COLOR_RK4, linewidth=2.0, markersize=6, label="Measured efficiency")
    ax2.axhline(y=1.0, color=COLOR_REFERENCE, linestyle="--", alpha=0.9, linewidth=1.3, label="Ideal (E=1)")
    ax2.set_xlabel("Number of Processes P")
    ax2.set_ylabel("Efficiency E(P) = S(P)/P")
    set_panel_title(ax2, "Strong Scaling: Efficiency")
    add_panel_label(ax2, "b")
    ax2.set_ylim(0, 1.15)
    ax2.legend(loc="best")
    apply_major_grid(ax2)
    disable_offset_text(ax2)

    # --- Panel 3: Stacked bar — Remaining runtime vs critical-path communication ---
    ax3 = axes[2]
    x_pos = np.arange(len(P))
    bar_width = 0.6
    remaining_display = np.maximum(compute_overhead, 0.0)
    ax3.bar(
        x_pos,
        remaining_display,
        bar_width,
        label="Remaining runtime (wall - comm_max)",
        color=COLOR_VERLET,
        alpha=0.85,
    )
    ax3.bar(
        x_pos,
        comm_max,
        bar_width,
        bottom=remaining_display,
        label="Communication (critical-path max)",
        color=COLOR_EULER,
        alpha=0.85,
    )
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([str(p) for p in P])
    ax3.set_xlabel("Number of Processes P")
    ax3.set_ylabel("Wall Time [s]")
    set_panel_title(ax3, "Critical-Path Communication vs Remaining Runtime")
    add_panel_label(ax3, "c")
    ax3.legend(loc="best")
    apply_major_grid(ax3, axis="y")
    disable_offset_text(ax3)

    save_figure(fig, f"{PLOT_DIR}/{FIG10_ABC_PNG}")
    plt.close()
    print(f"Saved {PLOT_DIR}/{FIG10_ABC_PNG}")

    scaling_meta_path = "out/scaling_meta.txt"
    source_data_files = [strong_path]
    if os.path.exists(scaling_meta_path):
        source_data_files.append(scaling_meta_path)

    missing_provenance = [
        "Raw per-repetition timing samples are not retained in manifest-linked files; only medians are available in scaling_strong.csv.",
    ]
    if used_fallback:
        missing_provenance.append("CSV header provenance missing; file required fallback parsing.")
    if not has_n_column:
        missing_provenance.append("Strong-scaling CSV omitted N column; metadata assumes fixed N=2048.")
    if not os.path.exists(scaling_meta_path):
        missing_provenance.append("Hardware/environment snapshot out/scaling_meta.txt was not found.")

    f_fit_value = float(f_fit) if f_fit is not None else None
    max_theoretical_speedup = float(1.0 / f_fit) if f_fit is not None and f_fit > 0 else None
    max_measured_speedup = float(np.nanmax(speedup)) if speedup.size else None
    min_efficiency = float(np.nanmin(efficiency)) if efficiency.size else None
    max_efficiency = float(np.nanmax(efficiency)) if efficiency.size else None

    rows = []
    for i in range(len(P)):
        rows.append(
            {
                "P": int(P[i]),
                "N": int(N_values[i]),
                "wall_s": float(wall[i]),
                "comm_max_s": float(comm_max[i]),
                "remaining_runtime_s": float(compute_overhead[i]),
                "speedup": float(speedup[i]),
                "efficiency": float(efficiency[i]),
            }
        )

    write_plot_metadata(
        FIG10_ABC_PNG,
        "results3",
        {
            "figure_number": 10,
            "panels": ["a)", "b)", "c)"],
            "purpose": "Main Results 3 figure for strong scaling: show measured speedup/efficiency and a bottleneck-consistent communication breakdown.",
            "intended_claim": "The MPI implementation achieves strong-scaling gains while critical-path communication (max rank communication time) contributes a measurable share of runtime.",
            "audience_tier": "brief-facing",
            "source_data_files": unique_preserve_order(source_data_files),
            "source_manifest_keys": ["scaling.strong"],
            "simulation_run_identifiers": [],
            "benchmark_protocol": results3_protocol("strong"),
            "key_parameters": {
                "integrator": RESULTS3_INTEGRATOR,
                "fixed_particle_count_N": int(N_values[0]) if len(data) else None,
                "process_counts_P": [int(p) for p in P.tolist()],
                "timed_steps": RESULTS3_STRONG_TIMED_STEPS,
                "repetitions_per_configuration": RESULTS3_REPETITIONS,
                "seed": RESULTS3_SEED,
                "timestep_s": RESULTS3_TIMESTEP_S,
                "plots_in_figure": [
                    "speedup",
                    "efficiency",
                    "critical_path_communication_vs_remaining_runtime",
                ],
            },
            "fit_or_truncation": {
                "amdahl_fit_model": "S(P)=1/(f+(1-f)/P)",
                "amdahl_fit_domain": "P > 1",
                "excluded_points_from_amdahl_fit": [1] if np.any(P == 1) else [],
                "fit_method": "two-pass grid search in f (coarse 1e-3 then refined 1e-5 step over local window)",
            },
            "key_quantitative_summary": {
                "amdahl_serial_fraction_f": f_fit_value,
                "maximum_theoretical_speedup_from_fit": max_theoretical_speedup,
                "max_measured_speedup": max_measured_speedup,
                "efficiency_range": [min_efficiency, max_efficiency],
                "rows": rows,
            },
            "caveats": [
                "Strong-scaling data are aggregated medians, not raw replicate traces.",
                "Communication timing is solver-reported MPI_Allgatherv timing and may include measurement noise at small runtimes.",
                "Remaining runtime is defined as wall time minus critical-path communication and is not pure physical-force compute time.",
            ],
            "missing_provenance": missing_provenance,
        },
    )

    if f_fit is not None:
        print(f"  Amdahl serial fraction f = {f_fit:.6f}")
        print(f"  Maximum theoretical speedup = {1.0/f_fit:.1f}x")


def plot_size_scaling():
    """Plot wall time and wall-minus-comm_max runtime vs N."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    manifest = load_manifest()
    data, size_path, used_fallback = load_scaling_csv(manifest, "size")
    if data is None:
        print("Warning: scaling/size not found in manifest. Skipping size scaling.")
        return
    names = getattr(getattr(data, "dtype", None), "names", ()) or ()
    if "N" not in names:
        print("Warning: scaling/size is missing N column. Skipping size scaling plot.")
        return

    N = data['N']
    wall = data['wall_s']
    comm_col = "comm_max_s" if "comm_max_s" in names else "comm_s"
    comm_max = data[comm_col]
    remaining_runtime = np.maximum(wall - comm_max, 1e-9)  # floor to avoid log(0)

    # Fit power law to wall-minus-comm_max runtime for N >= 500
    mask = N >= 500
    slope_remaining, intercept_remaining = None, None
    slope_wall, intercept_wall = None, None
    if np.sum(mask) >= 2:
        log_N = np.log10(N[mask])
        log_remaining = np.log10(np.maximum(remaining_runtime[mask], 1e-10))
        slope_remaining, intercept_remaining = np.polyfit(log_N, log_remaining, 1)
        
        log_wall = np.log10(wall[mask])
        slope_wall, intercept_wall = np.polyfit(log_N, log_wall, 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 4.8), constrained_layout=True)

    wall_label = 'Wall time'
    if slope_wall is not None:
        wall_label += f' (O(N^{slope_wall:.2f}))'
    ax1.loglog(N, wall, "o-", color=COLOR_VERLET, linewidth=2.0, markersize=6, label=wall_label)
    
    rem_label = 'Remaining runtime (wall - comm_max)'
    if slope_remaining is not None:
        rem_label += f' (O(N^{slope_remaining:.2f}))'
    ax1.loglog(N, remaining_runtime, "^-", color=COLOR_RK4, linewidth=2.0, markersize=6, label=rem_label)

    ax1.loglog(
        N,
        comm_max,
        "s--",
        color=COLOR_EULER,
        linewidth=1.5,
        markersize=5,
        label="Comm time (max)",
        alpha=0.9,
    )
    N_ref = np.array([min(N), max(N)])
    t_ref = wall[-1] * (N_ref / N[-1]) ** 2
    ax1.loglog(N_ref, t_ref, "--", color=COLOR_REFERENCE, alpha=0.9, linewidth=1.5, label=r"$\sim N^2$ reference")
    ax1.set_xlabel("Number of Particles N")
    ax1.set_ylabel("Time [s]")
    set_panel_title(ax1, "Size Scaling (P=16)")
    add_panel_label(ax1, "a")
    ax1.legend(loc="best")
    apply_major_grid(ax1)

    comm_frac = comm_max / wall * 100
    ax2.plot(N, comm_frac, "o-", color=COLOR_EULER, linewidth=2.0, markersize=6)
    ax2.set_xlabel("Number of Particles N")
    ax2.set_ylabel("Communication Fraction [%]")
    set_panel_title(ax2, "Communication Overhead vs Problem Size")
    add_panel_label(ax2, "b")
    ax2.set_ylim(0, 100)
    apply_major_grid(ax2)
    ax2.axhline(y=50, color=COLOR_REFERENCE, linestyle="--", linewidth=1.2, label="50% reference")
    ax2.legend(loc="best")
    disable_offset_text(ax2)

    save_figure(fig, f"{PLOT_DIR}/{FIG9_AB_PNG}")
    plt.close()
    print(f"Saved {PLOT_DIR}/{FIG9_AB_PNG}")

    scaling_meta_path = "out/scaling_meta.txt"
    source_data_files = [size_path]
    if os.path.exists(scaling_meta_path):
        source_data_files.append(scaling_meta_path)

    missing_provenance = [
        "Raw per-repetition timing samples are not retained in manifest-linked files; only medians are available in scaling_size.csv.",
    ]
    if used_fallback:
        missing_provenance.append("CSV header provenance missing; file required fallback parsing.")
    if not os.path.exists(scaling_meta_path):
        missing_provenance.append("Hardware/environment snapshot out/scaling_meta.txt was not found.")

    comm_frac_min = float(np.nanmin(comm_frac)) if comm_frac.size else None
    comm_frac_max = float(np.nanmax(comm_frac)) if comm_frac.size else None
    rows = []
    for i in range(len(N)):
        rows.append(
            {
                "N": int(N[i]),
                "P": int(data["P"][i]),
                "wall_s": float(wall[i]),
                "comm_max_s": float(comm_max[i]),
                "remaining_runtime_s": float(remaining_runtime[i]),
                "communication_fraction_percent": float(comm_frac[i]),
            }
        )

    write_plot_metadata(
        FIG9_AB_PNG,
        "results3",
        {
            "figure_number": 9,
            "panels": ["a)", "b)"],
            "purpose": "Main Results 3 figure for problem-size scaling at fixed process count.",
            "intended_claim": "Runtime grows approximately as a power law near O(N^2) while communication fraction changes with size at fixed P=16.",
            "audience_tier": "brief-facing",
            "source_data_files": unique_preserve_order(source_data_files),
            "source_manifest_keys": ["scaling.size"],
            "simulation_run_identifiers": [],
            "benchmark_protocol": results3_protocol("size"),
            "key_parameters": {
                "integrator": RESULTS3_INTEGRATOR,
                "fixed_process_count_P": int(data["P"][0]) if len(data) else None,
                "particle_counts_N": [int(n) for n in N.tolist()],
                "timed_steps": RESULTS3_SIZE_TIMED_STEPS,
                "repetitions_per_configuration": RESULTS3_REPETITIONS,
                "seed": RESULTS3_SEED,
                "timestep_s": RESULTS3_TIMESTEP_S,
                "fit_mask_for_power_law": "N >= 500",
                "reference_curve": "~N^2 anchored to largest-N wall time",
            },
            "fit_or_truncation": {
                "power_law_fit_domain": [int(n) for n in N[mask].tolist()],
                "excluded_from_power_law_fit": [int(n) for n in N[~mask].tolist()],
                "fit_method": "linear regression in log10-space on selected N values",
            },
            "key_quantitative_summary": {
                "wall_time_power_law_exponent": float(slope_wall) if slope_wall is not None else None,
                "remaining_runtime_power_law_exponent": (
                    float(slope_remaining) if slope_remaining is not None else None
                ),
                "communication_fraction_percent_range": [comm_frac_min, comm_frac_max],
                "rows": rows,
            },
            "caveats": [
                "Power-law exponents depend on the chosen fit domain (here N >= 500).",
                "Communication fraction uses max rank communication timing from solver output, not network-level profiling counters.",
                "O(...) expressions in the legend are empirical power-law fits over the tested range, not rigorous statements of asymptotic complexity.",
            ],
            "missing_provenance": missing_provenance,
        },
    )


if __name__ == "__main__":
    apply_plot_style()
    remove_stale_results3_artifacts()
    plot_strong_scaling()
    plot_size_scaling()
