# MD Solver Production Data Bundle

## Executive Summary

| Field | Value |
|---|---|
| Purpose | Project-wide raw artifact bundle: manifest-linked CSV/notes with truncation for context-size control. |
| Generation timestamp (UTC) | 2026-03-10T17:33:34Z |
| Git commit | ccf5f1350359a1bc69a1ba7a6e4a295ae0f6aaad |
| Git working tree | dirty (16 changed paths) |
| Generation succeeded | yes |
| Generation status label | potential issue |
| Generation note | Bundle generated with warnings; review missing/empty artifact keys. |

### Top Important Current Facts

- Manifest-linked artifacts found: 28/28 paths currently exist.
- Core final figures present: 9/9 required figure files.
- Results 2 brief temperature single-number contrast: Verlet mean T=94.42 K (Δ=+0.02 K), Euler mean T=185.27 K (Δ=+90.87 K).
- Results 2 brief energy drift single-number contrast: Verlet max |ΔE/E0|=0.082%, Euler max |ΔE/E0|=127.587%.
- Results 1 endpoint convergence slopes: Euler 1.05, Verlet 2.00, RK4 3.94.
- Results 3 strong scaling: max measured speedup 24.12x; fitted Amdahl serial fraction f=0.0103.

## How to Read This File

- Authoritative for: Raw artifact payloads and exact file contents included for downstream LLM context.
- Less authoritative for: Interpretive judgment, confidence scoring, and compliance decisions.
- Companion files to read with this one: `ai/results.md`, `ai/audit_output.md`.

## Authoritative Facts

| Fact | Status | Evidence |
|---|---|---|
| Manifest present | confirmed | `out/manifest.json` |
| Core required figures present | confirmed | 9/9 required |
| Core required tables/data present | confirmed | 8/8 required |
| Plot metadata sidecars available | confirmed | `out/plots/metadata/*.json` |

## Generated Result Summaries (High Value)

- Manifest-linked artifacts found: 28/28 paths currently exist.
- Core final figures present: 9/9 required figure files.
- Results 2 brief temperature single-number contrast: Verlet mean T=94.42 K (Δ=+0.02 K), Euler mean T=185.27 K (Δ=+90.87 K).
- Results 2 brief energy drift single-number contrast: Verlet max |ΔE/E0|=0.082%, Euler max |ΔE/E0|=127.587%.
- Results 1 endpoint convergence slopes: Euler 1.05, Verlet 2.00, RK4 3.94.
- Results 3 strong scaling: max measured speedup 24.12x; fitted Amdahl serial fraction f=0.0103.

## Current Deliverables Map

### Current final figures
- [confirmed] Results 1: `out/plots/results1_ho_figure1_trajectories_dt0p01.png` (required)
- [confirmed] Results 1: `out/plots/results1_ho_figure2_phase_space_dt0p01.png` (required)
- [confirmed] Results 1: `out/plots/results1_ho_figure3_small_vs_large_dt.png` (required)
- [confirmed] Results 1: `out/plots/results1_ho_figure4_convergence_combined.png` (required)
- [confirmed] Results 1: `out/plots/results1_ho_figure5_energy_diagnostic.png` (optional)
- [confirmed] Results 2: `out/plots/results2_lj_brief_energy_100step_production.png` (required)
- [confirmed] Results 2: `out/plots/results2_lj_brief_temperature_100step_production.png` (required)
- [confirmed] Results 2: `out/plots/results2_lj_rdf_comparison_rahman1964.png` (required)
- [confirmed] Results 3: `out/plots/results3_strong_scaling_speedup_efficiency_breakdown.png` (required)
- [confirmed] Results 3: `out/plots/results3_problem_size_scaling_fixed_p16.png` (required)

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
- [expected by design] Legacy filename `out/plots/results1_ho_position_velocity_trajectories.png` replaced by `out/plots/results1_ho_figure1_trajectories_dt0p01.png`.
- [expected by design] Legacy filename `out/plots/results1_ho_phase_space_trajectories.png` replaced by `out/plots/results1_ho_figure2_phase_space_dt0p01.png`.
- [expected by design] Legacy filename `out/plots/results1_ho_convergence_endpoint_position_error.png` replaced by `out/plots/results1_ho_figure4_convergence_combined.png`.
- [expected by design] Legacy filename `out/plots/results1_ho_convergence_rms_phase_space_error.png` replaced by `out/plots/results1_ho_figure4_convergence_combined.png`.
- [expected by design] Legacy filename `out/plots/results1_ho_energy_conservation.png` replaced by `out/plots/results1_ho_figure5_energy_diagnostic.png`.

