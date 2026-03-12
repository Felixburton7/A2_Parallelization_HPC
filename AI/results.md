# Results Summary — WA2 MPI MD Solver

## Executive Summary

| Field | Value |
|---|---|
| Purpose | Project-wide interpreted summary of Results 1/2/3 from existing generated artifacts. |
| Generation timestamp (UTC) | 2026-03-12T11:55:09Z |
| Git commit | af72d143d0f35acbc02c67bcb510cf7ebd473543 |
| Git working tree | dirty (5 changed paths) |
| Generation succeeded | yes |
| Generation status label | confirmed |
| Generation note | Report-writing oriented analysis generated from current manifest-linked outputs. |

### Top Important Current Facts

- Manifest-linked artifacts found: 44/44 paths currently exist.
- Core final figures present: 9/9 required figure files.
- Results 2 brief temperature single-number contrast: Verlet mean T=94.42 K (Δ=+0.02 K), Euler mean T=185.27 K (Δ=+90.87 K).
- Results 2 brief energy drift single-number contrast: Verlet max |ΔE/E0|=0.082%, Euler max |ΔE/E0|=127.587%.
- Results 1 endpoint convergence slopes: Euler 1.05, Verlet 2.00, RK4 3.94.
- Results 3 strong scaling: max measured speedup 24.12x; fitted Amdahl serial fraction f=0.0103.

## How to Read This File

- Authoritative for: Interpretation-ready summaries, key metrics, and evidence linkage across assignment outputs.
- Less authoritative for: Full raw traces/logs and complete CSV payloads.
- Companion files to read with this one: `ai/results_bundle.md`, `ai/audit_output.md`.

## Authoritative Facts

| Fact | Status | Evidence |
|---|---|---|
| Manifest present | confirmed | `out/manifest.json` |
| Core required figures present | confirmed | 9/9 required |
| Core required tables/data present | confirmed | 8/8 required |
| Plot metadata sidecars available | confirmed | `out/plots/metadata/*.json` |

## Generated Result Summaries (High Value)

- Manifest-linked artifacts found: 44/44 paths currently exist.
- Core final figures present: 9/9 required figure files.
- Results 2 brief temperature single-number contrast: Verlet mean T=94.42 K (Δ=+0.02 K), Euler mean T=185.27 K (Δ=+90.87 K).
- Results 2 brief energy drift single-number contrast: Verlet max |ΔE/E0|=0.082%, Euler max |ΔE/E0|=127.587%.
- Results 1 endpoint convergence slopes: Euler 1.05, Verlet 2.00, RK4 3.94.
- Results 3 strong scaling: max measured speedup 24.12x; fitted Amdahl serial fraction f=0.0103.

## Current Deliverables Map

### Current final figures
- [confirmed] Results 1: `out/plots/results1_figure1ab.png` (required)
- [confirmed] Results 1: `out/plots/results1_figure1c.png` (required)
- [confirmed] Results 1: `out/plots/results1_figure2.png` (required)
- [confirmed] Results 1: `out/plots/results1_figure3.png` (required)
- [confirmed] Results 1: `out/plots/results1_figure4.png` (optional)
- [confirmed] Results 2: `out/plots/results2_figure6.png` (required)
- [confirmed] Results 2: `out/plots/results2_figure7.png` (required)
- [confirmed] Results 2: `out/plots/results2_figure8.png` (required)
- [confirmed] Results 3: `out/plots/results3_figure10abc.png` (required)
- [confirmed] Results 3: `out/plots/results3_figure9ab.png` (required)

### Current tables
- [confirmed] Manifest: `out/manifest.json` (required)
- [confirmed] Results 1: `out/summary/results1/results1_ho_convergence_summary.csv` (required)
- [confirmed] Results 1: `out/summary/results1/results1_ho_small_large_summary.csv` (required)
- [confirmed] Results 1: `out/summary/results1/results1_ho_endpoint_values.csv` (required)
- [confirmed] Results 2: `out/summary/results2/results2_quantitative_summary_table.csv` (required)
- [confirmed] Results 2: `out/summary/results2/results2_quantitative_summary_table.md` (required)
- [confirmed] Results 3: `out/scaling_strong.csv` (required)
- [confirmed] Results 3: `out/scaling_size.csv` (required)

### Core deliverables
- [confirmed] `ai/audit_output.md`
- [confirmed] `ai/results.md`
- [confirmed] `ai/results_bundle.md`
- [confirmed] `out/manifest.json`

### Diagnostics-only artifacts
- [informational] `out/plots/metadata/*.json` sidecars present: 10.
- [informational] Raw run CSV trees under `out/runs/` are primary diagnostics and provenance backing.

### Deprecated / legacy artifacts
- [expected by design] Legacy filename `out/plots/results1_ho_position_velocity_trajectories.png` replaced by `out/plots/results1_figure1ab.png`.
- [expected by design] Legacy filename `out/plots/results1_ho_phase_space_trajectories.png` replaced by `out/plots/results1_figure1c.png`.
- [expected by design] Legacy filename `out/plots/results1_ho_convergence_endpoint_position_error.png` replaced by `out/plots/results1_figure3.png`.
- [expected by design] Legacy filename `out/plots/results1_ho_convergence_rms_phase_space_error.png` replaced by `out/plots/results1_figure3.png`.
- [expected by design] Legacy filename `out/plots/results1_ho_energy_conservation.png` replaced by `out/plots/results1_figure4.png`.

## Report Claims Supported by Current Evidence

