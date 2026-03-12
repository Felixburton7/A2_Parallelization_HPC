# A2_Parallelization_HPC

The main project for final submission is in [`md-mpi/`](md-mpi/).

Start with:

- [`md-mpi/README.md`](md-mpi/README.md) for the full build, test, results-generation, and packaging workflow
- [`md-mpi/FINAL_SUBMISSION.md`](md-mpi/FINAL_SUBMISSION.md) for a short remote-server checklist

Shortest end-to-end run from the project root:

```bash
cd md-mpi
make clean
make
make test
bash scripts/run_results.sh
bash ai/generate_all_context.sh
make dist BCN=<your_candidate_number>
```
