# Final Submission Checklist

Use this from a clean copy of the repository on the remote machine.

## 1. Toolchain Check

```bash
mpicxx --version
mpirun --version
python3 - <<'PY'
import numpy, matplotlib
print("numpy:", numpy.__version__)
print("matplotlib:", matplotlib.__version__)
PY
```

## 2. Build And Test

```bash
make clean
make
make test
```

## 3. Generate Full Results

```bash
bash scripts/run_results.sh
```

Check that these exist afterward:

```bash
ls out/manifest.json
ls out/plots/results*.png
ls out/summary/results1
ls out/summary/results2
ls out/scaling_strong.csv out/scaling_size.csv
```

## 4. Sanity-Check The Report Facts

Before finalising the write-up, confirm these are still true for the generated dataset:

- required LJ production run: `100` steps / `1 ps`
- RDF: separate long Verlet run (`20000` production steps)
- default scaling path is pinned deterministic reference data from `scripts/data/reference_scaling/`
- pinned strong scaling: `1000` timed steps
- pinned size scaling: `1000` timed steps
- pinned timing data are medians over `11` repetitions per point

## 5. Create Submission Tarball

```bash
make dist BCN=<your_candidate_number>
```

Inspect the tarball contents:

```bash
tar -tzvf <your_candidate_number>_wa2.tar.gz | head -40
```

## 6. Final Manual Check

- README matches what you actually ran.
- The report text matches the generated data.
- Scaling section and script settings agree on the configured timed-step counts.
- The tarball does not include `out/` or binaries.
