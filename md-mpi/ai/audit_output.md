# Audit Output — WA2 MPI MD Solver

## 1. Metadata

| Field | Value |
|-------|-------|
| Timestamp (UTC) | 2026-03-04T14:17:09Z |
| Git commit | a5d11719079a76f5dabe4c6d25113aba068fcec5 |
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
./ai/analyse_results.py
./ai/archive/claude.md
./ai/archive/code.md
./ai/archive/constraints.md
./ai/archive/current_code.md
./ai/archive/task_overview.md
./ai/audit_output.md
./ai/audit.sh
./ai/generate_all_context.sh
./ai/make_results.sh
./ai/pack_context.sh
./ai/pack_results.sh
./ai/results_bundle.md
./ai/results.md
./include/md/constants.hpp
./include/md/integrators.hpp
./include/md/mic.hpp
./include/md/mpi_context.hpp
./include/md/observables.hpp
./include/md/params.hpp
./include/md/potentials.hpp
./include/md/rng.hpp
./include/md/system.hpp
./Makefile
./md_solver
./README.md
./scripts/append_manifest.py
./scripts/check_tolerance.py
./scripts/plot_ho.py
./scripts/plot_lj.py
./scripts/plot_scaling.py
./scripts/run_all_data.sh
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
total 1064
drwxr-xr-x@ 10 felix  staff     320 Mar  4 14:17 .
drwxr-xr-x   6 felix  staff     192 Mar  4 14:17 ..
-rw-r--r--@  1 felix  staff   71663 Mar  4 14:17 ho_convergence.png
-rw-r--r--@  1 felix  staff   44775 Mar  4 14:17 ho_energy.png
-rw-r--r--@  1 felix  staff  112160 Mar  4 14:17 ho_trajectories.png
-rw-r--r--   1 felix  staff   98238 Mar  4 14:17 lj_energy.png
-rw-r--r--   1 felix  staff   65154 Mar  4 14:17 lj_equilibrated_comparison.png
-rw-r--r--   1 felix  staff   30632 Mar  4 14:17 lj_rdf.png
-rw-r--r--   1 felix  staff   42276 Mar  4 14:17 lj_temperature.png
-rw-r--r--   1 felix  staff   65764 Mar  4 14:17 scaling_strong.png
```

### out/manifest.json
```json
{
  "ho_convergence": {
    "euler_dt1_0": "out/runs/ho_N1_euler_dt1.0_20260304_141600/ho_euler.csv",
    "euler_dt0_5": "out/runs/ho_N1_euler_dt0.5_20260304_141600/ho_euler.csv",
    "euler_dt0_1": "out/runs/ho_N1_euler_dt0.1_20260304_141600/ho_euler.csv",
    "euler_dt0_05": "out/runs/ho_N1_euler_dt0.05_20260304_141600/ho_euler.csv",
    "euler_dt0_01": "out/runs/ho_N1_euler_dt0.01_20260304_141600/ho_euler.csv",
    "euler_dt0_005": "out/runs/ho_N1_euler_dt0.005_20260304_141600/ho_euler.csv",
    "euler_dt0_001": "out/runs/ho_N1_euler_dt0.001_20260304_141600/ho_euler.csv",
    "euler_dt0_0005": "out/runs/ho_N1_euler_dt0.0005_20260304_141600/ho_euler.csv",
    "verlet_dt1_0": "out/runs/ho_N1_verlet_dt1.0_20260304_141600/ho_verlet.csv",
    "verlet_dt0_5": "out/runs/ho_N1_verlet_dt0.5_20260304_141600/ho_verlet.csv",
    "verlet_dt0_1": "out/runs/ho_N1_verlet_dt0.1_20260304_141600/ho_verlet.csv",
    "verlet_dt0_05": "out/runs/ho_N1_verlet_dt0.05_20260304_141600/ho_verlet.csv",
    "verlet_dt0_01": "out/runs/ho_N1_verlet_dt0.01_20260304_141600/ho_verlet.csv",
    "verlet_dt0_005": "out/runs/ho_N1_verlet_dt0.005_20260304_141600/ho_verlet.csv",
    "verlet_dt0_001": "out/runs/ho_N1_verlet_dt0.001_20260304_141600/ho_verlet.csv",
    "verlet_dt0_0005": "out/runs/ho_N1_verlet_dt0.0005_20260304_141600/ho_verlet.csv",
    "rk4_dt1_0": "out/runs/ho_N1_rk4_dt1.0_20260304_141600/ho_rk4.csv",
    "rk4_dt0_5": "out/runs/ho_N1_rk4_dt0.5_20260304_141600/ho_rk4.csv",
    "rk4_dt0_1": "out/runs/ho_N1_rk4_dt0.1_20260304_141600/ho_rk4.csv",
    "rk4_dt0_05": "out/runs/ho_N1_rk4_dt0.05_20260304_141600/ho_rk4.csv",
    "rk4_dt0_01": "out/runs/ho_N1_rk4_dt0.01_20260304_141600/ho_rk4.csv",
    "rk4_dt0_005": "out/runs/ho_N1_rk4_dt0.005_20260304_141600/ho_rk4.csv",
    "rk4_dt0_001": "out/runs/ho_N1_rk4_dt0.001_20260304_141600/ho_rk4.csv",
    "rk4_dt0_0005": "out/runs/ho_N1_rk4_dt0.0005_20260304_141600/ho_rk4.csv"
  },
  "lj_production": {
    "verlet_100": "out/runs/lj_N864_P4_verlet_100_20260304_141600/lj_verlet.csv",
    "euler_100": "out/runs/lj_N864_P4_euler_100_20260304_141600/lj_euler.csv",
    "verlet_200_equilibrated": "out/runs/lj_N864_P4_verlet_200_eq_20260304_141600/lj_verlet.csv"
  },
  "lj_gr": "out/runs/lj_N864_P4_gr_20260304_141600/gr.csv",
  "lj_gr_energy": "out/runs/lj_N864_P4_gr_20260304_141600/lj_verlet.csv",
  "scaling": {
    "strong": "out/scaling_strong.csv"
  }
}
```

### out/runs/ directories
```
out/runs/ho_N1_euler_dt0.0005_20260304_141600/
out/runs/ho_N1_euler_dt0.001_20260304_141600/
out/runs/ho_N1_euler_dt0.005_20260304_141600/
out/runs/ho_N1_euler_dt0.01_20260304_141600/
out/runs/ho_N1_euler_dt0.05_20260304_141600/
out/runs/ho_N1_euler_dt0.1_20260304_141600/
out/runs/ho_N1_euler_dt0.5_20260304_141600/
out/runs/ho_N1_euler_dt1.0_20260304_141600/
out/runs/ho_N1_rk4_dt0.0005_20260304_141600/
out/runs/ho_N1_rk4_dt0.001_20260304_141600/
out/runs/ho_N1_rk4_dt0.005_20260304_141600/
out/runs/ho_N1_rk4_dt0.01_20260304_141600/
out/runs/ho_N1_rk4_dt0.05_20260304_141600/
out/runs/ho_N1_rk4_dt0.1_20260304_141600/
out/runs/ho_N1_rk4_dt0.5_20260304_141600/
out/runs/ho_N1_rk4_dt1.0_20260304_141600/
out/runs/ho_N1_verlet_dt0.0005_20260304_141600/
out/runs/ho_N1_verlet_dt0.001_20260304_141600/
out/runs/ho_N1_verlet_dt0.005_20260304_141600/
out/runs/ho_N1_verlet_dt0.01_20260304_141600/
out/runs/ho_N1_verlet_dt0.05_20260304_141600/
out/runs/ho_N1_verlet_dt0.1_20260304_141600/
out/runs/ho_N1_verlet_dt0.5_20260304_141600/
out/runs/ho_N1_verlet_dt1.0_20260304_141600/
out/runs/lj_N108_P1_test_20260304_141600/
out/runs/lj_N108_P2_test_20260304_141600/
out/runs/lj_N864_P4_euler_100_20260304_141600/
out/runs/lj_N864_P4_gr_20260304_141600/
out/runs/lj_N864_P4_verlet_100_20260304_141600/
out/runs/lj_N864_P4_verlet_200_eq_20260304_141600/
```

## 3. Build and Warnings

```
rm -f src/main.o src/potentials/harmonic.o src/potentials/lennard_jones.o src/observables.o tests/test_runner.o tests/test_mic.o tests/test_force.o src/potentials/lennard_jones.o src/potentials/harmonic.o src/observables.o md_solver test_runner
rm -f src/integrators/*.o src/potentials/*.o tests/*.o

mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/main.o src/main.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/potentials/harmonic.o src/potentials/harmonic.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/potentials/lennard_jones.o src/potentials/lennard_jones.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/observables.o src/observables.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -o md_solver src/main.o src/potentials/harmonic.o src/potentials/lennard_jones.o src/observables.o
```

**Build status:** SUCCESS

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
rm -f src/integrators/*.o src/potentials/*.o tests/*.o
make: Nothing to be done for `all'.
```

**Warnings found:** 0

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

**Test status:** ALL PASSED

## 5. Smoke Runs

### 5a. HO — Velocity-Verlet (N=1, 1000 steps, dt=0.01, T_final≈10)

```
=== MD Solver ===
Mode: ho | Integrator: verlet
N = 1 | P = 1 | steps = 1000 | dt = 1.000e-02
L = 1.000000e+10 m (29411764705882353664.0000 sigma)
==================
Wall time: 0.003291 s (max across 1 ranks)
```

**Output (first 6 + last 3 lines):**
```
# mode: ho, integrator: verlet, N: 1, P: 1, dt: 0.01, steps: 1000, seed: 42, L: 10000000000, rcut: 7.65e-10, timestamp: 2026-03-04T14:17:14Z
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
=== MD Solver ===
Mode: ho | Integrator: rk4
N = 1 | P = 1 | steps = 1000 | dt = 1.000e-02
L = 1.000000e+10 m (29411764705882353664.0000 sigma)
==================
Wall time: 0.003906 s (max across 1 ranks)
```

**Output (first 6 + last 3):**
```
# mode: ho, integrator: rk4, N: 1, P: 1, dt: 0.01, steps: 1000, seed: 42, L: 10000000000, rcut: 7.65e-10, timestamp: 2026-03-04T14:17:15Z
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
=== MD Solver ===
Mode: ho | Integrator: euler
N = 1 | P = 1 | steps = 1000 | dt = 1.000e-02
L = 1.000000e+10 m (29411764705882353664.0000 sigma)
==================
Wall time: 0.003305 s (max across 1 ranks)
```

**Output (first 6 + last 3):**
```
# mode: ho, integrator: euler, N: 1, P: 1, dt: 0.01, steps: 1000, seed: 42, L: 10000000000, rcut: 7.65e-10, timestamp: 2026-03-04T14:17:15Z
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
=== MD Solver ===
Mode: lj | Integrator: verlet
N = 108 | P = 1 | steps = 10 | dt = 1.000e-14
L = 1.738930e-09 m (5.1145 sigma)
T_init = 94.4 K | seed = 42
==================
Wall time: 0.000461 s (max across 1 ranks)
```

**Output:**
```
# mode: lj, integrator: verlet, N: 108, P: 1, dt: 1e-14, steps: 10, seed: 42, L: 1.73893e-09, rcut: 7.65e-10, timestamp: 2026-03-04T14:17:15Z
step,time,E_kin,E_pot,E_total,temperature
0,0,2.09184891288e-19,-1.12926090964738e-18,-9.20076018359379e-19,94.4
1,1e-14,2.08952940324273e-19,-1.12903036097961e-18,-9.20077420655337e-19,94.2953262310627
2,2e-14,2.08327769566247e-19,-1.12840771146898e-18,-9.20079941902733e-19,94.0132020336875
3,3e-14,2.07279814481113e-19,-1.12736342912362e-18,-9.20083614642506e-19,93.5402856608675
4,4e-14,2.05766417434535e-19,-1.12585487169448e-18,-9.20088454259947e-19,92.8573267706855
5,5e-14,2.03732045550683e-19,-1.12382647756107e-18,-9.20094432010392e-19,91.9392647411899
6,6e-14,2.01109299736099e-19,-1.121210730094e-18,-9.20101430357899e-19,90.7556840180687
7,7e-14,1.9782137105245e-19,-1.11793054604546e-18,-9.20109174993009e-19,89.2719226152952
8,8e-14,1.93788239467119e-19,-1.11385504380398e-18,-9.2006680433686e-19,87.4518694589177
9,9e-14,1.88932451387229e-19,-1.10900656536631e-18,-9.20074113979076e-19,85.2605716461588
10,1e-13,1.83193844160901e-19,-1.10332388832566e-18,-9.20130044164762e-19,82.6708792509294
```

### 5e. LJ — Euler (N=108, 10 steps, P=1)

```
=== MD Solver ===
Mode: lj | Integrator: euler
N = 108 | P = 1 | steps = 10 | dt = 1.000e-14
L = 1.738930e-09 m (5.1145 sigma)
T_init = 94.4 K | seed = 42
==================
Wall time: 0.000468 s (max across 1 ranks)
```

**Output:**
```
# mode: lj, integrator: euler, N: 108, P: 1, dt: 1e-14, steps: 10, seed: 42, L: 1.73893e-09, rcut: 7.65e-10, timestamp: 2026-03-04T14:17:15Z
step,time,E_kin,E_pot,E_total,temperature
0,0,2.09184891288e-19,-1.12926090964738e-18,-9.20076018359379e-19,94.4
1,1e-14,2.09144192886232e-19,-1.12902994241994e-18,-9.19885749533712e-19,94.3816338115854
2,2e-14,2.08721895925538e-19,-1.12840586521172e-18,-9.19683969286181e-19,94.1910615726245
3,3e-14,2.07894523992715e-19,-1.12735747207365e-18,-9.19462948080934e-19,93.8176889548529
4,4e-14,2.06625321584501e-19,-1.12583963303995e-18,-9.19214311455453e-19,93.2449291030409
5,5e-14,2.04864000685478e-19,-1.12379287250225e-18,-9.18928871816775e-19,92.4500882718317
6,6e-14,2.02546939150224e-19,-1.12114343244424e-18,-9.18596493294018e-19,91.4044553507292
7,7e-14,1.99598314327998e-19,-1.11780435151736e-18,-9.1820603718936e-19,90.0738134410563
8,8e-14,1.95932967946968e-19,-1.11362950215605e-18,-9.17696534209077e-19,88.4197327077934
9,9e-14,1.91464855324552e-19,-1.10861809339369e-18,-9.17153238069135e-19,86.4033833005344
10,1e-13,1.86109378411333e-19,-1.10262544990855e-18,-9.16516071497222e-19,83.986588198866
```

### 5f. MPI Consistency — P=1 vs P=2 (N=108, 5 steps, Verlet)

```
=== MD Solver ===
Mode: lj | Integrator: verlet
N = 108 | P = 1 | steps = 5 | dt = 1.000e-14
L = 1.738930e-09 m (5.1145 sigma)
T_init = 94.4 K | seed = 42
==================
Wall time: 0.000407 s (max across 1 ranks)
=== MD Solver ===
Mode: lj | Integrator: verlet
N = 108 | P = 2 | steps = 5 | dt = 1.000e-14
L = 1.738930e-09 m (5.1145 sigma)
T_init = 94.4 K | seed = 42
==================
Wall time: 0.004498 s (max across 2 ranks)
MATCH
```

## 6. CLI Defaults vs. Brief Requirements

### CLI help output
```
Usage: mpirun -np P ./md_solver [options]

Options:
  --N <int>            Number of particles (default: 864)
  --steps <int>        Number of timesteps (default: 100)
  --dt <double>        Timestep (default: 1e-14)
  --T <double>         Initial temperature [K] (default: 94.4)
  --omega <double>     HO angular frequency (default: 1.0)
  --integrator <str>   euler, rk4, verlet (default: verlet)
  --mode <str>         ho, lj (default: lj)
  --no-output          Disable CSV output
  --seed <int>         RNG seed (default: 42)
  --rescale-step <int> Step for single velocity rescale (default: disabled)
  --timing             Enable timing mode (implies --no-output)
  --gr                 Enable g(r) accumulation (LJ only)
  --gr-discard <int>   Equilibration steps to discard (default: 500)
  --gr-interval <int>  Sample g(r) every N steps (default: 10)
  --outdir <str>       Output directory for generated CSVs
  --help               Print this message and exit
```

### Comparison

| Parameter | CLI Default | Brief Requirement | Match? |
|-----------|------------|-------------------|--------|
| N         | 864        | 864               | YES    |
| steps     | 100        | 100               | YES    |
| dt        | 1e-14      | 1e-14             | YES    |
| mode      | lj         | lj                | YES    |
| integrator| verlet     | verlet             | YES   |
| T_init    | 94.4 K     | 94.4 K            | YES    |

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
	rm -f src/integrators/*.o src/potentials/*.o tests/*.o

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

### `README.md` (87 lines)

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
# Primary run: 100 steps, Velocity-Verlet (single rescale at step 10)
mkdir -p out
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --steps 100 --rescale-step 10

# Primary run: 100 steps, Euler (single rescale at step 10)
mpirun -np 4 ./md_solver --mode lj --integrator euler --N 864 --steps 100 --rescale-step 10

# Equilibrated comparison run (rescale at 100, then post-rescale NVE segment)
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --steps 200 --rescale-step 100

# Supplementary g(r) (extended run, ~450 frames for smooth Rahman comparison)
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --steps 25500 --rescale-step 10 --gr --gr-discard 500 --gr-interval 10
```

### Scaling (Results 3)

```bash
# Recommended: use the automation script (median-of-10 paired runs)
bash scripts/run_all_data.sh

# Direct timing examples (single run each):
mpirun -np 1  ./md_solver --mode lj --integrator verlet --N 2048 --steps 200 --timing
mpirun -np 16 ./md_solver --mode lj --integrator verlet --N 864  --steps 500 --timing
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
ai/            — AI context workspace (excluded from submission)
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

// ── Derived quantities for optimised LJ kernel ──

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

// ── Magic numbers extracted from codebase ──

/// Fraction of sigma for random initial position perturbation
constexpr double fccPerturbation = 0.01;

/// g(r) histogram bin width in units of sigma
constexpr double grBinWidthSigma = 0.02;

/// Box size for HO mode (non-periodic; effectively unused but kept finite as a safety guard)
constexpr double L_ho_dummy = 1.0e10;

/// Lower bound numerical guard for temperature rescaling
constexpr double rescaleGuard = 1e-30;

// ── Rahman (1964) reference state point ──

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

### `include/md/params.hpp` (182 lines)

```cpp
/**
 * @file params.hpp
 * @brief Runtime parameter struct and CLI argument parser.
 *
 * All simulation parameters are configurable via command-line arguments.
 * No recompilation is needed to change N, dt, integrator, etc.
 */

