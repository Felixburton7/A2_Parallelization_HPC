#!/usr/bin/env python3
"""
ai/analyse_results.py — Read existing outputs in out/ and emit a reproducible, exam-safe
summary in Markdown for inclusion in ai/results.md.

Design principles:
- Never regenerates data. Only reads what exists.
- Avoids SciPy dependency (cluster portability).
- Avoids unverifiable “line-number claims”; reports evidence from files themselves.
"""

from __future__ import annotations

import csv
import glob
import json
import math
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple


MANIFEST_PATH = "out/manifest.json"
PLOTS_DIR = "out/plots"
RESULTS1_CURRENT_PLOTS = [
    "results1_figure1ab_trajectories_dt0p01.png",
    "results1_figure1c_phase_space_dt0p01.png",
    "results1_figure2_small_vs_large_dt.png",
    "results1_figure3_convergence_combined.png",
    "results1_figure4_energy_diagnostic.png",
]
RESULTS1_LEGACY_ALIAS = {
    "results1_ho_position_velocity_trajectories.png": "results1_figure1ab_trajectories_dt0p01.png",
    "results1_ho_phase_space_trajectories.png": "results1_figure1c_phase_space_dt0p01.png",
    "results1_ho_convergence_endpoint_position_error.png": "results1_figure3_convergence_combined.png",
    "results1_ho_convergence_rms_phase_space_error.png": "results1_figure3_convergence_combined.png",
    "results1_ho_energy_conservation.png": "results1_figure4_energy_diagnostic.png",
}


def load_manifest() -> Optional[Dict[str, Any]]:
    if not os.path.exists(MANIFEST_PATH):
        return None
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def nested_get(obj: Any, dotted: str, default: Any = None) -> Any:
    cur = obj
    for key in dotted.split("."):
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def first_nonempty_manifest_path(manifest: Dict[str, Any], keys: List[str]) -> str:
    for key in keys:
        value = nested_get(manifest, key, "")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def latest_glob_path(pattern: str) -> str:
    matches = [p for p in glob.glob(pattern) if os.path.isfile(p)]
    if not matches:
        return ""
    matches.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return matches[0]


def resolve_rdf_paths(manifest: Dict[str, Any]) -> Tuple[str, str]:
    gr_path = first_nonempty_manifest_path(
        manifest,
        [
            "lj_rdf.verlet_long",
            "lj_rdf.verlet",
            "results2_outputs.rdf_csv",
            "results2_outputs.rdf_gr_csv",
        ],
    )
    if not gr_path:
        gr_path = latest_glob_path("out/runs/lj_rdf_*/gr.csv")
    if not gr_path:
        gr_path = latest_glob_path("out/runs/lj_rdf*/gr.csv")

    energy_path = first_nonempty_manifest_path(
        manifest,
        [
            "lj_rdf.verlet_long_energy",
            "lj_rdf.verlet_energy",
            "results2_outputs.rdf_energy_csv",
        ],
    )
    if not energy_path and gr_path:
        sibling = os.path.join(os.path.dirname(gr_path), "lj_verlet.csv")
        if os.path.isfile(sibling):
            energy_path = sibling
    if not energy_path:
        energy_path = latest_glob_path("out/runs/lj_rdf_*/lj_verlet.csv")
    if not energy_path:
        energy_path = latest_glob_path("out/runs/lj_rdf*/lj_verlet.csv")

    return gr_path, energy_path


def load_csv_rows(filepath: str) -> Optional[List[Dict[str, float]]]:
    """
    Load CSV skipping comment lines, return list of dicts with float values.

    NOTE: we purposely coerce to float here because all numeric outputs we analyse are numeric.
    """
    if not filepath or not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [l for l in f if l.strip() and not l.startswith("#")]
    if not lines:
        return None
    reader = csv.DictReader(lines)
    fieldnames = reader.fieldnames or []

    # Fallback for headerless 4-column scaling CSVs. In that case DictReader
    # incorrectly treats the first data row as field names (e.g. "1,2048,...").
    if len(fieldnames) >= 4:
        try:
            [float(fieldnames[i]) for i in range(4)]
            headerless_scaling = True
        except ValueError:
            headerless_scaling = False
        if headerless_scaling:
            rows: List[Dict[str, float]] = []
            for line in lines:
                cols = [c.strip() for c in line.split(",")]
                if len(cols) < 4:
                    continue
                try:
                    rows.append(
                        {
                            "P": float(cols[0]),
                            "N": float(cols[1]),
                            "wall_s": float(cols[2]),
                            "comm_max_s": float(cols[3]),
                            "comm_s": float(cols[3]),
                        }
                    )
                except ValueError:
                    continue
            return rows if rows else None

    rows: List[Dict[str, float]] = []
    for row in reader:
        cleaned: Dict[str, float] = {}
        for k, v in row.items():
            if not k:
                continue
            if v is None:
                continue
            sv = str(v).strip()
            if not sv:
                continue
            try:
                cleaned[k] = float(sv)
            except ValueError:
                # Ignore non-numeric fields
                pass
        if cleaned:
            rows.append(cleaned)
    return rows


