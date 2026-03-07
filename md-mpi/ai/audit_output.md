# Audit Output — WA2 MPI MD Solver

## Executive Summary

| Field | Value |
|---|---|
| Purpose | Executable project-wide audit trace: build/tests/smoke runs and raw code/context evidence. |
| Generation timestamp (UTC) | 2026-03-07T18:15:41Z |
| Git commit | e535aaf9e86dfa3549c06a6d71e9792912fca492 |
| Git working tree | dirty (5 changed paths) |
| Generation succeeded | yes |
| Generation status label | confirmed |
| Generation note | Audit generation completed. |

### Top Important Current Facts

- Manifest-linked artifacts found: 44/44 paths currently exist.
- Core final figures present: 9/9 required figure files.
- Results 2 brief temperature single-number contrast: Verlet mean T=94.42 K (Δ=+0.02 K), Euler mean T=185.27 K (Δ=+90.87 K).
- Results 2 brief energy drift single-number contrast: Verlet max |ΔE/E0|=0.082%, Euler max |ΔE/E0|=127.587%.
- Results 1 endpoint convergence slopes: Euler 1.05, Verlet 2.00, RK4 3.94.
- Results 3 strong scaling: max measured speedup 14.62x; fitted Amdahl serial fraction f=0.0396.

## How to Read This File

- Authoritative for: Build/test execution traces and raw repository state at generation time.
- Less authoritative for: Narrative interpretation of scientific conclusions across all figures.
- Companion files to read with this one: `ai/results.md`, `ai/results_bundle.md`.

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
- Results 3 strong scaling: max measured speedup 14.62x; fitted Amdahl serial fraction f=0.0396.

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
| At the required run length, Velocity-Verlet gives a physically meaningful bounded NVE trajectory in total energy; Forward Euler shows strong total-energy drift and is unreliable. | `out/plots/results2_lj_brief_energy_100step_production.png`; `out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260306_163529/lj_verlet.csv`; `out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260306_163529/lj_euler.csv` | high | Relative drift is computed from total energy with E0 taken at the first finite production frame. |
| Velocity-Verlet remains close to the target state while Forward Euler heats strongly over the same required window. | `out/plots/results2_lj_brief_temperature_100step_production.png`; `out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260306_163529/lj_verlet.csv`; `out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260306_163529/lj_euler.csv` | high | Temperature is shown only for finite values; divergent tails are omitted. |
| The present Velocity-Verlet RDF reproduces liquid-argon shell structure (first peak, first minimum, second shell, long-range trend) with qualitative/semi-quantitative agreement to Rahman (1964), while peak heights are somewhat reduced. | `out/plots/results2_lj_rdf_comparison_rahman1964.png`; `out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260306_163529/gr.csv`; `out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260306_163529/lj_verlet.csv`; `out/summary/results2/rahman1964_fig2_manual_anchors.csv` | high | Rahman comparison uses a manually extracted approximate reference guide from printed Fig. 2. |
| The MPI implementation achieves substantial strong-scaling gains with non-zero communication overhead; Amdahl fit quantifies residual serial fraction. | `out/plots/results3_strong_scaling_speedup_efficiency_breakdown.png`; `out/scaling_strong.csv`; `out/scaling_meta.txt` | medium | Strong-scaling data are aggregated medians, not raw replicate traces. |
| Runtime grows approximately as a power law near O(N^2) while communication fraction changes with size at fixed P=16. | `out/plots/results3_problem_size_scaling_fixed_p16.png`; `out/scaling_size.csv`; `out/scaling_meta.txt` | medium | Power-law exponents depend on the chosen fit domain (here N >= 500). |
| Shows position and velocity trajectories at dt=0.01 for Euler, Velocity-Verlet, RK4 versus exact. | `out/plots/results1_ho_figure1_trajectories_dt0p01.png` | medium | No major caveat recorded in metadata. |
| Shows phase-space geometry at dt=0.01 and qualitative orbit preservation differences. | `out/plots/results1_ho_figure2_phase_space_dt0p01.png` | medium | No major caveat recorded in metadata. |
| Supporting diagnostic: Euler shows strong drift, Velocity-Verlet bounded oscillatory error, RK4 tiny drift on this interval. | `out/plots/results1_ho_figure5_energy_diagnostic.png` | medium | No major caveat recorded in metadata. |

## Freshness / Staleness Metadata

### Source files used to generate this file
| Source file | Found | Last modified (UTC) | Status |
|---|---|---|---|
| ai/audit.sh | yes | 2026-03-07T17:11:19Z | confirmed |
| ai/context_report.py | yes | 2026-03-07T17:15:25Z | confirmed |
| Makefile | yes | 2026-03-05T11:10:52Z | confirmed |
| tests/test_runner.cpp | yes | 2026-03-02T17:08:54Z | confirmed |
| src/main.cpp | yes | 2026-03-06T12:35:38Z | confirmed |
| out/manifest.json | yes | 2026-03-07T17:45:00Z | confirmed |

### Expected file checks
| Path | Expectation | Role | Status |
|---|---|---|---|
| out/manifest.json | required | project manifest | confirmed |
| Makefile | required | build definition | confirmed |
| src/main.cpp | required | core solver source | confirmed |
| tests/test_runner.cpp | required | unit-test entry | confirmed |
| scripts/plot_ho.py | required | results generator | confirmed |
| scripts/plot_lj.py | required | results generator | confirmed |
| scripts/plot_scaling.py | required | results generator | confirmed |

### Output currency relative to current repo evidence
| Context file | Last modified (UTC) | Latest evidence mtime (UTC) | Status | Note |
|---|---|---|---|---|
| ai/audit_output.md | 2026-03-07T18:15:41Z | 2026-03-07T18:15:16Z | confirmed | appears current (in-progress generation timestamp) |
| ai/results.md | 2026-03-07T17:48:10Z | 2026-03-07T18:15:16Z | potential issue | older than latest source/evidence; consider regeneration |
| ai/results_bundle.md | 2026-03-07T17:48:10Z | 2026-03-07T18:15:16Z | potential issue | older than latest source/evidence; consider regeneration |

## Diagnostics / Warnings

- [confirmed] Required artifacts for this context view were found.
- [potential issue] Context outputs older than latest repo evidence: `ai/results.md`, `ai/results_bundle.md`

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

## Detailed Audit Evidence (Raw and Verbose)

## 1. Metadata

| Field | Value |
|-------|-------|
| Timestamp (UTC) | 2026-03-07T18:15:34Z |
| Git commit | e535aaf9e86dfa3549c06a6d71e9792912fca492 |
| Hostname | MacBook-Pro-434.local |
| uname -a | Darwin MacBook-Pro-434.local 24.6.0 Darwin Kernel Version 24.6.0: Mon Jul 14 11:30:29 PDT 2025; root:xnu-11417.140.69~1/RELEASE_ARM64_T6000 arm64 |
| Compiler | Apple clang version 17.0.0 (clang-1700.0.13.5) |
| MPI runtime | mpirun (Open MPI) 5.0.8 |
| Working directory | /Users/felix/A2_MPhil/md-mpi |

## 2. Repository Tree

### Source tree (excluding out/ and .git/)
```
./.clang-format
./.gitignore
./Makefile
./README.md
./ai/__pycache__/analyse_results.cpython-311.pyc
./ai/__pycache__/analyse_results.cpython-313.pyc
./ai/analyse_results.py
./ai/archive/claude.md
./ai/archive/code.md
./ai/archive/constraints.md
./ai/archive/current_code.md
./ai/archive/task_overview.md
./ai/audit.sh
./ai/audit_output.md
./ai/audit_output.tmp.CQCVD7
./ai/audit_preface.tmp.cb58iE
./ai/context_report.py
./ai/generate_all_context.sh
./ai/make_results.sh
./ai/pack_context.sh
./ai/pack_results.sh
./ai/results.md
./ai/results_bundle.md
./include/md/constants.hpp
./include/md/integrators.hpp
./include/md/mic.hpp
./include/md/mpi_context.hpp
./include/md/observables.hpp
./include/md/params.hpp
./include/md/potentials.hpp
./include/md/rng.hpp
./include/md/system.hpp
./md_solver
./scripts/__pycache__/plot_lj.cpython-311.pyc
./scripts/__pycache__/plot_lj.cpython-313.pyc
./scripts/__pycache__/plot_scaling.cpython-313.pyc
./scripts/__pycache__/plot_style.cpython-311.pyc
./scripts/__pycache__/plot_style.cpython-313.pyc
./scripts/__pycache__/validate_manifest.cpython-311.pyc
./scripts/append_manifest.py
./scripts/check_gr_tolerance.py
./scripts/check_tolerance.py
./scripts/data/rahman1964_fig2_manual_anchors.csv
./scripts/make_results.sh
./scripts/plot_ho.py
./scripts/plot_lj.py
./scripts/plot_scaling.py
./scripts/plot_style.py
./scripts/run_all_data.sh
./scripts/run_results.sh
./scripts/run_scaling.sh
./scripts/validate_manifest.py
./src/main.cpp
./src/observables.cpp
./src/potentials/harmonic.cpp
./src/potentials/lennard_jones.cpp
./test_runner
./tests/test_force.cpp
./tests/test_mic.cpp
./tests/test_runner.cpp
```

### out/plots/
```
total 6360
drwx------  13 felix  staff     416 Mar  7 16:20 .
drwx------  20 felix  staff     640 Mar  6 16:35 ..
drwxr-xr-x  12 felix  staff     384 Mar  7 16:21 metadata
-rw-r--r--   1 felix  staff  352240 Mar  7 14:52 results1_ho_figure1_trajectories_dt0p01.png
-rw-r--r--   1 felix  staff  221196 Mar  7 14:52 results1_ho_figure2_phase_space_dt0p01.png
-rw-r--r--   1 felix  staff  683110 Mar  7 14:52 results1_ho_figure3_small_vs_large_dt.png
-rw-r--r--   1 felix  staff  366090 Mar  7 14:52 results1_ho_figure4_convergence_combined.png
-rw-r--r--   1 felix  staff  216304 Mar  7 14:52 results1_ho_figure5_energy_diagnostic.png
-rw-r--r--@  1 felix  staff  292464 Mar  7 18:15 results2_lj_brief_energy_100step_production.png
-rw-r--r--   1 felix  staff  144510 Mar  7 17:45 results2_lj_brief_temperature_100step_production.png
-rw-r--r--   1 felix  staff  234926 Mar  7 17:45 results2_lj_rdf_comparison_rahman1964.png
-rw-r--r--   1 felix  staff  291528 Mar  7 15:05 results3_problem_size_scaling_fixed_p16.png
-rw-r--r--   1 felix  staff  274607 Mar  7 15:05 results3_strong_scaling_speedup_efficiency_breakdown.png
```

