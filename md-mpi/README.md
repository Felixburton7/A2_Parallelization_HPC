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
