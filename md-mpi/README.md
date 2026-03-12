# WA2: MPI Parallelisation of Molecular Dynamics

This repository contains the C++17/MPI molecular dynamics solver, tests, data-generation scripts, plotting scripts, and submission packaging used for Written Assignment 2.

## Final Run Quick Path

If you want the shortest submission-rehearsal sequence from a clean checkout, run:

```bash
make clean
make
make test
bash scripts/run_results.sh
bash ai/generate_all_context.sh
make dist BCN=<your_candidate_number>
```

Use the rest of this README for checks, file locations, and what each step is expected to produce.

## Repository Layout

- `include/`, `src/`: solver implementation
- `tests/`: unit tests
- `scripts/`: data-generation, plotting, and validation scripts
- `ai/`: generated context files for report-writing and audit support
- `out/`: generated run data, plots, summaries, and metadata

## Dependencies

Required:

- `mpicxx` and `mpirun` / `mpiexec`
- C++17-capable compiler
- Python 3
- Python packages: `numpy`, `matplotlib`

Helpful checks:

```bash
mpicxx --version
mpirun --version
python3 - <<'PY'
import numpy, matplotlib
print("numpy:", numpy.__version__)
print("matplotlib:", matplotlib.__version__)
PY
```

## Build And Test

Run from the repository root:

```bash
make clean
make
make test
```

This builds:

- `md_solver`
- `test_runner`

## Quick Smoke Runs

Harmonic oscillator:

```bash
mpirun -np 1 ./md_solver --mode ho --integrator verlet --dt 0.01 --steps 1000 --N 1
```

Lennard-Jones Argon required-run style setup:

```bash
mpirun -np 4 ./md_solver --mode lj --integrator verlet --N 864 --dt 1e-14 \
  --target-temperature 94.4 --equilibration-steps 50 --production-steps 100 \
  --final-rescale-before-production
```

Timing-only scaling-style command:

```bash
mpirun -np 16 ./md_solver --mode lj --integrator verlet --N 864 --steps 2000 --timing
```

## End-To-End Report Workflow

### 1. Generate Data And Plots

```bash
bash scripts/run_results.sh
```

This runs:

- production data generation via `scripts/run_all_data.sh`
- canonical plot generation via:
  - `scripts/plot_ho.py`
  - `scripts/plot_lj.py`
  - `scripts/plot_scaling.py`

Important current scaling configuration:

- strong scaling: `N = 2048`, `500` timed steps, `20` repetitions per process count
- size scaling: `P = 16`, `2000` timed steps, `20` repetitions per particle count

These values come from `scripts/run_all_data.sh`. They are not encoded directly in the scaling CSV headers, so keep them consistent with the report text.

### 2. Validate Generated Outputs

`scripts/run_all_data.sh` already runs manifest validation, but you can rerun it explicitly:

```bash
python3 scripts/validate_manifest.py
```

Useful files to check after a full run:

- `out/manifest.json`
- `out/plots/results1_figure*.png`
- `out/plots/results2_figure*.png`
- `out/plots/results3_figure*.png`
- `out/summary/results1/*`
- `out/summary/results2/*`
- `out/scaling_strong.csv`
- `out/scaling_size.csv`

### 3. Generate AI Context Files

```bash
bash ai/generate_all_context.sh
```

This produces:

- `ai/audit_output.md`
- `ai/results.md`
- `ai/results_bundle.md`
- `ai/context_bundle.tar.gz`

Use these for report drafting, audit tracing, and external LLM context. They are not part of the final submission tarball.

## Remote-Server Final Run

If you want to rehearse the final submission workflow on a remote machine, use a clean copy of the repository and follow this order:

1. Check the toolchain.
   - `mpicxx --version`
   - `mpirun --version`
   - Python import check for `numpy` and `matplotlib`
2. Build and run tests.
   - `make clean`
   - `make`
   - `make test`
3. Generate the full report dataset and plots.
   - `bash scripts/run_results.sh`
4. Generate the context bundle used for drafting and checking.
   - `bash ai/generate_all_context.sh`
5. Inspect the key outputs listed above.
6. Create the submission tarball.
   - `make dist BCN=<your_candidate_number>`

If you only want a faster debug run before the full timing study, you can skip scaling:

```bash
bash scripts/run_results.sh --skip-scaling
python3 scripts/validate_manifest.py --skip-scaling
```

Do not use the `--skip-scaling` path for the final reported scaling results.

## Submission Packaging

Create the tarball with:

```bash
make dist BCN=<your_candidate_number>
```

The tarball includes:

- `include/`
- `src/`
- `tests/`
- `scripts/`
- `Makefile`
- `README.md`
- `FINAL_SUBMISSION.md`
- `.clang-format`

The tarball excludes generated artifacts such as:

- `ai/`
- `out/`
- binaries
- Python caches

The output tarball name is:

```text
<BCN>_wa2.tar.gz
```

## Notes For The Report

- The required Lennard-Jones production run is the `100`-step / `1 ps` run.
- The RDF figure comes from a separate long Verlet run (`20000` production steps), not from the required 100-step run.
- The current scaling dataset is based on `500` strong-scaling steps and `2000` size-scaling steps, not `100` steps.
- The Rahman RDF comparison is qualitative / semi-quantitative because the reference guide is based on transparent manual anchor points rather than exact tabulated data.

## Final Checklist

See [FINAL_SUBMISSION.md](FINAL_SUBMISSION.md) for a short submission checklist you can follow line by line on the remote server.
