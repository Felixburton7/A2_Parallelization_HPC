# WA2: MPI Parallelisation of Molecular Dynamics

This repository contains my C++17/MPI molecular dynamics code for Written Assignment 2, together with the tests, plotting scripts, and submission packaging.

## Repository Layout

- `include/`, `src/`: solver source code
- `tests/`: unit tests
- `scripts/`: data generation, plotting, and validation scripts
- `out/`: generated run data and figures

## Requirements

You will need:

- `mpicxx`
- `mpirun` or `mpiexec`
- a C++17 compiler
- Python 3 with `numpy` and `matplotlib`

## Build And Test

From the repository root, run:

```bash
make clean
make
make test
```

This builds the main solver `md_solver` and the test executable `test_runner`.

## Generate Results

To regenerate the data and figures used in the report, run:

```bash
bash scripts/run_results.sh
```

This writes the output files under `out/`.

By default, the Results 3 scaling plots use the reference tables in `scripts/data/reference_scaling/`.
If you want to measure scaling on the current machine instead, run:

```bash
bash scripts/run_results.sh --live-scaling
```

For a quicker check without the scaling part, run:

```bash
bash scripts/run_results.sh --skip-scaling
```

## Output Files

After a full run, the main things to check are:

- `out/plots/results1_figure*.png`
- `out/plots/results2_figure*.png`
- `out/plots/results3_figure*.png`
- `out/scaling_strong.csv`
- `out/scaling_size.csv`
- `out/runs/`

## Notes For The Report

- The required Lennard-Jones production run is `100` steps / `1 ps`.
- The RDF figure uses a separate long Verlet run with `20000` production steps.
- The default scaling data use `500` strong-scaling steps and `2000` size-scaling steps.
- Each scaling point is based on `11` repetitions.

## Submission

To create the submission tarball, run:

```bash
make dist BCN=4316J
```

The tarball contains the source files, tests, scripts, `Makefile`, `README.md`, and `.clang-format`.
It does not include `out/`, compiled binaries, or Python cache files.