| Claim | Supporting artifacts | Confidence | Caveat |
|---|---|---|---|
| Demonstrates first-, second-, and fourth-order convergence using endpoint and RMS phase-space metrics. | `out/plots/results1_figure3.png` | medium | No major caveat recorded in metadata. |
| Direct small-vs-large timestep comparison with full-range coarse behaviour retained; quantitative error values are reported in summary tables. | `out/plots/results1_figure2.png` | medium | No major caveat recorded in metadata. |
| At the required run length, Velocity-Verlet gives a physically meaningful bounded NVE trajectory in total energy; Forward Euler shows strong total-energy drift and is unreliable. | `out/plots/results2_figure6.png`; `out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329/lj_verlet.csv`; `out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329/lj_euler.csv` | high | Relative drift is computed from total energy with E0 taken at the first finite production frame. |
| Velocity-Verlet remains close to the target state while Forward Euler heats strongly over the same required window. | `out/plots/results2_figure7.png`; `out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329/lj_verlet.csv`; `out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329/lj_euler.csv` | high | Temperature is shown only for finite values; divergent tails are omitted. |
| The present Velocity-Verlet RDF reproduces liquid-argon shell structure (first peak, first minimum, second shell, long-range trend) with qualitative/semi-quantitative agreement to Rahman (1964), while peak heights are somewhat reduced. | `out/plots/results2_figure8.png`; `out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/gr.csv`; `out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/lj_verlet.csv`; `out/summary/results2/rahman1964_fig2_manual_anchors.csv` | high | Rahman comparison uses a manually extracted approximate reference guide from printed Fig. 2. |
| The MPI implementation achieves strong-scaling gains while critical-path communication (max rank communication time) contributes a measurable share of runtime. | `out/plots/results3_figure10abc.png`; `out/scaling_strong.csv`; `out/scaling_meta.txt` | medium | Strong-scaling data are aggregated medians, not raw replicate traces. |
| Runtime grows approximately as a power law near O(N^2) while communication fraction changes with size at fixed P=16. | `out/plots/results3_figure9ab.png`; `out/scaling_size.csv`; `out/scaling_meta.txt` | medium | Power-law exponents depend on the chosen fit domain (here N >= 500). |
| Shows position and velocity trajectories at dt=0.01 for Euler, Velocity-Verlet, RK4 versus exact. | `out/plots/results1_figure1ab.png` | medium | No major caveat recorded in metadata. |
| Shows phase-space geometry at dt=0.01 and qualitative orbit preservation differences. | `out/plots/results1_figure1c.png` | medium | No major caveat recorded in metadata. |
| Supporting diagnostic: Euler shows strong drift, Velocity-Verlet bounded oscillatory error, RK4 tiny drift on this interval. | `out/plots/results1_figure4.png` | medium | No major caveat recorded in metadata. |

## Freshness / Staleness Metadata

### Source files used to generate this file
| Source file | Found | Last modified (UTC) | Status |
|---|---|---|---|
| ai/make_results.sh | yes | 2026-03-12T11:53:11Z | confirmed |
| ai/report_writer_context.py | yes | 2026-03-12T11:54:53Z | confirmed |
| ai/analyse_results.py | yes | 2026-03-11T16:20:36Z | confirmed |
| ai/context_report.py | yes | 2026-03-12T11:53:16Z | confirmed |
| out/manifest.json | yes | 2026-03-11T12:01:14Z | confirmed |
| out/plots/metadata/results2_figure7.json | yes | 2026-03-11T12:01:13Z | confirmed |
| out/plots/metadata/results3_figure10abc.json | yes | 2026-03-11T12:01:13Z | confirmed |

### Expected file checks
| Path | Expectation | Role | Status |
|---|---|---|---|
| out/manifest.json | required | project manifest | confirmed |
| out/plots/results1_figure1ab.png | required | core final figure | confirmed |
| out/plots/results1_figure1c.png | required | core final figure | confirmed |
| out/plots/results1_figure2.png | required | core final figure | confirmed |
| out/plots/results1_figure3.png | required | core final figure | confirmed |
| out/plots/results2_figure6.png | required | core final figure | confirmed |
| out/plots/results2_figure7.png | required | core final figure | confirmed |
| out/plots/results2_figure8.png | required | core final figure | confirmed |
| out/plots/results3_figure10abc.png | required | core final figure | confirmed |
| out/plots/results3_figure9ab.png | required | core final figure | confirmed |
| out/manifest.json | required | core summary/table | confirmed |
| out/summary/results1/results1_ho_convergence_summary.csv | required | core summary/table | confirmed |
| out/summary/results1/results1_ho_small_large_summary.csv | required | core summary/table | confirmed |
| out/summary/results1/results1_ho_endpoint_values.csv | required | core summary/table | confirmed |
| out/summary/results2/results2_quantitative_summary_table.csv | required | core summary/table | confirmed |
| out/summary/results2/results2_quantitative_summary_table.md | required | core summary/table | confirmed |
| out/scaling_strong.csv | required | core summary/table | confirmed |
| out/scaling_size.csv | required | core summary/table | confirmed |
| out/plots/metadata/results2_figure7.json | required | metadata sidecar | confirmed |
| out/plots/metadata/results3_figure10abc.json | required | metadata sidecar | confirmed |

### Output currency relative to current repo evidence
| Context file | Last modified (UTC) | Latest evidence mtime (UTC) | Status | Note |
|---|---|---|---|---|
| ai/audit_output.md | 2026-03-12T11:55:08Z | 2026-03-11T12:01:15Z | confirmed | appears current |
| ai/results.md | 2026-03-12T11:55:09Z | 2026-03-11T12:01:15Z | confirmed | appears current (in-progress generation timestamp) |
| ai/results_bundle.md | 2026-03-12T11:55:08Z | 2026-03-11T12:01:15Z | confirmed | appears current |

## Diagnostics / Warnings

- [confirmed] Required artifacts for this context view were found.
- [confirmed] Context outputs appear current relative to latest tracked evidence.

## Known Limitations / Caveats (Project-wide)