## Report Claims Supported by Current Evidence

| Claim | Supporting artifacts | Confidence | Caveat |
|---|---|---|---|
| Demonstrates first-, second-, and fourth-order convergence using endpoint and RMS phase-space metrics. | `out/plots/results1_ho_figure4_convergence_combined.png` | medium | No major caveat recorded in metadata. |
| Direct small-vs-large timestep comparison with full-range coarse behaviour retained; quantitative error values are reported in summary tables. | `out/plots/results1_ho_figure3_small_vs_large_dt.png` | medium | No major caveat recorded in metadata. |
| At the required run length, Velocity-Verlet gives a physically meaningful bounded NVE trajectory in total energy; Forward Euler shows strong total-energy drift and is unreliable. | `out/plots/results2_lj_brief_energy_100step_production.png`; `out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260307_201536/lj_verlet.csv`; `out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260307_201536/lj_euler.csv` | high | Relative drift is computed from total energy with E0 taken at the first finite production frame. |
| Velocity-Verlet remains close to the target state while Forward Euler heats strongly over the same required window. | `out/plots/results2_lj_brief_temperature_100step_production.png`; `out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260307_201536/lj_verlet.csv`; `out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260307_201536/lj_euler.csv` | high | Temperature is shown only for finite values; divergent tails are omitted. |
| The present Velocity-Verlet RDF reproduces liquid-argon shell structure (first peak, first minimum, second shell, long-range trend) with qualitative/semi-quantitative agreement to Rahman (1964), while peak heights are somewhat reduced. | `out/plots/results2_lj_rdf_comparison_rahman1964.png`; `out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/gr.csv`; `out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/lj_verlet.csv`; `out/summary/results2/rahman1964_fig2_manual_anchors.csv` | high | Rahman comparison uses a manually extracted approximate reference guide from printed Fig. 2. |
| The MPI implementation achieves strong-scaling gains while critical-path communication (max rank communication time) contributes a measurable share of runtime. | `out/plots/results3_strong_scaling_speedup_efficiency_breakdown.png`; `out/scaling_strong.csv`; `out/scaling_meta.txt` | medium | Strong-scaling data are aggregated medians, not raw replicate traces. |
| Runtime grows approximately as a power law near O(N^2) while communication fraction changes with size at fixed P=16. | `out/plots/results3_problem_size_scaling_fixed_p16.png`; `out/scaling_size.csv`; `out/scaling_meta.txt` | medium | Power-law exponents depend on the chosen fit domain (here N >= 500). |
| Shows position and velocity trajectories at dt=0.01 for Euler, Velocity-Verlet, RK4 versus exact. | `out/plots/results1_ho_figure1_trajectories_dt0p01.png` | medium | No major caveat recorded in metadata. |
| Shows phase-space geometry at dt=0.01 and qualitative orbit preservation differences. | `out/plots/results1_ho_figure2_phase_space_dt0p01.png` | medium | No major caveat recorded in metadata. |
| Supporting diagnostic: Euler shows strong drift, Velocity-Verlet bounded oscillatory error, RK4 tiny drift on this interval. | `out/plots/results1_ho_figure5_energy_diagnostic.png` | medium | No major caveat recorded in metadata. |

## Freshness / Staleness Metadata

### Source files used to generate this file
| Source file | Found | Last modified (UTC) | Status |
|---|---|---|---|
| ai/pack_results.sh | yes | 2026-03-07T17:14:25Z | confirmed |
| ai/context_report.py | yes | 2026-03-07T17:15:25Z | confirmed |
| out/manifest.json | yes | 2026-03-09T16:34:08Z | confirmed |
| out/summary/results2/results2_quantitative_summary_table.csv | yes | 2026-03-07T20:33:31Z | confirmed |

