# Full Code Audit — WA2 MPI MD Solver

**Generated:** 2026-03-03 12:21:13
**Working directory:** /Users/felix/A2_MPhil/md-mpi

---

## 1. Directory Structure
```
./.clang-format
./.gitignore
./ai/audit_output.md
./ai/audit.sh
./ai/claude.md
./ai/code.md
./ai/constraints.md
./ai/current_code.md
./ai/pack_results.sh
./ai/results_bundle.md
./ai/task_overview.md
./include/md/constants.hpp
./include/md/integrators.hpp
./include/md/mpi_context.hpp
./include/md/observables.hpp
./include/md/params.hpp
./include/md/potentials.hpp
./include/md/rng.hpp
./include/md/system.hpp
./Makefile
./md_solver
./out/gr_smooth.csv
./out/gr.csv
./out/ho_euler.csv
./out/ho_rk4.csv
./out/ho_verlet.csv
./out/ho/euler_dt0.0005.csv
./out/ho/euler_dt0.001.csv
./out/ho/euler_dt0.005.csv
./out/ho/euler_dt0.01.csv
./out/ho/euler_dt0.05.csv
./out/ho/euler_dt0.1.csv
./out/ho/euler_dt0.5.csv
./out/ho/euler_dt1.0.csv
./out/ho/rk4_dt0.0005.csv
./out/ho/rk4_dt0.001.csv
./out/ho/rk4_dt0.005.csv
./out/ho/rk4_dt0.01.csv
./out/ho/rk4_dt0.05.csv
./out/ho/rk4_dt0.1.csv
./out/ho/rk4_dt0.5.csv
./out/ho/rk4_dt1.0.csv
./out/ho/verlet_dt0.0005.csv
./out/ho/verlet_dt0.001.csv
./out/ho/verlet_dt0.005.csv
./out/ho/verlet_dt0.01.csv
./out/ho/verlet_dt0.05.csv
./out/ho/verlet_dt0.1.csv
./out/ho/verlet_dt0.5.csv
./out/ho/verlet_dt1.0.csv
./out/lj_euler.csv
./out/lj_verlet.csv
./out/lj/euler_864_100.csv
./out/lj/verlet_864_100_rescaled.csv
./out/lj/verlet_864_100.csv
./out/lj/verlet_864_200_equilibrated.csv
./out/plots/ho_convergence.png
./out/plots/ho_energy.png
./out/plots/ho_trajectories.png
./out/plots/lj_energy.png
./out/plots/lj_equilibrated_comparison.png
./out/plots/lj_rdf.png
./out/plots/lj_temperature.png
./out/plots/scaling_size.png
./out/plots/scaling_strong.png
./out/scaling_size.csv
./out/scaling_strong.csv
./README.md
./scripts/plot_ho.py
./scripts/plot_lj.py
./scripts/plot_scaling.py
./scripts/run_all_data.sh
./scripts/run_scaling.sh
./src/integrators/euler.cpp
./src/integrators/euler.o
./src/integrators/rk4.cpp
./src/integrators/rk4.o
./src/integrators/velocity_verlet.cpp
./src/integrators/velocity_verlet.o
./src/main.cpp
./src/main.o
./src/potentials/harmonic.cpp
./src/potentials/harmonic.o
./src/potentials/lennard_jones.cpp
./src/potentials/lennard_jones.o
./test_runner
./tests/test_force.cpp
./tests/test_force.o
./tests/test_mic.cpp
./tests/test_mic.o
./tests/test_runner.cpp
./tests/test_runner.o
```

## Current Code Summary

# Current Code State — WA2: MPI MD Solver

**Generated:** 2026-03-02 22:35  
**Build:** ✅ Zero warnings (`-Wall -Wextra -pedantic`, `-g -O3 -march=native`)  
**Tests:** ✅ All pass (MIC, LJ force, position wrapping)  
**Total C++ lines:** ~1040

---

## Project Structure

```
md-mpi/
├── .clang-format              # BasedOnStyle: Google, ColumnLimit: 100
├── .gitignore                 # Excludes out/, ai/, *.o, binaries
├── Makefile                   # mpicxx, C++17, -O3 -march=native -g
├── README.md                  # Assessor-first: exact build/run/plot commands
│
├── include/md/
│   ├── constants.hpp          # All physical constants + derived quantities
│   ├── params.hpp             # CLI parser with 16 flags + mode/integrator validation
│   ├── mpi_context.hpp        # Rank/size, decomposition, Allgatherv, posGlobal buffer, comm timing
│   ├── system.hpp             # Flat interleaved pos/vel/acc arrays (no unused force array)
│   ├── rng.hpp                # FCC lattice (with N=4k³ validation) + Box-Muller velocities
│   ├── potentials.hpp         # ForceFunc typedef + HO/LJ declarations
│   ├── integrators.hpp        # Euler/RK4/VV declarations
│   └── observables.hpp        # KE, temperature, g(r) histogram (rescaling done in main.cpp)
│
├── src/
│   ├── main.cpp               # MPI driver: init→bcast→loop→g(r)→output
│   ├── integrators/
│   │   ├── euler.cpp           # AMM Eqn 4.27 (2nd-order position update)
│   │   ├── rk4.cpp             # Classical RK4 (HO verification only)
│   │   └── velocity_verlet.cpp # Half-kick / drift / half-kick
│   └── potentials/
│       ├── harmonic.cpp        # F = -mω²x, non-interacting
│       └── lennard_jones.cpp   # Optimised kernel (no pow, no sqrt)
│
├── tests/
│   ├── test_runner.cpp        # Aggregates all tests, exits non-zero on failure
│   ├── test_mic.cpp           # 9 MIC boundary tests + geometric safety check
│   └── test_force.cpp         # LJ force at r_min, PE check, sign test, wrap test
│
├── scripts/
│   ├── run_scaling.sh         # Batch scaling on cerberus1
│   ├── run_all_data.sh        # Full production data generation (HO + LJ + g(r) + scaling)
│   ├── plot_ho.py             # Phase-space, trajectory, convergence (position error)
│   ├── plot_lj.py             # Energy conservation + g(r)
│   └── plot_scaling.py        # Speedup, efficiency, Amdahl fit
│
└── ai/                        # Context files (excluded from tarball)
    ├── current_code.md        # This file
    ├── claude.md              # Execution checklist
    ├── task_overview.md       # Distilled spec, run matrix
    ├── constraints.md         # Hard constraints, numerical best practices
    ├── code.md                # Code quality standards
    ├── audit.sh               # Generates audit_output.md
    └── audit_output.md        # Latest full audit snapshot
```

## Data Layout

Flat interleaved `std::vector<double>` of size `3*localN`:
```
pos[3*i + 0] = x_i,  pos[3*i + 1] = y_i,  pos[3*i + 2] = z_i
```
`posGlobal` (size `3*N`) permanently allocated on all ranks.

## MPI Communication

| Operation | Function | When |
|-----------|----------|------|
| **Init broadcast** | `MPI_Bcast` (pos + vel) | Once at startup (NOT Scatterv) |
| **Position sync** | `MPI_Allgatherv` | Every step (LJ only, after wrap) |
| **Energy reduce** | `MPI_Reduce(SUM)` | Every step (not in timing mode) |
| **Rescale broadcast** | `MPI_Bcast(lambda)` | At rescale steps (λ computed on root) |
| **FCC error broadcast** | `MPI_Bcast(fccError)` | Once (all ranks participate, clean exit) |
| **g(r) reduce** | `MPI_Reduce(SUM)` | Once after time loop |
| **Timing** | `MPI_Reduce(MAX)` | Wall time + comm time after loop |

## Integrator MPI Sequences

**Euler (AMM 4.27):**
```
drift (x += v*dt + 0.5*a*dt²) → vel update → [wrap] → [Allgatherv] → force
```

**Velocity-Verlet:**
```
half-kick → drift → [wrap] → [Allgatherv] → force → half-kick
```

**RK4 (HO only):**
```
4 stages × (set intermediate state → [wrap] → [Allgatherv] → force)
final combine → [wrap] → [Allgatherv] → force
```

All `[wrap]` and `[Allgatherv]` are guarded with `if (!isHO)`.

## LJ Force Kernel

```
inv_r2 → inv_r6 → inv_r12
V = 4ε(σ¹²·inv_r12 - σ⁶·inv_r6)
f = 24ε·inv_r2·(2σ¹²·inv_r12 - σ⁶·inv_r6)
```
- No `pow`, no `sqrt` in hot loop
- PE accumulated unconditionally for all j≠i, × 0.5 after loop
- MIC: branch-predictor-friendly `if/else if` (not `std::round`)
- Hard cutoff at r_c = 2.25σ (geometric safety: r_c < L/2 ≈ 5.115σ)

## g(r) Pipeline

1. Accumulate pair distances into histogram (bin width = 0.02σ, range [0, L/2])
2. Uses unordered pairs (i < j) from local particles vs all global particles
3. Samples every `--gr-interval` steps after `--gr-discard` equilibration steps
4. `MPI_Reduce(SUM)` across ranks after time loop
5. Normalise: **g(r) = 2 × count / (ρ·N·4πr²·dr·nFrames)** (factor of 2 converts unordered→ordered pairs)
6. Write to `out/gr.csv` (columns: `r_sigma, gr`)

## Output Formats

| Mode | CSV columns | File |
|------|-------------|------|
| HO | `step,time,x,v,E_kin,E_pot,E_total` | `out/ho_{integrator}.csv` |
| LJ | `step,time,E_kin,E_pot,E_total,temperature` | `out/lj_{integrator}.csv` |
| g(r) | `r_sigma,gr` | `out/gr.csv` |

## CLI Parameters

```
--N <int>            Particles (default: 864, must be 4k³ for LJ)
--steps <int>        Timesteps (default: 100)
--dt <double>        Timestep (default: 1e-14 s)
--T <double>         Initial temperature [K] (default: 94.4)
--omega <double>     HO angular frequency (default: 1.0)
--integrator <str>   euler, rk4, verlet (default: verlet) — validated
--mode <str>         ho, lj (default: lj) — validated
--seed <int>         RNG seed (default: 42)
--rescale-step <int> Step for single velocity rescale (default: -1 = disabled)
--rescale-freq <int> Rescale every N steps during equilibration (default: 0 = off)
--rescale-end <int>  Stop continuous rescaling after this step (default: 0)
--timing             Timing mode (reports wall + comm + compute breakdown)
--no-output          Disable CSV output
--gr                 Enable g(r) accumulation (LJ only)
--gr-discard <int>   Equilibration steps before g(r) (default: 500)
--gr-interval <int>  Sample g(r) every N steps (default: 10)
```

Invalid --mode or --integrator values are rejected with a clear error + usage.

## Key Design Decisions

1. **MPI only** — No OpenMP, no threading
2. **Fixed particle partition** — Static at startup, no spatial decomposition
3. **O(N²/P) force** — Each rank computes local-vs-global forces
4. **Cannot exploit Newton's 3rd law** across MPI boundaries (acknowledged limitation)
5. **N_dof = 3(N-1)** after CoM removal for temperature calculation
6. **Position wrapping** skipped for HO (all integrators guarded with `if (!isHO)`)
7. **Velocity rescale uses MPI_Bcast(λ)** — compute on root, broadcast, scale locally
8. **FCC lattice validated** — `4*k*k*k != N` with MPI_Bcast(fccError) + clean MPI_Finalize (no MPI_Abort)
9. **Reproducibility** — single `std::mt19937_64` stream on rank 0, passed to both buildFCCLattice and generateVelocities
10. **CSV precision** — `std::setprecision(15)` for convergence analysis
11. **Comm timing** — `MPI_Wtime()` around `MPI_Allgatherv` when `--timing` is active

---

## 2. Build Output

```
rm -f src/main.o src/integrators/euler.o src/integrators/rk4.o src/integrators/velocity_verlet.o src/potentials/harmonic.o src/potentials/lennard_jones.o tests/test_runner.o tests/test_mic.o tests/test_force.o src/potentials/lennard_jones.o src/potentials/harmonic.o md_solver test_runner
rm -f src/integrators/*.o src/potentials/*.o tests/*.o
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/main.o src/main.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/integrators/euler.o src/integrators/euler.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/integrators/rk4.o src/integrators/rk4.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/integrators/velocity_verlet.o src/integrators/velocity_verlet.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/potentials/harmonic.o src/potentials/harmonic.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o src/potentials/lennard_jones.o src/potentials/lennard_jones.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -o md_solver src/main.o src/integrators/euler.o src/integrators/rk4.o src/integrators/velocity_verlet.o src/potentials/harmonic.o src/potentials/lennard_jones.o
```

---

## 3. Unit Test Output

```
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o tests/test_runner.o tests/test_runner.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o tests/test_mic.o tests/test_mic.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -c -o tests/test_force.o tests/test_force.cpp
mpicxx -std=c++17 -O3 -march=native -g -Wall -Wextra -pedantic -Iinclude -o test_runner tests/test_runner.o tests/test_mic.o tests/test_force.o src/potentials/lennard_jones.o src/potentials/harmonic.o
./test_runner
=== MD Unit Tests ===
  MIC tests: ALL PASSED
  Force/Wrapping tests: ALL PASSED
=====================
ALL TESTS PASSED
```

---

## 4. Smoke Tests

### 4a. HO — Velocity-Verlet (N=1, 100 steps, dt=0.01)

```
=== MD Solver ===
Mode: ho | Integrator: verlet
N = 1 | P = 1 | steps = 100 | dt = 1.000e-02
L = 1.000000e+10 m (29411764705882353664.0000 sigma)
==================
Wall time: 0.002687 s (max across 1 ranks)
```

**HO output (first 6 + last 3 lines):**
```
step,time,x,v,E_kin,E_pot,E_total
0,0,1,0,0,3.34521325e-26,3.34521325e-26
1,0.01,0.99995,-0.00999975,3.34504599142826e-30,3.34487873703803e-26,3.34521324163718e-26
2,0.02,0.999800005,-0.019998500025,1.33788459807669e-29,3.34387533195397e-26,3.34521321655205e-26
3,0.03,0.9995500299995,-0.0299952501999975,3.00973865483582e-29,3.34220343609982e-26,3.34521317475465e-26
4,0.04,0.999200099996,-0.039989000849975,5.34939804451606e-29,3.33986371821719e-26,3.34521311626171e-26
...
98,0.98,0.557019155525826,-0.830489263708922,2.30723511649216e-26,1.03792045118787e-26,3.34515556768003e-26
99,0.99,0.54868641193096,-0.836017791546206,2.33805567224582e-26,1.00709912490106e-26,3.34515479714687e-26
100,1,0.540298799694902,-0.841462717604335,2.36861003830942e-26,9.76543994959206e-27,3.34515403326863e-26
```

**Exact solution check:** cos(1) = 0.540302, -sin(1) = -0.841471

### 4b. HO — RK4 (N=1, 100 steps, dt=0.01)

```
=== MD Solver ===
Mode: ho | Integrator: rk4
N = 1 | P = 1 | steps = 100 | dt = 1.000e-02
L = 1.000000e+10 m (29411764705882353664.0000 sigma)
==================
Wall time: 0.000873 s (max across 1 ranks)
```

**HO RK4 output (first 6 + last 3):**
```
step,time,x,v,E_kin,E_pot,E_total
0,0,1,0,0,3.34521325e-26,3.34521325e-26
1,0.01,0.999950000416667,-0.00999983333333333,3.34510174382089e-30,3.34487873982557e-26,3.34521324999995e-26
2,0.02,0.999800006666597,-0.0199986666916665,1.33790689791868e-29,3.34387534310199e-26,3.34521324999991e-26
3,0.03,0.999550033749042,-0.0299955001999963,3.00978882529885e-29,3.34220346117456e-26,3.34521324999986e-26
4,0.04,0.999200106661083,-0.0399893341833025,5.34948722604319e-29,3.33986376277377e-26,3.34521324999981e-26
...
98,0.98,0.557022546833661,-0.830497370445917,2.30728016039672e-26,1.03793308959873e-26,3.34521324999545e-26
99,0.99,0.548689860650181,-0.836025978554681,2.33810146499215e-26,1.00711178500325e-26,3.34521324999541e-26
100,1,0.540302305937885,-0.841470984762289,2.36865658052478e-26,9.76556669470578e-27,3.34521324999536e-26
```