def comm_seconds(row: Dict[str, float]) -> float:
    """
    Return communication timing from a scaling CSV row.
    Prefer the current canonical key `comm_max_s`, fallback to legacy `comm_s`.
    """
    if "comm_max_s" in row:
        return float(row["comm_max_s"])
    if "comm_s" in row:
        return float(row["comm_s"])
    return 0.0


def parse_csv_metadata(filepath: str) -> Dict[str, str]:
    """
    Parse the first leading comment line of the form:

    # mode: lj, integrator: verlet, N: 864, P: 4, dt: 1e-14, steps: 100, ...

    Returns a dict of key->value (strings). If not present, returns {}.
    """
    if not filepath or not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not line.startswith("#"):
                break
            # first metadata line is enough
            s = line.lstrip("#").strip()
            # split on commas, parse "k: v"
            parts = [p.strip() for p in s.split(",")]
            md: Dict[str, str] = {}
            for p in parts:
                m = re.match(r"^([^:]+)\s*:\s*(.+)$", p)
                if m:
                    md[m.group(1).strip()] = m.group(2).strip()
            if md:
                return md
    return {}


def meta_int(meta: Dict[str, str], key: str, default: int = 0) -> int:
    try:
        return int(float(meta.get(key, str(default))))
    except ValueError:
        return default


def production_start_step(meta: Dict[str, str]) -> int:
    if "production_start_step" in meta:
        return meta_int(meta, "production_start_step", 0)
    return meta_int(meta, "production_start", 0)


def loglog_slope(points: List[Tuple[float, float]]) -> float:
    """Least-squares slope for log10(y) ~ a log10(x) + b."""
    xs = [math.log10(x) for x, _ in points]
    ys = [math.log10(y) for _, y in points]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    ss_xy = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    ss_xx = sum((xs[i] - mx) ** 2 for i in range(n))
    return ss_xy / ss_xx if ss_xx > 0 else float("nan")


def amdahl_fit_from_speedups(P: List[int], S: List[float]) -> Tuple[float, float, float, int]:
    """
    Fit Amdahl S(P) = 1 / ( f + (1-f)/P ) without SciPy.

    We linearise using y = 1/S:
        y(P) = f*(1 - 1/P) + 1/P = a(P)*f + b(P)

    So we do least squares for f over P>1:
        f = argmin Σ (y_i - (a_i f + b_i))^2

    Returns (f, f_err, max_abs_residual_in_S, P_at_max_residual)
    """
    assert len(P) == len(S)
    data = []
    for p, s in zip(P, S):
        if p <= 1:
            continue
        if s <= 0:
            continue
        y = 1.0 / s
        a = 1.0 - 1.0 / p
        b = 1.0 / p
        data.append((p, a, b, y))

    if len(data) < 2:
        return float("nan"), float("nan"), float("nan"), -1

    denom = sum(a * a for _, a, _, _ in data)
    num = sum(a * (y - b) for _, a, b, y in data)
    f = num / denom if denom > 0 else float("nan")

    # residuals in y-space
    resid_y = [y - (a * f + b) for _, a, b, y in data]
    dof = max(1, len(data) - 1)
    sigma2 = sum(r * r for r in resid_y) / dof
    f_err = math.sqrt(sigma2 / denom) if denom > 0 else float("nan")

    # residuals in S-space for reporting
    def S_model(p: int, f_: float) -> float:
        return 1.0 / (f_ + (1.0 - f_) / p)

    residuals_S = []
    for p, _, _, _ in data:
        s_pred = S_model(p, f)
        s_obs = S[P.index(p)]  # assumes unique P in CSV
        residuals_S.append((p, s_obs - s_pred))

    p_max, r_max = max(residuals_S, key=lambda pr: abs(pr[1]))
    return f, f_err, abs(r_max), p_max


def status_label(ok: bool, if_missing: str = "potential issue", if_ok: str = "confirmed") -> str:
    return if_ok if ok else if_missing