- Lennard-Jones uses a hard cutoff (no potential shift), so small energy discontinuities can occur when pairs cross r_cut.
- LJ force evaluation is direct all-pairs O(N^2) without neighbour lists; scaling trends depend strongly on chosen timestep counts.
- For Lennard-Jones runs, ranks use particle decomposition and allgather positions before force evaluation; in the fixed-N strong-scaling study, communication fraction rises with process count.
- Results 2 reference comparison uses manual Rahman Fig. 2 anchors for part of the curve; treat as qualitative/semi-quantitative.
- Strong/size scaling CSVs store aggregated timings rather than all replicate traces, limiting deeper uncertainty analysis.
- Artifact naming conventions evolved (including Results 1/2/3 figure renaming); legacy filename checks must be interpreted with rename context.

## Potentially Stale or Informational Items

| Status | Item | Interpretation |
|---|---|---|
| expected by design | `out/plots/results1_ho_position_velocity_trajectories.png` | Renamed; current artifact is `out/plots/results1_figure1ab.png`. |
| expected by design | `out/plots/results1_ho_phase_space_trajectories.png` | Renamed; current artifact is `out/plots/results1_figure1c.png`. |
| expected by design | `out/plots/results1_ho_convergence_endpoint_position_error.png` | Renamed; current artifact is `out/plots/results1_figure3.png`. |
| expected by design | `out/plots/results1_ho_convergence_rms_phase_space_error.png` | Renamed; current artifact is `out/plots/results1_figure3.png`. |
| expected by design | `out/plots/results1_ho_energy_conservation.png` | Renamed; current artifact is `out/plots/results1_figure4.png`. |
| informational | `scripts/__pycache__/` | Generated cache files may create noisy static-scan results unless excluded. |
| informational | `out/summary/results3/` | Results 3 currently tracked via `out/scaling_*.csv` and metadata JSON sidecars. |

## Cross-References

- `ai/audit_output.md`: executable build/test/smoke audit and raw source/verbatim evidence.
- `ai/results.md`: interpreted project-wide results summary and compliance-oriented checks.
- `ai/results_bundle.md`: raw/truncated artifact bundle for direct context ingestion.

## 0) Report-Writing Pack

This section is tuned for drafting the Results section itself: what to say first, which numbers to quote, what caveats must stay attached to those numbers, and where the current evidence is strongest.

### Writeup-Aligned Structure

1. Results 1 - Harmonic oscillator verification.
   - Use Fig. 1 for the qualitative distinction between trajectory overlap and phase-space geometry at dt=0.01.
   - Use Fig. 2 as the timestep-sensitivity contrast, Fig. 3 plus the convergence table for formal order, and Fig. 4 as supporting energy evidence rather than the primary proof.
2. Results 2 - Lennard-Jones argon.
   - Keep the required 100-step production run (energy and temperature) separate from the 20,000-step RDF validation run.
   - Say explicitly that step 0 in the CSV is the production initial frame after startup/equilibration.
3. Results 3 - scaling.
   - State the actual timing configuration used for the current dataset: strong scaling uses 500 timed steps and size scaling uses 2000 timed steps, using 20 repetitions per point.
   - That configuration comes from `scripts/run_all_data.sh`; it is not encoded in the scaling CSV headers.

### Report-Ready Quantitative Anchors

#### Results 1 - Harmonic oscillator
- Convergence slopes from the Results 1 summary: Euler 1.05, Velocity-Verlet 2.00, RK4 3.94 for endpoint error; Euler 1.03, Velocity-Verlet 2.00, RK4 4.00 for RMS phase-space error.
- Representative endpoint position error at dt=0.01: Euler 0.043, Velocity-Verlet 2.267e-05, RK4 4.475e-10.
- Energy drift at dt=0.01 from the small-vs-large summary: Euler max |dE/E0| = 10.517%, Velocity-Verlet = 0.00250%, RK4 = 0.000000%.
- Smallest RK4 endpoint error currently tabulated is 3.553e-15 at dt=5.0000e-04, which supports the machine-precision-floor discussion.

#### Results 2 - Lennard-Jones argon
- Required-run semantics from the figure metadata: 100 production steps, 1.0 ps, startup/equilibration completed before production, and step 0 is the production initial frame.
- Required-run energy comparison: Velocity-Verlet max |dE/E0| = 0.082% (mean 0.033%; final 0.026%), while Euler reaches 127.587% (mean 39.788%).
- Required-run temperature comparison: Velocity-Verlet mean 94.42 K (std 1.43 K; range 92.39-97.81 K), while Euler mean 185.27 K and reaches 396.05 K.
- RDF anchors from the long Validation run: first peak r/sigma=1.090, g=2.838; first minimum r/sigma=1.550, g=0.623; second peak r/sigma=2.070, g=1.253; tail mean g(r>4sigma)=1.0024.

#### Results 3 - scaling
- Current timing dataset configuration from `scripts/run_all_data.sh`: strong scaling uses 500 steps, size scaling uses 2000 steps, 20 repetitions per point.
- Strong scaling anchors: P=8 gives speedup 7.55 and efficiency 0.944; P=32 gives speedup 24.12 and efficiency 0.754. The fitted Amdahl parameter is f=0.0103.
- Strong-scaling communication fraction rises from 1.1% at P=2 to 15.2% at P=32.
- Size-scaling anchors: wall time scales approximately as N^1.85 and wall-minus-comm scales as N^1.93 over the fit domain [500, 864, 1372, 2048].
- Communication fraction at fixed P=16 ranges from 13.1% to 50.8% across the tested N values.

### Figure and Table Support Map

