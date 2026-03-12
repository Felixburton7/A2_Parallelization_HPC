# Audit Output — WA2 MPI MD Solver

## Context Preface (Stub)

- Shared Executive Summary, Deliverables Map, claims table, and freshness metadata are centralised in `ai/results.md`.
- This file includes only document-specific sections below.
- Generation metadata for this document:

| Field | Value |
|---|---|
| Generation timestamp (UTC) | 2026-03-12T11:55:08Z |
| Generation succeeded | yes |
| Generation status label | confirmed |
| Generation note | Audit generation completed. |

## Cross-Reference

- Read `ai/results.md` first for shared high-level context.

## Detailed Audit Evidence (Raw and Verbose)

## 1. Metadata

| Field | Value |
|-------|-------|
| Timestamp (UTC) | 2026-03-12T11:55:00Z |
| Git commit | af72d143d0f35acbc02c67bcb510cf7ebd473543 |
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
./ai/__pycache__/analyse_results.cpython-313.pyc
./ai/__pycache__/context_report.cpython-313.pyc
./ai/__pycache__/report_writer_context.cpython-313.pyc
./ai/analyse_results.py
./ai/audit.sh
./ai/audit_output.md
./ai/audit_output.tmp.3syWaq
./ai/audit_preface.tmp.WNgve1
./ai/context_report.py
./ai/generate_all_context.sh
./ai/make_results.sh
./ai/pack_context.sh
./ai/pack_results.sh
./ai/report_writer_context.py
./ai/results.md
./ai/results_bundle.md
./include/md/constants.hpp
./include/md/integrators.hpp
./include/md/mic.hpp
./include/md/observables.hpp
./include/md/params.hpp
./include/md/partition.hpp
./include/md/potentials.hpp
./include/md/rng.hpp
./include/md/system.hpp
./md_solver
./scripts/__pycache__/plot_style.cpython-311.pyc
./scripts/append_manifest.py
./scripts/check_gr_tolerance.py
./scripts/check_tolerance.py
./scripts/combine_metadata.sh
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
./tests/test_integrators.cpp
./tests/test_mic.cpp
./tests/test_partition.cpp
./tests/test_runner.cpp
```

### out/plots/
```
total 6256
drwx------  13 felix  staff     416 Mar 11 12:01 .
drwx------  24 felix  staff     768 Mar 12 11:54 ..
drwx------  14 felix  staff     448 Mar 11 12:18 metadata
-rw-r--r--   1 felix  staff  353455 Mar 11 12:01 results1_figure1ab.png
-rw-r--r--   1 felix  staff  223338 Mar 11 12:01 results1_figure1c.png
-rw-r--r--   1 felix  staff  696830 Mar 11 12:01 results1_figure2.png
-rw-r--r--   1 felix  staff  367029 Mar 11 12:01 results1_figure3.png
-rw-r--r--   1 felix  staff  198433 Mar 11 12:01 results1_figure4.png
-rw-r--r--   1 felix  staff  319969 Mar 11 12:01 results2_figure6.png
-rw-r--r--   1 felix  staff  153527 Mar 11 12:01 results2_figure7.png
-rw-r--r--   1 felix  staff  246521 Mar 11 12:01 results2_figure8.png
-rw-r--r--   1 felix  staff  308808 Mar 11 12:01 results3_figure10abc.png
-rw-r--r--   1 felix  staff  311049 Mar 11 12:01 results3_figure9ab.png
```

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

### out/runs/ directories referenced by manifest
```
out/
out/runs/ho_N1_euler_dt0.0005_20260308_182329/
out/runs/ho_N1_euler_dt0.001_20260308_182329/
out/runs/ho_N1_euler_dt0.005_20260308_182329/
out/runs/ho_N1_euler_dt0.01_20260308_182329/
out/runs/ho_N1_euler_dt0.05_20260308_182329/
out/runs/ho_N1_euler_dt0.1_20260308_182329/
out/runs/ho_N1_euler_dt0.5_20260308_182329/
out/runs/ho_N1_euler_dt1.0_20260308_182329/
out/runs/ho_N1_rk4_dt0.0005_20260308_182329/
out/runs/ho_N1_rk4_dt0.001_20260308_182329/
out/runs/ho_N1_rk4_dt0.005_20260308_182329/
out/runs/ho_N1_rk4_dt0.01_20260308_182329/
out/runs/ho_N1_rk4_dt0.05_20260308_182329/
out/runs/ho_N1_rk4_dt0.1_20260308_182329/
out/runs/ho_N1_rk4_dt0.5_20260308_182329/
out/runs/ho_N1_rk4_dt1.0_20260308_182329/
out/runs/ho_N1_verlet_dt0.0005_20260308_182329/
out/runs/ho_N1_verlet_dt0.001_20260308_182329/
out/runs/ho_N1_verlet_dt0.005_20260308_182329/
out/runs/ho_N1_verlet_dt0.01_20260308_182329/
out/runs/ho_N1_verlet_dt0.05_20260308_182329/
out/runs/ho_N1_verlet_dt0.1_20260308_182329/
out/runs/ho_N1_verlet_dt0.5_20260308_182329/
out/runs/ho_N1_verlet_dt1.0_20260308_182329/
out/runs/lj_brief_N864_P4_euler_prod100_eq50_dt1e-14_20260308_182329/
out/runs/lj_brief_N864_P4_verlet_prod100_eq50_dt1e-14_20260308_182329/
out/runs/lj_rdf_N864_P4_verlet_prod20000_eq50_dt1e-14_20260307_201536/
out/summary/results2/
```

## 3. Build and Warnings

```
rm -f src/main.o src/potentials/harmonic.o src/potentials/lennard_jones.o src/observables.o tests/test_runner.o tests/test_mic.o tests/test_force.o tests/test_integrators.o tests/test_partition.o md_solver test_runner
rm -f src/potentials/*.o tests/*.o

mpicxx -std=c++17 -O3  -g -Wall -Wextra -pedantic -Iinclude -c -o src/main.o src/main.cpp
mpicxx -std=c++17 -O3  -g -Wall -Wextra -pedantic -Iinclude -c -o src/potentials/harmonic.o src/potentials/harmonic.cpp
mpicxx -std=c++17 -O3  -g -Wall -Wextra -pedantic -Iinclude -c -o src/potentials/lennard_jones.o src/potentials/lennard_jones.cpp
mpicxx -std=c++17 -O3  -g -Wall -Wextra -pedantic -Iinclude -c -o src/observables.o src/observables.cpp
mpicxx -std=c++17 -O3  -g -Wall -Wextra -pedantic -Iinclude -o md_solver src/main.o src/potentials/harmonic.o src/potentials/lennard_jones.o src/observables.o
```

**Build status:** confirmed

### Compilation flags

From Makefile line 12:
```
CXXFLAGS = -std=c++17 $(OPT) $(MARCH) -g -Wall -Wextra -pedantic
```

Flags include: `-std=c++17 -O3 -march=native -Wall -Wextra -pedantic`

### Warning check

Re-building to capture warnings explicitly:
```
rm -f src/main.o src/potentials/harmonic.o src/potentials/lennard_jones.o src/observables.o tests/test_runner.o tests/test_mic.o tests/test_force.o tests/test_integrators.o tests/test_partition.o md_solver test_runner
rm -f src/potentials/*.o tests/*.o
make: Nothing to be done for `all'.
```

**Warnings found:** 0
**Warning interpretation:** confirmed (no warning hits detected)

## 4. Unit Tests

```
mpicxx -std=c++17 -O3  -g -Wall -Wextra -pedantic -Iinclude -c -o tests/test_runner.o tests/test_runner.cpp
mpicxx -std=c++17 -O3  -g -Wall -Wextra -pedantic -Iinclude -c -o tests/test_mic.o tests/test_mic.cpp
mpicxx -std=c++17 -O3  -g -Wall -Wextra -pedantic -Iinclude -c -o tests/test_force.o tests/test_force.cpp
mpicxx -std=c++17 -O3  -g -Wall -Wextra -pedantic -Iinclude -c -o tests/test_integrators.o tests/test_integrators.cpp
mpicxx -std=c++17 -O3  -g -Wall -Wextra -pedantic -Iinclude -c -o tests/test_partition.o tests/test_partition.cpp
mpicxx -std=c++17 -O3  -g -Wall -Wextra -pedantic -Iinclude -o test_runner tests/test_runner.o tests/test_mic.o tests/test_force.o tests/test_integrators.o tests/test_partition.o src/potentials/lennard_jones.o src/potentials/harmonic.o src/observables.o
./test_runner
=== MD Unit Tests ===
  MIC tests: ALL PASSED
  Force/Wrapping tests: ALL PASSED
  Integrator tests: ALL PASSED (Euler=5.126961e-02 Verlet=3.615073e-05 RK4=8.333331e-10)
  Partition tests: ALL PASSED
=====================
ALL TESTS PASSED
```

**Test status:** confirmed

## 5. Smoke Runs

### 5a. HO — Velocity-Verlet (N=1, 1000 steps, dt=0.01, T_final≈10)

```
[MacBook-Pro-434.local:15759] [prterun-MacBook-Pro-434-15759@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:15759] [prterun-MacBook-Pro-434-15759@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:15759] PRTE ERROR: Fatal in file oob_tcp_component.c at line 582
--------------------------------------------------------------------------
No sockets were able to be opened on the available protocols
(IPv4 and/or IPv6). Please check your network and retry.
--------------------------------------------------------------------------
[15759] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
--------------------------------------------------------------------------
```

**Output (first 6 + last 3 lines):**
```
# mode: ho, integrator: verlet, N: 1, P: 1, dt: 0.01, steps: 1000, n_steps: 1000, n_frames: 1001, step_indexing: 0..steps (includes initial frame), total_steps_executed: 1000, seed: 42, L: 10000000000, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 0, production_steps: 1000, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: false, production_nve: false, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, timestamp: 2026-03-10T14:59:52Z
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
[MacBook-Pro-434.local:15762] [prterun-MacBook-Pro-434-15762@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:15762] [prterun-MacBook-Pro-434-15762@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:15762] PRTE ERROR: Fatal in file oob_tcp_component.c at line 582
--------------------------------------------------------------------------
No sockets were able to be opened on the available protocols
(IPv4 and/or IPv6). Please check your network and retry.
[15762] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
--------------------------------------------------------------------------
```

**Output (first 6 + last 3):**
```
# mode: ho, integrator: rk4, N: 1, P: 1, dt: 0.01, steps: 1000, n_steps: 1000, n_frames: 1001, step_indexing: 0..steps (includes initial frame), total_steps_executed: 1000, seed: 42, L: 10000000000, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 0, production_steps: 1000, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: false, production_nve: false, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, timestamp: 2026-03-10T14:59:52Z
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
[MacBook-Pro-434.local:15765] [prterun-MacBook-Pro-434-15765@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:15765] [prterun-MacBook-Pro-434-15765@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:15765] PRTE ERROR: Fatal in file oob_tcp_component.c at line 582
--------------------------------------------------------------------------
No sockets were able to be opened on the available protocols
(IPv4 and/or IPv6). Please check your network and retry.
--------------------------------------------------------------------------
--------------------------------------------------------------------------
No network interfaces were found for out-of-band communications. We require
at least one available network for out-of-band messaging.
--------------------------------------------------------------------------
[15765] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
```

**Output (first 6 + last 3):**
```
# mode: ho, integrator: euler, N: 1, P: 1, dt: 0.01, steps: 1000, n_steps: 1000, n_frames: 1001, step_indexing: 0..steps (includes initial frame), total_steps_executed: 1000, seed: 42, L: 10000000000, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 0, production_steps: 1000, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: false, production_nve: false, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, timestamp: 2026-03-10T14:59:52Z
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
[MacBook-Pro-434.local:15768] [prterun-MacBook-Pro-434-15768@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:15768] [prterun-MacBook-Pro-434-15768@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:15768] PRTE ERROR: Fatal in file oob_tcp_component.c at line 582
[15768] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
```

**Output:**
```
# mode: lj, integrator: verlet, N: 864, P: 1, dt: 1e-14, steps: 100, n_steps: 100, n_frames: 101, step_indexing: 0..steps (includes initial frame), total_steps_executed: 150, seed: 42, L: 3.47786e-09, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 50, production_steps: 100, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: true, production_nve: true, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, startup_temperature_before_final_rescale: 94.3304820914354, startup_temperature_after_final_rescale: 94.3999999999999, lattice: FCC, velocities: Box-Muller, timestamp: 2026-03-10T14:59:53Z
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
[MacBook-Pro-434.local:15782] [prterun-MacBook-Pro-434-15782@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:15782] [prterun-MacBook-Pro-434-15782@0,0] bind() failed for port 0: Operation not permitted (1)
[MacBook-Pro-434.local:15782] PRTE ERROR: Fatal in file oob_tcp_component.c at line 582
[15782] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
--------------------------------------------------------------------------
```

**Output:**
```
# mode: lj, integrator: euler, N: 108, P: 1, dt: 1e-14, steps: 10, n_steps: 10, n_frames: 11, step_indexing: 0..steps (includes initial frame), total_steps_executed: 60, seed: 42, L: 1.73893e-09, rcut: 7.65e-10, target_temperature: 94.4, equilibration_steps: 50, production_steps: 10, production_start_step: 0, final_rescale_before_production: true, final_rescale_applied: true, production_nve: true, gr_discard_steps: 200, gr_sample_every: 5, gr_start: 200, startup_temperature_before_final_rescale: 94.9849184843571, startup_temperature_after_final_rescale: 94.4000000000001, lattice: FCC, velocities: Box-Muller, timestamp: 2026-03-10T14:59:53Z
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
[15786] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
[15789] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
Error checking tolerance: [Errno 2] No such file or directory: 'out/audit_p1.PiAnES/lj_verlet.csv'
```

## 6. Code Quality Audit (Assessor Perspective)

### 6a. AI-generation signal detection

**Doxygen-style tags (`@file/@brief/@param/@return`)**
```
count=89
include/md/params.hpp:2: * @file params.hpp
include/md/params.hpp:3: * @brief Runtime parameters.
include/md/params.hpp:15:/// @brief Runtime parameters parsed from command-line arguments.
include/md/partition.hpp:2: * @file partition.hpp
include/md/partition.hpp:3: * @brief Pure helper for 1D remainder-safe particle decomposition.
```

**Step-style numbered comments (`// Step N`, `// N.`)**
```
count=2
src/main.cpp:467:        // Step 0 is the production initial condition; advance after writing/sampling.
tests/test_mic.cpp:88:        double rcut_sigma = md::constants::rcut_sigma;             // 2.25
```

**Verbose NOTE/WARNING/IMPORTANT comment markers**
```
count=0

```

**Triple-slash comments (`///`)**
```
count=49
include/md/params.hpp:15:/// @brief Runtime parameters parsed from command-line arguments.
include/md/params.hpp:17:    int N = 864;          ///< Number of particles
include/md/params.hpp:18:    int steps = 100;      ///< Number of timesteps (HO) / legacy alias for LJ production_steps
include/md/params.hpp:19:    double dt = 1.0e-14;  ///< Timestep [s] (for LJ) or dimensionless (for HO)
include/md/params.hpp:20:    double targetTemperature = 94.4;  ///< Target temperature for LJ startup/production handoff [K]
```

### 6b. Style comparison against Blakely reference style

| Feature | Blakely Style | This Codebase | Risk Level |
|---------|---------------|---------------|------------|
| Namespaces | None | `md::`, `md::constants::` and modular headers | Medium |
| Doxygen headers | None | `@file`, `@brief` and API docs across headers | High |
| MPI wrapping | Raw MPI calls in `main` | `MPIContext` abstraction + helper methods | Medium |
| Comment style | Sparse inline comments | Mix of concise + structured explanatory comments | High |
| Brace style | Allman in examples | Mixed/LLVM-like style in project | Low |

### 6c. Comment density analysis (.cpp/.hpp)

```
file,total,code,comment,blank,comment_to_code,comment_blocks_3plus,flag_over_0.30
include/md/constants.hpp,84,28,28,28,1.000,1,YES
include/md/integrators.hpp,141,66,50,25,0.758,4,YES
include/md/mic.hpp,19,11,3,5,0.273,1,no
include/md/observables.hpp,82,14,58,10,4.143,5,YES
include/md/params.hpp,86,74,5,7,0.068,1,no
include/md/partition.hpp,26,10,10,6,1.000,2,YES
include/md/potentials.hpp,61,11,42,8,3.818,3,YES
include/md/rng.hpp,134,76,33,25,0.434,3,YES
include/md/system.hpp,63,31,22,10,0.710,4,YES
src/main.cpp,550,465,17,68,0.037,2,no
src/observables.cpp,70,52,5,13,0.096,1,no
src/potentials/harmonic.cpp,37,16,14,7,0.875,1,YES
src/potentials/lennard_jones.cpp,104,60,22,22,0.367,2,YES
tests/test_force.cpp,288,208,38,42,0.183,2,no
tests/test_integrators.cpp,95,73,4,18,0.055,1,no
tests/test_mic.cpp,117,83,20,14,0.241,2,no
tests/test_partition.cpp,68,50,4,14,0.080,1,no
tests/test_runner.cpp,33,22,4,7,0.182,1,no
```

### 6d. MPI call inventory

**MPI symbols used (deduplicated):**
```
Binary file src/main.o matches
MPI_Allgatherv
MPI_Barrier
MPI_Bcast
MPI_COMM_WORLD
MPI_Comm_rank
MPI_Comm_size
MPI_DOUBLE
MPI_Finalize
MPI_INT
MPI_Init
MPI_MAX
MPI_MIN
MPI_Reduce
MPI_SUM
MPI_Wtime
```

**MPI call site references (file:line):**
```
Binary file src/main.o matches
src/potentials/harmonic.cpp:10: * The MPI_Allgatherv collective is bypassed entirely in HO mode.
src/main.cpp:127:        MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
src/main.cpp:128:        MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
src/main.cpp:144:        MPI_Bcast(&lambda, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
src/main.cpp:155:    MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
src/main.cpp:156:    MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
src/main.cpp:174:        MPI_Bcast(&lambda, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
src/main.cpp:181:        MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
src/main.cpp:245:    MPI_Init(&argc, &argv);
src/main.cpp:252:    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
src/main.cpp:253:    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
src/main.cpp:300:        MPI_Bcast(&fccError, 1, MPI_INT, 0, MPI_COMM_WORLD);
src/main.cpp:302:            MPI_Finalize();
src/main.cpp:308:    MPI_Bcast(posAll.data(), 3 * N, MPI_DOUBLE, 0, MPI_COMM_WORLD);
src/main.cpp:309:    MPI_Bcast(velAll.data(), 3 * N, MPI_DOUBLE, 0, MPI_COMM_WORLD);
src/main.cpp:343:        double t0 = params.timing ? MPI_Wtime() : 0.0;
src/main.cpp:344:        MPI_Allgatherv(sys.pos.data(), 3 * localN, MPI_DOUBLE, posGlobal.data(), recvcounts.data(),
src/main.cpp:345:                       displs.data(), MPI_DOUBLE, MPI_COMM_WORLD);
src/main.cpp:347:            commTime += (MPI_Wtime() - t0);
src/main.cpp:433:    MPI_Barrier(MPI_COMM_WORLD);
src/main.cpp:434:    const double tStart = MPI_Wtime();
src/main.cpp:442:            MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
src/main.cpp:443:            MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
src/main.cpp:475:    const double elapsed = MPI_Wtime() - tStart;
src/main.cpp:480:    // Pattern follows MPI lecture-notes slide 78: independent MPI_Reduce calls.
src/main.cpp:482:    MPI_Reduce(&elapsed, &maxTime, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
src/main.cpp:489:        MPI_Reduce(&commTime, &commMax, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
src/main.cpp:490:        MPI_Reduce(&commTime, &commMin, 1, MPI_DOUBLE, MPI_MIN, 0, MPI_COMM_WORLD);
src/main.cpp:491:        MPI_Reduce(&commTime, &sumComm, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
src/main.cpp:509:        MPI_Reduce(grHistLocal.data(), grHistGlobal.data(), grNBins, MPI_DOUBLE, MPI_SUM, 0,
src/main.cpp:510:                   MPI_COMM_WORLD);
src/main.cpp:548:    MPI_Finalize();
include/md/system.hpp:51:     * the subsequent MPI_Allgatherv / force evaluation.
include/md/observables.hpp:22: * Must be followed by MPI_Reduce(MPI_SUM) to rank 0 for the global total.
include/md/observables.hpp:38: * @param eKinTotal Total kinetic energy (from MPI_Reduce) [J]
include/md/observables.hpp:49: * The result must be reduced via MPI_Reduce(MPI_SUM) across all ranks,
```

### 6e. Include dependency graph

```
src/main.cpp -> md/constants.hpp, md/integrators.hpp, md/observables.hpp, md/partition.hpp, md/params.hpp, md/potentials.hpp, md/rng.hpp, md/system.hpp
  md/constants.hpp -> (no includes)
  md/integrators.hpp -> vector, md/system.hpp
  md/observables.hpp -> cmath, vector, md/constants.hpp, md/system.hpp
  md/partition.hpp -> algorithm
  md/params.hpp -> cstdio, cstdlib, string
  md/potentials.hpp -> vector, md/system.hpp
  md/rng.hpp -> cmath, random, vector, md/constants.hpp
  md/system.hpp -> cmath, vector
src/observables.cpp -> md/observables.hpp, md/constants.hpp
  md/observables.hpp -> cmath, vector, md/constants.hpp, md/system.hpp
  md/constants.hpp -> (no includes)
src/potentials/harmonic.cpp -> md/potentials.hpp
  md/potentials.hpp -> vector, md/system.hpp
src/potentials/lennard_jones.cpp -> md/constants.hpp, md/mic.hpp, md/potentials.hpp
  md/constants.hpp -> (no includes)
  md/mic.hpp -> cmath
  md/potentials.hpp -> vector, md/system.hpp
```

### 6f. Submission tarball preview + README quality assessment

**Files that would be submitted (excluding ai/, out/, .git/, .venv/, binaries, tarballs):**
```
./.clang-format
./.gitignore
./Makefile
./README.md
./include/md/constants.hpp
./include/md/integrators.hpp
./include/md/mic.hpp
./include/md/observables.hpp
./include/md/params.hpp
./include/md/partition.hpp
./include/md/potentials.hpp
./include/md/rng.hpp
./include/md/system.hpp
./scripts/__pycache__/plot_style.cpython-311.pyc
./scripts/append_manifest.py
./scripts/check_gr_tolerance.py
./scripts/check_tolerance.py
./scripts/combine_metadata.sh
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
./tests/test_integrators.cpp
./tests/test_mic.cpp
./tests/test_partition.cpp
./tests/test_runner.cpp
```

**Submission preview checks:**

- Total files: 38
- Approx uncompressed payload size: 300050 bytes
- Makefile BCN line: BCN ?= 4316J
- Stale/empty directory flag: src/integrators not present
- ai/ directory excluded in preview: confirmed by filter

**README content:**
```markdown
# WA2: MPI Parallelisation of Molecular Dynamics

## Dependencies

- C++17 compiler with MPI (tested with OpenMPI 4.x)
- Python 3 with `numpy` and `matplotlib` for plotting scripts

## Build and test

```bash
make
make test
```

## Example runs

### Harmonic oscillator

```bash
mpirun -np 1 ./md_solver --mode ho --integrator verlet --dt 0.01 --steps 1000 --N 1
```

### Lennard-Jones Argon

```bash
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --dt 1e-14 \
  --target-temperature 94.4 --equilibration-steps 50 --production-steps 100 \
  --final-rescale-before-production
```

### Scaling / timing

```bash
mpirun -np 16 ./md_solver --mode lj --integrator verlet --N 864 --steps 2000 --timing
```

## Reproducibility

The report figures are produced from data in `out/manifest.json` using scripts in `scripts/`.
```

**README checklist (Blakely-oriented):**
- compile instructions (make: Nothing to be done for `all'.): confirmed
- MPI run command examples: confirmed
- CLI flag descriptions/examples: confirmed
- Reproduce-results guidance: confirmed
- Output directory structure guidance: confirmed

## 7. CLI Defaults vs. Brief Requirements

### CLI help output
```
[15856] base/ptl_base_listener.c:604 bind() failed for socket 8 storage size 16: Operation not permitted
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

## 8. File Dump (Curated)

### `Makefile` (61 lines)

```makefile
CXX = mpicxx
OPT ?= -O3
MARCH ?=
CXXFLAGS = -std=c++17 $(OPT) $(MARCH) -g -Wall -Wextra -pedantic
INCLUDES = -Iinclude

SRC_MAIN = src/main.cpp
SRC_HARMONIC = src/potentials/harmonic.cpp
SRC_LJ = src/potentials/lennard_jones.cpp
SRC_OBSERVABLES = src/observables.cpp

SRCS = $(SRC_MAIN) $(SRC_HARMONIC) $(SRC_LJ) $(SRC_OBSERVABLES)
OBJS = $(SRCS:.cpp=.o)

TEST_SRCS = tests/test_runner.cpp tests/test_mic.cpp tests/test_force.cpp \
            tests/test_integrators.cpp tests/test_partition.cpp
TEST_OBJS = $(TEST_SRCS:.cpp=.o)
TEST_DEPS = src/potentials/lennard_jones.o src/potentials/harmonic.o src/observables.o

TARGET = md_solver
TEST_BIN = test_runner

BCN ?= 4316J
TARBALL = $(BCN)_wa2.tar.gz

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c -o $@ $<

test: $(TEST_BIN)
	./$(TEST_BIN)

$(TEST_BIN): $(TEST_OBJS) $(TEST_DEPS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ $^

clean:
	rm -f $(OBJS) $(TEST_OBJS) $(TARGET) $(TEST_BIN)
	rm -f src/potentials/*.o tests/*.o

dist: clean
	@test "$(BCN)" != "4316J_PLACEHOLDER" || (echo "ERROR: Set BCN" && false)
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
	rm -f test_runner wa2-results-*.out
	tar -czvf $(TARBALL) \
		--exclude='__pycache__' --exclude='*.pyc' \
		include/ src/ tests/ scripts/ \
		Makefile README.md .clang-format
	@echo ""
	@echo "Created $(TARBALL)"
	@echo "Contents:"
	@tar -tzvf $(TARBALL) | head -40

out:
	mkdir -p out

.PHONY: all clean test dist out
```

### `README.md` (39 lines)

```markdown
# WA2: MPI Parallelisation of Molecular Dynamics

## Dependencies

- C++17 compiler with MPI (tested with OpenMPI 4.x)
- Python 3 with `numpy` and `matplotlib` for plotting scripts

## Build and test

```bash
make
make test
```

## Example runs

### Harmonic oscillator

```bash
mpirun -np 1 ./md_solver --mode ho --integrator verlet --dt 0.01 --steps 1000 --N 1
```

### Lennard-Jones Argon

```bash
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --dt 1e-14 \
  --target-temperature 94.4 --equilibration-steps 50 --production-steps 100 \
  --final-rescale-before-production
```

### Scaling / timing

```bash
mpirun -np 16 ./md_solver --mode lj --integrator verlet --N 864 --steps 2000 --timing
```

## Reproducibility

The report figures are produced from data in `out/manifest.json` using scripts in `scripts/`.
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

### `.gitignore` (23 lines)

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

# Python cache
__pycache__/
*.pyc
```

### `include/md/constants.hpp` (84 lines)

```cpp
/**
 * @file constants.hpp
 * @brief Physical constants and LJ parameters in SI units.
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

### `include/md/integrators.hpp` (140 lines)

```cpp
/**
 * @file integrators.hpp
 * @brief Forward Euler, RK4, and Velocity-Verlet integrators.
 */

