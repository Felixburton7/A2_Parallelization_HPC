# MD Solver Production Data Bundle

## Executive Summary

| Field | Value |
|---|---|
| Purpose | Project-wide raw artifact bundle: manifest-linked CSV/notes with truncation for context-size control. |
| Generation timestamp (UTC) | 2026-03-09T13:10:49Z |
| Git commit | 1ee4694830cf559e7796ee6aa54cdd4fadc467f6 |
| Git working tree | dirty (2 changed paths) |
| Generation succeeded | yes |
| Generation status label | confirmed |
| Generation note | Raw bundle assembled from current manifest-linked project artifacts. |

### Top Important Current Facts

- Manifest-linked artifacts found: 44/44 paths currently exist.
- Core final figures present: 9/9 required figure files.
- Results 2 brief temperature single-number contrast: Verlet mean T=94.42 K (Δ=+0.02 K), Euler mean T=185.27 K (Δ=+90.87 K).
- Results 2 brief energy drift single-number contrast: Verlet max |ΔE/E0|=0.082%, Euler max |ΔE/E0|=127.587%.
- Results 1 endpoint convergence slopes: Euler 1.05, Verlet 2.00, RK4 3.94.
- Results 3 strong scaling: max measured speedup 14.92x; fitted Amdahl serial fraction f=0.0317.

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

