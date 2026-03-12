# MD Solver Production Data Bundle

## Context Preface (Stub)

- Shared Executive Summary, Deliverables Map, claims table, and freshness metadata are centralised in `ai/results.md`.
- This file includes only document-specific sections below.
- Generation metadata for this document:

| Field | Value |
|---|---|
| Generation timestamp (UTC) | 2026-03-12T11:55:08Z |
| Generation succeeded | yes |
| Generation status label | confirmed |
| Generation note | Raw bundle assembled from current manifest-linked project artifacts. |

## Cross-Reference

- Read `ai/results.md` first for shared high-level context.

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
  },
  "results2_outputs": {
    "generated_utc": "2026-03-11T12:01:14Z",
    "main_report_figures": [
      "out/plots/results2_figure6_lj_brief_energy_100step_production.png",
      "out/plots/results2_figure7_lj_brief_temperature_100step_production.png",
      "out/plots/results2_figure8_lj_rdf_comparison_rahman1964.png"
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
      "out/plots/metadata/results2_figure6_lj_brief_energy_100step_production.json",
      "out/plots/metadata/results2_figure7_lj_brief_temperature_100step_production.json",
      "out/plots/metadata/results2_figure8_lj_rdf_comparison_rahman1964.json"
    ]
  },
  "lj_rdf": {
    "verlet_long": "out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/gr.csv",
    "verlet_long_energy": "out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/lj_verlet.csv"
  }
}
```

## Current Package Ordering (Core Evidence First)

1. out/manifest.json
2. out/summary/results1/results1_ho_convergence_summary.csv
3. out/summary/results2/results2_quantitative_summary_table.md
4. out/plots/results2_figure6_lj_brief_energy_100step_production.png
5. out/plots/results2_figure7_lj_brief_temperature_100step_production.png
6. out/plots/results2_figure8_lj_rdf_comparison_rahman1964.png
7. out/plots/results3_figure9ab_problem_size_scaling_fixed_p16.png
8. out/plots/results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.png
9. out/scaling_strong.csv
10. out/scaling_size.csv

## Report-Writing Notes and Plot Metadata

This section pulls in the short human-readable notes and figure metadata sidecars that are most useful while drafting the Results section.

## Results 1 HO Convergence Summary (Markdown)
```markdown
# Results 1 HO Convergence Summary

Generated: 2026-03-11T12:01:15Z

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

## Results 1 Small-vs-Large Timestep Summary (Markdown)
```markdown
# Results 1 HO Small-vs-Large Timestep Summary

Generated: 2026-03-11T12:01:15Z

| Integrator | dt | abs(x(T)-x_exact(T)) | abs(v(T)-v_exact(T)) | RMS phase-space error | max abs(E-E0)/abs(E0) |
|---|---|---|---|---|---|
| Forward Euler | 0.5 | 8.367e+00 | 1.953e+00 | 3.863e+00 | 8.574e+01 |
| Forward Euler | 0.01 | 4.321e-02 | 2.760e-02 | 2.942e-02 | 1.052e-01 |
| Velocity-Verlet | 0.5 | 6.303e-02 | 6.663e-02 | 6.544e-02 | 6.231e-02 |
| Velocity-Verlet | 0.01 | 2.267e-05 | 2.816e-05 | 2.574e-05 | 2.500e-05 |
| RK4 | 0.5 | 8.076e-04 | 5.127e-03 | 3.035e-03 | 4.196e-03 |
| RK4 | 0.01 | 4.475e-10 | 7.030e-10 | 4.812e-10 | 1.389e-11 |
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

## Results 1 Endpoint Values (Markdown)
```markdown
# Results 1 HO Endpoint Values (Selected dt)

Generated: 2026-03-11T12:01:15Z

| Integrator | dt | x_num(T) | x_exact(T) | abs(Δx(T)) | v_num(T) | v_exact(T) | abs(Δv(T)) |
|---|---|---|---|---|---|---|---|
| Forward Euler | 0.5 | -9.206092e+00 | -8.390715e-01 | 8.367e+00 | -1.408562e+00 | 5.440211e-01 | 1.953e+00 |
| Forward Euler | 0.1 | -1.408847e+00 | -8.390715e-01 | 5.698e-01 | 8.485069e-01 | 5.440211e-01 | 3.045e-01 |
| Forward Euler | 0.01 | -8.822800e-01 | -8.390715e-01 | 4.321e-02 | 5.716182e-01 | 5.440211e-01 | 2.760e-02 |
| Velocity-Verlet | 0.5 | -7.760410e-01 | -8.390715e-01 | 6.303e-02 | 6.106556e-01 | 5.440211e-01 | 6.663e-02 |
| Velocity-Verlet | 0.1 | -8.367949e-01 | -8.390715e-01 | 2.277e-03 | 5.468316e-01 | 5.440211e-01 | 2.811e-03 |
| Velocity-Verlet | 0.01 | -8.390489e-01 | -8.390715e-01 | 2.267e-05 | 5.440493e-01 | 5.440211e-01 | 2.816e-05 |
| RK4 | 0.5 | -8.398791e-01 | -8.390715e-01 | 8.076e-04 | 5.388941e-01 | 5.440211e-01 | 5.127e-03 |
| RK4 | 0.1 | -8.390755e-01 | -8.390715e-01 | 3.935e-06 | 5.440138e-01 | 5.440211e-01 | 7.345e-06 |
| RK4 | 0.01 | -8.390715e-01 | -8.390715e-01 | 4.475e-10 | 5.440211e-01 | 5.440211e-01 | 7.030e-10 |
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

## Results 1 Results-Section Notes
```markdown
# Results 1 Auto-Summary Notes

Generated: 2026-03-11T12:01:15Z

Endpoint slopes: Euler 1.05, Velocity-Verlet 2.00, RK4 3.94.
RMS slopes: Euler 1.03, Velocity-Verlet 2.00, RK4 4.00.
```

## Results 1 Figure Caption Notes
```markdown
# Results 1 Figure Caption Notes (Auto-Generated)

Generated: 2026-03-11T12:01:15Z

Figure 1(a,b) (trajectories): Verifies x(t) and v(t) behaviour for all three methods against the exact solution at dt=0.01; Euler remains the visibly largest deviation while RK4 is nearly exact on this horizon.
Figure 1(c) (phase space): Shows geometric orbit quality at dt=0.01, with Euler clearly outside the closed exact orbit and a dedicated final-sector zoom showing all methods with endpoint markers.
Figure 2(a-f) (small vs large dt): Directly demonstrates timestep sensitivity with dt=0.5 and dt=0.01 for each method, retaining full coarse-range behaviour without dense in-panel text; quantitative values are provided in the summary tables; Forward Euler coarse/fine endpoint x-error ratio = 193.64; Velocity-Verlet coarse/fine endpoint x-error ratio = 2780.53; RK4 coarse/fine endpoint x-error ratio = 1804613.76.
Figure 3(a,b) (combined convergence): Fitted slopes are Euler 1.05/1.03, Velocity-Verlet 2.00/2.00, RK4 3.94/4.00 (endpoint/RMS), consistent with orders 1/2/4; filled markers denote fit-included points and open markers denote coarse points shown for context.
Figure 4(a) (energy diagnostic): At dt=0.01, Euler exhibits strong secular drift, Velocity-Verlet shows bounded oscillatory error, and RK4 drift is tiny on this interval; RK4 remains non-symplectic.
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

## Results 2 Recommended Figure Set
```markdown
# Recommended Final Results 2 Figure Set

Main report figures (core evidence, in order):
6. `out/plots/results2_figure6_lj_brief_energy_100step_production.png` (panels: a, b)
7. `out/plots/results2_figure7_lj_brief_temperature_100step_production.png` (panel: a)
8. `out/plots/results2_figure8_lj_rdf_comparison_rahman1964.png` (panel: a)
Table: `out/summary/results2/results2_quantitative_summary_table.md` (compact quantitative table)
Rationale: this set directly answers the brief-required 100-step Verlet-vs-Euler comparison and Rahman structural comparison with no extra non-deliverable figures.
```

## Results 2 What Changed and Why
```markdown
# Results 2: What Changed and Why