### Expected file checks
| Path | Expectation | Role | Status |
|---|---|---|---|
| out/manifest.json | required | project manifest | confirmed |
| out/plots/results1_ho_figure1_trajectories_dt0p01.png | required | core final figure | confirmed |
| out/plots/results1_ho_figure2_phase_space_dt0p01.png | required | core final figure | confirmed |
| out/plots/results1_ho_figure3_small_vs_large_dt.png | required | core final figure | confirmed |
| out/plots/results1_ho_figure4_convergence_combined.png | required | core final figure | confirmed |
| out/plots/results2_lj_brief_energy_100step_production.png | required | core final figure | confirmed |
| out/plots/results2_lj_brief_temperature_100step_production.png | required | core final figure | confirmed |
| out/plots/results2_lj_rdf_comparison_rahman1964.png | required | core final figure | confirmed |
| out/plots/results3_strong_scaling_speedup_efficiency_breakdown.png | required | core final figure | confirmed |
| out/plots/results3_problem_size_scaling_fixed_p16.png | required | core final figure | confirmed |
| out/manifest.json | required | core summary/table | confirmed |
| out/summary/results1/results1_ho_convergence_summary.csv | required | core summary/table | confirmed |
| out/summary/results1/results1_ho_small_large_summary.csv | required | core summary/table | confirmed |
| out/summary/results1/results1_ho_endpoint_values.csv | required | core summary/table | confirmed |
| out/summary/results2/results2_quantitative_summary_table.csv | required | core summary/table | confirmed |
| out/summary/results2/results2_quantitative_summary_table.md | required | core summary/table | confirmed |
| out/scaling_strong.csv | required | core summary/table | confirmed |
| out/scaling_size.csv | required | core summary/table | confirmed |
| out/plots/metadata/results2_lj_brief_temperature_100step_production.json | required | metadata sidecar | confirmed |
| out/plots/metadata/results3_strong_scaling_speedup_efficiency_breakdown.json | required | metadata sidecar | confirmed |

### Output currency relative to current repo evidence
| Context file | Last modified (UTC) | Latest evidence mtime (UTC) | Status | Note |
|---|---|---|---|---|
| ai/audit_output.md | 2026-03-10T17:33:33Z | 2026-03-10T16:35:08Z | confirmed | appears current |
| ai/results.md | 2026-03-10T17:33:34Z | 2026-03-10T16:35:08Z | confirmed | appears current |
| ai/results_bundle.md | 2026-03-10T17:33:34Z | 2026-03-10T16:35:08Z | confirmed | appears current (in-progress generation timestamp) |

## Diagnostics / Warnings

- [confirmed] Required artifacts for this context view were found.
- [confirmed] Context outputs appear current relative to latest tracked evidence.

## Known Limitations / Caveats (Project-wide)

- Lennard-Jones uses a hard cutoff (no potential shift), so small energy discontinuities can occur when pairs cross r_cut.
- LJ force evaluation is direct all-pairs O(N^2) without neighbour lists; scaling trends depend strongly on chosen timestep counts.
- MPI strategy uses particle decomposition plus Allgatherv-style position exchange each timestep; communication overhead rises with process count.
- Results 2 reference comparison uses manual Rahman Fig. 2 anchors for part of the curve; treat as qualitative/semi-quantitative.
- Strong/size scaling CSVs store aggregated timings rather than all replicate traces, limiting deeper uncertainty analysis.
- Artifact naming conventions evolved (notably Results 1 plot names); legacy filename checks must be interpreted with rename context.

## Potentially Stale or Informational Items

| Status | Item | Interpretation |
|---|---|---|
| expected by design | `out/plots/results1_ho_position_velocity_trajectories.png` | Renamed; current artifact is `out/plots/results1_ho_figure1_trajectories_dt0p01.png`. |
| expected by design | `out/plots/results1_ho_phase_space_trajectories.png` | Renamed; current artifact is `out/plots/results1_ho_figure2_phase_space_dt0p01.png`. |
| expected by design | `out/plots/results1_ho_convergence_endpoint_position_error.png` | Renamed; current artifact is `out/plots/results1_ho_figure4_convergence_combined.png`. |
| expected by design | `out/plots/results1_ho_convergence_rms_phase_space_error.png` | Renamed; current artifact is `out/plots/results1_ho_figure4_convergence_combined.png`. |
| expected by design | `out/plots/results1_ho_energy_conservation.png` | Renamed; current artifact is `out/plots/results1_ho_figure5_energy_diagnostic.png`. |
| informational | `scripts/__pycache__/` | Generated cache files may create noisy static-scan results unless excluded. |
| informational | `out/summary/results3/` | Results 3 currently tracked via `out/scaling_*.csv` and metadata JSON sidecars. |