### out/manifest.json
```json
{
  "ho_convergence": {
    "euler_dt1_0": "out/runs/ho_N1_euler_dt1.0_20260306_163529/ho_euler.csv",
    "euler_dt0_5": "out/runs/ho_N1_euler_dt0.5_20260306_163529/ho_euler.csv",
    "euler_dt0_1": "out/runs/ho_N1_euler_dt0.1_20260306_163529/ho_euler.csv",
    "euler_dt0_05": "out/runs/ho_N1_euler_dt0.05_20260306_163529/ho_euler.csv",
    "euler_dt0_01": "out/runs/ho_N1_euler_dt0.01_20260306_163529/ho_euler.csv",
    "euler_dt0_005": "out/runs/ho_N1_euler_dt0.005_20260306_163529/ho_euler.csv",
    "euler_dt0_001": "out/runs/ho_N1_euler_dt0.001_20260306_163529/ho_euler.csv",
    "euler_dt0_0005": "out/runs/ho_N1_euler_dt0.0005_20260306_163529/ho_euler.csv",
    "verlet_dt1_0": "out/runs/ho_N1_verlet_dt1.0_20260306_163529/ho_verlet.csv",
    "verlet_dt0_5": "out/runs/ho_N1_verlet_dt0.5_20260306_163529/ho_verlet.csv",
    "verlet_dt0_1": "out/runs/ho_N1_verlet_dt0.1_20260306_163529/ho_verlet.csv",
    "verlet_dt0_05": "out/runs/ho_N1_verlet_dt0.05_20260306_163529/ho_verlet.csv",
    "verlet_dt0_01": "out/runs/ho_N1_verlet_dt0.01_20260306_163529/ho_verlet.csv",
    "verlet_dt0_005": "out/runs/ho_N1_verlet_dt0.005_20260306_163529/ho_verlet.csv",
    "verlet_dt0_001": "out/runs/ho_N1_verlet_dt0.001_20260306_163529/ho_verlet.csv",
    "verlet_dt0_0005": "out/runs/ho_N1_verlet_dt0.0005_20260306_163529/ho_verlet.csv",
    "rk4_dt1_0": "out/runs/ho_N1_rk4_dt1.0_20260306_163529/ho_rk4.csv",
    "rk4_dt0_5": "out/runs/ho_N1_rk4_dt0.5_20260306_163529/ho_rk4.csv",
    "rk4_dt0_1": "out/runs/ho_N1_rk4_dt0.1_20260306_163529/ho_rk4.csv",
    "rk4_dt0_05": "out/runs/ho_N1_rk4_dt0.05_20260306_163529/ho_rk4.csv",
    "rk4_dt0_01": "out/runs/ho_N1_rk4_dt0.01_20260306_163529/ho_rk4.csv",
    "rk4_dt0_005": "out/runs/ho_N1_rk4_dt0.005_20260306_163529/ho_rk4.csv",
    "rk4_dt0_001": "out/runs/ho_N1_rk4_dt0.001_20260306_163529/ho_rk4.csv",
    "rk4_dt0_0005": "out/runs/ho_N1_rk4_dt0.0005_20260306_163529/ho_rk4.csv"
  },
  "lj_brief": {
    "verlet": "out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260306_163529/lj_verlet.csv",
    "euler": "out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260306_163529/lj_euler.csv"
  },
  "lj_rdf": {
    "verlet_long": "out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260306_163529/gr.csv",
    "verlet_long_energy": "out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260306_163529/lj_verlet.csv"
  },
  "scaling": {
    "strong": "out/scaling_strong.csv",
    "size": "out/scaling_size.csv"
  },
  "results2_outputs": {
    "generated_utc": "2026-03-07T17:45:00Z",
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

### out/runs/ directories referenced by manifest
```
out/
out/runs/ho_N1_euler_dt0.0005_20260306_163529/
out/runs/ho_N1_euler_dt0.001_20260306_163529/
out/runs/ho_N1_euler_dt0.005_20260306_163529/
out/runs/ho_N1_euler_dt0.01_20260306_163529/
out/runs/ho_N1_euler_dt0.05_20260306_163529/
out/runs/ho_N1_euler_dt0.1_20260306_163529/
out/runs/ho_N1_euler_dt0.5_20260306_163529/
out/runs/ho_N1_euler_dt1.0_20260306_163529/
out/runs/ho_N1_rk4_dt0.0005_20260306_163529/
out/runs/ho_N1_rk4_dt0.001_20260306_163529/
out/runs/ho_N1_rk4_dt0.005_20260306_163529/
out/runs/ho_N1_rk4_dt0.01_20260306_163529/
out/runs/ho_N1_rk4_dt0.05_20260306_163529/
out/runs/ho_N1_rk4_dt0.1_20260306_163529/
out/runs/ho_N1_rk4_dt0.5_20260306_163529/
out/runs/ho_N1_rk4_dt1.0_20260306_163529/
out/runs/ho_N1_verlet_dt0.0005_20260306_163529/
out/runs/ho_N1_verlet_dt0.001_20260306_163529/
out/runs/ho_N1_verlet_dt0.005_20260306_163529/
out/runs/ho_N1_verlet_dt0.01_20260306_163529/
out/runs/ho_N1_verlet_dt0.05_20260306_163529/
out/runs/ho_N1_verlet_dt0.1_20260306_163529/
out/runs/ho_N1_verlet_dt0.5_20260306_163529/
out/runs/ho_N1_verlet_dt1.0_20260306_163529/
out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260306_163529/
out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260306_163529/
out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260306_163529/
out/summary/results2/
```

## 3. Build and Warnings

```
rm -f src/main.o src/potentials/harmonic.o src/potentials/lennard_jones.o src/observables.o tests/test_runner.o tests/test_mic.o tests/test_force.o src/potentials/lennard_jones.o src/potentials/harmonic.o src/observables.o md_solver test_runner
rm -f src/potentials/*.o tests/*.o

mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/main.o src/main.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/potentials/harmonic.o src/potentials/harmonic.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/potentials/lennard_jones.o src/potentials/lennard_jones.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/observables.o src/observables.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -o md_solver src/main.o src/potentials/harmonic.o src/potentials/lennard_jones.o src/observables.o
```

**Build status:** confirmed

### Compilation flags

From Makefile line 12:
```
CXXFLAGS  = -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic
```

Flags include: `-std=c++17 -O3 -march=native -Wall -Wextra -pedantic`

### Warning check

Re-building to capture warnings explicitly:
```
rm -f src/main.o src/potentials/harmonic.o src/potentials/lennard_jones.o src/observables.o tests/test_runner.o tests/test_mic.o tests/test_force.o src/potentials/lennard_jones.o src/potentials/harmonic.o src/observables.o md_solver test_runner
rm -f src/potentials/*.o tests/*.o
make: Nothing to be done for `all'.
```

**Warnings found:** 0
**Warning interpretation:** confirmed (no warning hits detected)

## 4. Unit Tests

```
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o tests/test_runner.o tests/test_runner.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o tests/test_mic.o tests/test_mic.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o tests/test_force.o tests/test_force.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -o test_runner tests/test_runner.o tests/test_mic.o tests/test_force.o src/potentials/lennard_jones.o src/potentials/harmonic.o src/observables.o
./test_runner
=== MD Unit Tests ===
  MIC tests: ALL PASSED
  Force/Wrapping tests: ALL PASSED
=====================
ALL TESTS PASSED
```

**Test status:** confirmed

## 5. Smoke Runs

### 5a. HO — Velocity-Verlet (N=1, 1000 steps, dt=0.01, T_final≈10)

```
[MacBook-Pro-434.local:16177] [prterun-MacBook-Pro-434-16177@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:16177] [prterun-MacBook-Pro-434-16177@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:16177] PRTE ERROR: Fatal in file oob_tcp_component.c at line 582
--------------------------------------------------------------------------
No sockets were able to be opened on the available protocols
(IPv4 and/or IPv6). Please check your network and retry.
--------------------------------------------------------------------------
[16177] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
--------------------------------------------------------------------------
```

**Output (first 6 + last 3 lines):**
```
# mode: ho, integrator: verlet, N: 1, P: 1, dt: 0.01, steps: 1000, n_steps: 1000, n_frames: 1001, step_indexing: 0..steps (includes initial frame), total_steps_executed: 1000, seed: 42, L: 10000000000, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 0, production_steps: 1000, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: false, production_nve: false, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, timestamp: 2026-03-06T12:40:19Z
step,time,x,v,E_kin,E_pot,E_total
0,0,1,0,0,3.34521325e-26,3.34521325e-26
1,0.01,0.99995,-0.00999975,3.34504599142826e-30,3.34487873703803e-26,3.34521324163718e-26
2,0.02,0.999800005,-0.019998500025,1.33788459807669e-29,3.34387533195397e-26,3.34521321655205e-26
3,0.03,0.9995500299995,-0.0299952501999975,3.00973865483582e-29,3.34220343609982e-26,3.34521317475465e-26
...
998,9.98,-0.849761496348259,0.527160745588082,9.2962958274447e-27,2.41556042593492e-26,3.34519000867939e-26
999,9.99,-0.844447400817561,0.535631790073911,9.59746413355533e-27,2.38544284238427e-26,3.3451892557398e-26
1000,10,-0.839048860546781,0.544049271380733,9.90148364197004e-27,2.35504013147503e-26,3.34518849567203e-26
```

### 5b. HO — RK4 (N=1, 1000 steps, dt=0.01, T_final≈10)

```
[MacBook-Pro-434.local:16180] [prterun-MacBook-Pro-434-16180@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:16180] [prterun-MacBook-Pro-434-16180@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:16180] PRTE ERROR: Fatal in file oob_tcp_component.c at line 582
--------------------------------------------------------------------------
[16180] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
No sockets were able to be opened on the available protocols
```

**Output (first 6 + last 3):**
```
# mode: ho, integrator: rk4, N: 1, P: 1, dt: 0.01, steps: 1000, n_steps: 1000, n_frames: 1001, step_indexing: 0..steps (includes initial frame), total_steps_executed: 1000, seed: 42, L: 10000000000, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 0, production_steps: 1000, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: false, production_nve: false, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, timestamp: 2026-03-06T12:40:19Z
step,time,x,v,E_kin,E_pot,E_total
0,0,1,0,0,3.34521325e-26,3.34521325e-26
1,0.01,0.999950000416667,-0.00999983333333333,3.34510174382089e-30,3.34487873982557e-26,3.34521324999995e-26
2,0.02,0.999800006666597,-0.0199986666916665,1.33790689791868e-29,3.34387534310199e-26,3.34521324999991e-26
3,0.03,0.999550033749042,-0.0299955001999963,3.00978882529885e-29,3.34220346117456e-26,3.34521324999986e-26
...
998,9.98,-0.84978341766768,0.527131997741721,9.29528193860932e-27,2.4156850560927e-26,3.34521324995363e-26
999,9.99,-0.844469696728789,0.535603333907579,9.59644440400895e-27,2.38556880955269e-26,3.34521324995359e-26
1000,10,-0.839071529523961,0.54402111018639,9.90045862308603e-27,2.35516738764494e-26,3.34521324995354e-26
```

### 5c. HO — Euler (N=1, 1000 steps, dt=0.01, T_final≈10)

```
[MacBook-Pro-434.local:16183] [prterun-MacBook-Pro-434-16183@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:16183] [prterun-MacBook-Pro-434-16183@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:16183] PRTE ERROR: Fatal in file oob_tcp_component.c at line 582
[16183] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
--------------------------------------------------------------------------
```

**Output (first 6 + last 3):**
```
# mode: ho, integrator: euler, N: 1, P: 1, dt: 0.01, steps: 1000, n_steps: 1000, n_frames: 1001, step_indexing: 0..steps (includes initial frame), total_steps_executed: 1000, seed: 42, L: 10000000000, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 0, production_steps: 1000, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: false, production_nve: false, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, timestamp: 2026-03-06T12:40:20Z
step,time,x,v,E_kin,E_pot,E_total
0,0,1,0,0,3.34521325e-26,3.34521325e-26
1,0.01,1,-0.01,3.34521325e-30,3.34521325e-26,3.345547771325e-26
2,0.02,0.9999,-0.02,1.3380853e-29,3.34454424080213e-26,3.34588232610213e-26
3,0.03,0.9997,-0.029999,3.01049121555021e-29,3.34320642311919e-26,3.34621691433474e-26
...
998,9.98,-0.893445456097998,0.553804667417217,1.02597559798136e-26,2.6702990249091e-26,3.69627462289046e-26
999,9.99,-0.887907409423826,0.562739121978197,1.05934647442089e-26,2.63729777593186e-26,3.69664425035275e-26
1000,10,-0.882280018204044,0.571618196072435,1.09303960503626e-26,2.60397430974153e-26,3.69701391477778e-26
```

### 5d. LJ — Velocity-Verlet (N=108, 10 steps, P=1)

```
[MacBook-Pro-434.local:16186] [prterun-MacBook-Pro-434-16186@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:16186] [prterun-MacBook-Pro-434-16186@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:16186] PRTE ERROR: Fatal in file oob_tcp_component.c at line 582
[16186] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
```

**Output:**
```
# mode: lj, integrator: verlet, N: 864, P: 1, dt: 1e-14, steps: 100, n_steps: 100, n_frames: 101, step_indexing: 0..steps (includes initial frame), total_steps_executed: 150, seed: 42, L: 3.47786e-09, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 50, production_steps: 100, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: true, production_nve: true, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, startup_temperature_before_final_rescale: 94.3304820914354, startup_temperature_after_final_rescale: 94.3999999999999, lattice: FCC, velocities: Box-Muller, timestamp: 2026-03-06T12:40:20Z
step,time,E_kin,E_pot,E_total,temperature
0,0,1.687164123192e-18,-7.47194927673328e-18,-5.78478515354128e-18,94.3999999999999
1,1e-14,1.68447578135402e-18,-7.46869101577964e-18,-5.78421523442562e-18,94.2495822273503
2,2e-14,1.68047549629073e-18,-7.46552676001374e-18,-5.785051263723e-18,94.0257587683379
3,3e-14,1.675573444974e-18,-7.46109573619852e-18,-5.78552229122452e-18,93.7514797945626
4,4e-14,1.67031939809281e-18,-7.45631122530418e-18,-5.78599182721137e-18,93.4575060081559
5,5e-14,1.66525309392628e-18,-7.4517277580709e-18,-5.78647466414463e-18,93.174036779083
6,6e-14,1.66078214268927e-18,-7.44785276849725e-18,-5.78707062580798e-18,92.9238786640711
7,7e-14,1.65716146413624e-18,-7.44493273747193e-18,-5.78777127333569e-18,92.7212949019413
8,8e-14,1.65460549217326e-18,-7.4422058796724e-18,-5.78760038749914e-18,92.5782834722954
9,9e-14,1.6534278355732e-18,-7.44166241106346e-18,-5.78823457549026e-18,92.5123913747116
10,1e-13,1.65412668053239e-18,-7.44185951670639e-18,-5.787732836174e-18,92.5514930621172
11,1.1e-13,1.65729060008612e-18,-7.44519272334869e-18,-5.78790212326257e-18,92.7285203007638
12,1.2e-13,1.6633765818926e-18,-7.45121991594431e-18,-5.78784333405171e-18,93.0690424080291
13,1.3e-13,1.67243894775827e-18,-7.46066468725163e-18,-5.78822573949337e-18,93.5760987909615
14,1.4e-13,1.68396198202923e-18,-7.47224354282029e-18,-5.78828156079106e-18,94.2208341905743
15,1.5e-13,1.69693087203493e-18,-7.48574394643748e-18,-5.78881307440254e-18,94.946467932846
16,1.6e-13,1.71004835930324e-18,-7.49863361001208e-18,-5.78858525070884e-18,95.6804159709217
17,1.7e-13,1.72204246107605e-18,-7.51038292801881e-18,-5.78834046694276e-18,96.3515084815964
18,1.8e-13,1.7319859370743e-18,-7.52014405717191e-18,-5.78815812009761e-18,96.9078646305515
19,1.9e-13,1.73943052715559e-18,-7.52748093519145e-18,-5.78805040803586e-18,97.3244034213031
20,2e-13,1.74437066635724e-18,-7.53138155080626e-18,-5.78701088444901e-18,97.6008134837422
21,2.1e-13,1.74710459181086e-18,-7.53494587371041e-18,-5.78784128189955e-18,97.7537817452611
22,2.2e-13,1.7480215327952e-18,-7.53528197899024e-18,-5.78726044619504e-18,97.8050863147046
23,2.3e-13,1.74742061897183e-18,-7.53552700056766e-18,-5.78810638159584e-18,97.7714640581936
24,2.4e-13,1.74550899555746e-18,-7.5337051750981e-18,-5.78819617954065e-18,97.6645051394755
25,2.5e-13,1.74247299270064e-18,-7.53152236931637e-18,-5.78904937661573e-18,97.494635080159
26,2.6e-13,1.73848649862318e-18,-7.52773313127077e-18,-5.78924663264759e-18,97.2715832526935
27,2.7e-13,1.73367522014907e-18,-7.52241513584086e-18,-5.78873991569179e-18,97.0023831898706
28,2.8e-13,1.72806293984258e-18,-7.51757447856569e-18,-5.78951153872311e-18,96.6883655708078
29,2.9e-13,1.72154970390465e-18,-7.51082018075638e-18,-5.78927047685173e-18,96.3239377928053
30,3e-13,1.7139722306459e-18,-7.5023855342226e-18,-5.78841330357669e-18,95.8999639388139
31,3.1e-13,1.70529887922345e-18,-7.49400830958688e-18,-5.78870943036343e-18,95.4146736442748
32,3.2e-13,1.69577237052573e-18,-7.48450826870902e-18,-5.78873589818329e-18,94.8816475985553
33,3.3e-13,1.68590120501956e-18,-7.47500978017349e-18,-5.78910857515394e-18,94.3293373573798
34,3.4e-13,1.67634845633446e-18,-7.46511942093019e-18,-5.78877096459573e-18,93.7948431351063
35,3.5e-13,1.6677929659191e-18,-7.45556989390052e-18,-5.78777692798142e-18,93.3161473851741
36,3.6e-13,1.66083877639135e-18,-7.44858603902785e-18,-5.7877472626365e-18,92.9270474260208
37,3.7e-13,1.65600850014213e-18,-7.44317686152285e-18,-5.78716836138073e-18,92.6567844020157
38,3.8e-13,1.65372773163601e-18,-7.44012414698609e-18,-5.78639641535008e-18,92.5291711224195
39,3.9e-13,1.65418403315184e-18,-7.44003268636633e-18,-5.78584865321449e-18,92.5547020488435
40,4e-13,1.65718453956044e-18,-7.44352897663574e-18,-5.7863444370753e-18,92.722586015245
41,4.1e-13,1.66213404395564e-18,-7.44737086246314e-18,-5.78523681850749e-18,92.9995200778442
42,4.2e-13,1.66814274561946e-18,-7.45348725606079e-18,-5.78534451044134e-18,93.3357182160495
43,4.3e-13,1.67431455296978e-18,-7.45888474195169e-18,-5.78457018898191e-18,93.6810424236129
44,4.4e-13,1.67999072999343e-18,-7.46513317145133e-18,-5.7851424414579e-18,93.9986351839537
45,4.5e-13,1.68470940965253e-18,-7.4695172552676e-18,-5.78480784561507e-18,94.2626541692412
46,4.6e-13,1.68806190930705e-18,-7.47309571905642e-18,-5.78503380974938e-18,94.4502328185476
47,4.7e-13,1.68958647214974e-18,-7.47469596346912e-18,-5.78510949131938e-18,94.5355349716528
48,4.8e-13,1.68887579098233e-18,-7.47510382499278e-18,-5.78622803401045e-18,94.4957710261768
49,4.9e-13,1.68583934152298e-18,-7.47178981302243e-18,-5.78595047149945e-18,94.3258759786103
50,5e-13,1.68079724462429e-18,-7.46700882633075e-18,-5.78621158170646e-18,94.0437611916173
51,5.1e-13,1.67439991753882e-18,-7.46152265511313e-18,-5.78712273757432e-18,93.6858187315051
52,5.2e-13,1.66747541438195e-18,-7.45449092240379e-18,-5.78701550802184e-18,93.2983797805322
53,5.3e-13,1.66091692597013e-18,-7.44803402430377e-18,-5.78711709833364e-18,92.9314200416633
54,5.4e-13,1.6555948873512e-18,-7.44246525474839e-18,-5.7868703673972e-18,92.6336419898891
55,5.5e-13,1.6522376336817e-18,-7.43953363575759e-18,-5.78729600207589e-18,92.4457973445201
56,5.6e-13,1.65132600997293e-18,-7.43917348238068e-18,-5.78784747240775e-18,92.3947902866264
57,5.7e-13,1.6530033651823e-18,-7.4408659264218e-18,-5.7878625612395e-18,92.4886414594838
58,5.8e-13,1.65702395432951e-18,-7.44471947643592e-18,-5.78769552210641e-18,92.7136009701083
59,5.9e-13,1.66283200787085e-18,-7.45096766852001e-18,-5.78813566064916e-18,93.0385724691851
60,6e-13,1.66972873205194e-18,-7.45769750402273e-18,-5.7879687719708e-18,93.4244571343136
61,6.1e-13,1.67705685909187e-18,-7.46449500676405e-18,-5.78743814767218e-18,93.8344795992655
62,6.2e-13,1.68429376182607e-18,-7.47118370749729e-18,-5.78688994567122e-18,94.2393978930566
63,6.3e-13,1.69109353519156e-18,-7.4785366055783e-18,-5.78744307038674e-18,94.619857978047
64,6.4e-13,1.69723908788048e-18,-7.48387031635612e-18,-5.78663122847564e-18,94.9637131880169
65,6.5e-13,1.70253846586652e-18,-7.4887765334233e-18,-5.78623806755678e-18,95.26022333484
66,6.6e-13,1.70677283533266e-18,-7.49312735702395e-18,-5.78635452169129e-18,95.497144255638
67,6.7e-13,1.70966668273834e-18,-7.49583472186753e-18,-5.78616803912919e-18,95.6590604505956
68,6.8e-13,1.71092556816934e-18,-7.49635053865602e-18,-5.78542497048668e-18,95.7294974537614
69,6.9e-13,1.71029490127496e-18,-7.49614154995616e-18,-5.7858466486812e-18,95.6942104570717
70,7e-13,1.7076202140512e-18,-7.49205691500308e-18,-5.78443670095188e-18,95.5445566857211
71,7.1e-13,1.7029018003409e-18,-7.48697009197181e-18,-5.78406829163091e-18,95.2805525807682
72,7.2e-13,1.6963457102432e-18,-7.4809445742481e-18,-5.7845988640049e-18,94.9137270320764
73,7.3e-13,1.68840858749515e-18,-7.4733641045854e-18,-5.78495551709025e-18,94.4696301139896
74,7.4e-13,1.67983089699382e-18,-7.46436962712612e-18,-5.7845387301323e-18,93.9896922275716
75,7.5e-13,1.67159821361495e-18,-7.45581419537416e-18,-5.78421598175921e-18,93.5290581373354
76,7.6e-13,1.66477640869556e-18,-7.45040119603428e-18,-5.78562478733873e-18,93.1473653455445
77,7.7e-13,1.66031096473095e-18,-7.44574710833835e-18,-5.7854361436074e-18,92.8975153727621
78,7.8e-13,1.65881830201206e-18,-7.44403863136079e-18,-5.78522032934873e-18,92.8139980914696
79,7.9e-13,1.66042409100495e-18,-7.44530837146013e-18,-5.78488428045518e-18,92.9038450001641
80,8e-13,1.6647134835938e-18,-7.45021118290105e-18,-5.78549769930724e-18,93.1438445679723
81,8.1e-13,1.67077911330439e-18,-7.45659990105184e-18,-5.78582078774745e-18,93.4832279372657
82,8.2e-13,1.67744895311606e-18,-7.46298108551396e-18,-5.7855321323979e-18,93.8564179959955
83,8.3e-13,1.68363886331392e-18,-7.46854861321558e-18,-5.78490974990166e-18,94.2027550918634
84,8.4e-13,1.6886056495076e-18,-7.47327652659135e-18,-5.78467087708375e-18,94.4806561035303
85,8.5e-13,1.69204171719358e-18,-7.47659996968837e-18,-5.78455825249479e-18,94.6729105410788
86,8.6e-13,1.69401364943217e-18,-7.47808414923524e-18,-5.78407049980307e-18,94.7832438517293
87,8.7e-13,1.69483899609822e-18,-7.47892646892905e-18,-5.78408747283083e-18,94.8294235471154
88,8.8e-13,1.6949486953557e-18,-7.47855979565366e-18,-5.78361110029796e-18,94.8355614265095
89,8.9e-13,1.69472100344872e-18,-7.47876353857899e-18,-5.78404253513026e-18,94.822821636869
90,9e-13,1.69442537753834e-18,-7.47835490946036e-18,-5.78392953192202e-18,94.8062808122054
91,9.1e-13,1.69419059567169e-18,-7.47806436382232e-18,-5.78387376815064e-18,94.7931443260111
92,9.2e-13,1.69402683593984e-18,-7.47789746893802e-18,-5.78387063299818e-18,94.7839816615887
93,9.3e-13,1.6939285024503e-18,-7.47764403876902e-18,-5.78371553631871e-18,94.7784797182479
94,9.4e-13,1.69394479660581e-18,-7.47770834591809e-18,-5.78376354931229e-18,94.7793914068374
95,9.5e-13,1.69414354335647e-18,-7.47749908245355e-18,-5.78335553909708e-18,94.7905116606434
96,9.6e-13,1.69459173731494e-18,-7.47785073190454e-18,-5.78325899458959e-18,94.8155889540131
97,9.7e-13,1.69527786433768e-18,-7.47915579047344e-18,-5.78387792613576e-18,94.8539790489993
98,9.8e-13,1.69603745977495e-18,-7.47982699115722e-18,-5.78378953138227e-18,94.8964798397003
99,9.9e-13,1.69664840466377e-18,-7.4799966425522e-18,-5.78334823788842e-18,94.9306633531548
100,1e-12,1.69688683932431e-18,-7.48014957868897e-18,-5.78326273936466e-18,94.9440042200242
```

### 5e. LJ — Euler (N=108, 10 steps, P=1)

```
[MacBook-Pro-434.local:16188] [prterun-MacBook-Pro-434-16188@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:16188] [prterun-MacBook-Pro-434-16188@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:16188] PRTE ERROR: Fatal in file oob_tcp_component.c at line 582
--------------------------------------------------------------------------
No sockets were able to be opened on the available protocols
(IPv4 and/or IPv6). Please check your network and retry.
--------------------------------------------------------------------------
[16188] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
```

**Output:**
```
# mode: lj, integrator: euler, N: 108, P: 1, dt: 1e-14, steps: 10, n_steps: 10, n_frames: 11, step_indexing: 0..steps (includes initial frame), total_steps_executed: 60, seed: 42, L: 1.73893e-09, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 50, production_steps: 10, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: true, production_nve: true, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, startup_temperature_before_final_rescale: 94.9849184843571, startup_temperature_after_final_rescale: 94.4000000000001, lattice: FCC, velocities: Box-Muller, timestamp: 2026-03-06T12:40:20Z
step,time,E_kin,E_pot,E_total,temperature
0,0,2.09184891288e-19,-9.12916763919551e-19,-7.03731872631551e-19,94.4000000000001
1,1e-14,2.11525263370756e-19,-9.10632329841394e-19,-6.99107066470638e-19,95.4561523982533
2,2e-14,2.14776832951035e-19,-9.0938833883245e-19,-6.94611505881416e-19,96.9235058313255
3,3e-14,2.18964511804124e-19,-9.08859592979484e-19,-6.89895081175361e-19,98.8133023711117
4,4e-14,2.24108503104857e-19,-9.09809852096508e-19,-6.85701348991651e-19,101.134659213852
5,5e-14,2.30011308581937e-19,-9.11507518253613e-19,-6.81496209671676e-19,103.798450243908
6,6e-14,2.36298938432358e-19,-9.13451036509845e-19,-6.77152098077487e-19,106.635903055271
7,7e-14,2.42703937969227e-19,-9.15283282486688e-19,-6.72579344517461e-19,109.526321921364
8,8e-14,2.49116447237105e-19,-9.17520494560082e-19,-6.68404047322977e-19,112.420129744484
9,9e-14,2.55437535169377e-19,-9.19786529495048e-19,-6.64348994325671e-19,115.272681365839
10,1e-13,2.61440695380733e-19,-9.2212063732577e-19,-6.60679941945037e-19,117.981760020911
```

### 5f. MPI Consistency — P=1 vs P=2 (N=108, 5 steps, Verlet)

```
[16191] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
[16192] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
MATCH
```

## 6. CLI Defaults vs. Brief Requirements

### CLI help output
```
[16194] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
```

### Comparison

| Parameter | CLI Default | Brief Requirement | Interpreted status |
|-----------|------------|-------------------|--------------------|
| N         | 864        | 864               | confirmed          |
| steps     | 100        | 100               | confirmed          |
| dt        | 1e-14      | 1e-14             | confirmed          |
| mode      | lj         | lj                | confirmed          |
| integrator| verlet     | verlet             | confirmed          |
| T_init    | 94.4 K     | 94.4 K            | confirmed          |

## 7. File Dump (Verbatim)

### `Makefile` (83 lines)

```makefile
# ──────────────────────────────────────────────────────────────────
# Makefile — WA2: MPI Parallelisation of Molecular Dynamics
# ──────────────────────────────────────────────────────────────────
# Targets:
#   make          Build the md_solver executable
#   make test     Build and run unit tests (exits non-zero on failure)
#   make clean    Remove object files and binaries
#   make dist     Create submission tarball (excludes out/, ai/, etc.)
# ──────────────────────────────────────────────────────────────────

CXX       = mpicxx
CXXFLAGS  = -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic
INCLUDES  = -Iinclude

# Source files
SRC_MAIN        = src/main.cpp
SRC_HARMONIC    = src/potentials/harmonic.cpp
SRC_LJ          = src/potentials/lennard_jones.cpp
SRC_OBSERVABLES = src/observables.cpp

SRCS = $(SRC_MAIN) $(SRC_HARMONIC) $(SRC_LJ) $(SRC_OBSERVABLES)
OBJS = $(SRCS:.cpp=.o)

# Test files
TEST_SRCS = tests/test_runner.cpp tests/test_mic.cpp tests/test_force.cpp
TEST_OBJS = $(TEST_SRCS:.cpp=.o)
# Tests also need the LJ potential (for test_force.cpp)
TEST_DEPS = src/potentials/lennard_jones.o src/potentials/harmonic.o src/observables.o

TARGET    = md_solver
TEST_BIN  = test_runner

TARBALL   = candidate_fb638_wa2.tar.gz

# ──────────────────────────────────────────────────────────────────
# Default target
# ──────────────────────────────────────────────────────────────────
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ $^

# ──────────────────────────────────────────────────────────────────
# Compilation rules
# ──────────────────────────────────────────────────────────────────
%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c -o $@ $<

# ──────────────────────────────────────────────────────────────────
# Unit tests (homebrew, no third-party libraries)
# ──────────────────────────────────────────────────────────────────
test: $(TEST_BIN)
	./$(TEST_BIN)

$(TEST_BIN): $(TEST_OBJS) $(TEST_DEPS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ $^

# ──────────────────────────────────────────────────────────────────
# Clean
# ──────────────────────────────────────────────────────────────────
clean:
	rm -f $(OBJS) $(TEST_OBJS) $(TEST_DEPS) $(TARGET) $(TEST_BIN)
	rm -f src/potentials/*.o tests/*.o

# ──────────────────────────────────────────────────────────────────
# Submission tarball
# ──────────────────────────────────────────────────────────────────
dist: clean
	tar -czvf $(TARBALL) \
		include/ src/ tests/ scripts/ \
		Makefile README.md .clang-format
	@echo ""
	@echo "Created $(TARBALL)"
	@echo "Contents:"
	@tar -tzvf $(TARBALL) | head -30

# ──────────────────────────────────────────────────────────────────
# Create output directory
# ──────────────────────────────────────────────────────────────────
out:
	mkdir -p out

.PHONY: all clean test dist
```

### `README.md` (95 lines)

```markdown
# WA2: MPI Parallelisation of Molecular Dynamics

## Dependencies

- C++17 compiler with MPI (tested with OpenMPI 4.x + GCC 8+)
- Python 3 with matplotlib, numpy (for plotting scripts)

## Build

```bash
make            # builds md_solver
make test       # runs unit tests (exits non-zero on failure)
```

All plots in the report are generated from `out/manifest.json` to guarantee provenance.


## Run Examples

### Harmonic Oscillator (Results 1)

```bash
# Single integrator run
mpirun -np 1 ./md_solver --mode ho --integrator verlet --dt 0.01 --steps 1000 --N 1

# Euler
mpirun -np 1 ./md_solver --mode ho --integrator euler --dt 0.01 --steps 1000 --N 1

# RK4
mpirun -np 1 ./md_solver --mode ho --integrator rk4 --dt 0.01 --steps 1000 --N 1
```

### Lennard-Jones Argon (Results 2)

```bash
# Brief-required run:
# startup/equilibration prepares the state, then production is a clean 100-step NVE trajectory.
# Output CSV stores the production trajectory only (step 0 is the production initial frame).
mkdir -p out
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --dt 1e-14 \
  --target-temperature 94.4 --equilibration-steps 50 --production-steps 100 \
  --final-rescale-before-production

# Brief-required Euler comparison
mpirun -np 4 ./md_solver --mode lj --integrator euler --N 864 --dt 1e-14 \
  --target-temperature 94.4 --equilibration-steps 50 --production-steps 100 \
  --final-rescale-before-production

# RDF comparison run (longer production for smoother g(r) statistics)
# g(r) sampling starts at production_start_step + gr_discard_steps
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --dt 1e-14 \
  --target-temperature 94.4 --equilibration-steps 50 --production-steps 20000 \
  --final-rescale-before-production --gr --gr-discard-steps 200 --gr-sample-every 5
```

### Scaling (Results 3)

```bash
# Recommended: use the automation script (median-of-20 paired runs)
bash scripts/run_all_data.sh

# On cerberus1, run scaling on an exclusive node:
srun --exclusive -N 1 --ntasks-per-node=32 bash scripts/run_all_data.sh

# Direct timing examples (single run each):
mpirun -np 1  ./md_solver --mode lj --integrator verlet --N 2048 --steps 200 --timing
mpirun -np 16 ./md_solver --mode lj --integrator verlet --N 864  --steps 2000 --timing
```

## Generate Plots

```bash
python3 scripts/plot_ho.py        # Phase-space and convergence plots
python3 scripts/plot_lj.py        # Energy conservation and g(r)
python3 scripts/plot_scaling.py   # Speedup, efficiency, Amdahl fit
```

## Clean / Package

```bash
make clean      # removes objects and binaries
make dist       # creates submission tarball
```

## Project Structure

```
include/md/    — C++ headers (constants, params, system, integrators, potentials, observables, MPI utilities)
src/           — Source implementations (main.cpp, potentials/lennard_jones.cpp)
tests/         — Unit tests (MIC wrapping, LJ force, position wrapping)
scripts/       — Python plotting scripts and bash automation
out/           — Generated data (excluded from submission)
```

Integrators (Euler, Velocity-Verlet, RK4) are implemented as inline functions in `include/md/integrators.hpp`.
```

### `.clang-format` (8 lines)

```
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 100
AllowShortFunctionsOnASingleLine: Inline
AllowShortIfStatementsOnASingleLine: false
AllowShortLoopsOnASingleLine: false
BreakBeforeBraces: Attach
PointerAlignment: Left
```

### `.gitignore` (19 lines)

```
# Generated data
out/

# AI context workspace
ai/

# Build artifacts
*.o
md_solver
test_runner

# Submission tarball
*.tar.gz

# Editor
.vscode/
.idea/
*.swp
*~
```

### `include/md/constants.hpp` (86 lines)

```cpp
/**
 * @file constants.hpp
 * @brief Physical constants for Molecular Dynamics simulation.
 *
 * Physical constants and derived LJ parameters (SI units).
 */

#ifndef MD_CONSTANTS_HPP
#define MD_CONSTANTS_HPP

namespace md {
namespace constants {

/// Boltzmann constant [J/K]
constexpr double kB = 1.380649e-23;

/// Lennard-Jones well depth / kB [K] (for Argon)
constexpr double eps_over_kB = 120.0;

/// Lennard-Jones well depth [J]
constexpr double epsilon = kB * eps_over_kB;

/// Lennard-Jones length scale (sigma) [m]
constexpr double sigma = 3.4e-10;

/// Argon atomic mass [kg]
constexpr double mass = 66.904265e-27;

/// Interaction cutoff in units of sigma
constexpr double rcut_sigma = 2.25;

/// Interaction cutoff [m]
constexpr double rcut = rcut_sigma * sigma;

// Derived quantities for optimised LJ kernel

/// sigma^2
constexpr double sigma2 = sigma * sigma;

/// sigma^6
constexpr double sigma6 = sigma2 * sigma2 * sigma2;

/// sigma^12
constexpr double sigma12 = sigma6 * sigma6;

/// Squared cutoff distance
constexpr double rcut2 = rcut * rcut;

/// 4 * epsilon (energy prefactor)
constexpr double four_eps = 4.0 * epsilon;

/// 24 * epsilon (force prefactor)
constexpr double twentyfour_eps = 24.0 * epsilon;

// Simulation constants

/// Fraction of sigma for random initial position perturbation
constexpr double fccPerturbation = 0.01;

/// g(r) histogram bin width in units of sigma
constexpr double grBinWidthSigma = 0.02;

/// Box size for HO mode (non-periodic; effectively unused but kept finite as a safety guard)
constexpr double L_ho_dummy = 1.0e10;

/// Lower bound numerical guard for temperature rescaling
constexpr double rescaleGuard = 1e-30;

// Rahman (1964) reference state point

/// Number of particles in Rahman's simulation
constexpr int N_rahman = 864;

/// FCC lattice repeats for N=864 (4 * 6^3 = 864)
constexpr int k_rahman = 6;

/// Box side length for N=864 in units of sigma
constexpr double L_sigma_rahman = 10.229;

/// Box side length for N=864 [m]
constexpr double L_rahman = L_sigma_rahman * sigma;

}  // namespace constants
}  // namespace md

#endif  // MD_CONSTANTS_HPP
```

### `include/md/mic.hpp` (19 lines)

```cpp
#ifndef MD_MIC_HPP
#define MD_MIC_HPP

#include <cmath>

namespace md {

/// Apply the minimum image convention to a single displacement component.
/// Maps dx into (-L/2, +L/2] using the round-based minimum image convention.
/// Tie behavior from std::round: +L/2 -> -L/2 and -L/2 -> +L/2.
inline double applyMIC(double dx, double L) {
    double invL = 1.0 / L;
    dx -= L * std::round(dx * invL);
    return dx;
}

}  // namespace md

#endif
```

### `include/md/params.hpp` (88 lines)

```cpp
/**
 * @file params.hpp
 * @brief Runtime parameters.
 */

#ifndef MD_PARAMS_HPP
#define MD_PARAMS_HPP

#include <cstdlib>
#include <string>

namespace md {

/// @brief Runtime parameters parsed from command-line arguments.
struct Params {
    int N = 864;                        ///< Number of particles
    int steps = 100;                    ///< Number of timesteps (HO) / legacy alias for LJ production_steps
    double dt = 1.0e-14;                ///< Timestep [s] (for LJ) or dimensionless (for HO)
    double T_init = 94.4;               ///< Legacy alias of targetTemperature [K]
    double targetTemperature = 94.4;    ///< Target temperature for LJ startup/production handoff [K]
    int equilibrationSteps = 50;        ///< LJ startup timesteps before production (with optional rescaling)
    int productionSteps = 100;          ///< LJ production timesteps (NVE after startup/final rescale)
    bool finalRescaleBeforeProduction = true;  ///< Apply one exact rescale at startup->production boundary
    double omega = 1.0;                 ///< HO angular frequency (only for mode "ho")
    std::string integrator = "verlet";  ///< "euler", "rk4", "verlet"
    std::string mode = "lj";            ///< "ho" or "lj"
    bool output = true;                 ///< Enable CSV output
    int seed = 42;                      ///< RNG seed for reproducibility
    int rescaleStep = -1;               ///< Legacy alias for equilibrationSteps (for CLI compatibility)
    bool timing = false;                ///< Enable wall-clock timing (disables output)
    bool gr = false;                    ///< Enable g(r) accumulation
    int grDiscardSteps = 200;           ///< Steps to discard after production_start_step before g(r)
    int grSampleEvery = 5;              ///< Sample g(r) every N steps after discard
    std::string outdir = "";            ///< Output directory for per-run namespaces

    static void parse(int argc, char* argv[], Params& p) {
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg == "--N" && i + 1 < argc)
                p.N = std::atoi(argv[++i]);
            else if (arg == "--steps" && i + 1 < argc) {
                p.steps = std::atoi(argv[++i]);
                p.productionSteps = p.steps;
            } else if (arg == "--production-steps" && i + 1 < argc)
                p.productionSteps = std::atoi(argv[++i]);
            else if (arg == "--equilibration-steps" && i + 1 < argc)
                p.equilibrationSteps = std::atoi(argv[++i]);
            else if (arg == "--dt" && i + 1 < argc)
                p.dt = std::atof(argv[++i]);
            else if ((arg == "--T" || arg == "--target-temperature") && i + 1 < argc) {
                p.T_init = std::atof(argv[++i]);
                p.targetTemperature = p.T_init;
            }
            else if (arg == "--omega" && i + 1 < argc)
                p.omega = std::atof(argv[++i]);
            else if (arg == "--integrator" && i + 1 < argc)
                p.integrator = argv[++i];
            else if (arg == "--mode" && i + 1 < argc)
                p.mode = argv[++i];
            else if (arg == "--no-output")
                p.output = false;
            else if (arg == "--seed" && i + 1 < argc)
                p.seed = std::atoi(argv[++i]);
            else if (arg == "--outdir" && i + 1 < argc)
                p.outdir = argv[++i];
            else if (arg == "--rescale-step" && i + 1 < argc) {
                p.rescaleStep = std::atoi(argv[++i]);
                p.equilibrationSteps = p.rescaleStep < 0 ? 0 : p.rescaleStep;
            } else if (arg == "--final-rescale-before-production")
                p.finalRescaleBeforeProduction = true;
            else if (arg == "--no-final-rescale-before-production")
                p.finalRescaleBeforeProduction = false;
            else if (arg == "--timing") {
                p.timing = true;
                p.output = false;
            } else if (arg == "--gr")
                p.gr = true;
            else if ((arg == "--gr-discard-steps" || arg == "--gr-discard") && i + 1 < argc)
                p.grDiscardSteps = std::atoi(argv[++i]);
            else if ((arg == "--gr-sample-every" || arg == "--gr-interval") && i + 1 < argc)
                p.grSampleEvery = std::atoi(argv[++i]);
        }
    }
};

}  // namespace md

