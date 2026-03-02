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
    double maxTime = 0.0;
    MPI_Reduce(&elapsed, &maxTime, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    // Communication time breakdown (timing mode only)
    double maxCommTime = 0.0;
    if (params.timing) {
        MPI_Reduce(&ctx.commTime, &maxCommTime, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
    }

    if (ctx.isRoot()) {
        std::printf("Wall time: %.6f s (max across %d ranks)\n", maxTime, ctx.size);
        if (params.timing) {
            double computeTime = maxTime - maxCommTime;
            std::printf("  Comm time: %.6f s (%.1f%%)\n", maxCommTime,
                        100.0 * maxCommTime / maxTime);
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