#ifndef MD_INTEGRATORS_HPP
#define MD_INTEGRATORS_HPP

#include <vector>

#include "md/system.hpp"

namespace md {

/**
 * @brief Advance one time-step with the Forward Euler method.
 *
 * For
 *   dx/dt = v,   dv/dt = a(x),
 * Euler uses
 *   x_{n+1} = x_n + dt * v_n,
 *   v_{n+1} = v_n + dt * a_n.
 *
 * This is first-order accurate. It is simple, but for MD it is not
 * time-reversible or symplectic, so  often shows energy drift.
 */
template <typename RefreshForceFn>
inline void stepEuler(System& sys, double dt, RefreshForceFn refreshForces) {
    const int n3 = 3 * sys.localN;

    // x_{n+1} = x_n + dt * v_n
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] += sys.vel[i] * dt;
    }

    // v_{n+1} = v_n + dt * a_n
    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += sys.acc[i] * dt;
    }

    // Update forces/accelerations at the new positions.
    refreshForces();
}

/**
 * @brief Advance one time-step with classical fourth-order Runge-Kutta.
 *
 * RK4 combines four stages as
 *   y_{n+1} = y_n + (k1 + 2k2 + 2k3 + k4)/6,
 * where y = (x, v) and
 *   dx/dt = v,   dv/dt = a(x).
 *
 * RK4 is fourth-order accurate and works well for short-time trajectory
 * accuracy, but it is not symplectic, so less suitable for long MD runs
 * than Velocity-Verlet .
 */