## Cross-References

- `ai/audit_output.md`: executable build/test/smoke audit and raw source/verbatim evidence.
- `ai/results.md`: interpreted project-wide results summary and compliance-oriented checks.
- `ai/results_bundle.md`: raw/truncated artifact bundle for direct context ingestion.

## Raw Artifact Bundle (Verbatim / Truncated)

This section preserves raw artifact payloads (with explicit truncation for long trajectories).

## out/manifest.json
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
  }
}
```

## Current Package Ordering (Core Evidence First)

1. out/manifest.json
2. out/summary/results1/results1_ho_convergence_summary.csv
3. out/summary/results2/results2_quantitative_summary_table.md
4. out/plots/results2_lj_brief_energy_100step_production.png
5. out/plots/results2_lj_brief_temperature_100step_production.png
6. out/plots/results2_lj_rdf_comparison_rahman1964.png
7. out/scaling_strong.csv
8. out/scaling_size.csv

## Results 1 HO Convergence Summary (Markdown)
```markdown
# Results 1 HO Convergence Summary

Generated: 2026-03-07T20:33:29Z

| Integrator | Endpoint slope | RMS slope | Endpoint fit dt values | RMS fit dt values | Excluded coarse dt values |
|---|---|---|---|---|---|
| Forward Euler | 1.05 | 1.03 | 0.0005;0.001;0.005;0.01;0.05;0.1 | 0.0005;0.001;0.005;0.01;0.05;0.1 | 0.5;1 |
| Velocity-Verlet | 2.00 | 2.00 | 0.0005;0.001;0.005;0.01;0.05;0.1 | 0.0005;0.001;0.005;0.01;0.05;0.1 | 0.5;1 |
| RK4 | 3.94 | 4.00 | 0.001;0.005;0.01;0.05;0.1 | 0.0005;0.001;0.005;0.01;0.05;0.1 | 0.5;1 |
```

## Results 1 HO Convergence Summary (CSV)
```csv
integrator,integrator_label,endpoint_position_slope,rms_phase_space_slope,endpoint_fit_dt_values,rms_fit_dt_values,excluded_coarse_dt_values
euler,Forward Euler,1.0501683187830355,1.0321586375426215,0.0005;0.001;0.005;0.01;0.05;0.1,0.0005;0.001;0.005;0.01;0.05;0.1,0.5;1
verlet,Velocity-Verlet,2.000620867369963,2.0000840953365064,0.0005;0.001;0.005;0.01;0.05;0.1,0.0005;0.001;0.005;0.01;0.05;0.1,0.5;1
rk4,RK4,3.9442304587115373,3.9961192997018524,0.001;0.005;0.01;0.05;0.1,0.0005;0.001;0.005;0.01;0.05;0.1,0.5;1
```

## Results 1 Small-vs-Large Timestep Summary (CSV)
```csv
integrator,integrator_label,dt,endpoint_position_error,endpoint_velocity_error,rms_phase_space_error,max_relative_energy_drift
euler,Forward Euler,0.5,8.367020351721887,1.9525828174323399,3.863189505580034,85.73617379884048
euler,Forward Euler,0.01,0.043208489127591565,0.02759708518306525,0.02942320535893793,0.10516539260323106
verlet,Velocity-Verlet,0.5,0.06303048743925244,0.0666345063276792,0.06543639736680687,0.062313079833983626
verlet,Velocity-Verlet,0.01,2.266852967147681e-05,2.816049136322718e-05,2.574297005879334e-05,2.4999984407430367e-05
rk4,RK4,0.5,0.0008075801512805736,0.005127035265358737,0.003034557426149899,0.004196257140171827
rk4,RK4,0.01,4.4750858574360564e-10,7.029797854940512e-10,4.812453619614678e-10,1.3888375429078477e-11
```

## Results 1 Endpoint Values (CSV)
```csv
integrator,integrator_label,dt,x_num_final,x_exact_final,endpoint_position_error,v_num_final,v_exact_final,endpoint_velocity_error
euler,Forward Euler,0.5,-9.20609188079834,-0.8390715290764524,8.367020351721887,-1.40856170654297,0.5440211108893698,1.9525828174323399
euler,Forward Euler,0.1,-1.40884698291602,-0.8390715290764524,0.5697754538395675,0.84850692875778,0.5440211108893698,0.3044858178684102
euler,Forward Euler,0.01,-0.882280018204044,-0.8390715290764524,0.043208489127591565,0.571618196072435,0.5440211108893698,0.02759708518306525
verlet,Velocity-Verlet,0.5,-0.7760410416372,-0.8390715290764524,0.06303048743925244,0.610655617217049,0.5440211108893698,0.0666345063276792
verlet,Velocity-Verlet,0.1,-0.836794927110387,-0.8390715290764524,0.0022766019660653836,0.546831614244655,0.5440211108893698,0.00281050335528521
verlet,Velocity-Verlet,0.01,-0.839048860546781,-0.8390715290764524,2.266852967147681e-05,0.544049271380733,0.5440211108893698,2.816049136322718e-05
rk4,RK4,0.5,-0.839879109227733,-0.8390715290764524,0.0008075801512805736,0.538894075624011,0.5440211108893698,0.005127035265358737
rk4,RK4,0.1,-0.839075464413064,-0.8390715290764524,3.935336611582407e-06,0.544013766248773,0.5440211108893698,7.344640596818053e-06
rk4,RK4,0.01,-0.839071529523961,-0.8390715290764524,4.4750858574360564e-10,0.54402111018639,0.5440211108893698,7.029797854940512e-10
```

## Results 2 Quantitative Summary Table (Markdown)
# Results 2 Quantitative Summary Table

## Section A: Required 100-step production run

| Integrator | Production steps | Mean T [K] | Std T [K] | Max |ΔE/E0| [%] | Mean |ΔE/E0| [%] | Comment |
|---|---:|---:|---:|---:|---:|---|
| Velocity-Verlet | 100 | 94.42 | 1.43 | 0.082 | 0.033 | Bounded drift; near target state. |
| Euler | 100 | 185.27 | 74.57 | 127.587 | 39.788 | Strong drift/heating over required run; not a stable NVE trajectory. |

## Section B: RDF structural comparison

| Feature | Present work r/sigma | Present work g(r) | Rahman reference r/sigma | Rahman reference g(r) | Reference provenance | Comment |
|---|---:|---:|---:|---:|---|---|
| First peak | 1.090 | 2.838 | 1.088 | 2.700 | paper_anchored x (y approx.) | Broadly correct location; present peak height is lower. |
| First minimum | 1.550 | 0.623 | 1.559 | 0.620 | shape_anchor (manual approx.) | Minimum position and depth are broadly consistent. |
| Second peak | 2.070 | 1.253 | 2.059 | 1.250 | paper_anchored x (y approx.) | Second-shell position is consistent; present peak is lower. |
| Tail | >=4.0 (mean) | 1.002 | 3.412 | 1.000 | shape_anchor (manual approx.) | Long-range trend returns toward g(r)=1. |

Notes:
- Required run metrics are derived from manifest-linked `lj_brief` production CSV files (100 steps, 101 frames).
- RDF values are from manifest-linked long Verlet RDF run; Rahman values are manual figure anchors (not tabulated exact data).

## Results 2 Quantitative Summary Table (CSV)
```csv
section,Integrator/Feature,Production steps,Mean T [K],Std T [K],Max |ΔE/E0| [%],Mean |ΔE/E0| [%],Present work r/sigma,Present work g(r),Rahman reference r/sigma,Rahman reference g(r),Reference provenance,Comment
A,Velocity-Verlet,100,94.42,1.43,0.082,0.033,,,,,,Bounded drift; near target state.
A,Euler,100,185.27,74.57,127.587,39.788,,,,,,Strong drift/heating over required run; not a stable NVE trajectory.
B,First peak,,,,,,1.090,2.838,1.088,2.700,paper_anchored x (y approx.),Broadly correct location; present peak height is lower.
B,First minimum,,,,,,1.550,0.623,1.559,0.620,shape_anchor (manual approx.),Minimum position and depth are broadly consistent.
B,Second peak,,,,,,2.070,1.253,2.059,1.250,paper_anchored x (y approx.),Second-shell position is consistent; present peak is lower.
B,Tail,,,,,,>=4.0 (mean),1.002,3.412,1.000,shape_anchor (manual approx.),Long-range trend returns toward g(r)=1.
```

## Rahman Fig. 2 Manual Anchor Dataset
```csv
point_id,r_angstrom,r_over_sigma,g_value,point_type,source_note,uncertainty_note
1,3.0,0.882353,0.00,shape_anchor,"approximate onset / exclusion-region anchor from printed figure","manual visual extraction from printed curve; approximate y and x"
2,3.7,1.088235,2.70,paper_anchored,"x-position from Rahman Fig. 2 annotation; y estimated from plotted peak","x anchored to annotated figure value; y manually estimated from printed curve"
3,4.5,1.323529,1.35,shape_anchor,"approximate descending shoulder after first peak","manual visual extraction from printed curve; approximate y and x"
4,5.3,1.558824,0.62,shape_anchor,"approximate first minimum from printed figure","manual visual extraction from printed curve; approximate y and x"
5,7.0,2.058824,1.25,paper_anchored,"x-position from Rahman Fig. 2 annotation; y estimated from plotted second-shell peak","x anchored to annotated figure value; y manually estimated from printed curve"
6,8.0,2.352941,0.95,shape_anchor,"approximate post-second-peak descent","manual visual extraction from printed curve; approximate y and x"
7,8.8,2.588235,0.82,shape_anchor,"approximate second minimum / oscillatory trough","manual visual extraction from printed curve; approximate y and x"
8,10.4,3.058824,1.05,paper_anchored,"x-position from Rahman Fig. 2 annotation; y estimated from printed curve near third-shell region","x anchored to annotated figure value; y manually estimated from printed curve"
9,11.6,3.411765,1.00,shape_anchor,"approximate long-range return toward unity","manual visual extraction from printed curve; approximate y and x"
```

## Results 2 Report Note
```markdown
# Results 2 Report Note