#endif  // MD_PARAMS_HPP
```

### `include/md/mpi_context.hpp` (103 lines)

```cpp
/**
 * @file mpi_context.hpp
 * @brief MPI rank/size management, particle decomposition, and Allgatherv setup.
 *
 * Encapsulates all MPI-specific state: rank, size, local particle count,
 * offset, recvcounts/displs arrays for MPI_Allgatherv, and the permanent
 * global position buffer. All MPI array arguments use int type as required
 * by the MPI standard.
 */

#ifndef MD_MPI_CONTEXT_HPP
#define MD_MPI_CONTEXT_HPP

#include <mpi.h>

#include <algorithm>
#include <vector>

namespace md {

/**
 * @brief MPI context: decomposition and Allgatherv helpers.
 */
class MPIContext {
   public:
    int rank;    ///< This process's rank
    int size;    ///< Total number of MPI processes
    int N;       ///< Total number of particles (global)
    int localN;  ///< Number of particles owned by this rank
    int offset;  ///< Starting global index for this rank's particles

    std::vector<int> recvcounts;    ///< Number of doubles received from each rank (3 * localN[r])
    std::vector<int> displs;        ///< Displacement in doubles for each rank (3 * offset[r])
    std::vector<double> posGlobal;  ///< Permanent global position buffer (size 3*N)

    double commTime = 0.0;    ///< Accumulated MPI_Allgatherv wall time [s] (timing mode only)
    bool timingMode = false;  ///< When true, measure communication time

    /**
     * @brief Initialise MPI context with particle decomposition.
     *
     * Distributes N particles across P ranks as evenly as possible.
     * Rank r owns particles [offset_r, offset_r + localN_r).
     * The first (N % P) ranks each get one extra particle.
     *
     * Also pre-computes recvcounts and displs arrays for MPI_Allgatherv,
     * and allocates the permanent posGlobal buffer.
     *
     * @param totalN Total number of particles
     */
    void init(int totalN) {
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        MPI_Comm_size(MPI_COMM_WORLD, &size);
        N = totalN;

        // Remainder-safe decomposition
        localN = N / size + (rank < N % size ? 1 : 0);
        offset = rank * (N / size) + std::min(rank, N % size);

        // Pre-compute Allgatherv parameters (int arrays, values in doubles)
        recvcounts.resize(size);
        displs.resize(size);
        for (int r = 0; r < size; ++r) {
            int ln = N / size + (r < N % size ? 1 : 0);
            int off = r * (N / size) + std::min(r, N % size);
            recvcounts[r] = 3 * ln;
            displs[r] = 3 * off;
        }

        // Permanent global position buffer
        posGlobal.resize(3 * N, 0.0);
    }

    /**
     * @brief Gather local positions from all ranks into posGlobal.
     *
     * Each rank sends its local positions (3*localN doubles) and receives
     * the complete global position array (3*N doubles). This is the ONLY
     * collective communication in the time-stepping loop for LJ mode.
     *
     * When timingMode is true, the wall time spent in MPI_Allgatherv is
     * accumulated in commTime for compute-vs-communication analysis.
     *
     * @param posLocal Local position array (3*localN doubles, interleaved)
     */
    void allgatherPositions(const std::vector<double>& posLocal) {
        double t0 = timingMode ? MPI_Wtime() : 0.0;
        MPI_Allgatherv(posLocal.data(), 3 * localN, MPI_DOUBLE, posGlobal.data(), recvcounts.data(),
                       displs.data(), MPI_DOUBLE, MPI_COMM_WORLD);
        if (timingMode)
            commTime += (MPI_Wtime() - t0);
    }

    /**
     * @brief Check if this rank is the root (rank 0).
     * @return true if rank == 0
     */
    bool isRoot() const { return rank == 0; }
};

}  // namespace md

#endif  // MD_MPI_CONTEXT_HPP
```

### `include/md/system.hpp` (70 lines)

```cpp
/**
 * @file system.hpp
 * @brief Particle system state using flat, interleaved std::vector<double> arrays.
 *
 * All kinematic variables (position, velocity, acceleration/force) are stored
 * as contiguous 1D interleaved arrays of size 3*localN. Access pattern:
 *   arr[3*i + d]  for local particle i, dimension d ∈ {0, 1, 2}
 *
 * This layout ensures cache-locality and maps directly to MPI_Allgatherv
 * buffer requirements, eliminating indexing translation errors.
 */

#ifndef MD_SYSTEM_HPP
#define MD_SYSTEM_HPP

#include <cmath>
#include <vector>

namespace md {

/**
 * @brief State of the local particle system on one MPI rank.
 */
struct System {
    int localN;  ///< Number of particles owned by this rank
    int offset;  ///< Starting global index for this rank's particles
    int N;       ///< Total number of particles (global)
    double L;    ///< Box side length [m]

    std::vector<double> pos;  ///< Local positions  [3*localN], interleaved (x,y,z,x,y,z,...)
    std::vector<double> vel;  ///< Local velocities  [3*localN], interleaved
    std::vector<double> acc;  ///< Local accelerations [3*localN], interleaved (a = F/m)

    /**
     * @brief Initialise system arrays for localN particles.
     *
     * @param ln   Number of local particles
     * @param off  Starting global index
     * @param totalN Total particles
     * @param boxL Box side length
     */
    void init(int ln, int off, int totalN, double boxL) {
        localN = ln;
        offset = off;
        N = totalN;
        L = boxL;

        pos.assign(3 * localN, 0.0);
        vel.assign(3 * localN, 0.0);
        acc.assign(3 * localN, 0.0);
    }

    /**
     * @brief Wrap all local positions into the canonical range [0, L).
     *
     * Prevents unbounded coordinate growth and floating-point precision loss.
     * Must be called after every drift (position update) step and before
     * the subsequent MPI_Allgatherv / force evaluation.
     */
    void wrapPositions() {
        double invL = 1.0 / L;
        for (int i = 0; i < 3 * localN; ++i) {
            pos[i] -= L * std::floor(pos[i] * invL);
        }
    }
};

}  // namespace md

#endif  // MD_SYSTEM_HPP
```

### `include/md/rng.hpp` (140 lines)

```cpp
/**
 * @file rng.hpp
 * @brief FCC lattice construction and Box-Muller velocity initialisation.
 *
 * All random number generation uses std::mt19937_64 with a fixed seed,
 * executed ONLY on rank 0 for bitwise reproducibility across all MPI
 * configurations. Both functions accept a reference to a shared generator
 * to draw from a single, statistically sound random stream.
 */

#ifndef MD_RNG_HPP
#define MD_RNG_HPP

#include <cmath>
#include <random>
#include <vector>

#include "md/constants.hpp"

namespace md {

/**
 * @brief Construct an FCC lattice with N = 4k^3 particles in a cubic box.
 *
 * Four basis atoms per unit cell at fractional coordinates:
 *   (0.0, 0.0, 0.0), (0.5, 0.5, 0.0), (0.5, 0.0, 0.5), (0.0, 0.5, 0.5)
 *
 * A small random zero-mean perturbation (~0.01*sigma per coordinate) is
 * applied to break exact symmetry and prevent force singularities.
 *
 * @param N     Total number of particles (must be 4*k^3, validated by caller)
 * @param L     Box side length [m]
 * @param gen   Reference to shared RNG (caller owns lifetime)
 * @return      Flat interleaved position array of size 3*N
 */
std::vector<double> buildFCCLattice(int N, double L, std::mt19937_64& gen) {
    // Determine k such that N = 4*k^3 (validated by caller)
    int k = static_cast<int>(std::round(std::cbrt(N / 4.0)));

    std::vector<double> positions(3 * N);

    // Unit cell side length
    double a = L / k;

    // FCC basis vectors (fractional coordinates)
    const double basis[4][3] = {{0.0, 0.0, 0.0}, {0.5, 0.5, 0.0}, {0.5, 0.0, 0.5}, {0.0, 0.5, 0.5}};

    // Perturbation magnitude (zero-mean uniform distribution)
    double pertMag = constants::fccPerturbation * constants::sigma;
    std::uniform_real_distribution<double> pertDist(-pertMag, pertMag);

    int idx = 0;
    for (int ix = 0; ix < k; ++ix) {
        for (int iy = 0; iy < k; ++iy) {
            for (int iz = 0; iz < k; ++iz) {
                for (int b = 0; b < 4; ++b) {
                    positions[3 * idx + 0] = (ix + basis[b][0]) * a + pertDist(gen);
                    positions[3 * idx + 1] = (iy + basis[b][1]) * a + pertDist(gen);
                    positions[3 * idx + 2] = (iz + basis[b][2]) * a + pertDist(gen);
                    ++idx;
                }
            }
        }
    }

    return positions;
}

/**
 * @brief Maxwell-Boltzmann velocities via Box-Muller. Removes CoM drift, rescales to target T.
 *
 * @param N      Total number of particles
 * @param T      Target temperature [K]
 * @param mass   Particle mass [kg]
 * @param gen    Reference to shared RNG (same stream as lattice perturbation)
 * @return       Flat interleaved velocity array of size 3*N
 */
std::vector<double> generateVelocities(int N, double T, double mass, std::mt19937_64& gen) {
    std::vector<double> vel(3 * N);

    double sigmaV = std::sqrt(constants::kB * T / mass);
    constexpr double pi = 3.14159265358979323846;

    std::uniform_real_distribution<double> uDist(0.0, 1.0);

    int totalComponents = 3 * N;

    // Box-Muller: generate pairs of normal deviates
    for (int i = 0; i < totalComponents; i += 2) {
        double u1, u2;
        // Ensure u1 > 0 to avoid log(0)
        do {
            u1 = uDist(gen);
        } while (u1 == 0.0);
        u2 = uDist(gen);

        double mag = sigmaV * std::sqrt(-2.0 * std::log(u1));
        double z1 = mag * std::cos(2.0 * pi * u2);
        double z2 = mag * std::sin(2.0 * pi * u2);

        vel[i] = z1;
        if (i + 1 < totalComponents) {
            vel[i + 1] = z2;
        }
    }

    // Remove centre-of-mass drift to ensure zero total momentum.
    double vxMean = 0.0, vyMean = 0.0, vzMean = 0.0;
    for (int i = 0; i < N; ++i) {
        vxMean += vel[3 * i + 0];
        vyMean += vel[3 * i + 1];
        vzMean += vel[3 * i + 2];
    }
    vxMean /= N;
    vyMean /= N;
    vzMean /= N;

    for (int i = 0; i < N; ++i) {
        vel[3 * i + 0] -= vxMean;
        vel[3 * i + 1] -= vyMean;
        vel[3 * i + 2] -= vzMean;
    }

    double sumSq = 0.0;
    for (int i = 0; i < 3 * N; ++i) {
        sumSq += vel[i] * vel[i];
    }
    double tActual = (mass / (3.0 * (N - 1) * constants::kB)) * sumSq;
    double lambda = std::sqrt(T / tActual);

    for (int i = 0; i < 3 * N; ++i) {
        vel[i] *= lambda;
    }

    return vel;
}

}  // namespace md

#endif  // MD_RNG_HPP
```

### `include/md/potentials.hpp` (67 lines)

```cpp
/**
 * @file potentials.hpp
 * @brief Harmonic Oscillator and Lennard-Jones acceleration/energy kernels.
 *
 * Both potentials implement a common interface:
 *   computeForces(system, posGlobal, localPE)
 *
 * The HO potential computes a = -omega^2 * x purely locally, ignoring
 * the global position data. The LJ potential uses the global positions
 * from MPI_Allgatherv with minimum image convention and hard cutoff.
 */

#ifndef MD_POTENTIALS_HPP
#define MD_POTENTIALS_HPP

#include <vector>

#include "md/system.hpp"

namespace md {

/**
 * @brief Compute harmonic oscillator accelerations for local particles.
 *
 * a_i = -omega^2 * x_i  (independent, non-interacting particles)
 * V_i = 0.5 * m * omega^2 * x_i^2
 *
 * This kernel operates purely on local data and does NOT require any
 * global position information. The MPI_Allgatherv call should be
 * bypassed entirely in HO mode to eliminate unnecessary O(N)
 * communication overhead.
 *
 * Validation runs should use N=1. The code supports N independent copies.
 *
 * @param[in,out] sys       System state (accelerations written to sys.acc)
 * @param[in]     posGlobal Ignored for HO (may be empty)
 * @param[out]    localPE   Local potential energy contribution
 * @param[in]     omega     Angular frequency
 * @param[in]     mass      Particle mass [kg]
 */
void computeHOForces(System& sys, const std::vector<double>& posGlobal, double& localPE,
                     double omega, double mass);

/**
 * @brief Compute Lennard-Jones forces for local particles against all particles.
 *
 * Uses the optimised kernel with shared intermediates (no pow, no sqrt).
 * Applies minimum image convention and hard
 * cutoff at rcut. Accumulates potential energy unconditionally for all
 * j != i; the local sum is multiplied by 0.5 AFTER the loop to correct
 * for double-counting.
 *
 * Force formula (Rahman Appendix, brief Eqn 3):
 *   a_i = (24*eps/m) * sum_{j!=i} (x_i - x_j)/r^2_ij
 *         * [2*(sigma/r_ij)^12 - (sigma/r_ij)^6]
 *
 * @param[in,out] sys       System state (forces written to sys.acc)
 * @param[in]     posGlobal Global positions (3*N doubles, from Allgatherv)
 * @param[out]    localPE   Local PE contribution (pre-halved for this rank's pairs)
 * @param[in]     mass      Particle mass [kg]
 */
void computeLJForces(System& sys, const std::vector<double>& posGlobal, double& localPE,
                     double mass);

}  // namespace md

#endif  // MD_POTENTIALS_HPP
```

### `include/md/integrators.hpp` (115 lines)

```cpp
/**
 * @file integrators.hpp
 * @brief Forward Euler, RK4, and Velocity-Verlet integrators.
 */

#ifndef MD_INTEGRATORS_HPP
#define MD_INTEGRATORS_HPP

#include <vector>

#include "md/mpi_context.hpp"
#include "md/system.hpp"

namespace md {

template <typename ForceFunctor>
inline void stepEuler(System& sys, MPIContext& ctx, double dt, ForceFunctor computeForce,
                      double& localPE, bool isHO) {
    const int n3 = 3 * sys.localN;

    for (int i = 0; i < n3; ++i) {
        sys.pos[i] += sys.vel[i] * dt;
    }

    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += sys.acc[i] * dt;
    }

    if (!isHO) {
        sys.wrapPositions();
        ctx.allgatherPositions(sys.pos);
    }

    computeForce(sys, ctx.posGlobal, localPE);
}

template <typename ForceFunctor>
inline void stepRK4(System& sys, MPIContext& ctx, double dt, ForceFunctor computeForce,
                    double& localPE, bool isHO) {
    const int n3 = 3 * sys.localN;

    std::vector<double> x0(sys.pos);
    std::vector<double> v0(sys.vel);

    auto evalStage = [&](std::vector<double>& kx, std::vector<double>& kv, double weight,
                         const std::vector<double>& prevKx, const std::vector<double>& prevKv) {
        if (weight > 0.0) {
            for (int i = 0; i < n3; ++i) {
                sys.pos[i] = x0[i] + weight * prevKx[i];
                sys.vel[i] = v0[i] + weight * prevKv[i];
            }
            if (!isHO) {
                sys.wrapPositions();
                ctx.allgatherPositions(sys.pos);
            }
            computeForce(sys, ctx.posGlobal, localPE);
        }
        for (int i = 0; i < n3; ++i) {
            kx[i] = sys.vel[i] * dt;
            kv[i] = sys.acc[i] * dt;
        }
    };

    std::vector<double> k1x(n3), k1v(n3);
    evalStage(k1x, k1v, 0.0, k1x, k1v);

    std::vector<double> k2x(n3), k2v(n3);
    evalStage(k2x, k2v, 0.5, k1x, k1v);

    std::vector<double> k3x(n3), k3v(n3);
    evalStage(k3x, k3v, 0.5, k2x, k2v);

    std::vector<double> k4x(n3), k4v(n3);
    evalStage(k4x, k4v, 1.0, k3x, k3v);

    for (int i = 0; i < n3; ++i) {
        sys.pos[i] = x0[i] + (k1x[i] + 2.0 * k2x[i] + 2.0 * k3x[i] + k4x[i]) / 6.0;
        sys.vel[i] = v0[i] + (k1v[i] + 2.0 * k2v[i] + 2.0 * k3v[i] + k4v[i]) / 6.0;
    }

    if (!isHO) {
        sys.wrapPositions();
        ctx.allgatherPositions(sys.pos);
    }
    computeForce(sys, ctx.posGlobal, localPE);
}

template <typename ForceFunctor>
inline void stepVelocityVerlet(System& sys, MPIContext& ctx, double dt, ForceFunctor computeForce,
                               double& localPE, bool isHO) {
    const int n3 = 3 * sys.localN;
    const double halfDt = 0.5 * dt;

    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += halfDt * sys.acc[i];
    }
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] += dt * sys.vel[i];
    }

    if (!isHO) {
        sys.wrapPositions();
        ctx.allgatherPositions(sys.pos);
    }

    computeForce(sys, ctx.posGlobal, localPE);

    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += halfDt * sys.acc[i];
    }
}

}  // namespace md

#endif  // MD_INTEGRATORS_HPP
```

### `include/md/observables.hpp` (90 lines)

```cpp
/**
 * @file observables.hpp
 * @brief Thermodynamic observables: energies, temperature, g(r) binning.
 *
 * Provides functions for computing kinetic energy (local), measuring
 * temperature from the equipartition theorem, and accumulating the
 * radial distribution function g(r) histogram.
 */

#ifndef MD_OBSERVABLES_HPP
#define MD_OBSERVABLES_HPP

#include <cmath>
#include <vector>

#include "md/constants.hpp"
#include "md/system.hpp"

namespace md {

/**
 * @brief Compute local kinetic energy for this rank's particles.
 *
 * E_kin_local = 0.5 * m * sum_i |v_i|^2
 *
 * Must be followed by MPI_Reduce(MPI_SUM) to rank 0 for the global total.
 *
 * @param sys   System state (reads velocities)
 * @param mass  Particle mass [kg]
 * @return      Local kinetic energy [J]
 */
double computeLocalKineticEnergy(const System& sys, double mass);

/**
 * @brief Compute temperature from total kinetic energy.
 *
 * T = (2 / (N_dof * k_B)) * E_kin_total
 *
 * Uses N_dof = 3*(N-1) (after CoM drift removal) for thermodynamic accuracy.
 * The difference from 3*N is <0.35% for N=864.
 *
 * @param eKinTotal Total kinetic energy (from MPI_Reduce) [J]
 * @param N         Total number of particles
 * @return          Instantaneous temperature [K]
 */
double computeTemperature(double eKinTotal, int N);

// NOTE: Velocity rescaling is performed directly in main.cpp using
// computeTemperature() + MPI_Bcast(lambda) for MPI-correct thermostatting.
// No standalone rescaleVelocities() helper — avoids duplication.

/**
 * @brief Accumulate pair distances into a g(r) histogram.
 *
 * Uses unordered pairs (i < j) from this rank's local particles against
 * all global particles. Bin width = dr, range [0, rMax).
 * The result must be reduced via MPI_Reduce(MPI_SUM) across all ranks,
 * then normalised by the ideal gas shell volume and number of frames.
 *
 * @param posGlobal  Global positions (3*N doubles)
 * @param N          Total number of particles
 * @param L          Box side length
 * @param offset     Starting global index for this rank
 * @param localN     Number of local particles
 * @param dr         Bin width
 * @param rMax       Maximum distance to bin
 * @param histogram  Output histogram (must be pre-sized)
 */
void accumulateGR(const std::vector<double>& posGlobal, int N, double L, int offset, int localN,
                  double dr, double rMax, std::vector<double>& histogram);

/**
 * @brief Normalise the accumulated g(r) histogram.
 *
 * Since we count unordered pairs (i < j), each pair appears exactly once.
 * The standard formula uses ordered pairs (factor of N*(N-1) total), so we
 * multiply by 2 to compensate:
 *   g(r) = 2 * count / (rho * N * 4*pi*r^2 * dr * nFrames)
 *
 * @param histogram  Accumulated histogram (modified in-place to g(r))
 * @param dr         Bin width
 * @param N          Total number of particles
 * @param L          Box side length
 * @param nFrames    Number of frames accumulated
 */
void normaliseGR(std::vector<double>& histogram, double dr, int N, double L, int nFrames);

}  // namespace md

#endif  // MD_OBSERVABLES_HPP
```

### `src/main.cpp` (572 lines)

```cpp
/**
 * @file main.cpp
 * @brief Main entry point for the MPI Molecular Dynamics solver.
 *
 * Workflow:
 *   1. MPI_Init, parse CLI parameters
 *   2. Rank 0 generates initial conditions (FCC lattice + Box-Muller velocities)
 *   3. MPI_Bcast distributes complete state to all ranks
 *   4. Each rank extracts its local partition
 *   5. Initial force evaluation
 *   6. Time-stepping loop with selected integrator
 *   7. Observables computed and output (rank 0 only)
 *   8. MPI_Finalize
 *
 * All runtime parameters come from CLI arguments (see params.hpp).
 */

#include <mpi.h>
#include <sys/stat.h>

#include <cmath>
#include <cstdio>
#include <ctime>
#include <algorithm>
#include <fstream>
#include <functional>
#include <iomanip>
#include <limits>
#include <random>
#include <string>
#include <vector>