def analyse_ho(manifest: Dict[str, Any]) -> None:
    print("### HO Convergence Analysis\n")

    ho = manifest.get("ho_convergence", {})
    if not ho:
        print("**No HO convergence data in manifest.**\n")
        return

    # Exact solution at T=10 for x(0)=1,v(0)=0, ω=1 (as used by plotting scripts)
    x_exact = math.cos(10.0)
    v_exact = -math.sin(10.0)

    integrators: Dict[str, List[Tuple[float, float, float, float]]] = {}
    phase_metrics: Dict[str, List[Tuple[float, float, float]]] = {}
    for key, fpath in ho.items():
        parts = key.split("_dt")
        if len(parts) != 2:
            continue
        integ = parts[0]
        dt = float(parts[1].replace("_", "."))
        data = load_csv_rows(fpath)
        if not data:
            continue
        x_final = data[-1].get("x")
        v_final = data[-1].get("v")
        if x_final is None or v_final is None:
            continue
        err = abs(x_final - x_exact)
        integrators.setdefault(integ, []).append((dt, err, x_final, v_final))

        phase_err2: List[float] = []
        for row in data:
            t = row.get("time")
            x = row.get("x")
            v = row.get("v")
            if t is None or x is None or v is None:
                continue
            dx = x - math.cos(t)
            dv = v + math.sin(t)
            phase_err2.append(dx * dx + dv * dv)
        if phase_err2:
            e_max = math.sqrt(max(phase_err2))
            e_rms = math.sqrt(sum(phase_err2) / len(phase_err2))
            phase_metrics.setdefault(integ, []).append((dt, e_max, e_rms))

    print("| Integrator | dt | x_num(T=10) | |x error| |")
    print("|------------|-----|-------------|----------|")
    for integ in ["euler", "verlet", "rk4"]:
        pts = sorted(integrators.get(integ, []), key=lambda t: -t[0])
        for dt, err, xf, _vf in pts:
            print(f"| {integ} | {dt:g} | {xf:.10e} | {err:.4e} |")
    print("")

    print("**Velocity convergence at T=10:**")
    print("| Integrator | dt | v_num(T=10) | |v error| |")
    print("|------------|-----|-------------|----------|")
    for integ in ["euler", "verlet", "rk4"]:
        pts = sorted(integrators.get(integ, []), key=lambda t: -t[0])
        for dt, _err, _xf, vf in pts:
            v_err = abs(vf - v_exact)
            print(f"| {integ} | {dt:g} | {vf:.10e} | {v_err:.4e} |")
    print("")

    # Slopes (fit only in the small-dt regime to avoid “pre-asymptotic” contamination)
    print("**Fitted convergence slopes (log-log on |x(T=10)-x_exact|):**\n")
    for integ in ["euler", "verlet", "rk4"]:
        raw = [(dt, err) for dt, err, *_ in integrators.get(integ, []) if err > 1e-14]
        if len(raw) < 3:
            print(f"- {integ}: insufficient points above machine epsilon")
            continue

        # Heuristic: fit on dt <= 0.1 (matches typical asymptotic regime here)
        fit_pts = [(dt, err) for dt, err in raw if dt <= 0.1]
        if len(fit_pts) < 3:
            fit_pts = sorted(raw)[: max(3, len(raw) // 2)]  # fallback: smallest half

        slope = loglog_slope(sorted(fit_pts))
        expected = {"euler": 1, "verlet": 2, "rk4": 4}[integ]
        used = ", ".join(f"{dt:g}" for dt, _ in sorted(fit_pts))
        print(f"- {integ}: slope = {slope:.2f} (expected {expected}); fit dt = [{used}]")
    print("")

    print("**Whole-trajectory RMS phase-space convergence slopes:**\n")
    for integ in ["euler", "verlet", "rk4"]:
        raw: List[Tuple[float, float]] = []
        for dt, _e_max, e_rms in phase_metrics.get(integ, []):
            if e_rms > 1e-16:
                raw.append((dt, e_rms))
        if len(raw) < 3:
            print(f"- {integ}: insufficient points above machine epsilon")
            continue

        fit_pts = [(dt, err) for dt, err in raw if dt <= 0.1]
        if len(fit_pts) < 3:
            fit_pts = sorted(raw)[: max(3, len(raw) // 2)]

        slope = loglog_slope(sorted(fit_pts))
        expected = {"euler": 1, "verlet": 2, "rk4": 4}[integ]
        used = ", ".join(f"{dt:g}" for dt, _ in sorted(fit_pts))
        print(f"- {integ}: slope = {slope:.2f} (expected {expected}); fit dt = [{used}]")
    print("")

    # Energy drift at dt=0.01 (if present)
    print("**Energy conservation diagnostic (dt≈0.01):**")
    for integ in ["euler", "verlet", "rk4"]:
        candidate = None
        for k, v in ho.items():
            if k.startswith(integ) and ("dt0_01" in k or "dt0.01" in k):
                candidate = v
                break
        if not candidate:
            continue
        data = load_csv_rows(candidate)
        if not data:
            continue
        etot = [r.get("E_total") for r in data if "E_total" in r]
        if not etot:
            continue
        e0 = etot[0]
        if abs(e0) < 1e-30:
            continue
        max_drift = max(abs(e - e0) / abs(e0) for e in etot) * 100.0
        print(f"- {integ}: max |ΔE/E0| = {max_drift:.6f}% (dt≈0.01)")
    print("")

    print("**Plots presence (current naming):**")
    for p in RESULTS1_CURRENT_PLOTS:
        f = os.path.join(PLOTS_DIR, p)
        print(f"- `{f}` — {status_label(os.path.exists(f))}")
    print("**Legacy filename aliases (staleness-aware check):**")
    for legacy, current in RESULTS1_LEGACY_ALIAS.items():
        legacy_path = os.path.join(PLOTS_DIR, legacy)
        current_path = os.path.join(PLOTS_DIR, current)
        if os.path.exists(legacy_path):
            if os.path.exists(current_path):
                state = "informational (legacy + current both present)"
            else:
                state = "potential issue (legacy present, current missing)"
        else:
            if os.path.exists(current_path):
                state = "expected by design (renamed to current filename)"
            else:
                state = "potential issue (both legacy and current names missing)"
        print(f"- `{legacy_path}` → `{current_path}` — {state}")
    print("")


def analyse_lj(manifest: Dict[str, Any]) -> None:
    print("### LJ / Argon Analysis\n")

    run_specs = [
        ("lj_brief.verlet", "Brief (required) — Velocity-Verlet"),
        ("lj_brief.euler", "Brief (required) — Euler"),
    ]
    for key, label in run_specs:
        fpath = nested_get(manifest, key, "")
        data = load_csv_rows(fpath)
        if not data:
            print(f"**{label}:** data not found at `{fpath}`\n")
            continue

        meta = parse_csv_metadata(fpath)
        production_start = production_start_step(meta)
        n_steps_meta = meta_int(meta, "n_steps", meta_int(meta, "steps", -1))
        n_frames_meta = meta_int(meta, "n_frames", -1)

        prod_rows = [r for r in data if r.get("step", -1) >= production_start]
        if not prod_rows:
            prod_rows = data

        e_prod = [r["E_total"] for r in prod_rows if "E_total" in r and math.isfinite(r["E_total"])]
        temps_prod = [r["temperature"] for r in prod_rows if "temperature" in r and math.isfinite(r["temperature"])]

        if e_prod:
            e0 = e_prod[0]
            rel = [abs(e - e0) / abs(e0) * 100.0 for e in e_prod] if abs(e0) > 1e-30 else []
            max_drift = max(rel) if rel else float("nan")
            mean_drift = sum(rel) / len(rel) if rel else float("nan")
        else:
            max_drift = mean_drift = float("nan")

        if temps_prod:
            t_mean = sum(temps_prod) / len(temps_prod)
            t_std = math.sqrt(sum((t - t_mean) ** 2 for t in temps_prod) / len(temps_prod))
            t_min, t_max = min(temps_prod), max(temps_prod)
        else:
            t_mean = t_std = t_min = t_max = float("nan")

        steps_observed = int(max(r.get("step", -1) for r in data))
        frames_observed = len(data)

        print(f"**{label} (CSV: `{fpath}`):**")
        if meta:
            print(
                f"- Metadata: N={meta.get('N','?')}, P={meta.get('P','?')}, dt={meta.get('dt','?')}, "
                f"n_steps={n_steps_meta}, n_frames={n_frames_meta}, step_indexing={meta.get('step_indexing','?')}"
            )
            print(
                f"- Equilibration/production: equilibration_steps={meta.get('equilibration_steps','?')}, "
                f"production_steps={meta.get('production_steps', n_steps_meta)}, "
                f"production_start_step={production_start}, "
                f"final_rescale_before_production={meta.get('final_rescale_before_production','?')}"
            )
        print(f"- Observed in CSV: max_step={steps_observed}, frames={frames_observed}")
        print(
            f"- Production window (step >= {production_start}): "
            f"Max |ΔE/E0| = {max_drift:.4f}% ; Mean |ΔE/E0| = {mean_drift:.4f}%"
        )
        if temps_prod:
            print(
                f"- Production temperature: mean={t_mean:.2f} K, std={t_std:.2f} K, "
                f"range=[{t_min:.2f},{t_max:.2f}]"
            )
        print("")

    # g(r)
    gr_path, gr_energy_path = resolve_rdf_paths(manifest)
    gr = load_csv_rows(gr_path)
    if gr:
        r_vals = [row.get("r_sigma", 0.0) for row in gr]
        g_vals = [row.get("gr", 0.0) for row in gr]
        imax = max(range(len(g_vals)), key=lambda i: g_vals[i])
        peak1_r, peak1_g = r_vals[imax], g_vals[imax]

        # minimum between 1.3 and 2.0
        candidates = [(r, g) for r, g in zip(r_vals, g_vals) if 1.3 < r < 2.0]
        min1_r, min1_g = min(candidates, key=lambda rg: rg[1]) if candidates else (float("nan"), float("nan"))

        # second peak between 1.5 and 2.5
        candidates2 = [(r, g) for r, g in zip(r_vals, g_vals) if 1.5 < r < 2.5]
        peak2_r, peak2_g = max(candidates2, key=lambda rg: rg[1]) if candidates2 else (float("nan"), float("nan"))

        tail = [g for r, g in zip(r_vals, g_vals) if r > 4.0]
        g_tail = sum(tail) / len(tail) if tail else float("nan")

        meta = parse_csv_metadata(gr_path)

        print("**g(r) shape diagnostics (long RDF production run):**")
        if meta:
            print(f"- Metadata: N={meta.get('N','?')}, P={meta.get('P','?')}, dt={meta.get('dt','?')}, steps={meta.get('steps','?')}")
        print(f"- First peak: r/σ = {peak1_r:.3f}, g = {peak1_g:.3f}")
        print(f"- First minimum: r/σ = {min1_r:.3f}, g = {min1_g:.3f}")
        print(f"- Second peak: r/σ = {peak2_r:.3f}, g = {peak2_g:.3f}")
        print(f"- Tail (r>4σ): <g> = {g_tail:.4f} (should → 1)")
        print(f"- CSV: `{gr_path}`")
        if gr_energy_path:
            print(f"- Companion trajectory CSV: `{gr_energy_path}`")
        print("")
        print("- Interpretation: shell locations agree broadly with Rahman (1964), with somewhat reduced present-work peak heights.")
        print("- Provenance: Rahman guide values are manual Fig. 2 anchors (paper-anchored x values at 3.7 Å, 7.0 Å, 10.4 Å; other points are approximate shape anchors).\n")
    else:
        print("**g(r):** data not found\n")

    print("**Plots presence:**")
    core_plots = [
        "results2_figure6_lj_brief_energy_100step_production.png",
        "results2_figure7_lj_brief_temperature_100step_production.png",
        "results2_figure8_lj_rdf_comparison_rahman1964.png",
    ]
    for p in core_plots:
        f = os.path.join(PLOTS_DIR, p)
        print(f"- `{f}` — {status_label(os.path.exists(f))}")
    print("- Core Results 2 evidence: required-run energy + required-run temperature + RDF-vs-Rahman.")
    table_md = "out/summary/results2/results2_quantitative_summary_table.md"
    table_csv = "out/summary/results2/results2_quantitative_summary_table.csv"
    rahman_anchor = "out/summary/results2/rahman1964_fig2_manual_anchors.csv"
    print(f"- Results 2 quantitative table (MD): `{table_md}` — {status_label(os.path.exists(table_md))}")
    print(f"- Results 2 quantitative table (CSV): `{table_csv}` — {status_label(os.path.exists(table_csv))}")
    print(f"- Rahman anchor dataset: `{rahman_anchor}` — {status_label(os.path.exists(rahman_anchor))}")
    print("")


def analyse_scaling(manifest: Dict[str, Any]) -> None:
    print("### Scaling Analysis\n")

    scaling = manifest.get("scaling", {})

    # Strong scaling
    strong_path = scaling.get("strong", "")
    strong = load_csv_rows(strong_path)
    if strong:
        t1 = strong[0]["wall_s"]
        P_vals = [int(r["P"]) for r in strong]
        wall = [r["wall_s"] for r in strong]
        comm = [comm_seconds(r) for r in strong]
        speedup = [t1 / w if w > 0 else float("nan") for w in wall]
        eff = [speedup[i] / P_vals[i] if P_vals[i] > 0 else float("nan") for i in range(len(P_vals))]

        print("**Strong scaling (from CSV):**\n")
        print("| P | Wall [s] | Comm [s] | Comm% | Speedup | Efficiency |")
        print("|---|----------|----------|-------|---------|------------|")
        for p, w, c, s, e in zip(P_vals, wall, comm, speedup, eff):
            comm_pct = (c / w * 100.0) if w > 0 else 0.0
            print(f"| {p} | {w:.6f} | {c:.6f} | {comm_pct:.1f}% | {s:.2f} | {e:.3f} |")
        print("")

        f_fit, f_err, max_res, p_at = amdahl_fit_from_speedups(P_vals, speedup)
        if math.isnan(f_fit):
            print("**Amdahl fit:** insufficient data.\n")
        else:
            print("**Amdahl fit (no SciPy; linear least squares on 1/S):**")
            print(f"- f = {f_fit:.6f} ± {f_err:.6f}")
            if f_fit > 0:
                print(f"- Max theoretical speedup ≈ {1.0 / f_fit:.1f}x")
            print(f"- Max |S_obs - S_fit| = {max_res:.3f} at P={p_at}\n")

        print(f"- CSV: `{strong_path}`\n")
    else:
        print("**Strong scaling:** data not found\n")

    # Size scaling
    size_path = scaling.get("size", "")
    size = load_csv_rows(size_path)
    if size:
        Ns = [int(r["N"]) for r in size]
        wall = [r["wall_s"] for r in size]
        comm = [comm_seconds(r) for r in size]
        comp = [max(1e-12, wall[i] - comm[i]) for i in range(len(size))]

        print("**Size scaling (from CSV):**\n")
        print("| N | Wall [s] | Comm [s] | Compute=Wall-Comm [s] | Comm% |")
        print("|---|----------|----------|----------------------|-------|")
        for n, w, c, cp in zip(Ns, wall, comm, comp):
            comm_pct = (c / w * 100.0) if w > 0 else 0.0
            print(f"| {n} | {w:.6f} | {c:.6f} | {cp:.6f} | {comm_pct:.1f}% |")
        print("")

        wall_pts = [(float(n), float(w)) for n, w in zip(Ns, wall) if w > 0]
        comp_pts = [(float(n), float(cp)) for n, cp in zip(Ns, comp) if cp > 0]
        if len(wall_pts) >= 3:
            slope_wall = loglog_slope(sorted(wall_pts))
            slope_comp = loglog_slope(sorted(comp_pts))
            print(f"**Size-scaling exponent (log-log fit over all N points):**")
            print(f"- wall ~ N^{slope_wall:.2f}")
            print(f"- compute-only (wall-comm) ~ N^{slope_comp:.2f}")
            print("")
            print("⚠️ If you expect O(N²) (direct all-pairs), but see <2.0 here, increase scaling timesteps")
            print("   (e.g. 500–2000 steps) so start-up/communication overhead doesn’t dominate the fit.\n")

        print(f"- CSV: `{size_path}`\n")
    else:
        print("**Size scaling:** data not found\n")

    print("**Plots presence:**")
    for p in [
        "results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.png",
        "results3_figure9ab_problem_size_scaling_fixed_p16.png",
    ]:
        f = os.path.join(PLOTS_DIR, p)
        print(f"- `{f}` — {status_label(os.path.exists(f))}")
    print("")


def verify_manifest_files(manifest: Dict[str, Any]) -> None:
    print("### File Verification\n")

    def walk(obj: Any, keypath: str = "") -> None:
        if isinstance(obj, str):
            looks_like_path = (
                "/" in obj
                or obj.startswith("out/")
                or obj.endswith((".csv", ".png", ".json", ".md"))
            )
            if looks_like_path:
                status = status_label(os.path.exists(obj))
                print(f"- `{keypath}` → `{obj}` — {status}")
            else:
                print(f"- `{keypath}` → `{obj}` — informational")
            return
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{keypath}.{k}" if keypath else k)

    walk(manifest)
    print("")


def scan_submission_tree() -> Dict[str, List[str]]:
    """
    Lightweight static scan for common compliance problems:
    - identifying strings (felix, CRSid-like, email-like)
    - rand() usage
    - OpenMP pragmas
    """
    hits = {
        "identifiers": [],
        "rand": [],
        "openmp": [],
    }
    # Only scan the files that would go into the dist tarball (plus README)
    roots = ["include", "src", "tests", "scripts"]
    extra = ["Makefile", "README.md", ".clang-format"]
    files: List[str] = []
    for r in roots:
        if os.path.isdir(r):
            for root, _dirs, fnames in os.walk(r):
                for fn in fnames:
                    # Exclude generated caches/binaries to avoid false positives.
                    if fn.endswith((".o", ".a", ".so", ".dylib", ".pyc")):
                        continue
                    if fn in {"md_solver", "test_runner"}:
                        continue
                    files.append(os.path.join(root, fn))
    for fn in extra:
        if os.path.exists(fn):
            files.append(fn)

    id_patterns = [
        re.compile(r"\bfelix\b", re.IGNORECASE),
        re.compile(r"@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),      # email-ish
        re.compile(r"\b[a-z]{2,4}\d{2,4}\b", re.IGNORECASE), # CRSid-ish (heuristic)
        re.compile(r"/Users/"),
    ]
    files = [fp for fp in files if "__pycache__" not in fp and "/.git/" not in fp]

    for fp in files:
        try:
            txt = open(fp, "r", encoding="utf-8", errors="ignore").read()
        except Exception:
            continue

        for pat in id_patterns:
            if pat.search(txt):
                hits["identifiers"].append(fp)
                break

        if re.search(r"(^|[^a-zA-Z0-9_])(std::)?rand\s*\(", txt):
            hits["rand"].append(fp)

        if re.search(r"#\s*pragma\s+omp\b", txt) or "omp.h" in txt:
            hits["openmp"].append(fp)

    # Deduplicate
    for k in list(hits.keys()):
        hits[k] = sorted(set(hits[k]))
    return hits


def compliance_section(manifest: Dict[str, Any]) -> None:
    print("## E) Compliance & Known Limitations\n")

    print("### Evidence-based checklist (from actual output files)\n")
    print("| Requirement | Status | Evidence / interpretation |")
    print("|-------------|--------|---------------------------|")

    def emit(requirement: str, status: str, evidence: str) -> None:
        print(f"| {requirement} | {status} | {evidence} |")

    # LJ brief-required run
    vv_path = nested_get(manifest, "lj_brief.verlet", "")
    eu_path = nested_get(manifest, "lj_brief.euler", "")
    vv_meta = parse_csv_metadata(vv_path)
    eu_meta = parse_csv_metadata(eu_path)

    def brief_ok(meta: Dict[str, str]) -> bool:
        if not meta:
            return False
        n_steps = meta_int(meta, "n_steps", meta_int(meta, "steps", -1))
        n_frames = meta_int(meta, "n_frames", -1)
        return (
            meta.get("N") == "864"
            and meta.get("dt") == "1e-14"
            and n_steps == 100
            and n_frames == 101
            and "0..steps" in meta.get("step_indexing", "")
        )

    def production_ok(meta: Dict[str, str]) -> bool:
        if not meta:
            return False
        equil_steps = meta_int(meta, "equilibration_steps", 0)
        production_steps = meta_int(meta, "production_steps", meta_int(meta, "n_steps", -1))
        production_start = production_start_step(meta)
        total_steps = meta_int(meta, "total_steps_executed", equil_steps + production_steps)
        final_rescale = meta.get("final_rescale_before_production", "").lower() in {"true", "1"}
        production_nve = meta.get("production_nve", "").lower() in {"true", "1"}
        return (
            production_start == 0
            and production_steps == 100
            and total_steps == equil_steps + production_steps
            and final_rescale
            and production_nve
        )

    emit(
        "LJ brief run (Verlet) N=864, dt=1e-14, n_steps=100, n_frames=101",
        status_label(brief_ok(vv_meta)),
        f"`{vv_path}` header: {vv_meta or 'missing metadata/header'}",
    )
    emit(
        "LJ brief run (Euler) N=864, dt=1e-14, n_steps=100, n_frames=101",
        status_label(brief_ok(eu_meta)),
        f"`{eu_path}` header: {eu_meta or 'missing metadata/header'}",
    )
    emit(
        "LJ two-stage semantics (Verlet brief)",
        status_label(production_ok(vv_meta)),
        "Expected production_start_step=0, production_steps=100, total_steps_executed=equilibration_steps+production_steps, final_rescale_before_production=true, production_nve=true",
    )
    emit(
        "LJ two-stage semantics (Euler brief)",
        status_label(production_ok(eu_meta)),
        "Expected production_start_step=0, production_steps=100, total_steps_executed=equilibration_steps+production_steps, final_rescale_before_production=true, production_nve=true",
    )

    # HO convergence existence
    has_ho = bool(manifest.get("ho_convergence", {}))
    emit(
        "HO convergence data present",
        status_label(has_ho),
        f"`manifest.ho_convergence` {'present' if has_ho else 'missing'}",
    )

    # Required current plots presence (by filename)
    required_plots = [
        "results1_figure1ab_trajectories_dt0p01.png",
        "results1_figure1c_phase_space_dt0p01.png",
        "results1_figure2_small_vs_large_dt.png",
        "results1_figure3_convergence_combined.png",
        "results2_figure6_lj_brief_energy_100step_production.png",
        "results2_figure7_lj_brief_temperature_100step_production.png",
        "results2_figure8_lj_rdf_comparison_rahman1964.png",
        "results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.png",
        "results3_figure9ab_problem_size_scaling_fixed_p16.png",
    ]
    present_required = [p for p in required_plots if os.path.exists(os.path.join(PLOTS_DIR, p))]
    missing_required = [p for p in required_plots if not os.path.exists(os.path.join(PLOTS_DIR, p))]
    emit(
        "Required current plot set present",
        status_label(not missing_required),
        f"present={present_required}; missing={missing_required or 'none'}",
    )

    legacy_missing = [
        old for old in RESULTS1_LEGACY_ALIAS
        if not os.path.exists(os.path.join(PLOTS_DIR, old))
    ]
    if len(legacy_missing) == len(RESULTS1_LEGACY_ALIAS):
        legacy_status = "expected by design"
        legacy_note = "Legacy Results 1 filenames are absent because plots were renamed to the `results1_figure*` scheme."
    else:
        legacy_status = "informational"
        legacy_note = "Some legacy Results 1 filename aliases still exist in out/plots."
    emit("Legacy Results 1 plot-name aliases", legacy_status, legacy_note)

    # Build system sanity
    has_makefile = os.path.exists("Makefile")
    emit("Makefile present", status_label(has_makefile), f"`Makefile` {'exists' if has_makefile else 'missing'}")

    # Static scan for prohibited patterns
    hits = scan_submission_tree()
    emit("No rand()/std::rand() usage", status_label(not hits["rand"]), str(hits["rand"] or "none"))
    emit("No OpenMP usage", status_label(not hits["openmp"]), str(hits["openmp"] or "none"))

    identifiers = hits["identifiers"]
    core_identifier_hits = [p for p in identifiers if p.startswith(("include/", "src/", "tests/")) or p in {"Makefile", "README.md", ".clang-format"}]
    if not identifiers:
        id_status = "confirmed"
        id_note = "none"
    elif core_identifier_hits:
        id_status = "potential issue"
        id_note = f"core files with possible identifiers: {core_identifier_hits}"
    else:
        id_status = "informational"
        id_note = f"non-core helper files flagged: {identifiers}"
    emit("No obvious identifying strings in scanned files", id_status, id_note)
    print("")

    print("### Known limitations (state these honestly in the report)\n")
    print("- LJ uses a **hard cutoff** (no potential shifting), so you should expect small energy discontinuities when pairs cross r_cut.")
    print("- LJ forces are computed by a **direct all-pairs loop** (no neighbour lists). This is correct but O(N²).")
    print("- For **Lennard-Jones strong-scaling runs**, ranks use particle decomposition and allgather positions before force evaluation; the measured communication fraction rises with P.")
    print("- LJ startup rescales velocities each startup step (`--equilibration-steps`) and can apply a final startup->production rescale (`--final-rescale-before-production`) before production NVE.\n")


def main() -> None:
    manifest = load_manifest()
    if manifest is None:
        print("**ERROR:** out/manifest.json not found.")
        print("Run `bash scripts/run_all_data.sh` (or your production workflow) to generate data first.")
        sys.exit(1)

    section = sys.argv[1] if len(sys.argv) > 1 else "all"

    if section in ("provenance", "all"):
        print("## A) Provenance\n")
        print("### out/manifest.json")
        print("```json")
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            print(f.read().rstrip())
        print("```\n")
        verify_manifest_files(manifest)

    if section in ("ho", "all"):
        print("## B) Results 1: Harmonic Oscillator\n")
        analyse_ho(manifest)

    if section in ("lj", "all"):
        print("## C) Results 2: Lennard-Jones / Argon\n")
        analyse_lj(manifest)

    if section in ("scaling", "all"):
        print("## D) Results 3: Scaling\n")
        analyse_scaling(manifest)

    if section in ("compliance", "all"):
        compliance_section(manifest)


if __name__ == "__main__":
    main()
