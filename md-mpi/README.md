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
# Primary run: 500-step equilibration (velocity rescaling each step) + 100-step NVE production.
# Production runs use P=4; see scripts/run_all_data.sh for the P=1 vs P=2 consistency check.
mkdir -p out
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --steps 600 --rescale-step 500

# Primary run: 500-step equilibration + 100-step Euler production
mpirun -np 4 ./md_solver --mode lj --integrator euler --N 864 --steps 600 --rescale-step 500

# Equilibrated comparison run (rescale at 100, then post-rescale NVE segment)
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --steps 200 --rescale-step 100

# Supplementary g(r) (extended run, ~450 frames for smooth Rahman comparison)
# --gr-discard is relative to production_start; with --rescale-step 500, discard=0 starts sampling at step 500.
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --steps 25500 --rescale-step 500 --gr --gr-discard 0 --gr-interval 10
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