The Lennard-Jones Argon test case follows the Rahman-style state point at 94.4 K with N=864 atoms in a periodic box, using dt = 1e-14 s.

For the brief-required production run (100 steps, 1 ps), startup/equilibration is performed first, then a final startup->production temperature rescale is applied before production. In the saved production CSV, step 0 is the production initial frame (n_frames = 101).

Across this required production window, Velocity-Verlet remains near the target state and shows small bounded energy drift. Forward Euler shows strong energy drift and substantial temperature growth over the same window, so it is not suitable for a stable NVE Argon trajectory here.

For structure, the Velocity-Verlet RDF from a longer production run reproduces the expected liquid-argon shell pattern (first peak, first minimum, second shell, and long-range return toward g(r)=1), with broad agreement to Rahman (1964).

The Rahman comparison is based on a manually extracted approximate guide from Rahman Fig. 2. Sigma = 3.4 Å is paper-supported; the x-positions 3.7 Å, 7.0 Å, and 10.4 Å are directly anchored to annotated figure positions; remaining points are approximate shape anchors read from the printed curve.

This comparison should be stated as qualitative / semi-quantitative rather than exact, especially for peak heights (present-work peaks are somewhat reduced).
```

## Rahman Extraction Note
```markdown
# Rahman Data Extraction Note (Fig. 2)