#ifndef MD_PARAMS_HPP
#define MD_PARAMS_HPP

#include <cstdlib>
#include <iostream>
#include <string>

namespace md {

/// Parse result status (avoids std::exit before MPI_Finalize)
enum class ParseStatus { Ok, Help, Error };

static bool nextVal(int& i, int argc, const char* flag) {
    if (++i >= argc) {
        std::cerr << "Missing value for " << flag << "\n";
        return false;
    }
    return true;
}

/**
 * @brief Simulation parameters, parsed from command-line arguments.
 */
struct Params {
    int N = 864;                        ///< Number of particles
    int steps = 100;                    ///< Number of timesteps
    double dt = 1.0e-14;                ///< Timestep [s] (for LJ) or dimensionless (for HO)
    double T_init = 94.4;               ///< Initial temperature [K]
    double omega = 1.0;                 ///< HO angular frequency (only for mode "ho")
    std::string integrator = "verlet";  ///< "euler", "rk4", "verlet"
    std::string mode = "lj";            ///< "ho" or "lj"
    bool output = true;                 ///< Enable CSV output
    int seed = 42;                      ///< RNG seed for reproducibility
    int rescaleStep = -1;               ///< Step at which to apply optional rescale (-1 = disabled)
    bool timing = false;                ///< Enable wall-clock timing (disables output)
    bool gr = false;                    ///< Enable g(r) accumulation
    int grDiscard = 500;                ///< Number of equilibration steps to discard before g(r)
    int grInterval = 10;                ///< Sample g(r) every N steps after discard
    std::string outdir = "";            ///< Output directory for per-run namespaces

