#!/usr/bin/env python3
"""
Generate high-signal project-wide context sections for ai/audit_output.md,
ai/results.md, and ai/results_bundle.md.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

COMPANION_FILES = [
    "ai/audit_output.md",
    "ai/results.md",
    "ai/results_bundle.md",
]

CORE_FIGURES: List[Tuple[str, str, bool]] = [
    ("Results 1", "out/plots/results1_figure1ab_trajectories_dt0p01.png", True),
    ("Results 1", "out/plots/results1_figure1c_phase_space_dt0p01.png", True),
    ("Results 1", "out/plots/results1_figure2_small_vs_large_dt.png", True),
    ("Results 1", "out/plots/results1_figure3_convergence_combined.png", True),
    ("Results 1", "out/plots/results1_figure4_energy_diagnostic.png", False),
    ("Results 2", "out/plots/results2_figure6_lj_brief_energy_100step_production.png", True),
    ("Results 2", "out/plots/results2_figure7_lj_brief_temperature_100step_production.png", True),
    ("Results 2", "out/plots/results2_figure8_lj_rdf_comparison_rahman1964.png", True),
    ("Results 3", "out/plots/results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.png", True),
    ("Results 3", "out/plots/results3_figure9ab_problem_size_scaling_fixed_p16.png", True),
]

CORE_TABLES: List[Tuple[str, str, bool]] = [
    ("Manifest", "out/manifest.json", True),
    ("Results 1", "out/summary/results1/results1_ho_convergence_summary.csv", True),
    ("Results 1", "out/summary/results1/results1_ho_small_large_summary.csv", True),
    ("Results 1", "out/summary/results1/results1_ho_endpoint_values.csv", True),
    ("Results 2", "out/summary/results2/results2_quantitative_summary_table.csv", True),
    ("Results 2", "out/summary/results2/results2_quantitative_summary_table.md", True),
    ("Results 3", "out/scaling_strong.csv", True),
    ("Results 3", "out/scaling_size.csv", True),
]

LEGACY_PLOT_ALIASES = {
    "out/plots/results1_ho_position_velocity_trajectories.png": "out/plots/results1_figure1ab_trajectories_dt0p01.png",
    "out/plots/results1_ho_phase_space_trajectories.png": "out/plots/results1_figure1c_phase_space_dt0p01.png",
    "out/plots/results1_ho_convergence_endpoint_position_error.png": "out/plots/results1_figure3_convergence_combined.png",
    "out/plots/results1_ho_convergence_rms_phase_space_error.png": "out/plots/results1_figure3_convergence_combined.png",
    "out/plots/results1_ho_energy_conservation.png": "out/plots/results1_figure4_energy_diagnostic.png",
}

STALE_RESULTS2_ARTIFACTS = [
    "out/plots/results2_lj_extended_energy_stability.png",
    "out/plots/results2_lj_extended_temperature_stability.png",
    "out/plots/metadata/results2_lj_extended_energy_stability.json",
    "out/plots/metadata/results2_lj_extended_temperature_stability.json",
]

DOC_PROFILES = {
    "audit": {
        "title": "Audit Output — WA2 MPI MD Solver",
        "purpose": "Executable project-wide audit trace: build/tests/smoke runs and raw code/context evidence.",
        "authoritative_for": "Build/test execution traces and raw repository state at generation time.",
        "less_authoritative_for": "Narrative interpretation of scientific conclusions across all figures.",
        "companion_priority": ["ai/results.md", "ai/results_bundle.md"],
        "generation_sources": [
            "ai/audit.sh",
            "ai/context_report.py",
            "Makefile",
            "tests/test_runner.cpp",
            "src/main.cpp",
            "out/manifest.json",
        ],
    },
    "results": {
        "title": "Results Summary — WA2 MPI MD Solver",
        "purpose": "Project-wide interpreted summary of Results 1/2/3 from existing generated artifacts.",
        "authoritative_for": "Interpretation-ready summaries, key metrics, and evidence linkage across assignment outputs.",
        "less_authoritative_for": "Full raw traces/logs and complete CSV payloads.",
        "companion_priority": ["ai/results_bundle.md", "ai/audit_output.md"],
        "generation_sources": [
            "ai/make_results.sh",
            "ai/report_writer_context.py",
            "ai/analyse_results.py",
            "ai/context_report.py",
            "out/manifest.json",
            "out/plots/metadata/results2_figure7_lj_brief_temperature_100step_production.json",
            "out/plots/metadata/results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.json",
        ],
    },
    "bundle": {
        "title": "MD Solver Production Data Bundle",
        "purpose": "Project-wide raw artifact bundle: manifest-linked CSV/notes with truncation for context-size control.",
        "authoritative_for": "Raw artifact payloads and exact file contents included for downstream LLM context.",
        "less_authoritative_for": "Interpretive judgment, confidence scoring, and compliance decisions.",
        "companion_priority": ["ai/results.md", "ai/audit_output.md"],
        "generation_sources": [
            "ai/pack_results.sh",
            "ai/context_report.py",
            "out/manifest.json",
            "out/summary/results2/results2_quantitative_summary_table.csv",
        ],
    },
}

DOC_OUTPUT_PATH = {
    "audit": "ai/audit_output.md",
    "results": "ai/results.md",
    "bundle": "ai/results_bundle.md",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_bool(raw: str) -> bool:
    return raw.strip().lower() in {"1", "true", "yes", "y"}


def fmt_yes_no(value: bool) -> str:
    return "yes" if value else "no"


def file_exists(path: str) -> bool:
    return Path(path).exists()


def file_mtime_utc(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return "missing"
    return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_read_json(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "no git"


def git_dirty_count() -> Optional[int]:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
        )
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        return len(lines)
    except subprocess.CalledProcessError:
        return None


def status_label(ok: bool, missing_ok: bool = False) -> str:
    if ok:
        return "confirmed"
    if missing_ok:
        return "not applicable"
    return "potential issue"


def flatten_manifest_paths(obj: Any) -> List[str]:
    out: List[str] = []

    def walk(cur: Any) -> None:
        if isinstance(cur, str):
            if cur.startswith("out/") or cur.endswith((".csv", ".json", ".png", ".md")):
                out.append(cur)
            return
        if isinstance(cur, dict):
            for val in cur.values():
                walk(val)
        elif isinstance(cur, list):
            for val in cur:
                walk(val)

    walk(obj)
    return sorted(set(out))


def read_results2_table() -> Dict[str, float]:
    path = Path("out/summary/results2/results2_quantitative_summary_table.csv")
    if not path.exists():
        return {}
    out: Dict[str, float] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            label = (row.get("Integrator/Feature") or "").strip()
            section = (row.get("section") or "").strip()
            if section != "A":
                continue
            try:
                mean_t = float(row.get("Mean T [K]") or "nan")
                max_drift = float(row.get("Max |ΔE/E0| [%]") or "nan")
            except ValueError:
                continue
            key = "verlet" if "Verlet" in label else ("euler" if "Euler" in label else "")
            if not key:
                continue
            out[f"{key}_mean_t"] = mean_t
            out[f"{key}_max_drift"] = max_drift
    return out


def read_results1_slopes() -> Dict[str, float]:
    path = Path("out/summary/results1/results1_ho_convergence_summary.csv")
    if not path.exists():
        return {}
    out: Dict[str, float] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            integrator = (row.get("integrator") or "").strip().lower()
            if not integrator:
                continue
            try:
                out[f"{integrator}_endpoint_slope"] = float(row.get("endpoint_position_slope") or "nan")
            except ValueError:
                pass
    return out


def read_scaling_metadata() -> Dict[str, float]:
    path = Path("out/plots/metadata/results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.json")
    payload = safe_read_json(str(path))
    if not payload:
        return {}
    summary = payload.get("key_quantitative_summary", {})
    out: Dict[str, float] = {}
    for key in ["max_measured_speedup", "amdahl_serial_fraction_f", "maximum_theoretical_speedup_from_fit"]:
        try:
            out[key] = float(summary.get(key))
        except (TypeError, ValueError):
            continue
    return out


def compute_top_facts(manifest: Dict[str, Any]) -> List[str]:
    facts: List[str] = []

    manifest_paths = flatten_manifest_paths(manifest)
    existing_manifest_paths = [p for p in manifest_paths if file_exists(p)]
    facts.append(
        f"Manifest-linked artifacts found: {len(existing_manifest_paths)}/{len(manifest_paths)} paths currently exist."
    )

    required_figs = [p for _, p, required in CORE_FIGURES if required]
    required_figs_present = [p for p in required_figs if file_exists(p)]
    facts.append(
        f"Core final figures present: {len(required_figs_present)}/{len(required_figs)} required figure files."
    )

    r2 = read_results2_table()
    if r2:
        target_k = 94.4
        vv_mean = r2.get("verlet_mean_t")
        eu_mean = r2.get("euler_mean_t")
        vv_drift = r2.get("verlet_max_drift")
        eu_drift = r2.get("euler_max_drift")
        if vv_mean is not None and eu_mean is not None and vv_drift is not None and eu_drift is not None:
            facts.append(
                "Results 2 brief temperature single-number contrast: "
                f"Verlet mean T={vv_mean:.2f} K (Δ={vv_mean - target_k:+.2f} K), "
                f"Euler mean T={eu_mean:.2f} K (Δ={eu_mean - target_k:+.2f} K)."
            )
            facts.append(
                "Results 2 brief energy drift single-number contrast: "
                f"Verlet max |ΔE/E0|={vv_drift:.3f}%, Euler max |ΔE/E0|={eu_drift:.3f}%."
            )

    slopes = read_results1_slopes()
    if slopes:
        e = slopes.get("euler_endpoint_slope")
        v = slopes.get("verlet_endpoint_slope")
        r = slopes.get("rk4_endpoint_slope")
        if e is not None and v is not None and r is not None:
            facts.append(
                f"Results 1 endpoint convergence slopes: Euler {e:.2f}, Verlet {v:.2f}, RK4 {r:.2f}."
            )

    scaling = read_scaling_metadata()
    if scaling:
        ms = scaling.get("max_measured_speedup")
        sf = scaling.get("amdahl_serial_fraction_f")
        if ms is not None and sf is not None:
            facts.append(f"Results 3 strong scaling: max measured speedup {ms:.2f}x; fitted Amdahl serial fraction f={sf:.4f}.")

    return facts


def deliverables_map() -> Dict[str, List[str]]:
    final_figures: List[str] = []
    for section, path, required in CORE_FIGURES:
        exists = file_exists(path)
        label = "confirmed" if exists else ("not applicable" if not required else "potential issue")
        note = "required" if required else "optional"
        final_figures.append(f"[{label}] {section}: `{path}` ({note})")

    tables: List[str] = []
    for section, path, required in CORE_TABLES:
        exists = file_exists(path)
        label = "confirmed" if exists else ("not applicable" if not required else "potential issue")
        note = "required" if required else "optional"
        tables.append(f"[{label}] {section}: `{path}` ({note})")

    core_deliverables = []
    for path in ["ai/audit_output.md", "ai/results.md", "ai/results_bundle.md", "out/manifest.json"]:
        core_deliverables.append(f"[{status_label(file_exists(path))}] `{path}`")

    diagnostics = []
    meta_dir = Path("out/plots/metadata")
    meta_count = len(list(meta_dir.glob("*.json"))) if meta_dir.exists() else 0
    diagnostics.append(
        f"[informational] `out/plots/metadata/*.json` sidecars present: {meta_count}."
    )
    diagnostics.append(
        f"[informational] Raw run CSV trees under `out/runs/` are primary diagnostics and provenance backing."
    )

    legacy = []
    for old_path, new_path in LEGACY_PLOT_ALIASES.items():
        old_exists = file_exists(old_path)
        new_exists = file_exists(new_path)
        if not old_exists and new_exists:
            legacy.append(f"[expected by design] Legacy filename `{old_path}` replaced by `{new_path}`.")
        elif old_exists and new_exists:
            legacy.append(f"[informational] Both legacy and current filenames exist: `{old_path}` and `{new_path}`.")
        elif old_exists and not new_exists:
            legacy.append(f"[potential issue] Legacy filename exists without current replacement: `{old_path}`.")

    for path in STALE_RESULTS2_ARTIFACTS:
        if file_exists(path):
            legacy.append(f"[potential issue] Stale/removed Results 2 artifact still present: `{path}`.")

    if not legacy:
        legacy.append("[informational] No legacy/stale artifact flags detected.")

    return {
        "final_figures": final_figures,
        "tables": tables,
        "core_deliverables": core_deliverables,
        "diagnostics": diagnostics,
        "legacy": legacy,
    }


def markdown_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def collect_claim_rows(max_rows: int = 10) -> List[List[str]]:
    meta_dir = Path("out/plots/metadata")
    if not meta_dir.exists():
        return [["No metadata sidecars found", "`out/plots/metadata/`", "low", "Metadata files are missing."]]

    priority_order = [
        "results1_figure3_convergence_combined.json",
        "results1_figure2_small_vs_large_dt.json",
        "results2_figure6_lj_brief_energy_100step_production.json",
        "results2_figure7_lj_brief_temperature_100step_production.json",
        "results2_figure8_lj_rdf_comparison_rahman1964.json",
        "results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.json",
        "results3_figure9ab_problem_size_scaling_fixed_p16.json",
    ]

    files = [meta_dir / name for name in priority_order if (meta_dir / name).exists()]
    for candidate in sorted(meta_dir.glob("*.json")):
        if candidate not in files:
            files.append(candidate)

    rows: List[List[str]] = []
    for path in files:
        payload = safe_read_json(str(path))
        if not payload:
            continue

        claim = str(payload.get("claim") or payload.get("intended_claim") or payload.get("purpose") or "").strip()
        if not claim:
            continue

        support_items: List[str] = []
        plot_file = str(payload.get("plot_file_png") or payload.get("figure_filename") or "").strip()
        if plot_file:
            support_items.append(f"`{plot_file}`")
        for src in payload.get("source_data_files", [])[:3]:
            if isinstance(src, str):
                support_items.append(f"`{src}`")
        if not support_items:
            support_items.append(f"`{path.as_posix()}`")

        missing = payload.get("missing_provenance", [])
        sources = [src for src in payload.get("source_data_files", []) if isinstance(src, str)]
        sources_exist = all(file_exists(src) for src in sources) if sources else False

        if sources and sources_exist and not missing:
            confidence = "high"
        elif sources and sources_exist:
            confidence = "medium"
        elif sources:
            confidence = "low"
        else:
            confidence = "medium"

        caveats = payload.get("caveats", [])
        if caveats and isinstance(caveats, list):
            caveat = str(caveats[0])
        elif missing and isinstance(missing, list):
            caveat = str(missing[0])
        else:
            caveat = "No major caveat recorded in metadata."

        rows.append([claim, "; ".join(support_items[:4]), confidence, caveat])
        if len(rows) >= max_rows:
            break

    if not rows:
        rows.append(["No claim metadata found", "`out/plots/metadata/*.json`", "low", "Claim extraction not available."])
    return rows


def freshness_sources_for_doc(doc: str) -> List[str]:
    profile = DOC_PROFILES[doc]
    return list(profile["generation_sources"])


def expected_files_for_doc(doc: str) -> List[Tuple[str, bool, str]]:
    expected: List[Tuple[str, bool, str]] = [("out/manifest.json", True, "project manifest")]

    if doc in {"results", "bundle"}:
        for _section, path, required in CORE_FIGURES:
            if required:
                expected.append((path, True, "core final figure"))
        for _section, path, required in CORE_TABLES:
            if required:
                expected.append((path, True, "core summary/table"))
        expected.append(("out/plots/metadata/results2_figure7_lj_brief_temperature_100step_production.json", True, "metadata sidecar"))
        expected.append(("out/plots/metadata/results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.json", True, "metadata sidecar"))

    if doc == "audit":
        expected.extend(
            [
                ("Makefile", True, "build definition"),
                ("src/main.cpp", True, "core solver source"),
                ("tests/test_runner.cpp", True, "unit-test entry"),
                ("scripts/plot_ho.py", True, "results generator"),
                ("scripts/plot_lj.py", True, "results generator"),
                ("scripts/plot_scaling.py", True, "results generator"),
            ]
        )

    return expected


def latest_mtime(paths: Iterable[str]) -> Optional[float]:
    mtimes: List[float] = []
    for path in paths:
        p = Path(path)
        if p.exists():
            mtimes.append(p.stat().st_mtime)
    return max(mtimes) if mtimes else None


def format_mtime(ts: Optional[float]) -> str:
    if ts is None:
        return "n/a"
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def output_currency_rows(current_doc: Optional[str] = None, current_time: Optional[float] = None) -> List[List[str]]:
    evidence_sources = [path for _sec, path, required in CORE_FIGURES if required]
    evidence_sources += [path for _sec, path, required in CORE_TABLES if required]
    evidence_sources += ["out/manifest.json"]

    latest_evidence = latest_mtime(evidence_sources)
    generator_sources = [
        "ai/audit.sh",
        "ai/make_results.sh",
        "ai/pack_results.sh",
        "ai/analyse_results.py",
        "ai/context_report.py",
    ]
    latest_generator = latest_mtime(generator_sources)

    rows: List[List[str]] = []
    virtual_now = time.time() if current_time is None else current_time
    for path in COMPANION_FILES:
        p = Path(path)
        if current_doc and path == current_doc:
            mtime = virtual_now
            stale_vs_evidence = latest_evidence is not None and mtime + 1e-6 < latest_evidence
            stale_vs_generator = latest_generator is not None and mtime + 1e-6 < latest_generator
            stale = stale_vs_evidence or stale_vs_generator
            note = "appears current (in-progress generation timestamp)" if not stale else "older than latest source/evidence; consider regeneration"
            rows.append(
                [
                    path,
                    format_mtime(mtime),
                    format_mtime(latest_evidence),
                    "confirmed" if not stale else "potential issue",
                    note,
                ]
            )
            continue

        if not p.exists():
            rows.append([path, "missing", format_mtime(latest_evidence), "potential issue", "context file missing"])
            continue

        mtime = p.stat().st_mtime
        stale_vs_evidence = latest_evidence is not None and mtime + 1e-6 < latest_evidence
        stale_vs_generator = latest_generator is not None and mtime + 1e-6 < latest_generator
        stale = stale_vs_evidence or stale_vs_generator
        note = "appears current" if not stale else "older than latest source/evidence; consider regeneration"
        rows.append(
            [
                path,
                format_mtime(mtime),
                format_mtime(latest_evidence),
                "confirmed" if not stale else "potential issue",
                note,
            ]
        )
    return rows


def stale_items() -> List[List[str]]:
    rows: List[List[str]] = []

    for old_path, new_path in LEGACY_PLOT_ALIASES.items():
        old_exists = file_exists(old_path)
        new_exists = file_exists(new_path)
        if not old_exists and new_exists:
            rows.append(["expected by design", f"`{old_path}`", f"Renamed; current artifact is `{new_path}`."])
        elif old_exists and new_exists:
            rows.append(["informational", f"`{old_path}`", f"Legacy and current filenames both exist (`{new_path}`)."])
        elif old_exists and not new_exists:
            rows.append(["potential issue", f"`{old_path}`", "Legacy name exists but expected current replacement is missing."])

    for stale in STALE_RESULTS2_ARTIFACTS:
        if file_exists(stale):
            rows.append(["potential issue", f"`{stale}`", "Deprecated Results 2 extended artifact still present."])

    if Path("scripts/__pycache__").exists():
        rows.append(
            [
                "informational",
                "`scripts/__pycache__/`",
                "Generated cache files may create noisy static-scan results unless excluded.",
            ]
        )

    if not Path("out/summary/results3").exists():
        rows.append(
            [
                "informational",
                "`out/summary/results3/`",
                "Results 3 currently tracked via `out/scaling_*.csv` and metadata JSON sidecars.",
            ]
        )

    if not rows:
        rows.append(["informational", "none", "No stale/informational flags detected."])
    return rows


def project_caveats() -> List[str]:
    return [
        "Lennard-Jones uses a hard cutoff (no potential shift), so small energy discontinuities can occur when pairs cross r_cut.",
        "LJ force evaluation is direct all-pairs O(N^2) without neighbour lists; scaling trends depend strongly on chosen timestep counts.",
        "For Lennard-Jones runs, ranks use particle decomposition and allgather positions before force evaluation; in the fixed-N strong-scaling study, communication fraction rises with process count.",
        "Results 2 reference comparison uses manual Rahman Fig. 2 anchors for part of the curve; treat as qualitative/semi-quantitative.",
        "Strong/size scaling CSVs store aggregated timings rather than all replicate traces, limiting deeper uncertainty analysis.",
        "Artifact naming conventions evolved (including Results 1/2/3 figure renaming); legacy filename checks must be interpreted with rename context.",
    ]


def render_preface(doc: str, generation_status: str, generation_succeeded: bool, generation_note: str, preface_mode: str) -> str:
    profile = DOC_PROFILES[doc]

    if preface_mode == "stub":
        lines: List[str] = []
        lines.append(f"# {profile['title']}")
        lines.append("")
        lines.append("## Context Preface (Stub)")
        lines.append("")
        lines.append("- Shared Executive Summary, Deliverables Map, claims table, and freshness metadata are centralised in `ai/results.md`.")
        lines.append("- This file includes only document-specific sections below.")
        lines.append("- Generation metadata for this document:")
        lines.append("")
        lines.append(
            markdown_table(
                ["Field", "Value"],
                [
                    ["Generation timestamp (UTC)", utc_now()],
                    ["Generation succeeded", fmt_yes_no(generation_succeeded)],
                    ["Generation status label", generation_status],
                    ["Generation note", generation_note],
                ],
            )
        )
        lines.append("")
        lines.append("## Cross-Reference")
        lines.append("")
        lines.append("- Read `ai/results.md` first for shared high-level context.")
        lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    manifest = safe_read_json("out/manifest.json")

    commit = git_commit()
    dirty = git_dirty_count()
    dirty_text = "unknown" if dirty is None else ("clean" if dirty == 0 else f"dirty ({dirty} changed paths)")

    top_facts = compute_top_facts(manifest if manifest else {})
    deliverables = deliverables_map()
    claims = collect_claim_rows()
    freshness_sources = freshness_sources_for_doc(doc)
    expected = expected_files_for_doc(doc)
    currency_rows = output_currency_rows(current_doc=DOC_OUTPUT_PATH.get(doc), current_time=time.time())
    stale_rows = stale_items()

    diagnostics: List[str] = []
    missing_required = [path for path, required, _note in expected if required and not file_exists(path)]
    if missing_required:
        diagnostics.append(
            "[potential issue] Missing required artifacts: " + ", ".join(f"`{path}`" for path in missing_required)
        )
    else:
        diagnostics.append("[confirmed] Required artifacts for this context view were found.")

    stale_outputs = [row[0] for row in currency_rows if row[3] == "potential issue"]
    if stale_outputs:
        diagnostics.append(
            "[potential issue] Context outputs older than latest repo evidence: "
            + ", ".join(f"`{path}`" for path in stale_outputs)
        )
    else:
        diagnostics.append("[confirmed] Context outputs appear current relative to latest tracked evidence.")

    lines: List[str] = []
    lines.append(f"# {profile['title']}")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(markdown_table(
        ["Field", "Value"],
        [
            ["Purpose", str(profile["purpose"])],
            ["Generation timestamp (UTC)", utc_now()],
            ["Git commit", commit],
            ["Git working tree", dirty_text],
            ["Generation succeeded", fmt_yes_no(generation_succeeded)],
            ["Generation status label", generation_status],
            ["Generation note", generation_note],
        ],
    ))
    lines.append("")
    lines.append("### Top Important Current Facts")
    lines.append("")
    for fact in top_facts:
        lines.append(f"- {fact}")
    lines.append("")

    lines.append("## How to Read This File")
    lines.append("")
    lines.append(f"- Authoritative for: {profile['authoritative_for']}")
    lines.append(f"- Less authoritative for: {profile['less_authoritative_for']}")
    lines.append(
        "- Companion files to read with this one: "
        + ", ".join(f"`{path}`" for path in profile["companion_priority"])
        + "."
    )
    lines.append("")

    lines.append("## Authoritative Facts")
    lines.append("")
    lines.append(markdown_table(
        ["Fact", "Status", "Evidence"],
        [
            [
                "Manifest present",
                status_label(file_exists("out/manifest.json")),
                "`out/manifest.json`",
            ],
            [
                "Core required figures present",
                status_label(all(file_exists(path) for _sec, path, req in CORE_FIGURES if req)),
                f"{sum(1 for _sec, path, req in CORE_FIGURES if req and file_exists(path))}/{sum(1 for _sec, _path, req in CORE_FIGURES if req)} required",
            ],
            [
                "Core required tables/data present",
                status_label(all(file_exists(path) for _sec, path, req in CORE_TABLES if req)),
                f"{sum(1 for _sec, path, req in CORE_TABLES if req and file_exists(path))}/{sum(1 for _sec, _path, req in CORE_TABLES if req)} required",
            ],
            [
                "Plot metadata sidecars available",
                "confirmed" if Path("out/plots/metadata").exists() else "potential issue",
                "`out/plots/metadata/*.json`",
            ],
        ],
    ))
    lines.append("")

    lines.append("## Generated Result Summaries (High Value)")
    lines.append("")
    for fact in top_facts:
        lines.append(f"- {fact}")
    lines.append("")

    lines.append("## Current Deliverables Map")
    lines.append("")
    lines.append("### Current final figures")
    for row in deliverables["final_figures"]:
        lines.append(f"- {row}")
    lines.append("")
    lines.append("### Current tables")
    for row in deliverables["tables"]:
        lines.append(f"- {row}")
    lines.append("")
    lines.append("### Core deliverables")
    for row in deliverables["core_deliverables"]:
        lines.append(f"- {row}")
    lines.append("")
    lines.append("### Diagnostics-only artifacts")
    for row in deliverables["diagnostics"]:
        lines.append(f"- {row}")
    lines.append("")
    lines.append("### Deprecated / legacy artifacts")
    for row in deliverables["legacy"]:
        lines.append(f"- {row}")
    lines.append("")

    lines.append("## Report Claims Supported by Current Evidence")
    lines.append("")
    lines.append(markdown_table(
        ["Claim", "Supporting artifacts", "Confidence", "Caveat"],
        claims,
    ))
    lines.append("")

    lines.append("## Freshness / Staleness Metadata")
    lines.append("")
    lines.append("### Source files used to generate this file")
    source_rows: List[List[str]] = []
    for src in freshness_sources:
        exists = file_exists(src)
        source_rows.append([src, fmt_yes_no(exists), file_mtime_utc(src), "confirmed" if exists else "potential issue"])
    lines.append(markdown_table(["Source file", "Found", "Last modified (UTC)", "Status"], source_rows))
    lines.append("")

    lines.append("### Expected file checks")
    expected_rows: List[List[str]] = []
    for path, required, note in expected:
        exists = file_exists(path)
        label = "confirmed" if exists else ("informational" if not required else "potential issue")
        expected_rows.append([path, "required" if required else "optional", note, label])
    lines.append(markdown_table(["Path", "Expectation", "Role", "Status"], expected_rows))
    lines.append("")

    lines.append("### Output currency relative to current repo evidence")
    lines.append(markdown_table(
        ["Context file", "Last modified (UTC)", "Latest evidence mtime (UTC)", "Status", "Note"],
        currency_rows,
    ))
    lines.append("")

    lines.append("## Diagnostics / Warnings")
    lines.append("")
    for item in diagnostics:
        lines.append(f"- {item}")
    lines.append("")

    lines.append("## Known Limitations / Caveats (Project-wide)")
    lines.append("")
    for caveat in project_caveats():
        lines.append(f"- {caveat}")
    lines.append("")

    lines.append("## Potentially Stale or Informational Items")
    lines.append("")
    lines.append(markdown_table(["Status", "Item", "Interpretation"], stale_rows))
    lines.append("")

    lines.append("## Cross-References")
    lines.append("")
    lines.append("- `ai/audit_output.md`: executable build/test/smoke audit and raw source/verbatim evidence.")
    lines.append("- `ai/results.md`: interpreted project-wide results summary and compliance-oriented checks.")
    lines.append("- `ai/results_bundle.md`: raw/truncated artifact bundle for direct context ingestion.")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Render project-wide context prefaces for AI context files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    preface_parser = subparsers.add_parser("preface", help="Render markdown preface for a specific context file.")
    preface_parser.add_argument("--doc", choices=sorted(DOC_PROFILES.keys()), required=True)
    preface_parser.add_argument("--generation-status", default="informational")
    preface_parser.add_argument("--generation-succeeded", default="true")
    preface_parser.add_argument("--generation-note", default="generation completed")
    preface_parser.add_argument("--preface-mode", choices=["full", "stub"], default="full")

    args = parser.parse_args()

    if args.command == "preface":
        succeeded = parse_bool(args.generation_succeeded)
        print(
            render_preface(
                doc=args.doc,
                generation_status=args.generation_status.strip() or "informational",
                generation_succeeded=succeeded,
                generation_note=args.generation_note.strip() or "generation completed",
                preface_mode=args.preface_mode,
            ),
            end="",
        )
        return

    raise RuntimeError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