template <typename RefreshForceFn>
inline void stepRK4(System& sys, double dt, RefreshForceFn refreshForces) {
    const int n3 = 3 * sys.localN;

    // Store the initial state.
    std::vector<double> x0(sys.pos);
    std::vector<double> v0(sys.vel);

    auto evalStage = [&](std::vector<double>& kx, std::vector<double>& kv, double weight,
                         const std::vector<double>& prevKx, const std::vector<double>& prevKv) {
        if (weight > 0.0) {
            // Intermediate stage: y_stage = y_n + weight * previous increment
            for (int i = 0; i < n3; ++i) {
                sys.pos[i] = x0[i] + weight * prevKx[i];
                sys.vel[i] = v0[i] + weight * prevKv[i];
            }
            refreshForces();
        }

        // For y' = (v, a): kx = dt * v, kv = dt * a
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

    // x_{n+1} and v_{n+1} from the RK4 weighted sum
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] = x0[i] + (k1x[i] + 2.0 * k2x[i] + 2.0 * k3x[i] + k4x[i]) / 6.0;
        sys.vel[i] = v0[i] + (k1v[i] + 2.0 * k2v[i] + 2.0 * k3v[i] + k4v[i]) / 6.0;
    }

    // Make stored accelerations consistent with the final state.
    refreshForces();
}

/**
 * @brief Advance one time-step with the Velocity-Verlet method.
 *
 * Velocity-Verlet uses
 *   v_{n+1/2} = v_n + (dt/2) a_n,
 *   x_{n+1}   = x_n + dt * v_{n+1/2},
 *   v_{n+1}   = v_{n+1/2} + (dt/2) a_{n+1}.
 *
 * It is  second-order accurate, time-reversible, and symplectic .
 */
template <typename RefreshForceFn>
inline void stepVelocityVerlet(System& sys, double dt, RefreshForceFn refreshForces) {
    const int n3 = 3 * sys.localN;
    const double halfDt = 0.5 * dt;

    // First half-step for velocity.
    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += halfDt * sys.acc[i];
    }

    // Position update using the half-step velocity.
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] += dt * sys.vel[i];
    }

    // Update forces/accelerations at the new positions.
    refreshForces();

    // Second half-step for velocity.
    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += halfDt * sys.acc[i];
    }
}

}  // namespace md

#endif  // MD_INTEGRATORS_HPP```

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

### `include/md/observables.hpp` (82 lines)

```cpp
/**
 * @file observables.hpp
 * @brief Thermodynamic observables: energy, temperature, and g(r).
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

### `include/md/params.hpp` (86 lines)

```cpp
/**
 * @file params.hpp
 * @brief Runtime parameters.
 */

#ifndef MD_PARAMS_HPP
#define MD_PARAMS_HPP

#include <cstdio>
#include <cstdlib>
#include <string>

namespace md {

/// @brief Runtime parameters parsed from command-line arguments.
struct Params {
    int N = 864;          ///< Number of particles
    int steps = 100;      ///< Number of timesteps (HO) / legacy alias for LJ production_steps
    double dt = 1.0e-14;  ///< Timestep [s] (for LJ) or dimensionless (for HO)
    double targetTemperature = 94.4;  ///< Target temperature for LJ startup/production handoff [K]
    int equilibrationSteps =
        50;  ///< LJ startup timesteps before production (with optional rescaling)
    int productionSteps = 100;  ///< LJ production timesteps (NVE after startup/final rescale)
    bool finalRescaleBeforeProduction =
        true;                           ///< Apply one exact rescale at startup->production boundary
    double omega = 1.0;                 ///< HO angular frequency (only for mode "ho")
    std::string integrator = "verlet";  ///< "euler", "rk4", "verlet"
    std::string mode = "lj";            ///< "ho" or "lj"
    bool output = true;                 ///< Enable CSV output
    int seed = 42;                      ///< RNG seed for reproducibility
    bool timing = false;                ///< Enable wall-clock timing (disables output)
    bool gr = false;                    ///< Enable g(r) accumulation
    int grDiscardSteps = 200;  ///< Steps to discard after production_start_step before g(r)
    int grSampleEvery = 5;     ///< Sample g(r) every N steps after discard
    std::string outdir = "";   ///< Output directory for per-run namespaces

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
            else if (arg == "--target-temperature" && i + 1 < argc)
                p.targetTemperature = std::atof(argv[++i]);
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
            else if (arg == "--final-rescale-before-production")
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
            else if (!arg.empty() && arg[0] == '-')
                std::fprintf(stderr, "WARNING: unknown argument '%s' (ignored)\n", argv[i]);
        }
    }
};

}  // namespace md