| Subsection | Primary artifact(s) | Best use in the report | Exact anchors to lift | Caveat to retain |
|---|---|---|---|---|
| Results 1 opening paragraph | `results1_figure1ab.png`, `results1_figure1c.png` | Separate near-overlap in x(t), v(t) from geometric orbit quality. | dt=0.01, Euler is still the visibly worst method; Velocity-Verlet remains near-closed in phase space; RK4 is nearly exact. | This figure is qualitative; formal order comes from Fig. 3, not Fig. 1. |
| Results 1 timestep sensitivity | `results1_figure2.png`, `results1_ho_small_large_summary.csv` | Show that coarse-step behaviour separates structural stability from accuracy. | At dt=0.5 Euler is unstable, Velocity-Verlet remains bounded, RK4 stays accurate; dt=0.01 errors are tabulated separately. | Do not use dt=0.5 points in the convergence-fit claim. |
| Results 1 convergence paragraph | `results1_figure3.png`, `results1_ho_convergence_summary.csv`, `results1_ho_endpoint_values.csv` | Main proof of first/second/fourth-order behaviour. | Endpoint slopes 1.05, 2.00, 3.94; RMS slopes 1.03, 2.00, 4.00; RK4 floor at 3.6e-15 for dt=5e-4. | State the fit rule: dt <= 0.1, with coarse points retained only for context. |
| Results 1 energy paragraph | `results1_figure4.png` | Supporting evidence for long-time structure preservation. | At dt=0.01, Euler max |dE/E0| = 10.52%; Velocity-Verlet = 0.00250%; RK4 = 1.39e-11%. | Use this as structural support, not as the only accuracy argument. |
| Results 2 required-run paragraph | `results2_figure6.png`, `results2_figure7.png`, `results2_quantitative_summary_table.md` | Main evidence that Velocity-Verlet is production-usable and Euler is not. | Velocity-Verlet max |dE/E0| = 0.082%; Euler = 127.587%; mean temperatures 94.42 K vs 185.27 K; Euler max temperature 396.05 K. | State that this is the required 100-step, 1 ps production run and that step 0 is the production initial frame. |
| Results 2 RDF paragraph | `results2_figure8.png`, `rahman1964_fig2_manual_anchors.csv` | Structural validation against Rahman-style shell locations. | First peak 1.09 / 2.838, first minimum 1.55 / 0.623, second peak 2.07 / 1.253, tail mean 1.002. | Keep the wording qualitative or semi-quantitative because the Rahman guide is manually anchored. |
| Results 3 strong scaling | `results3_figure10abc.png`, `scaling_strong.csv` | Main performance figure for speedup, efficiency, and communication growth. | S(32)=24.12, E(32)=0.754, fitted f=0.0103, comm fraction 1.1% at P=2 to 15.2% at P=32. | Amdahl f is an empirical descriptor of the measured curve, not a literal machine-independent serial fraction. |
| Results 3 size scaling | `results3_figure9ab.png`, `scaling_size.csv` | Show near-O(N^2) growth and falling communication fraction at larger N. | Wall ~ N^1.85, wall-minus-comm ~ N^1.93, communication fraction 50.8% down to 13.1%. | Say explicitly that the power-law fit is over N >= 500, not all N values. |

### Stronger Presentation Opportunities

- Tighten the Lennard-Jones temperature wording to the exact measured maximum (`396.05 K`) if you want a more precise claim than `~400 K`.
- Fix the scaling-methods/results wording if it still says `100 steps`: the current dataset comes from 500 strong-scaling steps and 2000 size-scaling steps.
- If you want stronger Results 3 uncertainty reporting, cite `out/scaling_strong_stats.csv` and `out/scaling_size_stats.csv` or add IQR/error bars; the headline plots use median timings.
- Keep the RDF paragraph explicitly separate from the required 100-step run; otherwise the reader can incorrectly infer that g(r) came from the brief-mandated 1 ps trajectory.
- If space is tight, Fig. 4 can be shortened to a supporting sentence because Fig. 3 already carries the formal-order argument.
- If you want more implementation-context support while writing, `results_bundle.md` should include the plot-metadata JSON files and targeted figure-script excerpts after regeneration.

### Guardrails Against Overclaiming

- Do not describe the Rahman comparison as exact agreement; the present reference curve is a transparent manual guide, not tabulated truth data.
- Do not describe the fitted Amdahl parameter as a literal serial fraction of the code in a machine-independent sense.
- Do not say the size-scaling exponent uses all tested N values; the current fit domain is N >= 500.
- Do not say RK4 is the best production MD integrator overall just because it has the smallest short-time truncation error; your own evidence also shows the importance of symplectic structure and communication cost.
- Do not silently state `100 steps` for the scaling dataset unless you regenerate the timings with that configuration.

## Generated Result Summaries (Detailed)

The section below is the detailed verbatim analyzer output from `ai/analyse_results.py`.

## A) Provenance