    /**
     * @brief Parse command-line arguments into a Params struct.
     *
     * Validates mode ∈ {ho, lj} and integrator ∈ {euler, rk4, verlet}.
     *
     * @param argc   Argument count
     * @param argv   Argument values
     * @param[out] p Parsed Params struct
     * @return ParseStatus::Ok on success, Help or Error otherwise
     */
    static ParseStatus parse(int argc, char* argv[], Params& p) {
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg == "--help") {
                printUsage(argv[0]);
                return ParseStatus::Help;
            } else if (arg == "--N") {
                if (nextVal(i, argc, "--N"))
                    p.N = std::atoi(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--steps") {
                if (nextVal(i, argc, "--steps"))
                    p.steps = std::atoi(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--dt") {
                if (nextVal(i, argc, "--dt"))
                    p.dt = std::atof(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--T") {
                if (nextVal(i, argc, "--T"))
                    p.T_init = std::atof(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--omega") {
                if (nextVal(i, argc, "--omega"))
                    p.omega = std::atof(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--integrator") {
                if (nextVal(i, argc, "--integrator"))
                    p.integrator = argv[i];
                else
                    return ParseStatus::Error;
            } else if (arg == "--mode") {
                if (nextVal(i, argc, "--mode"))
                    p.mode = argv[i];
                else
                    return ParseStatus::Error;
            } else if (arg == "--no-output") {
                p.output = false;
            } else if (arg == "--seed") {
                if (nextVal(i, argc, "--seed"))
                    p.seed = std::atoi(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--outdir") {
                if (nextVal(i, argc, "--outdir"))
                    p.outdir = argv[i];
                else
                    return ParseStatus::Error;
            } else if (arg == "--rescale-step") {
                if (nextVal(i, argc, "--rescale-step"))
                    p.rescaleStep = std::atoi(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--timing") {
                p.timing = true;
                p.output = false;
            } else if (arg == "--gr") {
                p.gr = true;
            } else if (arg == "--gr-discard") {
                if (nextVal(i, argc, "--gr-discard"))
                    p.grDiscard = std::atoi(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--gr-interval") {
                if (nextVal(i, argc, "--gr-interval"))
                    p.grInterval = std::atoi(argv[i]);
                else
                    return ParseStatus::Error;
            } else {
                std::cerr << "Unknown argument: " << arg << "\n";
                return ParseStatus::Error;
            }
        }

        // Validate mode
        if (p.mode != "ho" && p.mode != "lj") {
            std::cerr << "Invalid --mode '" << p.mode << "' (must be 'ho' or 'lj')\n";
            return ParseStatus::Error;
        }

        // Validate integrator
        if (p.integrator != "euler" && p.integrator != "rk4" && p.integrator != "verlet") {
            std::cerr << "Invalid --integrator '" << p.integrator
                      << "' (must be 'euler', 'rk4', or 'verlet')\n";
            return ParseStatus::Error;
        }

        return ParseStatus::Ok;
    }

    /**
     * @brief Print usage information to stdout.
     * @param progName Name of the executable.
     */
    static void printUsage(const char* progName) {
        std::cout << "Usage: mpirun -np P " << progName << " [options]\n"
                  << "\nOptions:\n"
                  << "  --N <int>            Number of particles (default: 864)\n"
                  << "  --steps <int>        Number of timesteps (default: 100)\n"
                  << "  --dt <double>        Timestep (default: 1e-14)\n"
                  << "  --T <double>         Initial temperature [K] (default: 94.4)\n"
                  << "  --omega <double>     HO angular frequency (default: 1.0)\n"
                  << "  --integrator <str>   euler, rk4, verlet (default: verlet)\n"
                  << "  --mode <str>         ho, lj (default: lj)\n"
                  << "  --no-output          Disable CSV output\n"
                  << "  --seed <int>         RNG seed (default: 42)\n"
                  << "  --rescale-step <int> Step for single velocity rescale (default: disabled)\n"
                  << "  --timing             Enable timing mode (implies --no-output)\n"
                  << "  --gr                 Enable g(r) accumulation (LJ only)\n"
                  << "  --gr-discard <int>   Equilibration steps to discard (default: 500)\n"
                  << "  --gr-interval <int>  Sample g(r) every N steps (default: 10)\n"
                  << "  --outdir <str>       Output directory for generated CSVs\n"
                  << "  --help               Print this message and exit\n";
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

### `include/md/rng.hpp` (139 lines)

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
        double z1 = mag * std::cos(2.0 * M_PI * u2);
        double z2 = mag * std::sin(2.0 * M_PI * u2);

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

### `include/md/potentials.hpp` (64 lines)

```cpp
/**
 * @file potentials.hpp
 * @brief Harmonic Oscillator and Lennard-Jones force/energy kernels.
 *
 * Both potentials implement a common interface:
 *   computeForces(system, posGlobal, localPE)
 *
 * The HO potential computes F = -omega^2 * x purely locally, ignoring
 * the global position data. The LJ potential uses the global positions
 * from MPI_Allgatherv with minimum image convention and hard cutoff.
 */

#ifndef MD_POTENTIALS_HPP
#define MD_POTENTIALS_HPP

#include <vector>

#include "md/system.hpp"

namespace md {

/**
 * @brief Compute harmonic oscillator forces for local particles.
 *
 * F_i = -omega^2 * x_i  (independent, non-interacting particles)
 *
 * This kernel operates purely on local data and does NOT require any
 * global position information. The MPI_Allgatherv call should be
 * bypassed entirely in HO mode to eliminate unnecessary O(N)
 * communication overhead.
 *
 * @param[in,out] sys       System state (forces written to sys.acc)
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

### `src/main.cpp` (385 lines)

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
#include <fstream>
#include <functional>
#include <iomanip>
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

    // ── Parse parameters (never calls std::exit — returns status) ──
    md::Params params;
    md::ParseStatus status = md::Params::parse(argc, argv, params);

    if (status != md::ParseStatus::Ok) {
        MPI_Finalize();
        return (status == md::ParseStatus::Help) ? 0 : 1;
    }

    // ── Initialise MPI context and particle decomposition ──
    md::MPIContext ctx;
    ctx.init(params.N);
    ctx.timingMode = params.timing;

    const bool isHO = (params.mode == "ho");
    const int N = params.N;

    // ── Compute box side length ──
    // For LJ: scale from Rahman's L=10.229*sigma for N=864 to maintain constant density
    // For HO: L is irrelevant (non-interacting), set to a large value
    double L;
    if (isHO) {
        L = md::constants::L_ho_dummy;  // effectively unused for HO
    } else {
        L = md::constants::L_sigma_rahman * md::constants::sigma *
            std::cbrt(static_cast<double>(N) / md::constants::N_rahman);
    }

    // ── Generate initial conditions on rank 0, broadcast to all ──
    std::vector<double> posAll(3 * N, 0.0);
    std::vector<double> velAll(3 * N, 0.0);
    int fccError = 0;  // broadcast from root to all ranks (LJ only)

    if (ctx.isRoot()) {
        if (isHO) {
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
                velAll = md::generateVelocities(N, params.T_init, md::constants::mass, gen);
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

    // ── Initialise local system state ──
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

    // ── Wrap positions into [0, L) ──
    if (!isHO) {
        sys.wrapPositions();
        ctx.allgatherPositions(sys.pos);
    }

    // ── Build force function (binds potential-specific parameters) ──
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

    // ── Initial force evaluation ──
    double localPE = 0.0;
    if (isHO) {
        evalHO(sys, ctx.posGlobal, localPE);
    } else {
        evalLJ(sys, ctx.posGlobal, localPE);
    }

    // ── Create output directory and open file (rank 0 only) ──
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
                    << ", steps: " << params.steps << ", seed: " << params.seed << ", L: " << L
                    << ", rcut: " << md::constants::rcut_sigma * md::constants::sigma
                    << ", timestamp: " << tstr << "\n";
            if (isHO) {
                // HO: output position, velocity, energy for phase-space & convergence plots
                outFile << "step,time,x,v,E_kin,E_pot,E_total\n";
            } else {
                outFile << "step,time,E_kin,E_pot,E_total,temperature\n";
            }
        }
    }

    // ── Print simulation info (rank 0) ──
    if (ctx.isRoot() && !params.timing) {
        std::printf("=== MD Solver ===\n");
        std::printf("Mode: %s | Integrator: %s\n", params.mode.c_str(), params.integrator.c_str());
        std::printf("N = %d | P = %d | steps = %d | dt = %.3e\n", N, ctx.size, params.steps,
                    params.dt);
        std::printf("L = %.6e m (%.4f sigma)\n", L, L / md::constants::sigma);
        if (!isHO) {
            std::printf("T_init = %.1f K | seed = %d\n", params.T_init, params.seed);
        }
        std::printf("==================\n");
    }

    // ── g(r) histogram setup (LJ only) ──
    // Keep HO mode at zero-sized buffers to avoid meaningless allocations.
    const double grDr = md::constants::grBinWidthSigma * md::constants::sigma;  // bin width
    const double grRMax = isHO ? 0.0 : 0.5 * L;                                  // [0, L/2] for LJ
    const int grNBins = isHO ? 0 : static_cast<int>(grRMax / grDr);
    std::vector<double> grHistLocal(grNBins, 0.0);
    int grFrames = 0;

    // ── Timing setup ──
    MPI_Barrier(MPI_COMM_WORLD);
    double tStart = MPI_Wtime();

    // ── Time-stepping loop ──
    for (int step = 0; step <= params.steps; ++step) {
        // ── Compute observables (skip entirely in timing mode for clean benchmarks) ──
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

            // ── Single-step Velocity Rescaling ──
            if (step == params.rescaleStep && !isHO) {
                double lambda = 1.0;
                if (ctx.isRoot()) {
                    double tMeasured = md::computeTemperature(totalKE, N);
                    if (tMeasured > md::constants::rescaleGuard) {
                        lambda = std::sqrt(params.T_init / tMeasured);
                    }
                    if (!params.timing) {
                        std::printf(
                            "Rescale at step %d: lambda = %.15e, T_before = %.6f K, T_after = %.6f "
                            "K\n",
                            step, lambda, tMeasured, params.T_init);
                    }
                }
                MPI_Bcast(&lambda, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
                for (int i = 0; i < 3 * sys.localN; ++i) {
                    sys.vel[i] *= lambda;
                }
            }
        }

        // ── Accumulate g(r) histogram (LJ only, after equilibration) ──
        if (params.gr && !isHO && step >= params.grDiscard &&
            (step - params.grDiscard) % params.grInterval == 0) {
            md::accumulateGR(ctx.posGlobal, N, L, ctx.offset, ctx.localN, grDr, grRMax,
                             grHistLocal);
            ++grFrames;
        }

        // ── Advance one timestep (skip on the last iteration — we only want observables) ──
        if (step == params.steps)
            break;

        // 6-way dispatch: necessary to avoid std::function virtual dispatch overhead in the hot
        // loop
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
        } else {  // Verlet (default)
            if (isHO)
                md::stepVelocityVerlet(sys, ctx, params.dt, evalHO, localPE, isHO);
            else
                md::stepVelocityVerlet(sys, ctx, params.dt, evalLJ, localPE, isHO);
        }
    }

    // ── Timing completion ──
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

    // ── Write g(r) to file (LJ only) ──
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
                       << ", steps: " << params.steps << ", seed: " << params.seed << ", L: " << L
                       << ", rcut: " << md::constants::rcut_sigma * md::constants::sigma
                       << ", timestamp: " << tstr << "\n";
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
    }

    // ── Close output file ──
    if (outFile.is_open()) {
        outFile.close();
    }

    MPI_Finalize();
    return 0;
}
```

### `src/potentials/harmonic.cpp` (35 lines)

```cpp
/**
 * @file harmonic.cpp
 * @brief Harmonic Oscillator force/energy kernel.
 *
 * F_i = -omega^2 * x_i  (each component independently)
 * V_i = 0.5 * omega^2 * x_i^2
 *
 * This is a non-interacting potential: particles do not see each other.
 * The MPI_Allgatherv collective is bypassed entirely in HO mode.
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

### `src/potentials/lennard_jones.cpp` (100 lines)

```cpp
/**
 * @file lennard_jones.cpp
 * @brief Lennard-Jones force and potential energy kernel.
 *
 * Implements U(r) = 4*eps*[(sigma/r)^12 - (sigma/r)^6] via
 * invR2 → invR6 → invR12 (no pow, no sqrt in force loop).
 *
 * Hard cutoff at rcut = 2.25*sigma with branchless minimum image convention.
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

### `tests/test_mic.cpp` (116 lines)

```cpp
/**
 * @file test_mic.cpp
 * @brief Unit tests for the Minimum Image Convention.
 *
 * Tests that the branch-predictor-friendly MIC correctly wraps
 * inter-particle displacements to [-L/2, +L/2). Also tests that
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

    // ── Test 1: LJ force at potential minimum r = 2^(1/6)*sigma ──
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

    // ── Test 2: Position wrapping ──
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

    // ── Test 3: LJ force sign check ──
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

### `scripts/run_all_data.sh` (210 lines)

```sh
#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# run_all_data.sh — Generate ALL production data for the report
#
# Designed for shared HPC clusters (cerberus1). Uses median-of-10
# paired (wall, comm) repetitions for scaling benchmarks to filter contention noise.
# ──────────────────────────────────────────────────────────────────

set -euo pipefail

SOLVER="./md_solver"
OUTDIR="out"
SKIP_SCALING=0
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
mpirun -np 1 $SOLVER --mode lj --integrator verlet --N 108 --steps 10 --outdir "$D1"
mpirun -np 2 $SOLVER --mode lj --integrator verlet --N 108 --steps 10 --outdir "$D2"
if python3 scripts/check_tolerance.py "$D1/lj_verlet.csv" "$D2/lj_verlet.csv" > /dev/null 2>&1; then
    echo "  P=1 vs P=2 data: MATCH ✅"
else
    echo "  P=1 vs P=2 data: MISMATCH ❌"
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

# ── 2. Results 2: LJ Production ──
echo ""
echo "=== RESULTS 2: LJ PRODUCTION ==="
RUNDIR_V="$OUTDIR/runs/lj_N864_P4_verlet_100_${TIMESTAMP}"
mkdir -p "$RUNDIR_V"
echo "  Verlet N=864 100 steps..."
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 --steps 100 --dt 1e-14 --rescale-step 10 --outdir "$RUNDIR_V" > /dev/null
if [ -s "$RUNDIR_V/lj_verlet.csv" ]; then
    python3 scripts/append_manifest.py "lj_production.verlet_100" "$RUNDIR_V/lj_verlet.csv"
    echo "  -> output saved to manifest ✅"
fi

RUNDIR_E="$OUTDIR/runs/lj_N864_P4_euler_100_${TIMESTAMP}"
mkdir -p "$RUNDIR_E"
echo "  Euler N=864 100 steps..."
mpirun -np 4 $SOLVER --mode lj --integrator euler --N 864 --steps 100 --dt 1e-14 --rescale-step 10 --outdir "$RUNDIR_E" > /dev/null
if [ -s "$RUNDIR_E/lj_euler.csv" ]; then
    python3 scripts/append_manifest.py "lj_production.euler_100" "$RUNDIR_E/lj_euler.csv"
    echo "  -> output saved to manifest ✅"
fi

# ── Equilibrated NVE comparison ──
RUNDIR_EQ="$OUTDIR/runs/lj_N864_P4_verlet_200_eq_${TIMESTAMP}"
mkdir -p "$RUNDIR_EQ"
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 \
    --steps 200 --rescale-step 100 --outdir "$RUNDIR_EQ" > /dev/null
python3 scripts/append_manifest.py "lj_production.verlet_200_equilibrated" "$RUNDIR_EQ/lj_verlet.csv"

# ── 3. g(r) Production Run ──
echo ""
echo "=== g(r) PRODUCTION RUN ==="
RUNDIR_GR="$OUTDIR/runs/lj_N864_P4_gr_${TIMESTAMP}"
mkdir -p "$RUNDIR_GR"
# Added rescale step to avoid dropping temperature significantly
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 --steps 25500 \
    --rescale-step 10 --gr --gr-discard 500 --gr-interval 10 --outdir "$RUNDIR_GR" > /dev/null
if [ -s "$RUNDIR_GR/gr.csv" ]; then
    python3 scripts/append_manifest.py "lj_gr" "$RUNDIR_GR/gr.csv"
    python3 scripts/append_manifest.py "lj_gr_energy" "$RUNDIR_GR/lj_verlet.csv"
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
echo "=== RESULTS 3: STRONG SCALING (10 reps, N=2048, 200 steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_strong.csv"
python3 scripts/append_manifest.py "scaling.strong" "$OUTDIR/scaling_strong.csv"

REPS=10
for P in 1 2 4 8 16 24 32; do
    WALLS=""
    COMMS=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np $P $SOLVER --mode lj --integrator verlet --N 2048 --steps 200 --timing 2>/dev/null)
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

# ── 5. Size Scaling (median of 10 paired samples) ──
echo ""
echo "=== RESULTS 3: SIZE SCALING (10 reps, P=16, 500 steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_size.csv"
python3 scripts/append_manifest.py "scaling.size" "$OUTDIR/scaling_size.csv"

for N in 108 256 500 864 1372 2048; do
    WALLS=""
    COMMS=""
    for REP in $(seq 1 $REPS); do
        OUTPUT=$(mpirun -np 16 $SOLVER --mode lj --integrator verlet --N $N --steps 500 --timing 2>/dev/null)
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

### `scripts/run_scaling.sh` (114 lines)

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
STEPS=100
INTEGRATOR="verlet"
REPS=10

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
            --N "$N_STRONG" --steps "$STEPS" --timing 2>&1)

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
            --N "$N" --steps 500 --timing 2>&1)

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

### `scripts/plot_ho.py` (278 lines)

```py
#!/usr/bin/env python3
"""
plot_ho.py — Generate Harmonic Oscillator verification plots (Results 1).

Produces:
  1. Position & velocity vs time for all three integrators (with exact overlay)
  2. Phase-space (v vs x) diagrams
  3. Log-log convergence: |x_num(T) - x_exact(T)| vs dt with fitted slopes
  4. Energy conservation comparison

Usage:
  python3 scripts/plot_ho.py           # plot from existing data in out/ho/
  python3 scripts/plot_ho.py --run     # run simulations first, then plot
"""

import os
import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt

# ── Configuration ──
INTEGRATORS = ["euler", "verlet", "rk4"]
INTEGRATOR_LABELS = {"euler": "Forward Euler", "rk4": "RK4", "verlet": "Velocity-Verlet"}
INTEGRATOR_COLORS = {"euler": "#e74c3c", "rk4": "#3498db", "verlet": "#2ecc71"}
INTEGRATOR_ORDERS = {"euler": 1, "rk4": 4, "verlet": 2}

DT_VALUES = [1.0, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005]
DT_STEPS = {1.0: 10, 0.5: 20, 0.1: 100, 0.05: 200, 0.01: 1000,
            0.005: 2000, 0.001: 10000, 0.0005: 20000}
OMEGA = 1.0
T_FINAL = 10.0
TRAJ_DT = 0.01  # dt used for trajectory/phase-space plots

OUT_DIR = "out"
HO_DIR = "out/ho"
PLOT_DIR = "out/plots"


def exact_solution(t, omega=OMEGA):
    """Exact HO solution: x(t) = cos(wt), v(t) = -w*sin(wt)."""
    x = np.cos(omega * t)
    v = -omega * np.sin(omega * t)
    return x, v


def run_ho_simulations():
    """Run HO simulations for all integrators and dt values."""
    os.makedirs(HO_DIR, exist_ok=True)
    for integ in INTEGRATORS:
        for dt in DT_VALUES:
            steps = DT_STEPS[dt]
            cmd = [
                "mpirun", "-np", "1", "./md_solver",
                "--mode", "ho", "--integrator", integ,
                "--dt", str(dt), "--steps", str(steps), "--N", "1"
            ]
            print(f"Running: {integ} dt={dt} steps={steps}")
            subprocess.run(cmd, check=True, capture_output=True)
            src = f"{OUT_DIR}/ho_{integ}.csv"
            dst = f"{HO_DIR}/{integ}_dt{dt}.csv"
            if os.path.exists(src):
                os.rename(src, dst)
    print("All HO simulations complete.")


import json
import csv

def load_manifest():
    with open("out/manifest.json", "r") as f:
        return json.load(f)

def load_csv(filepath):
    """Load CSV with headers, skipping comment lines."""
    def filter_comments(f):
        for line in f:
            if line.strip() and not line.startswith('#'):
                yield line
    with open(filepath, 'r') as f:
        # np.genfromtxt has trouble with Python generators, so read to list
        lines = list(filter_comments(f))
    return np.genfromtxt(lines, delimiter=',', names=True)


def plot_trajectories():
    """Plot x(t), v(t), phase space for all integrators at dt=0.01."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    t_exact = np.linspace(0, T_FINAL, 1000)
    x_exact, v_exact = exact_solution(t_exact)

    manifest = load_manifest()
    
    for integ in INTEGRATORS:
        dt_key = str(TRAJ_DT).replace('.', '_')
        fpath = manifest.get("ho_convergence", {}).get(f"{integ}_dt{dt_key}", "")
        if not os.path.exists(fpath):
            print(f"Warning: {fpath} not found, skipping {integ}")
            continue

        data = load_csv(fpath)
        t = data['time']
        x = data['x']
        v = data['v']

        color = INTEGRATOR_COLORS[integ]
        label = INTEGRATOR_LABELS[integ]

        axes[0].plot(t, x, color=color, label=label, linewidth=1.5, alpha=0.8)
        axes[1].plot(t, v, color=color, label=label, linewidth=1.5, alpha=0.8)
        axes[2].plot(x, v, color=color, label=label, linewidth=1.2, alpha=0.8)

    # Exact overlays
    axes[0].plot(t_exact, x_exact, 'k--', linewidth=1, alpha=0.5, label='Exact')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Position x')
    axes[0].set_title('Position vs Time')
    axes[0].legend(fontsize=9)
    axes[0].grid(True)

    axes[1].plot(t_exact, v_exact, 'k--', linewidth=1, alpha=0.5, label='Exact')
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Velocity v')
    axes[1].set_title('Velocity vs Time')
    axes[1].legend(fontsize=9)
    axes[1].grid(True)

    x_ep, v_ep = exact_solution(np.linspace(0, 2 * np.pi / OMEGA, 500))
    axes[2].plot(x_ep, v_ep, 'k--', linewidth=1, alpha=0.5, label='Exact')
    axes[2].set_xlabel('Position x')
    axes[2].set_ylabel('Velocity v')
    axes[2].set_title('Phase Space (v vs x)')
    axes[2].legend(fontsize=9)
    axes[2].set_aspect('equal')
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/ho_trajectories.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_trajectories.png")


def plot_convergence():
    """Log-log convergence plot with fitted slopes."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))

    x_ex_final, _ = exact_solution(T_FINAL)

    manifest = load_manifest()

    for integ in INTEGRATORS:
        errors = []
        dts = []

        for dt in DT_VALUES:
            dt_key = str(dt).replace('.', '_')
            try:
                fpath = manifest.get("ho_convergence", {}).get(f"{integ}_dt{dt_key}", "")
            except Exception:
                fpath = ""
            if not os.path.exists(fpath):
                continue

            data = load_csv(fpath)
            x_num_final = data['x'][-1]
            err = abs(x_num_final - x_ex_final)

            if err > 1e-16:  # skip if at machine epsilon
                errors.append(err)
                dts.append(dt)

        if len(dts) < 2:
            print(f"Warning: not enough data for {integ} convergence")
            continue

        dts = np.array(dts)
        errors = np.array(errors)

        log_dt = np.log10(dts)
        log_err = np.log10(errors)
        slope, intercept = np.polyfit(log_dt, log_err, 1)

        color = INTEGRATOR_COLORS[integ]
        expected = INTEGRATOR_ORDERS[integ]
        label = f"{INTEGRATOR_LABELS[integ]} (slope={slope:.2f}, expected {expected})"

        ax.loglog(dts, errors, 'o-', color=color, label=label,
                  linewidth=2, markersize=6)

        # Reference slope line
        dt_ref = np.array([min(dts), max(dts)])
        err_ref = errors[0] * (dt_ref / dts[0]) ** expected
        ax.loglog(dt_ref, err_ref, '--', color=color, alpha=0.4, linewidth=1)

    ax.set_xlabel(r'$\Delta t$')
    ax.set_ylabel(r'$|x_{num}(T) - x_{exact}(T)|$')
    ax.set_title('Convergence: Position Error vs Timestep')
    ax.legend(fontsize=10)
    ax.grid(True, which='both')

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/ho_convergence.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_convergence.png")


def plot_energy_conservation():
    """Energy conservation comparison for all integrators."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    manifest = load_manifest()
    
    for integ in INTEGRATORS:
        dt_key = str(TRAJ_DT).replace('.', '_')
        fpath = manifest.get("ho_convergence", {}).get(f"{integ}_dt{dt_key}", "")
        if not os.path.exists(fpath):
            continue

        data = load_csv(fpath)
        t = data['time']
        E = data['E_total']

        color = INTEGRATOR_COLORS[integ]
        label = INTEGRATOR_LABELS[integ]

        E0 = E[0]
        rel_dev = (E - E0) / abs(E0) if abs(E0) > 1e-30 else E - E0
        ax.plot(t, rel_dev, color=color, label=label, linewidth=1.5)

    ax.set_xlabel('Time')
    ax.set_ylabel(r'$(E - E_0) / |E_0|$')
    ax.set_title('HO Energy Conservation (dt=0.01)')
    ax.legend(fontsize=10)
    ax.grid(True)

    # Add zoomed inset to show VV vs RK4 near zero
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    axins = inset_axes(ax, width="40%", height="30%", loc="lower right", borderpad=2)
    
    for integ in INTEGRATORS:
        if integ == "euler": continue # Skip Euler for inset
        dt_key = str(TRAJ_DT).replace('.', '_')
        fpath = manifest.get("ho_convergence", {}).get(f"{integ}_dt{dt_key}", "")
        if not os.path.exists(fpath): continue
        data = load_csv(fpath)
        t = data['time']
        E = data['E_total']
        E0 = E[0]
        rel_dev = (E - E0) / abs(E0) if abs(E0) > 1e-30 else E - E0
        axins.plot(t, rel_dev, color=INTEGRATOR_COLORS[integ], linewidth=1.5)
    
    axins.set_title('Zoom: VV vs RK4')
    axins.grid(True)
    axins.tick_params(axis='both', which='major', labelsize=8)
    
    # Optional: adjust y-limits of inset manually if needed
    # (Leaving it auto-scaled, which usually captures the O(1e-4) VV vs O(1e-15) RK4 nicely.)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/ho_energy.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_energy.png")


if __name__ == "__main__":
    if "--run" in sys.argv:
        run_ho_simulations()

    plot_trajectories()
    plot_convergence()
    plot_energy_conservation()
```

### `scripts/plot_lj.py` (262 lines)

```py
#!/usr/bin/env python3
"""
plot_lj.py — Generate Lennard-Jones / Argon validation plots (Results 2).

Produces:
  1. Energy conservation: E_kin, E_pot, E_total vs time for Verlet and Euler
  2. Temperature vs time
  3. Raw NVE vs equilibrated NVE energy comparison
  4. g(r) vs r/sigma

Usage:
  python3 scripts/plot_lj.py
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUT_DIR = "out"
LJ_DIR = "out/lj"
PLOT_DIR = "out/plots"

SIGMA = 3.4e-10
EPSILON_OVER_KB = 120.0
KB = 1.380649e-23
EPSILON = KB * EPSILON_OVER_KB


import json
import csv

def load_manifest():
    with open("out/manifest.json", "r") as f:
        return json.load(f)

def load_csv(filepath):
    """Load CSV with headers, skipping comment lines."""
    def filter_comments(f):
        for line in f:
            if line.strip() and not line.startswith('#'):
                yield line
    with open(filepath, 'r') as f:
        lines = list(filter_comments(f))
    return np.genfromtxt(lines, delimiter=',', names=True)


def plot_energy_conservation():
    """Plot E_kin, E_pot, E_total vs time for Verlet and Euler."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    configs = [
        ("verlet_100", "Velocity-Verlet (NVE)", "#2ecc71"),
        ("euler_100", "Forward Euler", "#e74c3c"),
    ]

    manifest = load_manifest()
    
    for idx, (key, label, color) in enumerate(configs):
        fpath = manifest.get("lj_production", {}).get(key, "")
        if not os.path.exists(fpath):
            print(f"Warning: {fpath} not found, skipping")
            continue

        data = load_csv(fpath)
        t = data['time'] * 1e12  # ps
        ekin = data['E_kin'] / EPSILON
        epot = data['E_pot'] / EPSILON
        etot = data['E_total'] / EPSILON

        ax = axes[idx, 0]
        ax.plot(t, ekin, label=r'$E_{kin}$', color='tab:red', linewidth=1.5)
        ax.plot(t, epot, label=r'$E_{pot}$', color='tab:blue', linewidth=1.5)
        ax.plot(t, etot, label=r'$E_{total}$', color='k', linewidth=2)
        ax.set_xlabel('Time [ps]')
        ax.set_ylabel(r'Energy [$\varepsilon$]')
        ax.set_title(f'{label}: Energy vs Time')
        ax.legend()
        ax.grid(True)

        # Relative deviation
        ax2 = axes[idx, 1]
        e0 = etot[0]
        rel_dev = (etot - e0) / abs(e0) if abs(e0) > 1e-30 else etot - e0
        ax2.plot(t, rel_dev, color=color, linewidth=1.5)
        ax2.set_xlabel('Time [ps]')
        ax2.set_ylabel(r'$(E_{total} - E_0) / |E_0|$')
        ax2.set_title(f'{label}: Relative Energy Deviation')
        ax2.grid(True)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_energy.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_energy.png")


def plot_temperature():
    """Plot temperature vs time."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    configs = [
        ("verlet_100", "Velocity-Verlet", "#2ecc71"),
        ("euler_100", "Forward Euler", "#e74c3c"),
    ]

    manifest = load_manifest()

    for key, label, color in configs:
        fpath = manifest.get("lj_production", {}).get(key, "")
        if not os.path.exists(fpath):
            continue

        data = load_csv(fpath)
        t = data['time'] * 1e12
        T = data['temperature']
        ax.plot(t, T, label=label, color=color, linewidth=1.5)

    ax.axhline(y=94.4, color='k', linestyle='--', alpha=0.5, label='T = 94.4 K')
    ax.set_xlabel('Time [ps]')
    ax.set_ylabel('Temperature [K]')
    ax.set_title('Temperature vs Time (N=864, NVE)')
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_temperature.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_temperature.png")


def plot_equilibrated_comparison():
    """Compare raw NVE vs equilibrated NVE energy deviation."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # --- Left panel: full trajectories ---
    configs = [
        ("verlet_100", "Raw NVE (100 steps)", "#e74c3c", '-'),
        ("verlet_200_equilibrated", "Equilibrated (rescale→100, NVE→200)", "#2ecc71", '-'),
    ]

    manifest = load_manifest()

    for key, label, color, ls in configs:
        fpath = manifest.get("lj_production", {}).get(key, "")
        if not os.path.exists(fpath):
            print(f"  {fpath} not found, skipping")
            continue

        data = load_csv(fpath)
        step = data['step']
        etot = data['E_total'] / EPSILON
        e0 = etot[0]
        rel_dev = (etot - e0) / abs(e0)

        ax1.plot(step, rel_dev, color=color, label=label, linewidth=1.5, linestyle=ls)

    ax1.set_xlabel('Step')
    ax1.set_ylabel(r'$(E_{total} - E_0) / |E_0|$')
    ax1.set_title('Energy Deviation: Full Trajectories')
    ax1.axvline(x=100, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
    ax1.text(102, ax1.get_ylim()[1] * 0.5, 'NVE starts', rotation=90,
             color='gray', va='center')
    ax1.legend(fontsize=9)
    ax1.grid(True)

    # --- Right panel: NVE-only phase comparison ---
    # Raw NVE: all 100 steps
    fpath_raw = manifest.get("lj_production", {}).get("verlet_100", "")
    fpath_eq = manifest.get("lj_production", {}).get("verlet_200_equilibrated", "")

    if os.path.exists(fpath_raw):
        data = load_csv(fpath_raw)
        etot = data['E_total'] / EPSILON
        e0 = etot[0]
        nve_steps = np.arange(len(etot))
        ax2.plot(nve_steps, (etot - e0) / abs(e0), color='tab:red', linewidth=1.5,
                 label=f'Raw NVE (drift={abs(etot[-1]-e0)/abs(e0)*100:.2f}%)')

    if os.path.exists(fpath_eq):
        data = load_csv(fpath_eq)
        # NVE phase starts after step 100
        nve_mask = data['step'] > 100
        if np.any(nve_mask):
            etot_nve = data['E_total'][nve_mask] / EPSILON
            e0_nve = etot_nve[0]
            nve_steps = np.arange(len(etot_nve))
            ax2.plot(nve_steps, (etot_nve - e0_nve) / abs(e0_nve), color='tab:green', linewidth=1.5,
                     label=f'Post-equilibration NVE (drift={abs(etot_nve[-1]-e0_nve)/abs(e0_nve)*100:.2f}%)')

    ax2.set_xlabel('NVE Step')
    ax2.set_ylabel(r'$(E_{total} - E_0) / |E_0|$')
    ax2.set_title('NVE Energy Conservation Comparison')
    ax2.legend(fontsize=9)
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_equilibrated_comparison.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_equilibrated_comparison.png")


def plot_rdf():
    """Plot g(r) radial distribution function."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    manifest = load_manifest()
    fpath = manifest.get("lj_gr", "")
    if not os.path.exists(fpath):
        print("No g(r) data found. Skipping RDF plot.")
        return

    data = load_csv(fpath)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(data['r_sigma'], data['gr'], '-', color='k', linewidth=1.5)
    ax.axhline(y=1.0, color='k', linestyle='--', label='g(r) = 1')
    ax.set_xlabel(r'$r / \sigma$')
    ax.set_ylabel(r'$g(r)$')

    try:
        fpath_energy = manifest.get("lj_gr_energy", "")
        if os.path.exists(fpath_energy):
            energy_data = load_csv(fpath_energy)
            gr_mask = energy_data['step'] >= 500
            if np.any(gr_mask):
                T_mean = np.mean(energy_data['temperature'][gr_mask])
                ax.set_title(rf'Radial Distribution Function (Liquid Argon, $\langle T \rangle$ = {T_mean:.0f} K)')
            else:
                ax.set_title(r'Radial Distribution Function (Liquid Argon)')
        else:
            ax.set_title(r'Radial Distribution Function (Liquid Argon)')
    except Exception as e:
        print(f"Warning: could not compute T_mean for title: {e}")
        ax.set_title(r'Radial Distribution Function (Liquid Argon)')

    ax.set_xlim(0, 5)
    ax.legend()
    ax.grid(True)

    # Annotate first peak
    peak_idx = np.argmax(data['gr'])
    ax.annotate(f"Peak: g({data['r_sigma'][peak_idx]:.2f}σ) = {data['gr'][peak_idx]:.2f}",
                xy=(data['r_sigma'][peak_idx], data['gr'][peak_idx]),
                xytext=(2.5, 2.5),
                arrowprops=dict(arrowstyle='->', color='gray'))

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_rdf.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_rdf.png")


if __name__ == "__main__":
    plot_energy_conservation()
    plot_temperature()
    plot_equilibrated_comparison()
    plot_rdf()
```

### `scripts/plot_scaling.py` (229 lines)

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
import numpy as np
import matplotlib.pyplot as plt

PLOT_DIR = "out/plots"


def load_manifest():
    with open("out/manifest.json", "r") as f:
        return json.load(f)


def load_scaling_csv(key):
    manifest = load_manifest()
    path = manifest.get("scaling", {}).get(key, "")
    if not os.path.exists(path):
        return None
    data = np.genfromtxt(path, delimiter=',', names=True, encoding=None)
    names = getattr(getattr(data, "dtype", None), "names", None)
    if names and "P" in names and "wall_s" in names:
        return data

    # Fallback: tolerate headerless CSVs ("P,N,wall_s,comm_s" missing).
    raw = np.genfromtxt(path, delimiter=',', encoding=None)
    if raw is None:
        return None
    if raw.ndim == 1:
        raw = np.array([raw])
    if raw.shape[1] < 4:
        return None
    out = np.zeros(raw.shape[0], dtype=[("P", float), ("N", float), ("wall_s", float), ("comm_s", float)])
    out["P"] = raw[:, 0]
    out["N"] = raw[:, 1]
    out["wall_s"] = raw[:, 2]
    out["comm_s"] = raw[:, 3]
    print(f"Warning: {path} missing header; parsed as 4-column numeric fallback.")
    return out


def amdahl(P, f):
    """Amdahl's Law: S(P) = 1 / (f + (1-f)/P)."""
    return 1.0 / (f + (1.0 - f) / P)


def plot_strong_scaling():
    """Plot speedup, efficiency, and compute/comm breakdown."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    data = load_scaling_csv("strong")
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
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # --- Panel 1: Speedup ---
    ax1 = axes[0]
    ax1.plot(P, speedup, 'o-', color='tab:green', linewidth=2, markersize=8, label='Measured')
    ax1.plot(P, P.astype(float), 'k--', alpha=0.5, linewidth=1.5, label='Ideal (S=P)')
    if f_fit is not None:
        ax1.plot(P_fit, S_fit, '-', color='tab:red', linewidth=1.5,
                 label=f'Amdahl fit (f={f_fit:.4f})')
    ax1.set_xlabel('Number of Processes P')
    ax1.set_ylabel('Speedup S(P)')
    ax1.set_title('Strong Scaling: Speedup')
    ax1.legend(fontsize=10)
    ax1.grid(True)

    # --- Panel 2: Efficiency ---
    ax2 = axes[1]
    ax2.plot(P, efficiency, 'o-', color='tab:blue', linewidth=2, markersize=8)
    ax2.axhline(y=1.0, color='k', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Number of Processes P')
    ax2.set_ylabel('Efficiency E(P) = S(P)/P')
    ax2.set_title('Strong Scaling: Efficiency')
    ax2.set_ylim(0, 1.15)
    ax2.grid(True)

    # --- Panel 3: Stacked bar — Compute vs Communication ---
    ax3 = axes[2]
    x_pos = np.arange(len(P))
    bar_width = 0.6
    compute_display = np.maximum(compute, 0)
    ax3.bar(x_pos, compute_display, bar_width, label='Compute', color='tab:green', alpha=0.8)
    ax3.bar(x_pos, comm, bar_width, bottom=compute_display, label='Communication',
            color='tab:red', alpha=0.8)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([str(p) for p in P])
    ax3.set_xlabel('Number of Processes P')
    ax3.set_ylabel('Wall Time [s]')
    ax3.set_title('Compute vs Communication Time')
    ax3.legend(fontsize=10)
    ax3.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/scaling_strong.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/scaling_strong.png")

    if f_fit is not None:
        print(f"  Amdahl serial fraction f = {f_fit:.6f}")
        print(f"  Maximum theoretical speedup = {1.0/f_fit:.1f}x")


def plot_size_scaling():
    """Plot wall time and compute time vs N."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    data = load_scaling_csv("size")
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

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    wall_label = 'Wall time'
    if slope_wall is not None:
        wall_label += f' (O(N^{slope_wall:.2f}))'
    ax1.loglog(N, wall, 'o-', color='tab:green', linewidth=2, markersize=8, label=wall_label)
    
    comp_label = 'Compute time'
    if slope_comp is not None:
        comp_label += f' (O(N^{slope_comp:.2f}))'
    ax1.loglog(N, compute, '^-', color='tab:orange', linewidth=2, markersize=8, label=comp_label)

    ax1.loglog(N, comm, 's--', color='tab:red', linewidth=1.5, markersize=6,
               label='Comm time', alpha=0.7)
    N_ref = np.array([min(N), max(N)])
    t_ref = wall[-1] * (N_ref / N[-1]) ** 2
    ax1.loglog(N_ref, t_ref, 'k--', alpha=0.4, linewidth=1.5, label=r'$\sim N^2$ reference')
    ax1.set_xlabel('Number of Particles N')
    ax1.set_ylabel('Time [s]')
    ax1.set_title('Size Scaling (P=16)')
    ax1.legend(fontsize=10)
    ax1.grid(True, which='both')

    comm_frac = comm / wall * 100
    ax2.plot(N, comm_frac, 'o-', color='tab:red', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Particles N')
    ax2.set_ylabel('Communication Fraction [%]')
    ax2.set_title('Communication Overhead vs Problem Size')
    ax2.set_ylim(0, 100)
    ax2.grid(True)
    ax2.axhline(y=50, color='k', linestyle='--')

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/scaling_size.png")
    plt.close()
    print(f"Saved {PLOT_DIR}/scaling_size.png")


if __name__ == "__main__":
    plot_strong_scaling()
    plot_size_scaling()
```

### `scripts/validate_manifest.py` (99 lines)

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

    require_file(manifest, "lj_production.verlet_100", errors)
    require_file(manifest, "lj_production.euler_100", errors)
    require_file(manifest, "lj_production.verlet_200_equilibrated", errors)
    require_file(manifest, "lj_gr", errors)
    require_file(manifest, "lj_gr_energy", errors)

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
include/md/mic.hpp                                   18 lines
include/md/mpi_context.hpp                          103 lines
include/md/observables.hpp                           90 lines
include/md/params.hpp                               182 lines
include/md/potentials.hpp                            64 lines
include/md/rng.hpp                                  139 lines
include/md/system.hpp                                70 lines
src/main.cpp                                        385 lines
src/observables.cpp                                  70 lines
src/potentials/harmonic.cpp                          35 lines
src/potentials/lennard_jones.cpp                    100 lines
tests/test_force.cpp                                198 lines
tests/test_mic.cpp                                  116 lines
tests/test_runner.cpp                                33 lines

Total C++ lines:
    1804
```

**End of audit.**
