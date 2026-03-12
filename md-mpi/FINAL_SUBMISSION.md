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

## 4. Generate Context Files

```bash
bash ai/generate_all_context.sh
```

Check that these exist afterward:

```bash
ls ai/audit_output.md ai/results.md ai/results_bundle.md ai/context_bundle.tar.gz
```

## 5. Sanity-Check The Report Facts

Before finalising the write-up, confirm these are still true for the generated dataset:

- required LJ production run: `100` steps / `1 ps`
- RDF: separate long Verlet run (`20000` production steps)
- strong scaling: `500` timed steps
- size scaling: `2000` timed steps
- timing data are medians over `20` repetitions per point

## 6. Create Submission Tarball

```bash
make dist BCN=<your_candidate_number>
```

Inspect the tarball contents:

```bash
tar -tzvf <your_candidate_number>_wa2.tar.gz | head -40
```

## 7. Final Manual Check

- README matches what you actually ran.
- The report text matches the generated data.
- Scaling section does not claim `100` steps unless you regenerated the timings that way.
- The tarball does not include `out/`, `ai/`, or binaries.