### 4c. HO — Euler (N=1, 100 steps, dt=0.01)

```
=== MD Solver ===
Mode: ho | Integrator: euler
N = 1 | P = 1 | steps = 100 | dt = 1.000e-02
L = 1.000000e+10 m (29411764705882353664.0000 sigma)
==================
Wall time: 0.000992 s (max across 1 ranks)
```

**HO Euler output (first 6 + last 3):**
```
step,time,x,v,E_kin,E_pot,E_total
0,0,1,0,0,3.34521325e-26,3.34521325e-26
1,0.01,0.99995,-0.01,3.34521325e-30,3.34487873703803e-26,3.34521325836303e-26
2,0.02,0.9998000025,-0.0199995,1.3380183965713e-29,3.34387531523125e-26,3.34521333362782e-26
3,0.03,0.999550017499875,-0.029997500025,3.01019016893748e-29,3.34220335250963e-26,3.34521354267856e-26
4,0.04,0.99920006499875,-0.0399930001999987,5.35046809800916e-29,3.33986348425796e-26,3.34521395235597e-26
...
98,0.98,0.556316912119778,-0.832530864188268,2.31859286042238e-26,1.03530505337063e-26,3.35389791379301e-26
99,0.99,0.547963787632289,-0.838094033309466,2.34968316814062e-26,1.00444815686556e-26,3.35413132500617e-26
100,1,0.539555449109813,-0.843573671185789,2.38050907423816e-26,9.73858757869014e-27,3.35436783210717e-26
```

### 4d. LJ — Velocity-Verlet (N=108, 10 steps, P=1)

```
=== MD Solver ===
Mode: lj | Integrator: verlet
N = 108 | P = 1 | steps = 10 | dt = 1.000e-14
L = 1.738930e-09 m (5.1145 sigma)
T_init = 94.4 K | seed = 42
==================
Wall time: 0.000729 s (max across 1 ranks)
```

**LJ output:**
```
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

### 4e. LJ — Parallel Consistency (P=2, N=108, 5 steps)

```
=== MD Solver ===
Mode: lj | Integrator: verlet
N = 108 | P = 2 | steps = 5 | dt = 1.000e-14
L = 1.738930e-09 m (5.1145 sigma)
T_init = 94.4 K | seed = 42
==================
Wall time: 0.001953 s (max across 2 ranks)
```

**LJ P=2 output (should match P=1 for steps 0-5):**
```
step,time,E_kin,E_pot,E_total,temperature
0,0,2.09184891288e-19,-1.12926090964738e-18,-9.20076018359379e-19,94.4
1,1e-14,2.08952940324273e-19,-1.12903036097961e-18,-9.20077420655337e-19,94.2953262310627
2,2e-14,2.08327769566247e-19,-1.12840771146898e-18,-9.20079941902733e-19,94.0132020336875
3,3e-14,2.07279814481113e-19,-1.12736342912362e-18,-9.20083614642506e-19,93.5402856608675
4,4e-14,2.05766417434535e-19,-1.12585487169448e-18,-9.20088454259947e-19,92.8573267706854
5,5e-14,2.03732045550683e-19,-1.12382647756107e-18,-9.20094432010392e-19,91.9392647411899
```

### 4f. LJ — Euler (N=108, 10 steps)

```
=== MD Solver ===
Mode: lj | Integrator: euler
N = 108 | P = 1 | steps = 10 | dt = 1.000e-14
L = 1.738930e-09 m (5.1145 sigma)
T_init = 94.4 K | seed = 42
==================
Wall time: 0.000791 s (max across 1 ranks)
```

**LJ Euler output:**
```
step,time,E_kin,E_pot,E_total,temperature
0,0,2.09184891288e-19,-1.12926090964738e-18,-9.20076018359379e-19,94.4
1,1e-14,2.09144192886232e-19,-1.12903036097961e-18,-9.19886168093377e-19,94.3816338115854
2,2e-14,2.08721930537138e-19,-1.12840724624128e-18,-9.19685315704147e-19,94.1910771919891
3,3e-14,2.07894878960696e-19,-1.1273612115808e-18,-9.19466332620101e-19,93.8178491431783
4,4e-14,2.06626659369165e-19,-1.12584839357268e-18,-9.19221734203516e-19,93.245532812379
5,5e-14,2.0486759590329e-19,-1.12381130865358e-18,-9.18943712750289e-19,92.4517107052653
6,6e-14,2.02555070269067e-19,-1.12117937773952e-18,-9.18624307470456e-19,91.4081247248129
7,7e-14,1.99614874443516e-19,-1.11787068379777e-18,-9.18255809354249e-19,90.0812866141682
8,8e-14,1.95964360907104e-19,-1.11374692399182e-18,-9.17782563084718e-19,88.4338995791127
9,9e-14,1.91521204616192e-19,-1.10881928262626e-18,-9.17298078010064e-19,86.428812350874
10,1e-13,1.86205903489114e-19,-1.10296026074531e-18,-9.16754357256201e-19,84.0301475940328
```

### 4g. g(r) — Radial Distribution Function (N=108, 50 steps)

```
=== MD Solver ===
Mode: lj | Integrator: verlet
N = 108 | P = 1 | steps = 50 | dt = 1.000e-14
L = 1.738930e-09 m (5.1145 sigma)
T_init = 94.4 K | seed = 42
==================
Wall time: 0.003116 s (max across 1 ranks)
g(r) written to out/gr.csv (127 bins, 9 frames)
```

**g(r) output (first peak region):**
```
r_sigma,gr
0.01,0
0.03,0
...
1.03,1.1089
1.05,1.73857
1.07,1.98422
1.09,2.22791
1.11,2.42821
1.13,3.06577
1.15,2.88338
1.17,2.94863
1.19,3.29438
1.21,2.91622
1.23,2.76853
1.25,2.62223
1.27,1.9681
1.29,1.53579
1.31,1.30605
...
2.49,0.727899
2.51,0.722784
2.53,0.822311
```

### 4h. MPI Velocity Rescale (P=2, rescale at step 5)

```
=== MD Solver ===
Mode: lj | Integrator: verlet
N = 108 | P = 2 | steps = 10 | dt = 1.000e-14
L = 1.738930e-09 m (5.1145 sigma)
T_init = 94.4 K | seed = 42
==================
Rescale at step 5: lambda = 1.013294030170873e+00, T_before = 91.939265 K, T_after = 94.400000 K
Wall time: 0.007058 s (max across 2 ranks)
```

**LJ with rescale output:**
```
step,time,E_kin,E_pot,E_total,temperature
0,0,2.09184891288e-19,-1.12926090964738e-18,-9.20076018359379e-19,94.4
1,1e-14,2.08952940324273e-19,-1.12903036097961e-18,-9.20077420655337e-19,94.2953262310627
2,2e-14,2.08327769566247e-19,-1.12840771146898e-18,-9.20079941902733e-19,94.0132020336875
3,3e-14,2.07279814481113e-19,-1.12736342912362e-18,-9.20083614642506e-19,93.5402856608675
4,4e-14,2.05766417434535e-19,-1.12585487169448e-18,-9.20088454259947e-19,92.8573267706854
5,5e-14,2.03732045550683e-19,-1.12382647756107e-18,-9.20094432010392e-19,91.9392647411899
6,6e-14,2.06522371395575e-19,-1.12117129414391e-18,-9.14648922748338e-19,93.1984702131339
7,7e-14,2.03174367218241e-19,-1.11783144715343e-18,-9.14657079935188e-19,91.6875982166225
8,8e-14,1.99056208850067e-19,-1.11367147825058e-18,-9.1461526940051e-19,89.8291745629731
9,9e-14,1.94085430780824e-19,-1.10870848367489e-18,-9.14623052894068e-19,87.5859845942937
10,1e-13,1.8819842319568e-19,-1.10282624182649e-18,-9.14627818630815e-19,84.9293227645802
```

### 4i. FCC Validation — Invalid N

```
ERROR: N = 100 is not a valid FCC particle count (need N = 4*k^3, nearest k = 3 gives N = 108)
(no error output captured)
```

**Expected:** Error message with nearest valid N

### 4j. FCC Validation — Valid Ns

```
=== MD Solver ===
=== MD Solver ===
=== MD Solver ===
=== MD Solver ===
=== MD Solver ===
=== MD Solver ===
=== MD Solver ===
```

### 4k. Timing Mode (no output, no observables)

```
=== MD Solver ===
Mode: lj | Integrator: verlet
N = 108 | P = 1 | steps = 100 | dt = 1.000e-14
L = 1.738930e-09 m (5.1145 sigma)
T_init = 94.4 K | seed = 42
==================
Wall time: 0.005403 s (max across 1 ranks)
  Comm time: 0.000007 s (0.1%)
  Compute time: 0.005396 s (99.9%)
```

### 4l. CLI Help

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
  --rescale-freq <int> Rescale every N steps during equilibration (default: 0 = off)
  --rescale-end <int>  Stop continuous rescaling after this step (default: 0)
  --timing             Enable timing mode (implies --no-output)
  --gr                 Enable g(r) accumulation (LJ only)
  --gr-discard <int>   Equilibration steps to discard (default: 500)
  --gr-interval <int>  Sample g(r) every N steps (default: 10)
  --help               Print this message and exit
```

---

## 5. C++ Source Files

### `include/md/constants.hpp` (89 lines)

```cpp
/**
 * @file constants.hpp
 * @brief Physical constants for Molecular Dynamics simulation.
 *
 * All constants are defined as constexpr values in SI units unless
 * otherwise noted. No magic numbers should appear anywhere else in
 * the codebase — reference this header instead.
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

/// Pi
constexpr double pi = 3.14159265358979323846;

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

// ── Rahman (1964) reference state point ──

/// Number of particles in Rahman's simulation
constexpr int N_rahman = 864;

/// FCC lattice repeats for N=864 (4 * 6^3 = 864)
constexpr int k_rahman = 6;

/// Box side length for N=864 in units of sigma
constexpr double L_sigma_rahman = 10.229;

/// Box side length for N=864 [m]
constexpr double L_rahman = L_sigma_rahman * sigma;

/// Initial temperature [K]
constexpr double T_init = 94.4;

/// Timestep [s]
constexpr double dt_rahman = 1.0e-14;

/// Total simulation time [s]
constexpr double T_sim = 1.0e-12;

/// Number of timesteps (T_sim / dt)
constexpr int steps_rahman = 100;

}  // namespace constants
}  // namespace md

#endif  // MD_CONSTANTS_HPP
```

### `include/md/params.hpp` (201 lines)

```cpp
/**
 * @file params.hpp
 * @brief Runtime parameter struct and CLI argument parser.
 *
 * All simulation parameters are configurable via command-line arguments.
 * No recompilation is needed to change N, dt, integrator, etc.
 *
 * The parser never calls std::exit() — it returns a ParseStatus so the
 * caller can handle MPI_Finalize() cleanly before exiting.
 */

#ifndef MD_PARAMS_HPP
#define MD_PARAMS_HPP

#include <cstdlib>
#include <iostream>
#include <string>

namespace md {

/// Parse result status (avoids std::exit before MPI_Finalize).
enum class ParseStatus { Ok, Help, Error };

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
    int rescale_step = -1;              ///< Step at which to apply optional rescale (-1 = disabled)
    int rescale_freq = 0;               ///< Rescale every N steps during equilibration (0 = off)
    int rescale_end = 0;                ///< Stop rescaling after this step (0 = off)
    bool timing = false;                ///< Enable wall-clock timing (disables output)
    bool gr = false;                    ///< Enable g(r) accumulation
    int gr_discard = 500;               ///< Number of equilibration steps to discard before g(r)
    int gr_interval = 10;               ///< Sample g(r) every N steps after discard

    /**
     * @brief Parse command-line arguments into a Params struct.
     *
     * Does NOT call std::exit(). Returns a ParseStatus so the caller
     * can call MPI_Finalize() before exiting.
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
                return ParseStatus::Help;
            } else if (arg == "--N") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --N\n";
                    return ParseStatus::Error;
                }
                p.N = std::atoi(argv[++i]);
            } else if (arg == "--steps") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --steps\n";
                    return ParseStatus::Error;
                }
                p.steps = std::atoi(argv[++i]);
            } else if (arg == "--dt") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --dt\n";
                    return ParseStatus::Error;
                }
                p.dt = std::atof(argv[++i]);
            } else if (arg == "--T") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --T\n";
                    return ParseStatus::Error;
                }
                p.T_init = std::atof(argv[++i]);
            } else if (arg == "--omega") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --omega\n";
                    return ParseStatus::Error;
                }
                p.omega = std::atof(argv[++i]);
            } else if (arg == "--integrator") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --integrator\n";
                    return ParseStatus::Error;
                }
                p.integrator = argv[++i];
            } else if (arg == "--mode") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --mode\n";
                    return ParseStatus::Error;
                }
                p.mode = argv[++i];
            } else if (arg == "--no-output") {
                p.output = false;
            } else if (arg == "--seed") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --seed\n";
                    return ParseStatus::Error;
                }
                p.seed = std::atoi(argv[++i]);
            } else if (arg == "--rescale-step") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --rescale-step\n";
                    return ParseStatus::Error;
                }
                p.rescale_step = std::atoi(argv[++i]);
            } else if (arg == "--rescale-freq") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --rescale-freq\n";
                    return ParseStatus::Error;
                }
                p.rescale_freq = std::atoi(argv[++i]);
            } else if (arg == "--rescale-end") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --rescale-end\n";
                    return ParseStatus::Error;
                }
                p.rescale_end = std::atoi(argv[++i]);
            } else if (arg == "--timing") {
                p.timing = true;
                p.output = false;
            } else if (arg == "--gr") {
                p.gr = true;
            } else if (arg == "--gr-discard") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --gr-discard\n";
                    return ParseStatus::Error;
                }
                p.gr_discard = std::atoi(argv[++i]);
            } else if (arg == "--gr-interval") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --gr-interval\n";
                    return ParseStatus::Error;
                }
                p.gr_interval = std::atoi(argv[++i]);
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
        std::cout
            << "Usage: mpirun -np P " << progName << " [options]\n"
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
            << "  --rescale-freq <int> Rescale every N steps during equilibration (default: 0 = "
               "off)\n"
            << "  --rescale-end <int>  Stop continuous rescaling after this step (default: 0)\n"
            << "  --timing             Enable timing mode (implies --no-output)\n"
            << "  --gr                 Enable g(r) accumulation (LJ only)\n"
            << "  --gr-discard <int>   Equilibration steps to discard (default: 500)\n"
            << "  --gr-interval <int>  Sample g(r) every N steps (default: 10)\n"
            << "  --help               Print this message and exit\n";
    }
};

}  // namespace md

#endif  // MD_PARAMS_HPP
```

### `include/md/mpi_context.hpp` (107 lines)

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
 * @brief Encapsulates MPI state and particle decomposition.
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
        if (timingMode) {
            double t0 = MPI_Wtime();
            MPI_Allgatherv(posLocal.data(), 3 * localN, MPI_DOUBLE, posGlobal.data(),
                           recvcounts.data(), displs.data(), MPI_DOUBLE, MPI_COMM_WORLD);
            commTime += (MPI_Wtime() - t0);
        } else {
            MPI_Allgatherv(posLocal.data(), 3 * localN, MPI_DOUBLE, posGlobal.data(),
                           recvcounts.data(), displs.data(), MPI_DOUBLE, MPI_COMM_WORLD);
        }
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