### out/manifest.json
```json
{
  "ho_convergence": {
    "euler_dt1_0": "out/runs/ho_N1_euler_dt1.0_20260308_182329/ho_euler.csv",
    "euler_dt0_5": "out/runs/ho_N1_euler_dt0.5_20260308_182329/ho_euler.csv",
    "euler_dt0_1": "out/runs/ho_N1_euler_dt0.1_20260308_182329/ho_euler.csv",
    "euler_dt0_05": "out/runs/ho_N1_euler_dt0.05_20260308_182329/ho_euler.csv",
    "euler_dt0_01": "out/runs/ho_N1_euler_dt0.01_20260308_182329/ho_euler.csv",
    "euler_dt0_005": "out/runs/ho_N1_euler_dt0.005_20260308_182329/ho_euler.csv",
    "euler_dt0_001": "out/runs/ho_N1_euler_dt0.001_20260308_182329/ho_euler.csv",
    "euler_dt0_0005": "out/runs/ho_N1_euler_dt0.0005_20260308_182329/ho_euler.csv",
    "verlet_dt1_0": "out/runs/ho_N1_verlet_dt1.0_20260308_182329/ho_verlet.csv",
    "verlet_dt0_5": "out/runs/ho_N1_verlet_dt0.5_20260308_182329/ho_verlet.csv",
    "verlet_dt0_1": "out/runs/ho_N1_verlet_dt0.1_20260308_182329/ho_verlet.csv",
    "verlet_dt0_05": "out/runs/ho_N1_verlet_dt0.05_20260308_182329/ho_verlet.csv",
    "verlet_dt0_01": "out/runs/ho_N1_verlet_dt0.01_20260308_182329/ho_verlet.csv",
    "verlet_dt0_005": "out/runs/ho_N1_verlet_dt0.005_20260308_182329/ho_verlet.csv",
    "verlet_dt0_001": "out/runs/ho_N1_verlet_dt0.001_20260308_182329/ho_verlet.csv",
    "verlet_dt0_0005": "out/runs/ho_N1_verlet_dt0.0005_20260308_182329/ho_verlet.csv",
    "rk4_dt1_0": "out/runs/ho_N1_rk4_dt1.0_20260308_182329/ho_rk4.csv",
    "rk4_dt0_5": "out/runs/ho_N1_rk4_dt0.5_20260308_182329/ho_rk4.csv",
    "rk4_dt0_1": "out/runs/ho_N1_rk4_dt0.1_20260308_182329/ho_rk4.csv",
    "rk4_dt0_05": "out/runs/ho_N1_rk4_dt0.05_20260308_182329/ho_rk4.csv",
    "rk4_dt0_01": "out/runs/ho_N1_rk4_dt0.01_20260308_182329/ho_rk4.csv",
    "rk4_dt0_005": "out/runs/ho_N1_rk4_dt0.005_20260308_182329/ho_rk4.csv",
    "rk4_dt0_001": "out/runs/ho_N1_rk4_dt0.001_20260308_182329/ho_rk4.csv",
    "rk4_dt0_0005": "out/runs/ho_N1_rk4_dt0.0005_20260308_182329/ho_rk4.csv"
  },
  "lj_brief": {
    "verlet": "out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329/lj_verlet.csv",
    "euler": "out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329/lj_euler.csv"
  },
  "scaling": {
    "strong": "out/scaling_strong.csv",
    "size": "out/scaling_size.csv"
  },
  "results2_outputs": {
    "generated_utc": "2026-03-11T12:01:14Z",
    "main_report_figures": [
      "out/plots/results2_figure6.png",
      "out/plots/results2_figure7.png",
      "out/plots/results2_figure8.png"
    ],
    "main_report_tables": [
      "out/summary/results2/results2_quantitative_summary_table.md",
      "out/summary/results2/results2_quantitative_summary_table.csv",
      "out/summary/results2/results2_quantitative_summary_table.json"
    ],
    "rahman_reference_dataset": "out/summary/results2/rahman1964_fig2_manual_anchors.csv",
    "notes": [
      "out/summary/results2/results2_report_note.md",
      "out/summary/results2/results2_recommended_figure_set.md",
      "out/summary/results2/results2_rahman_extraction_note.md",
      "out/summary/results2/results2_what_changed_and_why.md"
    ],
    "plot_metadata_files": [
      "out/plots/metadata/results2_figure6.json",
      "out/plots/metadata/results2_figure7.json",
      "out/plots/metadata/results2_figure8.json"
    ]
  },
  "lj_rdf": {
    "verlet_long": "out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/gr.csv",
    "verlet_long_energy": "out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/lj_verlet.csv"
  }
}
```

### File Verification

- `ho_convergence.euler_dt1_0` → `out/runs/ho_N1_euler_dt1.0_20260308_182329/ho_euler.csv` — confirmed
- `ho_convergence.euler_dt0_5` → `out/runs/ho_N1_euler_dt0.5_20260308_182329/ho_euler.csv` — confirmed
- `ho_convergence.euler_dt0_1` → `out/runs/ho_N1_euler_dt0.1_20260308_182329/ho_euler.csv` — confirmed
- `ho_convergence.euler_dt0_05` → `out/runs/ho_N1_euler_dt0.05_20260308_182329/ho_euler.csv` — confirmed
- `ho_convergence.euler_dt0_01` → `out/runs/ho_N1_euler_dt0.01_20260308_182329/ho_euler.csv` — confirmed
- `ho_convergence.euler_dt0_005` → `out/runs/ho_N1_euler_dt0.005_20260308_182329/ho_euler.csv` — confirmed
- `ho_convergence.euler_dt0_001` → `out/runs/ho_N1_euler_dt0.001_20260308_182329/ho_euler.csv` — confirmed
- `ho_convergence.euler_dt0_0005` → `out/runs/ho_N1_euler_dt0.0005_20260308_182329/ho_euler.csv` — confirmed
- `ho_convergence.verlet_dt1_0` → `out/runs/ho_N1_verlet_dt1.0_20260308_182329/ho_verlet.csv` — confirmed
- `ho_convergence.verlet_dt0_5` → `out/runs/ho_N1_verlet_dt0.5_20260308_182329/ho_verlet.csv` — confirmed
- `ho_convergence.verlet_dt0_1` → `out/runs/ho_N1_verlet_dt0.1_20260308_182329/ho_verlet.csv` — confirmed
- `ho_convergence.verlet_dt0_05` → `out/runs/ho_N1_verlet_dt0.05_20260308_182329/ho_verlet.csv` — confirmed
- `ho_convergence.verlet_dt0_01` → `out/runs/ho_N1_verlet_dt0.01_20260308_182329/ho_verlet.csv` — confirmed
- `ho_convergence.verlet_dt0_005` → `out/runs/ho_N1_verlet_dt0.005_20260308_182329/ho_verlet.csv` — confirmed
- `ho_convergence.verlet_dt0_001` → `out/runs/ho_N1_verlet_dt0.001_20260308_182329/ho_verlet.csv` — confirmed
- `ho_convergence.verlet_dt0_0005` → `out/runs/ho_N1_verlet_dt0.0005_20260308_182329/ho_verlet.csv` — confirmed
- `ho_convergence.rk4_dt1_0` → `out/runs/ho_N1_rk4_dt1.0_20260308_182329/ho_rk4.csv` — confirmed
- `ho_convergence.rk4_dt0_5` → `out/runs/ho_N1_rk4_dt0.5_20260308_182329/ho_rk4.csv` — confirmed
- `ho_convergence.rk4_dt0_1` → `out/runs/ho_N1_rk4_dt0.1_20260308_182329/ho_rk4.csv` — confirmed
- `ho_convergence.rk4_dt0_05` → `out/runs/ho_N1_rk4_dt0.05_20260308_182329/ho_rk4.csv` — confirmed
- `ho_convergence.rk4_dt0_01` → `out/runs/ho_N1_rk4_dt0.01_20260308_182329/ho_rk4.csv` — confirmed
- `ho_convergence.rk4_dt0_005` → `out/runs/ho_N1_rk4_dt0.005_20260308_182329/ho_rk4.csv` — confirmed
- `ho_convergence.rk4_dt0_001` → `out/runs/ho_N1_rk4_dt0.001_20260308_182329/ho_rk4.csv` — confirmed
- `ho_convergence.rk4_dt0_0005` → `out/runs/ho_N1_rk4_dt0.0005_20260308_182329/ho_rk4.csv` — confirmed
- `lj_brief.verlet` → `out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329/lj_verlet.csv` — confirmed
- `lj_brief.euler` → `out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329/lj_euler.csv` — confirmed
- `scaling.strong` → `out/scaling_strong.csv` — confirmed
- `scaling.size` → `out/scaling_size.csv` — confirmed
- `results2_outputs.generated_utc` → `2026-03-11T12:01:14Z` — informational
- `results2_outputs.rahman_reference_dataset` → `out/summary/results2/rahman1964_fig2_manual_anchors.csv` — confirmed
- `lj_rdf.verlet_long` → `out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/gr.csv` — confirmed
- `lj_rdf.verlet_long_energy` → `out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/lj_verlet.csv` — confirmed