#include "md/constants.hpp"
#include "md/integrators.hpp"
#include "md/mpi_context.hpp"
#include "md/observables.hpp"
#include "md/params.hpp"
#include "md/potentials.hpp"
#include "md/rng.hpp"
#include "md/system.hpp"

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    // Parse parameters
    md::Params params;
    md::Params::parse(argc, argv, params);

    // MPI setup and particle decomposition
    md::MPIContext ctx;
    ctx.init(params.N);
    ctx.timingMode = params.timing;

    const bool isHO = (params.mode == "ho");
    const int N = params.N;
    const int equilibrationSteps = isHO ? 0 : std::max(0, params.equilibrationSteps);
    const int nSteps = isHO ? params.steps : std::max(0, params.productionSteps);
    const int nFrames = nSteps + 1;
    const int totalStepsExecuted = nSteps + equilibrationSteps;
    const int productionStartStep = 0;
    int grDiscardSteps = params.grDiscardSteps;
    int grSampleEvery = params.grSampleEvery;
    if (grDiscardSteps < 0) {
        if (ctx.isRoot()) {
            std::fprintf(stderr,
                         "WARNING: --gr-discard-steps=%d is invalid; using 0 instead.\n",
                         grDiscardSteps);
        }
        grDiscardSteps = 0;
    }
    if (grSampleEvery <= 0) {
        if (ctx.isRoot()) {
            std::fprintf(stderr,
                         "WARNING: --gr-sample-every=%d is invalid; using 1 instead.\n",
                         grSampleEvery);
        }
        grSampleEvery = 1;
    }
    const int grStart = productionStartStep + grDiscardSteps;
    const int maxGRFrames = (!isHO && params.gr && grStart <= nSteps)
                                ? (1 + (nSteps - grStart) / grSampleEvery)
                                : 0;

    // Box side length (constant density scaling for LJ)
    // For LJ: scale from Rahman's L=10.229*sigma for N=864 to maintain constant density
    // For HO: L is irrelevant (non-interacting), set to a large value
    double L;
    if (isHO) {
        L = md::constants::L_ho_dummy;  // effectively unused for HO
    } else {
        L = md::constants::L_sigma_rahman * md::constants::sigma *
            std::cbrt(static_cast<double>(N) / md::constants::N_rahman);
    }

    // Generate initial conditions on rank 0, broadcast to all
    std::vector<double> posAll(3 * N, 0.0);
    std::vector<double> velAll(3 * N, 0.0);
    int fccError = 0;  // broadcast from root to all ranks (LJ only)

    if (ctx.isRoot()) {
        if (isHO) {
            if (params.N != 1) {
                std::fprintf(
                    stderr,
                    "WARNING: HO validation expects N=1. Continuing with N>1 treats particles as "
                    "independent copies.\n");
            }
            // HO: single particle (or N independent particles) with simple IC
            // x(0) = 1.0, v(0) = 0.0 for each particle (each dimension)
            for (int i = 0; i < N; ++i) {
                posAll[3 * i + 0] = 1.0;  // x = 1
                posAll[3 * i + 1] = 0.0;  // y = 0
                posAll[3 * i + 2] = 0.0;  // z = 0
                velAll[3 * i + 0] = 0.0;
                velAll[3 * i + 1] = 0.0;
                velAll[3 * i + 2] = 0.0;
            }
        } else {
            // Validate FCC particle count: N must equal 4*k^3
            int k = static_cast<int>(std::round(std::cbrt(N / 4.0)));
            if (4 * k * k * k != N) {
                std::fprintf(stderr,
                             "ERROR: N = %d is not a valid FCC particle count "
                             "(need N = 4*k^3, nearest k = %d gives N = %d)\n",
                             N, k, 4 * k * k * k);
                fccError = 1;
            } else {
                // LJ: FCC lattice with perturbation + Box-Muller velocities
                // Single RNG stream for both
                std::mt19937_64 gen(params.seed);
                posAll = md::buildFCCLattice(N, L, gen);
                velAll =
                    md::generateVelocities(N, params.targetTemperature, md::constants::mass, gen);

                double sumV2 = 0.0;
                for (int i = 0; i < 3 * N; ++i) {
                    sumV2 += velAll[i] * velAll[i];
                }
                double eKin0 = 0.5 * md::constants::mass * sumV2;
                double tMeasured0 = md::computeTemperature(eKin0, N);

                std::printf("=== Initial Conditions (Rank 0) ===\n");
                std::printf("Seed used for RNG: %d\n", params.seed);
                std::printf("FCC lattice generated\n");
                std::printf("Perturbation amplitude: %.6e m (%.4f sigma)\n",
                            md::constants::fccPerturbation * md::constants::sigma,
                            md::constants::fccPerturbation);
                std::printf("Box-Muller velocities applied\n");
                std::printf("Initial measured Temperature: %.6f K\n", tMeasured0);
                std::printf("===================================\n");
            }
        }
    }

    // All ranks check FCC validation result (LJ only)
    if (!isHO) {
        MPI_Bcast(&fccError, 1, MPI_INT, 0, MPI_COMM_WORLD);
        if (fccError) {
            MPI_Finalize();
            return 1;
        }
    }

    // Broadcast complete initial state to all ranks
    // (NOT MPI_Scatterv — every rank needs global positions for first force eval)
    MPI_Bcast(posAll.data(), 3 * N, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(velAll.data(), 3 * N, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // Initialise local system state
    md::System sys;
    sys.init(ctx.localN, ctx.offset, N, L);

    // Extract local partition from global arrays
    for (int i = 0; i < ctx.localN; ++i) {
        for (int d = 0; d < 3; ++d) {
            sys.pos[3 * i + d] = posAll[3 * (ctx.offset + i) + d];
            sys.vel[3 * i + d] = velAll[3 * (ctx.offset + i) + d];
        }
    }

    // Copy full positions into global buffer for first force evaluation
    ctx.posGlobal = posAll;

    // Wrap positions into [0, L)
    if (!isHO) {
        sys.wrapPositions();
        ctx.allgatherPositions(sys.pos);
    }

    // Build force function
    double omega = params.omega;
    double mass = md::constants::mass;

    auto evalHO = [omega, mass](md::System& s, const std::vector<double>& pg, double& pe) {
        md::computeHOForces(s, pg, pe, omega, mass);
    };
    auto evalLJ = [mass](md::System& s, const std::vector<double>& pg, double& pe) {
        md::computeLJForces(s, pg, pe, mass);
    };

    enum class IntegratorType { Euler, RK4, Verlet };
    IntegratorType intType = IntegratorType::Verlet;
    if (params.integrator == "euler")
        intType = IntegratorType::Euler;
    else if (params.integrator == "rk4")
        intType = IntegratorType::RK4;
    double localPE = 0.0;

    auto advanceOneStep = [&]() {
        if (intType == IntegratorType::Euler) {
            if (isHO)
                md::stepEuler(sys, ctx, params.dt, evalHO, localPE, isHO);
            else
                md::stepEuler(sys, ctx, params.dt, evalLJ, localPE, isHO);
        } else if (intType == IntegratorType::RK4) {
            if (isHO)
                md::stepRK4(sys, ctx, params.dt, evalHO, localPE, isHO);
            else
                md::stepRK4(sys, ctx, params.dt, evalLJ, localPE, isHO);
        } else {
            if (isHO)
                md::stepVelocityVerlet(sys, ctx, params.dt, evalHO, localPE, isHO);
            else
                md::stepVelocityVerlet(sys, ctx, params.dt, evalLJ, localPE, isHO);
        }
    };

    // Initial force evaluation
    if (isHO) {
        evalHO(sys, ctx.posGlobal, localPE);
    } else {
        evalLJ(sys, ctx.posGlobal, localPE);
    }

    bool finalRescaleApplied = false;
    double startupTempBeforeFinal = std::numeric_limits<double>::quiet_NaN();
    double startupTempAfterFinal = std::numeric_limits<double>::quiet_NaN();

    // LJ startup/equilibration: optional pre-production preparation with rescaling.
    if (!isHO) {
        for (int startupStep = 1; startupStep <= equilibrationSteps; ++startupStep) {
            double localKE = md::computeLocalKineticEnergy(sys, md::constants::mass);
            double totalKE = 0.0, totalPE = 0.0;
            MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
            MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

            double lambda = 1.0;
            if (ctx.isRoot()) {
                double tMeasured = md::computeTemperature(totalKE, N);
                if (tMeasured > md::constants::rescaleGuard) {
                    lambda = std::sqrt(params.targetTemperature / tMeasured);
                }
                if (!params.timing) {
                    std::printf(
                        "Startup rescale step %d/%d: lambda = %.15e, T_before = %.6f K, "
                        "target = %.6f K\n",
                        startupStep, equilibrationSteps, lambda, tMeasured, params.targetTemperature);
                }
            }
            MPI_Bcast(&lambda, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
            for (int i = 0; i < 3 * sys.localN; ++i) {
                sys.vel[i] *= lambda;
            }

            advanceOneStep();
        }

        double localKE = md::computeLocalKineticEnergy(sys, md::constants::mass);
        double totalKE = 0.0, totalPE = 0.0;
        MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
        MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

        if (ctx.isRoot()) {
            startupTempBeforeFinal = md::computeTemperature(totalKE, N);
        }

        if (params.finalRescaleBeforeProduction) {
            double lambda = 1.0;
            if (ctx.isRoot()) {
                if (startupTempBeforeFinal > md::constants::rescaleGuard) {
                    lambda = std::sqrt(params.targetTemperature / startupTempBeforeFinal);
                }
                finalRescaleApplied = std::abs(lambda - 1.0) > 1e-12;
                if (!params.timing) {
                    std::printf("Startup->production rescale: lambda = %.15e, T_before = %.6f K\n",
                                lambda, startupTempBeforeFinal);
                }
            }
            MPI_Bcast(&lambda, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
            for (int i = 0; i < 3 * sys.localN; ++i) {
                sys.vel[i] *= lambda;
            }

            localKE = md::computeLocalKineticEnergy(sys, md::constants::mass);
            totalKE = 0.0;
            MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
            if (ctx.isRoot()) {
                startupTempAfterFinal = md::computeTemperature(totalKE, N);
            }
        } else {
            startupTempAfterFinal = startupTempBeforeFinal;
        }
    }

    // Create output directory and open file on rank 0
    std::ofstream outFile;
    if (params.output && ctx.isRoot()) {
        std::string fname;
        if (!params.outdir.empty()) {
            fname = params.outdir + "/" + params.mode + "_" + params.integrator + ".csv";
        } else {
            mkdir("out", 0755);
            fname = "out/" + params.mode + "_" + params.integrator + ".csv";
        }
        outFile.open(fname);
        if (outFile.is_open()) {
            outFile << std::setprecision(15);
            std::time_t t = std::time(nullptr);
            char tstr[100];
            std::strftime(tstr, sizeof(tstr), "%Y-%m-%dT%H:%M:%SZ", std::gmtime(&t));
            outFile << "# mode: " << params.mode << ", integrator: " << params.integrator
                    << ", N: " << N << ", P: " << ctx.size << ", dt: " << params.dt
                    << ", steps: " << nSteps << ", n_steps: " << nSteps
                    << ", n_frames: " << nFrames
                    << ", step_indexing: 0..steps (includes initial frame)"
                    << ", total_steps_executed: " << totalStepsExecuted
                    << ", seed: " << params.seed << ", L: " << L
                    << ", rcut: " << md::constants::rcut_sigma * md::constants::sigma
                    << ", target_temperature: " << params.targetTemperature
                    << ", equilibration_steps: " << equilibrationSteps
                    << ", production_steps: " << nSteps
                    << ", production_start_step: " << productionStartStep
                    << ", final_rescale_before_production: "
                    << (params.finalRescaleBeforeProduction ? "true" : "false")
                    << ", final_rescale_applied: " << (finalRescaleApplied ? "true" : "false")
                    << ", production_nve: " << (!isHO ? "true" : "false")
                    << ", gr_discard_steps: " << grDiscardSteps
                    << ", gr_sample_every: " << grSampleEvery << ", gr_start: " << grStart;
            if (!isHO && std::isfinite(startupTempBeforeFinal)) {
                outFile << ", startup_temperature_before_final_rescale: " << startupTempBeforeFinal;
            }
            if (!isHO && std::isfinite(startupTempAfterFinal)) {
                outFile << ", startup_temperature_after_final_rescale: " << startupTempAfterFinal;
            }
            if (!isHO) {
                outFile << ", lattice: FCC, velocities: Box-Muller";
            }
            outFile << ", timestamp: " << tstr << "\n";
            if (isHO) {
                // HO: output position, velocity, energy for phase-space & convergence plots
                outFile << "step,time,x,v,E_kin,E_pot,E_total\n";
            } else {
                outFile << "step,time,E_kin,E_pot,E_total,temperature\n";
            }
        }
    }

    // Print simulation info on rank 0
    if (ctx.isRoot() && !params.timing) {
        std::printf("=== MD Solver ===\n");
        std::printf("Mode: %s | Integrator: %s\n", params.mode.c_str(), params.integrator.c_str());
        std::printf(
            "N = %d | P = %d | timesteps = %d | frames = %d (step 0..%d) | dt = %.3e\n", N,
            ctx.size, nSteps, nFrames, nSteps, params.dt);
        if (!isHO) {
            std::printf(
                "LJ semantics: --equilibration-steps prepares the state, --production-steps "
                "controls the reported NVE trajectory.\n");
            std::printf(
                "Output includes the production initial frame at step 0 (n_frames = "
                "production_steps + 1).\n");
            std::printf("L = %.6e m (%.4f sigma)\n", L, L / md::constants::sigma);
            std::printf("Target temperature = %.1f K | seed = %d\n", params.targetTemperature,
                        params.seed);
            std::printf("Startup timesteps = %d | production timesteps = %d | total executed = %d\n",
                        equilibrationSteps, nSteps, totalStepsExecuted);
            std::printf("Production simulated time = %.3e s (= production_steps * dt)\n",
                        nSteps * params.dt);
            std::printf("production_start_step = %d (production-only output)\n", productionStartStep);
            if (std::isfinite(startupTempBeforeFinal)) {
                std::printf("Startup boundary temperature before final rescale: %.6f K\n",
                            startupTempBeforeFinal);
            }
            if (std::isfinite(startupTempAfterFinal)) {
                std::printf("Startup boundary temperature after final rescale: %.6f K\n",
                            startupTempAfterFinal);
            }
            if (params.gr) {
                std::printf(
                    "g(r): production_start_step=%d, gr_start=%d (= production_start_step + "
                    "gr_discard_steps=%d), sample_every=%d\n",
                    productionStartStep, grStart, grDiscardSteps, grSampleEvery);
            }
        } else {
            std::printf(
                "Step semantics: --steps is the number of integration updates; output includes "
                "the initial frame at step 0.\n");
            std::printf("HO mode: periodic box size is not used\n");
        }
        std::printf("==================\n");
    }

    if (params.gr && !isHO && maxGRFrames <= 0 && ctx.isRoot()) {
        if (grStart > nSteps) {
            std::fprintf(stderr,
                         "WARNING: g(r) requested but gr_start=%d is beyond final step=%d. "
                         "No RDF frames will be sampled.\n",
                         grStart, nSteps);
        } else {
            std::fprintf(stderr,
                         "WARNING: g(r) requested but no frames available "
                         "(production_steps=%d, production_start_step=%d, gr_discard_steps=%d).\n",
                         nSteps, productionStartStep, grDiscardSteps);
        }
    }

    // g(r) histogram setup for LJ mode
    // Keep HO mode at zero-sized buffers to avoid meaningless allocations.
    const double grDr = md::constants::grBinWidthSigma * md::constants::sigma;  // bin width
    const double grRMax = isHO ? 0.0 : 0.5 * L;                                  // [0, L/2] for LJ
    const int grNBins = isHO ? 0 : static_cast<int>(grRMax / grDr);
    std::vector<double> grHistLocal(grNBins, 0.0);
    int grFrames = 0;

    // Timing setup
    MPI_Barrier(MPI_COMM_WORLD);
    double tStart = MPI_Wtime();

    // Time-stepping loop
    for (int step = 0; step <= nSteps; ++step) {
        // Compute observables (skip in timing mode)
        double totalKE = 0.0, totalPE = 0.0;
        if (!params.timing) {
            double localKE = md::computeLocalKineticEnergy(sys, md::constants::mass);

            // Reduce energies to rank 0
            MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
            MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

            double totalE = totalKE + totalPE;

            // Output (rank 0 only)
            if (params.output && ctx.isRoot() && outFile.is_open()) {
                double time = step * params.dt;
                if (isHO) {
                    // HO: output x, v for first particle (1D oscillator on x-axis)
                    double x = sys.pos[0];  // position of particle 0, x-component
                    double v = sys.vel[0];  // velocity of particle 0, x-component
                    outFile << step << "," << time << "," << x << "," << v << "," << totalKE << ","
                            << totalPE << "," << totalE << "\n";
                } else {
                    double T = md::computeTemperature(totalKE, N);
                    outFile << step << "," << time << "," << totalKE << "," << totalPE << ","
                            << totalE << "," << T << "\n";
                }
            }

        }

        // Accumulate g(r) histogram in the production window
        if (params.gr && !isHO && step >= grStart && ((step - grStart) % grSampleEvery == 0)) {
            md::accumulateGR(ctx.posGlobal, N, L, ctx.offset, ctx.localN, grDr, grRMax,
                             grHistLocal);
            ++grFrames;
        }

        // Advance one timestep; skip update on the last iteration
        if (step == nSteps)
            break;

        advanceOneStep();
    }

    // Timing completion
    double tEnd = MPI_Wtime();
    double elapsed = tEnd - tStart;

    // Find the slowest rank using MPI_MAXLOC — ensures wall and comm come
    // from the SAME rank, guaranteeing comm <= wall. Allreduce so all ranks
    // know slowestRank (needed for the subsequent MPI_Bcast).
    struct {
        double val;
        int rank;
    } localData{elapsed, ctx.rank}, globalData{0.0, 0};
    MPI_Allreduce(&localData, &globalData, 1, MPI_DOUBLE_INT, MPI_MAXLOC, MPI_COMM_WORLD);

    double maxTime = globalData.val;
    int slowestRank = globalData.rank;

    // Get comm time from the slowest rank (not the max comm across all ranks)
    double reportedCommTime = 0.0;
    if (params.timing) {
        if (ctx.rank == slowestRank) {
            reportedCommTime = ctx.commTime;
        }
        MPI_Bcast(&reportedCommTime, 1, MPI_DOUBLE, slowestRank, MPI_COMM_WORLD);
    }

    if (ctx.isRoot()) {
        std::printf("Wall time: %.6f s (max across %d ranks)\n", maxTime, ctx.size);
        if (params.timing) {
            double computeTime = maxTime - reportedCommTime;
            std::printf("  Comm time: %.6f s (%.1f%%)\n", reportedCommTime,
                        100.0 * reportedCommTime / maxTime);
            std::printf("  Compute time: %.6f s (%.1f%%)\n", computeTime,
                        100.0 * computeTime / maxTime);
        }
    }

    // Write g(r) to file for LJ mode
    if (params.gr && !isHO && grFrames > 0) {
        // Reduce histogram across all ranks
        std::vector<double> grHistGlobal(grNBins, 0.0);
        MPI_Reduce(grHistLocal.data(), grHistGlobal.data(), grNBins, MPI_DOUBLE, MPI_SUM, 0,
                   MPI_COMM_WORLD);

        if (ctx.isRoot()) {
            // Normalise: g(r) = (1 / (rho * N)) * count / (4*pi*r^2 * dr * nFrames)
            md::normaliseGR(grHistGlobal, grDr, N, L, grFrames);

            std::string grFname = params.outdir.empty() ? "out/gr.csv" : params.outdir + "/gr.csv";
            std::ofstream grFile(grFname);
            if (grFile.is_open()) {
                std::time_t t = std::time(nullptr);
                char tstr[100];
                std::strftime(tstr, sizeof(tstr), "%Y-%m-%dT%H:%M:%SZ", std::gmtime(&t));
                grFile << "# mode: " << params.mode << ", integrator: " << params.integrator
                       << ", N: " << N << ", P: " << ctx.size << ", dt: " << params.dt
                       << ", steps: " << nSteps << ", n_steps: " << nSteps
                       << ", n_frames: " << nFrames
                       << ", step_indexing: 0..steps (includes initial frame)"
                       << ", total_steps_executed: " << totalStepsExecuted
                       << ", seed: " << params.seed << ", L: " << L
                       << ", rcut: " << md::constants::rcut_sigma * md::constants::sigma
                       << ", target_temperature: " << params.targetTemperature
                       << ", equilibration_steps: " << equilibrationSteps
                       << ", production_steps: " << nSteps
                       << ", production_start_step: " << productionStartStep
                       << ", final_rescale_before_production: "
                       << (params.finalRescaleBeforeProduction ? "true" : "false")
                       << ", final_rescale_applied: " << (finalRescaleApplied ? "true" : "false")
                       << ", production_nve: true"
                       << ", gr_discard_steps: " << grDiscardSteps
                       << ", gr_sample_every: " << grSampleEvery << ", gr_start: " << grStart
                       << ", lattice: FCC, velocities: Box-Muller, timestamp: " << tstr << "\n";
                grFile << "r_sigma,gr\n";
                for (int b = 0; b < grNBins; ++b) {
                    double rMid = (b + 0.5) * grDr;
                    grFile << (rMid / md::constants::sigma) << "," << grHistGlobal[b] << "\n";
                }
                grFile.close();
                if (!params.timing) {
                    std::printf("g(r) written to %s (%d bins, %d frames)\n", grFname.c_str(),
                                grNBins, grFrames);
                }
            }
        }
    } else if (params.gr && !isHO && ctx.isRoot() && !params.timing) {
        std::fprintf(stderr,
                     "WARNING: g(r) skipped because no frames were sampled. "
                     "Adjust --production-steps, --equilibration-steps, --gr-discard-steps, or "
                     "--gr-sample-every.\n");
    }

    // Close output file
    if (outFile.is_open()) {
        outFile.close();
    }

    MPI_Finalize();
    return 0;
}
```

### `src/observables.cpp` (70 lines)

```cpp
#include "md/observables.hpp"

#include <cmath>

#include "md/constants.hpp"

namespace md {

double computeLocalKineticEnergy(const System& sys, double mass) {
    double eKin = 0.0;
    for (int i = 0; i < 3 * sys.localN; ++i) {
        eKin += sys.vel[i] * sys.vel[i];
    }
    return 0.5 * mass * eKin;
}

double computeTemperature(double eKinTotal, int N) {
    int nDof = 3 * (N - 1);  // degrees of freedom after CoM removal
    return (2.0 * eKinTotal) / (nDof * constants::kB);
}

void accumulateGR(const std::vector<double>& posGlobal, int N, double L, int offset, int localN,
                  double dr, double rMax, std::vector<double>& histogram) {
    int nBins = static_cast<int>(histogram.size());
    const double invL = 1.0 / L;  // constant per call

    for (int i = offset; i < offset + localN; ++i) {
        for (int j = i + 1; j < N; ++j) {
            double dx = posGlobal[3 * i + 0] - posGlobal[3 * j + 0];
            double dy = posGlobal[3 * i + 1] - posGlobal[3 * j + 1];
            double dz = posGlobal[3 * i + 2] - posGlobal[3 * j + 2];

            // Minimum image convention
            dx -= L * std::round(dx * invL);
            dy -= L * std::round(dy * invL);
            dz -= L * std::round(dz * invL);

            double r = std::sqrt(dx * dx + dy * dy + dz * dz);
            if (r < rMax) {
                int bin = static_cast<int>(r / dr);
                if (bin < nBins) {
                    histogram[bin] += 1.0;
                }
            }
        }
    }
}

void normaliseGR(std::vector<double>& histogram, double dr, int N, double L, int nFrames) {
    double V = L * L * L;
    // Finite-N correction: reference density is (N-1)/V because a particle cannot pair with itself.
    // This differs from the N/V convention in some textbooks; the report must state this choice
    // explicitly.
    double rho = static_cast<double>(N - 1) / V;

    for (int bin = 0; bin < static_cast<int>(histogram.size()); ++bin) {
        double rLow = bin * dr;
        double rInner = rLow;
        double rOuter = rLow + dr;
        double shellVol =
            (4.0 / 3.0) * M_PI * (rOuter * rOuter * rOuter - rInner * rInner * rInner);

        // Factor of 2: unordered pairs (i<j) → ordered pair convention
        if (shellVol > 0.0 && nFrames > 0) {
            histogram[bin] *= 2.0 / (rho * static_cast<double>(N) * shellVol * nFrames);
        }
    }
}

}  // namespace md
```

### `src/potentials/harmonic.cpp` (37 lines)

```cpp
/**
 * @file harmonic.cpp
 * @brief Harmonic Oscillator acceleration/energy kernel.
 *
 * sys.acc stores acceleration (not force).
 * a_i = -omega^2 * x_i  (each component independently)
 * V_i = 0.5 * m * omega^2 * x_i^2
 *
 * This is a non-interacting potential: particles do not see each other.
 * The MPI_Allgatherv collective is bypassed entirely in HO mode.
 * Validation runs should use N=1. Code supports N independent copies.
 */

#include "md/potentials.hpp"

namespace md {

void computeHOForces(System& sys, const std::vector<double>& /*posGlobal*/, double& localPE,
                     double omega, double mass) {
    double omega2 = omega * omega;
    localPE = 0.0;

    for (int i = 0; i < sys.localN; ++i) {
        for (int d = 0; d < 3; ++d) {
            int idx = 3 * i + d;
            double x = sys.pos[idx];

            // Acceleration = F/m = -omega^2 * x
            sys.acc[idx] = -omega2 * x;

            // Potential energy: V = 0.5 * m * omega^2 * x^2
            localPE += 0.5 * mass * omega2 * x * x;
        }
    }
}

}  // namespace md
```

### `src/potentials/lennard_jones.cpp` (104 lines)

```cpp
/**
 * @file lennard_jones.cpp
 * @brief Lennard-Jones force and potential energy kernel.
 *
 * Implements U(r) = 4*eps*[(sigma/r)^12 - (sigma/r)^6] via
 * invR2 → invR6 → invR12 (no pow, no sqrt in force loop).
 *
 * Hard cutoff at rcut = 2.25*sigma with round-based minimum image convention.
 * PE is summed over all j != i (both directions) and multiplied by 0.5
 * after the loop to correct for double-counting.
 */

#include <cmath>

#include "md/constants.hpp"
#include "md/mic.hpp"
#include "md/potentials.hpp"

namespace md {

void computeLJForces(System& sys, const std::vector<double>& posGlobal, double& localPE,
                     double mass) {
    const double L = sys.L;
    const int N = sys.N;
    const int offset = sys.offset;
    const int localN = sys.localN;

    // Pre-computed constants (from constants.hpp)
    const double s6 = constants::sigma6;
    const double s12 = constants::sigma12;
    const double fe = constants::four_eps;
    const double te = constants::twentyfour_eps;
    const double rc2 = constants::rcut2;
    const double tiny = 1e-30 * constants::sigma2;
    const double invMass = 1.0 / mass;

    // Zero local forces and PE
    for (int i = 0; i < 3 * localN; ++i) {
        sys.acc[i] = 0.0;
    }
    localPE = 0.0;
    for (int i = 0; i < localN; ++i) {
        int gi = offset + i;  // global index

        // Local particle from sys.pos; remote particles from posGlobal
        double xi = sys.pos[3 * i + 0];
        double yi = sys.pos[3 * i + 1];
        double zi = sys.pos[3 * i + 2];

        double fx = 0.0, fy = 0.0, fz = 0.0;
        double pei = 0.0;

        for (int j = 0; j < N; ++j) {
            // Skip self-interaction to avoid r^2 = 0 singularity
            if (j == gi)
                continue;

            double dx = xi - posGlobal[3 * j + 0];
            double dy = yi - posGlobal[3 * j + 1];
            double dz = zi - posGlobal[3 * j + 2];

            // Minimum image convention
            dx = md::applyMIC(dx, L);
            dy = md::applyMIC(dy, L);
            dz = md::applyMIC(dz, L);

            double r2 = dx * dx + dy * dy + dz * dz;

            if (r2 < tiny)
                continue;

            if (r2 >= rc2)
                continue;  // hard cutoff

            double invR2 = 1.0 / r2;
            double invR6 = invR2 * invR2 * invR2;
            double invR12 = invR6 * invR6;

            // Potential energy (accumulate unconditionally — multiply by 0.5 after loop)
            pei += fe * (s12 * invR12 - s6 * invR6);

            // Force scalar: f/r = 24*eps/r^2 * [2*(sigma/r)^12 - (sigma/r)^6]
            double fScalar = te * invR2 * (2.0 * s12 * invR12 - s6 * invR6);

            fx += fScalar * dx;
            fy += fScalar * dy;
            fz += fScalar * dz;
        }

        // Store as acceleration: a = F/m
        sys.acc[3 * i + 0] = fx * invMass;
        sys.acc[3 * i + 1] = fy * invMass;
        sys.acc[3 * i + 2] = fz * invMass;

        localPE += pei;
    }

    // Each rank loops its local particles i against all N particles j≠i, accumulating V(r_ij).
    // Across all ranks, every ordered pair (i,j) with j≠i is visited exactly once. Since V(r_ij) =
    // V(r_ji), this double-counts each unordered pair, so halve.
    localPE *= 0.5;
}

}  // namespace md
```

### `tests/test_runner.cpp` (33 lines)

```cpp
/**
 * @file test_runner.cpp
 * @brief Homebrew unit test runner (no third-party libraries).
 *
 * Calls all test functions and exits with code 0 if all pass,
 * non-zero if any fail. Intended to be invoked via `make test`.
 */

#include <cstdio>
#include <cstdlib>

// Test function declarations (defined in separate .cpp files)
extern int testMIC();
extern int testForce();

int main() {
    std::printf("=== MD Unit Tests ===\n");

    int totalFailures = 0;

    totalFailures += testMIC();
    totalFailures += testForce();

    std::printf("=====================\n");

    if (totalFailures == 0) {
        std::printf("ALL TESTS PASSED\n");
        return 0;
    } else {
        std::printf("TOTAL FAILURES: %d\n", totalFailures);
        return 1;
    }
}
```

### `tests/test_mic.cpp` (117 lines)

```cpp
/**
 * @file test_mic.cpp
 * @brief Unit tests for the Minimum Image Convention.
 *
 * Tests that the minimum image convention correctly wraps
 * inter-particle displacements to (-L/2, +L/2], with tie behavior
 * from std::round at +/-L/2. Also tests that
 * the geometric safety condition r_c < L/2 holds for the Rahman
 * state point (r_c = 2.25*sigma < L/2 ≈ 5.115*sigma).
 */

#include <cmath>
#include <cstdio>
#include <cstdlib>

#include "md/constants.hpp"
#include "md/mic.hpp"

int testMIC() {
    int failures = 0;
    double L = 10.0;
    double tol = 1e-14;

    // Test 1: displacement within [-L/2, L/2) should be unchanged
    {
        double dx = 3.0;
        double result = md::applyMIC(dx, L);
        if (std::abs(result - 3.0) > tol) {
            std::printf("FAIL: MIC unchanged test: got %e, expected 3.0\n", result);
            ++failures;
        }
    }

    // Test 2: displacement > L/2 should wrap by -L
    {
        double dx = 7.0;  // > 5.0 = L/2
        double result = md::applyMIC(dx, L);
        if (std::abs(result - (-3.0)) > tol) {
            std::printf("FAIL: MIC positive wrap: got %e, expected -3.0\n", result);
            ++failures;
        }
    }

    // Test 3: displacement < -L/2 should wrap by +L
    {
        double dx = -6.0;  // < -5.0
        double result = md::applyMIC(dx, L);
        if (std::abs(result - 4.0) > tol) {
            std::printf("FAIL: MIC negative wrap: got %e, expected 4.0\n", result);
            ++failures;
        }
    }

    // Test 4: displacement at exactly L/2 boundary
    {
        double dx = 5.0;  // == L/2 (std::round(0.5) is 1.0, wraps to -5.0)
        double result = md::applyMIC(dx, L);
        if (std::abs(result - (-5.0)) > tol) {
            std::printf("FAIL: MIC boundary L/2: got %e, expected -5.0\n", result);
            ++failures;
        }
    }

    // Test 5: displacement at exactly -L/2 boundary
    {
        double dx = -5.0;  // == -L/2 (std::round(-0.5) is -1.0, wraps to 5.0)
        double result = md::applyMIC(dx, L);
        if (std::abs(result - 5.0) > tol) {
            std::printf("FAIL: MIC boundary -L/2: got %e, expected 5.0\n", result);
            ++failures;
        }
    }

    // Test 6: zero displacement
    {
        double dx = 0.0;
        double result = md::applyMIC(dx, L);
        if (std::abs(result) > tol) {
            std::printf("FAIL: MIC zero: got %e, expected 0.0\n", result);
            ++failures;
        }
    }

    // Test 7: Geometric safety condition: r_c = 2.25*sigma < L/2
    // For Rahman: L = 10.229*sigma, so L/2 = 5.1145*sigma
    // r_c = 2.25*sigma < 5.1145*sigma ✓
    {
        double rcut_sigma = md::constants::rcut_sigma;             // 2.25
        double halfL_sigma = md::constants::L_sigma_rahman / 2.0;  // ~5.1145
        if (rcut_sigma >= halfL_sigma) {
            std::printf("FAIL: Geometric safety: rcut/sigma=%.4f >= L/(2*sigma)=%.4f\n", rcut_sigma,
                        halfL_sigma);
            ++failures;
        }
    }

    // Test 8: 3D MIC with all components wrapping
    {
        double dx = 8.0, dy = -7.0, dz = 0.5;
        dx = md::applyMIC(dx, L);
        dy = md::applyMIC(dy, L);
        dz = md::applyMIC(dz, L);

        if (std::abs(dx - (-2.0)) > tol || std::abs(dy - 3.0) > tol || std::abs(dz - 0.5) > tol) {
            std::printf("FAIL: 3D MIC: got (%e, %e, %e), expected (-2, 3, 0.5)\n", dx, dy, dz);
            ++failures;
        }
    }

    if (failures == 0) {
        std::printf("  MIC tests: ALL PASSED\n");
    } else {
        std::printf("  MIC tests: %d FAILED\n", failures);
    }

    return failures;
}
```

### `tests/test_force.cpp` (198 lines)

```cpp
/**
 * @file test_force.cpp
 * @brief Unit tests for the LJ force kernel and position wrapping.
 *
 * Test 1: Two particles at r = 2^(1/6)*sigma (LJ potential minimum).
 *         At this separation the net force is zero. Assert |F| < 1e-12.
 *
 * Test 2: Verify position wrapping correctly maps coordinates to [0, L).
 *
 * Test 3: LJ force sign check — particles closer than equilibrium
 *         should repel, further should attract.
 */

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <vector>

#include "md/constants.hpp"
#include "md/potentials.hpp"
#include "md/system.hpp"

int testForce() {
    int failures = 0;

    // Test 1: LJ force at potential minimum r = 2^(1/6)*sigma
    {
        const double sigma = md::constants::sigma;
        const double rMin = std::pow(2.0, 1.0 / 6.0) * sigma;
        const double mass = md::constants::mass;
        const double L = 10.229 * sigma;  // Rahman box

        // Two particles separated by r_min along x-axis
        int N = 2;
        md::System sys;
        sys.init(N, 0, N, L);

        sys.pos[0] = 0.0;
        sys.pos[1] = 0.0;
        sys.pos[2] = 0.0;
        sys.pos[3] = rMin;
        sys.pos[4] = 0.0;
        sys.pos[5] = 0.0;

        // Global position buffer (same as local for P=1 serial test)
        std::vector<double> posGlobal(sys.pos.begin(), sys.pos.end());

        double localPE = 0.0;
        md::computeLJForces(sys, posGlobal, localPE, mass);

        // Check that force on particle 0 is negligible
        double fx0 = sys.acc[0] * mass;  // convert acceleration back to force
        double fy0 = sys.acc[1] * mass;
        double fz0 = sys.acc[2] * mass;
        double fMag0 = std::sqrt(fx0 * fx0 + fy0 * fy0 + fz0 * fz0);

        if (fMag0 > 1e-12) {
            std::printf("FAIL: LJ force at r_min: |F| = %e (expected < 1e-12)\n", fMag0);
            ++failures;
        }

        // Also check particle 1 force (should be equal and opposite, so also ~0)
        double fx1 = sys.acc[3] * mass;
        double fy1 = sys.acc[4] * mass;
        double fz1 = sys.acc[5] * mass;
        double fMag1 = std::sqrt(fx1 * fx1 + fy1 * fy1 + fz1 * fz1);

        if (fMag1 > 1e-12) {
            std::printf("FAIL: LJ force at r_min (particle 1): |F| = %e (expected < 1e-12)\n",
                        fMag1);
            ++failures;
        }

        // Check PE: at r_min, V = -epsilon
        // Each particle sees the other, so localPE = 2 * V * 0.5 = V = -epsilon
        // (since we loop both i->j and j->i, multiply by 0.5)
        double expectedPE = -md::constants::epsilon;
        double peRelErr = std::abs(localPE - expectedPE) / std::abs(expectedPE);
        if (peRelErr > 1e-10) {
            std::printf("FAIL: LJ PE at r_min: got %e, expected %e (rel err %e)\n", localPE,
                        expectedPE, peRelErr);
            ++failures;
        }
    }

    // Test 2: Position wrapping
    {
        double L = 10.0;
        md::System sys;
        sys.init(3, 0, 3, L);

        // Set positions outside [0, L)
        sys.pos[0] = 15.0;    // should wrap to 5.0
        sys.pos[1] = -3.0;    // should wrap to 7.0
        sys.pos[2] = 10.0;    // should wrap to 0.0
        sys.pos[3] = 0.0;     // should stay 0.0
        sys.pos[4] = 9.999;   // should stay 9.999
        sys.pos[5] = 25.5;    // should wrap to 5.5
        sys.pos[6] = -10.5;   // should wrap to 9.5
        sys.pos[7] = 100.0;   // should wrap to 0.0
        sys.pos[8] = -0.001;  // should wrap to 9.999

        sys.wrapPositions();

        struct WrapTest {
            int idx;
            double expected;
            const char* desc;
        };

        WrapTest tests[] = {
            {0, 5.0, "15.0 -> 5.0"},  {1, 7.0, "-3.0 -> 7.0"},      {2, 0.0, "10.0 -> 0.0"},
            {3, 0.0, "0.0 -> 0.0"},   {4, 9.999, "9.999 -> 9.999"}, {5, 5.5, "25.5 -> 5.5"},
            {6, 9.5, "-10.5 -> 9.5"}, {7, 0.0, "100.0 -> 0.0"},     {8, 9.999, "-0.001 -> 9.999"},
        };

        for (const auto& t : tests) {
            double val = sys.pos[t.idx];
            if (std::abs(val - t.expected) > 1e-10) {
                std::printf("FAIL: Wrap [%s]: got %e, expected %e\n", t.desc, val, t.expected);
                ++failures;
            }
            // Also check value is in [0, L)
            if (val < 0.0 || val >= L) {
                std::printf("FAIL: Wrap [%s]: result %e not in [0, %f)\n", t.desc, val, L);
                ++failures;
            }
        }
    }

    // Test 3: LJ force sign check
    {
        const double sigma = md::constants::sigma;
        const double mass = md::constants::mass;
        const double L = 10.229 * sigma;

        // Two particles closer than equilibrium: should REPEL (force pushes apart)
        {
            double r = 1.0 * sigma;  // < 2^(1/6)*sigma
            int N = 2;
            md::System sys;
            sys.init(N, 0, N, L);

            sys.pos[0] = 0.0;
            sys.pos[1] = 0.0;
            sys.pos[2] = 0.0;
            sys.pos[3] = r;
            sys.pos[4] = 0.0;
            sys.pos[5] = 0.0;

            std::vector<double> posGlobal(sys.pos.begin(), sys.pos.end());
            double pe = 0.0;
            md::computeLJForces(sys, posGlobal, pe, mass);

            // Particle 0 at x=0:  force on it should be in -x direction (pushed away from particle
            // 1)
            double ax0 = sys.acc[0];
            if (ax0 >= 0.0) {
                std::printf("FAIL: LJ repulsion: F_x on particle 0 should be < 0, got %e\n", ax0);
                ++failures;
            }
        }

        // Two particles further than equilibrium: should ATTRACT
        {
            double r = 1.5 * sigma;  // > 2^(1/6)*sigma but < rcut
            int N = 2;
            md::System sys;
            sys.init(N, 0, N, L);

            sys.pos[0] = 0.0;
            sys.pos[1] = 0.0;
            sys.pos[2] = 0.0;
            sys.pos[3] = r;
            sys.pos[4] = 0.0;
            sys.pos[5] = 0.0;

            std::vector<double> posGlobal(sys.pos.begin(), sys.pos.end());
            double pe = 0.0;
            md::computeLJForces(sys, posGlobal, pe, mass);

            // Particle 0 at x=0:  force should be in +x direction (attracted toward particle 1)
            double ax0 = sys.acc[0];
            if (ax0 <= 0.0) {
                std::printf("FAIL: LJ attraction: F_x on particle 0 should be > 0, got %e\n", ax0);
                ++failures;
            }
        }
    }

    if (failures == 0) {
        std::printf("  Force/Wrapping tests: ALL PASSED\n");
    } else {
        std::printf("  Force/Wrapping tests: %d FAILED\n", failures);
    }

    return failures;
}
```

### `scripts/make_results.sh` (13 lines)

```sh
#!/bin/bash
# Thin compatibility wrapper.
# Use --generate-data to run production data generation before writing results.

set -euo pipefail
cd "$(dirname "$0")/.."

if [ "${1:-}" = "--generate-data" ]; then
  shift
  bash scripts/run_all_data.sh "$@"
fi

bash ai/make_results.sh
```

### `scripts/run_all_data.sh` (263 lines)

```sh
#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# run_all_data.sh — Generate ALL production data for the report
#
# Designed for shared HPC clusters (cerberus1). Uses median-of-20
# paired (wall, comm) repetitions for scaling benchmarks to filter contention noise.
# ──────────────────────────────────────────────────────────────────

set -euo pipefail

SOLVER="./md_solver"
OUTDIR="out"
SKIP_SCALING=0
STRONG_STEPS=200
# Use longer runs for size scaling so fixed overhead is less dominant at small N.
SIZE_STEPS=2000

LJ_DT="1e-14"
LJ_TARGET_T=94.4
LJ_BRIEF_EQUIL=50
LJ_BRIEF_PROD_STEPS=100
LJ_BRIEF_FRAMES=$((LJ_BRIEF_PROD_STEPS + 1))
LJ_RDF_EQUIL=$LJ_BRIEF_EQUIL
LJ_RDF_PROD_STEPS=20000
LJ_RDF_FRAMES=$((LJ_RDF_PROD_STEPS + 1))
LJ_GR_DISCARD_STEPS=200
LJ_GR_SAMPLE_EVERY=5
for arg in "$@"; do
  [ "$arg" = "--skip-scaling" ] && SKIP_SCALING=1
done

rm -f "$OUTDIR/manifest.json"
mkdir -p "$OUTDIR/runs"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "=========================================="
echo "  FULL DATA GENERATION — $(date)"
echo "=========================================="

# Helper: given parallel arrays of wall and comm times, pick the
# median by wall time and return the paired (wall, comm).
pick_median_pair() {
    local walls=($1)
    local comms=($2)
    local n=${#walls[@]}
    local tmpfile
    tmpfile=$(mktemp)
    for i in $(seq 0 $((n-1))); do
        echo "${walls[$i]} ${comms[$i]}"
    done | sort -n -k1 > "$tmpfile"
    local mid=$(( (n - 1) / 2 ))
    local line
    line=$(sed -n "$((mid+1))p" "$tmpfile")
    rm -f "$tmpfile"
    echo "$line"
}

# ── 0. Parallel Consistency Check ──
echo ""
echo "=== PARALLEL CONSISTENCY CHECK ==="
D1="$OUTDIR/runs/lj_N108_P1_test_${TIMESTAMP}"
D2="$OUTDIR/runs/lj_N108_P2_test_${TIMESTAMP}"
mkdir -p "$D1" "$D2"
mpirun -np 1 $SOLVER --mode lj --integrator verlet --N 108 \
    --equilibration-steps 0 --production-steps 10 \
    --target-temperature $LJ_TARGET_T --final-rescale-before-production --outdir "$D1"
mpirun -np 2 $SOLVER --mode lj --integrator verlet --N 108 \
    --equilibration-steps 0 --production-steps 10 \
    --target-temperature $LJ_TARGET_T --final-rescale-before-production --outdir "$D2"
if python3 scripts/check_tolerance.py "$D1/lj_verlet.csv" "$D2/lj_verlet.csv" > /dev/null 2>&1; then
    echo "  P=1 vs P=2 data: MATCH ✅"
else
    echo "  P=1 vs P=2 data: MISMATCH ❌"
fi

echo ""
echo "=== RDF PARALLEL CONSISTENCY CHECK ==="
DGR1="$OUTDIR/runs/lj_gr_N108_P1_test_${TIMESTAMP}"
DGR2="$OUTDIR/runs/lj_gr_N108_P2_test_${TIMESTAMP}"
mkdir -p "$DGR1" "$DGR2"
mpirun -np 1 $SOLVER --mode lj --integrator verlet --N 108 --dt 1e-14 \
    --equilibration-steps 20 --production-steps 400 \
    --target-temperature $LJ_TARGET_T --final-rescale-before-production \
    --gr --gr-discard-steps 20 --gr-sample-every 2 --outdir "$DGR1" > /dev/null
mpirun -np 2 $SOLVER --mode lj --integrator verlet --N 108 --dt 1e-14 \
    --equilibration-steps 20 --production-steps 400 \
    --target-temperature $LJ_TARGET_T --final-rescale-before-production \
    --gr --gr-discard-steps 20 --gr-sample-every 2 --outdir "$DGR2" > /dev/null
if python3 scripts/check_gr_tolerance.py "$DGR1/gr.csv" "$DGR2/gr.csv" > /dev/null 2>&1; then
    echo "  g(r) P=1 vs P=2 data: MATCH ✅"
else
    echo "  g(r) P=1 vs P=2 data: MISMATCH ❌"
fi

# ── 1. Results 1: HO Convergence ──
echo ""
echo "=== RESULTS 1: HO CONVERGENCE ==="
DT_LIST="1.0:10 0.5:20 0.1:100 0.05:200 0.01:1000 0.005:2000 0.001:10000 0.0005:20000"
for INT in euler verlet rk4; do
    for ENTRY in $DT_LIST; do
        DT=$(echo $ENTRY | cut -d: -f1)
        STEPS=$(echo $ENTRY | cut -d: -f2)
        RUNDIR="$OUTDIR/runs/ho_N1_${INT}_dt${DT}_${TIMESTAMP}"
        mkdir -p "$RUNDIR"
        # Exam validation requires HO to run with N=1.
        mpirun -np 1 $SOLVER --mode ho --integrator $INT --N 1 --steps $STEPS --dt $DT --outdir "$RUNDIR" > /dev/null
        DSTFILE="$RUNDIR/ho_${INT}.csv"
        if [ -s "$DSTFILE" ]; then
            python3 scripts/append_manifest.py "ho_convergence.${INT}_dt${DT//./_}" "$DSTFILE"
            echo "  $INT dt=$DT steps=$STEPS -> $DSTFILE ✅"
        else
            echo "  $INT dt=$DT steps=$STEPS -> FAILED"
        fi
    done
done

# ── 2. Results 2: LJ Brief ──
echo ""
echo "=== RESULTS 2: LJ BRIEF ==="
echo "  Convention: startup is configured by --equilibration-steps, production by --production-steps."
echo "  CSV output reports production trajectory only: step 0 is the production initial frame."

# Brief run (required by brief): exactly 100-step NVE production at dt=1e-14 s.
RUNDIR_BRIEF_V="$OUTDIR/runs/lj_brief_N864_P4_verlet_prod${LJ_BRIEF_PROD_STEPS}_eq${LJ_BRIEF_EQUIL}_dt1e-14_${TIMESTAMP}"
mkdir -p "$RUNDIR_BRIEF_V"
echo "  Brief (required) Verlet: equilibration=${LJ_BRIEF_EQUIL}, production=${LJ_BRIEF_PROD_STEPS}, frames=${LJ_BRIEF_FRAMES}, dt=${LJ_DT}, target_T=${LJ_TARGET_T} K..."
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 \
    --dt $LJ_DT --target-temperature $LJ_TARGET_T \
    --equilibration-steps $LJ_BRIEF_EQUIL \
    --production-steps $LJ_BRIEF_PROD_STEPS \
    --final-rescale-before-production \
    --outdir "$RUNDIR_BRIEF_V" > /dev/null
if [ -s "$RUNDIR_BRIEF_V/lj_verlet.csv" ]; then
    python3 scripts/append_manifest.py "lj_brief.verlet" "$RUNDIR_BRIEF_V/lj_verlet.csv"
    echo "  -> brief Verlet output saved to manifest ✅"
fi

RUNDIR_BRIEF_E="$OUTDIR/runs/lj_brief_N864_P4_euler_prod${LJ_BRIEF_PROD_STEPS}_eq${LJ_BRIEF_EQUIL}_dt1e-14_${TIMESTAMP}"
mkdir -p "$RUNDIR_BRIEF_E"
echo "  Brief (required) Euler: equilibration=${LJ_BRIEF_EQUIL}, production=${LJ_BRIEF_PROD_STEPS}, frames=${LJ_BRIEF_FRAMES}, dt=${LJ_DT}, target_T=${LJ_TARGET_T} K..."
mpirun -np 4 $SOLVER --mode lj --integrator euler --N 864 \
    --dt $LJ_DT --target-temperature $LJ_TARGET_T \
    --equilibration-steps $LJ_BRIEF_EQUIL \
    --production-steps $LJ_BRIEF_PROD_STEPS \
    --final-rescale-before-production \
    --outdir "$RUNDIR_BRIEF_E" > /dev/null
if [ -s "$RUNDIR_BRIEF_E/lj_euler.csv" ]; then
    python3 scripts/append_manifest.py "lj_brief.euler" "$RUNDIR_BRIEF_E/lj_euler.csv"
    echo "  -> brief Euler output saved to manifest ✅"
fi

# ── 3. g(r) Production Run (long) ──
echo ""
echo "=== g(r) PRODUCTION RUN (LONG) ==="
echo "  RDF long run: equilibration=${LJ_RDF_EQUIL}, production=${LJ_RDF_PROD_STEPS}, frames=${LJ_RDF_FRAMES}, discard_steps=${LJ_GR_DISCARD_STEPS}, sample_every=${LJ_GR_SAMPLE_EVERY}"
RUNDIR_GR="$OUTDIR/runs/lj_rdf_N864_P4_verlet_prod${LJ_RDF_PROD_STEPS}_eq${LJ_RDF_EQUIL}_dt1e-14_${TIMESTAMP}"
mkdir -p "$RUNDIR_GR"
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 \
    --dt $LJ_DT \
    --target-temperature $LJ_TARGET_T \
    --equilibration-steps $LJ_RDF_EQUIL \
    --production-steps $LJ_RDF_PROD_STEPS \
    --final-rescale-before-production \
    --gr \
    --gr-discard-steps $LJ_GR_DISCARD_STEPS \
    --gr-sample-every $LJ_GR_SAMPLE_EVERY \
    --outdir "$RUNDIR_GR" > /dev/null
if [ -s "$RUNDIR_GR/gr.csv" ]; then
    python3 scripts/append_manifest.py "lj_rdf.verlet_long" "$RUNDIR_GR/gr.csv"
    python3 scripts/append_manifest.py "lj_rdf.verlet_long_energy" "$RUNDIR_GR/lj_verlet.csv"
    echo "  g(r) done, output saved to manifest ✅"
else
    echo "  g(r) FAILED ❌"
fi

# ── 4. Strong/Size Scaling ──
if [ "$SKIP_SCALING" = "1" ]; then
  echo ""
  echo "=== SKIPPING SCALING (--skip-scaling) ==="
  # Re-register existing files in manifest if they exist
  [ -f "$OUTDIR/scaling_strong.csv" ] && python3 scripts/append_manifest.py "scaling.strong" "$OUTDIR/scaling_strong.csv"
  [ -f "$OUTDIR/scaling_size.csv" ]   && python3 scripts/append_manifest.py "scaling.size"   "$OUTDIR/scaling_size.csv"
else
echo ""
echo "=== RESULTS 3: STRONG SCALING (20 reps, N=2048, ${STRONG_STEPS} steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_strong.csv"
python3 scripts/append_manifest.py "scaling.strong" "$OUTDIR/scaling_strong.csv"

REPS=20
for P in 1 2 4 8 16 24 32; do
    WALLS=""
    COMMS=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np $P $SOLVER --mode lj --integrator verlet --N 2048 --steps $STRONG_STEPS --timing 2>/dev/null)
        W=$(awk '/Wall time/ {print $3; exit}' <<< "$OUTPUT")
        C=$(awk '/Comm time/ {print $3; exit}' <<< "$OUTPUT")
        [ -z "$C" ] && C="0.0"
        C=$(awk -v w="$W" -v c="$C" 'BEGIN{if (c > w) print w; else print c}')
        WALLS="$WALLS $W"
        COMMS="$COMMS $C"
        echo "    P=$P rep=$REP wall=$W comm=$C"
    done
    PAIR=$(pick_median_pair "$WALLS" "$COMMS")
    MEDIAN_W=$(echo "$PAIR" | awk '{print $1}')
    MEDIAN_C=$(echo "$PAIR" | awk '{print $2}')
    echo "$P,2048,$MEDIAN_W,$MEDIAN_C" >> "$OUTDIR/scaling_strong.csv"
    echo "  >> P=$P MEDIAN: wall=$MEDIAN_W comm=$MEDIAN_C"
done

# ── 5. Size Scaling (median of 20 paired samples) ──
echo ""
echo "=== RESULTS 3: SIZE SCALING (20 reps, P=16, ${SIZE_STEPS} steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_size.csv"
python3 scripts/append_manifest.py "scaling.size" "$OUTDIR/scaling_size.csv"

for N in 108 256 500 864 1372 2048; do
    WALLS=""
    COMMS=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np 16 $SOLVER --mode lj --integrator verlet --N $N --steps $SIZE_STEPS --timing 2>/dev/null)
        W=$(awk '/Wall time/ {print $3; exit}' <<< "$OUTPUT")
        C=$(awk '/Comm time/ {print $3; exit}' <<< "$OUTPUT")
        [ -z "$C" ] && C="0.0"
        C=$(awk -v w="$W" -v c="$C" 'BEGIN{if (c > w) print w; else print c}')
        WALLS="$WALLS $W"
        COMMS="$COMMS $C"
        echo "    N=$N rep=$REP wall=$W comm=$C"
    done
    PAIR=$(pick_median_pair "$WALLS" "$COMMS")
    MEDIAN_W=$(echo "$PAIR" | awk '{print $1}')
    MEDIAN_C=$(echo "$PAIR" | awk '{print $2}')
    echo "16,$N,$MEDIAN_W,$MEDIAN_C" >> "$OUTDIR/scaling_size.csv"
    echo "  >> N=$N MEDIAN: wall=$MEDIAN_W comm=$MEDIAN_C"
done

fi  # end --skip-scaling check

{
  echo "hostname: $(hostname)"
  if command -v lscpu &>/dev/null; then
    echo "cpu: $(lscpu | grep 'Model name' | sed 's/.*: *//')"
  else
    echo "cpu: $(head -1 /proc/cpuinfo | sed 's/.*: *//')"
  fi
  echo "compiler: $(mpicxx --version | head -1)"
  echo "mpi: $(mpirun --version | head -1)"
  echo "date: $(date -Iseconds)"
} > "$OUTDIR/scaling_meta.txt"

# ── Validate manifest integrity before downstream plotting/analysis ──
if [ "$SKIP_SCALING" = "1" ]; then
  python3 scripts/validate_manifest.py --skip-scaling
else
  python3 scripts/validate_manifest.py
fi

# ── Summary ──
echo ""
echo "=========================================="
echo "  ALL DONE — $(date)"
echo "=========================================="
echo "Manifest written to: $OUTDIR/manifest.json"
```

### `scripts/run_results.sh` (12 lines)

```sh
#!/bin/bash
# Run end-to-end Results data generation and plotting.
# Usage:
#   bash scripts/run_results.sh [--skip-scaling]

set -euo pipefail
cd "$(dirname "$0")/.."

bash scripts/run_all_data.sh "$@"
python3 scripts/plot_ho.py
python3 scripts/plot_lj.py
python3 scripts/plot_scaling.py
```

### `scripts/run_scaling.sh` (115 lines)

```sh
#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# run_scaling.sh — Batch scaling benchmarks with comm breakdown
#
# Uses PAIRED observations: for each rep, records (wall, comm) as a pair.
# The median is selected by wall time, and the comm from THAT SAME rep
# is reported. This guarantees comm <= wall for every data point.
#
# Usage:
#   bash scripts/run_scaling.sh
#
# Produces:
#   out/scaling_strong.csv   (P,N,wall_s,comm_s)
#   out/scaling_size.csv     (P,N,wall_s,comm_s)
# ──────────────────────────────────────────────────────────────────

set -euo pipefail

SOLVER="./md_solver"
OUTDIR="out"
STRONG_STEPS=200
SIZE_STEPS=2000
INTEGRATOR="verlet"
REPS=20

mkdir -p "$OUTDIR"

# Helper: given parallel arrays of wall and comm times, pick the
# median by wall time and return the paired (wall, comm).
# Usage: pick_median_pair "w1 ... wn" "c1 ... cn"
# Prints: wall_median comm_from_same_rep
pick_median_pair() {
    local walls=($1)
    local comms=($2)
    local n=${#walls[@]}

    # Create index-sorted-by-wall array using a temp file
    local tmpfile
    tmpfile=$(mktemp)
    for i in $(seq 0 $((n-1))); do
        echo "${walls[$i]} ${comms[$i]}"
    done | sort -n -k1 > "$tmpfile"

    # Pick the middle row (0-indexed: row (n-1)/2 for odd n)
    local mid=$(( (n - 1) / 2 ))
    local line
    line=$(sed -n "$((mid+1))p" "$tmpfile")
    rm -f "$tmpfile"

    echo "$line"
}

# ─── Strong Scaling: N=2048, vary P ──────────────────────────────
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_strong.csv"

N_STRONG=2048
for P in 1 2 4 8 16 24 32; do
    WALLS=""
    COMMS=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun --oversubscribe -np "$P" "$SOLVER" \
            --mode lj --integrator "$INTEGRATOR" \
            --N "$N_STRONG" --steps "$STRONG_STEPS" --timing 2>&1)

        WALL=$(awk '/Wall time/ {print $3; exit}' <<< "$OUTPUT")
        COMM=$(awk '/Comm time/ {print $3; exit}' <<< "$OUTPUT")
        # P=1 has no comm line
        if [ -z "$COMM" ]; then COMM="0.000000"; fi
        COMM=$(awk -v w="$WALL" -v c="$COMM" 'BEGIN{if (c > w) print w; else print c}')

        WALLS="$WALLS $WALL"
        COMMS="$COMMS $COMM"
        echo "  P=$P rep=$REP wall=$WALL comm=$COMM"
    done

    PAIR=$(pick_median_pair "$WALLS" "$COMMS")
    MED_WALL=$(echo "$PAIR" | awk '{print $1}')
    MED_COMM=$(echo "$PAIR" | awk '{print $2}')
    echo "$P,$N_STRONG,$MED_WALL,$MED_COMM" >> "$OUTDIR/scaling_strong.csv"
    echo ">> P=$P MEDIAN: wall=$MED_WALL comm=$MED_COMM"
done

echo ""

# ─── Size Scaling: P=16, vary N ──────────────────────────────────
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_size.csv"

P_SIZE=16
for N in 108 256 500 864 1372 2048; do
    WALLS=""
    COMMS=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun --oversubscribe -np "$P_SIZE" "$SOLVER" \
            --mode lj --integrator "$INTEGRATOR" \
            --N "$N" --steps "$SIZE_STEPS" --timing 2>&1)

        WALL=$(awk '/Wall time/ {print $3; exit}' <<< "$OUTPUT")
        COMM=$(awk '/Comm time/ {print $3; exit}' <<< "$OUTPUT")
        if [ -z "$COMM" ]; then COMM="0.000000"; fi
        COMM=$(awk -v w="$WALL" -v c="$COMM" 'BEGIN{if (c > w) print w; else print c}')

        WALLS="$WALLS $WALL"
        COMMS="$COMMS $COMM"
        echo "  N=$N rep=$REP wall=$WALL comm=$COMM"
    done

    PAIR=$(pick_median_pair "$WALLS" "$COMMS")
    MED_WALL=$(echo "$PAIR" | awk '{print $1}')
    MED_COMM=$(echo "$PAIR" | awk '{print $2}')
    echo "$P_SIZE,$N,$MED_WALL,$MED_COMM" >> "$OUTDIR/scaling_size.csv"
    echo ">> N=$N MEDIAN: wall=$MED_WALL comm=$MED_COMM"
done

echo ""
echo "Done. Results in $OUTDIR/scaling_strong.csv and $OUTDIR/scaling_size.csv"
```

### `scripts/append_manifest.py` (68 lines)

```py
#!/usr/bin/env python3
"""
append_manifest.py — Safely append/update a key path in out/manifest.json.

Usage:
  python3 scripts/append_manifest.py <key.path> <file_path>
"""

import json
import os
import sys
import tempfile
from pathlib import Path


def set_nested(data, key_path, value):
    keys = key_path.split(".")
    d = data
    for k in keys[:-1]:
        if k not in d or not isinstance(d[k], dict):
            d[k] = {}
        d = d[k]
    d[keys[-1]] = value


def load_manifest(path: Path):
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in {path}: {e}", file=sys.stderr)
        return None


def atomic_write(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def main():
    if len(sys.argv) != 3:
        print("Usage: append_manifest.py <key.path> <file_path>", file=sys.stderr)
        sys.exit(1)

    key_path = sys.argv[1]
    file_path = sys.argv[2]
    manifest_path = Path("out/manifest.json")

    data = load_manifest(manifest_path)
    if data is None:
        sys.exit(2)

    set_nested(data, key_path, file_path)
    atomic_write(manifest_path, data)


if __name__ == "__main__":
    main()
```

### `scripts/check_gr_tolerance.py` (74 lines)

```py
#!/usr/bin/env python3
"""
check_gr_tolerance.py — Compare two g(r) CSV files with tolerances.

Usage:
  python3 scripts/check_gr_tolerance.py <gr_p1.csv> <gr_p2.csv>
"""

import csv
import sys


ABS_TOL = 1e-6
REL_TOL = 1e-5


def filter_comments(handle):
    for line in handle:
        if line.strip() and not line.startswith("#"):
            yield line


def as_rows(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return list(csv.DictReader(filter_comments(f)))


def close_enough(a, b):
    diff = abs(a - b)
    if diff <= ABS_TOL:
        return True
    return diff / (abs(a) + 1e-18) <= REL_TOL


def main():
    if len(sys.argv) != 3:
        print("Usage: check_gr_tolerance.py <gr_p1.csv> <gr_p2.csv>")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]
    try:
        rows1 = as_rows(file1)
        rows2 = as_rows(file2)
    except Exception as exc:
        print(f"Error reading g(r) files: {exc}")
        sys.exit(1)

    if len(rows1) != len(rows2):
        print(f"Length mismatch: {len(rows1)} vs {len(rows2)}")
        sys.exit(1)

    for i, (r1, r2) in enumerate(zip(rows1, rows2)):
        try:
            x1 = float(r1["r_sigma"])
            x2 = float(r2["r_sigma"])
            g1 = float(r1["gr"])
            g2 = float(r2["gr"])
        except Exception as exc:
            print(f"Malformed row {i}: {exc}")
            sys.exit(1)

        if not close_enough(x1, x2):
            print(f"Mismatch at row {i}, col r_sigma: {x1} vs {x2}")
            sys.exit(1)
        if not close_enough(g1, g2):
            print(f"Mismatch at row {i}, col gr: {g1} vs {g2}")
            sys.exit(1)

    print("MATCH")
    sys.exit(0)


if __name__ == "__main__":
    main()
```

### `scripts/check_tolerance.py` (37 lines)

```py
import sys
import csv

def check_csv(file1, file2):
    try:
        def filter_comments(f):
            for line in f:
                if line.strip() and not line.startswith('#'):
                    yield line

        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            r1 = list(csv.DictReader(filter_comments(f1)))
            r2 = list(csv.DictReader(filter_comments(f2)))
            
            if len(r1) != len(r2):
                print(f"Length mismatch: {len(r1)} vs {len(r2)}")
                sys.exit(1)
                
            for i, (row1, row2) in enumerate(zip(r1, r2)):
                for col in ['E_kin', 'E_pot']:
                    v1, v2 = float(row1[col]), float(row2[col])
                    diff = abs(v1 - v2)
                    if diff > 1e-12 and diff / (abs(v1) + 1e-18) > 1e-12:
                        print(f"Mismatch at row {i}, col {col}: {v1} vs {v2}")
                        sys.exit(1)
                        
        print("MATCH")
        sys.exit(0)
    except Exception as e:
        print(f"Error checking tolerance: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: check_tolerance.py <file1.csv> <file2.csv>")
        sys.exit(1)
    check_csv(sys.argv[1], sys.argv[2])
```

### `scripts/plot_ho.py` (1468 lines)

```py
#!/usr/bin/env python3
"""
plot_ho.py — Results 1 harmonic oscillator plotting package.

Main figures (brief-facing):
  1) out/plots/results1_ho_figure1_trajectories_dt0p01.png
  2) out/plots/results1_ho_figure2_phase_space_dt0p01.png
  3) out/plots/results1_ho_figure3_small_vs_large_dt.png
  4) out/plots/results1_ho_figure4_convergence_combined.png

Optional supporting figure:
  5) out/plots/results1_ho_figure5_energy_diagnostic.png

Generated artifacts:
  - out/summary/results1/results1_ho_small_large_summary.(csv|md)
  - out/summary/results1/results1_ho_convergence_summary.(csv|md)
  - out/summary/results1/results1_ho_endpoint_values.(csv|md)
  - out/summary/results1/results1_ho_caption_notes.md

Each figure gets a JSON metadata sidecar in:
  out/plots/metadata/<figure_name>.json
"""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from plot_style import (
    INTEGRATOR_STYLE,
    apply_major_grid,
    apply_plot_style,
    disable_offset_text,
    save_figure,
)

# Configuration
INTEGRATORS = ["euler", "verlet", "rk4"]
INTEGRATOR_LABELS = {"euler": "Forward Euler", "verlet": "Velocity-Verlet", "rk4": "RK4"}
INTEGRATOR_ORDERS = {"euler": 1, "verlet": 2, "rk4": 4}

DT_VALUES = [1.0, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005]
DT_STEPS = {
    1.0: 10,
    0.5: 20,
    0.1: 100,
    0.05: 200,
    0.01: 1000,
    0.005: 2000,
    0.001: 10000,
    0.0005: 20000,
}
DT_SMALL = 0.01
DT_LARGE = 0.5
TRAJ_DT = DT_SMALL

OMEGA = 1.0
X0 = 1.0
V0 = 0.0
T_FINAL = 10.0

OUT_DIR = "out"
PLOT_DIR = "out/plots"
PLOT_META_DIR = "out/plots/metadata"
SUMMARY_DIR = "out/summary"
SUMMARY_RESULTS1_DIR = "out/summary/results1"

FIG1_PNG = "results1_ho_figure1_trajectories_dt0p01.png"
FIG2_PNG = "results1_ho_figure2_phase_space_dt0p01.png"
FIG3_PNG = "results1_ho_figure3_small_vs_large_dt.png"
FIG4_PNG = "results1_ho_figure4_convergence_combined.png"
FIG5_PNG = "results1_ho_figure5_energy_diagnostic.png"

R1_SMALL_LARGE_CSV = f"{SUMMARY_RESULTS1_DIR}/results1_ho_small_large_summary.csv"
R1_SMALL_LARGE_MD = f"{SUMMARY_RESULTS1_DIR}/results1_ho_small_large_summary.md"
R1_CONVERGENCE_CSV = f"{SUMMARY_RESULTS1_DIR}/results1_ho_convergence_summary.csv"
R1_CONVERGENCE_MD = f"{SUMMARY_RESULTS1_DIR}/results1_ho_convergence_summary.md"
R1_ENDPOINT_VALUES_CSV = f"{SUMMARY_RESULTS1_DIR}/results1_ho_endpoint_values.csv"
R1_ENDPOINT_VALUES_MD = f"{SUMMARY_RESULTS1_DIR}/results1_ho_endpoint_values.md"
R1_CAPTION_NOTES_MD = f"{SUMMARY_RESULTS1_DIR}/results1_ho_caption_notes.md"
R1_SECTION_NOTES_MD = f"{SUMMARY_RESULTS1_DIR}/results1_results_section_notes.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def dt_key(dt: float) -> str:
    return str(dt).replace(".", "_")


def format_dt(dt: float) -> str:
    return f"{dt:g}"


def exact_solution(t: np.ndarray | float, omega: float = OMEGA, x0: float = X0, v0: float = V0):
    """
    Authoritative exact HO solution used throughout.
    x(t) = x0 cos(omega t) + (v0/omega) sin(omega t)
    v(t) = -x0 omega sin(omega t) + v0 cos(omega t)
    """
    t_arr = np.asarray(t, dtype=float)
    if abs(omega) < 1e-15:
        x = x0 + v0 * t_arr
        v = np.full_like(t_arr, v0, dtype=float)
        return x, v

    wt = omega * t_arr
    x = x0 * np.cos(wt) + (v0 / omega) * np.sin(wt)
    v = -x0 * omega * np.sin(wt) + v0 * np.cos(wt)
    return x, v


def exact_phase_curve(num_points: int = 1200, t_final: float = T_FINAL):
    t = np.linspace(0.0, t_final, num_points, dtype=float)
    return exact_solution(t)


def load_manifest():
    manifest_path = f"{OUT_DIR}/manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(filepath: str):
    """Load CSV with header, skipping comment lines."""

    def non_comment_lines(handle):
        for line in handle:
            if line.strip() and not line.startswith("#"):
                yield line

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = list(non_comment_lines(f))
    if not lines:
        return None

    data = np.genfromtxt(lines, delimiter=",", names=True)
    if data is None:
        return None
    if getattr(data, "shape", ()) == ():
        data = np.array([data], dtype=data.dtype)
    return data


def write_csv(path: str, fieldnames: List[str], rows: List[Dict[str, object]]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"Saved {path}")


def markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def fmt_sci(x: float, digits: int = 3) -> str:
    if not np.isfinite(x):
        return "nan"
    return f"{x:.{digits}e}"


def fmt_pct_from_ratio(x: float, digits: int = 4) -> str:
    if not np.isfinite(x):
        return "nan"
    pct = 100.0 * x
    if abs(pct) < 10 ** (-digits):
        return f"{pct:.2e}%"
    return f"{pct:.{digits}f}%"


def write_plot_metadata(plot_png_name: str, extra: Dict[str, object]) -> None:
    os.makedirs(PLOT_META_DIR, exist_ok=True)
    payload = {
        "generated_utc": utc_now(),
        "plot_file_png": f"{PLOT_DIR}/{plot_png_name}",
        "parameters": {
            "omega": OMEGA,
            "x0": X0,
            "v0": V0,
            "t_final": T_FINAL,
            "dt_small": DT_SMALL,
            "dt_large": DT_LARGE,
            "exact_solution": "x(t)=x0 cos(omega t)+(v0/omega) sin(omega t); v(t)=-x0 omega sin(omega t)+v0 cos(omega t)",
        },
    }
    payload.update(extra)
    sidecar_name = f"{os.path.splitext(plot_png_name)[0]}.json"
    sidecar = f"{PLOT_META_DIR}/{sidecar_name}"
    with open(sidecar, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
    print(f"Saved {sidecar}")


def save_plot_pair(fig, png_name: str, metadata: Dict[str, object]) -> None:
    os.makedirs(PLOT_DIR, exist_ok=True)
    png_path = f"{PLOT_DIR}/{png_name}"
    save_figure(fig, png_path)
    print(f"Saved {png_path}")
    write_plot_metadata(png_name, metadata)


def run_ho_simulations():
    """Optional helper: rerun HO sweep and refresh manifest entries."""
    os.makedirs(f"{OUT_DIR}/runs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for integ in INTEGRATORS:
        for dt in DT_VALUES:
            steps = DT_STEPS[dt]
            run_dir = f"{OUT_DIR}/runs/ho_N1_{integ}_dt{dt}_{timestamp}"
            os.makedirs(run_dir, exist_ok=True)
            cmd = [
                "mpirun",
                "-np",
                "1",
                "./md_solver",
                "--mode",
                "ho",
                "--integrator",
                integ,
                "--dt",
                str(dt),
                "--steps",
                str(steps),
                "--N",
                "1",
                "--outdir",
                run_dir,
            ]
            print(f"Running: {integ} dt={dt} steps={steps}")
            subprocess.run(cmd, check=True)
            dst = f"{run_dir}/ho_{integ}.csv"
            if os.path.exists(dst):
                subprocess.run(
                    [sys.executable, "scripts/append_manifest.py", f"ho_convergence.{integ}_dt{dt_key(dt)}", dst],
                    check=True,
                )
    print("All HO simulations complete and manifest updated.")


def collect_ho_data(manifest) -> Tuple[Dict[str, Dict[float, Dict[str, object]]], List[str]]:
    datasets: Dict[str, Dict[float, Dict[str, object]]] = {integ: {} for integ in INTEGRATORS}
    warnings: List[str] = []
    ho_map = manifest.get("ho_convergence", {})
    for integ in INTEGRATORS:
        for dt in DT_VALUES:
            key = f"{integ}_dt{dt_key(dt)}"
            path = ho_map.get(key, "")
            if not path or not os.path.exists(path):
                warnings.append(f"missing data file for {key}: {path or '(empty manifest path)'}")
                continue
            data = load_csv(path)
            if data is None or len(data) == 0:
                warnings.append(f"empty or unreadable CSV for {key}: {path}")
                continue
            datasets[integ][dt] = {"path": path, "data": data}
    return datasets, warnings


def compute_metrics_for_dataset(integ: str, dt: float, dataset: Dict[str, object]) -> Dict[str, object]:
    data = dataset["data"]
    path = dataset["path"]
    names = set(data.dtype.names or [])
    required = {"time", "x", "v"}
    if not required.issubset(names):
        raise ValueError(f"{path} missing required columns {sorted(required - names)}")

    t = np.asarray(data["time"], dtype=float)
    x = np.asarray(data["x"], dtype=float)
    v = np.asarray(data["v"], dtype=float)
    if len(t) == 0:
        raise ValueError(f"{path} has no trajectory rows")

    x_exact, v_exact = exact_solution(t)
    endpoint_x_error = float(abs(x[-1] - x_exact[-1]))
    endpoint_v_error = float(abs(v[-1] - v_exact[-1]))

    phase_dist = np.sqrt((x - x_exact) ** 2 + (v - v_exact) ** 2)
    finite_phase = np.isfinite(phase_dist)
    rms_phase_error = float(np.sqrt(np.mean(phase_dist[finite_phase] ** 2))) if np.any(finite_phase) else float("nan")

    max_relative_energy_drift = float("nan")
    if "E_total" in names:
        E = np.asarray(data["E_total"], dtype=float)
        finite_E = np.isfinite(E)
        if np.any(finite_E):
            E = E[finite_E]
            E0 = E[0]
            if abs(E0) > 1e-30:
                max_relative_energy_drift = float(np.max(np.abs((E - E0) / abs(E0))))
            else:
                max_relative_energy_drift = float(np.max(np.abs(E - E0)))

    return {
        "integrator": integ,
        "integrator_label": INTEGRATOR_LABELS[integ],
        "dt": float(dt),
        "path": path,
        "final_time": float(t[-1]),
        "x_num_final": float(x[-1]),
        "v_num_final": float(v[-1]),
        "x_exact_final": float(x_exact[-1]),
        "v_exact_final": float(v_exact[-1]),
        "endpoint_position_error": endpoint_x_error,
        "endpoint_velocity_error": endpoint_v_error,
        "rms_phase_space_error": rms_phase_error,
        "max_relative_energy_drift": max_relative_energy_drift,
    }


def compute_metrics(datasets: Dict[str, Dict[float, Dict[str, object]]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for integ in INTEGRATORS:
        for dt in DT_VALUES:
            ds = datasets.get(integ, {}).get(dt)
            if ds is None:
                continue
            rows.append(compute_metrics_for_dataset(integ, dt, ds))
    return rows


def integrator_rank(name: str) -> int:
    try:
        return INTEGRATORS.index(name)
    except ValueError:
        return len(INTEGRATORS)


def sorted_metrics(metrics: List[Dict[str, object]]) -> List[Dict[str, object]]:
    return sorted(metrics, key=lambda r: (integrator_rank(str(r["integrator"])), -float(r["dt"])))


def metrics_index(metrics: List[Dict[str, object]]) -> Dict[Tuple[str, float], Dict[str, object]]:
    return {(str(r["integrator"]), float(r["dt"])): r for r in metrics}


def select_fit_points(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    fit_pts = [(dt, err) for dt, err in points if dt <= 0.1]
    if len(fit_pts) < 3:
        fit_pts = sorted(points)[: max(3, len(points) // 2)]
    return sorted(fit_pts)


def fit_loglog(points: List[Tuple[float, float]]) -> Tuple[float, float]:
    x = np.log10(np.asarray([p[0] for p in points], dtype=float))
    y = np.log10(np.asarray([p[1] for p in points], dtype=float))
    slope, intercept = np.polyfit(x, y, 1)
    return float(slope), float(intercept)


def build_fit_summary(
    metrics: List[Dict[str, object]],
    metric_key: str,
    epsilon: float,
    metric_name: str,
) -> Dict[str, Dict[str, object]]:
    out: Dict[str, Dict[str, object]] = {}
    for integ in INTEGRATORS:
        raw = []
        for row in metrics:
            if row["integrator"] != integ:
                continue
            err = float(row[metric_key])
            if np.isfinite(err) and err > epsilon:
                raw.append((float(row["dt"]), err))
        raw = sorted(raw)
        if len(raw) < 2:
            continue
        fit_pts = select_fit_points(raw)
        if len(fit_pts) < 2:
            continue
        slope, intercept = fit_loglog(fit_pts)
        fit_dts = [float(dt) for dt, _ in fit_pts]
        excluded = [float(dt) for dt, _ in raw if not any(abs(dt - fdt) < 1e-15 for fdt in fit_dts)]
        out[integ] = {
            "metric": metric_name,
            "integrator": integ,
            "integrator_label": INTEGRATOR_LABELS[integ],
            "expected_order": INTEGRATOR_ORDERS[integ],
            "slope": slope,
            "intercept": intercept,
            "fit_dts": fit_dts,
            "excluded_dts": excluded,
            "n_points": len(raw),
        }
    return out


def row_for(metrics_idx: Dict[Tuple[str, float], Dict[str, object]], integ: str, dt: float):
    return metrics_idx.get((integ, dt))


def merge_fit_info(endpoint_fit: Dict[str, Dict[str, object]], rms_fit: Dict[str, Dict[str, object]]):
    merged = {}
    for integ in INTEGRATORS:
        ep = endpoint_fit.get(integ)
        rm = rms_fit.get(integ)
        if ep is None or rm is None:
            continue
        excluded_union = sorted(set([float(x) for x in ep["excluded_dts"]] + [float(x) for x in rm["excluded_dts"]]))
        merged[integ] = {
            "integrator_label": INTEGRATOR_LABELS[integ],
            "endpoint_slope": float(ep["slope"]),
            "rms_slope": float(rm["slope"]),
            "expected_order": INTEGRATOR_ORDERS[integ],
            "endpoint_fit_dt_values": [float(v) for v in ep["fit_dts"]],
            "rms_fit_dt_values": [float(v) for v in rm["fit_dts"]],
            "excluded_coarse_dt_values": excluded_union,
        }
    return merged


def add_reference_slope(ax, dts: np.ndarray, errs: np.ndarray, expected: int, color: str) -> None:
    anchor_idx = len(dts) // 2
    dt_anchor = dts[anchor_idx]
    err_anchor = errs[anchor_idx]
    dt_ref = np.array([np.min(dts), np.max(dts)], dtype=float)
    err_ref = err_anchor * (dt_ref / dt_anchor) ** expected
    ax.loglog(dt_ref, err_ref, "--", color=color, alpha=0.45, linewidth=1.2)


def _window_yrange(series: List[Tuple[np.ndarray, np.ndarray]], t0: float, t1: float, pad_frac: float = 0.20) -> Tuple[float, float]:
    vals: List[np.ndarray] = []
    for t, y in series:
        tt = np.asarray(t, dtype=float)
        yy = np.asarray(y, dtype=float)
        mask = (tt >= t0) & (tt <= t1)
        if np.any(mask):
            vals.append(yy[mask])
    if not vals:
        y0 = np.asarray(series[0][1], dtype=float)
        return float(np.min(y0)), float(np.max(y0))
    stacked = np.concatenate(vals)
    ymin = float(np.nanmin(stacked))
    ymax = float(np.nanmax(stacked))
    span = ymax - ymin
    if span <= 1e-14:
        span = max(abs(ymax) * 0.1, 1e-3)
    return ymin - pad_frac * span, ymax + pad_frac * span


def plot_figure1_trajectories(datasets: Dict[str, Dict[float, Dict[str, object]]]) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(9.2, 7.6), sharex=True, constrained_layout=False)
    t_exact = np.linspace(0.0, T_FINAL, 2000, dtype=float)
    x_exact, v_exact = exact_solution(t_exact)
    exact_style = INTEGRATOR_STYLE["exact"]
    zoom_t0, zoom_t1 = 9.0, 10.0
    plot_series = {
        "x": [("exact", t_exact, x_exact)],
        "v": [("exact", t_exact, v_exact)],
    }

    for integ in INTEGRATORS:
        ds = datasets.get(integ, {}).get(TRAJ_DT)
        if ds is None:
            print(f"Warning: {integ} dt={TRAJ_DT:g} missing for Figure 1.")
            continue
        data = ds["data"]
        style = INTEGRATOR_STYLE[integ]
        lw = float(style["linewidth"])
        alpha = 0.95
        if integ == "euler":
            lw = 2.3
            alpha = 0.98
        elif integ in ("verlet", "rk4"):
            lw = 2.0
            alpha = 0.93
        axes[0].plot(
            data["time"],
            data["x"],
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=lw,
            alpha=alpha,
            zorder=3,
            label=INTEGRATOR_LABELS[integ],
        )
        axes[1].plot(
            data["time"],
            data["v"],
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=lw,
            alpha=alpha,
            zorder=3,
            label=INTEGRATOR_LABELS[integ],
        )
        t_num = np.asarray(data["time"], dtype=float)
        plot_series["x"].append((integ, t_num, np.asarray(data["x"], dtype=float)))
        plot_series["v"].append((integ, t_num, np.asarray(data["v"], dtype=float)))

    axes[0].plot(
        t_exact,
        x_exact,
        color=exact_style["color"],
        linestyle=exact_style["linestyle"],
        linewidth=2.0,
        alpha=0.90,
        zorder=6,
        label="Exact",
    )
    axes[1].plot(
        t_exact,
        v_exact,
        color=exact_style["color"],
        linestyle=exact_style["linestyle"],
        linewidth=2.0,
        alpha=0.90,
        zorder=6,
        label="Exact",
    )

    # Keep full context and stable axis limits across reruns.
    axes[1].set_xlim(0.0, T_FINAL)
    # Subtle source-window highlight for the endpoint zoom.
    for ax in axes:
        ax.axvspan(zoom_t0, zoom_t1, color="#9a9a9a", alpha=0.08, zorder=0)

    inset_meta: Dict[str, object] = {}
    panel_specs = [("x", axes[0], "x"), ("v", axes[1], "v")]
    for panel_key, ax, ykey in panel_specs:
        series = [(t, y) for _, t, y in plot_series[ykey]]
        axins = inset_axes(ax, width="20%", height="24%", loc="upper right", borderpad=0.95)
        inset_meta[panel_key] = {"used": True, "placement": "inside-upper right", "time_window": [zoom_t0, zoom_t1]}

        for integ, t, y in plot_series[ykey]:
            if integ == "exact":
                st = exact_style
                lw = 1.8
                alpha = 0.88
            else:
                st = INTEGRATOR_STYLE[str(integ)]
                lw = 2.1 if integ == "euler" else 1.8
                alpha = 0.96 if integ == "euler" else 0.92
            axins.plot(t, y, color=st["color"], linestyle=st["linestyle"], linewidth=lw, alpha=alpha, zorder=3)

        yz0, yz1 = _window_yrange(series, zoom_t0, zoom_t1, pad_frac=0.22)
        axins.set_xlim(zoom_t0, zoom_t1)
        axins.set_ylim(yz0, yz1)
        apply_major_grid(axins)
        disable_offset_text(axins)
        axins.tick_params(axis="both", which="major", labelsize=7)

    axes[0].set_title("(a) Position x(t)", loc="left")
    axes[1].set_title("(b) Velocity v(t)", loc="left")
    axes[0].set_ylabel("Position x [reduced units]")
    axes[1].set_ylabel("Velocity v [reduced units]")
    axes[1].set_xlabel(r"Time $[1/\omega]$")
    for ax in axes:
        apply_major_grid(ax)
        disable_offset_text(ax)
        # Add top headroom so inset bottoms clear nearby curves.
        ymin, ymax = ax.get_ylim()
        span = ymax - ymin
        if span > 0:
            ax.set_ylim(ymin, ymax + 0.10 * span)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 0.965))
    fig.suptitle(r"Harmonic oscillator trajectories ($\Delta t=0.01$)", fontsize=13, y=0.995)
    fig.subplots_adjust(top=0.88, bottom=0.10, left=0.10, right=0.98, hspace=0.24)

    save_plot_pair(
        fig,
        FIG1_PNG,
        {
            "kind": "main_results1_figure",
            "figure_number": 1,
            "claim": "Shows position and velocity trajectories at dt=0.01 for Euler, Velocity-Verlet, RK4 versus exact.",
            "panels": ["(a) x(t)", "(b) v(t)"],
            "insets": inset_meta,
            "zoom_window": [zoom_t0, zoom_t1],
            "endpoint_note": "Near-overlap is expected at small Δt; endpoint errors still rank Euler > Velocity-Verlet > RK4.",
            "shared_legend": True,
        },
    )
    plt.close(fig)


def plot_figure2_phase_space(datasets: Dict[str, Dict[float, Dict[str, object]]]) -> None:
    fig, ax = plt.subplots(figsize=(6.7, 6.5), constrained_layout=False)
    exact_style = INTEGRATOR_STYLE["exact"]
    series = {}

    for integ in INTEGRATORS:
        ds = datasets.get(integ, {}).get(TRAJ_DT)
        if ds is None:
            print(f"Warning: {integ} dt={TRAJ_DT:g} missing for Figure 2.")
            continue
        data = ds["data"]
        series[integ] = data
        style = INTEGRATOR_STYLE[integ]
        ax.plot(
            data["x"],
            data["v"],
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=style["linewidth"],
            alpha=0.96,
            zorder=3,
            label=INTEGRATOR_LABELS[integ],
        )

    x_exact, v_exact = exact_phase_curve(num_points=2200, t_final=T_FINAL)
    ax.plot(
        x_exact,
        v_exact,
        color=exact_style["color"],
        linestyle=exact_style["linestyle"],
        linewidth=2.4,
        alpha=0.98,
        zorder=6,
        label="Exact",
    )

    ax.set_title(r"Phase-space trajectories ($\Delta t=0.01$)")
    ax.set_xlabel("Position x [reduced units]")
    ax.set_ylabel("Velocity v [reduced units]")
    ax.set_aspect("equal", "box")
    apply_major_grid(ax)
    disable_offset_text(ax)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False, borderaxespad=0.0)

    # Place zoom outside the main axes, under the external legend.
    axins = inset_axes(
        ax,
        width="24%",
        height="24%",
        bbox_to_anchor=(1.10, 0.07, 0.98, 0.98),
        bbox_transform=ax.transAxes,
        loc="lower left",
        borderpad=0.0,
    )
    # Inset: local final-time sector with all methods; endpoint markers reveal near-coincidence.
    zoom_t_start = 8.8
    zx_all: List[float] = []
    zv_all: List[float] = []
    marker_map = {"euler": "o", "verlet": "s", "rk4": "^"}
    for integ in INTEGRATORS:
        data = series.get(integ)
        if data is None:
            continue
        style = INTEGRATOR_STYLE[integ]
        tt = np.asarray(data["time"], dtype=float)
        xx = np.asarray(data["x"], dtype=float)
        vv = np.asarray(data["v"], dtype=float)
        mask = tt >= zoom_t_start
        if np.any(mask):
            xloc = xx[mask]
            vloc = vv[mask]
            axins.plot(
                xloc,
                vloc,
                color=style["color"],
                linestyle=style["linestyle"],
                linewidth=style["linewidth"],
                alpha=0.98,
                zorder=3,
            )
            axins.plot(xloc[-1], vloc[-1], marker=marker_map.get(integ, "o"), markersize=4.0, color=style["color"], zorder=4)
            zx_all.extend(xloc.tolist())
            zv_all.extend(vloc.tolist())
    tz = np.linspace(zoom_t_start, T_FINAL, 400, dtype=float)
    xz, vz = exact_solution(tz)
    axins.plot(xz, vz, color=exact_style["color"], linestyle=":", linewidth=1.6, alpha=0.85, zorder=2)
    axins.plot(xz[-1], vz[-1], marker="D", markersize=4.0, color=exact_style["color"], zorder=4)
    zx_all.extend(xz.tolist())
    zv_all.extend(vz.tolist())
    if zx_all and zv_all:
        xmin, xmax = min(zx_all), max(zx_all)
        ymin, ymax = min(zv_all), max(zv_all)
        xpad = max(0.01, 0.22 * (xmax - xmin))
        ypad = max(0.01, 0.22 * (ymax - ymin))
        axins.set_xlim(xmin - xpad, xmax + xpad)
        axins.set_ylim(ymin - ypad, ymax + ypad)
    axins.set_title(r"Zoom near $t\approx T$", fontsize=7.8, pad=2)
    axins.tick_params(axis="both", which="major", labelsize=7)
    apply_major_grid(axins)
    disable_offset_text(axins)
    fig.subplots_adjust(left=0.12, right=0.74, top=0.91, bottom=0.11)

    save_plot_pair(
        fig,
        FIG2_PNG,
        {
            "kind": "main_results1_figure",
            "figure_number": 2,
            "claim": "Shows phase-space geometry at dt=0.01 and qualitative orbit preservation differences.",
            "panel": "v_vs_x",
            "shared_legend": True,
        },
    )
    plt.close(fig)


def _plot_small_large_series(ax, x_data, y_data, exact_x, exact_y, method_color, include_coarse: bool = True):
    # Keep exact clearly distinct from coarse/fine numerical styles in this comparison panel.
    exact_style = INTEGRATOR_STYLE["exact"]
    ax.plot(
        exact_x,
        exact_y,
        color=exact_style["color"],
        linestyle=":",
        linewidth=max(2.0, float(exact_style["linewidth"])),
        alpha=0.95,
    )
    if include_coarse:
        ax.plot(
            x_data["coarse"],
            y_data["coarse"],
            color=method_color,
            linestyle="-.",
            linewidth=1.9,
            alpha=0.92,
        )
    ax.plot(x_data["fine"], y_data["fine"], color=method_color, linestyle="-", linewidth=2.2, alpha=0.92)


def plot_figure3_small_vs_large(
    datasets: Dict[str, Dict[float, Dict[str, object]]],
    metrics_idx: Dict[Tuple[str, float], Dict[str, object]],
) -> None:
    fig, axes = plt.subplots(len(INTEGRATORS), 2, figsize=(12.8, 11.1), constrained_layout=False)
    t_exact = np.linspace(0.0, T_FINAL, 2400, dtype=float)
    x_exact, v_exact = exact_solution(t_exact)

    for row_idx, integ in enumerate(INTEGRATORS):
        ax_traj = axes[row_idx, 0]
        ax_phase = axes[row_idx, 1]
        color = INTEGRATOR_STYLE[integ]["color"]

        ds_large = datasets.get(integ, {}).get(DT_LARGE)
        ds_small = datasets.get(integ, {}).get(DT_SMALL)
        if ds_large is None or ds_small is None:
            print(f"Warning: missing dt={DT_LARGE:g} or dt={DT_SMALL:g} for {integ} in Figure 3.")
            continue
        d_large = ds_large["data"]
        d_small = ds_small["data"]

        _plot_small_large_series(
            ax_traj,
            {"coarse": d_large["time"], "fine": d_small["time"]},
            {"coarse": d_large["x"], "fine": d_small["x"]},
            t_exact,
            x_exact,
            color,
        )
        _plot_small_large_series(
            ax_phase,
            {"coarse": d_large["x"], "fine": d_small["x"]},
            {"coarse": d_large["v"], "fine": d_small["v"]},
            x_exact,
            v_exact,
            color,
        )

        ax_traj.set_xlim(0.0, T_FINAL)
        ax_phase.set_aspect("equal", "box")
        ax_traj.set_ylabel(f"{INTEGRATOR_LABELS[integ]}\nPosition x")
        ax_phase.set_ylabel("Velocity v")
        if row_idx == len(INTEGRATORS) - 1:
            ax_traj.set_xlabel(r"Time $[1/\omega]$")
            ax_phase.set_xlabel("Position x")
        apply_major_grid(ax_traj)
        apply_major_grid(ax_phase)
        disable_offset_text(ax_traj)
        disable_offset_text(ax_phase)

    axes[0, 0].set_title("x(t) vs time", loc="left")
    axes[0, 1].set_title("phase space v(x)", loc="left")

    legend_handles = [
        Line2D(
            [0],
            [0],
            color=INTEGRATOR_STYLE["exact"]["color"],
            linestyle=":",
            linewidth=max(2.0, float(INTEGRATOR_STYLE["exact"]["linewidth"])),
            label="Exact",
        ),
        Line2D([0], [0], color="black", linestyle="-.", linewidth=2.0, label=f"Coarse dt={DT_LARGE:g}"),
        Line2D([0], [0], color="black", linestyle="-", linewidth=2.2, label=f"Fine dt={DT_SMALL:g}"),
    ]
    fig.legend(legend_handles, [h.get_label() for h in legend_handles], loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.972))
    fig.suptitle("Small vs Large Timestep Comparison", fontsize=13, y=0.995)
    fig.subplots_adjust(top=0.92, bottom=0.07, left=0.09, right=0.98, hspace=0.18, wspace=0.08)

    per_integrator = {}
    for integ in INTEGRATORS:
        m_large = row_for(metrics_idx, integ, DT_LARGE)
        m_small = row_for(metrics_idx, integ, DT_SMALL)
        if m_large is None or m_small is None:
            continue
        per_integrator[integ] = {
            "coarse": {
                "dt": DT_LARGE,
                "endpoint_position_error": float(m_large["endpoint_position_error"]),
                "endpoint_velocity_error": float(m_large["endpoint_velocity_error"]),
            },
            "fine": {
                "dt": DT_SMALL,
                "endpoint_position_error": float(m_small["endpoint_position_error"]),
                "endpoint_velocity_error": float(m_small["endpoint_velocity_error"]),
            },
        }

    save_plot_pair(
        fig,
        FIG3_PNG,
        {
            "kind": "main_results1_figure",
            "figure_number": 3,
            "claim": "Direct small-vs-large timestep comparison with full-range coarse behaviour retained; quantitative error values are reported in summary tables.",
            "layout": {"rows": INTEGRATORS, "columns": ["x(t)", "v(x)"]},
            "shared_legend": True,
            "error_annotations": per_integrator,
            "insets": {"euler_trajectory_zoom": False, "euler_phase_zoom": False},
        },
    )
    plt.close(fig)


def _plot_convergence_panel(
    ax,
    metrics: List[Dict[str, object]],
    fit_summary: Dict[str, Dict[str, object]],
    metric_key: str,
    epsilon: float,
    ylabel: str,
    panel_title: str,
):
    method_handles: List[Line2D] = []
    for integ in INTEGRATORS:
        rows = [
            (float(r["dt"]), float(r[metric_key]))
            for r in metrics
            if r["integrator"] == integ and np.isfinite(float(r[metric_key])) and float(r[metric_key]) > epsilon
        ]
        rows = sorted(rows)
        if len(rows) < 2:
            continue
        dts = np.asarray([p[0] for p in rows], dtype=float)
        errs = np.asarray([p[1] for p in rows], dtype=float)
        style = INTEGRATOR_STYLE[integ]
        expected = INTEGRATOR_ORDERS[integ]
        fit_info = fit_summary.get(integ, {})
        slope = fit_info.get("slope", float("nan"))
        label = f"{INTEGRATOR_LABELS[integ]} (s={float(slope):.2f}, exp {expected})"
        line = ax.loglog(
            dts,
            errs,
            linestyle=style["linestyle"],
            color=style["color"],
            linewidth=style["linewidth"],
            alpha=0.95,
            label=label,
        )[0]
        method_handles.append(line)

        fit_dts = [float(v) for v in fit_info.get("fit_dts", [])]
        if fit_dts:
            inc_mask = np.array([any(abs(dt - fd) <= 1e-12 * max(1.0, abs(dt), abs(fd)) for fd in fit_dts) for dt in dts], dtype=bool)
        else:
            inc_mask = np.ones_like(dts, dtype=bool)
        exc_mask = ~inc_mask

        ax.scatter(dts[inc_mask], errs[inc_mask], marker="o", s=40, facecolors=style["color"], edgecolors=style["color"], linewidths=0.8, zorder=4)
        if np.any(exc_mask):
            ax.scatter(dts[exc_mask], errs[exc_mask], marker="o", s=40, facecolors="white", edgecolors=style["color"], linewidths=1.3, zorder=4)

        if fit_dts and np.isfinite(float(fit_info.get("intercept", float("nan")))):
            dt_fit = np.asarray(sorted(fit_dts), dtype=float)
            dt_fit_line = np.array([np.min(dt_fit), np.max(dt_fit)], dtype=float)
            err_fit_line = (10.0 ** float(fit_info["intercept"])) * (dt_fit_line ** float(fit_info["slope"]))
            ax.loglog(dt_fit_line, err_fit_line, ":", color=style["color"], alpha=0.85, linewidth=1.7)

    ax.set_xlabel(r"$\Delta t\ [1/\omega]$")
    ax.set_ylabel(ylabel)
    ax.set_title(panel_title, loc="left")
    apply_major_grid(ax)
    disable_offset_text(ax)
    ax.legend(handles=method_handles, loc="best", frameon=False)


def plot_figure4_convergence_combined(
    metrics: List[Dict[str, object]],
    endpoint_fit: Dict[str, Dict[str, object]],
    rms_fit: Dict[str, Dict[str, object]],
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.0), constrained_layout=False)

    _plot_convergence_panel(
        axes[0],
        metrics=metrics,
        fit_summary=endpoint_fit,
        metric_key="endpoint_position_error",
        epsilon=1e-14,
        ylabel=r"$|x_{\mathrm{num}}(T)-x_{\mathrm{exact}}(T)|$",
        panel_title=r"(a) Endpoint position error at $T=10$",
    )
    _plot_convergence_panel(
        axes[1],
        metrics=metrics,
        fit_summary=rms_fit,
        metric_key="rms_phase_space_error",
        epsilon=1e-16,
        ylabel=r"$\mathrm{RMS}_t \sqrt{(x-x_{ex})^2 + (v-v_{ex})^2}$",
        panel_title=r"(b) RMS phase-space error over $0\leq t\leq 10$",
    )

    fig.suptitle(
        r"Convergence to the exact solution (expected orders: Euler 1, Velocity-Verlet 2, RK4 4)",
        fontsize=12.8,
        y=0.995,
    )
    fig.subplots_adjust(top=0.84, bottom=0.17, left=0.08, right=0.98, wspace=0.27)
    fig.text(
        0.5,
        0.040,
        r"Filled markers: used in slope fit ($\Delta t \leq 0.1$). Open markers: coarse points shown for context.",
        ha="center",
        va="center",
        fontsize=9,
    )

    meta_fits = {
        "endpoint_position_error": {
            integ: {
                "fitted_slope": float(info["slope"]),
                "expected_order": int(info["expected_order"]),
                "fit_dt_values": [float(v) for v in info["fit_dts"]],
                "excluded_dt_values": [float(v) for v in info["excluded_dts"]],
            }
            for integ, info in endpoint_fit.items()
        },
        "rms_phase_space_error": {
            integ: {
                "fitted_slope": float(info["slope"]),
                "expected_order": int(info["expected_order"]),
                "fit_dt_values": [float(v) for v in info["fit_dts"]],
                "excluded_dt_values": [float(v) for v in info["excluded_dts"]],
            }
            for integ, info in rms_fit.items()
        },
    }

    save_plot_pair(
        fig,
        FIG4_PNG,
        {
            "kind": "main_results1_figure",
            "figure_number": 4,
            "claim": "Demonstrates first-, second-, and fourth-order convergence using endpoint and RMS phase-space metrics.",
            "panels": ["(a) endpoint_position_error", "(b) rms_phase_space_error"],
            "fit_rule": "dt <= 0.1; fallback to smallest half if fewer than 3 points",
            "fits": meta_fits,
            "coarse_points_retained_on_plot": True,
        },
    )
    plt.close(fig)


def plot_figure5_energy_diagnostic(
    datasets: Dict[str, Dict[float, Dict[str, object]]],
    metrics_idx: Dict[Tuple[str, float], Dict[str, object]],
) -> None:
    fig, ax = plt.subplots(figsize=(8.6, 5.3), constrained_layout=False)

    for integ in INTEGRATORS:
        ds = datasets.get(integ, {}).get(TRAJ_DT)
        if ds is None:
            continue
        data = ds["data"]
        if "E_total" not in set(data.dtype.names or []):
            continue
        t = np.asarray(data["time"], dtype=float)
        E = np.asarray(data["E_total"], dtype=float)
        finite = np.isfinite(E)
        if not np.any(finite):
            continue
        t = t[finite]
        E = E[finite]
        E0 = E[0]
        rel = (E - E0) / abs(E0) if abs(E0) > 1e-30 else (E - E0)
        style = INTEGRATOR_STYLE[integ]
        ax.plot(
            t,
            rel,
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=style["linewidth"],
            label=INTEGRATOR_LABELS[integ],
        )

    ax.set_xlabel(r"Time $[1/\omega]$")
    ax.set_ylabel(r"$(E-E_0)/|E_0|$ (dimensionless)")
    ax.set_title(r"Energy drift at $\Delta t=0.01$")
    apply_major_grid(ax)
    disable_offset_text(ax)
    ax.legend(loc="upper right", bbox_to_anchor=(0.995, 0.60), frameon=False)

    summary_lines = []
    for integ in INTEGRATORS:
        row = row_for(metrics_idx, integ, TRAJ_DT)
        if row is None:
            continue
        summary_lines.append((integ, INTEGRATOR_LABELS[integ], fmt_pct_from_ratio(float(row["max_relative_energy_drift"]), 4)))
    if summary_lines:
        ax.text(
            0.02,
            0.985,
            "Max relative energy drift",
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=8.7,
            fontweight="semibold",
            bbox={"facecolor": "white", "alpha": 0.90, "edgecolor": "none", "pad": 0.25},
        )
        y = 0.952
        for integ, label, drift_text in summary_lines:
            ax.text(
                0.02,
                y,
                label,
                transform=ax.transAxes,
                va="top",
                ha="left",
                fontsize=8.2,
                color=INTEGRATOR_STYLE[integ]["color"],
                fontweight="semibold",
                bbox={"facecolor": "white", "alpha": 0.90, "edgecolor": "none", "pad": 0.15},
            )
            ax.text(
                0.20,
                y,
                f"max |ΔE/E0| = {drift_text}",
                transform=ax.transAxes,
                va="top",
                ha="left",
                fontsize=8.2,
                color="#222222",
                bbox={"facecolor": "white", "alpha": 0.90, "edgecolor": "none", "pad": 0.15},
            )
            y -= 0.038

    axins = inset_axes(
        ax,
        width="31%",
        height="27%",
        bbox_to_anchor=(0.0, 0.05, 1.0, 1.0),
        bbox_transform=ax.transAxes,
        loc="lower right",
        borderpad=2.0,
    )
    for integ in ("verlet", "rk4"):
        ds = datasets.get(integ, {}).get(TRAJ_DT)
        if ds is None:
            continue
        data = ds["data"]
        if "E_total" not in set(data.dtype.names or []):
            continue
        t = np.asarray(data["time"], dtype=float)
        E = np.asarray(data["E_total"], dtype=float)
        finite = np.isfinite(E)
        if not np.any(finite):
            continue
        t = t[finite]
        E = E[finite]
        E0 = E[0]
        rel = (E - E0) / abs(E0) if abs(E0) > 1e-30 else (E - E0)
        style = INTEGRATOR_STYLE[integ]
        axins.plot(t, rel, color=style["color"], linestyle=style["linestyle"], linewidth=style["linewidth"])
    axins.set_title("Zoom: VV vs RK4", fontsize=8.5, pad=2)
    axins.tick_params(axis="both", which="major", labelsize=7)
    axins.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.1e}"))
    apply_major_grid(axins)
    disable_offset_text(axins)

    # Keep lower area clean for publication readability; no extra sentence below inset.
    fig.subplots_adjust(top=0.90, bottom=0.12, left=0.10, right=0.98)

    save_plot_pair(
        fig,
        FIG5_PNG,
        {
            "kind": "supporting_results1_figure",
            "figure_number": 5,
            "claim": "Supporting diagnostic: Euler shows strong drift, Velocity-Verlet bounded oscillatory error, RK4 tiny drift on this interval.",
            "note": "RK4 is not symplectic.",
        },
    )
    plt.close(fig)


def _write_markdown(path: str, lines: List[str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Saved {path}")


def generate_table_outputs(
    metrics: List[Dict[str, object]],
    endpoint_fit: Dict[str, Dict[str, object]],
    rms_fit: Dict[str, Dict[str, object]],
    sanity_warnings: List[str],
) -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(SUMMARY_RESULTS1_DIR, exist_ok=True)
    ordered = sorted_metrics(metrics)
    idx = metrics_index(metrics)

    # 1) Small-vs-large summary
    small_large_rows = []
    for integ in INTEGRATORS:
        for dt in [DT_LARGE, DT_SMALL]:
            row = row_for(idx, integ, dt)
            if row is None:
                continue
            small_large_rows.append(
                {
                    "integrator": integ,
                    "integrator_label": INTEGRATOR_LABELS[integ],
                    "dt": float(dt),
                    "endpoint_position_error": float(row["endpoint_position_error"]),
                    "endpoint_velocity_error": float(row["endpoint_velocity_error"]),
                    "rms_phase_space_error": float(row["rms_phase_space_error"]),
                    "max_relative_energy_drift": float(row["max_relative_energy_drift"]),
                }
            )
    write_csv(
        R1_SMALL_LARGE_CSV,
        [
            "integrator",
            "integrator_label",
            "dt",
            "endpoint_position_error",
            "endpoint_velocity_error",
            "rms_phase_space_error",
            "max_relative_energy_drift",
        ],
        small_large_rows,
    )
    small_large_md = [
        "# Results 1 HO Small-vs-Large Timestep Summary",
        "",
        f"Generated: {utc_now()}",
        "",
        markdown_table(
            [
                "Integrator",
                "dt",
                "abs(x(T)-x_exact(T))",
                "abs(v(T)-v_exact(T))",
                "RMS phase-space error",
                "max abs(E-E0)/abs(E0)",
            ],
            [
                [
                    INTEGRATOR_LABELS[str(r["integrator"])],
                    format_dt(float(r["dt"])),
                    fmt_sci(float(r["endpoint_position_error"]), 3),
                    fmt_sci(float(r["endpoint_velocity_error"]), 3),
                    fmt_sci(float(r["rms_phase_space_error"]), 3),
                    fmt_sci(float(r["max_relative_energy_drift"]), 3),
                ]
                for r in small_large_rows
            ],
        ),
    ]
    _write_markdown(R1_SMALL_LARGE_MD, small_large_md)

    # 2) Convergence summary
    merged_fit = merge_fit_info(endpoint_fit, rms_fit)
    convergence_rows = []
    for integ in INTEGRATORS:
        info = merged_fit.get(integ)
        if info is None:
            continue
        convergence_rows.append(
            {
                "integrator": integ,
                "integrator_label": info["integrator_label"],
                "endpoint_position_slope": info["endpoint_slope"],
                "rms_phase_space_slope": info["rms_slope"],
                "endpoint_fit_dt_values": ";".join(format_dt(float(v)) for v in info["endpoint_fit_dt_values"]),
                "rms_fit_dt_values": ";".join(format_dt(float(v)) for v in info["rms_fit_dt_values"]),
                "excluded_coarse_dt_values": ";".join(format_dt(float(v)) for v in info["excluded_coarse_dt_values"]),
            }
        )
    write_csv(
        R1_CONVERGENCE_CSV,
        [
            "integrator",
            "integrator_label",
            "endpoint_position_slope",
            "rms_phase_space_slope",
            "endpoint_fit_dt_values",
            "rms_fit_dt_values",
            "excluded_coarse_dt_values",
        ],
        convergence_rows,
    )
    conv_md = [
        "# Results 1 HO Convergence Summary",
        "",
        f"Generated: {utc_now()}",
        "",
        markdown_table(
            [
                "Integrator",
                "Endpoint slope",
                "RMS slope",
                "Endpoint fit dt values",
                "RMS fit dt values",
                "Excluded coarse dt values",
            ],
            [
                [
                    str(r["integrator_label"]),
                    f"{float(r['endpoint_position_slope']):.2f}",
                    f"{float(r['rms_phase_space_slope']):.2f}",
                    str(r["endpoint_fit_dt_values"]),
                    str(r["rms_fit_dt_values"]),
                    str(r["excluded_coarse_dt_values"]) if str(r["excluded_coarse_dt_values"]) else "-",
                ]
                for r in convergence_rows
            ],
        ),
    ]
    _write_markdown(R1_CONVERGENCE_MD, conv_md)

    # 3) Endpoint values table (selected dt)
    selected_dts = [0.5, 0.1, 0.01]
    endpoint_rows = []
    for integ in INTEGRATORS:
        for dt in selected_dts:
            row = row_for(idx, integ, dt)
            if row is None:
                continue
            endpoint_rows.append(
                {
                    "integrator": integ,
                    "integrator_label": INTEGRATOR_LABELS[integ],
                    "dt": dt,
                    "x_num_final": float(row["x_num_final"]),
                    "x_exact_final": float(row["x_exact_final"]),
                    "endpoint_position_error": float(row["endpoint_position_error"]),
                    "v_num_final": float(row["v_num_final"]),
                    "v_exact_final": float(row["v_exact_final"]),
                    "endpoint_velocity_error": float(row["endpoint_velocity_error"]),
                }
            )
    write_csv(
        R1_ENDPOINT_VALUES_CSV,
        [
            "integrator",
            "integrator_label",
            "dt",
            "x_num_final",
            "x_exact_final",
            "endpoint_position_error",
            "v_num_final",
            "v_exact_final",
            "endpoint_velocity_error",
        ],
        endpoint_rows,
    )
    endpoint_md = [
        "# Results 1 HO Endpoint Values (Selected dt)",
        "",
        f"Generated: {utc_now()}",
        "",
        markdown_table(
            [
                "Integrator",
                "dt",
                "x_num(T)",
                "x_exact(T)",
                "abs(Δx(T))",
                "v_num(T)",
                "v_exact(T)",
                "abs(Δv(T))",
            ],
            [
                [
                    str(r["integrator_label"]),
                    format_dt(float(r["dt"])),
                    fmt_sci(float(r["x_num_final"]), 6),
                    fmt_sci(float(r["x_exact_final"]), 6),
                    fmt_sci(float(r["endpoint_position_error"]), 3),
                    fmt_sci(float(r["v_num_final"]), 6),
                    fmt_sci(float(r["v_exact_final"]), 6),
                    fmt_sci(float(r["endpoint_velocity_error"]), 3),
                ]
                for r in endpoint_rows
            ],
        ),
    ]
    _write_markdown(R1_ENDPOINT_VALUES_MD, endpoint_md)

    # 4) Caption/helper notes
    fig3_bits = []
    for integ in INTEGRATORS:
        coarse = row_for(idx, integ, DT_LARGE)
        fine = row_for(idx, integ, DT_SMALL)
        if coarse is None or fine is None:
            continue
        fig3_bits.append(
            f"{INTEGRATOR_LABELS[integ]} coarse/fine endpoint x-error ratio = "
            f"{float(coarse['endpoint_position_error']) / max(float(fine['endpoint_position_error']), 1e-300):.2f}"
        )

    notes = [
        "# Results 1 Figure Caption Notes (Auto-Generated)",
        "",
        f"Generated: {utc_now()}",
        "",
        f"Figure 1 (trajectories): Verifies x(t) and v(t) behaviour for all three methods against the exact solution at dt={format_dt(TRAJ_DT)}; Euler remains the visibly largest deviation while RK4 is nearly exact on this horizon.",
        "Figure 2 (phase space): Shows geometric orbit quality at dt=0.01, with Euler clearly outside the closed exact orbit and a dedicated final-sector zoom showing all methods with endpoint markers.",
        "Figure 3 (small vs large dt): Directly demonstrates timestep sensitivity with dt=0.5 and dt=0.01 for each method, retaining full coarse-range behaviour without dense in-panel text; quantitative values are provided in the summary tables; "
        + "; ".join(fig3_bits)
        + ".",
        f"Figure 4 (combined convergence): Fitted slopes are Euler {endpoint_fit['euler']['slope']:.2f}/{rms_fit['euler']['slope']:.2f}, Velocity-Verlet {endpoint_fit['verlet']['slope']:.2f}/{rms_fit['verlet']['slope']:.2f}, RK4 {endpoint_fit['rk4']['slope']:.2f}/{rms_fit['rk4']['slope']:.2f} (endpoint/RMS), consistent with orders 1/2/4; filled markers denote fit-included points and open markers denote coarse points shown for context.",
        "Figure 5 (energy diagnostic): At dt=0.01, Euler exhibits strong secular drift, Velocity-Verlet shows bounded oscillatory error, and RK4 drift is tiny on this interval; RK4 remains non-symplectic.",
    ]
    if sanity_warnings:
        notes.append("")
        notes.append("Sanity warnings:")
        for warning in sanity_warnings:
            notes.append(f"- WARNING: {warning}")
    _write_markdown(R1_CAPTION_NOTES_MD, notes)

    # Keep one compact machine summary for compatibility with downstream note workflows.
    legacy_notes = [
        "# Results 1 Auto-Summary Notes",
        "",
        f"Generated: {utc_now()}",
        "",
        f"Endpoint slopes: Euler {endpoint_fit['euler']['slope']:.2f}, Velocity-Verlet {endpoint_fit['verlet']['slope']:.2f}, RK4 {endpoint_fit['rk4']['slope']:.2f}.",
        f"RMS slopes: Euler {rms_fit['euler']['slope']:.2f}, Velocity-Verlet {rms_fit['verlet']['slope']:.2f}, RK4 {rms_fit['rk4']['slope']:.2f}.",
    ]
    _write_markdown(R1_SECTION_NOTES_MD, legacy_notes)


def run_sanity_checks(
    endpoint_fit: Dict[str, Dict[str, object]],
    rms_fit: Dict[str, Dict[str, object]],
    metrics_idx: Dict[Tuple[str, float], Dict[str, object]],
) -> List[str]:
    warnings: List[str] = []

    for integ in INTEGRATORS:
        expected = INTEGRATOR_ORDERS[integ]
        efit = endpoint_fit.get(integ)
        if efit is None:
            warnings.append(f"missing endpoint-position fit for {integ}")
        else:
            slope = float(efit["slope"])
            if abs(slope - expected) > 0.35:
                warnings.append(f"endpoint-position slope for {integ} is {slope:.2f}, far from expected {expected}")

        rfit = rms_fit.get(integ)
        if rfit is None:
            warnings.append(f"missing RMS phase-space fit for {integ}")
        else:
            slope = float(rfit["slope"])
            if abs(slope - expected) > 0.35:
                warnings.append(f"RMS phase-space slope for {integ} is {slope:.2f}, far from expected {expected}")

    for integ in INTEGRATORS:
        coarse = row_for(metrics_idx, integ, DT_LARGE)
        fine = row_for(metrics_idx, integ, DT_SMALL)
        if coarse is None or fine is None:
            warnings.append(f"cannot compare coarse vs fine dt for {integ}")
            continue
        if float(coarse["endpoint_position_error"]) <= float(fine["endpoint_position_error"]):
            warnings.append(f"coarse dt position error is not larger than fine dt for {integ} ({DT_LARGE:g} vs {DT_SMALL:g})")
        if float(coarse["endpoint_velocity_error"]) <= float(fine["endpoint_velocity_error"]):
            warnings.append(f"coarse dt velocity error is not larger than fine dt for {integ} ({DT_LARGE:g} vs {DT_SMALL:g})")

    euler = row_for(metrics_idx, "euler", DT_SMALL)
    verlet = row_for(metrics_idx, "verlet", DT_SMALL)
    if euler is not None and verlet is not None:
        if float(euler["max_relative_energy_drift"]) <= float(verlet["max_relative_energy_drift"]):
            warnings.append("Euler energy drift is not larger than Velocity-Verlet at dt=0.01")
    else:
        warnings.append("missing dt=0.01 energy-drift rows for Euler and/or Velocity-Verlet")

    return warnings


def main():
    apply_plot_style()

    if "--run" in sys.argv:
        run_ho_simulations()

    manifest = load_manifest()
    datasets, data_warnings = collect_ho_data(manifest)
    for warning in data_warnings:
        print(f"Warning: {warning}")

    required_missing = []
    for integ in INTEGRATORS:
        for dt in [DT_SMALL, DT_LARGE]:
            if dt not in datasets.get(integ, {}):
                required_missing.append(f"{integ} dt={dt:g}")
    if required_missing:
        raise RuntimeError("Missing required HO datasets for small-vs-large comparison: " + ", ".join(required_missing))

    metrics = compute_metrics(datasets)
    if not metrics:
        raise RuntimeError("No HO metrics could be computed from manifest datasets.")
    m_idx = metrics_index(metrics)

    endpoint_fit = build_fit_summary(
        metrics=metrics,
        metric_key="endpoint_position_error",
        epsilon=1e-14,
        metric_name="endpoint_position_error",
    )
    rms_fit = build_fit_summary(
        metrics=metrics,
        metric_key="rms_phase_space_error",
        epsilon=1e-16,
        metric_name="rms_phase_space_error",
    )

    plot_figure1_trajectories(datasets)
    plot_figure2_phase_space(datasets)
    plot_figure3_small_vs_large(datasets, m_idx)
    plot_figure4_convergence_combined(metrics, endpoint_fit, rms_fit)
    plot_figure5_energy_diagnostic(datasets, m_idx)

    sanity_warnings = run_sanity_checks(endpoint_fit, rms_fit, m_idx)
    generate_table_outputs(metrics, endpoint_fit, rms_fit, sanity_warnings)

    if sanity_warnings:
        print("=== SANITY CHECK WARNINGS ===")
        for warning in sanity_warnings:
            print(f"WARNING: {warning}")
    else:
        print("All numerical sanity checks passed.")


if __name__ == "__main__":
    main()
```

### `scripts/plot_lj.py` (1505 lines)

```py
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
        ax_d.plot(t, rel_dev_pct, color=color, linestyle=linestyle, linewidth=max(2.2, linewidth))
        ax_d.set_ylabel(r"$\Delta E / E_0$ [%]")
        ax_d.axhline(0.0, color=COLOR_REFERENCE, linestyle="--", linewidth=1.0, alpha=0.6)
        apply_major_grid(ax_d)
        disable_offset_text(ax_d)

        row_label = label
        ax_d.text(
            0.98,
            0.92,
            row_label,
            transform=ax_d.transAxes,
            fontsize=9,
            ha="right",
            bbox={"facecolor": "white", "alpha": 0.86, "edgecolor": "none"},
        )

        if row == 0:
            ax_d.set_title(r"Signed relative drift $\Delta E/E_0$ [%]")

        finite_etot = etot[np.isfinite(etot)]
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
                0.02,
                0.93,
                "\n".join(ann_lines),
                transform=ax_d.transAxes,
                ha="left",
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
        "energy_title": "Argon LJ required production run (1 ps, 100 steps): signed total-energy drift",
        "temperature_title": "Argon LJ Required Run (100 Steps, 1 ps): Temperature",
        "energy_purpose": (
            "Core brief-facing evidence for the required 100-step production run using signed total-energy drift only: "
            "Velocity-Verlet remains bounded while Forward Euler drifts strongly."
        ),
        "energy_claim": (
            "At the required run length, Velocity-Verlet gives a physically meaningful bounded "
            "NVE trajectory in total energy; Forward Euler shows strong total-energy drift and is unreliable."
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
```

### `scripts/plot_scaling.py` (424 lines)

```py
#!/usr/bin/env python3
"""
plot_scaling.py — Generate scaling analysis plots (Results 3).

Produces:
  1. Strong scaling: Speedup S(P) with Amdahl's Law fit
  2. Efficiency E(P) = S(P)/P
  3. Stacked bar chart: Compute vs Communication time
  4. Size scaling: Wall time vs N with O(N²) reference

Usage:
  python3 scripts/plot_scaling.py

Prerequisites (from manifest.json):
  scaling.strong -> out/scaling_strong.csv  (columns: P,N,wall_s,comm_s)
  scaling.size   -> out/scaling_size.csv    (columns: P,N,wall_s,comm_s)
"""

import os
import json
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


def load_scaling_csv(manifest, key):
    path = manifest.get("scaling", {}).get(key, "")
    if not os.path.exists(path):
        return None, path, False
    data = np.genfromtxt(path, delimiter=',', names=True, encoding=None)
    names = getattr(getattr(data, "dtype", None), "names", None)
    if names and "P" in names and "wall_s" in names:
        return data, path, False

    # Fallback: tolerate headerless CSVs ("P,N,wall_s,comm_s" missing).
    raw = np.genfromtxt(path, delimiter=',', encoding=None)
    if raw is None:
        return None, path, False
    if raw.ndim == 1:
        raw = np.array([raw])
    if raw.shape[1] < 4:
        return None, path, False
    out = np.zeros(raw.shape[0], dtype=[("P", float), ("N", float), ("wall_s", float), ("comm_s", float)])
    out["P"] = raw[:, 0]
    out["N"] = raw[:, 1]
    out["wall_s"] = raw[:, 2]
    out["comm_s"] = raw[:, 3]
    print(f"Warning: {path} missing header; parsed as 4-column numeric fallback.")
    return out, path, True


def amdahl(P, f):
    """Amdahl's Law: S(P) = 1 / (f + (1-f)/P)."""
    return 1.0 / (f + (1.0 - f) / P)


def plot_strong_scaling():
    """Plot speedup, efficiency, and compute/comm breakdown."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    manifest = load_manifest()
    data, strong_path, used_fallback = load_scaling_csv(manifest, "strong")
    if data is None:
        print("Warning: scaling/strong not found in manifest. Skipping strong scaling.")
        return

    P = data['P'].astype(int)
    wall = data['wall_s']
    comm = data['comm_s']
    compute = np.maximum(wall - comm, 1e-9)  # floor to avoid log(0) at small N

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
    ax1.set_title("Strong Scaling: Speedup")
    ax1.legend(loc="best")
    apply_major_grid(ax1)
    disable_offset_text(ax1)

    # --- Panel 2: Efficiency ---
    ax2 = axes[1]
    ax2.plot(P, efficiency, "o-", color=COLOR_RK4, linewidth=2.0, markersize=6, label="Measured efficiency")
    ax2.axhline(y=1.0, color=COLOR_REFERENCE, linestyle="--", alpha=0.9, linewidth=1.3, label="Ideal (E=1)")
    ax2.set_xlabel("Number of Processes P")
    ax2.set_ylabel("Efficiency E(P) = S(P)/P")
    ax2.set_title("Strong Scaling: Efficiency")
    ax2.set_ylim(0, 1.15)
    ax2.legend(loc="best")
    apply_major_grid(ax2)
    disable_offset_text(ax2)

    # --- Panel 3: Stacked bar — Compute vs Communication ---
    ax3 = axes[2]
    x_pos = np.arange(len(P))
    bar_width = 0.6
    compute_display = np.maximum(compute, 0)
    ax3.bar(x_pos, compute_display, bar_width, label="Compute", color=COLOR_VERLET, alpha=0.85)
    ax3.bar(
        x_pos,
        comm,
        bar_width,
        bottom=compute_display,
        label="Communication",
        color=COLOR_EULER,
        alpha=0.85,
    )
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([str(p) for p in P])
    ax3.set_xlabel("Number of Processes P")
    ax3.set_ylabel("Wall Time [s]")
    ax3.set_title("Compute vs Communication Time")
    ax3.legend(loc="best")
    apply_major_grid(ax3, axis="y")
    disable_offset_text(ax3)

    save_figure(fig, f"{PLOT_DIR}/results3_strong_scaling_speedup_efficiency_breakdown.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/results3_strong_scaling_speedup_efficiency_breakdown.png")

    scaling_meta_path = "out/scaling_meta.txt"
    source_data_files = [strong_path]
    if os.path.exists(scaling_meta_path):
        source_data_files.append(scaling_meta_path)

    missing_provenance = [
        "Raw per-repetition timing samples are not retained in manifest-linked files; only medians are available in scaling_strong.csv.",
        "Timing step count and replication count are configured in scripts/run_all_data.sh but not encoded in scaling_strong.csv.",
    ]
    if used_fallback:
        missing_provenance.append("CSV header provenance missing; file required fallback parsing.")
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
                "N": int(data["N"][i]),
                "wall_s": float(wall[i]),
                "comm_s": float(comm[i]),
                "speedup": float(speedup[i]),
                "efficiency": float(efficiency[i]),
            }
        )

    write_plot_metadata(
        "results3_strong_scaling_speedup_efficiency_breakdown.png",
        "results3",
        {
            "purpose": "Main Results 3 figure for strong scaling: show measured speedup/efficiency and compute-vs-communication breakdown.",
            "intended_claim": "The MPI implementation achieves substantial strong-scaling gains with non-zero communication overhead; Amdahl fit quantifies residual serial fraction.",
            "audience_tier": "brief-facing",
            "source_data_files": unique_preserve_order(source_data_files),
            "source_manifest_keys": ["scaling.strong"],
            "simulation_run_identifiers": [],
            "key_parameters": {
                "integrator": "verlet",
                "fixed_particle_count_N": int(data["N"][0]) if len(data) else None,
                "process_counts_P": [int(p) for p in P.tolist()],
                "plots_in_figure": ["speedup", "efficiency", "compute_vs_communication"],
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
                "Communication time is solver-reported timing and may include measurement noise at small runtimes.",
            ],
            "missing_provenance": missing_provenance,
        },
    )

    if f_fit is not None:
        print(f"  Amdahl serial fraction f = {f_fit:.6f}")
        print(f"  Maximum theoretical speedup = {1.0/f_fit:.1f}x")


def plot_size_scaling():
    """Plot wall time and compute time vs N."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    manifest = load_manifest()
    data, size_path, used_fallback = load_scaling_csv(manifest, "size")
    if data is None:
        print("Warning: scaling/size not found in manifest. Skipping size scaling.")
        return

    N = data['N']
    wall = data['wall_s']
    comm = data['comm_s']
    compute = np.maximum(wall - comm, 1e-9)  # floor to avoid log(0) at small N

    # Fit power law to compute time (wall - comm) for N >= 500
    mask = N >= 500
    slope_comp, intercept_comp = None, None
    slope_wall, intercept_wall = None, None
    if np.sum(mask) >= 2:
        log_N = np.log10(N[mask])
        log_comp = np.log10(np.maximum(compute[mask], 1e-10))
        slope_comp, intercept_comp = np.polyfit(log_N, log_comp, 1)
        
        log_wall = np.log10(wall[mask])
        slope_wall, intercept_wall = np.polyfit(log_N, log_wall, 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 4.8), constrained_layout=True)

    wall_label = 'Wall time'
    if slope_wall is not None:
        wall_label += f' (O(N^{slope_wall:.2f}))'
    ax1.loglog(N, wall, "o-", color=COLOR_VERLET, linewidth=2.0, markersize=6, label=wall_label)
    
    comp_label = 'Compute time'
    if slope_comp is not None:
        comp_label += f' (O(N^{slope_comp:.2f}))'
    ax1.loglog(N, compute, "^-", color=COLOR_RK4, linewidth=2.0, markersize=6, label=comp_label)

    ax1.loglog(N, comm, "s--", color=COLOR_EULER, linewidth=1.5, markersize=5, label="Comm time", alpha=0.9)
    N_ref = np.array([min(N), max(N)])
    t_ref = wall[-1] * (N_ref / N[-1]) ** 2
    ax1.loglog(N_ref, t_ref, "--", color=COLOR_REFERENCE, alpha=0.9, linewidth=1.5, label=r"$\sim N^2$ reference")
    ax1.set_xlabel("Number of Particles N")
    ax1.set_ylabel("Time [s]")
    ax1.set_title("Size Scaling (P=16)")
    ax1.legend(loc="best")
    apply_major_grid(ax1)

    comm_frac = comm / wall * 100
    ax2.plot(N, comm_frac, "o-", color=COLOR_EULER, linewidth=2.0, markersize=6)
    ax2.set_xlabel("Number of Particles N")
    ax2.set_ylabel("Communication Fraction [%]")
    ax2.set_title("Communication Overhead vs Problem Size")
    ax2.set_ylim(0, 100)
    apply_major_grid(ax2)
    ax2.axhline(y=50, color=COLOR_REFERENCE, linestyle="--", linewidth=1.2, label="50% reference")
    ax2.legend(loc="best")
    disable_offset_text(ax2)

    save_figure(fig, f"{PLOT_DIR}/results3_problem_size_scaling_fixed_p16.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/results3_problem_size_scaling_fixed_p16.png")

    scaling_meta_path = "out/scaling_meta.txt"
    source_data_files = [size_path]
    if os.path.exists(scaling_meta_path):
        source_data_files.append(scaling_meta_path)

    missing_provenance = [
        "Raw per-repetition timing samples are not retained in manifest-linked files; only medians are available in scaling_size.csv.",
        "Timing step count and replication count are configured in scripts/run_all_data.sh but not encoded in scaling_size.csv.",
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
                "comm_s": float(comm[i]),
                "compute_s": float(compute[i]),
                "communication_fraction_percent": float(comm_frac[i]),
            }
        )

    write_plot_metadata(
        "results3_problem_size_scaling_fixed_p16.png",
        "results3",
        {
            "purpose": "Main Results 3 figure for problem-size scaling at fixed process count.",
            "intended_claim": "Runtime grows approximately as a power law near O(N^2) while communication fraction changes with size at fixed P=16.",
            "audience_tier": "brief-facing",
            "source_data_files": unique_preserve_order(source_data_files),
            "source_manifest_keys": ["scaling.size"],
            "simulation_run_identifiers": [],
            "key_parameters": {
                "integrator": "verlet",
                "fixed_process_count_P": int(data["P"][0]) if len(data) else None,
                "particle_counts_N": [int(n) for n in N.tolist()],
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
                "compute_time_power_law_exponent": float(slope_comp) if slope_comp is not None else None,
                "communication_fraction_percent_range": [comm_frac_min, comm_frac_max],
                "rows": rows,
            },
            "caveats": [
                "Power-law exponents depend on the chosen fit domain (here N >= 500).",
                "Communication fraction uses solver-reported communication timing, not network-level profiling counters.",
            ],
            "missing_provenance": missing_provenance,
        },
    )


if __name__ == "__main__":
    apply_plot_style()
    plot_strong_scaling()
    plot_size_scaling()
```

### `scripts/plot_style.py` (60 lines)

```py
#!/usr/bin/env python3
"""Shared Matplotlib style helpers for all report plots."""

from matplotlib import pyplot as plt

# Color-blind-friendly palette (Okabe-Ito inspired)
COLOR_EULER = "#E69F00"     # orange
COLOR_VERLET = "#0072B2"    # blue
COLOR_RK4 = "#332288"       # indigo
COLOR_REFERENCE = "#6C6C6C" # gray
COLOR_ACCENT = "#CC79A7"    # magenta

INTEGRATOR_STYLE = {
    "euler": {"color": COLOR_EULER, "linestyle": "--", "linewidth": 2.0},
    "verlet": {"color": COLOR_VERLET, "linestyle": "-", "linewidth": 2.0},
    "rk4": {"color": COLOR_RK4, "linestyle": "-.", "linewidth": 2.0},
    "exact": {"color": COLOR_REFERENCE, "linestyle": "-", "linewidth": 2.2},
}


def apply_plot_style():
    """Apply consistent style defaults used across all figures."""
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
            "lines.linewidth": 2.0,
            "lines.markersize": 5.5,
            "axes.formatter.useoffset": False,
            "axes.formatter.use_mathtext": True,
            "savefig.dpi": 300,
        }
    )


def apply_major_grid(ax, axis="both"):
    """Draw a subtle major-only grid and disable minor-grid clutter."""
    ax.grid(True, which="major", axis=axis, alpha=0.22, linewidth=0.6)
    ax.grid(False, which="minor", axis=axis)


def disable_offset_text(ax):
    """Disable floating axis offset text like '1e-5'/'1e6'."""
    for offset in (ax.xaxis.offsetText, ax.yaxis.offsetText):
        offset.set_visible(False)
    try:
        ax.ticklabel_format(axis="both", style="plain", useOffset=False)
    except Exception:
        # Log axes do not support ticklabel_format(style='plain').
        pass


def save_figure(fig, path):
    """Save with tight bounding box and constrained layout support."""
    fig.savefig(path, bbox_inches="tight")
```

### `scripts/validate_manifest.py` (98 lines)

```py
#!/usr/bin/env python3
"""
validate_manifest.py — Ensure out/manifest.json has expected keys and valid paths.
"""

import argparse
import json
import sys
from pathlib import Path


DT_KEYS = ["1_0", "0_5", "0_1", "0_05", "0_01", "0_005", "0_001", "0_0005"]
INTEGRATORS = ["euler", "verlet", "rk4"]


def nested_get(obj, dotted):
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def require_file(manifest, key, errors):
    value = nested_get(manifest, key)
    if not value:
        errors.append(f"missing key: {key}")
        return
    p = Path(value)
    if not p.exists():
        errors.append(f"missing file for {key}: {value}")


def check_scaling_header(path, errors):
    p = Path(path)
    if not p.exists():
        errors.append(f"missing scaling file: {path}")
        return
    try:
        first = p.read_text(encoding="utf-8", errors="replace").splitlines()[0].strip()
    except IndexError:
        first = ""
    if first != "P,N,wall_s,comm_s":
        errors.append(
            f"bad header in {path}: '{first}' (expected 'P,N,wall_s,comm_s')"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="out/manifest.json")
    parser.add_argument("--skip-scaling", action="store_true")
    args = parser.parse_args()

    mpath = Path(args.manifest)
    if not mpath.exists():
        print(f"ERROR: missing manifest: {args.manifest}", file=sys.stderr)
        sys.exit(1)

    try:
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid manifest JSON: {e}", file=sys.stderr)
        sys.exit(1)

    errors = []

    for integ in INTEGRATORS:
        for dt in DT_KEYS:
            require_file(manifest, f"ho_convergence.{integ}_dt{dt}", errors)

    require_file(manifest, "lj_brief.verlet", errors)
    require_file(manifest, "lj_brief.euler", errors)
    require_file(manifest, "lj_rdf.verlet_long", errors)
    require_file(manifest, "lj_rdf.verlet_long_energy", errors)

    if not args.skip_scaling:
        require_file(manifest, "scaling.strong", errors)
        require_file(manifest, "scaling.size", errors)
        strong = nested_get(manifest, "scaling.strong")
        size = nested_get(manifest, "scaling.size")
        if strong:
            check_scaling_header(strong, errors)
        if size:
            check_scaling_header(size, errors)

    if errors:
        print("Manifest validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("Manifest validation OK")


if __name__ == "__main__":
    main()
```

## 8. File Sizes

```
include/md/constants.hpp                             86 lines
include/md/integrators.hpp                          115 lines
include/md/mic.hpp                                   19 lines
include/md/mpi_context.hpp                          103 lines
include/md/observables.hpp                           90 lines
include/md/params.hpp                                88 lines
include/md/potentials.hpp                            67 lines
include/md/rng.hpp                                  140 lines
include/md/system.hpp                                70 lines
src/main.cpp                                        572 lines
src/observables.cpp                                  70 lines
src/potentials/harmonic.cpp                          37 lines
src/potentials/lennard_jones.cpp                    104 lines
tests/test_force.cpp                                198 lines
tests/test_mic.cpp                                  117 lines
tests/test_runner.cpp                                33 lines

Total C++ lines:
    1909
```

**End of audit.**
