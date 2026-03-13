#!/usr/bin/env python3
"""
Emit report-writing-focused Markdown context for ai/results.md.

This is intentionally different from analyse_results.py:
- analyse_results.py is a broad reproducibility and evidence summary
- this script is a targeted "write the Results section from this" pack
"""

from __future__ import annotations

import csv
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_json(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def load_csv_rows(path: str) -> List[Dict[str, str]]:
    p = Path(path)
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(rows: List[Dict[str, str]], key: str, value: str) -> Dict[str, str]:
    for row in rows:
        if (row.get(key) or "").strip() == value:
            return row
    return {}


def find_row_float(rows: List[Dict[str, str]], key: str, value: float, tol: float = 1e-12) -> Dict[str, str]:
    for row in rows:
        try:
            row_value = float(row.get(key, "nan"))
        except ValueError:
            continue
        if abs(row_value - value) <= tol:
            return row
    return {}


def maybe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        if math.isfinite(float(value)):
            return float(value)
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        parsed = float(text)
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


def fmt_num(value: Any, digits: int = 3) -> str:
    parsed = maybe_float(value)
    if parsed is None:
        return "n/a"
    if parsed == 0.0:
        return "0"
    abs_value = abs(parsed)
    if abs_value >= 1000 or abs_value < 1e-3:
        return f"{parsed:.{digits}e}"
    return f"{parsed:.{digits}f}"


def fmt_pct(value: Any, digits: int = 3) -> str:
    parsed = maybe_float(value)
    if parsed is None:
        return "n/a"
    return f"{parsed:.{digits}f}%"


def fmt_ratio_as_pct(value: Any, digits: int = 3) -> str:
    parsed = maybe_float(value)
    if parsed is None:
        return "n/a"
    return f"{100.0 * parsed:.{digits}f}%"


def per_integrator(meta: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for row in meta.get("key_quantitative_summary", {}).get("per_integrator", []):
        integrator = str(row.get("integrator", "")).strip()
        if integrator:
            out[integrator] = row
    return out


def load_manifest() -> Dict[str, Any]:
    return load_json("out/manifest.json")


def ho_smallest_rk4_error(manifest: Dict[str, Any]) -> Dict[str, Optional[float]]:
    x_exact = math.cos(10.0)
    best_dt: Optional[float] = None
    best_err: Optional[float] = None

    for key, path in manifest.get("ho_convergence", {}).items():
        if not str(key).startswith("rk4_dt"):
            continue
        try:
            dt = float(str(key).split("_dt", 1)[1].replace("_", "."))
        except ValueError:
            continue
        csv_path = Path(path)
        if not csv_path.exists():
            continue
        with csv_path.open("r", encoding="utf-8", errors="ignore") as handle:
            lines = [line for line in handle if line.strip() and not line.startswith("#")]
        if not lines:
            continue
        rows = list(csv.DictReader(lines))
        if not rows:
            continue
        x_final = maybe_float(rows[-1].get("x"))
        if x_final is None:
            continue
        err = abs(x_final - x_exact)
        if best_dt is None or dt < best_dt:
            best_dt = dt
            best_err = err

    return {"dt": best_dt, "error": best_err}


def parse_run_all_data_config() -> Dict[str, Optional[int]]:
    path = Path("scripts/run_all_data.sh")
    if not path.exists():
        return {
            "strong_steps": None,
            "size_steps": None,
            "brief_steps": None,
            "rdf_steps": None,
            "reps": None,
        }
    text = path.read_text(encoding="utf-8", errors="ignore")

    def extract(name: str) -> Optional[int]:
        match = re.search(rf"^{name}=(\d+)", text, flags=re.MULTILINE)
        return int(match.group(1)) if match else None

    return {
        "strong_steps": extract("STRONG_STEPS"),
        "size_steps": extract("SIZE_STEPS"),
        "brief_steps": extract("LJ_BRIEF_PROD_STEPS"),
        "rdf_steps": extract("LJ_RDF_PROD_STEPS"),
        "reps": extract("REPS"),
    }


def print_heading(title: str) -> None:
    print(title)
    print("")


def emit_structure_plan(config: Dict[str, Optional[int]]) -> None:
    print_heading("### Writeup-Aligned Structure")
    print("1. Results 1 - Harmonic oscillator verification.")
    print("   - Use Fig. 1 for the qualitative distinction between trajectory overlap and phase-space geometry at dt=0.01.")
    print("   - Use Fig. 2 as the timestep-sensitivity contrast, Fig. 3 plus the convergence table for formal order, and Fig. 4 as supporting energy evidence rather than the primary proof.")
    print("2. Results 2 - Lennard-Jones argon.")
    print("   - Keep the required 100-step production run (energy and temperature) separate from the 20,000-step RDF validation run.")
    print("   - Say explicitly that step 0 in the CSV is the production initial frame after startup/equilibration.")
    print("3. Results 3 - scaling.")
    if config["strong_steps"] and config["size_steps"]:
        reps_text = f", using {config['reps']} repetitions per point" if config["reps"] else ""
        print(
            f"   - State the actual timing configuration used for the current dataset: "
            f"strong scaling uses {config['strong_steps']} timed steps and size scaling uses {config['size_steps']} timed steps{reps_text}."
        )
        print("   - That configuration comes from `scripts/run_all_data.sh`; it is not encoded in the scaling CSV headers.")
    else:
        print("   - State the actual timing configuration used for the current dataset from `scripts/run_all_data.sh`, because the scaling CSVs do not encode it.")
    print("")


def emit_quantitative_anchors(
    manifest: Dict[str, Any],
    results1_conv: List[Dict[str, str]],
    results1_small_large: List[Dict[str, str]],
    meta6: Dict[str, Any],
    meta7: Dict[str, Any],
    meta8: Dict[str, Any],
    meta9: Dict[str, Any],
    meta10: Dict[str, Any],
    config: Dict[str, Optional[int]],
) -> None:
    print_heading("### Report-Ready Quantitative Anchors")

    euler_conv = find_row(results1_conv, "integrator", "euler")
    verlet_conv = find_row(results1_conv, "integrator", "verlet")
    rk4_conv = find_row(results1_conv, "integrator", "rk4")
    euler_small = find_row_float(results1_small_large, "dt", 0.01)
    euler_small = euler_small if euler_small.get("integrator") == "euler" else find_row(
        [row for row in results1_small_large if row.get("integrator") == "euler"], "dt", "0.01"
    )
    verlet_small = find_row(
        [row for row in results1_small_large if row.get("integrator") == "verlet"], "dt", "0.01"
    )
    rk4_small = find_row(
        [row for row in results1_small_large if row.get("integrator") == "rk4"], "dt", "0.01"
    )
    rk4_floor = ho_smallest_rk4_error(manifest)

    print("#### Results 1 - Harmonic oscillator")
    print(
        "- Convergence slopes from the Results 1 summary: "
        f"Euler {fmt_num(euler_conv.get('endpoint_position_slope'), 2)}, "
        f"Velocity-Verlet {fmt_num(verlet_conv.get('endpoint_position_slope'), 2)}, "
        f"RK4 {fmt_num(rk4_conv.get('endpoint_position_slope'), 2)} for endpoint error; "
        f"Euler {fmt_num(euler_conv.get('rms_phase_space_slope'), 2)}, "
        f"Velocity-Verlet {fmt_num(verlet_conv.get('rms_phase_space_slope'), 2)}, "
        f"RK4 {fmt_num(rk4_conv.get('rms_phase_space_slope'), 2)} for RMS phase-space error."
    )
    print(
        "- Representative endpoint position error at dt=0.01: "
        f"Euler {fmt_num(euler_small.get('endpoint_position_error'), 3)}, "
        f"Velocity-Verlet {fmt_num(verlet_small.get('endpoint_position_error'), 3)}, "
        f"RK4 {fmt_num(rk4_small.get('endpoint_position_error'), 3)}."
    )
    print(
        "- Energy drift at dt=0.01 from the small-vs-large summary: "
        f"Euler max |dE/E0| = {fmt_ratio_as_pct(euler_small.get('max_relative_energy_drift'), 3)}, "
        f"Velocity-Verlet = {fmt_ratio_as_pct(verlet_small.get('max_relative_energy_drift'), 5)}, "
        f"RK4 = {fmt_ratio_as_pct(rk4_small.get('max_relative_energy_drift'), 6)}."
    )
    print(
        "- Smallest RK4 endpoint error currently tabulated is "
        f"{fmt_num(rk4_floor.get('error'), 3)} at dt={fmt_num(rk4_floor.get('dt'), 4)}, "
        "which supports the machine-precision-floor discussion."
    )
    print("")

    energy_by_int = per_integrator(meta6)
    temp_by_int = per_integrator(meta7)
    rdf_q = meta8.get("key_quantitative_summary", {})

    vv_energy = energy_by_int.get("verlet", {})
    eu_energy = energy_by_int.get("euler", {})
    vv_temp = temp_by_int.get("verlet", {})
    eu_temp = temp_by_int.get("euler", {})
    run_semantics = meta6.get("key_parameters", {}).get("run_semantics", {})

    print("#### Results 2 - Lennard-Jones argon")
    print(
        "- Required-run semantics from the figure metadata: "
        f"{run_semantics.get('required_production_steps', 'n/a')} production steps, "
        f"{run_semantics.get('required_production_time_ps', 'n/a')} ps, "
        "startup/equilibration completed before production, and step 0 is the production initial frame."
    )
    print(
        "- Required-run energy comparison: "
        f"Velocity-Verlet max |dE/E0| = {fmt_pct(vv_energy.get('max_abs_relative_energy_deviation_percent'), 3)} "
        f"(mean {fmt_pct(vv_energy.get('mean_abs_relative_energy_deviation_percent'), 3)}; "
        f"final {fmt_pct(vv_energy.get('final_relative_energy_deviation_percent'), 3)}), "
        f"while Euler reaches {fmt_pct(eu_energy.get('max_abs_relative_energy_deviation_percent'), 3)} "
        f"(mean {fmt_pct(eu_energy.get('mean_abs_relative_energy_deviation_percent'), 3)})."
    )
    print(
        "- Required-run temperature comparison: "
        f"Velocity-Verlet mean {fmt_num(vv_temp.get('mean_temperature_k'), 2)} K "
        f"(std {fmt_num(vv_temp.get('std_temperature_k'), 2)} K; "
        f"range {fmt_num(vv_temp.get('min_temperature_k'), 2)}-{fmt_num(vv_temp.get('max_temperature_k'), 2)} K), "
        f"while Euler mean {fmt_num(eu_temp.get('mean_temperature_k'), 2)} K and reaches "
        f"{fmt_num(eu_temp.get('max_temperature_k'), 2)} K."
    )
    print(
        "- RDF anchors from the long Validation run: "
        f"first peak r/sigma={fmt_num(rdf_q.get('present_work_first_peak_r_over_sigma'), 3)}, "
        f"g={fmt_num(rdf_q.get('present_work_first_peak_g'), 3)}; "
        f"first minimum r/sigma={fmt_num(rdf_q.get('present_work_first_minimum_r_over_sigma'), 3)}, "
        f"g={fmt_num(rdf_q.get('present_work_first_minimum_g'), 3)}; "
        f"second peak r/sigma={fmt_num(rdf_q.get('present_work_second_peak_r_over_sigma'), 3)}, "
        f"g={fmt_num(rdf_q.get('present_work_second_peak_g'), 3)}; "
        f"tail mean g(r>4sigma)={fmt_num(rdf_q.get('present_work_long_range_mean_g_for_r_over_sigma_ge_4'), 4)}."
    )
    print("")

    strong_q = meta10.get("key_quantitative_summary", {})
    strong_rows = strong_q.get("rows", [])
    size_q = meta9.get("key_quantitative_summary", {})
    p8_row = next((row for row in strong_rows if int(row.get("P", -1)) == 8), {})
    p32_row = next((row for row in strong_rows if int(row.get("P", -1)) == 32), {})
    p2_row = next((row for row in strong_rows if int(row.get("P", -1)) == 2), {})
    fit_domain = meta9.get("fit_or_truncation", {}).get("power_law_fit_domain", [])

    def comm_pct(row: Dict[str, Any]) -> Optional[float]:
        wall = maybe_float(row.get("wall_s"))
        comm = maybe_float(row.get("comm_max_s"))
        if wall is None or comm is None or wall <= 0:
            return None
        return 100.0 * comm / wall

    print("#### Results 3 - scaling")
    if config["strong_steps"] or config["size_steps"]:
        reps_text = f", {config['reps']} repetitions per point" if config["reps"] else ""
        print(
            "- Current timing dataset configuration from `scripts/run_all_data.sh`: "
            f"strong scaling uses {config['strong_steps'] or 'n/a'} steps, "
            f"size scaling uses {config['size_steps'] or 'n/a'} steps{reps_text}."
        )
    print(
        "- Strong scaling anchors: "
        f"P=8 gives speedup {fmt_num(p8_row.get('speedup'), 2)} and efficiency {fmt_num(p8_row.get('efficiency'), 3)}; "
        f"P=32 gives speedup {fmt_num(p32_row.get('speedup'), 2)} and efficiency {fmt_num(p32_row.get('efficiency'), 3)}. "
        f"The fitted Amdahl parameter is f={fmt_num(strong_q.get('amdahl_serial_fraction_f'), 4)}."
    )
    print(
        "- Strong-scaling communication fraction rises from "
        f"{fmt_pct(comm_pct(p2_row), 1)} at P=2 to {fmt_pct(comm_pct(p32_row), 1)} at P=32."
    )
    print(
        "- Size-scaling anchors: wall time scales approximately as N^"
        f"{fmt_num(size_q.get('wall_time_power_law_exponent'), 2)} and "
        f"wall-minus-comm scales as N^{fmt_num(size_q.get('remaining_runtime_power_law_exponent'), 2)} "
        f"over the fit domain {fit_domain or 'n/a'}."
    )
    print(
        "- Communication fraction at fixed P=16 ranges from "
        f"{fmt_pct(size_q.get('communication_fraction_percent_range', [None, None])[0], 1)} to "
        f"{fmt_pct(size_q.get('communication_fraction_percent_range', [None, None])[1], 1)} across the tested N values."
    )
    print("")


def emit_support_map() -> None:
    print_heading("### Figure and Table Support Map")
    print("| Subsection | Primary artifact(s) | Best use in the report | Exact anchors to lift | Caveat to retain |")
    print("|---|---|---|---|---|")
    print(
        "| Results 1 opening paragraph | `results1_figure1ab_trajectories_dt0p01.png`, "
        "`results1_figure1c_phase_space_dt0p01.png` | Separate near-overlap in x(t), v(t) from geometric orbit quality. | "
        "dt=0.01, Euler is still the visibly worst method; Velocity-Verlet remains near-closed in phase space; RK4 is nearly exact. | "
        "This figure is qualitative; formal order comes from Fig. 3, not Fig. 1. |"
    )
    print(
        "| Results 1 timestep sensitivity | `results1_figure2_small_vs_large_dt.png`, "
        "`results1_ho_small_large_summary.csv` | Show that coarse-step behaviour separates structural stability from accuracy. | "
        "At dt=0.5 Euler is unstable, Velocity-Verlet remains bounded, RK4 stays accurate; dt=0.01 errors are tabulated separately. | "
        "Do not use dt=0.5 points in the convergence-fit claim. |"
    )
    print(
        "| Results 1 convergence paragraph | `results1_figure3_convergence_combined.png`, "
        "`results1_ho_convergence_summary.csv`, `results1_ho_endpoint_values.csv` | Main proof of first/second/fourth-order behaviour. | "
        "Endpoint slopes 1.05, 2.00, 3.94; RMS slopes 1.03, 2.00, 4.00; RK4 floor at 3.6e-15 for dt=5e-4. | "
        "State the fit rule: dt <= 0.1, with coarse points retained only for context. |"
    )
    print(
        "| Results 1 energy paragraph | `results1_figure4_energy_diagnostic.png` | Supporting evidence for long-time structure preservation. | "
        "At dt=0.01, Euler max |dE/E0| = 10.52%; Velocity-Verlet = 0.00250%; RK4 = 1.39e-11%. | "
        "Use this as structural support, not as the only accuracy argument. |"
    )
    print(
        "| Results 2 required-run paragraph | `results2_figure6_lj_brief_energy_100step_production.png`, "
        "`results2_figure7_lj_brief_temperature_100step_production.png`, "
        "`results2_quantitative_summary_table.md` | Main evidence that Velocity-Verlet is production-usable and Euler is not. | "
        "Velocity-Verlet max |dE/E0| = 0.082%; Euler = 127.587%; mean temperatures 94.42 K vs 185.27 K; Euler max temperature 396.05 K. | "
        "State that this is the required 100-step, 1 ps production run and that step 0 is the production initial frame. |"
    )
    print(
        "| Results 2 RDF paragraph | `results2_figure8_lj_rdf_comparison_rahman1964.png`, "
        "`rahman1964_fig2_manual_anchors.csv` | Structural validation against Rahman-style shell locations. | "
        "First peak 1.09 / 2.838, first minimum 1.55 / 0.623, second peak 2.07 / 1.253, tail mean 1.002. | "
        "Keep the wording qualitative or semi-quantitative because the Rahman guide is manually anchored. |"
    )
    print(
        "| Results 3 strong scaling | `results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.png`, "
        "`scaling_strong.csv` | Main performance figure for speedup, efficiency, and communication growth. | "
        "S(32)=24.12, E(32)=0.754, fitted f=0.0103, comm fraction 1.1% at P=2 to 15.2% at P=32. | "
        "Amdahl f is an empirical descriptor of the measured curve, not a literal machine-independent serial fraction. |"
    )
    print(
        "| Results 3 size scaling | `results3_figure9ab_problem_size_scaling_fixed_p16.png`, "
        "`scaling_size.csv` | Show near-O(N^2) growth and falling communication fraction at larger N. | "
        "Wall ~ N^1.85, wall-minus-comm ~ N^1.93, communication fraction 50.8% down to 13.1%. | "
        "Say explicitly that the power-law fit is over N >= 500, not all N values. |"
    )
    print("")


def emit_presentation_improvements(config: Dict[str, Optional[int]]) -> None:
    print_heading("### Stronger Presentation Opportunities")
    print("- Tighten the Lennard-Jones temperature wording to the exact measured maximum (`396.05 K`) if you want a more precise claim than `~400 K`.")
    if config["strong_steps"] or config["size_steps"]:
        print(
            f"- Fix the scaling-methods/results wording if it still says `100 steps`: "
            f"the current dataset comes from {config['strong_steps'] or 'n/a'} strong-scaling steps and "
            f"{config['size_steps'] or 'n/a'} size-scaling steps."
        )
    print("- If you want stronger Results 3 uncertainty reporting, cite `out/scaling_strong_stats.csv` and `out/scaling_size_stats.csv` or add IQR/error bars; the headline plots use median timings.")
    print("- Keep the RDF paragraph explicitly separate from the required 100-step run; otherwise the reader can incorrectly infer that g(r) came from the brief-mandated 1 ps trajectory.")
    print("- If space is tight, Fig. 4 can be shortened to a supporting sentence because Fig. 3 already carries the formal-order argument.")
    print("- If you want more implementation-context support while writing, `results_bundle.md` should include the plot-metadata JSON files and targeted figure-script excerpts after regeneration.")
    print("")


def emit_guardrails() -> None:
    print_heading("### Guardrails Against Overclaiming")
    print("- Do not describe the Rahman comparison as exact agreement; the present reference curve is a transparent manual guide, not tabulated truth data.")
    print("- Do not describe the fitted Amdahl parameter as a literal serial fraction of the code in a machine-independent sense.")
    print("- Do not say the size-scaling exponent uses all tested N values; the current fit domain is N >= 500.")
    print("- Do not say RK4 is the best production MD integrator overall just because it has the smallest short-time truncation error; your own evidence also shows the importance of symplectic structure and communication cost.")
    print("- Do not silently state `100 steps` for the scaling dataset unless you regenerate the timings with that configuration.")
    print("")


def main() -> None:
    manifest_path = Path("out/manifest.json")
    if not manifest_path.exists():
        print("Manifest missing: out/manifest.json", file=sys.stderr)
        sys.exit(1)

    results1_conv = load_csv_rows("out/summary/results1/results1_ho_convergence_summary.csv")
    results1_small_large = load_csv_rows("out/summary/results1/results1_ho_small_large_summary.csv")
    manifest = load_manifest()
    meta6 = load_json("out/plots/metadata/results2_figure6_lj_brief_energy_100step_production.json")
    meta7 = load_json("out/plots/metadata/results2_figure7_lj_brief_temperature_100step_production.json")
    meta8 = load_json("out/plots/metadata/results2_figure8_lj_rdf_comparison_rahman1964.json")
    meta9 = load_json("out/plots/metadata/results3_figure9ab_problem_size_scaling_fixed_p16.json")
    meta10 = load_json("out/plots/metadata/results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.json")
    config = parse_run_all_data_config()

    print("## 0) Report-Writing Pack")
    print("")
    print("This section is tuned for drafting the Results section itself: what to say first, which numbers to quote, what caveats must stay attached to those numbers, and where the current evidence is strongest.")
    print("")

    emit_structure_plan(config)
    emit_quantitative_anchors(
        manifest,
        results1_conv,
        results1_small_large,
        meta6,
        meta7,
        meta8,
        meta9,
        meta10,
        config,
    )
    emit_support_map()
    emit_presentation_improvements(config)
    emit_guardrails()


if __name__ == "__main__":
    main()