## B) Results 1: Harmonic Oscillator

### HO Convergence Analysis

| Integrator | dt | x_num(T=10) | |x error| |
|------------|-----|-------------|----------|
| euler | 1 | 0.0000000000e+00 | 8.3907e-01 |
| euler | 0.5 | -9.2060918808e+00 | 8.3670e+00 |
| euler | 0.1 | -1.4088469829e+00 | 5.6978e-01 |
| euler | 0.05 | -1.0828263574e+00 | 2.4375e-01 |
| euler | 0.01 | -8.8228001820e-01 | 4.3208e-02 |
| euler | 0.005 | -8.6035893618e-01 | 2.1287e-02 |
| euler | 0.001 | -8.4327921300e-01 | 4.2077e-03 |
| euler | 0.0005 | -8.4117228641e-01 | 2.1008e-03 |
| verlet | 1 | -5.0000000000e-01 | 3.3907e-01 |
| verlet | 0.5 | -7.7604104164e-01 | 6.3030e-02 |
| verlet | 0.1 | -8.3679492711e-01 | 2.2766e-03 |
| verlet | 0.05 | -8.3850422560e-01 | 5.6730e-04 |
| verlet | 0.01 | -8.3904886055e-01 | 2.2669e-05 |
| verlet | 0.005 | -8.3906586213e-01 | 5.6669e-06 |
| verlet | 0.001 | -8.3907130240e-01 | 2.2668e-07 |
| verlet | 0.0005 | -8.3907147241e-01 | 5.6669e-08 |
| rk4 | 1 | -8.1661815660e-01 | 2.2453e-02 |
| rk4 | 0.5 | -8.3987910923e-01 | 8.0758e-04 |
| rk4 | 0.1 | -8.3907546441e-01 | 3.9353e-06 |
| rk4 | 0.05 | -8.3907179396e-01 | 2.6489e-07 |
| rk4 | 0.01 | -8.3907152952e-01 | 4.4751e-10 |
| rk4 | 0.005 | -8.3907152910e-01 | 2.8151e-11 |
| rk4 | 0.001 | -8.3907152908e-01 | 5.2514e-14 |
| rk4 | 0.0005 | -8.3907152908e-01 | 3.5527e-15 |

**Velocity convergence at T=10:**
| Integrator | dt | v_num(T=10) | |v error| |
|------------|-----|-------------|----------|
| euler | 1 | -3.2000000000e+01 | 3.2544e+01 |
| euler | 0.5 | -1.4085617065e+00 | 1.9526e+00 |
| euler | 0.1 | 8.4850692876e-01 | 3.0449e-01 |
| euler | 0.05 | 6.8933296355e-01 | 1.4531e-01 |
| euler | 0.01 | 5.7161819607e-01 | 2.7597e-02 |
| euler | 0.005 | 5.5772120301e-01 | 1.3700e-02 |
| euler | 0.001 | 5.4674521576e-01 | 2.7241e-03 |
| euler | 0.0005 | 5.4538216400e-01 | 1.3611e-03 |
| verlet | 1 | 7.5000000000e-01 | 2.0598e-01 |
| verlet | 0.5 | 6.1065561722e-01 | 6.6635e-02 |
| verlet | 0.1 | 5.4683161424e-01 | 2.8105e-03 |
| verlet | 0.05 | 5.4472478784e-01 | 7.0368e-04 |
| verlet | 0.01 | 5.4404927138e-01 | 2.8160e-05 |
| verlet | 0.005 | 5.4402815112e-01 | 7.0402e-06 |
| verlet | 0.001 | 5.4402139250e-01 | 2.8161e-07 |
| verlet | 0.0005 | 5.4402118129e-01 | 7.0403e-08 |
| rk4 | 1 | 4.6694988177e-01 | 7.7071e-02 |
| rk4 | 0.5 | 5.3889407562e-01 | 5.1270e-03 |
| rk4 | 0.1 | 5.4401376625e-01 | 7.3446e-06 |
| rk4 | 0.05 | 5.4402066246e-01 | 4.4843e-07 |
| rk4 | 0.01 | 5.4402111019e-01 | 7.0298e-10 |
| rk4 | 0.005 | 5.4402111085e-01 | 4.3822e-11 |
| rk4 | 0.001 | 5.4402111089e-01 | 6.6724e-14 |
| rk4 | 0.0005 | 5.4402111089e-01 | 1.2212e-15 |

**Fitted convergence slopes (log-log on |x(T=10)-x_exact|):**