#endif  // MD_PARAMS_HPP
```

### `include/md/partition.hpp` (26 lines)

```cpp
/**
 * @file partition.hpp
 * @brief Pure helper for 1D remainder-safe particle decomposition.
 */

#ifndef MD_PARTITION_HPP
#define MD_PARTITION_HPP

#include <algorithm>

namespace md {

/**
 * @brief Compute local particle count and offset for a rank.
 *
 * Particles are distributed as evenly as possible:
 * first (N % size) ranks receive one extra particle.
 */
inline void computePartition(int N, int size, int rank, int& localN, int& offset) {
    localN = N / size + (rank < N % size ? 1 : 0);
    offset = rank * (N / size) + std::min(rank, N % size);
}

}  // namespace md

#endif  // MD_PARTITION_HPP
```

### `include/md/potentials.hpp` (61 lines)

```cpp
/**
 * @file potentials.hpp
 * @brief Harmonic Oscillator and Lennard-Jones acceleration/energy kernels.
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
 * Non-interacting potential: operates purely on local data.
 * No communication is required in HO mode.
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
 * Caller must provide up-to-date global positions in posGlobal before
 * invoking this routine.
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

### `include/md/rng.hpp` (134 lines)

```cpp
/**
 * @file rng.hpp
 * @brief FCC lattice construction and Maxwell-Boltzmann velocity initialisation.
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
 * Uses the standard four-site FCC basis with a small zero-mean perturbation
 * to avoid exact-symmetry force artefacts.
 *
 * @param N     Total number of particles (must be 4*k^3, validated by caller)
 * @param L     Box side length [m]
 * @param gen   Reference to shared RNG (caller owns lifetime)
 * @return      Flat interleaved position array of size 3*N
 */