- Manifest-linked artifacts found: 44/44 paths currently exist.
- Core final figures present: 9/9 required figure files.
- Results 2 brief temperature single-number contrast: Verlet mean T=94.42 K (Δ=+0.02 K), Euler mean T=185.27 K (Δ=+90.87 K).
- Results 2 brief energy drift single-number contrast: Verlet max |ΔE/E0|=0.082%, Euler max |ΔE/E0|=127.587%.
- Results 1 endpoint convergence slopes: Euler 1.05, Verlet 2.00, RK4 3.94.
- Results 3 strong scaling: max measured speedup 14.92x; fitted Amdahl serial fraction f=0.0317.

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
| At the required run length, Velocity-Verlet gives a physically meaningful bounded NVE trajectory in total energy; Forward Euler shows strong total-energy drift and is unreliable. | `out/plots/results2_lj_brief_energy_100step_production.png`; `out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_174309/lj_verlet.csv`; `out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_174309/lj_euler.csv` | high | Relative drift is computed from total energy with E0 taken at the first finite production frame. |
| Velocity-Verlet remains close to the target state while Forward Euler heats strongly over the same required window. | `out/plots/results2_lj_brief_temperature_100step_production.png`; `out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_174309/lj_verlet.csv`; `out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_174309/lj_euler.csv` | high | Temperature is shown only for finite values; divergent tails are omitted. |
| The present Velocity-Verlet RDF reproduces liquid-argon shell structure (first peak, first minimum, second shell, long-range trend) with qualitative/semi-quantitative agreement to Rahman (1964), while peak heights are somewhat reduced. | `out/plots/results2_lj_rdf_comparison_rahman1964.png`; `out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260308_174309/gr.csv`; `out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260308_174309/lj_verlet.csv`; `out/summary/results2/rahman1964_fig2_manual_anchors.csv` | high | Rahman comparison uses a manually extracted approximate reference guide from printed Fig. 2. |
| The MPI implementation achieves substantial strong-scaling gains with non-zero communication overhead; Amdahl fit quantifies residual serial fraction. | `out/plots/results3_strong_scaling_speedup_efficiency_breakdown.png`; `out/scaling_strong.csv`; `out/scaling_meta.txt` | medium | Strong-scaling data are aggregated medians, not raw replicate traces. |
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
| out/manifest.json | yes | 2026-03-08T17:44:36Z | confirmed |
| out/summary/results2/results2_quantitative_summary_table.csv | yes | 2026-03-08T17:44:36Z | confirmed |

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
| ai/audit_output.md | 2026-03-09T13:10:48Z | 2026-03-08T19:58:26Z | confirmed | appears current |
| ai/results.md | 2026-03-09T13:10:48Z | 2026-03-08T19:58:26Z | confirmed | appears current |
| ai/results_bundle.md | 2026-03-09T13:10:49Z | 2026-03-08T19:58:26Z | confirmed | appears current (in-progress generation timestamp) |

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
    "euler_dt1_0": "out/runs/ho_N1_euler_dt1.0_20260308_174309/ho_euler.csv",
    "euler_dt0_5": "out/runs/ho_N1_euler_dt0.5_20260308_174309/ho_euler.csv",
    "euler_dt0_1": "out/runs/ho_N1_euler_dt0.1_20260308_174309/ho_euler.csv",
    "euler_dt0_05": "out/runs/ho_N1_euler_dt0.05_20260308_174309/ho_euler.csv",
    "euler_dt0_01": "out/runs/ho_N1_euler_dt0.01_20260308_174309/ho_euler.csv",
    "euler_dt0_005": "out/runs/ho_N1_euler_dt0.005_20260308_174309/ho_euler.csv",
    "euler_dt0_001": "out/runs/ho_N1_euler_dt0.001_20260308_174309/ho_euler.csv",
    "euler_dt0_0005": "out/runs/ho_N1_euler_dt0.0005_20260308_174309/ho_euler.csv",
    "verlet_dt1_0": "out/runs/ho_N1_verlet_dt1.0_20260308_174309/ho_verlet.csv",
    "verlet_dt0_5": "out/runs/ho_N1_verlet_dt0.5_20260308_174309/ho_verlet.csv",
    "verlet_dt0_1": "out/runs/ho_N1_verlet_dt0.1_20260308_174309/ho_verlet.csv",
    "verlet_dt0_05": "out/runs/ho_N1_verlet_dt0.05_20260308_174309/ho_verlet.csv",
    "verlet_dt0_01": "out/runs/ho_N1_verlet_dt0.01_20260308_174309/ho_verlet.csv",
    "verlet_dt0_005": "out/runs/ho_N1_verlet_dt0.005_20260308_174309/ho_verlet.csv",
    "verlet_dt0_001": "out/runs/ho_N1_verlet_dt0.001_20260308_174309/ho_verlet.csv",
    "verlet_dt0_0005": "out/runs/ho_N1_verlet_dt0.0005_20260308_174309/ho_verlet.csv",
    "rk4_dt1_0": "out/runs/ho_N1_rk4_dt1.0_20260308_174309/ho_rk4.csv",
    "rk4_dt0_5": "out/runs/ho_N1_rk4_dt0.5_20260308_174309/ho_rk4.csv",
    "rk4_dt0_1": "out/runs/ho_N1_rk4_dt0.1_20260308_174309/ho_rk4.csv",
    "rk4_dt0_05": "out/runs/ho_N1_rk4_dt0.05_20260308_174309/ho_rk4.csv",
    "rk4_dt0_01": "out/runs/ho_N1_rk4_dt0.01_20260308_174309/ho_rk4.csv",
    "rk4_dt0_005": "out/runs/ho_N1_rk4_dt0.005_20260308_174309/ho_rk4.csv",
    "rk4_dt0_001": "out/runs/ho_N1_rk4_dt0.001_20260308_174309/ho_rk4.csv",
    "rk4_dt0_0005": "out/runs/ho_N1_rk4_dt0.0005_20260308_174309/ho_rk4.csv"
  },
  "lj_brief": {
    "verlet": "out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_174309/lj_verlet.csv",
    "euler": "out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_174309/lj_euler.csv"
  },
  "lj_rdf": {
    "verlet_long": "out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260308_174309/gr.csv",
    "verlet_long_energy": "out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260308_174309/lj_verlet.csv"
  },
  "scaling": {
    "strong": "out/scaling_strong.csv",
    "size": "out/scaling_size.csv"
  },
  "results2_outputs": {
    "generated_utc": "2026-03-08T17:44:36Z",
    "main_report_figures": [
      "out/plots/results2_lj_brief_energy_100step_production.png",
      "out/plots/results2_lj_brief_temperature_100step_production.png",
      "out/plots/results2_lj_rdf_comparison_rahman1964.png"
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
      "out/plots/metadata/results2_lj_brief_energy_100step_production.json",
      "out/plots/metadata/results2_lj_brief_temperature_100step_production.json",
      "out/plots/metadata/results2_lj_rdf_comparison_rahman1964.json"
    ]
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

Generated: 2026-03-08T17:44:19Z

| Integrator | Endpoint slope | RMS slope | Endpoint fit dt values | RMS fit dt values | Excluded coarse dt values |
|---|---|---|---|---|---|
| Forward Euler | 1.05 | 1.03 | 0.0005;0.001;0.005;0.01;0.05;0.1 | 0.0005;0.001;0.005;0.01;0.05;0.1 | 0.5;1 |
| Velocity-Verlet | 2.00 | 2.00 | 0.0005;0.001;0.005;0.01;0.05;0.1 | 0.0005;0.001;0.005;0.01;0.05;0.1 | 0.5;1 |
| RK4 | 3.94 | 4.00 | 0.001;0.005;0.01;0.05;0.1 | 0.0005;0.001;0.005;0.01;0.05;0.1 | 0.5;1 |
```

## Results 1 HO Convergence Summary (CSV)
```csv
integrator,integrator_label,endpoint_position_slope,rms_phase_space_slope,endpoint_fit_dt_values,rms_fit_dt_values,excluded_coarse_dt_values
euler,Forward Euler,1.0501683187830357,1.0321586375426217,0.0005;0.001;0.005;0.01;0.05;0.1,0.0005;0.001;0.005;0.01;0.05;0.1,0.5;1
verlet,Velocity-Verlet,2.000620867369962,2.0000840953366517,0.0005;0.001;0.005;0.01;0.05;0.1,0.0005;0.001;0.005;0.01;0.05;0.1,0.5;1
rk4,RK4,3.9442304587115364,3.996152298168813,0.001;0.005;0.01;0.05;0.1,0.0005;0.001;0.005;0.01;0.05;0.1,0.5;1
```

## Results 1 Small-vs-Large Timestep Summary (CSV)
```csv
integrator,integrator_label,dt,endpoint_position_error,endpoint_velocity_error,rms_phase_space_error,max_relative_energy_drift
euler,Forward Euler,0.5,8.367020351721887,1.9525828174323399,3.863189505580034,85.73617379884048
euler,Forward Euler,0.01,0.043208489127591565,0.02759708518306525,0.02942320535893793,0.10516539260323106
verlet,Velocity-Verlet,0.5,0.06303048743925244,0.0666345063276792,0.06543639736680687,0.062313079833983626
verlet,Velocity-Verlet,0.01,2.266852967147681e-05,2.816049136322718e-05,2.5742970058794124e-05,2.4999984407430367e-05
rk4,RK4,0.5,0.0008075801512805736,0.005127035265358737,0.0030345574261499034,0.004196257140171827
rk4,RK4,0.01,4.4750858574360564e-10,7.029797854940512e-10,4.81245362046023e-10,1.3888375429078477e-11
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
| First minimum | 1.550 | 0.624 | 1.559 | 0.620 | shape_anchor (manual approx.) | Minimum position and depth are broadly consistent. |
| Second peak | 2.090 | 1.254 | 2.059 | 1.250 | paper_anchored x (y approx.) | Second-shell position is consistent; present peak is lower. |
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
B,First minimum,,,,,,1.550,0.624,1.559,0.620,shape_anchor (manual approx.),Minimum position and depth are broadly consistent.
B,Second peak,,,,,,2.090,1.254,2.059,1.250,paper_anchored x (y approx.),Second-shell position is consistent; present peak is lower.
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

## Radial Distribution Function g(r) (Long RDF production run)
```csv
# mode: lj, integrator: verlet, N: 864, P: 4, dt: 1e-14, steps: 20000, n_steps: 20000, n_frames: 20001, step_indexing: 0..steps (includes initial frame), total_steps_executed: 20050, seed: 42, L: 3.47786e-09, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 50, production_steps: 20000, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: true, production_nve: true, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, startup_temperature_before_final_rescale: 94.3305, startup_temperature_after_final_rescale: 94.4, lattice: FCC, velocities: Box-Muller, timestamp: 2026-03-08T17:43:33Z
r_sigma,gr
0.01,0
0.03,0
0.05,0
0.07,0
0.09,0
0.11,0
0.13,0
0.15,0
0.17,0
0.19,0
0.21,0
0.23,0
0.25,0
0.27,0
0.29,0
0.31,0
0.33,0
0.35,0
0.37,0
0.39,0
0.41,0
0.43,0
0.45,0
0.47,0
0.49,0
0.51,0
0.53,0
0.55,0
0.57,0
0.59,0
0.61,0
0.63,0
0.65,0
0.67,0
0.69,0
0.71,0
0.73,0
0.75,0
0.77,0
0.79,0
0.81,0
0.83,0
0.85,0
0.87,3.8098e-06
0.89,0.000101934
0.91,0.00251767
0.93,0.0254925
0.95,0.132824
0.97,0.419037
0.99,0.910794
1.01,1.52615
1.03,2.11664
1.05,2.55422
1.07,2.78709
1.09,2.83766
1.11,2.74788
1.13,2.58314
1.15,2.36113
1.17,2.13547
1.19,1.92177
1.21,1.72441
1.23,1.54661
1.25,1.39532
1.27,1.25653
1.29,1.1461
1.31,1.04822
1.33,0.966056
1.35,0.897241
1.37,0.834794
1.39,0.785628
1.41,0.747639
1.43,0.711134
1.45,0.683181
1.47,0.662612
1.49,0.645968
1.51,0.63309
1.53,0.625351
1.55,0.623919
1.57,0.625756
1.59,0.626199
1.61,0.636227
1.63,0.646488
1.65,0.662188
1.67,0.680364
1.69,0.701951
1.71,0.729869
1.73,0.75727
1.75,0.791782
1.77,0.827433
1.79,0.865194
1.81,0.903028
1.83,0.942802
1.85,0.982156
1.87,1.01848
1.89,1.05208
1.91,1.08559
1.93,1.11528
1.95,1.14695
1.97,1.17121
1.99,1.19586
2.01,1.21599
2.03,1.23404
2.05,1.24575
2.07,1.2518
2.09,1.25407
2.11,1.24839
2.13,1.2393
2.15,1.22289
2.17,1.20296
2.19,1.17929
2.21,1.15299
2.23,1.12463
2.25,1.09539
2.27,1.06656
2.29,1.03732
2.31,1.011
2.33,0.986248
2.35,0.964062
2.37,0.942856
2.39,0.924993
2.41,0.908704
2.43,0.894533
2.45,0.882091
2.47,0.873204
2.49,0.868248
2.51,0.864926
2.53,0.862321
2.55,0.863665
2.57,0.866786
2.59,0.870286
2.61,0.877461
2.63,0.887349
2.65,0.89742
2.67,0.909339
2.69,0.924273
2.71,0.938738
2.73,0.953031
2.75,0.968304
2.77,0.983313
2.79,0.997027
2.81,1.01055
2.83,1.02458
2.85,1.03568
2.87,1.0474
2.89,1.05837
2.91,1.06564
2.93,1.07155
2.95,1.07718
2.97,1.08026
2.99,1.08347
3.01,1.08171
3.03,1.08209
3.05,1.0791
3.07,1.07468
3.09,1.07078
3.11,1.06537
3.13,1.05928
3.15,1.05102
3.17,1.04359
3.19,1.03652
3.21,1.02753
3.23,1.0197
3.25,1.00983
3.27,1.00205
3.29,0.995408
3.31,0.987177
3.33,0.980418
3.35,0.974766
3.37,0.967883
3.39,0.963588
3.41,0.959367
3.43,0.956334
3.45,0.953886
3.47,0.95155
3.49,0.950382
3.51,0.951405
3.53,0.952513
3.55,0.954168
3.57,0.957567
3.59,0.960548
3.61,0.963873
3.63,0.968564
3.65,0.973637
3.67,0.979954
3.69,0.985656
3.71,0.99222
3.73,0.997082
3.75,1.00271
3.77,1.00757
3.79,1.01203
3.81,1.0167
3.83,1.01957
3.85,1.02429
3.87,1.02688
3.89,1.02938
3.91,1.03021
3.93,1.03275
3.95,1.03274
3.97,1.03229
3.99,1.0315
4.01,1.0306
4.03,1.02899
4.05,1.02644
4.07,1.02387
4.09,1.02129
4.11,1.01859
4.13,1.01442
4.15,1.01161
4.17,1.00854
4.19,1.00624
4.21,1.00253
4.23,0.999237
4.25,0.996812
4.27,0.993538
4.29,0.991779
4.31,0.989305
4.33,0.98745
4.35,0.985721
4.37,0.983839
4.39,0.98302
4.41,0.981715
4.43,0.982073
4.45,0.981951
4.47,0.98199
4.49,0.983635
4.51,0.984656
4.53,0.984429
4.55,0.98657
4.57,0.988463
4.59,0.991218
4.61,0.992686
4.63,0.994076
4.65,0.995741
4.67,0.998743
4.69,1.00096
4.71,1.00265
4.73,1.00538
4.75,1.00695
4.77,1.00802
4.79,1.00864
4.81,1.00979
4.83,1.01153
4.85,1.01121
4.87,1.01274
4.89,1.0126
4.91,1.01308
4.93,1.01213
4.95,1.01224
4.97,1.01214
4.99,1.01119
5.01,1.01096
5.03,1.01028
5.05,1.00824
5.07,1.00787
5.09,1.00499
```

## LJ Brief (required) — Velocity-Verlet (100 steps) (Truncated)
```csv
# mode: lj, integrator: verlet, N: 864, P: 4, dt: 1e-14, steps: 100, n_steps: 100, n_frames: 101, step_indexing: 0..steps (includes initial frame), total_steps_executed: 150, seed: 42, L: 3.47786e-09, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 50, production_steps: 100, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: true, production_nve: true, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, startup_temperature_before_final_rescale: 94.3304820914355, startup_temperature_after_final_rescale: 94.4, lattice: FCC, velocities: Box-Muller, timestamp: 2026-03-08T17:43:13Z
step,time,E_kin,E_pot,E_total,temperature
0,0,1.687164123192e-18,-7.47194927673327e-18,-5.78478515354127e-18,94.4
1,1e-14,1.68447578135403e-18,-7.46869101577964e-18,-5.78421523442562e-18,94.2495822273505
2,2e-14,1.68047549629074e-18,-7.46552676001374e-18,-5.785051263723e-18,94.0257587683384
3,3e-14,1.675573444974e-18,-7.46109573619852e-18,-5.78552229122452e-18,93.7514797945626
4,4e-14,1.67031939809282e-18,-7.45631122530418e-18,-5.78599182721136e-18,93.4575060081561
5,5e-14,1.66525309392627e-18,-7.4517277580709e-18,-5.78647466414463e-18,93.1740367790827
6,6e-14,1.66078214268927e-18,-7.44785276849725e-18,-5.78707062580798e-18,92.923878664071
7,7e-14,1.65716146413624e-18,-7.44493273747192e-18,-5.78777127333568e-18,92.7212949019414
...
96,9.6e-13,1.69459173731494e-18,-7.47785073190453e-18,-5.78325899458959e-18,94.8155889540131
97,9.7e-13,1.69527786433769e-18,-7.47915579047344e-18,-5.78387792613575e-18,94.8539790489995
98,9.8e-13,1.69603745977495e-18,-7.47982699115721e-18,-5.78378953138226e-18,94.8964798397002
99,9.9e-13,1.69664840466377e-18,-7.4799966425522e-18,-5.78334823788842e-18,94.9306633531547
100,1e-12,1.69688683932431e-18,-7.48014957868897e-18,-5.78326273936467e-18,94.944004220024
```

## LJ Brief (required) — Euler (100 steps) (Truncated)
```csv
# mode: lj, integrator: euler, N: 864, P: 4, dt: 1e-14, steps: 100, n_steps: 100, n_frames: 101, step_indexing: 0..steps (includes initial frame), total_steps_executed: 150, seed: 42, L: 3.47786e-09, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 50, production_steps: 100, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: true, production_nve: true, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, startup_temperature_before_final_rescale: 95.9438964430546, startup_temperature_after_final_rescale: 94.4, lattice: FCC, velocities: Box-Muller, timestamp: 2026-03-08T17:43:13Z
step,time,E_kin,E_pot,E_total,temperature
0,0,1.687164123192e-18,-7.45788627945411e-18,-5.7707221562621e-18,94.4
1,1e-14,1.71215309673989e-18,-7.45868004418276e-18,-5.74652694744287e-18,95.7981799817184
2,2e-14,1.73483048401096e-18,-7.45692677351975e-18,-5.72209628950879e-18,97.0670223717161
3,3e-14,1.75546219602372e-18,-7.45364080407685e-18,-5.69817860805313e-18,98.221405390672
4,4e-14,1.77471374295437e-18,-7.44887878027046e-18,-5.67416503731609e-18,99.2985655823047
5,5e-14,1.79343662740945e-18,-7.4440707852582e-18,-5.65063415784875e-18,100.346146115973
6,6e-14,1.81217672543825e-18,-7.43791547906308e-18,-5.62573875362483e-18,101.394689781406
7,7e-14,1.83095887647807e-18,-7.43214116298387e-18,-5.6011822865058e-18,102.445586391752
...
96,9.6e-13,6.00578991146878e-18,-5.5231928214339e-18,4.82597090034878e-19,336.035220195429
97,9.7e-13,6.13936575448821e-18,-5.42104665725488e-18,7.18319097233329e-19,343.509039373838
98,9.8e-13,6.48254212789355e-18,-5.44980989537892e-18,1.03273223251463e-18,362.710401709692
99,9.9e-13,6.86618425843563e-18,-5.5058955874421e-18,1.36028867099353e-18,384.175899123574
100,1e-12,7.07845459472165e-18,-5.48646086295564e-18,1.59199373176601e-18,396.052822933149
```

## Strong Scaling (median paired timings)
```csv
P,wall_s,comm_s,speedup,efficiency
1,2.701,0.000,1.00,1.000
2,1.362,0.024,1.98,0.991
4,0.728,0.022,3.71,0.927
8,0.372,0.005,7.26,0.907
16,0.229,0.027,11.80,0.737
24,0.182,0.059,14.82,0.617
32,0.181,0.089,14.96,0.468
```

## Size Scaling (median paired timings)
```csv
P,wall_s,comm_s,comm_percent,speedup,efficiency
1,2.701,0.000,0.0,1.00,1.000
2,1.362,0.024,1.7,1.98,0.991
4,0.728,0.022,3.1,3.71,0.927
8,0.372,0.005,1.4,7.26,0.907
16,0.229,0.027,11.8,11.80,0.737
24,0.182,0.059,32.4,14.82,0.617
32,0.181,0.089,49.2,14.96,0.468
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

## LJ RDF long run trajectory (energy/temperature) (Truncated)
```csv
# mode: lj, integrator: verlet, N: 864, P: 4, dt: 1e-14, steps: 20000, n_steps: 20000, n_frames: 20001, step_indexing: 0..steps (includes initial frame), total_steps_executed: 20050, seed: 42, L: 3.47786e-09, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 50, production_steps: 20000, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: true, production_nve: true, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, startup_temperature_before_final_rescale: 94.3304820914355, startup_temperature_after_final_rescale: 94.4, lattice: FCC, velocities: Box-Muller, timestamp: 2026-03-08T17:43:14Z
step,time,E_kin,E_pot,E_total,temperature
0,0,1.687164123192e-18,-7.47194927673327e-18,-5.78478515354127e-18,94.4
1,1e-14,1.68447578135403e-18,-7.46869101577964e-18,-5.78421523442562e-18,94.2495822273505
2,2e-14,1.68047549629074e-18,-7.46552676001374e-18,-5.785051263723e-18,94.0257587683384
3,3e-14,1.675573444974e-18,-7.46109573619852e-18,-5.78552229122452e-18,93.7514797945626
4,4e-14,1.67031939809282e-18,-7.45631122530418e-18,-5.78599182721136e-18,93.4575060081561
5,5e-14,1.66525309392627e-18,-7.4517277580709e-18,-5.78647466414463e-18,93.1740367790827
6,6e-14,1.66078214268927e-18,-7.44785276849725e-18,-5.78707062580798e-18,92.923878664071
7,7e-14,1.65716146413624e-18,-7.44493273747192e-18,-5.78777127333568e-18,92.7212949019414
...
19996,1.9996e-10,1.65702437118566e-18,-7.44717126917675e-18,-5.79014689799109e-18,92.7136242939922
19997,1.9997e-10,1.65525047822275e-18,-7.44520155003441e-18,-5.78995107181166e-18,92.6143716525942
19998,1.9998e-10,1.65253012736643e-18,-7.44243595403518e-18,-5.78990582666875e-18,92.4621629152782
19999,1.9999e-10,1.64888054502845e-18,-7.43746285705333e-18,-5.78858231202488e-18,92.2579619321199
20000,2e-10,1.64447086546004e-18,-7.43257658172455e-18,-5.78810571626451e-18,92.011232081991
```

## Diagnostics / Warnings (Bundle Generator)

- Status: confirmed
- No bundle-generation warnings were emitted.

## Potentially Stale or Informational Items (Bundle View)

- informational: Long trajectory files are intentionally truncated (head 10 + tail 5) for context size control.
- informational: Read `ai/results.md` for interpreted conclusions and confidence statements.
- informational: Read `ai/audit_output.md` for executable build/test/smoke traces.