- euler: slope = 1.05 (expected 1); fit dt = [0.0005, 0.001, 0.005, 0.01, 0.05, 0.1]
- verlet: slope = 2.00 (expected 2); fit dt = [0.0005, 0.001, 0.005, 0.01, 0.05, 0.1]
- rk4: slope = 3.94 (expected 4); fit dt = [0.001, 0.005, 0.01, 0.05, 0.1]

**Whole-trajectory RMS phase-space convergence slopes:**

- euler: slope = 1.03 (expected 1); fit dt = [0.0005, 0.001, 0.005, 0.01, 0.05, 0.1]
- verlet: slope = 2.00 (expected 2); fit dt = [0.0005, 0.001, 0.005, 0.01, 0.05, 0.1]
- rk4: slope = 4.00 (expected 4); fit dt = [0.0005, 0.001, 0.005, 0.01, 0.05, 0.1]

**Energy conservation diagnostic (dt≈0.01):**
- euler: max |ΔE/E0| = 10.516539% (dt≈0.01)
- verlet: max |ΔE/E0| = 0.002500% (dt≈0.01)
- rk4: max |ΔE/E0| = 0.000000% (dt≈0.01)

**Plots presence (current naming):**
- `out/plots/results1_figure1ab.png` — confirmed
- `out/plots/results1_figure1c.png` — confirmed
- `out/plots/results1_figure2.png` — confirmed
- `out/plots/results1_figure3.png` — confirmed
- `out/plots/results1_figure4.png` — confirmed
**Legacy filename aliases (staleness-aware check):**
- `out/plots/results1_ho_position_velocity_trajectories.png` → `out/plots/results1_figure1ab.png` — expected by design (renamed to current filename)
- `out/plots/results1_ho_phase_space_trajectories.png` → `out/plots/results1_figure1c.png` — expected by design (renamed to current filename)
- `out/plots/results1_ho_convergence_endpoint_position_error.png` → `out/plots/results1_figure3.png` — expected by design (renamed to current filename)
- `out/plots/results1_ho_convergence_rms_phase_space_error.png` → `out/plots/results1_figure3.png` — expected by design (renamed to current filename)
- `out/plots/results1_ho_energy_conservation.png` → `out/plots/results1_figure4.png` — expected by design (renamed to current filename)

## C) Results 2: Lennard-Jones / Argon

### LJ / Argon Analysis

**Brief (required) — Velocity-Verlet (CSV: `out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329/lj_verlet.csv`):**
- Metadata: N=864, P=4, dt=1e-14, n_steps=100, n_frames=101, step_indexing=0..steps (includes initial frame)
- Equilibration/production: equilibration_steps=50, production_steps=100, production_start_step=0, final_rescale_before_production=true
- Observed in CSV: max_step=100, frames=101
- Production window (step >= 0): Max |ΔE/E0| = 0.0817% ; Mean |ΔE/E0| = 0.0326%
- Production temperature: mean=94.42 K, std=1.43 K, range=[92.39,97.81]

**Brief (required) — Euler (CSV: `out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329/lj_euler.csv`):**
- Metadata: N=864, P=4, dt=1e-14, n_steps=100, n_frames=101, step_indexing=0..steps (includes initial frame)
- Equilibration/production: equilibration_steps=50, production_steps=100, production_start_step=0, final_rescale_before_production=true
- Observed in CSV: max_step=100, frames=101
- Production window (step >= 0): Max |ΔE/E0| = 127.5874% ; Mean |ΔE/E0| = 39.7877%
- Production temperature: mean=185.27 K, std=74.57 K, range=[94.40,396.05]

**g(r) shape diagnostics (long RDF production run):**
- Metadata: N=864, P=4, dt=1e-14, steps=20000
- First peak: r/σ = 1.090, g = 2.838
- First minimum: r/σ = 1.550, g = 0.623
- Second peak: r/σ = 2.070, g = 1.253
- Tail (r>4σ): <g> = 1.0024 (should → 1)
- CSV: `out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/gr.csv`
- Companion trajectory CSV: `out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/lj_verlet.csv`

- Interpretation: shell locations agree broadly with Rahman (1964), with somewhat reduced present-work peak heights.
- Provenance: Rahman guide values are manual Fig. 2 anchors (paper-anchored x values at 3.7 Å, 7.0 Å, 10.4 Å; other points are approximate shape anchors).

**Plots presence:**
- `out/plots/results2_figure6.png` — confirmed
- `out/plots/results2_figure7.png` — confirmed
- `out/plots/results2_figure8.png` — confirmed
- Core Results 2 evidence: required-run energy + required-run temperature + RDF-vs-Rahman.
- Results 2 quantitative table (MD): `out/summary/results2/results2_quantitative_summary_table.md` — confirmed
- Results 2 quantitative table (CSV): `out/summary/results2/results2_quantitative_summary_table.csv` — confirmed
- Rahman anchor dataset: `out/summary/results2/rahman1964_fig2_manual_anchors.csv` — confirmed

## D) Results 3: Scaling

### Scaling Analysis

**Strong scaling (from CSV):**

| P | Wall [s] | Comm [s] | Comm% | Speedup | Efficiency |
|---|----------|----------|-------|---------|------------|
| 1 | 45.964284 | 0.001237 | 0.0% | 1.00 | 1.000 |
| 2 | 23.148061 | 0.244091 | 1.1% | 1.99 | 0.993 |
| 4 | 12.002224 | 0.660859 | 5.5% | 3.83 | 0.957 |
| 8 | 6.089443 | 0.554423 | 9.1% | 7.55 | 0.944 |
| 16 | 3.213709 | 0.367247 | 11.4% | 14.30 | 0.894 |
| 24 | 2.366625 | 0.318543 | 13.5% | 19.42 | 0.809 |
| 32 | 1.905649 | 0.289675 | 15.2% | 24.12 | 0.754 |