### `include/md/system.hpp` (69 lines)

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
        for (int i = 0; i < 3 * localN; ++i) {
            pos[i] -= L * std::floor(pos[i] / L);
        }
    }
};

}  // namespace md

#endif  // MD_SYSTEM_HPP
```

### `include/md/rng.hpp` (152 lines)

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
inline std::vector<double> buildFCCLattice(int N, double L, std::mt19937_64& gen) {
    // Determine k such that N = 4*k^3 (validated by caller)
    int k = static_cast<int>(std::round(std::cbrt(N / 4.0)));

    std::vector<double> positions(3 * N);

    // Unit cell side length
    double a = L / k;

    // FCC basis vectors (fractional coordinates)
    const double basis[4][3] = {{0.0, 0.0, 0.0}, {0.5, 0.5, 0.0}, {0.5, 0.0, 0.5}, {0.0, 0.5, 0.5}};

    // Perturbation magnitude (zero-mean uniform distribution)
    double pertMag = 0.01 * constants::sigma;
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
 * @brief Generate Maxwell-Boltzmann velocities using Box-Muller transform.
 *
 * Generates 3N velocity components from a Gaussian distribution with
 * standard deviation sigma_v = sqrt(k_B * T / m). Uses pairs of uniform
 * deviates to produce pairs of normal deviates via the Box-Muller method.
 *
 * After generation:
 *   1. Centre-of-mass drift is removed (subtract mean velocity)
 *   2. Velocities are rescaled to exactly match the target temperature
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
        double z1 = mag * std::cos(2.0 * constants::pi * u2);
        double z2 = mag * std::sin(2.0 * constants::pi * u2);

        vel[i] = z1;
        if (i + 1 < totalComponents) {
            vel[i + 1] = z2;
        }
    }

    // Remove centre-of-mass drift
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

    // Rescale to exact target temperature: lambda = sqrt(T_target / T_measured)
    // T_measured = (2 / (N_dof * kB)) * E_kin, where N_dof = 3*(N-1)
    double eKin = 0.0;
    for (int i = 0; i < 3 * N; ++i) {
        eKin += vel[i] * vel[i];
    }
    eKin *= 0.5 * mass;

    int nDof = 3 * (N - 1);  // degrees of freedom after CoM removal
    double tMeasured = (2.0 * eKin) / (nDof * constants::kB);
    double lambda = std::sqrt(T / tMeasured);

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
 * Applies branch-predictor-friendly minimum image convention and hard
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

### `include/md/integrators.hpp` (103 lines)

```cpp
/**
 * @file integrators.hpp
 * @brief Forward Euler (AMM Eqn 4.27), RK4, and Velocity-Verlet integrators.
 *
 * Each integrator advances the system state by one timestep, including:
 *   - Position/velocity updates
 *   - Position wrapping into [0, L)
 *   - MPI_Allgatherv for global position synchronisation (LJ mode only)
 *   - Force recomputation from updated positions
 *
 * The MPI_Allgatherv placement follows §2.3 of the project charter:
 *   Velocity-Verlet: half-kick → drift → wrap → Allgatherv → force → half-kick
 *   Euler:           drift → vel update → wrap → Allgatherv → force (for next step)
 */

#ifndef MD_INTEGRATORS_HPP
#define MD_INTEGRATORS_HPP

#include <functional>
#include <string>
#include <vector>

#include "md/mpi_context.hpp"
#include "md/system.hpp"

namespace md {

/// Force computation function signature
using ForceFunc = std::function<void(System&, const std::vector<double>&, double&)>;

/**
 * @brief Forward Euler integrator (AMM Handout Eqn 4.27).
 *
 * Position update: x_{n+1} = x_n + v_n * dt + 0.5 * a_n * dt^2
 *   (2nd-order Taylor expansion for position)
 * Velocity update: v_{n+1} = v_n + a_n * dt
 *   (1st-order for velocity — this is the global error bottleneck)
 *
 * Global truncation error: O(dt). NOT symplectic. Energy drifts.
 *
 * MPI sequence: drift → vel update → wrap → Allgatherv → force (for next step)
 *
 * @param sys        System state
 * @param ctx        MPI context (for Allgatherv)
 * @param dt         Timestep
 * @param forceFunc  Force computation function
 * @param localPE    Output: local potential energy
 * @param isHO       If true, skip MPI_Allgatherv (HO communication bypass)
 */
void stepEuler(System& sys, MPIContext& ctx, double dt, ForceFunc forceFunc, double& localPE,
               bool isHO);

/**
 * @brief RK4 integrator (classical 4th-order Runge-Kutta).
 *
 * Reformulates the 2nd-order ODE as a first-order system:
 *   y = (x, v)^T,  f(y) = (v, a(x))^T
 *
 * Applies standard RK4 stages (k1, k2, k3, k4) and combines them
 * with the 1/6 weighting.
 *
 * Global truncation error: O(dt^4). NOT symplectic.
 * Requires 4 force evaluations per step.
 *
 * NOTE: Only used for HO verification. Impractical for LJ production
 * due to 4 MPI_Allgatherv calls per timestep.
 *
 * @param sys        System state
 * @param ctx        MPI context (for Allgatherv, if needed)
 * @param dt         Timestep
 * @param forceFunc  Force computation function
 * @param localPE    Output: local potential energy
 * @param isHO       If true, skip MPI_Allgatherv (HO communication bypass)
 */
void stepRK4(System& sys, MPIContext& ctx, double dt, ForceFunc forceFunc, double& localPE,
             bool isHO);

/**
 * @brief Velocity-Verlet integrator (half-kick / drift / half-kick form).
 *
 * Step 1 (half-kick):  v_{n+1/2} = v_n + 0.5 * a_n * dt
 * Step 2 (drift):      x_{n+1}   = x_n + v_{n+1/2} * dt
 * Step 3 (wrap):       Wrap x into [0, L)
 * Step 4 (gather):     MPI_Allgatherv to sync global positions
 * Step 5 (force eval): Compute a_{n+1} from global positions
 * Step 6 (half-kick):  v_{n+1}   = v_{n+1/2} + 0.5 * a_{n+1} * dt
 *
 * Global truncation error: O(dt^2). Symplectic and time-reversible.
 * Energy oscillates with bounded fluctuations (no drift).
 *
 * @param sys        System state
 * @param ctx        MPI context (for Allgatherv)
 * @param dt         Timestep
 * @param forceFunc  Force computation function
 * @param localPE    Output: local potential energy
 * @param isHO       If true, skip MPI_Allgatherv (HO communication bypass)
 */
void stepVelocityVerlet(System& sys, MPIContext& ctx, double dt, ForceFunc forceFunc,
                        double& localPE, bool isHO);

}  // namespace md

#endif  // MD_INTEGRATORS_HPP
```

### `include/md/observables.hpp` (146 lines)

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
inline double computeLocalKineticEnergy(const System& sys, double mass) {
    double eKin = 0.0;
    for (int i = 0; i < 3 * sys.localN; ++i) {
        eKin += sys.vel[i] * sys.vel[i];
    }
    return 0.5 * mass * eKin;
}

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
inline double computeTemperature(double eKinTotal, int N) {
    int nDof = 3 * (N - 1);  // degrees of freedom after CoM removal
    return (2.0 * eKinTotal) / (nDof * constants::kB);
}

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
inline void accumulateGR(const std::vector<double>& posGlobal, int N, double L, int offset,
                         int localN, double dr, double rMax, std::vector<double>& histogram) {
    double halfL = 0.5 * L;
    int nBins = static_cast<int>(histogram.size());

    for (int i = offset; i < offset + localN; ++i) {
        for (int j = i + 1; j < N; ++j) {
            double dx = posGlobal[3 * i + 0] - posGlobal[3 * j + 0];
            double dy = posGlobal[3 * i + 1] - posGlobal[3 * j + 1];
            double dz = posGlobal[3 * i + 2] - posGlobal[3 * j + 2];

            // Minimum image convention (branch-predictor friendly)
            if (dx > halfL)
                dx -= L;
            else if (dx < -halfL)
                dx += L;
            if (dy > halfL)
                dy -= L;
            else if (dy < -halfL)
                dy += L;
            if (dz > halfL)
                dz -= L;
            else if (dz < -halfL)
                dz += L;

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
inline void normaliseGR(std::vector<double>& histogram, double dr, int N, double L, int nFrames) {
    double V = L * L * L;
    double rho = N / V;

    for (int bin = 0; bin < static_cast<int>(histogram.size()); ++bin) {
        double rLow = bin * dr;
        double rMid = rLow + 0.5 * dr;
        double shellVol = 4.0 * constants::pi * rMid * rMid * dr;

        // Factor of 2: unordered pairs → ordered pairs
        if (shellVol > 0.0 && nFrames > 0) {
            histogram[bin] *= 2.0 / (rho * N * shellVol * nFrames);
        }
    }
}

}  // namespace md

#endif  // MD_OBSERVABLES_HPP
```