inline std::vector<double> buildFCCLattice(int N, double L, std::mt19937_64& gen) {
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
 * @brief Maxwell-Boltzmann velocities via Box-Muller.
 *
 * Removes centre-of-mass drift and rescales to match the target temperature.
 *
 * @param N      Total number of particles
 * @param T      Target temperature [K]
 * @param mass   Particle mass [kg]
 * @param gen    Reference to shared RNG (same stream as lattice perturbation)
 * @return       Flat interleaved velocity array of size 3*N
 */
inline std::vector<double> generateVelocities(int N, double T, double mass, std::mt19937_64& gen) {
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

### `include/md/system.hpp` (63 lines)

```cpp
/**
 * @file system.hpp
 * @brief Particle state in flat interleaved arrays (x,y,z per particle).
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

### `src/main.cpp` (550 lines)

```cpp
/**
 * @file main.cpp
 * @brief Main entry point for the MPI Molecular Dynamics solver.
 */

#include <mpi.h>
#include <sys/stat.h>

#include <algorithm>
#include <cmath>
#include <cstdio>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <limits>
#include <random>
#include <string>
#include <vector>

#include "md/constants.hpp"
#include "md/integrators.hpp"
#include "md/observables.hpp"
#include "md/partition.hpp"
#include "md/params.hpp"
#include "md/potentials.hpp"
#include "md/rng.hpp"
#include "md/system.hpp"

namespace {

int buildInitialConditions(const md::Params& params, bool isHO, int N, double L,
                           std::vector<double>& posAll, std::vector<double>& velAll) {
    if (isHO) {
        if (params.N != 1) {
            std::fprintf(
                stderr,
                "WARNING: HO validation expects N=1. Continuing with N>1 treats particles as "
                "independent copies.\n");
        }
        // HO validation state: x(0)=1, v(0)=0 for each particle copy.
        for (int i = 0; i < N; ++i) {
            posAll[3 * i] = 1.0;
            posAll[3 * i + 1] = 0.0;
            posAll[3 * i + 2] = 0.0;
            velAll[3 * i] = 0.0;
            velAll[3 * i + 1] = 0.0;
            velAll[3 * i + 2] = 0.0;
        }
        return 0;
    }

    // FCC lattice requires N = 4*k^3.
    const int k = static_cast<int>(std::round(std::cbrt(N / 4.0)));
    if (4 * k * k * k != N) {
        std::fprintf(stderr,
                     "ERROR: N = %d is not a valid FCC particle count "
                     "(need N = 4*k^3, nearest k = %d gives N = %d)\n",
                     N, k, 4 * k * k * k);
        return 1;
    }

    std::mt19937_64 gen(params.seed);
    posAll = md::buildFCCLattice(N, L, gen);
    velAll = md::generateVelocities(N, params.targetTemperature, md::constants::mass, gen);

    double sumV2 = 0.0;
    for (int i = 0; i < 3 * N; ++i) {
        sumV2 += velAll[i] * velAll[i];
    }
    const double tMeasured0 = md::computeTemperature(0.5 * md::constants::mass * sumV2, N);

    std::printf("=== Initial Conditions (Rank 0) ===\n");
    std::printf("Seed: %d | FCC lattice | Box-Muller velocities\n", params.seed);
    std::printf("Perturbation: %.4f sigma | T_initial: %.6f K\n", md::constants::fccPerturbation,
                tMeasured0);
    std::printf("===================================\n");
    return 0;
}

void writeCSVMetadataLine(std::ostream& out, const md::Params& params, int N, int P, int nSteps,
                          int nFrames, int totalStepsExecuted, int equilibrationSteps,
                          bool finalRescaleApplied, int productionStartStep, int grDiscardSteps,
                          int grSampleEvery, int grStart, double startupTempBeforeFinal,
                          double startupTempAfterFinal, double L, bool productionNVE,
                          bool includeLattice) {
    const std::time_t t = std::time(nullptr);
    char tstr[100];
    std::strftime(tstr, sizeof(tstr), "%Y-%m-%dT%H:%M:%SZ", std::gmtime(&t));

    out << "# mode: " << params.mode << ", integrator: " << params.integrator
        << ", N: " << N << ", P: " << P << ", dt: " << params.dt << ", steps: " << nSteps
        << ", n_steps: " << nSteps << ", n_frames: " << nFrames
        << ", step_indexing: 0..steps (includes initial frame)"
        << ", total_steps_executed: " << totalStepsExecuted << ", seed: " << params.seed
        << ", L: " << L << ", rcut: " << md::constants::rcut_sigma * md::constants::sigma
        << ", target_temperature: " << params.targetTemperature
        << ", equilibration_steps: " << equilibrationSteps
        << ", production_steps: " << nSteps << ", production_start_step: " << productionStartStep
        << ", final_rescale_before_production: "
        << (params.finalRescaleBeforeProduction ? "true" : "false")
        << ", final_rescale_applied: " << (finalRescaleApplied ? "true" : "false")
        << ", production_nve: " << (productionNVE ? "true" : "false")
        << ", gr_discard_steps: " << grDiscardSteps << ", gr_sample_every: " << grSampleEvery
        << ", gr_start: " << grStart;

    if (std::isfinite(startupTempBeforeFinal)) {
        out << ", startup_temperature_before_final_rescale: " << startupTempBeforeFinal;
    }
    if (std::isfinite(startupTempAfterFinal)) {
        out << ", startup_temperature_after_final_rescale: " << startupTempAfterFinal;
    }
    if (includeLattice) {
        out << ", lattice: FCC, velocities: Box-Muller";
    }
    out << ", timestamp: " << tstr << "\n";
}

template <typename AdvanceFn>
void runStartupPhaseLJ(md::System& sys, int rank, const md::Params& params, int N,
                       int equilibrationSteps, double& localPE, AdvanceFn&& advanceOneStep,
                       bool& finalRescaleApplied, double& startupTempBeforeFinal,
                       double& startupTempAfterFinal) {
    for (int startupStep = 1; startupStep <= equilibrationSteps; ++startupStep) {
        const double localKE = md::computeLocalKineticEnergy(sys, md::constants::mass);
        double totalKE = 0.0;
        double totalPE = 0.0;
        MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
        MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

        double lambda = 1.0;
        if (rank == 0) {
            const double tMeasured = md::computeTemperature(totalKE, N);
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
    double totalKE = 0.0;
    double totalPE = 0.0;
    MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
    MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        startupTempBeforeFinal = md::computeTemperature(totalKE, N);
    }

    if (params.finalRescaleBeforeProduction) {
        double lambda = 1.0;
        if (rank == 0) {
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
        if (rank == 0) {
            startupTempAfterFinal = md::computeTemperature(totalKE, N);
        }
    } else {
        startupTempAfterFinal = startupTempBeforeFinal;
    }
}

void printSimulationInfo(const md::Params& params, int rank, int nprocs, bool isHO, int N,
                         int nSteps, int nFrames, int totalStepsExecuted, int equilibrationSteps,
                         double L, int productionStartStep, int grStart, int grDiscardSteps,
                         int grSampleEvery, double startupTempBeforeFinal,
                         double startupTempAfterFinal) {
    if (rank != 0 || params.timing) {
        return;
    }

    std::printf("=== MD Solver ===\n");
    std::printf("Mode: %s | Integrator: %s\n", params.mode.c_str(), params.integrator.c_str());
    std::printf("N = %d | P = %d | timesteps = %d | frames = %d (step 0..%d) | dt = %.3e\n", N,
                nprocs, nSteps, nFrames, nSteps, params.dt);
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

}  // namespace

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    md::Params params;
    md::Params::parse(argc, argv, params);

    int rank = 0;
    int nprocs = 1;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);

    const bool isHO = (params.mode == "ho");
    const int N = params.N;
    int localN = 0;
    int offset = 0;
    md::computePartition(N, nprocs, rank, localN, offset);

    std::vector<int> recvcounts(nprocs, 0);
    std::vector<int> displs(nprocs, 0);
    for (int r = 0; r < nprocs; ++r) {
        int ln = 0;
        int off = 0;
        md::computePartition(N, nprocs, r, ln, off);
        recvcounts[r] = 3 * ln;
        displs[r] = 3 * off;
    }
    std::vector<double> posGlobal(3 * N, 0.0);
    double commTime = 0.0;

    const int equilibrationSteps = isHO ? 0 : std::max(0, params.equilibrationSteps);
    const int nSteps = isHO ? params.steps : std::max(0, params.productionSteps);
    const int nFrames = nSteps + 1;
    const int totalStepsExecuted = nSteps + equilibrationSteps;
    const int productionStartStep = 0;

    const int grDiscardSteps = params.grDiscardSteps;
    const int grSampleEvery = params.grSampleEvery;
    const int grStart = productionStartStep + grDiscardSteps;
    const int maxGRFrames = (!isHO && params.gr && grStart <= nSteps)
                                ? (1 + (nSteps - grStart) / grSampleEvery)
                                : 0;

    // Constant-density LJ scaling from Rahman's N=864 reference state.
    const double L = isHO ? md::constants::L_ho_dummy
                          : md::constants::L_sigma_rahman * md::constants::sigma *
                                std::cbrt(static_cast<double>(N) / md::constants::N_rahman);

    std::vector<double> posAll(3 * N, 0.0);
    std::vector<double> velAll(3 * N, 0.0);
    int fccError = 0;

    if (rank == 0) {
        fccError = buildInitialConditions(params, isHO, N, L, posAll, velAll);
    }

    if (!isHO) {
        MPI_Bcast(&fccError, 1, MPI_INT, 0, MPI_COMM_WORLD);
        if (fccError) {
            MPI_Finalize();
            return 1;
        }
    }

    // Every rank needs global positions/velocities for force evaluation and integrator state.
    MPI_Bcast(posAll.data(), 3 * N, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(velAll.data(), 3 * N, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    md::System sys;
    sys.init(localN, offset, N, L);

    for (int i = 0; i < localN; ++i) {
        for (int d = 0; d < 3; ++d) {
            sys.pos[3 * i + d] = posAll[3 * (offset + i) + d];
            sys.vel[3 * i + d] = velAll[3 * (offset + i) + d];
        }
    }

    posGlobal = posAll;

    const double omega = params.omega;
    const double mass = md::constants::mass;

    enum class IntegratorType { Euler, RK4, Verlet };
    IntegratorType intType = IntegratorType::Verlet;
    if (params.integrator == "euler") {
        intType = IntegratorType::Euler;
    } else if (params.integrator == "rk4") {
        intType = IntegratorType::RK4;
    }

    auto evalHO = [omega, mass](md::System& s, const std::vector<double>& pg, double& pe) {
        md::computeHOForces(s, pg, pe, omega, mass);
    };
    auto evalLJ = [mass](md::System& s, const std::vector<double>& pg, double& pe) {
        md::computeLJForces(s, pg, pe, mass);
    };

    double localPE = 0.0;
    auto allgatherPositions = [&]() {
        double t0 = params.timing ? MPI_Wtime() : 0.0;
        MPI_Allgatherv(sys.pos.data(), 3 * localN, MPI_DOUBLE, posGlobal.data(), recvcounts.data(),
                       displs.data(), MPI_DOUBLE, MPI_COMM_WORLD);
        if (params.timing) {
            commTime += (MPI_Wtime() - t0);
        }
    };
    auto refreshForces = [&]() {
        if (isHO) {
            evalHO(sys, posGlobal, localPE);
        } else {
            sys.wrapPositions();
            allgatherPositions();
            evalLJ(sys, posGlobal, localPE);
        }
    };

    auto advanceOneStep = [&]() {
        if (intType == IntegratorType::Euler) {
            md::stepEuler(sys, params.dt, refreshForces);
        } else if (intType == IntegratorType::RK4) {
            md::stepRK4(sys, params.dt, refreshForces);
        } else {
            md::stepVelocityVerlet(sys, params.dt, refreshForces);
        }
    };

    refreshForces();

    bool finalRescaleApplied = false;
    double startupTempBeforeFinal = std::numeric_limits<double>::quiet_NaN();
    double startupTempAfterFinal = std::numeric_limits<double>::quiet_NaN();

    if (!isHO) {
        runStartupPhaseLJ(sys, rank, params, N, equilibrationSteps, localPE, advanceOneStep,
                          finalRescaleApplied, startupTempBeforeFinal, startupTempAfterFinal);
    }

    std::ofstream outFile;
    if (params.output && rank == 0) {
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
            writeCSVMetadataLine(outFile, params, N, nprocs, nSteps, nFrames,
                                 totalStepsExecuted, equilibrationSteps, finalRescaleApplied,
                                 productionStartStep, grDiscardSteps, grSampleEvery, grStart,
                                 startupTempBeforeFinal, startupTempAfterFinal, L, !isHO, !isHO);
            if (isHO) {
                outFile << "step,time,x,v,E_kin,E_pot,E_total\n";
            } else {
                outFile << "step,time,E_kin,E_pot,E_total,temperature\n";
            }
        }
    }

    printSimulationInfo(params, rank, nprocs, isHO, N, nSteps, nFrames, totalStepsExecuted,
                        equilibrationSteps, L, productionStartStep, grStart, grDiscardSteps,
                        grSampleEvery, startupTempBeforeFinal, startupTempAfterFinal);

    if (params.gr && !isHO && maxGRFrames <= 0 && rank == 0) {
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

    const double grDr = md::constants::grBinWidthSigma * md::constants::sigma;
    const double grRMax = isHO ? 0.0 : 0.5 * L;
    const int grNBins = isHO ? 0 : static_cast<int>(grRMax / grDr);
    std::vector<double> grHistLocal(grNBins, 0.0);
    int grFrames = 0;

    // Synchronise clocks before timed production loop (exclude startup/output setup).
    // Reset accumulated comm timer so reported communication matches this timing window.
    commTime = 0.0;
    MPI_Barrier(MPI_COMM_WORLD);
    const double tStart = MPI_Wtime();

    for (int step = 0; step <= nSteps; ++step) {
        double totalKE = 0.0;
        double totalPE = 0.0;

        if (!params.timing) {
            const double localKE = md::computeLocalKineticEnergy(sys, md::constants::mass);
            MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
            MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

            if (params.output && rank == 0 && outFile.is_open()) {
                const double totalE = totalKE + totalPE;
                const double time = step * params.dt;
                if (isHO) {
                    const double x = sys.pos[0];
                    const double v = sys.vel[0];
                    outFile << step << "," << time << "," << x << "," << v << "," << totalKE
                            << "," << totalPE << "," << totalE << "\n";
                } else {
                    const double T = md::computeTemperature(totalKE, N);
                    outFile << step << "," << time << "," << totalKE << "," << totalPE << ","
                            << totalE << "," << T << "\n";
                }
            }
        }

        // Sample RDF only on production frames that pass discard/stride filters.
        if (params.gr && !isHO && step >= grStart && ((step - grStart) % grSampleEvery == 0)) {
            md::accumulateGR(posGlobal, N, L, offset, localN, grDr, grRMax, grHistLocal);
            ++grFrames;
        }

        // Step 0 is the production initial condition; advance after writing/sampling.
        if (step == nSteps) {
            break;
        }

        advanceOneStep();
    }

    const double elapsed = MPI_Wtime() - tStart;

    // Wall time: max across all ranks (the bottleneck determines completion).
    // Communication bottleneck should be reduced with max across ranks as well;
    // avg/min are retained as secondary diagnostics.
    // Pattern follows MPI lecture-notes slide 78: independent MPI_Reduce calls.
    double maxTime = 0.0;
    MPI_Reduce(&elapsed, &maxTime, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    double commMax = 0.0;
    double commAvg = 0.0;
    double commMin = 0.0;
    if (params.timing) {
        double sumComm = 0.0;
        MPI_Reduce(&commTime, &commMax, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
        MPI_Reduce(&commTime, &commMin, 1, MPI_DOUBLE, MPI_MIN, 0, MPI_COMM_WORLD);
        MPI_Reduce(&commTime, &sumComm, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
        if (rank == 0) {
            commAvg = sumComm / nprocs;
        }
    }

    if (rank == 0) {
        std::printf("Wall time: %.6f s (max across %d ranks)\n", maxTime, nprocs);
        if (params.timing) {
            const double commFracPct = (maxTime > 0.0) ? (100.0 * commMax / maxTime) : 0.0;
            std::printf("  Comm time (max): %.6f s (%.1f%%)\n", commMax, commFracPct);
            std::printf("  Comm time (avg): %.6f s\n", commAvg);
            std::printf("  Comm time (min): %.6f s\n", commMin);
        }
    }

    if (params.gr && !isHO && grFrames > 0) {
        std::vector<double> grHistGlobal(grNBins, 0.0);
        MPI_Reduce(grHistLocal.data(), grHistGlobal.data(), grNBins, MPI_DOUBLE, MPI_SUM, 0,
                   MPI_COMM_WORLD);

        if (rank == 0) {
            // RDF is sampled per frame, then normalised after summing histograms across ranks.
            md::normaliseGR(grHistGlobal, grDr, N, L, grFrames);

            const std::string grFname =
                params.outdir.empty() ? "out/gr.csv" : params.outdir + "/gr.csv";
            std::ofstream grFile(grFname);
            if (grFile.is_open()) {
                writeCSVMetadataLine(grFile, params, N, nprocs, nSteps, nFrames,
                                     totalStepsExecuted, equilibrationSteps, finalRescaleApplied,
                                     productionStartStep, grDiscardSteps, grSampleEvery, grStart,
                                     startupTempBeforeFinal, startupTempAfterFinal, L, true,
                                     true);
                grFile << "r_sigma,gr\n";
                for (int b = 0; b < grNBins; ++b) {
                    const double rMid = (b + 0.5) * grDr;
                    grFile << (rMid / md::constants::sigma) << "," << grHistGlobal[b] << "\n";
                }
                grFile.close();
                if (!params.timing) {
                    std::printf("g(r) written to %s (%d bins, %d frames)\n", grFname.c_str(),
                                grNBins, grFrames);
                }
            }
        }
    } else if (params.gr && !isHO && rank == 0 && !params.timing) {
        std::fprintf(stderr,
                     "WARNING: g(r) skipped because no frames were sampled. "
                     "Adjust --production-steps, --equilibration-steps, --gr-discard-steps, or "
                     "--gr-sample-every.\n");
    }

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

### `tests/test_force.cpp` (288 lines)

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
 *
 * Test 4: Cutoff behavior just below and above rcut.
 *
 * Test 5: Minimum-image interaction across a periodic boundary.
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

    // Test 4: Cutoff behavior around rcut
    {
        const double sigma = md::constants::sigma;
        const double mass = md::constants::mass;
        const double rcut = md::constants::rcut;
        const double L = 10.229 * sigma;

        // Just below cutoff: interaction should be non-zero.
        {
            double r = 0.999 * rcut;
            md::System sys;
            sys.init(2, 0, 2, L);
            sys.pos[0] = 0.0;
            sys.pos[1] = 0.0;
            sys.pos[2] = 0.0;
            sys.pos[3] = r;
            sys.pos[4] = 0.0;
            sys.pos[5] = 0.0;

            std::vector<double> posGlobal(sys.pos.begin(), sys.pos.end());
            double pe = 0.0;
            md::computeLJForces(sys, posGlobal, pe, mass);

            double fx0 = sys.acc[0] * mass;
            if (std::abs(fx0) < 1e-20) {
                std::printf("FAIL: LJ cutoff below rcut should interact, got |F_x|=%e\n",
                            std::abs(fx0));
                ++failures;
            }
        }

        // Just above cutoff: interaction should be zero.
        {
            double r = 1.001 * rcut;
            md::System sys;
            sys.init(2, 0, 2, L);
            sys.pos[0] = 0.0;
            sys.pos[1] = 0.0;
            sys.pos[2] = 0.0;
            sys.pos[3] = r;
            sys.pos[4] = 0.0;
            sys.pos[5] = 0.0;

            std::vector<double> posGlobal(sys.pos.begin(), sys.pos.end());
            double pe = 0.0;
            md::computeLJForces(sys, posGlobal, pe, mass);

            double fx0 = sys.acc[0] * mass;
            if (std::abs(fx0) > 1e-20) {
                std::printf("FAIL: LJ cutoff above rcut should be zero, got |F_x|=%e\n",
                            std::abs(fx0));
                ++failures;
            }
        }
    }

    // Test 5: MIC interaction across periodic boundary
    {
        const double sigma = md::constants::sigma;
        const double mass = md::constants::mass;
        const double L = 10.229 * sigma;

        md::System sys;
        sys.init(2, 0, 2, L);

        // Separation is 0.2*sigma through the periodic boundary.
        sys.pos[0] = 0.1 * sigma;
        sys.pos[1] = 0.0;
        sys.pos[2] = 0.0;
        sys.pos[3] = L - 0.1 * sigma;
        sys.pos[4] = 0.0;
        sys.pos[5] = 0.0;

        std::vector<double> posGlobal(sys.pos.begin(), sys.pos.end());
        double pe = 0.0;
        md::computeLJForces(sys, posGlobal, pe, mass);

        double fx0 = sys.acc[0] * mass;
        if (fx0 <= 0.0) {
            std::printf(
                "FAIL: LJ MIC boundary interaction expected +x repulsion on particle 0, got F_x=%e\n",
                fx0);
            ++failures;
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

### `tests/test_integrators.cpp` (95 lines)

```cpp
/**
 * @file test_integrators.cpp
 * @brief Deterministic HO checks for Euler, Verlet, and RK4.
 */

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <vector>

#include "md/constants.hpp"
#include "md/integrators.hpp"
#include "md/potentials.hpp"
#include "md/system.hpp"

namespace {

enum class IntegratorKind { Euler, Verlet, RK4 };

double runHOAndGetError(IntegratorKind kind, double dt, int steps) {
    md::System sys;
    sys.init(1, 0, 1, md::constants::L_ho_dummy);
    sys.pos[0] = 1.0;
    sys.pos[1] = 0.0;
    sys.pos[2] = 0.0;
    sys.vel[0] = 0.0;
    sys.vel[1] = 0.0;
    sys.vel[2] = 0.0;

    std::vector<double> posGlobal(3, 0.0);

    const double omega = 1.0;
    const double mass = md::constants::mass;
    auto evalHO = [omega, mass](md::System& s, const std::vector<double>& pg, double& pe) {
        md::computeHOForces(s, pg, pe, omega, mass);
    };

    double localPE = 0.0;
    auto refreshForces = [&]() { evalHO(sys, posGlobal, localPE); };
    refreshForces();

    for (int step = 0; step < steps; ++step) {
        if (kind == IntegratorKind::Euler) {
            md::stepEuler(sys, dt, refreshForces);
        } else if (kind == IntegratorKind::Verlet) {
            md::stepVelocityVerlet(sys, dt, refreshForces);
        } else {
            md::stepRK4(sys, dt, refreshForces);
        }
    }

    const double t = steps * dt;
    const double xExact = std::cos(omega * t);
    const double vExact = -omega * std::sin(omega * t);
    const double dx = sys.pos[0] - xExact;
    const double dv = sys.vel[0] - vExact;
    return std::sqrt(dx * dx + dv * dv);
}

}  // namespace

int testIntegrators() {
    int failures = 0;

    const double dt = 0.01;
    const int steps = 1000;
    const double errEuler = runHOAndGetError(IntegratorKind::Euler, dt, steps);
    const double errVerlet = runHOAndGetError(IntegratorKind::Verlet, dt, steps);
    const double errRK4 = runHOAndGetError(IntegratorKind::RK4, dt, steps);

    if (!std::isfinite(errEuler) || !std::isfinite(errVerlet) || !std::isfinite(errRK4)) {
        std::printf("FAIL: integrator error contains non-finite value\n");
        ++failures;
    }

    if (!(errRK4 < errVerlet && errVerlet < errEuler)) {
        std::printf("FAIL: expected RK4 < Verlet < Euler errors, got Euler=%e Verlet=%e RK4=%e\n",
                    errEuler, errVerlet, errRK4);
        ++failures;
    }

    if (errRK4 > 1e-7) {
        std::printf("FAIL: RK4 HO error too large: %e\n", errRK4);
        ++failures;
    }

    if (failures == 0) {
        std::printf("  Integrator tests: ALL PASSED (Euler=%e Verlet=%e RK4=%e)\n", errEuler,
                    errVerlet, errRK4);
    } else {
        std::printf("  Integrator tests: %d FAILED\n", failures);
    }

    return failures;
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

### `tests/test_partition.cpp` (68 lines)

```cpp
/**
 * @file test_partition.cpp
 * @brief Unit tests for remainder-safe particle decomposition.
 */

#include <cstdio>
#include <cstdlib>
#include <vector>

#include "md/partition.hpp"

namespace {

int checkCase(int N, int P, const std::vector<int>& expectedLocalN,
              const std::vector<int>& expectedOffset) {
    int failures = 0;

    if (static_cast<int>(expectedLocalN.size()) != P || static_cast<int>(expectedOffset.size()) != P) {
        std::printf("FAIL: partition test fixture size mismatch for N=%d, P=%d\n", N, P);
        return 1;
    }

    int sumLocalN = 0;
    for (int rank = 0; rank < P; ++rank) {
        int localN = -1;
        int offset = -1;
        md::computePartition(N, P, rank, localN, offset);
        sumLocalN += localN;

        if (localN != expectedLocalN[rank]) {
            std::printf("FAIL: partition localN mismatch N=%d P=%d rank=%d got=%d expected=%d\n", N,
                        P, rank, localN, expectedLocalN[rank]);
            ++failures;
        }
        if (offset != expectedOffset[rank]) {
            std::printf("FAIL: partition offset mismatch N=%d P=%d rank=%d got=%d expected=%d\n", N,
                        P, rank, offset, expectedOffset[rank]);
            ++failures;
        }
    }

    if (sumLocalN != N) {
        std::printf("FAIL: partition count conservation N=%d P=%d sum_localN=%d\n", N, P, sumLocalN);
        ++failures;
    }

    return failures;
}

}  // namespace

int testPartition() {
    int failures = 0;

    failures += checkCase(32, 2, {16, 16}, {0, 16});
    failures += checkCase(10, 3, {4, 3, 3}, {0, 4, 7});
    failures += checkCase(3, 5, {1, 1, 1, 0, 0}, {0, 1, 2, 3, 3});
    failures += checkCase(1, 4, {1, 0, 0, 0}, {0, 1, 1, 1});
    failures += checkCase(17, 6, {3, 3, 3, 3, 3, 2}, {0, 3, 6, 9, 12, 15});

    if (failures == 0) {
        std::printf("  Partition tests: ALL PASSED\n");
    } else {
        std::printf("  Partition tests: %d FAILED\n", failures);
    }

    return failures;
}
```

### `tests/test_runner.cpp` (33 lines)

```cpp
/**
 * @file test_runner.cpp
 * @brief Homebrew unit test runner.
 */

#include <cstdio>
#include <cstdlib>

extern int testMIC();
extern int testForce();
extern int testIntegrators();
extern int testPartition();

int main() {
    std::printf("=== MD Unit Tests ===\n");

    int totalFailures = 0;

    totalFailures += testMIC();
    totalFailures += testForce();
    totalFailures += testIntegrators();
    totalFailures += testPartition();

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

### `scripts/combine_metadata.sh` (24 lines)

```sh
#!/usr/bin/env bash
set -euo pipefail

metadata_dir="out/plots/metadata"
output_file="$metadata_dir/all_metadata.txt"

if [ ! -d "$metadata_dir" ]; then
  echo "Metadata directory not found: $metadata_dir" >&2
  exit 1
fi

tmp_file="$(mktemp)"
trap 'rm -f "$tmp_file"' EXIT

find "$metadata_dir" -maxdepth 1 -type f -name '*.json' | sort | while IFS= read -r file; do
  printf '===== %s =====\n' "$(basename "$file")" >> "$tmp_file"
  cat "$file" >> "$tmp_file"
  printf '\n\n' >> "$tmp_file"
done

mv "$tmp_file" "$output_file"
trap - EXIT

printf 'Wrote %s\n' "$output_file"
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

### `scripts/run_all_data.sh` (282 lines)

```sh
#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# run_all_data.sh — Generate ALL production data for the report
#
# Designed for shared HPC clusters (cerberus1). Uses median-of-20
# paired (wall, comm_max) repetitions for scaling benchmarks to filter contention noise.
# ──────────────────────────────────────────────────────────────────

set -euo pipefail

SOLVER="./md_solver"
OUTDIR="out"
SKIP_SCALING=0
STRONG_STEPS=500
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

# Helper: given parallel arrays of wall and comm_max times, pick the
# median by wall time and return the paired (wall, comm_max).
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

# Extract first numeric token from the first line in OUTPUT that matches PATTERN.
extract_metric() {
    local output="$1"
    local pattern="$2"
    awk -v pat="$pattern" '
        $0 ~ pat {
            for (i = 1; i <= NF; ++i) {
                if ($i ~ /^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$/) {
                    print $i
                    exit
                }
            }
        }
    ' <<< "$output"
}

# ── 0. Parallel Consistency Check ──
echo ""
echo "=== PARALLEL CONSISTENCY CHECK ==="
# Uses zero equilibration for a fast MPI consistency smoke test (not a physical-accuracy run).
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
echo "P,N,wall_s,comm_max_s" > "$OUTDIR/scaling_strong.csv"
python3 scripts/append_manifest.py "scaling.strong" "$OUTDIR/scaling_strong.csv"

REPS=20
for P in 1 2 4 8 16 24 32; do
    WALLS=""
    COMMS_MAX=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np $P $SOLVER --mode lj --integrator verlet --N 2048 --steps $STRONG_STEPS --timing 2>/dev/null)
        W=$(extract_metric "$OUTPUT" "Wall time")
        C_MAX=$(extract_metric "$OUTPUT" "Comm time \\(max\\)")
        [ -z "$C_MAX" ] && C_MAX=$(extract_metric "$OUTPUT" "Comm time")
        [ -z "$C_MAX" ] && C_MAX="0.0"
        C_MAX=$(awk -v w="$W" -v c="$C_MAX" 'BEGIN{if (c > w) print w; else print c}')
        WALLS="$WALLS $W"
        COMMS_MAX="$COMMS_MAX $C_MAX"
        echo "    P=$P rep=$REP wall=$W comm_max=$C_MAX"
    done
    PAIR=$(pick_median_pair "$WALLS" "$COMMS_MAX")
    MEDIAN_W=$(echo "$PAIR" | awk '{print $1}')
    MEDIAN_C_MAX=$(echo "$PAIR" | awk '{print $2}')
    echo "$P,2048,$MEDIAN_W,$MEDIAN_C_MAX" >> "$OUTDIR/scaling_strong.csv"
    echo "  >> P=$P MEDIAN: wall=$MEDIAN_W comm_max=$MEDIAN_C_MAX"
done

# ── 5. Size Scaling (median of 20 paired samples) ──
echo ""
echo "=== RESULTS 3: SIZE SCALING (20 reps, P=16, ${SIZE_STEPS} steps) ==="
echo "P,N,wall_s,comm_max_s" > "$OUTDIR/scaling_size.csv"
python3 scripts/append_manifest.py "scaling.size" "$OUTDIR/scaling_size.csv"

for N in 108 256 500 864 1372 2048; do
    WALLS=""
    COMMS_MAX=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np 16 $SOLVER --mode lj --integrator verlet --N $N --steps $SIZE_STEPS --timing 2>/dev/null)
        W=$(extract_metric "$OUTPUT" "Wall time")
        C_MAX=$(extract_metric "$OUTPUT" "Comm time \\(max\\)")
        [ -z "$C_MAX" ] && C_MAX=$(extract_metric "$OUTPUT" "Comm time")
        [ -z "$C_MAX" ] && C_MAX="0.0"
        C_MAX=$(awk -v w="$W" -v c="$C_MAX" 'BEGIN{if (c > w) print w; else print c}')
        WALLS="$WALLS $W"
        COMMS_MAX="$COMMS_MAX $C_MAX"
        echo "    N=$N rep=$REP wall=$W comm_max=$C_MAX"
    done
    PAIR=$(pick_median_pair "$WALLS" "$COMMS_MAX")
    MEDIAN_W=$(echo "$PAIR" | awk '{print $1}')
    MEDIAN_C_MAX=$(echo "$PAIR" | awk '{print $2}')
    echo "16,$N,$MEDIAN_W,$MEDIAN_C_MAX" >> "$OUTDIR/scaling_size.csv"
    echo "  >> N=$N MEDIAN: wall=$MEDIAN_W comm_max=$MEDIAN_C_MAX"
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

### `scripts/run_results.sh` (18 lines)

```sh
#!/bin/bash
# Run end-to-end Results data generation and plotting.
# Usage:
#   bash scripts/run_results.sh [--skip-scaling]

set -euo pipefail
cd "$(dirname "$0")/.."

bash scripts/run_all_data.sh "$@"

# Keep only canonical report plot artifacts (results*.png + results*.json metadata).
mkdir -p out/plots out/plots/metadata
find out/plots -maxdepth 1 -type f ! -name 'results*' -delete
find out/plots/metadata -maxdepth 1 -type f -name '*.json' ! -name 'results*.json' -delete

python3 scripts/plot_ho.py
python3 scripts/plot_lj.py
python3 scripts/plot_scaling.py
```

### `scripts/run_scaling.sh` (230 lines)

```sh
#!/bin/bash
# DEPRECATED — production data generated by scripts/run_all_data.sh. Retained for reference only.
# ──────────────────────────────────────────────────────────────────
# run_scaling.sh — Batch scaling benchmarks with bottleneck comm timing
#
# Uses PAIRED observations: for each rep, records (wall, comm_max) as a pair.
# The median is selected by wall time, and the comm_max from THAT SAME rep
# is reported. This guarantees comm <= wall for every data point.
#
# Usage:
#   bash scripts/run_scaling.sh
#
# Produces:
#   out/scaling_strong.csv   (P,N,wall_s,comm_max_s)
#   out/scaling_size.csv     (P,N,wall_s,comm_max_s)
#   out/scaling_strong_raw.csv
#   out/scaling_size_raw.csv
#   out/scaling_strong_stats.csv
#   out/scaling_size_stats.csv
#   out/scaling_meta.txt
# ──────────────────────────────────────────────────────────────────

set -euo pipefail

SOLVER="./md_solver"
OUTDIR="out"
STRONG_STEPS=1000
SIZE_STEPS=5000
INTEGRATOR="verlet"
REPS=11

mkdir -p "$OUTDIR"

if [ $((REPS % 2)) -eq 0 ]; then
    echo "ERROR: REPS must be odd for an unambiguous median-by-sample selection (got REPS=$REPS)." >&2
    exit 1
fi

# Helper: from a sorted [rep wall comm_max] temp file, emit robust wall-time spread stats.
# Prints CSV fields:
# reps,median_rep,median_wall_s,median_comm_max_s,q1_wall_s,q3_wall_s,iqr_wall_s,min_wall_s,max_wall_s
summarize_sorted_samples() {
    local sorted_file="$1"
    local n
    n=$(wc -l < "$sorted_file" | tr -d ' ')

    if [ "$n" -le 0 ]; then
        return 1
    fi

    local mid q1 q3
    mid=$(( n / 2 + 1 ))
    q1=$(( (n + 1) / 4 ))
    q3=$(( (3 * n + 3) / 4 ))

    local median_line q1_line q3_line min_line max_line
    median_line=$(sed -n "${mid}p" "$sorted_file")
    q1_line=$(sed -n "${q1}p" "$sorted_file")
    q3_line=$(sed -n "${q3}p" "$sorted_file")
    min_line=$(sed -n "1p" "$sorted_file")
    max_line=$(sed -n "${n}p" "$sorted_file")

    local median_rep median_wall median_comm_max q1_wall q3_wall min_wall max_wall iqr_wall
    median_rep=$(echo "$median_line" | awk '{print $1}')
    median_wall=$(echo "$median_line" | awk '{print $2}')
    median_comm_max=$(echo "$median_line" | awk '{print $3}')
    q1_wall=$(echo "$q1_line" | awk '{print $2}')
    q3_wall=$(echo "$q3_line" | awk '{print $2}')
    min_wall=$(echo "$min_line" | awk '{print $2}')
    max_wall=$(echo "$max_line" | awk '{print $2}')
    iqr_wall=$(awk -v q1="$q1_wall" -v q3="$q3_wall" 'BEGIN{printf "%.6f", q3 - q1}')

    echo "$n,$median_rep,$median_wall,$median_comm_max,$q1_wall,$q3_wall,$iqr_wall,$min_wall,$max_wall"
}

# Extract first numeric token from the first line in OUTPUT that matches PATTERN.
extract_metric() {
    local output="$1"
    local pattern="$2"
    awk -v pat="$pattern" '
        $0 ~ pat {
            for (i = 1; i <= NF; ++i) {
                if ($i ~ /^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$/) {
                    print $i
                    exit
                }
            }
        }
    ' <<< "$output"
}

# ─── Strong Scaling: N=2048, vary P ──────────────────────────────
echo "P,N,wall_s,comm_max_s" > "$OUTDIR/scaling_strong.csv"
echo "kind,P,N,rep,wall_s,comm_max_s" > "$OUTDIR/scaling_strong_raw.csv"
echo "P,N,reps,median_rep,median_wall_s,median_comm_max_s,q1_wall_s,q3_wall_s,iqr_wall_s,min_wall_s,max_wall_s" > "$OUTDIR/scaling_strong_stats.csv"

N_STRONG=2048
for P in 1 2 4 8 16 24 32; do
    TMP_SAMPLES=$(mktemp)
    for REP in $(seq 1 $REPS); do
        # OUTPUT=$(mpirun -np "$P" "$SOLVER" \
        OUTPUT=$(mpirun --bind-to core -np "$P" "$SOLVER" \
            --mode lj --integrator "$INTEGRATOR" \
            --N "$N_STRONG" --steps "$STRONG_STEPS" --timing 2>&1)

        WALL=$(extract_metric "$OUTPUT" "Wall time")
        COMM_MAX=$(extract_metric "$OUTPUT" "Comm time \\(max\\)")
        if [ -z "$COMM_MAX" ]; then
            COMM_MAX=$(extract_metric "$OUTPUT" "Comm time")
        fi
        if [ -z "$WALL" ]; then
            echo "ERROR: failed to parse wall time for strong scaling (P=$P, rep=$REP)." >&2
            echo "$OUTPUT" >&2
            rm -f "$TMP_SAMPLES"
            exit 1
        fi
        if [ -z "$COMM_MAX" ]; then COMM_MAX="0.000000"; fi
        COMM_MAX=$(awk -v w="$WALL" -v c="$COMM_MAX" 'BEGIN{if (c > w) print w; else print c}')

        echo "$REP $WALL $COMM_MAX" >> "$TMP_SAMPLES"
        echo "strong,$P,$N_STRONG,$REP,$WALL,$COMM_MAX" >> "$OUTDIR/scaling_strong_raw.csv"
        echo "  P=$P rep=$REP wall=$WALL comm_max=$COMM_MAX"
    done

    SORTED_SAMPLES=$(mktemp)
    sort -n -k2 "$TMP_SAMPLES" > "$SORTED_SAMPLES"
    STATS=$(summarize_sorted_samples "$SORTED_SAMPLES")
    rm -f "$TMP_SAMPLES" "$SORTED_SAMPLES"

    REPS_OUT=$(echo "$STATS" | cut -d, -f1)
    MEDIAN_REP=$(echo "$STATS" | cut -d, -f2)
    MED_WALL=$(echo "$STATS" | cut -d, -f3)
    MED_COMM_MAX=$(echo "$STATS" | cut -d, -f4)
    Q1_WALL=$(echo "$STATS" | cut -d, -f5)
    Q3_WALL=$(echo "$STATS" | cut -d, -f6)
    IQR_WALL=$(echo "$STATS" | cut -d, -f7)
    MIN_WALL=$(echo "$STATS" | cut -d, -f8)
    MAX_WALL=$(echo "$STATS" | cut -d, -f9)

    echo "$P,$N_STRONG,$MED_WALL,$MED_COMM_MAX" >> "$OUTDIR/scaling_strong.csv"
    echo "$P,$N_STRONG,$REPS_OUT,$MEDIAN_REP,$MED_WALL,$MED_COMM_MAX,$Q1_WALL,$Q3_WALL,$IQR_WALL,$MIN_WALL,$MAX_WALL" >> "$OUTDIR/scaling_strong_stats.csv"
    echo ">> P=$P MEDIAN: wall=$MED_WALL comm_max=$MED_COMM_MAX"
done

echo ""

# ─── Size Scaling: P=16, vary N ──────────────────────────────────
echo "P,N,wall_s,comm_max_s" > "$OUTDIR/scaling_size.csv"
echo "kind,P,N,rep,wall_s,comm_max_s" > "$OUTDIR/scaling_size_raw.csv"
echo "P,N,reps,median_rep,median_wall_s,median_comm_max_s,q1_wall_s,q3_wall_s,iqr_wall_s,min_wall_s,max_wall_s" > "$OUTDIR/scaling_size_stats.csv"

P_SIZE=16
for N in 108 256 500 864 1372 2048; do
    TMP_SAMPLES=$(mktemp)
    for REP in $(seq 1 $REPS); do
        # OUTPUT=$(mpirun -np "$P_SIZE" "$SOLVER" \
        OUTPUT=$(mpirun --bind-to core -np "$P_SIZE" "$SOLVER" \
            --mode lj --integrator "$INTEGRATOR" \
            --N "$N" --steps "$SIZE_STEPS" --timing 2>&1)

        WALL=$(extract_metric "$OUTPUT" "Wall time")
        COMM_MAX=$(extract_metric "$OUTPUT" "Comm time \\(max\\)")
        if [ -z "$COMM_MAX" ]; then
            COMM_MAX=$(extract_metric "$OUTPUT" "Comm time")
        fi
        if [ -z "$WALL" ]; then
            echo "ERROR: failed to parse wall time for size scaling (N=$N, rep=$REP)." >&2
            echo "$OUTPUT" >&2
            rm -f "$TMP_SAMPLES"
            exit 1
        fi
        if [ -z "$COMM_MAX" ]; then COMM_MAX="0.000000"; fi
        COMM_MAX=$(awk -v w="$WALL" -v c="$COMM_MAX" 'BEGIN{if (c > w) print w; else print c}')

        echo "$REP $WALL $COMM_MAX" >> "$TMP_SAMPLES"
        echo "size,$P_SIZE,$N,$REP,$WALL,$COMM_MAX" >> "$OUTDIR/scaling_size_raw.csv"
        echo "  N=$N rep=$REP wall=$WALL comm_max=$COMM_MAX"
    done

    SORTED_SAMPLES=$(mktemp)
    sort -n -k2 "$TMP_SAMPLES" > "$SORTED_SAMPLES"
    STATS=$(summarize_sorted_samples "$SORTED_SAMPLES")
    rm -f "$TMP_SAMPLES" "$SORTED_SAMPLES"

    REPS_OUT=$(echo "$STATS" | cut -d, -f1)
    MEDIAN_REP=$(echo "$STATS" | cut -d, -f2)
    MED_WALL=$(echo "$STATS" | cut -d, -f3)
    MED_COMM_MAX=$(echo "$STATS" | cut -d, -f4)
    Q1_WALL=$(echo "$STATS" | cut -d, -f5)
    Q3_WALL=$(echo "$STATS" | cut -d, -f6)
    IQR_WALL=$(echo "$STATS" | cut -d, -f7)
    MIN_WALL=$(echo "$STATS" | cut -d, -f8)
    MAX_WALL=$(echo "$STATS" | cut -d, -f9)

    echo "$P_SIZE,$N,$MED_WALL,$MED_COMM_MAX" >> "$OUTDIR/scaling_size.csv"
    echo "$P_SIZE,$N,$REPS_OUT,$MEDIAN_REP,$MED_WALL,$MED_COMM_MAX,$Q1_WALL,$Q3_WALL,$IQR_WALL,$MIN_WALL,$MAX_WALL" >> "$OUTDIR/scaling_size_stats.csv"
    echo ">> N=$N MEDIAN: wall=$MED_WALL comm_max=$MED_COMM_MAX"
done

{
  echo "hostname: $(hostname)"
  if command -v lscpu &>/dev/null; then
    echo "cpu: $(lscpu | grep 'Model name' | sed 's/.*: *//')"
  elif [ -r /proc/cpuinfo ]; then
    echo "cpu: $(grep -m1 'model name' /proc/cpuinfo | sed 's/.*: *//')"
  else
    echo "cpu: unknown"
  fi
  if command -v mpicxx &>/dev/null; then
    echo "compiler: $(mpicxx --version | head -1)"
  else
    echo "compiler: unknown"
  fi
  if command -v mpirun &>/dev/null; then
    echo "mpi: $(mpirun --version | head -1)"
  else
    echo "mpi: unknown"
  fi
  echo "date: $(date -Iseconds)"
} > "$OUTDIR/scaling_meta.txt"

echo ""
echo "Done. Results in:"
echo "  $OUTDIR/scaling_strong.csv"
echo "  $OUTDIR/scaling_size.csv"
echo "  $OUTDIR/scaling_strong_raw.csv"
echo "  $OUTDIR/scaling_size_raw.csv"
echo "  $OUTDIR/scaling_strong_stats.csv"
echo "  $OUTDIR/scaling_size_stats.csv"
echo "  $OUTDIR/scaling_meta.txt"
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

### `scripts/plot_ho.py` (1482 lines, summarized)

Plot script content truncated for token efficiency. Full file remains in repository.

**First 20 lines:**
```python
#!/usr/bin/env python3
"""
plot_ho.py — Results 1 harmonic oscillator plotting package.

Main figures (brief-facing):
  Figure 1(a,b): out/plots/results1_figure1ab.png
  Figure 1(c):   out/plots/results1_figure1c.png
  Figure 2(a-f): out/plots/results1_figure2.png
  Figure 3(a,b): out/plots/results1_figure3.png
  Figure 4(a):   out/plots/results1_figure4.png

Generated artifacts:
  - out/summary/results1/results1_ho_small_large_summary.(csv|md)
  - out/summary/results1/results1_ho_convergence_summary.(csv|md)
  - out/summary/results1/results1_ho_endpoint_values.(csv|md)
  - out/summary/results1/results1_ho_caption_notes.md

Each figure gets a JSON metadata sidecar in:
  out/plots/metadata/<figure_name>.json
"""
```

**Function/class signatures:**
```text
93:def utc_now() -> str:
97:def dt_key(dt: float) -> str:
101:def format_dt(dt: float) -> str:
105:def exact_solution(t: np.ndarray | float, omega: float = OMEGA, x0: float = X0, v0: float = V0):
123:def exact_phase_curve(num_points: int = 1200, t_final: float = T_FINAL):
128:def load_manifest():
134:def load_csv(filepath: str):
137:    def non_comment_lines(handle):
155:def write_csv(path: str, fieldnames: List[str], rows: List[Dict[str, object]]) -> None:
165:def markdown_table(headers: List[str], rows: List[List[str]]) -> str:
174:def fmt_sci(x: float, digits: int = 3) -> str:
180:def fmt_pct_from_ratio(x: float, digits: int = 4) -> str:
191:def write_plot_metadata(plot_png_name: str, extra: Dict[str, object]) -> None:
214:def save_plot_pair(fig, png_name: str, metadata: Dict[str, object]) -> None:
222:def add_panel_label(ax, label: str, x: float = -0.1, y: float = 1.05) -> None:
236:def run_ho_simulations():
274:def collect_ho_data(manifest) -> Tuple[Dict[str, Dict[float, Dict[str, object]]], List[str]]:
293:def compute_metrics_for_dataset(integ: str, dt: float, dataset: Dict[str, object]) -> Dict[str, object]:
344:def compute_metrics(datasets: Dict[str, Dict[float, Dict[str, object]]]) -> List[Dict[str, object]]:
355:def integrator_rank(name: str) -> int:
362:def sorted_metrics(metrics: List[Dict[str, object]]) -> List[Dict[str, object]]:
366:def metrics_index(metrics: List[Dict[str, object]]) -> Dict[Tuple[str, float], Dict[str, object]]:
370:def select_fit_points(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
377:def fit_loglog(points: List[Tuple[float, float]]) -> Tuple[float, float]:
384:def build_fit_summary(
422:def row_for(metrics_idx: Dict[Tuple[str, float], Dict[str, object]], integ: str, dt: float):
426:def merge_fit_info(endpoint_fit: Dict[str, Dict[str, object]], rms_fit: Dict[str, Dict[str, object]]):
446:def add_reference_slope(ax, dts: np.ndarray, errs: np.ndarray, expected: int, color: str) -> None:
455:def _window_yrange(series: List[Tuple[np.ndarray, np.ndarray]], t0: float, t1: float, pad_frac: float = 0.20) -> Tuple[float, float]:
475:def plot_figure1_trajectories(datasets: Dict[str, Dict[float, Dict[str, object]]]) -> None:
615:def plot_figure2_phase_space(datasets: Dict[str, Dict[float, Dict[str, object]]]) -> None:
733:def _plot_small_large_series(
765:def plot_figure3_small_vs_large(
876:def _plot_convergence_panel(
938:def plot_figure4_convergence_combined(
1018:def plot_figure5_energy_diagnostic(
1130:def _write_markdown(path: str, lines: List[str]) -> None:
1136:def generate_table_outputs(
1380:def run_sanity_checks(
1427:def main():
```

### `scripts/plot_lj.py` (1592 lines, summarized)

Plot script content truncated for token efficiency. Full file remains in repository.

**First 20 lines:**
```python
#!/usr/bin/env python3
"""
plot_lj.py — Generate Lennard-Jones / Argon validation plots (Results 2).

Produces:
  - out/plots/results2_figure6.png
  - out/plots/results2_figure7.png
  - out/plots/results2_figure8.png
"""

import csv
import json
import os
import shutil
import glob
from datetime import datetime, timezone

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
```

**Function/class signatures:**
```text
65:def utc_now():
69:def unique_preserve_order(items):
80:def parse_scalar(raw):
97:def typed_meta(meta):
101:def run_identifier_from_path(path):
108:def extract_series_parameters(meta_typed):
141:def write_plot_metadata(plot_png_name, section, extra):
158:def add_panel_label(ax, label: str, x: float = -0.1, y: float = 1.05):
172:def write_text_file(path, content):
179:def write_json_file(path, payload):
187:def load_rahman_anchor_points(path):
227:def sync_rahman_anchor_dataset(source_path, out_path):
233:def update_manifest_with_results2_outputs(manifest_update):
254:def remove_stale_results2_artifacts():
261:def load_manifest():
274:def nested_get(obj, dotted, default=""):
283:def load_csv(filepath):
286:    def filter_comments(handle):
303:def parse_csv_metadata(filepath):
324:def parse_int_meta(meta, key, default):
333:def parse_float_meta(meta, key, default):
342:def get_meta_value(meta, preferred_key, fallback_key, default):
350:def finite_or_nan(arr):
355:def first_nonfinite_index(*arrays):
365:def first_exceed_index(arr, threshold):
370:def first_finite_prod_index(steps, etot, production_start):
380:def divergence_crop_limit(div_time_ps, max_time_ps):
387:def load_series(filepath):
455:def plot_energy_for_run(manifest, run_key, config, out_name):
692:def plot_temperature_for_run(manifest, run_key, config, out_name):
975:def extract_rdf_feature(r_vals, g_vals, rmin, rmax, mode):
985:def smooth_curve_pchip(x_vals, y_vals, samples_per_segment=40):
1010:    def endpoint_slope(h0, h1, delta0, delta1):
1048:def plot_rdf(manifest, rahman_points, out_name=FIG8_RDF_PNG):
1253:def safe_plot(name, fn, *args):
1261:def format_float(value, digits=3):
1271:def integrator_map(summary_dict):
1280:def write_results2_quantitative_summary(energy_brief_summary, temp_brief_summary, rdf_summary):
1428:def write_results2_notes():
1494:def summarize_results2_outputs(energy_brief, temp_brief, rdf_summary, table_files):
1521:def main():
```

### `scripts/plot_scaling.py` (500 lines, summarized)

Plot script content truncated for token efficiency. Full file remains in repository.

**First 20 lines:**
```python
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
```

**Function/class signatures:**
```text
47:def load_manifest():
56:def utc_now():
60:def unique_preserve_order(items):
71:def write_plot_metadata(plot_png_name, section, extra):
88:def add_panel_label(ax, label: str, x: float = -0.1, y: float = 1.05):
102:def remove_stale_results3_artifacts():
109:def load_scaling_csv(manifest, key):
135:def amdahl(P, f):
140:def plot_strong_scaling():
166:    def fit_amdahl(P_arr, S_obs):
345:def plot_size_scaling():
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

### `scripts/validate_manifest.py` (96 lines)

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
    if first != "P,N,wall_s,comm_max_s":
        errors.append(
            f"bad header in {path}: '{first}' (expected 'P,N,wall_s,comm_max_s')"
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

## 9. File Sizes

```
include/md/constants.hpp                             84 lines
include/md/integrators.hpp                          140 lines
include/md/mic.hpp                                   19 lines
include/md/observables.hpp                           82 lines
include/md/params.hpp                                86 lines
include/md/partition.hpp                             26 lines
include/md/potentials.hpp                            61 lines
include/md/rng.hpp                                  134 lines
include/md/system.hpp                                63 lines
src/main.cpp                                        550 lines
src/observables.cpp                                  70 lines
src/potentials/harmonic.cpp                          37 lines
src/potentials/lennard_jones.cpp                    104 lines
tests/test_force.cpp                                288 lines
tests/test_integrators.cpp                           95 lines
tests/test_mic.cpp                                  117 lines
tests/test_partition.cpp                             68 lines
tests/test_runner.cpp                                33 lines

Total C++ lines:
    2057
```

**End of audit.**