Reference file: `scripts/data/rahman1964_fig2_manual_anchors.csv` (copied to `out/summary/results2/rahman1964_fig2_manual_anchors.csv` during plotting).

Exactly paper-supported elements used:
- sigma = 3.4 Å (used for the top-axis conversion and r/sigma conversion)
- Fig. 2 annotated x-positions at 3.7 Å, 7.0 Å, and 10.4 Å

Approximate elements (manual extraction from printed curve):
- all Rahman g(r) values
- all non-annotated x positions used as shape anchors

Interpretation rule:
- this anchor set is a transparent visual guide only; it is not exact tabulated truth and should not be over-interpreted.
```

## LJ Brief (required) — Velocity-Verlet (100 steps) (Truncated)
```csv
# mode: lj, integrator: verlet, N: 864, P: 4, dt: 1e-14, steps: 100, n_steps: 100, n_frames: 101, step_indexing: 0..steps (includes initial frame), total_steps_executed: 150, seed: 42, L: 3.47786e-09, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 50, production_steps: 100, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: true, production_nve: true, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, startup_temperature_before_final_rescale: 94.3304820914355, startup_temperature_after_final_rescale: 94.4, lattice: FCC, velocities: Box-Muller, timestamp: 2026-03-08T18:23:51Z
step,time,E_kin,E_pot,E_total,temperature
0,0,1.687164123192e-18,-7.47194927673327e-18,-5.78478515354127e-18,94.4
1,1e-14,1.68447578135403e-18,-7.46869101577964e-18,-5.78421523442562e-18,94.2495822273505
2,2e-14,1.68047549629074e-18,-7.46552676001374e-18,-5.78505126372299e-18,94.0257587683384
3,3e-14,1.675573444974e-18,-7.46109573619852e-18,-5.78552229122452e-18,93.7514797945627
4,4e-14,1.67031939809282e-18,-7.45631122530418e-18,-5.78599182721136e-18,93.4575060081561
5,5e-14,1.66525309392627e-18,-7.4517277580709e-18,-5.78647466414463e-18,93.1740367790827
6,6e-14,1.66078214268927e-18,-7.44785276849725e-18,-5.78707062580798e-18,92.923878664071
7,7e-14,1.65716146413624e-18,-7.44493273747192e-18,-5.78777127333568e-18,92.7212949019415
...
96,9.6e-13,1.69459173731495e-18,-7.47785073190453e-18,-5.78325899458959e-18,94.8155889540133
97,9.7e-13,1.69527786433769e-18,-7.47915579047344e-18,-5.78387792613575e-18,94.8539790489995
98,9.8e-13,1.69603745977495e-18,-7.47982699115721e-18,-5.78378953138226e-18,94.8964798397003
99,9.9e-13,1.69664840466377e-18,-7.4799966425522e-18,-5.78334823788842e-18,94.9306633531546
100,1e-12,1.6968868393243e-18,-7.48014957868897e-18,-5.78326273936467e-18,94.944004220024
```

## LJ Brief (required) — Euler (100 steps) (Truncated)
```csv
# mode: lj, integrator: euler, N: 864, P: 4, dt: 1e-14, steps: 100, n_steps: 100, n_frames: 101, step_indexing: 0..steps (includes initial frame), total_steps_executed: 150, seed: 42, L: 3.47786e-09, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 50, production_steps: 100, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: true, production_nve: true, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, startup_temperature_before_final_rescale: 95.9438964430546, startup_temperature_after_final_rescale: 94.4, lattice: FCC, velocities: Box-Muller, timestamp: 2026-03-08T18:23:53Z
step,time,E_kin,E_pot,E_total,temperature
0,0,1.687164123192e-18,-7.45788627945411e-18,-5.77072215626211e-18,94.4
1,1e-14,1.71215309673989e-18,-7.45868004418276e-18,-5.74652694744287e-18,95.7981799817184
2,2e-14,1.73483048401096e-18,-7.45692677351975e-18,-5.72209628950879e-18,97.0670223717161
3,3e-14,1.75546219602372e-18,-7.45364080407685e-18,-5.69817860805314e-18,98.2214053906719
4,4e-14,1.77471374295437e-18,-7.44887878027046e-18,-5.6741650373161e-18,99.2985655823047
5,5e-14,1.79343662740945e-18,-7.4440707852582e-18,-5.65063415784875e-18,100.346146115973
6,6e-14,1.81217672543825e-18,-7.43791547906309e-18,-5.62573875362483e-18,101.394689781406
7,7e-14,1.83095887647808e-18,-7.43214116298388e-18,-5.6011822865058e-18,102.445586391752
...
96,9.6e-13,6.00578991146863e-18,-5.52319282143391e-18,4.8259709003472e-19,336.035220195422
97,9.7e-13,6.13936575448804e-18,-5.4210466572549e-18,7.18319097233137e-19,343.509039373828
98,9.8e-13,6.48254212789332e-18,-5.44980989537892e-18,1.0327322325144e-18,362.710401709679
99,9.9e-13,6.86618425843547e-18,-5.50589558744214e-18,1.36028867099333e-18,384.175899123566
100,1e-12,7.07845459472154e-18,-5.48646086295571e-18,1.59199373176582e-18,396.052822933143
```

## Strong Scaling (median paired timings)
```csv
P,N,wall_s,comm_max_s
1,2048,45.964284,0.001237
2,2048,23.148061,0.244091
4,2048,12.002224,0.660859
8,2048,6.089443,0.554423
16,2048,3.213709,0.367247
24,2048,2.366625,0.318543
32,2048,1.905649,0.289675
```

## Size Scaling (median paired timings)
```csv
P,N,wall_s,comm_max_s
16,108,0.068603,0.034871
16,256,0.361851,0.098397
16,500,1.419085,0.323552
16,864,3.848148,0.711096
16,1372,9.102605,1.511462
16,2048,19.195878,2.507444
```

## HO Convergence Summary (all dt values, final step only)
```csv
integrator,dt,x_final,v_final,E_total_final
euler,0.0005,-0.841172286406609,0.545382164003126,3.36198119909349e-26
euler,0.001,-0.843279212997926,0.546745215762798,3.37883318520048e-26
euler,0.005,-0.860358936177427,0.557721203005937,3.51672380302267e-26
euler,0.01,-0.882280018204044,0.571618196072435,3.69701391477778e-26
euler,0.05,-1.08282635743614,0.689332963545504,5.51188397043902e-26
euler,0.1,-1.40884698291602,0.84850692875778,9.04817906096412e-26
euler,0.5,-9.20609188079834,-1.40856170654297,2.90150997846184e-24
euler,1.0,0,-32,3.425498368e-23
rk4,0.0005,-0.839071529076456,0.544021110889371,3.34521325000003e-26
rk4,0.001,-0.839071529076505,0.544021110889303,3.34521325000005e-26
rk4,0.005,-0.839071529104603,0.544021110845548,3.34521324999853e-26
rk4,0.01,-0.839071529523961,0.54402111018639,3.34521324995354e-26
rk4,0.05,-0.839071793964388,0.54402066246069,3.34521310485382e-26
rk4,0.1,-0.839075464413064,0.544013766248773,3.34520860968133e-26
rk4,0.5,-0.839879109227733,0.538894075624011,3.33117587501429e-26
rk4,1.0,-0.816618156599971,0.466949881766836,2.96020397880759e-26
verlet,0.0005,-0.839071472407576,0.544021181291987,3.34521318812208e-26
verlet,0.001,-0.839071302400887,0.544021392499808,3.34521300248818e-26
verlet,0.005,-0.839065862128419,0.544028151116923,3.34520706201451e-26
verlet,0.01,-0.839048860546781,0.544049271380733,3.34518849567203e-26
verlet,0.05,-0.838504225599749,0.544724787839314,3.34459248157118e-26
verlet,0.1,-0.836794927110387,0.546831614244655,3.34270622801754e-26
verlet,0.5,-0.7760410416372,0.610655617217049,3.26205118552794e-26
verlet,1.0,-0.5,0.75,2.717985765625e-26
```

## Diagnostics / Warnings (Bundle Generator)

- Status: potential issue
- Generator warnings captured below:
```
manifest key missing or empty: lj_rdf.verlet_long
manifest key missing or empty: lj_rdf.verlet_long_energy
```

## Potentially Stale or Informational Items (Bundle View)

- informational: Long trajectory files are intentionally truncated (head 10 + tail 5) for context size control.
- informational: Read `ai/results.md` for interpreted conclusions and confidence statements.
- informational: Read `ai/audit_output.md` for executable build/test/smoke traces.

