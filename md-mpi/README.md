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