1. Removed extended 600-step Results 2 figures from the active workflow and report package.
2. Kept only the three brief-facing Results 2 figures plus a compact quantitative table.
3. Replaced old sparse hard-coded Rahman points with a transparent 9-point two-tier anchor dataset (paper_anchored + shape_anchor) stored in machine-readable CSV.
4. Updated RDF figure and metadata to make provenance explicit and to avoid implying exact Rahman tabulated data.
5. Tightened required-run energy/temperature metadata to explicitly state startup/equilibration and step-0 production semantics.
6. Added automatic Results 2 quantitative summary table generation (Markdown + CSV + JSON).
7. Added report-ready claim-safe notes and explicit final Results 2 figure ordering.
```

## Plot Metadata: Results 1 Figure 1(a,b) Trajectories
```json
{
  "claim": "Shows position and velocity trajectories at dt=0.01 for Euler, Velocity-Verlet, RK4 versus exact.",
  "endpoint_note": "Near-overlap is expected at small \u0394t; endpoint errors still rank Euler > Velocity-Verlet > RK4.",
  "figure_number": 1,
  "generated_utc": "2026-03-11T12:01:13Z",
  "insets": {
    "v": {
      "placement": "inside-upper right",
      "time_window": [
        9.0,
        10.0
      ],
      "used": true
    },
    "x": {
      "placement": "inside-upper right",
      "time_window": [
        9.0,
        10.0
      ],
      "used": true
    }
  },
  "kind": "main_results1_figure",
  "panels": [
    "a) x(t)",
    "b) v(t)"
  ],
  "parameters": {
    "dt_large": 0.5,
    "dt_small": 0.01,
    "exact_solution": "x(t)=x0 cos(omega t)+(v0/omega) sin(omega t); v(t)=-x0 omega sin(omega t)+v0 cos(omega t)",
    "omega": 1.0,
    "t_final": 10.0,
    "v0": 0.0,
    "x0": 1.0
  },
  "plot_file_png": "out/plots/results1_figure1ab_trajectories_dt0p01.png",
  "shared_legend": true,
  "zoom_window": [
    9.0,
    10.0
  ]
}```

## Plot Metadata: Results 1 Figure 1(c) Phase Space
```json
{
  "claim": "Shows phase-space geometry at dt=0.01 and qualitative orbit preservation differences.",
  "figure_number": 1,
  "generated_utc": "2026-03-11T12:01:14Z",
  "kind": "main_results1_figure",
  "panel": "c) v_vs_x",
  "parameters": {
    "dt_large": 0.5,
    "dt_small": 0.01,
    "exact_solution": "x(t)=x0 cos(omega t)+(v0/omega) sin(omega t); v(t)=-x0 omega sin(omega t)+v0 cos(omega t)",
    "omega": 1.0,
    "t_final": 10.0,
    "v0": 0.0,
    "x0": 1.0
  },
  "plot_file_png": "out/plots/results1_figure1c_phase_space_dt0p01.png",
  "shared_legend": true
}```

## Plot Metadata: Results 1 Figure 2 Small-vs-Large dt
```json
{
  "claim": "Direct small-vs-large timestep comparison with full-range coarse behaviour retained; quantitative error values are reported in summary tables.",
  "error_annotations": {
    "euler": {
      "coarse": {
        "dt": 0.5,
        "endpoint_position_error": 8.367020351721887,
        "endpoint_velocity_error": 1.9525828174323399
      },
      "fine": {
        "dt": 0.01,
        "endpoint_position_error": 0.043208489127591565,
        "endpoint_velocity_error": 0.02759708518306525
      }
    },
    "rk4": {
      "coarse": {
        "dt": 0.5,
        "endpoint_position_error": 0.0008075801512805736,
        "endpoint_velocity_error": 0.005127035265358737
      },
      "fine": {
        "dt": 0.01,
        "endpoint_position_error": 4.4750858574360564e-10,
        "endpoint_velocity_error": 7.029797854940512e-10
      }
    },
    "verlet": {
      "coarse": {
        "dt": 0.5,
        "endpoint_position_error": 0.06303048743925244,
        "endpoint_velocity_error": 0.0666345063276792
      },
      "fine": {
        "dt": 0.01,
        "endpoint_position_error": 2.266852967147681e-05,
        "endpoint_velocity_error": 2.816049136322718e-05
      }
    }
  },
  "figure_number": 2,
  "generated_utc": "2026-03-11T12:01:14Z",
  "insets": {
    "euler_phase_zoom": false,
    "euler_trajectory_zoom": false
  },
  "kind": "main_results1_figure",
  "layout": {
    "columns": [
      "x(t)",
      "v(x)"
    ],
    "rows": [
      "euler",
      "verlet",
      "rk4"
    ]
  },
  "panels": [
    "a)",
    "b)",
    "c)",
    "d)",
    "e)",
    "f)"
  ],
  "parameters": {
    "dt_large": 0.5,
    "dt_small": 0.01,
    "exact_solution": "x(t)=x0 cos(omega t)+(v0/omega) sin(omega t); v(t)=-x0 omega sin(omega t)+v0 cos(omega t)",
    "omega": 1.0,
    "t_final": 10.0,
    "v0": 0.0,
    "x0": 1.0
  },
  "plot_file_png": "out/plots/results1_figure2_small_vs_large_dt.png",
  "shared_legend": true
}```

## Plot Metadata: Results 1 Figure 3 Convergence
```json
{
  "claim": "Demonstrates first-, second-, and fourth-order convergence using endpoint and RMS phase-space metrics.",
  "coarse_points_retained_on_plot": true,
  "figure_number": 3,
  "fit_rule": "dt <= 0.1; fallback to smallest half if fewer than 3 points",
  "fits": {
    "endpoint_position_error": {
      "euler": {
        "excluded_dt_values": [
          0.5,
          1.0
        ],
        "expected_order": 1,
        "fit_dt_values": [
          0.0005,
          0.001,
          0.005,
          0.01,
          0.05,
          0.1
        ],
        "fitted_slope": 1.0501683187830357
      },
      "rk4": {
        "excluded_dt_values": [
          0.5,
          1.0
        ],
        "expected_order": 4,
        "fit_dt_values": [
          0.001,
          0.005,
          0.01,
          0.05,
          0.1
        ],
        "fitted_slope": 3.9442304587115364
      },
      "verlet": {
        "excluded_dt_values": [
          0.5,
          1.0
        ],
        "expected_order": 2,
        "fit_dt_values": [
          0.0005,
          0.001,
          0.005,
          0.01,
          0.05,
          0.1
        ],
        "fitted_slope": 2.000620867369962
      }
    },
    "rms_phase_space_error": {
      "euler": {
        "excluded_dt_values": [
          0.5,
          1.0
        ],
        "expected_order": 1,
        "fit_dt_values": [
          0.0005,
          0.001,
          0.005,
          0.01,
          0.05,
          0.1
        ],
        "fitted_slope": 1.0321586375426217
      },
      "rk4": {
        "excluded_dt_values": [
          0.5,
          1.0
        ],
        "expected_order": 4,
        "fit_dt_values": [
          0.0005,
          0.001,
          0.005,
          0.01,
          0.05,
          0.1
        ],
        "fitted_slope": 3.996152298168813
      },
      "verlet": {
        "excluded_dt_values": [
          0.5,
          1.0
        ],
        "expected_order": 2,
        "fit_dt_values": [
          0.0005,
          0.001,
          0.005,
          0.01,
          0.05,
          0.1
        ],
        "fitted_slope": 2.0000840953366517
      }
    }
  },
  "generated_utc": "2026-03-11T12:01:15Z",
  "kind": "main_results1_figure",
  "panels": [
    "a) endpoint_position_error",
    "b) rms_phase_space_error"
  ],
  "parameters": {
    "dt_large": 0.5,
    "dt_small": 0.01,
    "exact_solution": "x(t)=x0 cos(omega t)+(v0/omega) sin(omega t); v(t)=-x0 omega sin(omega t)+v0 cos(omega t)",
    "omega": 1.0,
    "t_final": 10.0,
    "v0": 0.0,
    "x0": 1.0
  },
  "plot_file_png": "out/plots/results1_figure3_convergence_combined.png"
}```

## Plot Metadata: Results 1 Figure 4 Energy Diagnostic
```json
{
  "claim": "Supporting diagnostic: Euler shows strong drift, Velocity-Verlet bounded oscillatory error, RK4 tiny drift on this interval.",
  "figure_number": 4,
  "generated_utc": "2026-03-11T12:01:15Z",
  "kind": "supporting_results1_figure",
  "note": "RK4 is not symplectic.",
  "parameters": {
    "dt_large": 0.5,
    "dt_small": 0.01,
    "exact_solution": "x(t)=x0 cos(omega t)+(v0/omega) sin(omega t); v(t)=-x0 omega sin(omega t)+v0 cos(omega t)",
    "omega": 1.0,
    "t_final": 10.0,
    "v0": 0.0,
    "x0": 1.0
  },
  "plot_file_png": "out/plots/results1_figure4_energy_diagnostic.png"
}```

## Plot Metadata: Results 2 Figure 6 Energy Drift
```json
{
  "audience_tier": "main-report-core",
  "caveats": [
    "Relative drift is computed from total energy with E0 taken at the first finite production frame.",
    "LJ uses a hard cutoff without potential shifting; small energy discontinuities can occur when pairs cross r_cut.",
    "For required-run interpretation, startup/equilibration is completed before this production trajectory."
  ],
  "figure_filename": "results2_figure6_lj_brief_energy_100step_production.png",
  "figure_number": 6,
  "fit_or_truncation": {
    "applied_xlim_ps": [
      0.0,
      1.0
    ],
    "crop_to_euler_divergence": false,
    "divergent_tail_handling": "no tail omitted; full available production window is plotted",
    "drift_only": true,
    "relative_deviation_reference": "first finite E_total point at or after production_start_step"
  },
  "generated_utc": "2026-03-11T12:01:13Z",
  "intended_claim": "At the required run length, Velocity-Verlet gives a physically meaningful bounded NVE trajectory in total energy; Forward Euler shows strong total-energy drift and is unreliable.",
  "key_parameters": {
    "drift_only_figure": true,
    "energy_units": "epsilon",
    "figure_layout": {
      "columns": [
        "signed relative total-energy deviation \u0394E/E0 [%] vs time [ps]"
      ],
      "rows": [
        "Velocity-Verlet",
        "Forward Euler"
      ]
    },
    "integrators_compared": [
      "verlet",
      "euler"
    ],
    "panel_content": "signed relative total-energy deviation only (\u0394E/E0 [%])",
    "run_semantics": {
      "final_rescale_before_production_expected": true,
      "required_production_steps": 100,
      "required_production_time_ps": 1.0,
      "startup_precedes_production": true,
      "step_0_semantics": "step 0 in CSV is the production initial frame"
    },
    "series_parameters": {
      "euler": {
        "L": 3.47786e-09,
        "N": 864,
        "P": 4,
        "dt": 1e-14,
        "equilibration_steps": 50,
        "final_rescale_applied": true,
        "final_rescale_before_production": true,
        "gr_discard_steps": 200,
        "gr_sample_every": 5,
        "gr_start": 200,
        "integrator": "euler",
        "mode": "lj",
        "n_frames": 101,
        "n_steps": 100,
        "production_nve": true,
        "production_start_step": 0,
        "production_steps": 100,
        "rcut": 7.65e-10,
        "startup_temperature_after_final_rescale": 94.4,
        "startup_temperature_before_final_rescale": 95.9438964430546,
        "target_temperature": 94.4,
        "timestamp": "2026-03-08T18:23:53Z",
        "total_steps_executed": 150
      },
      "verlet": {
        "L": 3.47786e-09,
        "N": 864,
        "P": 4,
        "dt": 1e-14,
        "equilibration_steps": 50,
        "final_rescale_applied": true,
        "final_rescale_before_production": true,
        "gr_discard_steps": 200,
        "gr_sample_every": 5,
        "gr_start": 200,
        "integrator": "verlet",
        "mode": "lj",
        "n_frames": 101,
        "n_steps": 100,
        "production_nve": true,
        "production_start_step": 0,
        "production_steps": 100,
        "rcut": 7.65e-10,
        "startup_temperature_after_final_rescale": 94.4,
        "startup_temperature_before_final_rescale": 94.3304820914355,
        "target_temperature": 94.4,
        "timestamp": "2026-03-08T18:23:51Z",
        "total_steps_executed": 150
      }
    },
    "temperature_divergence_threshold_k": 10000.0
  },
  "key_quantitative_summary": {
    "euler_divergence_time_ps": null,
    "max_time_ps_in_source": 1.0,
    "per_integrator": [
      {
        "divergence_reason": null,
        "divergence_step": null,
        "divergence_time_ps": null,
        "divergent_tail_omitted": false,
        "final_relative_energy_deviation_percent": 0.026317557803661323,
        "integrator": "verlet",
        "label": "Velocity-Verlet",
        "manifest_key": "lj_brief.verlet",
        "max_abs_relative_energy_deviation_percent": 0.08170372894395177,
        "mean_abs_relative_energy_deviation_percent": 0.03263207498204814,
        "mean_total_energy_eps": -3492.4966292122112,
        "points_plotted": 101,
        "reference_step_for_relative_deviation": 0,
        "run_identifier": "lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329",
        "source_file": "out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329/lj_verlet.csv"
      },
      {
        "divergence_reason": null,
        "divergence_step": null,
        "divergence_time_ps": null,
        "divergent_tail_omitted": false,
        "final_relative_energy_deviation_percent": 127.58742647206233,
        "integrator": "euler",
        "label": "Forward Euler",
        "manifest_key": "lj_brief.euler",
        "max_abs_relative_energy_deviation_percent": 127.58742647206233,
        "mean_abs_relative_energy_deviation_percent": 39.787667992896495,
        "mean_total_energy_eps": -2097.2542526111656,
        "points_plotted": 101,
        "reference_step_for_relative_deviation": 0,
        "run_identifier": "lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329",
        "source_file": "out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329/lj_euler.csv"
      }
    ]
  },
  "missing_provenance": [],
  "panels": [
    "a)",
    "b)"
  ],
  "plot_file_png": "out/plots/results2_figure6_lj_brief_energy_100step_production.png",
  "purpose": "Core brief-facing evidence for the required 100-step production run using signed total-energy drift only: Velocity-Verlet remains bounded while Forward Euler drifts strongly.",
  "section": "results2",
  "simulation_run_identifiers": [
    "lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329",
    "lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329"
  ],
  "source_data_files": [
    "out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329/lj_verlet.csv",
    "out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329/lj_euler.csv"
  ],
  "source_manifest_keys": [
    "lj_brief.verlet",
    "lj_brief.euler"
  ]
}```

## Plot Metadata: Results 2 Figure 7 Temperature
```json
{
  "audience_tier": "main-report-core",
  "caveats": [
    "Temperature is shown only for finite values; divergent tails are omitted.",
    "Target temperature line is a reference, not a fitted value.",
    "Temperature evidence is complementary and should be interpreted with the energy and RDF results."
  ],
  "figure_filename": "results2_figure7_lj_brief_temperature_100step_production.png",
  "figure_number": 7,
  "fit_or_truncation": {
    "applied_xlim_ps": null,
    "crop_to_euler_divergence": false,
    "divergent_tail_handling": "non-finite values or |T| > threshold are omitted from plotted tail",
    "production_start_line_ps": null,
    "zoom_inset": null
  },
  "generated_utc": "2026-03-11T12:01:13Z",
  "intended_claim": "Velocity-Verlet remains close to the target state while Forward Euler heats strongly over the same required window.",
  "key_parameters": {
    "integrators_compared": [
      "verlet",
      "euler"
    ],
    "run_semantics": {
      "final_rescale_before_production_expected": true,
      "required_production_steps": 100,
      "required_production_time_ps": 1.0,
      "startup_precedes_production": true,
      "step_0_semantics": "step 0 in CSV is the production initial frame"
    },
    "series_parameters": {
      "euler": {
        "L": 3.47786e-09,
        "N": 864,
        "P": 4,
        "dt": 1e-14,
        "equilibration_steps": 50,
        "final_rescale_applied": true,
        "final_rescale_before_production": true,
        "gr_discard_steps": 200,
        "gr_sample_every": 5,
        "gr_start": 200,
        "integrator": "euler",
        "mode": "lj",
        "n_frames": 101,
        "n_steps": 100,
        "production_nve": true,
        "production_start_step": 0,
        "production_steps": 100,
        "rcut": 7.65e-10,
        "startup_temperature_after_final_rescale": 94.4,
        "startup_temperature_before_final_rescale": 95.9438964430546,
        "target_temperature": 94.4,
        "timestamp": "2026-03-08T18:23:53Z",
        "total_steps_executed": 150
      },
      "verlet": {
        "L": 3.47786e-09,
        "N": 864,
        "P": 4,
        "dt": 1e-14,
        "equilibration_steps": 50,
        "final_rescale_applied": true,
        "final_rescale_before_production": true,
        "gr_discard_steps": 200,
        "gr_sample_every": 5,
        "gr_start": 200,
        "integrator": "verlet",
        "mode": "lj",
        "n_frames": 101,
        "n_steps": 100,
        "production_nve": true,
        "production_start_step": 0,
        "production_steps": 100,
        "rcut": 7.65e-10,
        "startup_temperature_after_final_rescale": 94.4,
        "startup_temperature_before_final_rescale": 94.3304820914355,
        "target_temperature": 94.4,
        "timestamp": "2026-03-08T18:23:51Z",
        "total_steps_executed": 150
      }
    },
    "target_temperature_k": 94.4,
    "temperature_divergence_threshold_k": 10000.0
  },
  "key_quantitative_summary": {
    "euler_divergence_time_ps": null,
    "max_time_ps_in_source": 1.0,
    "per_integrator": [
      {
        "divergence_reason": null,
        "divergence_step": null,
        "divergence_time_ps": null,
        "divergent_tail_omitted": false,
        "integrator": "verlet",
        "label": "Velocity-Verlet",
        "manifest_key": "lj_brief.verlet",
        "max_temperature_k": 97.8050863147049,
        "mean_temperature_k": 94.41593148560327,
        "min_temperature_k": 92.3947902866263,
        "points_plotted": 101,
        "run_identifier": "lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329",
        "source_file": "out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329/lj_verlet.csv",
        "std_temperature_k": 1.4282228787363203
      },
      {
        "divergence_reason": null,
        "divergence_step": null,
        "divergence_time_ps": null,
        "divergent_tail_omitted": false,
        "integrator": "euler",
        "label": "Forward Euler",
        "manifest_key": "lj_brief.euler",
        "max_temperature_k": 396.052822933143,
        "mean_temperature_k": 185.2703017814398,
        "min_temperature_k": 94.4,
        "points_plotted": 101,
        "run_identifier": "lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329",
        "source_file": "out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329/lj_euler.csv",
        "std_temperature_k": 74.5745315977212
      }
    ]
  },
  "missing_provenance": [],
  "panels": [
    "a)"
  ],
  "plot_file_png": "out/plots/results2_figure7_lj_brief_temperature_100step_production.png",
  "purpose": "Core brief-facing evidence for the required 100-step production run temperature response.",
  "section": "results2",
  "simulation_run_identifiers": [
    "lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329",
    "lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329"
  ],
  "source_data_files": [
    "out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329/lj_verlet.csv",
    "out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329/lj_euler.csv"
  ],
  "source_manifest_keys": [
    "lj_brief.verlet",
    "lj_brief.euler"
  ]
}```

## Plot Metadata: Results 2 Figure 8 RDF vs Rahman
```json
{
  "audience_tier": "main-report-core",
  "caveats": [
    "Rahman comparison uses a manually extracted approximate reference guide from printed Fig. 2.",
    "Sigma = 3.4 \u00c5 is paper-supported; x-positions 3.7 \u00c5, 7.0 \u00c5, and 10.4 \u00c5 are paper-anchored figure annotations.",
    "All Rahman g(r) values and all non-anchored x-values are approximate manual reads from the printed plot.",
    "No error bars are shown; comparison is qualitative/semi-quantitative rather than exact."
  ],
  "figure_filename": "results2_figure8_lj_rdf_comparison_rahman1964.png",
  "figure_number": 8,
  "fit_or_truncation": {
    "present_work_truncation": "none",
    "reference_guide": "shape-preserving cubic dashed guide through manual anchor points"
  },
  "generated_utc": "2026-03-11T12:01:14Z",
  "intended_claim": "The present Velocity-Verlet RDF reproduces liquid-argon shell structure (first peak, first minimum, second shell, long-range trend) with qualitative/semi-quantitative agreement to Rahman (1964), while peak heights are somewhat reduced.",
  "key_parameters": {
    "distance_units": {
      "main_axis": "r/sigma",
      "secondary_axis": "angstrom",
      "sigma_angstrom": 3.4
    },
    "present_work_series": {
      "L": 3.47786e-09,
      "N": 864,
      "P": 4,
      "dt": 1e-14,
      "equilibration_steps": 50,
      "final_rescale_applied": true,
      "final_rescale_before_production": true,
      "gr_discard_steps": 200,
      "gr_sample_every": 5,
      "gr_start": 200,
      "integrator": "verlet",
      "mode": "lj",
      "n_frames": 20001,
      "n_steps": 20000,
      "production_nve": true,
      "production_start_step": 0,
      "production_steps": 20000,
      "rcut": 7.65e-10,
      "target_temperature": 94.4,
      "timestamp": "2026-03-07T20:17:21Z",
      "total_steps_executed": 20050
    },
    "reference_dataset": {
      "model": "two-tier manual anchor set (paper_anchored + shape_anchor)",
      "n_points_paper_anchored": 3,
      "n_points_shape_anchor": 6,
      "n_points_total": 9,
      "paper_anchored_x_angstrom": [
        3.7,
        7.0,
        10.4
      ],
      "paper_sigma_angstrom": 3.4,
      "source_file": "out/summary/results2/rahman1964_fig2_manual_anchors.csv"
    }
  },
  "key_quantitative_summary": {
    "present_work_first_minimum_g": 0.622883,
    "present_work_first_minimum_r_over_sigma": 1.55,
    "present_work_first_peak_g": 2.83818,
    "present_work_first_peak_r_over_sigma": 1.09,
    "present_work_long_range_mean_g_for_r_over_sigma_ge_4": 1.0023870363636365,
    "present_work_second_peak_g": 1.2526,
    "present_work_second_peak_r_over_sigma": 2.07,
    "rahman_anchor_points": [
      {
        "g_value": 0.0,
        "point_id": 1,
        "point_type": "shape_anchor",
        "r_angstrom": 3.0,
        "r_over_sigma": 0.882353,
        "source_note": "approximate onset / exclusion-region anchor from printed figure",
        "uncertainty_note": "manual visual extraction from printed curve; approximate y and x"
      },
      {
        "g_value": 2.7,
        "point_id": 2,
        "point_type": "paper_anchored",
        "r_angstrom": 3.7,
        "r_over_sigma": 1.088235,
        "source_note": "x-position from Rahman Fig. 2 annotation; y estimated from plotted peak",
        "uncertainty_note": "x anchored to annotated figure value; y manually estimated from printed curve"
      },
      {
        "g_value": 1.35,
        "point_id": 3,
        "point_type": "shape_anchor",
        "r_angstrom": 4.5,
        "r_over_sigma": 1.323529,
        "source_note": "approximate descending shoulder after first peak",
        "uncertainty_note": "manual visual extraction from printed curve; approximate y and x"
      },
      {
        "g_value": 0.62,
        "point_id": 4,
        "point_type": "shape_anchor",
        "r_angstrom": 5.3,
        "r_over_sigma": 1.558824,
        "source_note": "approximate first minimum from printed figure",
        "uncertainty_note": "manual visual extraction from printed curve; approximate y and x"
      },
      {
        "g_value": 1.25,
        "point_id": 5,
        "point_type": "paper_anchored",
        "r_angstrom": 7.0,
        "r_over_sigma": 2.058824,
        "source_note": "x-position from Rahman Fig. 2 annotation; y estimated from plotted second-shell peak",
        "uncertainty_note": "x anchored to annotated figure value; y manually estimated from printed curve"
      },
      {
        "g_value": 0.95,
        "point_id": 6,
        "point_type": "shape_anchor",
        "r_angstrom": 8.0,
        "r_over_sigma": 2.352941,
        "source_note": "approximate post-second-peak descent",
        "uncertainty_note": "manual visual extraction from printed curve; approximate y and x"
      },
      {
        "g_value": 0.82,
        "point_id": 7,
        "point_type": "shape_anchor",
        "r_angstrom": 8.8,
        "r_over_sigma": 2.588235,
        "source_note": "approximate second minimum / oscillatory trough",
        "uncertainty_note": "manual visual extraction from printed curve; approximate y and x"
      },
      {
        "g_value": 1.05,
        "point_id": 8,
        "point_type": "paper_anchored",
        "r_angstrom": 10.4,
        "r_over_sigma": 3.058824,
        "source_note": "x-position from Rahman Fig. 2 annotation; y estimated from printed curve near third-shell region",
        "uncertainty_note": "x anchored to annotated figure value; y manually estimated from printed curve"
      },
      {
        "g_value": 1.0,
        "point_id": 9,
        "point_type": "shape_anchor",
        "r_angstrom": 11.6,
        "r_over_sigma": 3.411765,
        "source_note": "approximate long-range return toward unity",
        "uncertainty_note": "manual visual extraction from printed curve; approximate y and x"
      }
    ]
  },
  "missing_provenance": [],
  "panels": [
    "a)"
  ],
  "plot_file_png": "out/plots/results2_figure8_lj_rdf_comparison_rahman1964.png",
  "purpose": "Core brief-facing structural evidence: compare present-work Argon RDF against a transparent manually extracted Rahman (1964) Fig. 2 anchor guide.",
  "section": "results2",
  "simulation_run_identifiers": [
    "lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536"
  ],
  "source_data_files": [
    "out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/gr.csv",
    "out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/lj_verlet.csv",
    "out/summary/results2/rahman1964_fig2_manual_anchors.csv"
  ],
  "source_manifest_keys": [
    "lj_rdf.verlet_long",
    "lj_rdf.verlet_long_energy"
  ]
}```

## Plot Metadata: Results 3 Figure 9 Size Scaling
```json
{
  "audience_tier": "brief-facing",
  "caveats": [
    "Power-law exponents depend on the chosen fit domain (here N >= 500).",
    "Communication fraction uses max rank communication timing from solver output, not network-level profiling counters.",
    "O(...) expressions in the legend are empirical power-law fits over the tested range, not rigorous statements of asymptotic complexity."
  ],
  "figure_filename": "results3_figure9ab_problem_size_scaling_fixed_p16.png",
  "figure_number": 9,
  "fit_or_truncation": {
    "excluded_from_power_law_fit": [
      108,
      256
    ],
    "fit_method": "linear regression in log10-space on selected N values",
    "power_law_fit_domain": [
      500,
      864,
      1372,
      2048
    ]
  },
  "generated_utc": "2026-03-11T12:01:14Z",
  "intended_claim": "Runtime grows approximately as a power law near O(N^2) while communication fraction changes with size at fixed P=16.",
  "key_parameters": {
    "fit_mask_for_power_law": "N >= 500",
    "fixed_process_count_P": 16,
    "integrator": "verlet",
    "particle_counts_N": [
      108,
      256,
      500,
      864,
      1372,
      2048
    ],
    "reference_curve": "~N^2 anchored to largest-N wall time"
  },
  "key_quantitative_summary": {
    "communication_fraction_percent_range": [
      13.062408502492046,
      50.830138623675346
    ],
    "remaining_runtime_power_law_exponent": 1.928924774986787,
    "rows": [
      {
        "N": 108,
        "P": 16,
        "comm_max_s": 0.034871,
        "communication_fraction_percent": 50.830138623675346,
        "remaining_runtime_s": 0.033732,
        "wall_s": 0.068603
      },
      {
        "N": 256,
        "P": 16,
        "comm_max_s": 0.098397,
        "communication_fraction_percent": 27.19268428165184,
        "remaining_runtime_s": 0.26345399999999997,
        "wall_s": 0.361851
      },
      {
        "N": 500,
        "P": 16,
        "comm_max_s": 0.323552,
        "communication_fraction_percent": 22.800043690124273,
        "remaining_runtime_s": 1.0955329999999999,
        "wall_s": 1.419085
      },
      {
        "N": 864,
        "P": 16,
        "comm_max_s": 0.711096,
        "communication_fraction_percent": 18.478915052123774,
        "remaining_runtime_s": 3.137052,
        "wall_s": 3.848148
      },
      {
        "N": 1372,
        "P": 16,
        "comm_max_s": 1.511462,
        "communication_fraction_percent": 16.60471919851515,
        "remaining_runtime_s": 7.591143000000001,
        "wall_s": 9.102605
      },
      {
        "N": 2048,
        "P": 16,
        "comm_max_s": 2.507444,
        "communication_fraction_percent": 13.062408502492046,
        "remaining_runtime_s": 16.688434,
        "wall_s": 19.195878
      }
    ],
    "wall_time_power_law_exponent": 1.848050679703323
  },
  "missing_provenance": [
    "Raw per-repetition timing samples are not retained in manifest-linked files; only medians are available in scaling_size.csv.",
    "Timing step count and replication count are configured in scripts/run_all_data.sh but not encoded in scaling_size.csv."
  ],
  "panels": [
    "a)",
    "b)"
  ],
  "plot_file_png": "out/plots/results3_figure9ab_problem_size_scaling_fixed_p16.png",
  "purpose": "Main Results 3 figure for problem-size scaling at fixed process count.",
  "section": "results3",
  "simulation_run_identifiers": [],
  "source_data_files": [
    "out/scaling_size.csv",
    "out/scaling_meta.txt"
  ],
  "source_manifest_keys": [
    "scaling.size"
  ]
}```

## Plot Metadata: Results 3 Figure 10 Strong Scaling
```json
{
  "audience_tier": "brief-facing",
  "caveats": [
    "Strong-scaling data are aggregated medians, not raw replicate traces.",
    "Communication timing is solver-reported MPI_Allgatherv timing and may include measurement noise at small runtimes.",
    "Remaining runtime is defined as wall time minus critical-path communication and is not pure physical-force compute time."
  ],
  "figure_filename": "results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.png",
  "figure_number": 10,
  "fit_or_truncation": {
    "amdahl_fit_domain": "P > 1",
    "amdahl_fit_model": "S(P)=1/(f+(1-f)/P)",
    "excluded_points_from_amdahl_fit": [
      1
    ],
    "fit_method": "two-pass grid search in f (coarse 1e-3 then refined 1e-5 step over local window)"
  },
  "generated_utc": "2026-03-11T12:01:13Z",
  "intended_claim": "The MPI implementation achieves strong-scaling gains while critical-path communication (max rank communication time) contributes a measurable share of runtime.",
  "key_parameters": {
    "fixed_particle_count_N": 2048,
    "integrator": "verlet",
    "plots_in_figure": [
      "speedup",
      "efficiency",
      "critical_path_communication_vs_remaining_runtime"
    ],
    "process_counts_P": [
      1,
      2,
      4,
      8,
      16,
      24,
      32
    ]
  },
  "key_quantitative_summary": {
    "amdahl_serial_fraction_f": 0.010273219213813274,
    "efficiency_range": [
      0.7537504939262162,
      1.0
    ],
    "max_measured_speedup": 24.120015805638918,
    "maximum_theoretical_speedup_from_fit": 97.34047129602855,
    "rows": [
      {
        "N": 2048,
        "P": 1,
        "comm_max_s": 0.001237,
        "efficiency": 1.0,
        "remaining_runtime_s": 45.963046999999996,
        "speedup": 1.0,
        "wall_s": 45.964284
      },
      {
        "N": 2048,
        "P": 2,
        "comm_max_s": 0.244091,
        "efficiency": 0.9928322722149385,
        "remaining_runtime_s": 22.903969999999997,
        "speedup": 1.985664544429877,
        "wall_s": 23.148061
      },
      {
        "N": 2048,
        "P": 4,
        "comm_max_s": 0.660859,
        "efficiency": 0.9574118096779397,
        "remaining_runtime_s": 11.341365,
        "speedup": 3.829647238711759,
        "wall_s": 12.002224
      },
      {
        "N": 2048,
        "P": 8,
        "comm_max_s": 0.554423,
        "efficiency": 0.9435239807647431,
        "remaining_runtime_s": 5.53502,
        "speedup": 7.548191846117945,
        "wall_s": 6.089443
      },
      {
        "N": 2048,
        "P": 16,
        "comm_max_s": 0.367247,
        "efficiency": 0.8939103540488575,
        "remaining_runtime_s": 2.8464620000000003,
        "speedup": 14.30256566478172,
        "wall_s": 3.213709
      },
      {
        "N": 2048,
        "P": 24,
        "comm_max_s": 0.318543,
        "efficiency": 0.8092445993767496,
        "remaining_runtime_s": 2.048082,
        "speedup": 19.42187038504199,
        "wall_s": 2.366625
      },
      {
        "N": 2048,
        "P": 32,
        "comm_max_s": 0.289675,
        "efficiency": 0.7537504939262162,
        "remaining_runtime_s": 1.615974,
        "speedup": 24.120015805638918,
        "wall_s": 1.905649
      }
    ]
  },
  "missing_provenance": [
    "Raw per-repetition timing samples are not retained in manifest-linked files; only medians are available in scaling_strong.csv.",
    "Timing step count and replication count are configured in scripts/run_all_data.sh but not encoded in scaling_strong.csv."
  ],
  "panels": [
    "a)",
    "b)",
    "c)"
  ],
  "plot_file_png": "out/plots/results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.png",
  "purpose": "Main Results 3 figure for strong scaling: show measured speedup/efficiency and a bottleneck-consistent communication breakdown.",
  "section": "results3",
  "simulation_run_identifiers": [],
  "source_data_files": [
    "out/scaling_strong.csv",
    "out/scaling_meta.txt"
  ],
  "source_manifest_keys": [
    "scaling.strong"
  ]
}```

## Radial Distribution Function g(r) (Long RDF production run)
```csv
# mode: lj, integrator: verlet, N: 864, P: 4, dt: 1e-14, steps: 20000, n_steps: 20000, n_frames: 20001, step_indexing: 0..steps (includes initial frame), total_steps_executed: 20050, seed: 42, L: 3.47786e-09, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 50, production_steps: 20000, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: true, production_nve: true, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, lattice: FCC, velocities: Box-Muller, timestamp: 2026-03-07T20:17:21Z
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
0.91,0.0026883
0.93,0.0258626
0.95,0.13254
0.97,0.415982
0.99,0.909593
1.01,1.52879
1.03,2.12271
1.05,2.55824
1.07,2.79342
1.09,2.83818
1.11,2.74759
1.13,2.5743
1.15,2.35791
1.17,2.13456
1.19,1.92518
1.21,1.72541
1.23,1.549
1.25,1.39402
1.27,1.25852
1.29,1.14503
1.31,1.04926
1.33,0.964017
1.35,0.897164
1.37,0.836888
1.39,0.785884
1.41,0.745955
1.43,0.710637
1.45,0.683179
1.47,0.660071
1.49,0.643386
1.51,0.633484
1.53,0.627207
1.55,0.622883
1.57,0.62378
1.59,0.625782
1.61,0.633595
1.63,0.642956
1.65,0.658775
1.67,0.678359
1.69,0.701352
1.71,0.727159
1.73,0.757657
1.75,0.791516
1.77,0.826932
1.79,0.865815
1.81,0.904164
1.83,0.944967
1.85,0.981598
1.87,1.02022
1.89,1.05282
1.91,1.08999
1.93,1.1195
1.95,1.14849
1.97,1.17294
1.99,1.19701
2.01,1.2176
2.03,1.23404
2.05,1.2466
2.07,1.2526
2.09,1.25252
2.11,1.24885
2.13,1.2401
2.15,1.22373
2.17,1.2013
2.19,1.17938
2.21,1.15189
2.23,1.12323
2.25,1.09326
2.27,1.06476
2.29,1.03898
2.31,1.01213
2.33,0.98853
2.35,0.965112
2.37,0.943586
2.39,0.924586
2.41,0.908281
2.43,0.892499
2.45,0.882044
2.47,0.872744
2.49,0.86742
2.51,0.863286
2.53,0.861892
2.55,0.861865
2.57,0.865552
2.59,0.871718
2.61,0.877089
2.63,0.886204
2.65,0.897838
2.67,0.909019
2.69,0.923674
2.71,0.937226
2.73,0.951815
2.75,0.968815
2.77,0.983933
2.79,0.996281
2.81,1.01095
2.83,1.02361
2.85,1.03622
2.87,1.04783
2.89,1.05734
2.91,1.06592
2.93,1.07225
2.95,1.07681
2.97,1.08191
2.99,1.08315
3.01,1.08323
3.03,1.08206
3.05,1.07944
3.07,1.07468
3.09,1.07248
3.11,1.06628
3.13,1.06023
3.15,1.05337
3.17,1.04516
3.19,1.03709
3.21,1.02859
3.23,1.01881
3.25,1.01092
3.27,1.00279
3.29,0.994356
3.31,0.986455
3.33,0.980317
3.35,0.973186
3.37,0.967382
3.39,0.963043
3.41,0.958407
3.43,0.955429
3.45,0.952798
3.47,0.952467
3.49,0.949905
3.51,0.950979
3.53,0.95229
3.55,0.953391
3.57,0.956281
3.59,0.960488
3.61,0.963854
3.63,0.969534
3.65,0.974281
3.67,0.978263
3.69,0.985022
3.71,0.989991
3.73,0.995813
3.75,1.00217
3.77,1.0078
3.79,1.01197
3.81,1.01722
3.83,1.01972
3.85,1.0244
3.87,1.02711
3.89,1.02969
3.91,1.03245
3.93,1.03333
3.95,1.03214
3.97,1.03275
3.99,1.0322
4.01,1.03069
4.03,1.02851
4.05,1.02701
4.07,1.02378
4.09,1.02274
4.11,1.01889
4.13,1.0162
4.15,1.01261
4.17,1.00974
4.19,1.00719
4.21,1.00284
4.23,1.00014
4.25,0.997787
4.27,0.994053
4.29,0.991889
4.31,0.988648
4.33,0.986441
4.35,0.984858
4.37,0.98405
4.39,0.98237
4.41,0.982991
4.43,0.981283
4.45,0.981724
4.47,0.981088
4.49,0.982287
4.51,0.982634
4.53,0.98447
4.55,0.985861
4.57,0.987678
4.59,0.990277
4.61,0.991404
4.63,0.993918
4.65,0.995969
4.67,0.998167
4.69,1.00041
4.71,1.00289
4.73,1.00444
4.75,1.00641
4.77,1.00874
4.79,1.00953
4.81,1.01134
4.83,1.01165
4.85,1.01287
4.87,1.0123
4.89,1.01234
4.91,1.01306
4.93,1.01338
4.95,1.01275
4.97,1.01183
4.99,1.01206
5.01,1.01128
5.03,1.00998
5.05,1.00888
5.07,1.00813
5.09,1.00683
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
# mode: lj, integrator: verlet, N: 864, P: 4, dt: 1e-14, steps: 20000, n_steps: 20000, n_frames: 20001, step_indexing: 0..steps (includes initial frame), total_steps_executed: 20050, seed: 42, L: 3.47786e-09, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 50, production_steps: 20000, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: true, production_nve: true, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, startup_temperature_before_final_rescale: 94.3304820914355, startup_temperature_after_final_rescale: 94.4, lattice: FCC, velocities: Box-Muller, timestamp: 2026-03-07T20:15:59Z
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
19996,1.9996e-10,1.65858283722758e-18,-7.44452466037812e-18,-5.78594182315054e-18,92.8008233947411
19997,1.9997e-10,1.65317504285859e-18,-7.43975732746471e-18,-5.78658228460612e-18,92.498247147762
19998,1.9998e-10,1.65044538580607e-18,-7.43623420515029e-18,-5.78578881934422e-18,92.3455177112978
19999,1.9999e-10,1.65090291538904e-18,-7.4368571594683e-18,-5.78595424407926e-18,92.3711173503838
20000,2e-10,1.65432864996233e-18,-7.44032634879736e-18,-5.78599769883503e-18,92.5627936308788
```

## Results 3 Scaling Evidence Bundle

This section makes Results 3 explicit: benchmark inputs, derived metadata, and the code path that turns timed MPI runs into the scaling claims used in the report.

## Results 3 Hardware / Environment Snapshot
```text
hostname: dock-sc-r1l.dar.private.cam.ac.uk
cpu: unknown
compiler: Apple clang version 17.0.0 (clang-1700.0.13.5)
mpi: mpirun (Open MPI) 5.0.8
date: 2026-03-10T15:03:22+00:00
```

## Results 3 Strong Scaling Figure Metadata
```json
{
  "audience_tier": "brief-facing",
  "caveats": [
    "Strong-scaling data are aggregated medians, not raw replicate traces.",
    "Communication timing is solver-reported MPI_Allgatherv timing and may include measurement noise at small runtimes.",
    "Remaining runtime is defined as wall time minus critical-path communication and is not pure physical-force compute time."
  ],
  "figure_filename": "results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.png",
  "figure_number": 10,
  "fit_or_truncation": {
    "amdahl_fit_domain": "P > 1",
    "amdahl_fit_model": "S(P)=1/(f+(1-f)/P)",
    "excluded_points_from_amdahl_fit": [
      1
    ],
    "fit_method": "two-pass grid search in f (coarse 1e-3 then refined 1e-5 step over local window)"
  },
  "generated_utc": "2026-03-11T12:01:13Z",
  "intended_claim": "The MPI implementation achieves strong-scaling gains while critical-path communication (max rank communication time) contributes a measurable share of runtime.",
  "key_parameters": {
    "fixed_particle_count_N": 2048,
    "integrator": "verlet",
    "plots_in_figure": [
      "speedup",
      "efficiency",
      "critical_path_communication_vs_remaining_runtime"
    ],
    "process_counts_P": [
      1,
      2,
      4,
      8,
      16,
      24,
      32
    ]
  },
  "key_quantitative_summary": {
    "amdahl_serial_fraction_f": 0.010273219213813274,
    "efficiency_range": [
      0.7537504939262162,
      1.0
    ],
    "max_measured_speedup": 24.120015805638918,
    "maximum_theoretical_speedup_from_fit": 97.34047129602855,
    "rows": [
      {
        "N": 2048,
        "P": 1,
        "comm_max_s": 0.001237,
        "efficiency": 1.0,
        "remaining_runtime_s": 45.963046999999996,
        "speedup": 1.0,
        "wall_s": 45.964284
      },
      {
        "N": 2048,
        "P": 2,
        "comm_max_s": 0.244091,
        "efficiency": 0.9928322722149385,
        "remaining_runtime_s": 22.903969999999997,
        "speedup": 1.985664544429877,
        "wall_s": 23.148061
      },
      {
        "N": 2048,
        "P": 4,
        "comm_max_s": 0.660859,
        "efficiency": 0.9574118096779397,
        "remaining_runtime_s": 11.341365,
        "speedup": 3.829647238711759,
        "wall_s": 12.002224
      },
      {
        "N": 2048,
        "P": 8,
        "comm_max_s": 0.554423,
        "efficiency": 0.9435239807647431,
        "remaining_runtime_s": 5.53502,
        "speedup": 7.548191846117945,
        "wall_s": 6.089443
      },
      {
        "N": 2048,
        "P": 16,
        "comm_max_s": 0.367247,
        "efficiency": 0.8939103540488575,
        "remaining_runtime_s": 2.8464620000000003,
        "speedup": 14.30256566478172,
        "wall_s": 3.213709
      },
      {
        "N": 2048,
        "P": 24,
        "comm_max_s": 0.318543,
        "efficiency": 0.8092445993767496,
        "remaining_runtime_s": 2.048082,
        "speedup": 19.42187038504199,
        "wall_s": 2.366625
      },
      {
        "N": 2048,
        "P": 32,
        "comm_max_s": 0.289675,
        "efficiency": 0.7537504939262162,
        "remaining_runtime_s": 1.615974,
        "speedup": 24.120015805638918,
        "wall_s": 1.905649
      }
    ]
  },
  "missing_provenance": [
    "Raw per-repetition timing samples are not retained in manifest-linked files; only medians are available in scaling_strong.csv.",
    "Timing step count and replication count are configured in scripts/run_all_data.sh but not encoded in scaling_strong.csv."
  ],
  "panels": [
    "a)",
    "b)",
    "c)"
  ],
  "plot_file_png": "out/plots/results3_figure10abc_strong_scaling_speedup_efficiency_breakdown.png",
  "purpose": "Main Results 3 figure for strong scaling: show measured speedup/efficiency and a bottleneck-consistent communication breakdown.",
  "section": "results3",
  "simulation_run_identifiers": [],
  "source_data_files": [
    "out/scaling_strong.csv",
    "out/scaling_meta.txt"
  ],
  "source_manifest_keys": [
    "scaling.strong"
  ]
}```

## Results 3 Size Scaling Figure Metadata
```json
{
  "audience_tier": "brief-facing",
  "caveats": [
    "Power-law exponents depend on the chosen fit domain (here N >= 500).",
    "Communication fraction uses max rank communication timing from solver output, not network-level profiling counters.",
    "O(...) expressions in the legend are empirical power-law fits over the tested range, not rigorous statements of asymptotic complexity."
  ],
  "figure_filename": "results3_figure9ab_problem_size_scaling_fixed_p16.png",
  "figure_number": 9,
  "fit_or_truncation": {
    "excluded_from_power_law_fit": [
      108,
      256
    ],
    "fit_method": "linear regression in log10-space on selected N values",
    "power_law_fit_domain": [
      500,
      864,
      1372,
      2048
    ]
  },
  "generated_utc": "2026-03-11T12:01:14Z",
  "intended_claim": "Runtime grows approximately as a power law near O(N^2) while communication fraction changes with size at fixed P=16.",
  "key_parameters": {
    "fit_mask_for_power_law": "N >= 500",
    "fixed_process_count_P": 16,
    "integrator": "verlet",
    "particle_counts_N": [
      108,
      256,
      500,
      864,
      1372,
      2048
    ],
    "reference_curve": "~N^2 anchored to largest-N wall time"
  },
  "key_quantitative_summary": {
    "communication_fraction_percent_range": [
      13.062408502492046,
      50.830138623675346
    ],
    "remaining_runtime_power_law_exponent": 1.928924774986787,
    "rows": [
      {
        "N": 108,
        "P": 16,
        "comm_max_s": 0.034871,
        "communication_fraction_percent": 50.830138623675346,
        "remaining_runtime_s": 0.033732,
        "wall_s": 0.068603
      },
      {
        "N": 256,
        "P": 16,
        "comm_max_s": 0.098397,
        "communication_fraction_percent": 27.19268428165184,
        "remaining_runtime_s": 0.26345399999999997,
        "wall_s": 0.361851
      },
      {
        "N": 500,
        "P": 16,
        "comm_max_s": 0.323552,
        "communication_fraction_percent": 22.800043690124273,
        "remaining_runtime_s": 1.0955329999999999,
        "wall_s": 1.419085
      },
      {
        "N": 864,
        "P": 16,
        "comm_max_s": 0.711096,
        "communication_fraction_percent": 18.478915052123774,
        "remaining_runtime_s": 3.137052,
        "wall_s": 3.848148
      },
      {
        "N": 1372,
        "P": 16,
        "comm_max_s": 1.511462,
        "communication_fraction_percent": 16.60471919851515,
        "remaining_runtime_s": 7.591143000000001,
        "wall_s": 9.102605
      },
      {
        "N": 2048,
        "P": 16,
        "comm_max_s": 2.507444,
        "communication_fraction_percent": 13.062408502492046,
        "remaining_runtime_s": 16.688434,
        "wall_s": 19.195878
      }
    ],
    "wall_time_power_law_exponent": 1.848050679703323
  },
  "missing_provenance": [
    "Raw per-repetition timing samples are not retained in manifest-linked files; only medians are available in scaling_size.csv.",
    "Timing step count and replication count are configured in scripts/run_all_data.sh but not encoded in scaling_size.csv."
  ],
  "panels": [
    "a)",
    "b)"
  ],
  "plot_file_png": "out/plots/results3_figure9ab_problem_size_scaling_fixed_p16.png",
  "purpose": "Main Results 3 figure for problem-size scaling at fixed process count.",
  "section": "results3",
  "simulation_run_identifiers": [],
  "source_data_files": [
    "out/scaling_size.csv",
    "out/scaling_meta.txt"
  ],
  "source_manifest_keys": [
    "scaling.size"
  ]
}```

## Results 3 Strong Scaling (median paired timings)
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

## Results 3 Strong Scaling Spread Statistics
```csv
P,N,reps,median_rep,median_wall_s,median_comm_max_s,q1_wall_s,q3_wall_s,iqr_wall_s,min_wall_s,max_wall_s
1,2048,11,5,45.964284,0.001237,45.939541,45.993862,0.054321,45.924469,46.016555
2,2048,11,4,23.148061,0.244091,23.125517,23.178700,0.053183,23.092372,23.225670
4,2048,11,6,12.002224,0.660859,11.955384,12.046293,0.090909,11.907580,12.079985
8,2048,11,7,6.089443,0.554423,6.069468,6.114131,0.044663,6.065060,6.256730
16,2048,11,6,3.213709,0.367247,3.198008,3.250974,0.052966,3.196786,3.441516
24,2048,11,11,2.366625,0.318543,2.363009,2.379657,0.016648,2.353353,2.632289
32,2048,11,5,1.905649,0.289675,1.898566,1.915836,0.017270,1.897334,2.170807
```

## Results 3 Strong Scaling Raw Repetition Samples (Truncated)
```csv
kind,P,N,rep,wall_s,comm_max_s
strong,1,2048,1,46.016555,0.001253
strong,1,2048,2,45.955620,0.001226
strong,1,2048,3,45.955775,0.001223
strong,1,2048,4,45.924469,0.001238
strong,1,2048,5,45.964284,0.001237
strong,1,2048,6,45.987326,0.001268
strong,1,2048,7,45.970233,0.001218
strong,1,2048,8,45.932030,0.001225
strong,1,2048,9,45.993862,0.001219
...
strong,32,2048,7,1.897334,0.281727
strong,32,2048,8,1.915836,0.289266
strong,32,2048,9,1.906069,0.280465
strong,32,2048,10,1.912646,0.289764
strong,32,2048,11,1.923560,0.288857
```

## Results 3 Size Scaling (median paired timings)
```csv
P,N,wall_s,comm_max_s
16,108,0.068603,0.034871
16,256,0.361851,0.098397
16,500,1.419085,0.323552
16,864,3.848148,0.711096
16,1372,9.102605,1.511462
16,2048,19.195878,2.507444
```

## Results 3 Size Scaling Spread Statistics
```csv
P,N,reps,median_rep,median_wall_s,median_comm_max_s,q1_wall_s,q3_wall_s,iqr_wall_s,min_wall_s,max_wall_s
16,108,11,3,0.068603,0.034871,0.067999,0.069374,0.001375,0.067644,0.069928
16,256,11,2,0.361851,0.098397,0.358669,0.363746,0.005077,0.358334,0.367599
16,500,11,7,1.419085,0.323552,1.409080,1.421213,0.012133,1.403141,1.486871
16,864,11,7,3.848148,0.711096,3.835492,3.852665,0.017173,3.827708,3.854997
16,1372,11,3,9.102605,1.511462,9.088830,9.179895,0.091065,9.047623,9.195848
16,2048,11,2,19.195878,2.507444,19.040896,19.237802,0.196906,19.025029,19.529586
```

## Results 3 Size Scaling Raw Repetition Samples (Truncated)
```csv
kind,P,N,rep,wall_s,comm_max_s
size,16,108,1,0.069928,0.035449
size,16,108,2,0.068176,0.033999
size,16,108,3,0.068603,0.034871
size,16,108,4,0.068718,0.034910
size,16,108,5,0.069508,0.035598
size,16,108,6,0.068311,0.034320
size,16,108,7,0.068968,0.035066
size,16,108,8,0.067847,0.034156
size,16,108,9,0.067999,0.033752
...
size,16,2048,7,19.025029,2.572275
size,16,2048,8,19.034032,2.536390
size,16,2048,9,19.040896,2.549338
size,16,2048,10,19.253514,2.676820
size,16,2048,11,19.153381,2.654435
```

## Important Code Snippets

These excerpts are included so the bundle carries the implementation context behind the figures, not only the output tables.

## Integrator Implementations Compared in Results 1/2

Source: `include/md/integrators.hpp:27-135`
```cpp
    27	template <typename RefreshForceFn>
    28	inline void stepEuler(System& sys, double dt, RefreshForceFn refreshForces) {
    29	    const int n3 = 3 * sys.localN;
    30	
    31	    // x_{n+1} = x_n + dt * v_n
    32	    for (int i = 0; i < n3; ++i) {
    33	        sys.pos[i] += sys.vel[i] * dt;
    34	    }
    35	
    36	    // v_{n+1} = v_n + dt * a_n
    37	    for (int i = 0; i < n3; ++i) {
    38	        sys.vel[i] += sys.acc[i] * dt;
    39	    }
    40	
    41	    // Update forces/accelerations at the new positions.
    42	    refreshForces();
    43	}
    44	
    45	/**
    46	 * @brief Advance one time-step with classical fourth-order Runge-Kutta.
    47	 *
    48	 * RK4 combines four stages as
    49	 *   y_{n+1} = y_n + (k1 + 2k2 + 2k3 + k4)/6,
    50	 * where y = (x, v) and
    51	 *   dx/dt = v,   dv/dt = a(x).
    52	 *
    53	 * RK4 is fourth-order accurate and works well for short-time trajectory
    54	 * accuracy, but it is not symplectic, so less suitable for long MD runs
    55	 * than Velocity-Verlet .
    56	 */
    57	template <typename RefreshForceFn>
    58	inline void stepRK4(System& sys, double dt, RefreshForceFn refreshForces) {
    59	    const int n3 = 3 * sys.localN;
    60	
    61	    // Store the initial state.
    62	    std::vector<double> x0(sys.pos);
    63	    std::vector<double> v0(sys.vel);
    64	
    65	    auto evalStage = [&](std::vector<double>& kx, std::vector<double>& kv, double weight,
    66	                         const std::vector<double>& prevKx, const std::vector<double>& prevKv) {
    67	        if (weight > 0.0) {
    68	            // Intermediate stage: y_stage = y_n + weight * previous increment
    69	            for (int i = 0; i < n3; ++i) {
    70	                sys.pos[i] = x0[i] + weight * prevKx[i];
    71	                sys.vel[i] = v0[i] + weight * prevKv[i];
    72	            }
    73	            refreshForces();
    74	        }
    75	
    76	        // For y' = (v, a): kx = dt * v, kv = dt * a
    77	        for (int i = 0; i < n3; ++i) {
    78	            kx[i] = sys.vel[i] * dt;
    79	            kv[i] = sys.acc[i] * dt;
    80	        }
    81	    };
    82	
    83	    std::vector<double> k1x(n3), k1v(n3);
    84	    evalStage(k1x, k1v, 0.0, k1x, k1v);
    85	
    86	    std::vector<double> k2x(n3), k2v(n3);
    87	    evalStage(k2x, k2v, 0.5, k1x, k1v);
    88	
    89	    std::vector<double> k3x(n3), k3v(n3);
    90	    evalStage(k3x, k3v, 0.5, k2x, k2v);
    91	
    92	    std::vector<double> k4x(n3), k4v(n3);
    93	    evalStage(k4x, k4v, 1.0, k3x, k3v);
    94	
    95	    // x_{n+1} and v_{n+1} from the RK4 weighted sum
    96	    for (int i = 0; i < n3; ++i) {
    97	        sys.pos[i] = x0[i] + (k1x[i] + 2.0 * k2x[i] + 2.0 * k3x[i] + k4x[i]) / 6.0;
    98	        sys.vel[i] = v0[i] + (k1v[i] + 2.0 * k2v[i] + 2.0 * k3v[i] + k4v[i]) / 6.0;
    99	    }
   100	
   101	    // Make stored accelerations consistent with the final state.
   102	    refreshForces();
   103	}
   104	
   105	/**
   106	 * @brief Advance one time-step with the Velocity-Verlet method.
   107	 *
   108	 * Velocity-Verlet uses
   109	 *   v_{n+1/2} = v_n + (dt/2) a_n,
   110	 *   x_{n+1}   = x_n + dt * v_{n+1/2},
   111	 *   v_{n+1}   = v_{n+1/2} + (dt/2) a_{n+1}.
   112	 *
   113	 * It is  second-order accurate, time-reversible, and symplectic .
   114	 */
   115	template <typename RefreshForceFn>
   116	inline void stepVelocityVerlet(System& sys, double dt, RefreshForceFn refreshForces) {
   117	    const int n3 = 3 * sys.localN;
   118	    const double halfDt = 0.5 * dt;
   119	
   120	    // First half-step for velocity.
   121	    for (int i = 0; i < n3; ++i) {
   122	        sys.vel[i] += halfDt * sys.acc[i];
   123	    }
   124	
   125	    // Position update using the half-step velocity.
   126	    for (int i = 0; i < n3; ++i) {
   127	        sys.pos[i] += dt * sys.vel[i];
   128	    }
   129	
   130	    // Update forces/accelerations at the new positions.
   131	    refreshForces();
   132	
   133	    // Second half-step for velocity.
   134	    for (int i = 0; i < n3; ++i) {
   135	        sys.vel[i] += halfDt * sys.acc[i];
```

## MPI Position Exchange and Force Refresh Path

Source: `src/main.cpp:341-367`
```cpp
   341	    double localPE = 0.0;
   342	    auto allgatherPositions = [&]() {
   343	        double t0 = params.timing ? MPI_Wtime() : 0.0;
   344	        MPI_Allgatherv(sys.pos.data(), 3 * localN, MPI_DOUBLE, posGlobal.data(), recvcounts.data(),
   345	                       displs.data(), MPI_DOUBLE, MPI_COMM_WORLD);
   346	        if (params.timing) {
   347	            commTime += (MPI_Wtime() - t0);
   348	        }
   349	    };
   350	    auto refreshForces = [&]() {
   351	        if (isHO) {
   352	            evalHO(sys, posGlobal, localPE);
   353	        } else {
   354	            sys.wrapPositions();
   355	            allgatherPositions();
   356	            evalLJ(sys, posGlobal, localPE);
   357	        }
   358	    };
   359	
   360	    auto advanceOneStep = [&]() {
   361	        if (intType == IntegratorType::Euler) {
   362	            md::stepEuler(sys, params.dt, refreshForces);
   363	        } else if (intType == IntegratorType::RK4) {
   364	            md::stepRK4(sys, params.dt, refreshForces);
   365	        } else {
   366	            md::stepVelocityVerlet(sys, params.dt, refreshForces);
   367	        }
```

## Timed Production Loop and Max-Reduction Timing Output

Source: `src/main.cpp:430-505`
```cpp
   430	    // Synchronise clocks before timed production loop (exclude startup/output setup).
   431	    // Reset accumulated comm timer so reported communication matches this timing window.
   432	    commTime = 0.0;
   433	    MPI_Barrier(MPI_COMM_WORLD);
   434	    const double tStart = MPI_Wtime();
   435	
   436	    for (int step = 0; step <= nSteps; ++step) {
   437	        double totalKE = 0.0;
   438	        double totalPE = 0.0;
   439	
   440	        if (!params.timing) {
   441	            const double localKE = md::computeLocalKineticEnergy(sys, md::constants::mass);
   442	            MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
   443	            MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
   444	
   445	            if (params.output && rank == 0 && outFile.is_open()) {
   446	                const double totalE = totalKE + totalPE;
   447	                const double time = step * params.dt;
   448	                if (isHO) {
   449	                    const double x = sys.pos[0];
   450	                    const double v = sys.vel[0];
   451	                    outFile << step << "," << time << "," << x << "," << v << "," << totalKE
   452	                            << "," << totalPE << "," << totalE << "\n";
   453	                } else {
   454	                    const double T = md::computeTemperature(totalKE, N);
   455	                    outFile << step << "," << time << "," << totalKE << "," << totalPE << ","
   456	                            << totalE << "," << T << "\n";
   457	                }
   458	            }
   459	        }
   460	
   461	        // Sample RDF only on production frames that pass discard/stride filters.
   462	        if (params.gr && !isHO && step >= grStart && ((step - grStart) % grSampleEvery == 0)) {
   463	            md::accumulateGR(posGlobal, N, L, offset, localN, grDr, grRMax, grHistLocal);
   464	            ++grFrames;
   465	        }
   466	
   467	        // Step 0 is the production initial condition; advance after writing/sampling.
   468	        if (step == nSteps) {
   469	            break;
   470	        }
   471	
   472	        advanceOneStep();
   473	    }
   474	
   475	    const double elapsed = MPI_Wtime() - tStart;
   476	
   477	    // Wall time: max across all ranks (the bottleneck determines completion).
   478	    // Communication bottleneck should be reduced with max across ranks as well;
   479	    // avg/min are retained as secondary diagnostics.
   480	    // Pattern follows MPI lecture-notes slide 78: independent MPI_Reduce calls.
   481	    double maxTime = 0.0;
   482	    MPI_Reduce(&elapsed, &maxTime, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
   483	
   484	    double commMax = 0.0;
   485	    double commAvg = 0.0;
   486	    double commMin = 0.0;
   487	    if (params.timing) {
   488	        double sumComm = 0.0;
   489	        MPI_Reduce(&commTime, &commMax, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
   490	        MPI_Reduce(&commTime, &commMin, 1, MPI_DOUBLE, MPI_MIN, 0, MPI_COMM_WORLD);
   491	        MPI_Reduce(&commTime, &sumComm, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
   492	        if (rank == 0) {
   493	            commAvg = sumComm / nprocs;
   494	        }
   495	    }
   496	
   497	    if (rank == 0) {
   498	        std::printf("Wall time: %.6f s (max across %d ranks)\n", maxTime, nprocs);
   499	        if (params.timing) {
   500	            const double commFracPct = (maxTime > 0.0) ? (100.0 * commMax / maxTime) : 0.0;
   501	            std::printf("  Comm time (max): %.6f s (%.1f%%)\n", commMax, commFracPct);
   502	            std::printf("  Comm time (avg): %.6f s\n", commAvg);
   503	            std::printf("  Comm time (min): %.6f s\n", commMin);
   504	        }
   505	    }
```

## Results 3 Benchmark Collection (20 Paired Repetitions, Median Pair Retained)

Source: `scripts/run_all_data.sh:203-253`
```bash
   203	echo "=== RESULTS 3: STRONG SCALING (20 reps, N=2048, ${STRONG_STEPS} steps) ==="
   204	echo "P,N,wall_s,comm_max_s" > "$OUTDIR/scaling_strong.csv"
   205	python3 scripts/append_manifest.py "scaling.strong" "$OUTDIR/scaling_strong.csv"
   206	
   207	REPS=20
   208	for P in 1 2 4 8 16 24 32; do
   209	    WALLS=""
   210	    COMMS_MAX=""
   211	    for REP in $(seq 1 $REPS); do
   212	        OUTPUT=$(mpirun -np $P $SOLVER --mode lj --integrator verlet --N 2048 --steps $STRONG_STEPS --timing 2>/dev/null)
   213	        W=$(extract_metric "$OUTPUT" "Wall time")
   214	        C_MAX=$(extract_metric "$OUTPUT" "Comm time \\(max\\)")
   215	        [ -z "$C_MAX" ] && C_MAX=$(extract_metric "$OUTPUT" "Comm time")
   216	        [ -z "$C_MAX" ] && C_MAX="0.0"
   217	        C_MAX=$(awk -v w="$W" -v c="$C_MAX" 'BEGIN{if (c > w) print w; else print c}')
   218	        WALLS="$WALLS $W"
   219	        COMMS_MAX="$COMMS_MAX $C_MAX"
   220	        echo "    P=$P rep=$REP wall=$W comm_max=$C_MAX"
   221	    done
   222	    PAIR=$(pick_median_pair "$WALLS" "$COMMS_MAX")
   223	    MEDIAN_W=$(echo "$PAIR" | awk '{print $1}')
   224	    MEDIAN_C_MAX=$(echo "$PAIR" | awk '{print $2}')
   225	    echo "$P,2048,$MEDIAN_W,$MEDIAN_C_MAX" >> "$OUTDIR/scaling_strong.csv"
   226	    echo "  >> P=$P MEDIAN: wall=$MEDIAN_W comm_max=$MEDIAN_C_MAX"
   227	done
   228	
   229	# ── 5. Size Scaling (median of 20 paired samples) ──
   230	echo ""
   231	echo "=== RESULTS 3: SIZE SCALING (20 reps, P=16, ${SIZE_STEPS} steps) ==="
   232	echo "P,N,wall_s,comm_max_s" > "$OUTDIR/scaling_size.csv"
   233	python3 scripts/append_manifest.py "scaling.size" "$OUTDIR/scaling_size.csv"
   234	
   235	for N in 108 256 500 864 1372 2048; do
   236	    WALLS=""
   237	    COMMS_MAX=""
   238	    for REP in $(seq 1 $REPS); do
   239	        OUTPUT=$(mpirun -np 16 $SOLVER --mode lj --integrator verlet --N $N --steps $SIZE_STEPS --timing 2>/dev/null)
   240	        W=$(extract_metric "$OUTPUT" "Wall time")
   241	        C_MAX=$(extract_metric "$OUTPUT" "Comm time \\(max\\)")
   242	        [ -z "$C_MAX" ] && C_MAX=$(extract_metric "$OUTPUT" "Comm time")
   243	        [ -z "$C_MAX" ] && C_MAX="0.0"
   244	        C_MAX=$(awk -v w="$W" -v c="$C_MAX" 'BEGIN{if (c > w) print w; else print c}')
   245	        WALLS="$WALLS $W"
   246	        COMMS_MAX="$COMMS_MAX $C_MAX"
   247	        echo "    N=$N rep=$REP wall=$W comm_max=$C_MAX"
   248	    done
   249	    PAIR=$(pick_median_pair "$WALLS" "$COMMS_MAX")
   250	    MEDIAN_W=$(echo "$PAIR" | awk '{print $1}')
   251	    MEDIAN_C_MAX=$(echo "$PAIR" | awk '{print $2}')
   252	    echo "16,$N,$MEDIAN_W,$MEDIAN_C_MAX" >> "$OUTDIR/scaling_size.csv"
   253	    echo "  >> N=$N MEDIAN: wall=$MEDIAN_W comm_max=$MEDIAN_C_MAX"
```

## Results 1 Fit-Point Selection and Slope Construction

Source: `scripts/plot_ho.py:370-443`
```python
   370	def select_fit_points(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
   371	    fit_pts = [(dt, err) for dt, err in points if dt <= 0.1]
   372	    if len(fit_pts) < 3:
   373	        fit_pts = sorted(points)[: max(3, len(points) // 2)]
   374	    return sorted(fit_pts)
   375	
   376	
   377	def fit_loglog(points: List[Tuple[float, float]]) -> Tuple[float, float]:
   378	    x = np.log10(np.asarray([p[0] for p in points], dtype=float))
   379	    y = np.log10(np.asarray([p[1] for p in points], dtype=float))
   380	    slope, intercept = np.polyfit(x, y, 1)
   381	    return float(slope), float(intercept)
   382	
   383	
   384	def build_fit_summary(
   385	    metrics: List[Dict[str, object]],
   386	    metric_key: str,
   387	    epsilon: float,
   388	    metric_name: str,
   389	) -> Dict[str, Dict[str, object]]:
   390	    out: Dict[str, Dict[str, object]] = {}
   391	    for integ in INTEGRATORS:
   392	        raw = []
   393	        for row in metrics:
   394	            if row["integrator"] != integ:
   395	                continue
   396	            err = float(row[metric_key])
   397	            if np.isfinite(err) and err > epsilon:
   398	                raw.append((float(row["dt"]), err))
   399	        raw = sorted(raw)
   400	        if len(raw) < 2:
   401	            continue
   402	        fit_pts = select_fit_points(raw)
   403	        if len(fit_pts) < 2:
   404	            continue
   405	        slope, intercept = fit_loglog(fit_pts)
   406	        fit_dts = [float(dt) for dt, _ in fit_pts]
   407	        excluded = [float(dt) for dt, _ in raw if not any(abs(dt - fdt) < 1e-15 for fdt in fit_dts)]
   408	        out[integ] = {
   409	            "metric": metric_name,
   410	            "integrator": integ,
   411	            "integrator_label": INTEGRATOR_LABELS[integ],
   412	            "expected_order": INTEGRATOR_ORDERS[integ],
   413	            "slope": slope,
   414	            "intercept": intercept,
   415	            "fit_dts": fit_dts,
   416	            "excluded_dts": excluded,
   417	            "n_points": len(raw),
   418	        }
   419	    return out
   420	
   421	
   422	def row_for(metrics_idx: Dict[Tuple[str, float], Dict[str, object]], integ: str, dt: float):
   423	    return metrics_idx.get((integ, dt))
   424	
   425	
   426	def merge_fit_info(endpoint_fit: Dict[str, Dict[str, object]], rms_fit: Dict[str, Dict[str, object]]):
   427	    merged = {}
   428	    for integ in INTEGRATORS:
   429	        ep = endpoint_fit.get(integ)
   430	        rm = rms_fit.get(integ)
   431	        if ep is None or rm is None:
   432	            continue
   433	        excluded_union = sorted(set([float(x) for x in ep["excluded_dts"]] + [float(x) for x in rm["excluded_dts"]]))
   434	        merged[integ] = {
   435	            "integrator_label": INTEGRATOR_LABELS[integ],
   436	            "endpoint_slope": float(ep["slope"]),
   437	            "rms_slope": float(rm["slope"]),
   438	            "expected_order": INTEGRATOR_ORDERS[integ],
   439	            "endpoint_fit_dt_values": [float(v) for v in ep["fit_dts"]],
   440	            "rms_fit_dt_values": [float(v) for v in rm["fit_dts"]],
   441	            "excluded_coarse_dt_values": excluded_union,
   442	        }
   443	    return merged
```

## Results 1 Convergence Figure and Metadata Generation

Source: `scripts/plot_ho.py:938-1015`
```python
   938	def plot_figure4_convergence_combined(
   939	    metrics: List[Dict[str, object]],
   940	    endpoint_fit: Dict[str, Dict[str, object]],
   941	    rms_fit: Dict[str, Dict[str, object]],
   942	) -> None:
   943	    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.0), constrained_layout=False)
   944	
   945	    _plot_convergence_panel(
   946	        axes[0],
   947	        metrics=metrics,
   948	        fit_summary=endpoint_fit,
   949	        metric_key="endpoint_position_error",
   950	        epsilon=1e-14,
   951	        ylabel=r"$|x_{\mathrm{num}}(T)-x_{\mathrm{exact}}(T)|$",
   952	        panel_title=r"Endpoint position error at $T=10$",
   953	    )
   954	    _plot_convergence_panel(
   955	        axes[1],
   956	        metrics=metrics,
   957	        fit_summary=rms_fit,
   958	        metric_key="rms_phase_space_error",
   959	        epsilon=1e-16,
   960	        ylabel=r"$\mathrm{RMS}_t \sqrt{(x-x_{ex})^2 + (v-v_{ex})^2}$",
   961	        panel_title=r"RMS phase-space error over $0\leq t\leq 10$",
   962	    )
   963	    add_panel_label(axes[0], "a")
   964	    add_panel_label(axes[1], "b")
   965	
   966	    fig.suptitle(
   967	        r"Convergence to the exact solution (expected orders: Euler 1, Velocity-Verlet 2, RK4 4)",
   968	        fontsize=12.8,
   969	        y=0.995,
   970	    )
   971	    fig.subplots_adjust(top=0.84, bottom=0.17, left=0.08, right=0.98, wspace=0.27)
   972	    fig.text(
   973	        0.5,
   974	        0.040,
   975	        r"Filled markers: used in slope fit ($\Delta t \leq 0.1$). Open markers: coarse points shown for context.",
   976	        ha="center",
   977	        va="center",
   978	        fontsize=9,
   979	    )
   980	
   981	    meta_fits = {
   982	        "endpoint_position_error": {
   983	            integ: {
   984	                "fitted_slope": float(info["slope"]),
   985	                "expected_order": int(info["expected_order"]),
   986	                "fit_dt_values": [float(v) for v in info["fit_dts"]],
   987	                "excluded_dt_values": [float(v) for v in info["excluded_dts"]],
   988	            }
   989	            for integ, info in endpoint_fit.items()
   990	        },
   991	        "rms_phase_space_error": {
   992	            integ: {
   993	                "fitted_slope": float(info["slope"]),
   994	                "expected_order": int(info["expected_order"]),
   995	                "fit_dt_values": [float(v) for v in info["fit_dts"]],
   996	                "excluded_dt_values": [float(v) for v in info["excluded_dts"]],
   997	            }
   998	            for integ, info in rms_fit.items()
   999	        },
  1000	    }
  1001	
  1002	    save_plot_pair(
  1003	        fig,
  1004	        FIG4_PNG,
  1005	        {
  1006	            "kind": "main_results1_figure",
  1007	            "figure_number": 3,
  1008	            "claim": "Demonstrates first-, second-, and fourth-order convergence using endpoint and RMS phase-space metrics.",
  1009	            "panels": ["a) endpoint_position_error", "b) rms_phase_space_error"],
  1010	            "fit_rule": "dt <= 0.1; fallback to smallest half if fewer than 3 points",
  1011	            "fits": meta_fits,
  1012	            "coarse_points_retained_on_plot": True,
  1013	        },
  1014	    )
  1015	    plt.close(fig)
```

## Results 1 Summary Table Generation

Source: `scripts/plot_ho.py:1136-1235`
```python
  1136	def generate_table_outputs(
  1137	    metrics: List[Dict[str, object]],
  1138	    endpoint_fit: Dict[str, Dict[str, object]],
  1139	    rms_fit: Dict[str, Dict[str, object]],
  1140	    sanity_warnings: List[str],
  1141	) -> None:
  1142	    os.makedirs(OUT_DIR, exist_ok=True)
  1143	    os.makedirs(SUMMARY_RESULTS1_DIR, exist_ok=True)
  1144	    ordered = sorted_metrics(metrics)
  1145	    idx = metrics_index(metrics)
  1146	
  1147	    # 1) Small-vs-large summary
  1148	    small_large_rows = []
  1149	    for integ in INTEGRATORS:
  1150	        for dt in [DT_LARGE, DT_SMALL]:
  1151	            row = row_for(idx, integ, dt)
  1152	            if row is None:
  1153	                continue
  1154	            small_large_rows.append(
  1155	                {
  1156	                    "integrator": integ,
  1157	                    "integrator_label": INTEGRATOR_LABELS[integ],
  1158	                    "dt": float(dt),
  1159	                    "endpoint_position_error": float(row["endpoint_position_error"]),
  1160	                    "endpoint_velocity_error": float(row["endpoint_velocity_error"]),
  1161	                    "rms_phase_space_error": float(row["rms_phase_space_error"]),
  1162	                    "max_relative_energy_drift": float(row["max_relative_energy_drift"]),
  1163	                }
  1164	            )
  1165	    write_csv(
  1166	        R1_SMALL_LARGE_CSV,
  1167	        [
  1168	            "integrator",
  1169	            "integrator_label",
  1170	            "dt",
  1171	            "endpoint_position_error",
  1172	            "endpoint_velocity_error",
  1173	            "rms_phase_space_error",
  1174	            "max_relative_energy_drift",
  1175	        ],
  1176	        small_large_rows,
  1177	    )
  1178	    small_large_md = [
  1179	        "# Results 1 HO Small-vs-Large Timestep Summary",
  1180	        "",
  1181	        f"Generated: {utc_now()}",
  1182	        "",
  1183	        markdown_table(
  1184	            [
  1185	                "Integrator",
  1186	                "dt",
  1187	                "abs(x(T)-x_exact(T))",
  1188	                "abs(v(T)-v_exact(T))",
  1189	                "RMS phase-space error",
  1190	                "max abs(E-E0)/abs(E0)",
  1191	            ],
  1192	            [
  1193	                [
  1194	                    INTEGRATOR_LABELS[str(r["integrator"])],
  1195	                    format_dt(float(r["dt"])),
  1196	                    fmt_sci(float(r["endpoint_position_error"]), 3),
  1197	                    fmt_sci(float(r["endpoint_velocity_error"]), 3),
  1198	                    fmt_sci(float(r["rms_phase_space_error"]), 3),
  1199	                    fmt_sci(float(r["max_relative_energy_drift"]), 3),
  1200	                ]
  1201	                for r in small_large_rows
  1202	            ],
  1203	        ),
  1204	    ]
  1205	    _write_markdown(R1_SMALL_LARGE_MD, small_large_md)
  1206	
  1207	    # 2) Convergence summary
  1208	    merged_fit = merge_fit_info(endpoint_fit, rms_fit)
  1209	    convergence_rows = []
  1210	    for integ in INTEGRATORS:
  1211	        info = merged_fit.get(integ)
  1212	        if info is None:
  1213	            continue
  1214	        convergence_rows.append(
  1215	            {
  1216	                "integrator": integ,
  1217	                "integrator_label": info["integrator_label"],
  1218	                "endpoint_position_slope": info["endpoint_slope"],
  1219	                "rms_phase_space_slope": info["rms_slope"],
  1220	                "endpoint_fit_dt_values": ";".join(format_dt(float(v)) for v in info["endpoint_fit_dt_values"]),
  1221	                "rms_fit_dt_values": ";".join(format_dt(float(v)) for v in info["rms_fit_dt_values"]),
  1222	                "excluded_coarse_dt_values": ";".join(format_dt(float(v)) for v in info["excluded_coarse_dt_values"]),
  1223	            }
  1224	        )
  1225	    write_csv(
  1226	        R1_CONVERGENCE_CSV,
  1227	        [
  1228	            "integrator",
  1229	            "integrator_label",
  1230	            "endpoint_position_slope",
  1231	            "rms_phase_space_slope",
  1232	            "endpoint_fit_dt_values",
  1233	            "rms_fit_dt_values",
  1234	            "excluded_coarse_dt_values",
  1235	        ],
```

## Results 2 CSV Metadata Parsing and Production-Step Semantics

Source: `scripts/plot_lj.py:303-377`
```python
   303	def parse_csv_metadata(filepath):
   304	    """Parse first metadata comment line '# key: value, ...'."""
   305	    if not os.path.exists(filepath):
   306	        return {}
   307	    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
   308	        for line in f:
   309	            if not line.startswith("#"):
   310	                break
   311	            s = line.lstrip("#").strip()
   312	            parts = [p.strip() for p in s.split(",")]
   313	            meta = {}
   314	            for part in parts:
   315	                if ":" not in part:
   316	                    continue
   317	                k, v = part.split(":", 1)
   318	                meta[k.strip()] = v.strip()
   319	            if meta:
   320	                return meta
   321	    return {}
   322	
   323	
   324	def parse_int_meta(meta, key, default):
   325	    if key not in meta:
   326	        return default
   327	    try:
   328	        return int(float(meta[key]))
   329	    except ValueError:
   330	        return default
   331	
   332	
   333	def parse_float_meta(meta, key, default):
   334	    if key not in meta:
   335	        return default
   336	    try:
   337	        return float(meta[key])
   338	    except ValueError:
   339	        return default
   340	
   341	
   342	def get_meta_value(meta, preferred_key, fallback_key, default):
   343	    if preferred_key in meta:
   344	        return parse_int_meta(meta, preferred_key, default)
   345	    if fallback_key in meta:
   346	        return parse_int_meta(meta, fallback_key, default)
   347	    return default
   348	
   349	
   350	def finite_or_nan(arr):
   351	    arr = np.asarray(arr, dtype=float)
   352	    return np.where(np.isfinite(arr), arr, np.nan)
   353	
   354	
   355	def first_nonfinite_index(*arrays):
   356	    if not arrays:
   357	        return None
   358	    invalid = np.zeros(len(arrays[0]), dtype=bool)
   359	    for arr in arrays:
   360	        invalid |= ~np.isfinite(arr)
   361	    idx = np.where(invalid)[0]
   362	    return int(idx[0]) if idx.size > 0 else None
   363	
   364	
   365	def first_exceed_index(arr, threshold):
   366	    idx = np.where(np.abs(arr) > threshold)[0]
   367	    return int(idx[0]) if idx.size > 0 else None
   368	
   369	
   370	def first_finite_prod_index(steps, etot, production_start):
   371	    for i in range(len(steps)):
   372	        if steps[i] >= production_start and np.isfinite(etot[i]):
   373	            return i
   374	    for i in range(len(steps)):
   375	        if np.isfinite(etot[i]):
   376	            return i
   377	    return None
```

## Results 2 Energy Drift Extraction and Per-Integrator Summary

Source: `scripts/plot_lj.py:455-569`
```python
   455	def plot_energy_for_run(manifest, run_key, config, out_name):
   456	    os.makedirs(PLOT_DIR, exist_ok=True)
   457	    fig, axes = plt.subplots(
   458	        2,
   459	        1,
   460	        figsize=(9.4, 7.2),
   461	        sharex=True,
   462	        constrained_layout=True,
   463	    )
   464	    any_data = False
   465	    euler_divergence_time_ps = None
   466	    max_time_ps = 0.0
   467	    x_max = None
   468	    source_data_files = []
   469	    source_manifest_keys = []
   470	    simulation_run_identifiers = []
   471	    per_integrator_summary = []
   472	    series_parameters = {}
   473	    missing_provenance = []
   474	
   475	    for row, integrator in enumerate(config["integrators"]):
   476	        series_key = integrator["series_key"]
   477	        label = integrator["label"]
   478	        style_key = integrator["style_key"]
   479	        manifest_key = f"{run_key}.{series_key}"
   480	        style = INTEGRATOR_STYLE[integrator["style_key"]]
   481	        color = style["color"]
   482	        linestyle = style["linestyle"]
   483	        linewidth = style["linewidth"]
   484	
   485	        fpath = nested_get(manifest, manifest_key)
   486	        if not fpath or not os.path.exists(fpath):
   487	            print(f"Warning: missing {manifest_key}; skipping")
   488	            missing_provenance.append(f"manifest/data file missing for {manifest_key}")
   489	            continue
   490	
   491	        series = load_series(fpath)
   492	        if series is None:
   493	            missing_provenance.append(f"series unreadable or missing required columns for {manifest_key}")
   494	            continue
   495	        any_data = True
   496	
   497	        steps = series["steps"]
   498	        t = series["time_ps"]
   499	        if np.any(np.isfinite(t)):
   500	            max_time_ps = max(max_time_ps, float(np.nanmax(t)))
   501	        etot = series["etot_eps"]
   502	        meta_typed = series["meta_typed"]
   503	        source_data_files.append(fpath)
   504	        source_manifest_keys.append(manifest_key)
   505	        simulation_run_identifiers.append(series["run_identifier"])
   506	        series_parameters[style_key] = extract_series_parameters(meta_typed)
   507	
   508	        production_start = series["production_start_step"]
   509	        ref_idx = first_finite_prod_index(steps, etot, production_start)
   510	        if ref_idx is None:
   511	            rel_dev_pct = np.full_like(etot, np.nan)
   512	            rel_dev_ref_step = None
   513	            e0 = np.nan
   514	        else:
   515	            e0 = etot[ref_idx]
   516	            if np.isfinite(e0) and abs(e0) > 1e-30:
   517	                rel_dev_pct = 100.0 * (etot - e0) / abs(e0)
   518	            else:
   519	                rel_dev_pct = np.full_like(etot, np.nan)
   520	            rel_dev_ref_step = int(steps[ref_idx])
   521	
   522	        finite_etot = etot[np.isfinite(etot)]
   523	        ax_d = axes[row]
   524	        row_label = label
   525	        ax_d.plot(t, rel_dev_pct, color=color, linestyle=linestyle, linewidth=max(2.2, linewidth), label=row_label)
   526	        ax_d.set_ylabel(r"$\Delta E / E_0$ [%]")
   527	        ax_d.axhline(0.0, color=COLOR_REFERENCE, linestyle="--", linewidth=1.0, alpha=0.6)
   528	        apply_major_grid(ax_d)
   529	        disable_offset_text(ax_d)
   530	
   531	        add_panel_label(ax_d, chr(ord("a") + row))
   532	        ax_d.legend(
   533	            loc="upper left",
   534	            bbox_to_anchor=(0.02, 0.95),
   535	            fontsize=9,
   536	            frameon=True,
   537	            facecolor="white",
   538	            edgecolor="none",
   539	            framealpha=0.86,
   540	        )
   541	
   542	        if row == 0:
   543	            ax_d.set_title(r"Signed relative drift $\Delta E/E_0$ [%]")
   544	
   545	        divergence_step = series.get("divergence_step")
   546	        divergence_time_ps = series.get("divergence_time_ps")
   547	        divergence_reason = series.get("divergence_reason")
   548	        finite_rel_pct = rel_dev_pct[np.isfinite(rel_dev_pct)]
   549	        max_abs_rel_pct = float(np.nanmax(np.abs(finite_rel_pct))) if finite_rel_pct.size else None
   550	        mean_abs_rel_pct = float(np.nanmean(np.abs(finite_rel_pct))) if finite_rel_pct.size else None
   551	        final_rel_pct = float(finite_rel_pct[-1]) if finite_rel_pct.size else None
   552	        per_integrator_summary.append(
   553	            {
   554	                "integrator": style_key,
   555	                "label": label,
   556	                "manifest_key": manifest_key,
   557	                "source_file": fpath,
   558	                "run_identifier": series["run_identifier"],
   559	                "points_plotted": int(np.count_nonzero(np.isfinite(etot))),
   560	                "reference_step_for_relative_deviation": rel_dev_ref_step,
   561	                "max_abs_relative_energy_deviation_percent": max_abs_rel_pct,
   562	                "mean_abs_relative_energy_deviation_percent": mean_abs_rel_pct,
   563	                "final_relative_energy_deviation_percent": final_rel_pct,
   564	                "mean_total_energy_eps": float(np.nanmean(finite_etot)) if finite_etot.size else None,
   565	                "divergent_tail_omitted": bool(series["has_nonfinite"]),
   566	                "divergence_step": divergence_step,
   567	                "divergence_time_ps": divergence_time_ps,
   568	                "divergence_reason": divergence_reason,
   569	            }
```

## Results 2 RDF Feature Extraction and Metadata Packaging

Source: `scripts/plot_lj.py:975-1230`
```python
   975	def extract_rdf_feature(r_vals, g_vals, rmin, rmax, mode):
   976	    mask = np.isfinite(r_vals) & np.isfinite(g_vals) & (r_vals >= rmin) & (r_vals <= rmax)
   977	    if not np.any(mask):
   978	        return None, None
   979	    rr = r_vals[mask]
   980	    gg = g_vals[mask]
   981	    idx = int(np.argmax(gg)) if mode == "max" else int(np.argmin(gg))
   982	    return float(rr[idx]), float(gg[idx])
   983	
   984	
   985	def smooth_curve_pchip(x_vals, y_vals, samples_per_segment=40):
   986	    x = np.asarray(x_vals, dtype=float)
   987	    y = np.asarray(y_vals, dtype=float)
   988	    valid = np.isfinite(x) & np.isfinite(y)
   989	    x = x[valid]
   990	    y = y[valid]
   991	    if x.size < 2:
   992	        return x, y
   993	
   994	    order = np.argsort(x)
   995	    x = x[order]
   996	    y = y[order]
   997	    x, unique_idx = np.unique(x, return_index=True)
   998	    y = y[unique_idx]
   999	
  1000	    n = x.size
  1001	    if n == 2:
  1002	        xx = np.linspace(x[0], x[1], samples_per_segment + 1)
  1003	        yy = np.interp(xx, x, y)
  1004	        return xx, yy
  1005	
  1006	    h = np.diff(x)
  1007	    delta = np.diff(y) / h
  1008	    d = np.zeros(n, dtype=float)
  1009	
  1010	    def endpoint_slope(h0, h1, delta0, delta1):
  1011	        slope = ((2.0 * h0 + h1) * delta0 - h0 * delta1) / (h0 + h1)
  1012	        if np.sign(slope) != np.sign(delta0):
  1013	            return 0.0
  1014	        if np.sign(delta0) != np.sign(delta1) and abs(slope) > abs(3.0 * delta0):
  1015	            return 3.0 * delta0
  1016	        return slope
  1017	
  1018	    d[0] = endpoint_slope(h[0], h[1], delta[0], delta[1])
  1019	    d[-1] = endpoint_slope(h[-1], h[-2], delta[-1], delta[-2])
  1020	
  1021	    for k in range(1, n - 1):
  1022	        if delta[k - 1] == 0.0 or delta[k] == 0.0 or np.sign(delta[k - 1]) != np.sign(delta[k]):
  1023	            d[k] = 0.0
  1024	        else:
  1025	            w1 = 2.0 * h[k] + h[k - 1]
  1026	            w2 = h[k] + 2.0 * h[k - 1]
  1027	            d[k] = (w1 + w2) / (w1 / delta[k - 1] + w2 / delta[k])
  1028	
  1029	    x_dense_parts = []
  1030	    y_dense_parts = []
  1031	    for i in range(n - 1):
  1032	        t = np.linspace(0.0, 1.0, samples_per_segment, endpoint=False)
  1033	        hi = h[i]
  1034	        x_seg = x[i] + t * hi
  1035	        h00 = 2.0 * t**3 - 3.0 * t**2 + 1.0
  1036	        h10 = t**3 - 2.0 * t**2 + t
  1037	        h01 = -2.0 * t**3 + 3.0 * t**2
  1038	        h11 = t**3 - t**2
  1039	        y_seg = h00 * y[i] + h10 * hi * d[i] + h01 * y[i + 1] + h11 * hi * d[i + 1]
  1040	        x_dense_parts.append(x_seg)
  1041	        y_dense_parts.append(y_seg)
  1042	
  1043	    x_dense_parts.append(np.array([x[-1]]))
  1044	    y_dense_parts.append(np.array([y[-1]]))
  1045	    return np.concatenate(x_dense_parts), np.concatenate(y_dense_parts)
  1046	
  1047	
  1048	def plot_rdf(manifest, rahman_points, out_name=FIG8_RDF_PNG):
  1049	    os.makedirs(PLOT_DIR, exist_ok=True)
  1050	
  1051	    gr_path = nested_get(manifest, "lj_rdf.verlet_long")
  1052	    if not gr_path or not os.path.exists(gr_path):
  1053	        print("No RDF data found at manifest key lj_rdf.verlet_long. Skipping RDF plot.")
  1054	        return None
  1055	
  1056	    data = load_csv(gr_path)
  1057	    if data is None or len(data) == 0:
  1058	        print("RDF CSV is empty. Skipping RDF plot.")
  1059	        return None
  1060	
  1061	    names = set(data.dtype.names or [])
  1062	    if "r_sigma" not in names or "gr" not in names:
  1063	        print("RDF CSV missing r_sigma/gr columns. Skipping RDF plot.")
  1064	        return None
  1065	    gr_meta_typed = typed_meta(parse_csv_metadata(gr_path))
  1066	    run_identifier = run_identifier_from_path(gr_path)
  1067	
  1068	    r_sigma = finite_or_nan(np.asarray(data["r_sigma"], dtype=float))
  1069	    gr = finite_or_nan(np.asarray(data["gr"], dtype=float))
  1070	
  1071	    rahman_r_sigma = np.array([p["r_over_sigma"] for p in rahman_points], dtype=float)
  1072	    rahman_r_angstrom = np.array([p["r_angstrom"] for p in rahman_points], dtype=float)
  1073	    rahman_g = np.array([p["g_value"] for p in rahman_points], dtype=float)
  1074	    rahman_types = [p["point_type"] for p in rahman_points]
  1075	    paper_mask = np.array([pt == "paper_anchored" for pt in rahman_types], dtype=bool)
  1076	    shape_mask = ~paper_mask
  1077	    paper_points = [p for p in rahman_points if p["point_type"] == "paper_anchored"]
  1078	    rahman_guide_r, rahman_guide_g = smooth_curve_pchip(rahman_r_sigma, rahman_g, samples_per_segment=40)
  1079	
  1080	    fig, ax = plt.subplots(figsize=(8.4, 5.1), constrained_layout=True)
  1081	    ax.plot(r_sigma, gr, color="k", linewidth=2.2, zorder=4, label="Present work (Velocity-Verlet, NVE)")
  1082	    ax.plot(
  1083	        rahman_guide_r,
  1084	        rahman_guide_g,
  1085	        color=COLOR_EULER,
  1086	        linestyle=(0, (4, 3)),
  1087	        linewidth=1.6,
  1088	        alpha=0.72,
  1089	        zorder=5,
  1090	        label="Rahman guide (derived manual anchors)",
  1091	    )
  1092	    ax.scatter(
  1093	        rahman_r_sigma[paper_mask],
  1094	        rahman_g[paper_mask],
  1095	        s=42,
  1096	        marker="X",
  1097	        color=COLOR_EULER,
  1098	        edgecolors="white",
  1099	        linewidths=0.9,
  1100	        zorder=7,
  1101	        label="Rahman paper-anchored X points",
  1102	    )
  1103	    paper_annotation_offsets = [(22, -4), (22, 0), (18, 2)]
  1104	    annotation_fontsize = plt.rcParams.get("legend.fontsize", 10)
  1105	    for idx, point in enumerate(paper_points):
  1106	        dx, dy = paper_annotation_offsets[idx] if idx < len(paper_annotation_offsets) else (24, 8)
  1107	        anchor_x = float(point["r_over_sigma"])
  1108	        anchor_y = float(point["g_value"])
  1109	        label = (
  1110	            f"r={point['r_angstrom']:.1f} Å (r/σ={anchor_x:.3f})\n"
  1111	            f"g(r)≈{anchor_y:.2f}"
  1112	        )
  1113	        ax.annotate(
  1114	            label,
  1115	            xy=(anchor_x, anchor_y),
  1116	            xytext=(dx, dy),
  1117	            textcoords="offset points",
  1118	            fontsize=annotation_fontsize,
  1119	            color="black",
  1120	            ha="left",
  1121	            va="bottom",
  1122	            arrowprops={
  1123	                "arrowstyle": "->",
  1124	                "color": "black",
  1125	                "lw": 0.9,
  1126	                "shrinkA": 2,
  1127	                "shrinkB": 9,
  1128	                "alpha": 0.9,
  1129	            },
  1130	            bbox={"facecolor": "white", "alpha": 0.78, "edgecolor": "none", "pad": 1.3},
  1131	            zorder=5,
  1132	        )
  1133	    ax.axhline(y=1.0, color=COLOR_REFERENCE, linestyle=(0, (3, 3)), linewidth=1.0, alpha=0.65, label="g(r) = 1")
  1134	
  1135	    ax.set_title("Argon RDF Comparison: Present Work vs Rahman (1964)")
  1136	    ax.set_xlabel(r"Distance $r/\sigma$")
  1137	    ax.set_ylabel("g(r)")
  1138	    finite_r = r_sigma[np.isfinite(r_sigma)]
  1139	    xmax = np.nanmax(np.concatenate([finite_r, rahman_r_sigma])) if finite_r.size else np.max(rahman_r_sigma)
  1140	    ax.set_xlim(0.0, max(3.6, 1.03 * float(xmax)))
  1141	    ax.set_ylim(bottom=0.0)
  1142	    secax = ax.secondary_xaxis(
  1143	        "top",
  1144	        functions=(lambda x: x * SIGMA_ANGSTROM, lambda x: x / SIGMA_ANGSTROM),
  1145	    )
  1146	    secax.set_xlabel("Distance r (Å)")
  1147	    apply_major_grid(ax)
  1148	    disable_offset_text(ax)
  1149	    ax.legend(loc="upper right")
  1150	
  1151	    out_path = f"{PLOT_DIR}/{out_name}"
  1152	    save_figure(fig, out_path)
  1153	    plt.close(fig)
  1154	    print(f"Saved {out_path}")
  1155	
  1156	    finite_mask = np.isfinite(r_sigma) & np.isfinite(gr)
  1157	    r_plot = r_sigma[finite_mask]
  1158	    g_plot = gr[finite_mask]
  1159	
  1160	    first_peak_r, first_peak_g = extract_rdf_feature(r_plot, g_plot, 0.95, 1.30, mode="max")
  1161	    first_min_r, first_min_g = extract_rdf_feature(r_plot, g_plot, 1.30, 1.80, mode="min")
  1162	    second_peak_r, second_peak_g = extract_rdf_feature(r_plot, g_plot, 1.80, 2.40, mode="max")
  1163	    tail_mask = r_plot >= 4.0
  1164	    tail_mean = float(np.nanmean(g_plot[tail_mask])) if np.any(tail_mask) else None
  1165	
  1166	    write_plot_metadata(
  1167	        out_name,
  1168	        "results2",
  1169	        {
  1170	            "figure_number": 8,
  1171	            "panels": ["a)"],
  1172	            "purpose": (
  1173	                "Core brief-facing structural evidence: compare present-work Argon RDF against "
  1174	                "a transparent manually extracted Rahman (1964) Fig. 2 anchor guide."
  1175	            ),
  1176	            "intended_claim": (
  1177	                "The present Velocity-Verlet RDF reproduces liquid-argon shell structure "
  1178	                "(first peak, first minimum, second shell, long-range trend) with qualitative/"
  1179	                "semi-quantitative agreement to Rahman (1964), while peak heights are somewhat reduced."
  1180	            ),
  1181	            "audience_tier": "main-report-core",
  1182	            "source_data_files": unique_preserve_order(
  1183	                [
  1184	                    gr_path,
  1185	                    nested_get(manifest, "lj_rdf.verlet_long_energy", ""),
  1186	                    RAHMAN_OUT_FILE if os.path.exists(RAHMAN_OUT_FILE) else RAHMAN_SOURCE_FILE,
  1187	                ]
  1188	            ),
  1189	            "source_manifest_keys": ["lj_rdf.verlet_long", "lj_rdf.verlet_long_energy"],
  1190	            "simulation_run_identifiers": [run_identifier] if run_identifier else [],
  1191	            "key_parameters": {
  1192	                "present_work_series": extract_series_parameters(gr_meta_typed),
  1193	                "distance_units": {
  1194	                    "main_axis": "r/sigma",
  1195	                    "secondary_axis": "angstrom",
  1196	                    "sigma_angstrom": SIGMA_ANGSTROM,
  1197	                },
  1198	                "reference_dataset": {
  1199	                    "source_file": RAHMAN_OUT_FILE if os.path.exists(RAHMAN_OUT_FILE) else RAHMAN_SOURCE_FILE,
  1200	                    "model": "two-tier manual anchor set (paper_anchored + shape_anchor)",
  1201	                    "paper_anchored_x_angstrom": [3.7, 7.0, 10.4],
  1202	                    "paper_sigma_angstrom": SIGMA_ANGSTROM,
  1203	                    "n_points_total": len(rahman_points),
  1204	                    "n_points_paper_anchored": int(np.count_nonzero(paper_mask)),
  1205	                    "n_points_shape_anchor": int(np.count_nonzero(shape_mask)),
  1206	                },
  1207	            },
  1208	            "fit_or_truncation": {
  1209	                "reference_guide": "shape-preserving cubic dashed guide through manual anchor points",
  1210	                "present_work_truncation": "none",
  1211	            },
  1212	            "key_quantitative_summary": {
  1213	                "present_work_first_peak_r_over_sigma": first_peak_r,
  1214	                "present_work_first_peak_g": first_peak_g,
  1215	                "present_work_first_minimum_r_over_sigma": first_min_r,
  1216	                "present_work_first_minimum_g": first_min_g,
  1217	                "present_work_second_peak_r_over_sigma": second_peak_r,
  1218	                "present_work_second_peak_g": second_peak_g,
  1219	                "present_work_long_range_mean_g_for_r_over_sigma_ge_4": tail_mean,
  1220	                "rahman_anchor_points": rahman_points,
  1221	            },
  1222	            "caveats": [
  1223	                "Rahman comparison uses a manually extracted approximate reference guide from printed Fig. 2.",
  1224	                "Sigma = 3.4 Å is paper-supported; x-positions 3.7 Å, 7.0 Å, and 10.4 Å are paper-anchored figure annotations.",
  1225	                "All Rahman g(r) values and all non-anchored x-values are approximate manual reads from the printed plot.",
  1226	                "No error bars are shown; comparison is qualitative/semi-quantitative rather than exact.",
  1227	            ],
  1228	            "missing_provenance": [],
  1229	        },
  1230	    )
```

## Results 2 Quantitative Summary Table Generation

Source: `scripts/plot_lj.py:1280-1355`
```python
  1280	def write_results2_quantitative_summary(energy_brief_summary, temp_brief_summary, rdf_summary):
  1281	    os.makedirs(SUMMARY_DIR, exist_ok=True)
  1282	
  1283	    energy_by_int = integrator_map(energy_brief_summary or {})
  1284	    temp_by_int = integrator_map(temp_brief_summary or {})
  1285	
  1286	    rows_a = []
  1287	    for integrator, label in [("verlet", "Velocity-Verlet"), ("euler", "Euler")]:
  1288	        e_row = energy_by_int.get(integrator, {})
  1289	        t_row = temp_by_int.get(integrator, {})
  1290	        prod_steps = (
  1291	            (temp_brief_summary or {}).get("series_parameters", {}).get(integrator, {}).get("production_steps")
  1292	        )
  1293	        rows_a.append(
  1294	            {
  1295	                "Integrator": label,
  1296	                "Production steps": prod_steps if prod_steps is not None else "n/a",
  1297	                "Mean T [K]": format_float(t_row.get("mean_temperature_k"), 2),
  1298	                "Std T [K]": format_float(t_row.get("std_temperature_k"), 2),
  1299	                "Max |ΔE/E0| [%]": format_float(e_row.get("max_abs_relative_energy_deviation_percent"), 3),
  1300	                "Mean |ΔE/E0| [%]": format_float(e_row.get("mean_abs_relative_energy_deviation_percent"), 3),
  1301	                "Comment": (
  1302	                    "Bounded drift; near target state."
  1303	                    if integrator == "verlet"
  1304	                    else "Strong drift/heating over required run; not a stable NVE trajectory."
  1305	                ),
  1306	            }
  1307	        )
  1308	
  1309	    present_features = (rdf_summary or {}).get("present_features", {})
  1310	    rahman_features = (rdf_summary or {}).get("rahman_features", {})
  1311	    rows_b = []
  1312	    feature_rows = [
  1313	        ("first_peak", "First peak", "Broadly correct location; present peak height is lower."),
  1314	        ("first_minimum", "First minimum", "Minimum position and depth are broadly consistent."),
  1315	        ("second_peak", "Second peak", "Second-shell position is consistent; present peak is lower."),
  1316	        ("tail", "Tail", "Long-range trend returns toward g(r)=1."),
  1317	    ]
  1318	    for key, label, comment in feature_rows:
  1319	        present = present_features.get(key, {})
  1320	        rahman = rahman_features.get(key, None)
  1321	        if rahman:
  1322	            provenance = (
  1323	                "paper_anchored x (y approx.)"
  1324	                if rahman.get("point_type") == "paper_anchored"
  1325	                else "shape_anchor (manual approx.)"
  1326	            )
  1327	            rahman_r = format_float(rahman.get("r_over_sigma"), 3)
  1328	            rahman_g = format_float(rahman.get("g_value"), 3)
  1329	        else:
  1330	            provenance = "n/a"
  1331	            rahman_r = "n/a"
  1332	            rahman_g = "n/a"
  1333	
  1334	        rows_b.append(
  1335	            {
  1336	                "Feature": label,
  1337	                "Present work r/sigma": format_float(present.get("r_over_sigma"), 3),
  1338	                "Present work g(r)": format_float(present.get("g_value"), 3),
  1339	                "Rahman reference r/sigma": rahman_r,
  1340	                "Rahman reference g(r)": rahman_g,
  1341	                "Reference provenance": provenance,
  1342	                "Comment": comment,
  1343	            }
  1344	        )
  1345	
  1346	    md_lines = [
  1347	        "# Results 2 Quantitative Summary Table",
  1348	        "",
  1349	        "## Section A: Required 100-step production run",
  1350	        "",
  1351	        "| Integrator | Production steps | Mean T [K] | Std T [K] | Max |ΔE/E0| [%] | Mean |ΔE/E0| [%] | Comment |",
  1352	        "|---|---:|---:|---:|---:|---:|---|",
  1353	    ]
  1354	    for row in rows_a:
  1355	        md_lines.append(
```

## Results 3 Strong Scaling Derivations (Speedup, Efficiency, Amdahl Fit)

Source: `scripts/plot_scaling.py:140-255`
```python
   140	def plot_strong_scaling():
   141	    """Plot speedup, efficiency, and critical-path comm breakdown."""
   142	    os.makedirs(PLOT_DIR, exist_ok=True)
   143	
   144	    manifest = load_manifest()
   145	    data, strong_path, used_fallback = load_scaling_csv(manifest, "strong")
   146	    if data is None:
   147	        print("Warning: scaling/strong not found in manifest. Skipping strong scaling.")
   148	        return
   149	
   150	    names = getattr(getattr(data, "dtype", None), "names", ()) or ()
   151	    has_n_column = "N" in names
   152	
   153	    P = data['P'].astype(int)
   154	    wall = data['wall_s']
   155	    comm_col = "comm_max_s" if "comm_max_s" in names else "comm_s"
   156	    comm_max = data[comm_col]
   157	    compute_overhead = np.maximum(wall - comm_max, 0.0)
   158	    # Some exported strong-scaling tables omit N; Results 3 strong scaling uses fixed N=2048.
   159	    N_values = data["N"].astype(int) if has_n_column else np.full(len(P), 2048, dtype=int)
   160	
   161	    t1 = wall[0]
   162	    speedup = t1 / wall
   163	    efficiency = speedup / P
   164	
   165	    # Fit Amdahl's Law using pure NumPy two-pass grid search
   166	    def fit_amdahl(P_arr, S_obs):
   167	        """Fit Amdahl serial fraction f by minimising SSE in S-space.
   168	        Two-pass grid search: coarse (1e-3 resolution) then refined (1e-5).
   169	        Uses pure NumPy — no SciPy dependency, for cluster portability."""
   170	        best_f, best_sse = 0.0, 1e30
   171	        # Coarse pass
   172	        for f_trial in np.linspace(0.001, 0.999, 1000):
   173	            S_model = 1.0 / (f_trial + (1.0 - f_trial) / P_arr)
   174	            sse = np.sum((S_obs - S_model) ** 2)
   175	            if sse < best_sse:
   176	                best_f, best_sse = f_trial, sse
   177	        # Refined pass around coarse optimum
   178	        lo = max(0.0001, best_f - 0.002)
   179	        hi = min(0.9999, best_f + 0.002)
   180	        for f_trial in np.linspace(lo, hi, 10000):
   181	            S_model = 1.0 / (f_trial + (1.0 - f_trial) / P_arr)
   182	            sse = np.sum((S_obs - S_model) ** 2)
   183	            if sse < best_sse:
   184	                best_f, best_sse = f_trial, sse
   185	        return best_f
   186	
   187	    P_data = P[P > 1].astype(float)
   188	    S_data = speedup[P > 1]
   189	    f_fit = fit_amdahl(P_data, S_data) if len(P_data) > 0 else None
   190	
   191	    if f_fit is not None:
   192	        P_fit = np.linspace(1, max(P) * 1.1, 100)
   193	        S_fit = amdahl(P_fit, f_fit)
   194	    
   195	    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.8), constrained_layout=True)
   196	
   197	    # --- Panel 1: Speedup ---
   198	    ax1 = axes[0]
   199	    ax1.plot(P, speedup, "o-", color=COLOR_VERLET, linewidth=2.0, markersize=6, label="Measured")
   200	    ax1.plot(P, P.astype(float), "--", color=COLOR_REFERENCE, alpha=0.9, linewidth=1.5, label="Ideal (S=P)")
   201	    if f_fit is not None:
   202	        ax1.plot(P_fit, S_fit, "-", color=COLOR_EULER, linewidth=1.6, label=f"Amdahl fit (f={f_fit:.4f})")
   203	    ax1.set_xlabel("Number of Processes P")
   204	    ax1.set_ylabel("Speedup S(P)")
   205	    ax1.set_title("Strong Scaling: Speedup")
   206	    add_panel_label(ax1, "a")
   207	    ax1.legend(loc="best")
   208	    apply_major_grid(ax1)
   209	    disable_offset_text(ax1)
   210	
   211	    # --- Panel 2: Efficiency ---
   212	    ax2 = axes[1]
   213	    ax2.plot(P, efficiency, "o-", color=COLOR_RK4, linewidth=2.0, markersize=6, label="Measured efficiency")
   214	    ax2.axhline(y=1.0, color=COLOR_REFERENCE, linestyle="--", alpha=0.9, linewidth=1.3, label="Ideal (E=1)")
   215	    ax2.set_xlabel("Number of Processes P")
   216	    ax2.set_ylabel("Efficiency E(P) = S(P)/P")
   217	    ax2.set_title("Strong Scaling: Efficiency")
   218	    add_panel_label(ax2, "b")
   219	    ax2.set_ylim(0, 1.15)
   220	    ax2.legend(loc="best")
   221	    apply_major_grid(ax2)
   222	    disable_offset_text(ax2)
   223	
   224	    # --- Panel 3: Stacked bar — Remaining runtime vs critical-path communication ---
   225	    ax3 = axes[2]
   226	    x_pos = np.arange(len(P))
   227	    bar_width = 0.6
   228	    remaining_display = np.maximum(compute_overhead, 0.0)
   229	    ax3.bar(
   230	        x_pos,
   231	        remaining_display,
   232	        bar_width,
   233	        label="Remaining runtime (wall - comm_max)",
   234	        color=COLOR_VERLET,
   235	        alpha=0.85,
   236	    )
   237	    ax3.bar(
   238	        x_pos,
   239	        comm_max,
   240	        bar_width,
   241	        bottom=remaining_display,
   242	        label="Communication (critical-path max)",
   243	        color=COLOR_EULER,
   244	        alpha=0.85,
   245	    )
   246	    ax3.set_xticks(x_pos)
   247	    ax3.set_xticklabels([str(p) for p in P])
   248	    ax3.set_xlabel("Number of Processes P")
   249	    ax3.set_ylabel("Wall Time [s]")
   250	    ax3.set_title("Critical-Path Communication vs Remaining Runtime")
   251	    add_panel_label(ax3, "c")
   252	    ax3.legend(loc="best")
   253	    apply_major_grid(ax3, axis="y")
   254	    disable_offset_text(ax3)
   255	
```

## Results 3 Size Scaling Derivations (Power-Law Fit and Communication Fraction)

Source: `scripts/plot_scaling.py:345-445`
```python
   345	def plot_size_scaling():
   346	    """Plot wall time and wall-minus-comm_max runtime vs N."""
   347	    os.makedirs(PLOT_DIR, exist_ok=True)
   348	
   349	    manifest = load_manifest()
   350	    data, size_path, used_fallback = load_scaling_csv(manifest, "size")
   351	    if data is None:
   352	        print("Warning: scaling/size not found in manifest. Skipping size scaling.")
   353	        return
   354	    names = getattr(getattr(data, "dtype", None), "names", ()) or ()
   355	    if "N" not in names:
   356	        print("Warning: scaling/size is missing N column. Skipping size scaling plot.")
   357	        return
   358	
   359	    N = data['N']
   360	    wall = data['wall_s']
   361	    comm_col = "comm_max_s" if "comm_max_s" in names else "comm_s"
   362	    comm_max = data[comm_col]
   363	    remaining_runtime = np.maximum(wall - comm_max, 1e-9)  # floor to avoid log(0)
   364	
   365	    # Fit power law to wall-minus-comm_max runtime for N >= 500
   366	    mask = N >= 500
   367	    slope_remaining, intercept_remaining = None, None
   368	    slope_wall, intercept_wall = None, None
   369	    if np.sum(mask) >= 2:
   370	        log_N = np.log10(N[mask])
   371	        log_remaining = np.log10(np.maximum(remaining_runtime[mask], 1e-10))
   372	        slope_remaining, intercept_remaining = np.polyfit(log_N, log_remaining, 1)
   373	        
   374	        log_wall = np.log10(wall[mask])
   375	        slope_wall, intercept_wall = np.polyfit(log_N, log_wall, 1)
   376	
   377	    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 4.8), constrained_layout=True)
   378	
   379	    wall_label = 'Wall time'
   380	    if slope_wall is not None:
   381	        wall_label += f' (O(N^{slope_wall:.2f}))'
   382	    ax1.loglog(N, wall, "o-", color=COLOR_VERLET, linewidth=2.0, markersize=6, label=wall_label)
   383	    
   384	    rem_label = 'Remaining runtime (wall - comm_max)'
   385	    if slope_remaining is not None:
   386	        rem_label += f' (O(N^{slope_remaining:.2f}))'
   387	    ax1.loglog(N, remaining_runtime, "^-", color=COLOR_RK4, linewidth=2.0, markersize=6, label=rem_label)
   388	
   389	    ax1.loglog(
   390	        N,
   391	        comm_max,
   392	        "s--",
   393	        color=COLOR_EULER,
   394	        linewidth=1.5,
   395	        markersize=5,
   396	        label="Comm time (max)",
   397	        alpha=0.9,
   398	    )
   399	    N_ref = np.array([min(N), max(N)])
   400	    t_ref = wall[-1] * (N_ref / N[-1]) ** 2
   401	    ax1.loglog(N_ref, t_ref, "--", color=COLOR_REFERENCE, alpha=0.9, linewidth=1.5, label=r"$\sim N^2$ reference")
   402	    ax1.set_xlabel("Number of Particles N")
   403	    ax1.set_ylabel("Time [s]")
   404	    ax1.set_title("Size Scaling (P=16)")
   405	    add_panel_label(ax1, "a")
   406	    ax1.legend(loc="best")
   407	    apply_major_grid(ax1)
   408	
   409	    comm_frac = comm_max / wall * 100
   410	    ax2.plot(N, comm_frac, "o-", color=COLOR_EULER, linewidth=2.0, markersize=6)
   411	    ax2.set_xlabel("Number of Particles N")
   412	    ax2.set_ylabel("Communication Fraction [%]")
   413	    ax2.set_title("Communication Overhead vs Problem Size")
   414	    add_panel_label(ax2, "b")
   415	    ax2.set_ylim(0, 100)
   416	    apply_major_grid(ax2)
   417	    ax2.axhline(y=50, color=COLOR_REFERENCE, linestyle="--", linewidth=1.2, label="50% reference")
   418	    ax2.legend(loc="best")
   419	    disable_offset_text(ax2)
   420	
   421	    save_figure(fig, f"{PLOT_DIR}/{FIG9_AB_PNG}")
   422	    plt.close()
   423	    print(f"Saved {PLOT_DIR}/{FIG9_AB_PNG}")
   424	
   425	    scaling_meta_path = "out/scaling_meta.txt"
   426	    source_data_files = [size_path]
   427	    if os.path.exists(scaling_meta_path):
   428	        source_data_files.append(scaling_meta_path)
   429	
   430	    missing_provenance = [
   431	        "Raw per-repetition timing samples are not retained in manifest-linked files; only medians are available in scaling_size.csv.",
   432	        "Timing step count and replication count are configured in scripts/run_all_data.sh but not encoded in scaling_size.csv.",
   433	    ]
   434	    if used_fallback:
   435	        missing_provenance.append("CSV header provenance missing; file required fallback parsing.")
   436	    if not os.path.exists(scaling_meta_path):
   437	        missing_provenance.append("Hardware/environment snapshot out/scaling_meta.txt was not found.")
   438	
   439	    comm_frac_min = float(np.nanmin(comm_frac)) if comm_frac.size else None
   440	    comm_frac_max = float(np.nanmax(comm_frac)) if comm_frac.size else None
   441	    rows = []
   442	    for i in range(len(N)):
   443	        rows.append(
   444	            {
   445	                "N": int(N[i]),
```

## Diagnostics / Warnings (Bundle Generator)

- Status: confirmed
- No bundle-generation warnings were emitted.

## Potentially Stale or Informational Items (Bundle View)

- informational: Long trajectory files are intentionally truncated (head 10 + tail 5) for context size control.
- informational: Read `ai/results.md` for interpreted conclusions and confidence statements.
- informational: Read `ai/audit_output.md` for executable build/test/smoke traces.