### `src/main.cpp` (357 lines)

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
#include <fstream>
#include <functional>
#include <iomanip>
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
        int rank;
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        if (rank == 0) {
            md::Params::printUsage(argv[0]);
        }
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
        L = 1.0e10;  // effectively unbounded for HO
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
                // Single RNG stream for both (no seed+offset code smell)
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
    md::ForceFunc forceFunc;
    if (isHO) {
        double omega = params.omega;
        double mass = md::constants::mass;
        forceFunc = [omega, mass](md::System& s, const std::vector<double>& pg, double& pe) {
            md::computeHOForces(s, pg, pe, omega, mass);
        };
    } else {
        double mass = md::constants::mass;
        forceFunc = [mass](md::System& s, const std::vector<double>& pg, double& pe) {
            md::computeLJForces(s, pg, pe, mass);
        };
    }

    // ── Initial force evaluation ──
    double localPE = 0.0;
    forceFunc(sys, ctx.posGlobal, localPE);

    // ── Create output directory and open file (rank 0 only) ──
    std::ofstream outFile;
    if (params.output && ctx.isRoot()) {
        mkdir("out", 0755);  // create if not exists, ignore error if exists
        std::string fname = "out/" + params.mode + "_" + params.integrator + ".csv";
        outFile.open(fname);
        if (outFile.is_open()) {
            outFile << std::setprecision(15);
            if (isHO) {
                // HO: output position, velocity, energy for phase-space & convergence plots
                outFile << "step,time,x,v,E_kin,E_pot,E_total\n";
            } else {
                outFile << "step,time,E_kin,E_pot,E_total,temperature\n";
            }
        }
    }

    // ── Print simulation info (rank 0) ──
    if (ctx.isRoot()) {
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
    const double grDr = 0.02 * md::constants::sigma;  // bin width = 0.02*sigma
    const double grRMax = 0.5 * L;                    // bin range = [0, L/2]
    const int grNBins = static_cast<int>(grRMax / grDr);
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

            // ── Velocity rescaling (single-step or continuous thermostat) ──
            // NOTE: totalKE is only valid on rank 0 (from MPI_Reduce), so we
            // compute lambda on root and broadcast it to ensure ALL ranks rescale.
            bool doRescale = false;

            // Single-step rescale (legacy --rescale-step flag)
            if (step == params.rescale_step && !isHO) {
                doRescale = true;
            }

            // Continuous thermostat during equilibration
            if (params.rescale_freq > 0 && step <= params.rescale_end && !isHO &&
                step % params.rescale_freq == 0) {
                doRescale = true;
            }

            if (doRescale) {
                double lambda = 1.0;
                if (ctx.isRoot()) {
                    double tMeasured = md::computeTemperature(totalKE, N);
                    if (tMeasured > 1e-30) {
                        lambda = std::sqrt(params.T_init / tMeasured);
                    }
                    std::printf(
                        "Rescale at step %d: lambda = %.15e, T_before = %.6f K, T_after = %.6f "
                        "K\n",
                        step, lambda, tMeasured, params.T_init);
                }
                MPI_Bcast(&lambda, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
                for (int i = 0; i < 3 * sys.localN; ++i) {
                    sys.vel[i] *= lambda;
                }
            }
        }

        // ── Accumulate g(r) histogram (LJ only, after equilibration) ──
        if (params.gr && !isHO && step >= params.gr_discard &&
            (step - params.gr_discard) % params.gr_interval == 0) {
            md::accumulateGR(ctx.posGlobal, N, L, ctx.offset, ctx.localN, grDr, grRMax,
                             grHistLocal);
            ++grFrames;
        }

        // ── Advance one timestep (skip on the last iteration — we only want observables) ──
        if (step == params.steps)
            break;

        if (params.integrator == "euler") {
            md::stepEuler(sys, ctx, params.dt, forceFunc, localPE, isHO);
        } else if (params.integrator == "rk4") {
            md::stepRK4(sys, ctx, params.dt, forceFunc, localPE, isHO);
        } else {  // "verlet" (default)
            md::stepVelocityVerlet(sys, ctx, params.dt, forceFunc, localPE, isHO);
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

            std::ofstream grFile("out/gr.csv");
            if (grFile.is_open()) {
                grFile << "r_sigma,gr\n";
                for (int b = 0; b < grNBins; ++b) {
                    double rMid = (b + 0.5) * grDr;
                    grFile << (rMid / md::constants::sigma) << "," << grHistGlobal[b] << "\n";
                }
                grFile.close();
                std::printf("g(r) written to out/gr.csv (%d bins, %d frames)\n", grNBins, grFrames);
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

### `src/integrators/euler.cpp` (50 lines)

```cpp
/**
 * @file euler.cpp
 * @brief Forward Euler integrator (AMM Handout Eqn 4.27).
 *
 * Position update: x_{n+1} = x_n + v_n * dt + 0.5 * a_n * dt^2
 *   (2nd-order Taylor expansion for position)
 * Velocity update: v_{n+1} = v_n + a_n * dt
 *   (1st-order for velocity — global error bottleneck)
 *
 * MPI sequence (v4 lock-in):
 *   1. Drift:  x_{n+1} = x_n + v_n * dt + 0.5 * a_n * dt^2
 *   2. Vel:    v_{n+1} = v_n + a_n * dt
 *   3. Wrap:   x into [0, L)
 *   4. Gather: MPI_Allgatherv (skipped for HO mode)
 *   5. Force:  Compute a_{n+1} for next timestep
 */

#include "md/integrators.hpp"

namespace md {

void stepEuler(System& sys, MPIContext& ctx, double dt, ForceFunc forceFunc, double& localPE,
               bool isHO) {
    const int n3 = 3 * sys.localN;

    // Step 1: Drift — x_{n+1} = x_n + v_n * dt + 0.5 * a_n * dt^2
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] += sys.vel[i] * dt + 0.5 * sys.acc[i] * dt * dt;
    }

    // Step 2: Velocity update — v_{n+1} = v_n + a_n * dt
    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += sys.acc[i] * dt;
    }

    // Step 3: Wrap positions into [0, L) (LJ only — wrapping corrupts HO oscillation)
    if (!isHO) {
        sys.wrapPositions();
    }

    // Step 4: Gather global positions (skipped for HO — no inter-particle interaction)
    if (!isHO) {
        ctx.allgatherPositions(sys.pos);
    }

    // Step 5: Compute forces from updated positions (a_{n+1} for next step)
    forceFunc(sys, ctx.posGlobal, localPE);
}

}  // namespace md
```

### `src/integrators/rk4.cpp` (106 lines)

```cpp
/**
 * @file rk4.cpp
 * @brief 4th-order Runge-Kutta integrator.
 *
 * Reformulates the 2nd-order ODE as a first-order system:
 *   y = (x, v)^T,  f(y) = (v, a(x))^T
 *
 * Standard RK4 stages:
 *   k1 = dt * f(y_n)
 *   k2 = dt * f(y_n + k1/2)
 *   k3 = dt * f(y_n + k2/2)
 *   k4 = dt * f(y_n + k3)
 *   y_{n+1} = y_n + (k1 + 2*k2 + 2*k3 + k4) / 6
 *
 * Requires 4 force evaluations per step. Only used for HO verification.
 * Impractical for parallel LJ due to 4 MPI_Allgatherv calls per timestep.
 */

#include "md/integrators.hpp"

namespace md {

void stepRK4(System& sys, MPIContext& ctx, double dt, ForceFunc forceFunc, double& localPE,
             bool isHO) {
    const int n3 = 3 * sys.localN;

    // Save initial state
    std::vector<double> x0(sys.pos);
    std::vector<double> v0(sys.vel);

    // ── Stage 1: k1 = dt * f(y_n) ──
    // Forces already computed from previous step (stored in sys.acc)
    std::vector<double> k1x(n3), k1v(n3);
    for (int i = 0; i < n3; ++i) {
        k1x[i] = dt * sys.vel[i];  // dx/dt = v
        k1v[i] = dt * sys.acc[i];  // dv/dt = a(x)
    }

    // ── Stage 2: k2 = dt * f(y_n + k1/2) ──
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] = x0[i] + 0.5 * k1x[i];
        sys.vel[i] = v0[i] + 0.5 * k1v[i];
    }
    if (!isHO)
        sys.wrapPositions();
    if (!isHO)
        ctx.allgatherPositions(sys.pos);
    forceFunc(sys, ctx.posGlobal, localPE);

    std::vector<double> k2x(n3), k2v(n3);
    for (int i = 0; i < n3; ++i) {
        k2x[i] = dt * sys.vel[i];
        k2v[i] = dt * sys.acc[i];
    }

    // ── Stage 3: k3 = dt * f(y_n + k2/2) ──
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] = x0[i] + 0.5 * k2x[i];
        sys.vel[i] = v0[i] + 0.5 * k2v[i];
    }
    if (!isHO)
        sys.wrapPositions();
    if (!isHO)
        ctx.allgatherPositions(sys.pos);
    forceFunc(sys, ctx.posGlobal, localPE);

    std::vector<double> k3x(n3), k3v(n3);
    for (int i = 0; i < n3; ++i) {
        k3x[i] = dt * sys.vel[i];
        k3v[i] = dt * sys.acc[i];
    }

    // ── Stage 4: k4 = dt * f(y_n + k3) ──
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] = x0[i] + k3x[i];
        sys.vel[i] = v0[i] + k3v[i];
    }
    if (!isHO)
        sys.wrapPositions();
    if (!isHO)
        ctx.allgatherPositions(sys.pos);
    forceFunc(sys, ctx.posGlobal, localPE);

    std::vector<double> k4x(n3), k4v(n3);
    for (int i = 0; i < n3; ++i) {
        k4x[i] = dt * sys.vel[i];
        k4v[i] = dt * sys.acc[i];
    }

    // ── Combine: y_{n+1} = y_n + (k1 + 2*k2 + 2*k3 + k4) / 6 ──
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] = x0[i] + (k1x[i] + 2.0 * k2x[i] + 2.0 * k3x[i] + k4x[i]) / 6.0;
        sys.vel[i] = v0[i] + (k1v[i] + 2.0 * k2v[i] + 2.0 * k3v[i] + k4v[i]) / 6.0;
    }

    // Wrap final positions (LJ only)
    if (!isHO)
        sys.wrapPositions();

    // Recompute forces at final state
    if (!isHO)
        ctx.allgatherPositions(sys.pos);
    forceFunc(sys, ctx.posGlobal, localPE);
}

}  // namespace md
```

### `src/integrators/velocity_verlet.cpp` (58 lines)

```cpp
/**
 * @file velocity_verlet.cpp
 * @brief Velocity-Verlet integrator (half-kick / drift / half-kick form).
 *
 * MPI-aware sequence (v4 lock-in, §2.3):
 *   Step 1 (half-kick):  v_{n+1/2} = v_n + 0.5 * a_n * dt
 *   Step 2 (drift):      x_{n+1}   = x_n + v_{n+1/2} * dt
 *   Step 3 (wrap):       Wrap x into [0, L)
 *   Step 4 (gather):     MPI_Allgatherv to sync global positions
 *   Step 5 (force eval): Compute a_{n+1} from global positions
 *   Step 6 (half-kick):  v_{n+1}   = v_{n+1/2} + 0.5 * a_{n+1} * dt
 *
 * The Allgatherv is placed immediately after the position update and
 * wrap, but before the force evaluation, to guarantee that all ranks
 * compute forces against a consistent, globally-synchronised snapshot.
 *
 * Global truncation error: O(dt^2). Symplectic and time-reversible.
 */

#include "md/integrators.hpp"

namespace md {

void stepVelocityVerlet(System& sys, MPIContext& ctx, double dt, ForceFunc forceFunc,
                        double& localPE, bool isHO) {
    const int n3 = 3 * sys.localN;
    const double halfDt = 0.5 * dt;

    // Step 1: Half-kick — v_{n+1/2} = v_n + 0.5 * a_n * dt
    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += halfDt * sys.acc[i];
    }

    // Step 2: Drift — x_{n+1} = x_n + v_{n+1/2} * dt
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] += dt * sys.vel[i];
    }

    // Step 3: Wrap positions into [0, L) (LJ only — wrapping corrupts HO oscillation)
    if (!isHO) {
        sys.wrapPositions();
    }

    // Step 4: Gather global positions (skipped for HO — no inter-particle interaction)
    if (!isHO) {
        ctx.allgatherPositions(sys.pos);
    }

    // Step 5: Compute forces from updated positions
    forceFunc(sys, ctx.posGlobal, localPE);

    // Step 6: Half-kick — v_{n+1} = v_{n+1/2} + 0.5 * a_{n+1} * dt
    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += halfDt * sys.acc[i];
    }
}

}  // namespace md
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

### `src/potentials/lennard_jones.cpp` (112 lines)

```cpp
/**
 * @file lennard_jones.cpp
 * @brief Lennard-Jones force/energy kernel with optimised intermediates.
 *
 * Uses the shared-intermediate approach (no pow, no sqrt in the force loop):
 *   inv_r2 → inv_r6 → inv_r12
 *
 * Applies branch-predictor-friendly minimum image convention and hard
 * cutoff at rcut = 2.25*sigma.
 *
 * Potential energy is accumulated unconditionally for all j != i (no i<j
 * branch in the inner loop). The local sum is multiplied by 0.5 AFTER
 * the loop to correct for double-counting, guaranteeing pipeline
 * efficiency on superscalar CPUs.
 */

#include "md/constants.hpp"
#include "md/potentials.hpp"

namespace md {

void computeLJForces(System& sys, const std::vector<double>& posGlobal, double& localPE,
                     double mass) {
    const double L = sys.L;
    const double halfL = 0.5 * L;
    const int N = sys.N;
    const int offset = sys.offset;
    const int localN = sys.localN;

    // Pre-computed constants (from constants.hpp)
    const double s6 = constants::sigma6;
    const double s12 = constants::sigma12;
    const double fe = constants::four_eps;
    const double te = constants::twentyfour_eps;
    const double rc2 = constants::rcut2;
    const double inv_mass = 1.0 / mass;

    // Zero local forces and PE
    for (int i = 0; i < 3 * localN; ++i) {
        sys.acc[i] = 0.0;
    }
    localPE = 0.0;

    for (int i = 0; i < localN; ++i) {
        int gi = offset + i;  // global index

        double xi = posGlobal[3 * gi + 0];
        double yi = posGlobal[3 * gi + 1];
        double zi = posGlobal[3 * gi + 2];

        double fx = 0.0, fy = 0.0, fz = 0.0;
        double pei = 0.0;

        for (int j = 0; j < N; ++j) {
            // Skip self-interaction to avoid r^2 = 0 singularity
            if (j == gi)
                continue;

            double dx = xi - posGlobal[3 * j + 0];
            double dy = yi - posGlobal[3 * j + 1];
            double dz = zi - posGlobal[3 * j + 2];

            // Branch-predictor-friendly MIC (avoids std::round overhead in O(N^2) loop)
            if (dx > halfL)
                dx -= L;
            else if (dx < -halfL)
                dx += L;

            if (dy > halfL)
                dy -= L;
            else if (dy < -halfL)
                dy += L;

            if (dz > halfL)
                dz -= L;
            else if (dz < -halfL)
                dz += L;

            double r2 = dx * dx + dy * dy + dz * dz;

            if (r2 >= rc2)
                continue;  // hard cutoff

            double inv_r2 = 1.0 / r2;
            double inv_r6 = inv_r2 * inv_r2 * inv_r2;
            double inv_r12 = inv_r6 * inv_r6;

            // Potential energy (accumulate unconditionally — multiply by 0.5 after loop)
            pei += fe * (s12 * inv_r12 - s6 * inv_r6);

            // Force scalar: f/r = 24*eps/r^2 * [2*(sigma/r)^12 - (sigma/r)^6]
            double fScalar = te * inv_r2 * (2.0 * s12 * inv_r12 - s6 * inv_r6);

            fx += fScalar * dx;
            fy += fScalar * dy;
            fz += fScalar * dz;
        }

        // Store as acceleration: a = F/m
        sys.acc[3 * i + 0] = fx * inv_mass;
        sys.acc[3 * i + 1] = fy * inv_mass;
        sys.acc[3 * i + 2] = fz * inv_mass;

        localPE += pei;
    }

    // Correct for double-counting: each pair (i,j) counted once from i's side
    // and once from j's side, so multiply by 0.5
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

### `tests/test_mic.cpp` (130 lines)

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

namespace {

/// Apply the branch-predictor-friendly MIC to a single displacement component
inline double applyMIC(double dx, double L) {
    double halfL = 0.5 * L;
    if (dx > halfL)
        dx -= L;
    else if (dx < -halfL)
        dx += L;
    return dx;
}

}  // namespace

int testMIC() {
    int failures = 0;
    double L = 10.0;
    double tol = 1e-14;

    // Test 1: displacement within [-L/2, L/2) should be unchanged
    {
        double dx = 3.0;
        double result = applyMIC(dx, L);
        if (std::abs(result - 3.0) > tol) {
            std::printf("FAIL: MIC unchanged test: got %e, expected 3.0\n", result);
            ++failures;
        }
    }

    // Test 2: displacement > L/2 should wrap by -L
    {
        double dx = 7.0;  // > 5.0 = L/2
        double result = applyMIC(dx, L);
        if (std::abs(result - (-3.0)) > tol) {
            std::printf("FAIL: MIC positive wrap: got %e, expected -3.0\n", result);
            ++failures;
        }
    }

    // Test 3: displacement < -L/2 should wrap by +L
    {
        double dx = -6.0;  // < -5.0
        double result = applyMIC(dx, L);
        if (std::abs(result - 4.0) > tol) {
            std::printf("FAIL: MIC negative wrap: got %e, expected 4.0\n", result);
            ++failures;
        }
    }

    // Test 4: displacement at exactly L/2 boundary
    {
        double dx = 5.0;  // == L/2 (should remain, since condition is strict >)
        double result = applyMIC(dx, L);
        // dx == halfL is not > halfL, so it stays as-is
        if (std::abs(result - 5.0) > tol) {
            std::printf("FAIL: MIC boundary L/2: got %e, expected 5.0\n", result);
            ++failures;
        }
    }

    // Test 5: displacement at exactly -L/2 boundary
    {
        double dx = -5.0;  // == -L/2 (should remain)
        double result = applyMIC(dx, L);
        if (std::abs(result - (-5.0)) > tol) {
            std::printf("FAIL: MIC boundary -L/2: got %e, expected -5.0\n", result);
            ++failures;
        }
    }

    // Test 6: zero displacement
    {
        double dx = 0.0;
        double result = applyMIC(dx, L);
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
        dx = applyMIC(dx, L);
        dy = applyMIC(dy, L);
        dz = applyMIC(dz, L);

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

---

## 6. Build System & Scripts

### `Makefile`

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
SRC_MAIN      = src/main.cpp
SRC_EULER     = src/integrators/euler.cpp
SRC_RK4       = src/integrators/rk4.cpp
SRC_VERLET    = src/integrators/velocity_verlet.cpp
SRC_HARMONIC  = src/potentials/harmonic.cpp
SRC_LJ        = src/potentials/lennard_jones.cpp

SRCS = $(SRC_MAIN) $(SRC_EULER) $(SRC_RK4) $(SRC_VERLET) $(SRC_HARMONIC) $(SRC_LJ)
OBJS = $(SRCS:.cpp=.o)

# Test files
TEST_SRCS = tests/test_runner.cpp tests/test_mic.cpp tests/test_force.cpp
TEST_OBJS = $(TEST_SRCS:.cpp=.o)
# Tests also need the LJ potential (for test_force.cpp)
TEST_DEPS = src/potentials/lennard_jones.o src/potentials/harmonic.o

TARGET    = md_solver
TEST_BIN  = test_runner

TARBALL   = candidate_BCN_wa2.tar.gz

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

### `README.md`

# WA2: MPI Parallelisation of Molecular Dynamics

## Dependencies

- C++17 compiler with MPI (tested with OpenMPI 4.x + GCC 8+)
- Python 3 with matplotlib, numpy, scipy (for plotting scripts)

## Build

```bash
make            # builds md_solver
make test       # runs unit tests (exits non-zero on failure)
```

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
# Primary run: 100 steps, Velocity-Verlet (NVE, no mid-run rescale)
mkdir -p out
mpirun -np 1 ./md_solver --mode lj --integrator verlet --N 864 --steps 100

# Primary run: 100 steps, Euler
mpirun -np 1 ./md_solver --mode lj --integrator euler --N 864 --steps 100

# With equilibration rescale at step 10
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --steps 100 --rescale-step 10

# Supplementary g(r) (extended run, ~450 frames for smooth Rahman comparison)
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --steps 5000 --gr --gr-discard 500 --gr-interval 10
```

### Scaling (Results 3)

```bash
# Strong scaling: fixed N, vary P
mpirun -np 1  ./md_solver --mode lj --integrator verlet --N 2048 --steps 100 --timing
mpirun -np 2  ./md_solver --mode lj --integrator verlet --N 2048 --steps 100 --timing
mpirun -np 4  ./md_solver --mode lj --integrator verlet --N 2048 --steps 100 --timing
mpirun -np 8  ./md_solver --mode lj --integrator verlet --N 2048 --steps 100 --timing
mpirun -np 16 ./md_solver --mode lj --integrator verlet --N 2048 --steps 100 --timing

# Size scaling: fixed P, vary N
mpirun -np 16 ./md_solver --mode lj --integrator verlet --N 108  --steps 100 --timing
mpirun -np 16 ./md_solver --mode lj --integrator verlet --N 256  --steps 100 --timing
mpirun -np 16 ./md_solver --mode lj --integrator verlet --N 500  --steps 100 --timing
mpirun -np 16 ./md_solver --mode lj --integrator verlet --N 864  --steps 100 --timing
mpirun -np 16 ./md_solver --mode lj --integrator verlet --N 1372 --steps 100 --timing
mpirun -np 16 ./md_solver --mode lj --integrator verlet --N 2048 --steps 100 --timing
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
include/md/    — C++ headers (constants, params, system, integrators, potentials, observables, MPI)
src/           — Source implementations (main, integrators/, potentials/)
tests/         — Homebrew unit tests (MIC wrapping, LJ force, position wrapping)
scripts/       — Python plotting scripts and bash automation
out/           — Generated data (excluded from submission)
ai/            — AI context workspace (excluded from submission)
```

### `.clang-format`

```yaml
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 100
AllowShortFunctionsOnASingleLine: Inline
AllowShortIfStatementsOnASingleLine: false
AllowShortLoopsOnASingleLine: false
BreakBeforeBraces: Attach
PointerAlignment: Left
```

### `.gitignore`

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

### `scripts/run_all_data.sh` (155 lines)

```sh
#!/bin/bash
# ──────────────────────────────────────────────────────────────────
# run_all_data.sh — Generate ALL production data for the report
#
# Designed for shared HPC clusters (cerberus1). Uses median-of-5
# repetitions for scaling benchmarks to filter contention noise.
#
# Usage:
#   bash scripts/run_all_data.sh
# ──────────────────────────────────────────────────────────────────

SOLVER="./md_solver"
OUTDIR="out"

mkdir -p "$OUTDIR/ho" "$OUTDIR/lj"

echo "=========================================="
echo "  FULL DATA GENERATION — $(date)"
echo "=========================================="

# Helper: compute median of 5 values
median5() {
    echo "$@" | tr ' ' '\n' | sort -g | sed -n '3p'
}

# ── 0. Parallel Consistency Check ──
echo ""
echo "=== PARALLEL CONSISTENCY CHECK ==="
mpirun -np 1 $SOLVER --mode lj --N 108 --steps 10 2>/dev/null | grep "^[0-9]" > /tmp/d1.txt
mpirun -np 2 $SOLVER --mode lj --N 108 --steps 10 2>/dev/null | grep "^[0-9]" > /tmp/d2.txt
if diff -q /tmp/d1.txt /tmp/d2.txt > /dev/null 2>&1; then
    echo "  P=1 vs P=2 data: MATCH ✅"
else
    echo "  P=1 vs P=2 data: MISMATCH ❌"
fi

# ── 1. Results 1: HO Convergence ──
echo ""
echo "=== RESULTS 1: HO CONVERGENCE ==="
# dt values and corresponding steps (T_final = 10 for all)
# Using shell arithmetic to avoid python3 dependency
DT_LIST="1.0:10 0.5:20 0.1:100 0.05:200 0.01:1000 0.005:2000 0.001:10000 0.0005:20000"
for INT in euler verlet rk4; do
    for ENTRY in $DT_LIST; do
        DT=$(echo $ENTRY | cut -d: -f1)
        STEPS=$(echo $ENTRY | cut -d: -f2)
        mpirun -np 1 $SOLVER --mode ho --integrator $INT --N 1 --steps $STEPS --dt $DT 2>/dev/null
        SRCFILE="$OUTDIR/ho_${INT}.csv"
        DSTFILE="$OUTDIR/ho/${INT}_dt${DT}.csv"
        if [ -s "$SRCFILE" ]; then
            cp "$SRCFILE" "$DSTFILE"
            LINES=$(wc -l < "$DSTFILE")
            echo "  $INT dt=$DT steps=$STEPS -> $DSTFILE ($LINES lines)"
        else
            echo "  $INT dt=$DT steps=$STEPS -> FAILED (no output file)"
        fi
    done
done

# ── 2. Results 2: LJ Production ──
echo ""
echo "=== RESULTS 2: LJ PRODUCTION ==="

echo "  Verlet N=864 100 steps..."
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 --steps 100 2>/dev/null
if [ -s "$OUTDIR/lj_verlet.csv" ]; then
    cp "$OUTDIR/lj_verlet.csv" "$OUTDIR/lj/verlet_864_100.csv"
    echo "  -> lj/verlet_864_100.csv ($(wc -l < "$OUTDIR/lj/verlet_864_100.csv") lines) ✅"
fi

echo "  Euler N=864 100 steps..."
mpirun -np 4 $SOLVER --mode lj --integrator euler --N 864 --steps 100 2>/dev/null
if [ -s "$OUTDIR/lj_euler.csv" ]; then
    cp "$OUTDIR/lj_euler.csv" "$OUTDIR/lj/euler_864_100.csv"
    echo "  -> lj/euler_864_100.csv ($(wc -l < "$OUTDIR/lj/euler_864_100.csv") lines) ✅"
fi

# ── 3. g(r) Production Run ──
echo ""
echo "=== g(r) PRODUCTION RUN ==="
mpirun -np 4 $SOLVER --mode lj --integrator verlet --N 864 --steps 25500 \
    --rescale-freq 10 --rescale-end 500 --gr --gr-discard 500 --gr-interval 10 2>/dev/null
if [ -s "$OUTDIR/gr.csv" ]; then
    echo "  g(r) done: $(wc -l < "$OUTDIR/gr.csv") lines ✅"
else
    echo "  g(r) FAILED ❌"
fi

# ── 4. Strong Scaling (median of 5) ──
echo ""
echo "=== RESULTS 3: STRONG SCALING (5 reps, N=2048, 200 steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_strong.csv"

for P in 1 2 4 8 16 24 32; do
    WALLS=""
    COMMS=""
    for REP in 1 2 3 4 5; do
        OUTPUT=$(mpirun -np $P $SOLVER --mode lj --N 2048 --steps 200 --timing 2>/dev/null)
        W=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
        C=$(echo "$OUTPUT" | grep "Comm time" | awk '{print $3}')
        [ -z "$C" ] && C="0.0"
        WALLS="$WALLS $W"
        COMMS="$COMMS $C"
        echo "    P=$P rep=$REP wall=$W comm=$C"
    done
    MEDIAN_W=$(median5 $WALLS)
    MEDIAN_C=$(median5 $COMMS)
    echo "$P,2048,$MEDIAN_W,$MEDIAN_C" >> "$OUTDIR/scaling_strong.csv"
    echo "  >> P=$P MEDIAN: wall=$MEDIAN_W comm=$MEDIAN_C"
done

# ── 5. Size Scaling (median of 5) ──
echo ""
echo "=== RESULTS 3: SIZE SCALING (5 reps, P=16, 200 steps) ==="
echo "P,N,wall_s,comm_s" > "$OUTDIR/scaling_size.csv"

for N in 108 256 500 864 1372 2048; do
    WALLS=""
    COMMS=""
    for REP in 1 2 3 4 5; do
        OUTPUT=$(mpirun -np 16 $SOLVER --mode lj --N $N --steps 200 --timing 2>/dev/null)
        W=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
        C=$(echo "$OUTPUT" | grep "Comm time" | awk '{print $3}')
        [ -z "$C" ] && C="0.0"
        WALLS="$WALLS $W"
        COMMS="$COMMS $C"
        echo "    N=$N rep=$REP wall=$W comm=$C"
    done
    MEDIAN_W=$(median5 $WALLS)
    MEDIAN_C=$(median5 $COMMS)
    echo "16,$N,$MEDIAN_W,$MEDIAN_C" >> "$OUTDIR/scaling_size.csv"
    echo "  >> N=$N MEDIAN: wall=$MEDIAN_W comm=$MEDIAN_C"
done

# ── Summary ──
echo ""
echo "=========================================="
echo "  ALL DONE — $(date)"
echo "=========================================="
echo ""
echo "=== FILE INVENTORY ==="
echo "HO convergence files:"
ls -la "$OUTDIR/ho/" 2>/dev/null | grep csv
echo ""
echo "LJ production files:"
ls -la "$OUTDIR/lj/" 2>/dev/null | grep csv
echo ""
echo "g(r):"
ls -la "$OUTDIR/gr.csv" 2>/dev/null
echo ""
echo "Strong scaling:"
cat "$OUTDIR/scaling_strong.csv"
echo ""
echo "Size scaling:"
cat "$OUTDIR/scaling_size.csv"
```

### `scripts/run_scaling.sh` (112 lines)

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
# Usage: pick_median_pair "w1 w2 w3 w4 w5" "c1 c2 c3 c4 c5"
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

        WALL=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
        COMM=$(echo "$OUTPUT" | grep "Comm time" | awk '{print $3}')
        # P=1 has no comm line
        if [ -z "$COMM" ]; then COMM="0.000000"; fi

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
            --N "$N" --steps "$STEPS" --timing 2>&1)

        WALL=$(echo "$OUTPUT" | grep "Wall time" | awk '{print $3}')
        COMM=$(echo "$OUTPUT" | grep "Comm time" | awk '{print $3}')
        if [ -z "$COMM" ]; then COMM="0.000000"; fi

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

### `scripts/plot_ho.py` (252 lines)

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
from scipy.stats import linregress

# ── Configuration ──
INTEGRATORS = ["euler", "verlet", "rk4"]
INTEGRATOR_LABELS = {"euler": "Euler (AMM 4.27)", "rk4": "RK4", "verlet": "Velocity-Verlet"}
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


def load_csv(filepath):
    """Load CSV with headers."""
    return np.genfromtxt(filepath, delimiter=',', names=True)


def plot_trajectories():
    """Plot x(t), v(t), phase space for all integrators at dt=0.01."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    t_exact = np.linspace(0, T_FINAL, 1000)
    x_exact, v_exact = exact_solution(t_exact)

    for integ in INTEGRATORS:
        fpath = f"{HO_DIR}/{integ}_dt{TRAJ_DT}.csv"
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
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(t_exact, v_exact, 'k--', linewidth=1, alpha=0.5, label='Exact')
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Velocity v')
    axes[1].set_title('Velocity vs Time')
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)

    x_ep, v_ep = exact_solution(np.linspace(0, 2 * np.pi / OMEGA, 500))
    axes[2].plot(x_ep, v_ep, 'k--', linewidth=1, alpha=0.5, label='Exact')
    axes[2].set_xlabel('Position x')
    axes[2].set_ylabel('Velocity v')
    axes[2].set_title('Phase Space (v vs x)')
    axes[2].legend(fontsize=9)
    axes[2].set_aspect('equal')
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/ho_trajectories.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_trajectories.png")


def plot_convergence():
    """Log-log convergence plot with fitted slopes."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))

    x_ex_final, _ = exact_solution(T_FINAL)

    for integ in INTEGRATORS:
        errors = []
        dts = []

        for dt in DT_VALUES:
            fpath = f"{HO_DIR}/{integ}_dt{dt}.csv"
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
        slope, intercept, r_value, _, _ = linregress(log_dt, log_err)

        color = INTEGRATOR_COLORS[integ]
        expected = INTEGRATOR_ORDERS[integ]
        label = f"{INTEGRATOR_LABELS[integ]} (slope={slope:.2f}, expected {expected})"

        ax.loglog(dts, errors, 'o-', color=color, label=label,
                  linewidth=2, markersize=6)

        # Reference slope line
        dt_ref = np.array([min(dts), max(dts)])
        err_ref = errors[0] * (dt_ref / dts[0]) ** expected
        ax.loglog(dt_ref, err_ref, '--', color=color, alpha=0.4, linewidth=1)

    ax.set_xlabel(r'$\Delta t$', fontsize=14)
    ax.set_ylabel(r'$|x_{num}(T) - x_{exact}(T)|$', fontsize=14)
    ax.set_title('Convergence: Position Error vs Timestep', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, which='both', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/ho_convergence.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_convergence.png")


def plot_energy_conservation():
    """Energy conservation comparison for all integrators."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    for integ in INTEGRATORS:
        fpath = f"{HO_DIR}/{integ}_dt{TRAJ_DT}.csv"
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
    ax.grid(True, alpha=0.3)

    # Add zoomed inset to show VV vs RK4 near zero
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    axins = inset_axes(ax, width="40%", height="30%", loc="lower right", borderpad=2)
    
    for integ in INTEGRATORS:
        if integ == "euler": continue # Skip Euler for inset
        fpath = f"{HO_DIR}/{integ}_dt{TRAJ_DT}.csv"
        if not os.path.exists(fpath): continue
        data = load_csv(fpath)
        t = data['time']
        E = data['E_total']
        E0 = E[0]
        rel_dev = (E - E0) / abs(E0) if abs(E0) > 1e-30 else E - E0
        axins.plot(t, rel_dev, color=INTEGRATOR_COLORS[integ], linewidth=1.5)
    
    axins.set_title('Zoom: VV vs RK4', fontsize=9)
    axins.grid(True, alpha=0.3)
    axins.tick_params(axis='both', which='major', labelsize=8)
    
    # Optional: adjust y-limits of inset manually if needed
    # (Leaving it auto-scaled, which usually captures the O(1e-4) VV vs O(1e-15) RK4 nicely.)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/ho_energy.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/ho_energy.png")


if __name__ == "__main__":
    if "--run" in sys.argv:
        run_ho_simulations()

    plot_trajectories()
    plot_convergence()
    plot_energy_conservation()
```

### `scripts/plot_lj.py` (226 lines)

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


def load_csv(filepath):
    """Load CSV with headers."""
    return np.genfromtxt(filepath, delimiter=',', names=True)


def plot_energy_conservation():
    """Plot E_kin, E_pot, E_total vs time for Verlet and Euler."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    configs = [
        ("verlet_864_100", "Velocity-Verlet (NVE)", "#2ecc71"),
        ("euler_864_100", "Euler (AMM Eqn 4.27)", "#e74c3c"),
    ]

    for idx, (fname, label, color) in enumerate(configs):
        fpath = f"{LJ_DIR}/{fname}.csv"
        if not os.path.exists(fpath):
            print(f"Warning: {fpath} not found, skipping")
            continue

        data = load_csv(fpath)
        t = data['time'] * 1e12  # ps
        ekin = data['E_kin'] / EPSILON
        epot = data['E_pot'] / EPSILON
        etot = data['E_total'] / EPSILON

        ax = axes[idx, 0]
        ax.plot(t, ekin, label=r'$E_{kin}$', color='#e74c3c', linewidth=1.5)
        ax.plot(t, epot, label=r'$E_{pot}$', color='#3498db', linewidth=1.5)
        ax.plot(t, etot, label=r'$E_{total}$', color='#2c3e50', linewidth=2)
        ax.set_xlabel('Time [ps]')
        ax.set_ylabel(r'Energy [$\varepsilon$]')
        ax.set_title(f'{label}: Energy vs Time')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Relative deviation
        ax2 = axes[idx, 1]
        e0 = etot[0]
        rel_dev = (etot - e0) / abs(e0) if abs(e0) > 1e-30 else etot - e0
        ax2.plot(t, rel_dev, color=color, linewidth=1.5)
        ax2.set_xlabel('Time [ps]')
        ax2.set_ylabel(r'$(E_{total} - E_0) / |E_0|$')
        ax2.set_title(f'{label}: Relative Energy Deviation')
        ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_energy.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_energy.png")


def plot_temperature():
    """Plot temperature vs time."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    configs = [
        ("verlet_864_100", "Velocity-Verlet", "#2ecc71"),
        ("euler_864_100", "Euler (AMM 4.27)", "#e74c3c"),
    ]

    for fname, label, color in configs:
        fpath = f"{LJ_DIR}/{fname}.csv"
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
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_temperature.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_temperature.png")


def plot_equilibrated_comparison():
    """Compare raw NVE vs equilibrated NVE energy deviation."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # --- Left panel: full trajectories ---
    configs = [
        ("verlet_864_100", "Raw NVE (100 steps)", "#e74c3c", '-'),
        ("verlet_864_200_equilibrated", "Equilibrated (rescale→100, NVE→200)", "#2ecc71", '-'),
    ]

    for fname, label, color, ls in configs:
        fpath = f"{LJ_DIR}/{fname}.csv"
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
             fontsize=9, color='gray', va='center')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # --- Right panel: NVE-only phase comparison ---
    # Raw NVE: all 100 steps
    fpath_raw = f"{LJ_DIR}/verlet_864_100.csv"
    fpath_eq = f"{LJ_DIR}/verlet_864_200_equilibrated.csv"

    if os.path.exists(fpath_raw):
        data = load_csv(fpath_raw)
        etot = data['E_total'] / EPSILON
        e0 = etot[0]
        nve_steps = np.arange(len(etot))
        ax2.plot(nve_steps, (etot - e0) / abs(e0), color='#e74c3c', linewidth=1.5,
                 label=f'Raw NVE (drift={abs(etot[-1]-e0)/abs(e0)*100:.2f}%)')

    if os.path.exists(fpath_eq):
        data = load_csv(fpath_eq)
        # NVE phase starts after step 100
        nve_mask = data['step'] > 100
        if np.any(nve_mask):
            etot_nve = data['E_total'][nve_mask] / EPSILON
            e0_nve = etot_nve[0]
            nve_steps = np.arange(len(etot_nve))
            ax2.plot(nve_steps, (etot_nve - e0_nve) / abs(e0_nve), color='#2ecc71', linewidth=1.5,
                     label=f'Post-equilibration NVE (drift={abs(etot_nve[-1]-e0_nve)/abs(e0_nve)*100:.2f}%)')

    ax2.set_xlabel('NVE Step')
    ax2.set_ylabel(r'$(E_{total} - E_0) / |E_0|$')
    ax2.set_title('NVE Energy Conservation Comparison')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_equilibrated_comparison.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_equilibrated_comparison.png")


def plot_rdf():
    """Plot g(r) radial distribution function."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fpath = f"{OUT_DIR}/gr.csv"
    if not os.path.exists(fpath):
        print("No g(r) data found. Skipping RDF plot.")
        return

    data = np.genfromtxt(fpath, delimiter=',', names=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(data['r_sigma'], data['gr'], '-', color='#2c3e50', linewidth=1.5)
    ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.3, label='g(r) = 1')
    ax.set_xlabel(r'$r / \sigma$', fontsize=14)
    ax.set_ylabel(r'$g(r)$', fontsize=14)
    ax.set_title(r'Radial Distribution Function (Liquid Argon, $T_{\mathrm{init}}$ = 94.4 K)')
    ax.set_xlim(0, 5)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Annotate first peak
    peak_idx = np.argmax(data['gr'])
    ax.annotate(f"Peak: g({data['r_sigma'][peak_idx]:.2f}σ) = {data['gr'][peak_idx]:.2f}",
                xy=(data['r_sigma'][peak_idx], data['gr'][peak_idx]),
                xytext=(2.5, 2.5), fontsize=10,
                arrowprops=dict(arrowstyle='->', color='gray'))

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/lj_rdf.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/lj_rdf.png")


if __name__ == "__main__":
    plot_energy_conservation()
    plot_temperature()
    plot_equilibrated_comparison()
    plot_rdf()
```

### `scripts/plot_scaling.py` (166 lines)

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

Prerequisites:
  out/scaling_strong.csv  (columns: P,N,wall_s,comm_s)
  out/scaling_size.csv    (columns: P,N,wall_s,comm_s)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

OUT_DIR = "out"
PLOT_DIR = "out/plots"


def amdahl(P, f):
    """Amdahl's Law: S(P) = 1 / (f + (1-f)/P)."""
    return 1.0 / (f + (1.0 - f) / P)


def plot_strong_scaling():
    """Plot speedup, efficiency, and compute/comm breakdown."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fpath = f"{OUT_DIR}/scaling_strong.csv"
    if not os.path.exists(fpath):
        print(f"Warning: {fpath} not found. Skipping strong scaling.")
        return

    data = np.genfromtxt(fpath, delimiter=',', names=True)
    P = data['P'].astype(int)
    wall = data['wall_s']
    comm = data['comm_s']
    compute = wall - comm

    t1 = wall[0]
    speedup = t1 / wall
    efficiency = speedup / P

    # Fit Amdahl's Law
    f_fit = None
    try:
        popt, _ = curve_fit(amdahl, P, speedup, p0=[0.01], bounds=(0, 1))
        f_fit = popt[0]
        P_fit = np.linspace(1, max(P) * 1.1, 100)
        S_fit = amdahl(P_fit, f_fit)
    except Exception as e:
        print(f"Warning: Amdahl fit failed: {e}")

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # --- Panel 1: Speedup ---
    ax1 = axes[0]
    ax1.plot(P, speedup, 'o-', color='#2ecc71', linewidth=2, markersize=8, label='Measured')
    ax1.plot(P, P.astype(float), 'k--', alpha=0.5, linewidth=1.5, label='Ideal (S=P)')
    if f_fit is not None:
        ax1.plot(P_fit, S_fit, '-', color='#e74c3c', linewidth=1.5,
                 label=f'Amdahl fit (f={f_fit:.4f})')
    ax1.set_xlabel('Number of Processes P', fontsize=12)
    ax1.set_ylabel('Speedup S(P)', fontsize=12)
    ax1.set_title('Strong Scaling: Speedup', fontsize=13)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # --- Panel 2: Efficiency ---
    ax2 = axes[1]
    ax2.plot(P, efficiency, 'o-', color='#3498db', linewidth=2, markersize=8)
    ax2.axhline(y=1.0, color='k', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Number of Processes P', fontsize=12)
    ax2.set_ylabel('Efficiency E(P) = S(P)/P', fontsize=12)
    ax2.set_title('Strong Scaling: Efficiency', fontsize=13)
    ax2.set_ylim(0, 1.15)
    ax2.grid(True, alpha=0.3)

    # --- Panel 3: Stacked bar — Compute vs Communication ---
    ax3 = axes[2]
    x_pos = np.arange(len(P))
    bar_width = 0.6

    # Clamp negative compute to zero for display
    compute_display = np.maximum(compute, 0)

    ax3.bar(x_pos, compute_display, bar_width, label='Compute', color='#2ecc71', alpha=0.8)
    ax3.bar(x_pos, comm, bar_width, bottom=compute_display, label='Communication', color='#e74c3c', alpha=0.8)

    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([str(p) for p in P])
    ax3.set_xlabel('Number of Processes P', fontsize=12)
    ax3.set_ylabel('Wall Time [s]', fontsize=12)
    ax3.set_title('Compute vs Communication Time', fontsize=13)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/scaling_strong.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/scaling_strong.png")

    if f_fit is not None:
        print(f"  Amdahl serial fraction f = {f_fit:.6f}")
        print(f"  Maximum theoretical speedup = {1.0/f_fit:.1f}x")


def plot_size_scaling():
    """Plot wall time and compute time vs N."""
    os.makedirs(PLOT_DIR, exist_ok=True)

    fpath = f"{OUT_DIR}/scaling_size.csv"
    if not os.path.exists(fpath):
        print(f"Warning: {fpath} not found. Skipping size scaling.")
        return

    data = np.genfromtxt(fpath, delimiter=',', names=True)
    N = data['N']
    wall = data['wall_s']
    comm = data['comm_s']
    compute = wall - comm

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # --- Panel 1: Wall time vs N ---
    ax1.loglog(N, wall, 'o-', color='#2ecc71', linewidth=2, markersize=8, label='Wall time')
    ax1.loglog(N, comm, 's--', color='#e74c3c', linewidth=1.5, markersize=6, label='Comm time', alpha=0.7)

    # N² reference (normalised to largest N)
    N_ref = np.array([min(N), max(N)])
    t_ref = wall[-1] * (N_ref / N[-1]) ** 2
    ax1.loglog(N_ref, t_ref, 'k--', alpha=0.4, linewidth=1.5, label=r'$\sim N^2$ reference')

    ax1.set_xlabel('Number of Particles N', fontsize=12)
    ax1.set_ylabel('Time [s]', fontsize=12)
    ax1.set_title('Size Scaling (P=16)', fontsize=13)
    ax1.legend(fontsize=10)
    ax1.grid(True, which='both', alpha=0.3)

    # --- Panel 2: Communication fraction vs N ---
    comm_frac = comm / wall * 100
    ax2.plot(N, comm_frac, 'o-', color='#e74c3c', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Particles N', fontsize=12)
    ax2.set_ylabel('Communication Fraction [%]', fontsize=12)
    ax2.set_title('Communication Overhead vs Problem Size', fontsize=13)
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=50, color='k', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/scaling_size.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved {PLOT_DIR}/scaling_size.png")


if __name__ == "__main__":
    plot_strong_scaling()
    plot_size_scaling()
```

---

## 7. AI Context Files

### `ai/current_code.md` (165 lines)

# Current Code State — WA2: MPI MD Solver

**Generated:** 2026-03-02 22:35  
**Build:** ✅ Zero warnings (`-Wall -Wextra -pedantic`, `-g -O3 -march=native`)  
**Tests:** ✅ All pass (MIC, LJ force, position wrapping)  
**Total C++ lines:** ~1040

---

## Project Structure

```
md-mpi/
├── .clang-format              # BasedOnStyle: Google, ColumnLimit: 100
├── .gitignore                 # Excludes out/, ai/, *.o, binaries
├── Makefile                   # mpicxx, C++17, -O3 -march=native -g
├── README.md                  # Assessor-first: exact build/run/plot commands
│
├── include/md/
│   ├── constants.hpp          # All physical constants + derived quantities
│   ├── params.hpp             # CLI parser with 16 flags + mode/integrator validation
│   ├── mpi_context.hpp        # Rank/size, decomposition, Allgatherv, posGlobal buffer, comm timing
│   ├── system.hpp             # Flat interleaved pos/vel/acc arrays (no unused force array)
│   ├── rng.hpp                # FCC lattice (with N=4k³ validation) + Box-Muller velocities
│   ├── potentials.hpp         # ForceFunc typedef + HO/LJ declarations
│   ├── integrators.hpp        # Euler/RK4/VV declarations
│   └── observables.hpp        # KE, temperature, g(r) histogram (rescaling done in main.cpp)
│
├── src/
│   ├── main.cpp               # MPI driver: init→bcast→loop→g(r)→output
│   ├── integrators/
│   │   ├── euler.cpp           # AMM Eqn 4.27 (2nd-order position update)
│   │   ├── rk4.cpp             # Classical RK4 (HO verification only)
│   │   └── velocity_verlet.cpp # Half-kick / drift / half-kick
│   └── potentials/
│       ├── harmonic.cpp        # F = -mω²x, non-interacting
│       └── lennard_jones.cpp   # Optimised kernel (no pow, no sqrt)
│
├── tests/
│   ├── test_runner.cpp        # Aggregates all tests, exits non-zero on failure
│   ├── test_mic.cpp           # 9 MIC boundary tests + geometric safety check
│   └── test_force.cpp         # LJ force at r_min, PE check, sign test, wrap test
│
├── scripts/
│   ├── run_scaling.sh         # Batch scaling on cerberus1
│   ├── run_all_data.sh        # Full production data generation (HO + LJ + g(r) + scaling)
│   ├── plot_ho.py             # Phase-space, trajectory, convergence (position error)
│   ├── plot_lj.py             # Energy conservation + g(r)
│   └── plot_scaling.py        # Speedup, efficiency, Amdahl fit
│
└── ai/                        # Context files (excluded from tarball)
    ├── current_code.md        # This file
    ├── claude.md              # Execution checklist
    ├── task_overview.md       # Distilled spec, run matrix
    ├── constraints.md         # Hard constraints, numerical best practices
    ├── code.md                # Code quality standards
    ├── audit.sh               # Generates audit_output.md
    └── audit_output.md        # Latest full audit snapshot
```

## Data Layout

Flat interleaved `std::vector<double>` of size `3*localN`:
```
pos[3*i + 0] = x_i,  pos[3*i + 1] = y_i,  pos[3*i + 2] = z_i
```
`posGlobal` (size `3*N`) permanently allocated on all ranks.

## MPI Communication

| Operation | Function | When |
|-----------|----------|------|
| **Init broadcast** | `MPI_Bcast` (pos + vel) | Once at startup (NOT Scatterv) |
| **Position sync** | `MPI_Allgatherv` | Every step (LJ only, after wrap) |
| **Energy reduce** | `MPI_Reduce(SUM)` | Every step (not in timing mode) |
| **Rescale broadcast** | `MPI_Bcast(lambda)` | At rescale steps (λ computed on root) |
| **FCC error broadcast** | `MPI_Bcast(fccError)` | Once (all ranks participate, clean exit) |
| **g(r) reduce** | `MPI_Reduce(SUM)` | Once after time loop |
| **Timing** | `MPI_Reduce(MAX)` | Wall time + comm time after loop |

## Integrator MPI Sequences

**Euler (AMM 4.27):**
```
drift (x += v*dt + 0.5*a*dt²) → vel update → [wrap] → [Allgatherv] → force
```

**Velocity-Verlet:**
```
half-kick → drift → [wrap] → [Allgatherv] → force → half-kick
```

**RK4 (HO only):**
```
4 stages × (set intermediate state → [wrap] → [Allgatherv] → force)
final combine → [wrap] → [Allgatherv] → force
```

All `[wrap]` and `[Allgatherv]` are guarded with `if (!isHO)`.

## LJ Force Kernel

```
inv_r2 → inv_r6 → inv_r12
V = 4ε(σ¹²·inv_r12 - σ⁶·inv_r6)
f = 24ε·inv_r2·(2σ¹²·inv_r12 - σ⁶·inv_r6)
```
- No `pow`, no `sqrt` in hot loop
- PE accumulated unconditionally for all j≠i, × 0.5 after loop
- MIC: branch-predictor-friendly `if/else if` (not `std::round`)
- Hard cutoff at r_c = 2.25σ (geometric safety: r_c < L/2 ≈ 5.115σ)

## g(r) Pipeline

1. Accumulate pair distances into histogram (bin width = 0.02σ, range [0, L/2])
2. Uses unordered pairs (i < j) from local particles vs all global particles
3. Samples every `--gr-interval` steps after `--gr-discard` equilibration steps
4. `MPI_Reduce(SUM)` across ranks after time loop
5. Normalise: **g(r) = 2 × count / (ρ·N·4πr²·dr·nFrames)** (factor of 2 converts unordered→ordered pairs)
6. Write to `out/gr.csv` (columns: `r_sigma, gr`)

## Output Formats

| Mode | CSV columns | File |
|------|-------------|------|
| HO | `step,time,x,v,E_kin,E_pot,E_total` | `out/ho_{integrator}.csv` |
| LJ | `step,time,E_kin,E_pot,E_total,temperature` | `out/lj_{integrator}.csv` |
| g(r) | `r_sigma,gr` | `out/gr.csv` |

## CLI Parameters

```
--N <int>            Particles (default: 864, must be 4k³ for LJ)
--steps <int>        Timesteps (default: 100)
--dt <double>        Timestep (default: 1e-14 s)
--T <double>         Initial temperature [K] (default: 94.4)
--omega <double>     HO angular frequency (default: 1.0)
--integrator <str>   euler, rk4, verlet (default: verlet) — validated
--mode <str>         ho, lj (default: lj) — validated
--seed <int>         RNG seed (default: 42)
--rescale-step <int> Step for single velocity rescale (default: -1 = disabled)
--rescale-freq <int> Rescale every N steps during equilibration (default: 0 = off)
--rescale-end <int>  Stop continuous rescaling after this step (default: 0)
--timing             Timing mode (reports wall + comm + compute breakdown)
--no-output          Disable CSV output
--gr                 Enable g(r) accumulation (LJ only)
--gr-discard <int>   Equilibration steps before g(r) (default: 500)
--gr-interval <int>  Sample g(r) every N steps (default: 10)
```

Invalid --mode or --integrator values are rejected with a clear error + usage.

## Key Design Decisions

1. **MPI only** — No OpenMP, no threading
2. **Fixed particle partition** — Static at startup, no spatial decomposition
3. **O(N²/P) force** — Each rank computes local-vs-global forces
4. **Cannot exploit Newton's 3rd law** across MPI boundaries (acknowledged limitation)
5. **N_dof = 3(N-1)** after CoM removal for temperature calculation
6. **Position wrapping** skipped for HO (all integrators guarded with `if (!isHO)`)
7. **Velocity rescale uses MPI_Bcast(λ)** — compute on root, broadcast, scale locally
8. **FCC lattice validated** — `4*k*k*k != N` with MPI_Bcast(fccError) + clean MPI_Finalize (no MPI_Abort)
9. **Reproducibility** — single `std::mt19937_64` stream on rank 0, passed to both buildFCCLattice and generateVelocities
10. **CSV precision** — `std::setprecision(15)` for convergence analysis
11. **Comm timing** — `MPI_Wtime()` around `MPI_Allgatherv` when `--timing` is active

---

### `ai/claude.md` (131 lines)

# WA2 MPI MD Solver — Execution Checklist

**Last updated:** 2026-03-02 22:23  
**Status:** Code complete. Production data generated. Ready for plotting and report writing.

---

## Definition of Done

### Core Implementation ✅
- [x] Forward Euler integrator (AMM Eqn 4.27, 2nd-order position)
- [x] Classical RK4 integrator (HO verification only)
- [x] Velocity-Verlet integrator (symplectic, production LJ)
- [x] Harmonic Oscillator potential (F = -mω²x, non-interacting)
- [x] Lennard-Jones potential (optimised kernel, no pow/sqrt)
- [x] FCC lattice construction with N=4k³ validation (clean MPI_Finalize exit)
- [x] Box-Muller velocity generation (single std::mt19937_64 stream)
- [x] Centre-of-mass drift removal
- [x] Continuous thermostat (--rescale-freq / --rescale-end)
- [x] MPI_Bcast for initial state distribution
- [x] MPI_Allgatherv for position synchronisation (LJ only)
- [x] HO mode bypasses all MPI communication
- [x] Position wrapping guarded with `if (!isHO)` in ALL integrators
- [x] g(r) radial distribution function (accumulate + normalise + output)
- [x] Clean timing mode with comm/compute breakdown
- [x] CSV output at 15-digit precision (std::setprecision(15))

### MPI Correctness ✅
- [x] MPI_Reduce for KE and PE to rank 0
- [x] MPI_Bcast for velocity rescale lambda
- [x] MPI_Reduce for g(r) histogram
- [x] MPI_Reduce(MAX) for wall time + comm time
- [x] Parallel consistency: P=1 and P=2 give identical CSV data
- [x] int-typed recvcounts/displs for MPI_Allgatherv
- [x] Remainder-safe particle decomposition
- [x] Clean exit on invalid FCC N (MPI_Bcast error flag, no MPI_Abort)

### Code Quality ✅
- [x] Zero warnings under `-Wall -Wextra -pedantic`
- [x] `<cstdlib>` included for atoi/atof portability
- [x] --mode and --integrator validated (rejects typos)
- [x] Missing arg values give clear error messages
- [x] Doxygen comments on all public functions
- [x] No dead code (removed duplicate rescaleVelocities)
- [x] `-g` debug symbols alongside `-O3`
- [x] `make`, `make test`, `make clean`, `make dist` all work
- [x] Builds and runs on cerberus1 (tested 2026-03-02)

### Production Data Generated ✅
- [x] HO convergence: 24 CSVs (3 integrators × 8 dt values) at 15-digit precision
- [x] LJ Verlet NVE: N=864, 100 steps (raw FCC melting)
- [x] LJ Euler NVE: N=864, 100 steps (non-symplectic drift)
- [x] LJ Verlet equilibrated: N=864, 200 steps (rescale to step 100, NVE after)
- [x] g(r): N=864, 5000 steps, 451 frames, 255 bins (cerberus1)
- [x] Strong scaling: N=2048, P=1..32, median-of-5 reps (cerberus1)
- [x] Size scaling: P=16, N=108..2048, median-of-5 reps (cerberus1)

---

## Key Production Results

### HO Convergence (verified 15-digit precision)
- Euler: ratio ~2.0 when halving dt → confirmed O(Δt)
- Verlet: ratio ~4.0 down to error 5.7e-8 → confirmed O(Δt²)
- RK4: ratio ~15 down to error 3.6e-15 (machine eps) → confirmed O(Δt⁴)

### LJ Energy Conservation
- Raw NVE (no rescale): T=94.4→48.4K, E drift=0.77%
  (NOT physics — NVE conserves E regardless of phase transitions.
   Drift is from hard cutoff discontinuity at r_c=2.25σ. Particles
   crossing the cutoff boundary cause force jumps that break symplecticity.
   A shifted potential V(r)-V(r_c) would eliminate this.)
- Equilibrated NVE (rescale to step 100): T=94.1→94.6K, E drift=0.06%
  (Lower drift because equilibrated liquid has fewer particles crossing r_c per step)
- Euler NVE: E drift=6.4% (expected non-symplectic)

### g(r) Physical Validation
- First peak: r=1.09σ, g=2.82 (textbook liquid Ar)
- Hard core: g(r<0.9σ) ≈ 0
- Asymptote: g(r>3σ) = 1.003 → normalisation correct

### Strong Scaling (N=2048, cerberus1)
- P=1: 7.87s, P=32: 0.40s → speedup 19.8×
- Timing uses MPI_Allreduce(MAXLOC) to report slowest rank's breakdown
- Amdahl serial fraction: f ≈ 1.8% (use curve_fit in report)
- *Note:* Pure Amdahl's Law assumes constant serial fraction, but MPI_Allgatherv adds O(N log P) communication overhead. The fit over-predicts theoretical max speedup (57x). State this limitation in report.

---

## Report Checklist

### Methodology (20%)
- [ ] Describe all three integrators with equations
- [ ] State Euler = AMM Eqn 4.27 (2nd-order position, 1st-order velocity)
- [ ] Explain VV is symplectic and time-reversible
- [ ] Note RK4 requires 4 force evals/step → impractical for parallel LJ
- [ ] Describe MPI strategy: replicated data, fixed partition, O(N²/P)
- [ ] Acknowledge N3L limitation (cannot exploit across MPI boundaries)
- [ ] Discuss optimised LJ kernel: no pow/sqrt, precomputed constants
- [ ] MIC geometric safety proof: r_c = 2.25σ < L/2 = 5.11σ
- [ ] State g(r) normalisation convention (factor of 2, unordered pairs)
- [ ] Note hard cutoff (no potential shift) — consistent with Rahman

### Results 1 — HO (15%)
- [ ] x(t), v(t) trajectories for all 3 integrators with exact overlay
- [ ] Phase-space (v vs x) diagrams
- [ ] Log-log convergence plot with fitted slopes
- [ ] Energy conservation comparison (Euler drifts, VV bounded, RK4 exact)

### Results 2 — LJ (15%)
- [ ] Energy conservation: VV vs Euler for N=864
- [ ] Temperature evolution (show FCC melting T drop = KE↔PE exchange, NOT E_total change)
- [ ] Equilibrated NVE vs raw NVE comparison (0.06% vs 0.77%)
- [ ] Attribute 0.77% drift to hard cutoff discontinuity at r_c (NOT to phase transition)
- [ ] Note: shifted potential V(r)-V(r_c) would eliminate drift (acknowledge as known limitation)
- [ ] g(r) profile (compare with Rahman 1964)
- [ ] Explicitly discuss the ~0.1σ shift in the g(r) first peak compared to Rahman. Rahman's state is at 94.4 K, while this trajectory (post-melting) has an effective temperature of ~50 K, leading to a denser first coordination shell.
- [ ] State N_dof = 3(N-1) and explain why (CoM conservation removes 3 DoF)

### Results 3 — Scaling (10%)
- [ ] Strong scaling: speedup S(P) with Amdahl fit (curve_fit)
- [ ] Efficiency E(P) = S(P)/P
- [ ] Stacked bar chart: compute vs comm time for each P
- [ ] Note P=4 super-linear scaling (cache effect)
- [ ] Size scaling: compute/N² consistency for N≥864
- [ ] Discuss small-N communication dominance (N≤500 at P=16)

### Quality (20%)
- [ ] Clean code, modular design, no dead code
- [ ] README, Makefile, unit tests
- [ ] Reproducible (fixed seed, deterministic)

---

### `ai/task_overview.md` (162 lines)

# Task Overview — WA2: MPI Parallelisation of MD

## Integrator Summary

| Integrator | Global Order | Symplectic | Force Evals/Step | Use For |
|:-----------|:-------------|:-----------|:-----------------|:--------|
| Forward Euler (AMM Eqn 4.27) | 1 | No | 1 | HO + LJ |
| RK4 | 4 | No | 4 | HO ONLY |
| Velocity-Verlet | 2 | Yes | 1 (+ recompute) | HO + LJ production |

## Integrator Equations

### Forward Euler (AMM Handout Eqn 4.27 — 2nd-order Taylor position, 1st-order velocity)
```
x_{n+1} = x_n + v_n * dt + 0.5 * a_n * dt^2
v_{n+1} = v_n + a_n * dt
```

Order 1 globally (velocity bottleneck). Not symplectic. Energy drifts.
NOTE: This is the course's Euler formulation, not a pure 1st-order scheme. Cite AMM Handout §4.3.1.

### RK4 (as 2-vector first-order system)

State vector:
    y = (x, v)^T

Derivative:
    f(y) = (v, a(x))^T

Stages:
```
k1 = dt * f(y_n)
k2 = dt * f(y_n + k1 / 2)
k3 = dt * f(y_n + k2 / 2)
k4 = dt * f(y_n + k3)

y_{n+1} = y_n + (k1 + 2*k2 + 2*k3 + k4) / 6
```

Order 4 globally. Not symplectic. 4 force evaluations per step.

### Velocity-Verlet (half-kick / drift / wrap / Allgatherv / force / half-kick)

Full MPI-aware sequence (v4 lock-in):
```
Step 1 (half-kick):  v_{n+1/2} = v_n + 0.5 * a_n * dt
Step 2 (drift):      x_{n+1}   = x_n + v_{n+1/2} * dt
Step 3 (wrap):       Wrap x_{n+1} into [0, L)
Step 4 (gather):     MPI_Allgatherv to sync global positions
Step 5 (force eval): Compute a_{n+1} from global positions
Step 6 (half-kick):  v_{n+1}   = v_{n+1/2} + 0.5 * a_{n+1} * dt
```

### AMM Euler (MPI-aware sequence, v4 lock-in)
```
Step 1 (drift):      x_{n+1} = x_n + v_n * dt + 0.5 * a_n * dt^2
Step 2 (vel update): v_{n+1} = v_n + a_n * dt
Step 3 (wrap):       Wrap x_{n+1} into [0, L)
Step 4 (gather):     MPI_Allgatherv
Step 5 (force eval): Compute a_{n+1} for next timestep
```

Order 2 globally (Verlet) / Order 1 globally (Euler). Verlet is symplectic and time-reversible.

## LJ State Point (Canonical Constants)
```
N = 864 (= 4 * 6^3)
L = 10.229 sigma
r_max = 2.25 sigma
eps/k_B = 120 K
sigma = 3.4 Angstrom
m = 66.904265e-27 kg
T = 94.4 K
dt = 1e-14 s
T_sim = 1e-12 s (100 steps)
```

## Density Scaling for N != 864
```
L(N) = 10.229 * sigma * (N / 864)^(1/3)
```

## Valid FCC Particle Counts (N = 4k^3)
```
k=3: N = 108
k=4: N = 256
k=5: N = 500
k=6: N = 864
k=7: N = 1372
k=8: N = 2048
```

## g(r) Normalisation (unordered pairs, i < j)
```
g(r) = 2 / (rho * N) * <n(r, r+dr)> / (4 * pi * r^2 * dr)
```
Factor of 2 converts from unordered pair count to the standard g(r) convention.

Or equivalently with ordered pairs:
```
g(r) = (V / (N * (N-1))) * <n_ordered(r, r+dr)> / (4 * pi * r^2 * dr)
```

Be explicit about pair-counting convention in the report.

## Extended g(r) Protocol (v4 Lock-in)
```
Total steps: 5000
Discard first: 500 (equilibration)
Sample every: 10 steps (yields 450 frames)
Pair counting: i < j only (unordered)
Bin range: [0, L/2]  (NOT r_c)
Bin width: Δr = 0.02 sigma
Final reduction: MPI_Reduce(MPI_SUM) to rank 0
```

## Temperature Measurement
```
T = (2 / (N_dof * k_B)) * E_kin
```
where N_dof = 3(N-1) after CoM drift removal (or 3N — state choice clearly).

## Temperature Rescaling Policy (v5)
```
Single rescale: --rescale-step k (rescale at step k only)
Continuous: --rescale-freq F --rescale-end E (rescale every F steps until step E)
Production NVE: NO rescaling after equilibration
```
Used --rescale-freq 10 --rescale-end 500 for g(r) production run.

## Convergence Error Definition
```
e(dt) = |x_num(T_final) - x_exact(T_final)|
```

Plot log(e) vs log(dt). Fit slope to get observed order p.

## Run Matrix

| Config | Parameters | Outputs | Plots |
|:-------|:-----------|:--------|:------|
| HO_Sweep | N=1, dt sweep, 3 integrators, no Allgatherv | t, x, v, E | Phase-space, log-log convergence |
| LJ_100 (PRIMARY) | N=864, 100 steps, Euler+Verlet, NVE | t, Ekin, Epot, Etot | Energy conservation |
| LJ_EQUIL | N=864, 200 steps, rescale-freq=10, rescale-end=100, NVE 101-200 | t, Ekin, Epot, Etot | Raw vs equilibrated NVE comparison |
| LJ_RDF | N=864, 5000 steps, Verlet, 500 discard, sample/10 | r, g(r) | g(r) vs r/sigma |
| Scale_P | N=2048, P=1..32, median-of-5 | P, wall, comm | Speedup + Amdahl fit, Efficiency, Comm breakdown |
| Scale_N | P=16, N=108..2048, median-of-5 | N, wall, comm | Time vs N, Compute/N² consistency |
| Par_Valid | N=108, P=1,2 | CSV data lines | diff confirms bitwise-identical physics |

## Key Report Reminders
- The brief mandates 100 steps for LJ. This is your primary Results 2.
- No velocity rescaling during the 100-step production run.
- Extended g(r) run is supplementary only. Must be explicitly labelled.
- Rahman used a predictor-corrector; we compare physical results, not methods.
- RK4 is impractical for parallel LJ (4 Allgatherv per step). HO only.
- HO mode bypasses Allgatherv entirely — highlight this optimisation.
- Euler formulation is AMM Eqn 4.27 (2nd-order Taylor position). Cite explicitly.
- Amdahl's Law breaks down at high P due to Allgatherv communication overhead.
- Contrast fixed particle partitioning vs spatial domain decomposition explicitly.
- MIC is guaranteed safe because r_c = 2.25σ < L/2 ≈ 5.115σ.
- Use std::mt19937_64, not rand().
- FCC perturbation must have zero mean.

---

### `ai/constraints.md` (133 lines)

# Constraints & Best Practices — WA2

## Hard Assignment Constraints

1. **MPI ONLY.** OpenMP, `<thread>`, or any threading library is strictly forbidden.
2. **Fixed particle partitioning.** No spatial domain decomposition.
   Index ranges fixed at startup.
3. **Word count:** 3,000-5,000 words (including captions and references).
   - No penalty up to 5,250.
   - 10pp deduction for 5,251-5,500.
   - 20pp deduction for 5,501-6,000.
4. **Anonymity:** Blind Candidate Number only. No names, no CRSid.
5. **Testing:** Avoid third-party libraries. No gtest, no Boost.Test. Homebrew runner.
6. **RK4 scope:** Verify on HO only. Do NOT run RK4 for LJ MPI production.
7. **Rahman comparison:** Compare simulation results (energy, g(r)), NOT his method.
8. **Cutoff:** Hard cutoff at 2.25 sigma. No shifted-force/shifted-potential unless labelled extra.
9. **No `-Ofast`.** Use `-O3 -march=native`. Preserve IEEE754 associativity.
10. **LJ run length:** The brief mandates T_sim = 1e-12 s (100 steps). This is primary.
    Extended runs for g(r) are supplementary extensions only.
11. **RNG:** Use `std::mt19937_64` with fixed seed. Do NOT use `rand()` or `std::rand()`.
12. **MPI_Bcast for init:** Use `MPI_Bcast`, NOT `MPI_Scatterv`, for initial state distribution.
    Every rank needs the complete global state for the first force evaluation.
13. **MPI array types:** `recvcounts` and `displs` for `MPI_Allgatherv` must be `int` arrays.
    Passing `size_t` or `double` causes undefined behaviour.
14. **Data layout:** Flat interleaved `std::vector<double>` arrays, `pos[3*i + d]`.
    `pos_global` of size 3N permanently allocated on all ranks. (v4)
15. **Temperature rescaling:** Supports single rescale (`--rescale-step`) and continuous thermostat (`--rescale-freq` + `--rescale-end`). No rescaling during NVE production phase. (v5)
16. **HO bypass:** Skip `MPI_Allgatherv` entirely in HO mode. (v4)
17. **FCC perturbation:** Must have zero mean (symmetric distribution). (v4)

## Numerical Best Practices

### Force Kernel (no pow, no sqrt, no branching for PE)

```cpp
double r2 = dx*dx + dy*dy + dz*dz;

if (r2 >= rcut2) continue;

double inv_r2  = 1.0 / r2;
double inv_r6  = inv_r2 * inv_r2 * inv_r2;
double inv_r12 = inv_r6 * inv_r6;

double V_pair   = four_eps * (sigma12 * inv_r12 - sigma6 * inv_r6);
double f_scalar = twentyfour_eps * inv_r2
                * (2.0 * sigma12 * inv_r12 - sigma6 * inv_r6);

force[3*li + 0] += f_scalar * dx;
force[3*li + 1] += f_scalar * dy;
force[3*li + 2] += f_scalar * dz;

// Accumulate PE unconditionally — multiply by 0.5 AFTER the loop
local_pe += V_pair;
```

### Minimum Image Convention (branch-predictor optimised)

```cpp
double half_L = 0.5 * L;

if (dx >  half_L) dx -= L;
else if (dx < -half_L) dx += L;

if (dy >  half_L) dy -= L;
else if (dy < -half_L) dy += L;

if (dz >  half_L) dz -= L;
else if (dz < -half_L) dz += L;
```

**Assumption (v4 corrected):** The single-image MIC is guaranteed safe because the hard cutoff r_c = 2.25σ is strictly less than L/2 ≈ 5.115σ. Interacting particles will never trigger a multiple-box-length wrap. Document this geometric argument in the report.

### Position Wrapping (every step, after drift)

```cpp
for (int d = 0; d < 3; ++d) {
    pos[3*i + d] -= L * std::floor(pos[3*i + d] / L);
}
```

Prevents unbounded coordinate growth and floating-point precision loss.

### Energy Accounting

- **Forces:** Each local i loops all j != i (global positions from Allgatherv).
- **Potential Energy:** Accumulate V for ALL j != i unconditionally. Multiply local sum by 0.5 after the loop. Then `MPI_Reduce(MPI_SUM)` to rank 0.
- **Kinetic Energy:** Each rank sums 0.5 * m * |v|^2 for its local particles. Then `MPI_Reduce(MPI_SUM)` to rank 0.
- **Temperature:** T = (2 / (N_dof * k_B)) * E_kin_total, where N_dof = 3(N-1) or 3N (state choice clearly).

### Timing Protocol

```cpp
MPI_Barrier(MPI_COMM_WORLD);
double start = MPI_Wtime();

// ... computation loop (NO I/O) ...

double end = MPI_Wtime();
double elapsed = end - start;
double max_time;
MPI_Reduce(&elapsed, &max_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
```

### Floating-Point Non-Associativity

Different numbers of MPI ranks change the reduction tree structure, producing O(1e-14) to O(1e-12) differences in summed quantities. This is expected and must be documented. Validate via conserved quantities and statistical agreement, NOT bitwise equality. Initial conditions should be bitwise identical across P (because rank 0 generates and broadcasts). Trajectories should match up to round-off; energy curves should be statistically/visually indistinguishable.

### Parallel Initialisation

Rank 0 generates ALL random numbers and initial conditions using `std::mt19937_64` with a fixed seed. Distributes via **`MPI_Bcast`** (not `MPI_Scatterv`). This ensures bitwise-identical initial states AND every rank has the full global state for the first force evaluation.

## Amdahl's Law

```
S(P) = 1 / (f + (1 - f) / P)
```

Fit f from measured S(P). For this code:

- Serial fraction: initialisation (rank 0 RNG), I/O (rank 0 output), serial reductions.
- Parallel fraction: force computation O(N^2 / P), Allgatherv O(N).
- **Critical:** Amdahl's Law assumes constant f and negligible communication overhead. In practice, the O(N) Allgatherv cost grows with P, so the effective serial fraction is not constant. At high P, communication dominates computation, causing the measured speedup to fall below the Amdahl prediction. Discuss this deviation in the report.
- **v4 Refinement:** Explicitly contrast fixed particle partitioning (all-to-all communication, O(N) per collective) with spatial domain decomposition (halo exchange, O(N/P) per rank, scaling with subdomain surface area). This contrast is the "advanced real-world approaches" rubric point.

## Real-World Context (for Conclusions)

Production MD codes (LAMMPS, GROMACS) use:

- **Spatial decomposition coupled with halo/ghost cell exchange** for O(N/P) strong scaling
- Verlet neighbour lists for O(N) force evaluation
- Short-range cutoffs + Ewald summation for long-range electrostatics

Our O(N^2) all-pairs approach with fixed particle partitioning is pedagogically valuable but impractical at production scale. The communication pattern (global `MPI_Allgatherv`) contrasts sharply with production codes that only communicate with adjacent spatial domains. This must be discussed in the Conclusions section.

---

### `ai/code.md` (305 lines)

# Code Quality & Submission Standards — WA2

Source: Philip Blakely, "Code development and submission in the MPhil for
Scientific Computing." These are the standards the assessor (Blakely himself)
will use when evaluating the 20% Quality mark.

## The Golden Rule

"The assessors should be able to rerun any simulations and generate any results
presented in your dissertation."

Everything below serves this single principle.

---

## 1. README.md — The Assessor's Entry Point

The README is the first thing the assessor reads. It must contain:

```
# WA2: MPI Parallelisation of MD — Candidate BCN

## Dependencies
- C++17 compiler with MPI (tested with OpenMPI 4.x + GCC 8+)
- Python 3 with matplotlib, numpy (for plotting scripts)

## Build
make            # builds md_solver
make test       # runs unit tests (exits non-zero on failure)

## Run Examples

### Harmonic Oscillator (Results 1)
mpirun -np 1 ./md_solver --mode ho --integrator verlet --dt 0.01 --steps 1000

### Lennard-Jones Argon (Results 2)
mpirun -np 1 ./md_solver --mode lj --integrator verlet --N 864 --steps 100

### Lennard-Jones with Equilibration Pre-phase
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --steps 100 --rescale-step 10

### Scaling (Results 3)
mpirun -np 16 ./md_solver --mode lj --integrator verlet --N 2048 --steps 100 --no-output

## Generate Plots
python3 scripts/plot_ho.py
python3 scripts/plot_lj.py
python3 scripts/plot_scaling.py

## Clean / Package
make clean      # removes objects and binaries
make dist       # creates submission tarball
```

Key requirements from Blakely:
- "Instructions for compiling and running your code should be clear and complete."
- "You may assume they are using Linux."
- "You may assume sensible/default locations for libraries in a Makefile, but
  should label them appropriately therein."

---

## 2. No Magic Numbers

Every literal constant must be traceable. For this project, centralise all physical constants:

```cpp
// include/md/constants.hpp

#ifndef MD_CONSTANTS_HPP
#define MD_CONSTANTS_HPP

namespace md {
namespace constants {

    /// Boltzmann constant [J/K]
    constexpr double kB = 1.380649e-23;

    /// Lennard-Jones well depth / kB [K]
    constexpr double eps_over_kB = 120.0;

    /// Lennard-Jones length scale [m]
    constexpr double sigma = 3.4e-10;

    /// Argon atomic mass [kg]
    constexpr double mass = 66.904265e-27;

    /// Interaction cutoff [sigma units]
    constexpr double rcut_sigma = 2.25;

}  // namespace constants
}  // namespace md

#endif
```

All runtime parameters (N, dt, steps, integrator choice, output flags, rescale-step) must come from a settings file or CLI arguments — NEVER hard-coded.

---

## 3. Settings File / CLI Arguments

Blakely explicitly requires runtime-configurable parameters. For this project, a simple CLI parser in `params.hpp` is sufficient:

```cpp
struct Params {
    int N = 864;
    int steps = 100;
    double dt = 1e-14;
    double T_init = 94.4;
    std::string integrator = "verlet";  // "euler", "rk4", "verlet"
    std::string mode = "lj";            // "ho", "lj"
    bool output = true;
    int seed = 42;
    int rescale_step = -1;              // v4: default disabled (-1 = no additional rescale)
};
```

Parse from `argv` with a straightforward loop. Include representative config examples in `scripts/` or document exact commands in README.

---

## 4. Commenting & Documentation

### Doxygen Block Comments

Every public function and class must have a Doxygen comment:

```cpp
/**
 * @brief Compute LJ forces for local particles against all particles.
 *
 * Uses the optimised kernel with shared intermediates (no pow, no sqrt).
 * Applies minimum image convention and hard cutoff at rcut.
 * Accumulates potential energy unconditionally for all j != i;
 * caller must multiply by 0.5 to correct for double-counting.
 *
 * @param[in]  pos_global  Global positions (3N doubles, from Allgatherv)
 * @param[out] forces      Local forces (3*local_N doubles, interleaved)
 * @param[out] local_pe    Local contribution to potential energy (pre-halving)
 * @param[in]  offset      Starting global index for this rank
 * @param[in]  local_N     Number of particles owned by this rank
 * @param[in]  N           Total number of particles
 * @param[in]  L           Box side length
 * @param[in]  rcut2       Squared cutoff distance
 */
void compute_lj_forces(
    const std::vector<double>& pos_global,
    std::vector<double>& forces,
    double& local_pe,
    int offset, int local_N, int N,
    double L, double rcut2
);
```

### Inline Comments

Comment the *why*, not the *what*:

```cpp
// Skip self-interaction to avoid r^2 = 0 singularity
if (i == j) continue;

// Branch-predictor-friendly MIC (avoids std::round overhead in O(N^2) loop)
if (dx > half_L) dx -= L;
else if (dx < -half_L) dx += L;

// Wrap positions to [0, L) to prevent unbounded coordinate growth
pos[3*i + d] -= L * std::floor(pos[3*i + d] / L);
```

---

## 5. Naming Convention

Pick one convention and apply it consistently everywhere:

```
Variables:           camelCase        (localN, halfL, invR2)
Constants:           UPPER_SNAKE      (BOLTZMANN_K) or constexpr in namespace
Class names:         PascalCase       (MPIContext, VelocityVerlet)
Class member data:   m_prefix         (m_rank, m_size, m_localN)
Functions:           camelCase        (computeForces(), integrateStep())
Macros:              UPPER_SNAKE      (avoided where possible; use constexpr)
```

---

## 6. Modularisation

```
constants.hpp  — Physical constants (never duplicated)
params.hpp     — Runtime parameters (parsed once, includes --rescale-step)
rng.hpp        — FCC lattice (zero-mean perturbation) + Box-Muller using std::mt19937_64 (called once at init)
system.hpp     — State vectors: pos, vel, acc (flat interleaved std::vector<double>)
potentials.hpp — HO and LJ force/energy kernels (hot loop)
                 HO: compute_forces ignores global state, F = -kx locally
                 LJ: compute_forces uses pos_global from Allgatherv
integrators.hpp — Euler, RK4, Verlet step functions (including position wrapping + Allgatherv sequencing)
observables.hpp — E_kin, E_pot, temperature, g(r) binning
mpi_context.hpp — Rank/size, decomposition, Allgatherv helper (int arrays), pos_global allocation
main.cpp       — MPI_Init, parse params, time loop, MPI_Finalize
```

If you find yourself writing the same MIC code in both the force kernel and the g(r) binning, factor it into a shared inline function.

---

## 7. Submission Tarball

### What to Include

```
include/     — All .hpp headers
src/         — All .cpp source files
tests/       — Unit test source files
scripts/     — Python plotting scripts, bash run scripts
Makefile     — With targets: all, clean, dist, test
README.md    — Assessor-first instructions
```

### What to EXCLUDE

```
out/         — Generated data files
ai/          — AI context workspace
*.o          — Object files
md_solver    — Compiled binary
*.pdf        — Generated plots / report PDF
.git/        — Entire git history
```

### The `make dist` Target

```makefile
TARBALL = candidate_BCN_wa2.tar.gz

dist: clean
    tar -czvf $(TARBALL) \
        include/ src/ tests/ scripts/ \
        Makefile README.md
    @echo "Created $(TARBALL)"
    @echo "Contents:"
    @tar -tzvf $(TARBALL) | head -30
```

Size should be order of MB, not GB. If >5 MB, data files or binaries have leaked in.

---

## 8. Testing Discipline

- `make test` compiles and runs `tests/test_runner.cpp`.
- Exit code 0 = all pass. Non-zero = failure.
- Run `make test` after every significant change.
- Mandatory tests:
    1. MIC wrapping correctness
    2. LJ force magnitude < 1e-12 at r = 2^(1/6)*sigma
    3. Position wrapping to [0, L)

Optional additional tests (good for Quality marks):
- Energy conservation check: Verlet on HO for 1000 steps, |E_final - E_initial| < tolerance
- Parallel consistency: P=1 vs P=2 total energy agrees to ~1e-12 relative

---

## 9. Libraries and Dependencies

- **MPI** — required, assumed installed.
- **Standard C++ library** — `<vector>`, `<cmath>`, `<random>`, `<fstream>`, etc.
- **Python (matplotlib, numpy)** — for plotting scripts only.
- **No other dependencies.** No Boost, no Eigen, no gtest.

---

## 10. Anti-Plagiarism Compliance

- Submit anti-plagiarism declaration form separately.
- All code must be your own or properly referenced.
- AI-generated content is permitted (explicitly stated in brief).
- TurnItIn for report, MOSS for code similarity.

---

## Summary Checklist (Pre-Submission)

```
[ ] `make` compiles without warnings (-Wall -Wextra -pedantic)
[ ] `make test` passes (exit code 0)
[ ] `make dist` produces a clean tarball < 5 MB
[ ] Tarball contains NO: .o, binaries, .git/, out/, ai/, PDFs
[ ] README has exact build/run/plot commands
[ ] All constants in constants.hpp (no magic numbers in code)
[ ] All parameters from CLI / settings (no recompilation needed)
[ ] --rescale-step parameter implemented
[ ] Every public function has a Doxygen comment
[ ] Consistent naming convention throughout
[ ] Representative configs/scripts for reproducing all figures
[ ] Blind Candidate Number only — no names anywhere
[ ] Uses std::mt19937_64, not rand()
[ ] MPI arrays (recvcounts, displs) are int type
[ ] Data layout: flat interleaved std::vector<double>
[ ] pos_global permanently allocated on all ranks
[ ] HO mode bypasses Allgatherv
```

---

## 8. File Sizes

```
include/md/constants.hpp                             89 lines
include/md/integrators.hpp                          103 lines
include/md/mpi_context.hpp                          107 lines
include/md/observables.hpp                          146 lines
include/md/params.hpp                               201 lines
include/md/potentials.hpp                            64 lines
include/md/rng.hpp                                  152 lines
include/md/system.hpp                                69 lines
src/integrators/euler.cpp                            50 lines
src/integrators/rk4.cpp                             106 lines
src/integrators/velocity_verlet.cpp                  58 lines
src/main.cpp                                        357 lines
src/potentials/harmonic.cpp                          35 lines
src/potentials/lennard_jones.cpp                    112 lines
tests/test_force.cpp                                198 lines
tests/test_mic.cpp                                  130 lines
tests/test_runner.cpp                                33 lines

Total C++ lines:
    1079
```

**End of audit.**