**Amdahl fit (no SciPy; linear least squares on 1/S):**
- f = 0.009956 ± 0.000982
- Max theoretical speedup ≈ 100.4x
- Max |S_obs - S_fit| = 0.382 at P=16

- CSV: `out/scaling_strong.csv`

**Size scaling (from CSV):**

| N | Wall [s] | Comm [s] | Compute=Wall-Comm [s] | Comm% |
|---|----------|----------|----------------------|-------|
| 108 | 0.068603 | 0.034871 | 0.033732 | 50.8% |
| 256 | 0.361851 | 0.098397 | 0.263454 | 27.2% |
| 500 | 1.419085 | 0.323552 | 1.095533 | 22.8% |
| 864 | 3.848148 | 0.711096 | 3.137052 | 18.5% |
| 1372 | 9.102605 | 1.511462 | 7.591143 | 16.6% |
| 2048 | 19.195878 | 2.507444 | 16.688434 | 13.1% |

**Size-scaling exponent (log-log fit over all N points):**
- wall ~ N^1.92
- compute-only (wall-comm) ~ N^2.09

⚠️ If you expect O(N²) (direct all-pairs), but see <2.0 here, increase scaling timesteps
   (e.g. 500–2000 steps) so start-up/communication overhead doesn’t dominate the fit.

- CSV: `out/scaling_size.csv`

**Plots presence:**
- `out/plots/results3_figure10abc.png` — confirmed
- `out/plots/results3_figure9ab.png` — confirmed

## E) Compliance & Known Limitations

### Evidence-based checklist (from actual output files)

| Requirement | Status | Evidence / interpretation |
|-------------|--------|---------------------------|
| LJ brief run (Verlet) N=864, dt=1e-14, n_steps=100, n_frames=101 | confirmed | `out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329/lj_verlet.csv` header: {'mode': 'lj', 'integrator': 'verlet', 'N': '864', 'P': '4', 'dt': '1e-14', 'steps': '100', 'n_steps': '100', 'n_frames': '101', 'step_indexing': '0..steps (includes initial frame)', 'total_steps_executed': '150', 'seed': '42', 'L': '3.47786e-09', 'rcut': '7.65e-10', 'target_temperature': '94.4', 'equilibration_steps': '50', 'production_steps': '100', 'production_start_step': '0', 'final_rescale_before_production': 'true', 'final_rescale_applied': 'true', 'production_nve': 'true', 'gr_discard_steps': '200', 'gr_sample_every': '5', 'gr_start': '200', 'startup_temperature_before_final_rescale': '94.3304820914355', 'startup_temperature_after_final_rescale': '94.4', 'lattice': 'FCC', 'velocities': 'Box-Muller', 'timestamp': '2026-03-08T18:23:51Z'} |
| LJ brief run (Euler) N=864, dt=1e-14, n_steps=100, n_frames=101 | confirmed | `out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329/lj_euler.csv` header: {'mode': 'lj', 'integrator': 'euler', 'N': '864', 'P': '4', 'dt': '1e-14', 'steps': '100', 'n_steps': '100', 'n_frames': '101', 'step_indexing': '0..steps (includes initial frame)', 'total_steps_executed': '150', 'seed': '42', 'L': '3.47786e-09', 'rcut': '7.65e-10', 'target_temperature': '94.4', 'equilibration_steps': '50', 'production_steps': '100', 'production_start_step': '0', 'final_rescale_before_production': 'true', 'final_rescale_applied': 'true', 'production_nve': 'true', 'gr_discard_steps': '200', 'gr_sample_every': '5', 'gr_start': '200', 'startup_temperature_before_final_rescale': '95.9438964430546', 'startup_temperature_after_final_rescale': '94.4', 'lattice': 'FCC', 'velocities': 'Box-Muller', 'timestamp': '2026-03-08T18:23:53Z'} |
| LJ two-stage semantics (Verlet brief) | confirmed | Expected production_start_step=0, production_steps=100, total_steps_executed=equilibration_steps+production_steps, final_rescale_before_production=true, production_nve=true |
| LJ two-stage semantics (Euler brief) | confirmed | Expected production_start_step=0, production_steps=100, total_steps_executed=equilibration_steps+production_steps, final_rescale_before_production=true, production_nve=true |
| HO convergence data present | confirmed | `manifest.ho_convergence` present |
| Required current plot set present | confirmed | present=['results1_figure1ab.png', 'results1_figure1c.png', 'results1_figure2.png', 'results1_figure3.png', 'results2_figure6.png', 'results2_figure7.png', 'results2_figure8.png', 'results3_figure10abc.png', 'results3_figure9ab.png']; missing=none |
| Legacy Results 1 plot-name aliases | expected by design | Legacy Results 1 filenames are absent because plots were renamed to the `results1_figure*` scheme. |
| Makefile present | confirmed | `Makefile` exists |
| No rand()/std::rand() usage | confirmed | none |
| No OpenMP usage | confirmed | none |
| No obvious identifying strings in scanned files | potential issue | core files with possible identifiers: ['src/potentials/lennard_jones.cpp'] |

### Known limitations (state these honestly in the report)

- LJ uses a **hard cutoff** (no potential shifting), so you should expect small energy discontinuities when pairs cross r_cut.
- LJ forces are computed by a **direct all-pairs loop** (no neighbour lists). This is correct but O(N²).
- For **Lennard-Jones strong-scaling runs**, ranks use particle decomposition and allgather positions before force evaluation; the measured communication fraction rises with P.
- LJ startup rescales velocities each startup step (`--equilibration-steps`) and can apply a final startup->production rescale (`--final-rescale-before-production`) before production NVE.


## Diagnostics / Warnings (Results Generator)

- Status: confirmed
- No stderr warnings were emitted during results analysis generation.

## Potentially Stale or Informational Items (Results View)

- informational: This file summarizes existing outputs and does not regenerate simulation data.
- informational: For raw artifact payloads and longer CSV context, also read `ai/results_bundle.md`.
- informational: For executable build/test traces and source snapshots, also read `ai/audit_output.md`.

