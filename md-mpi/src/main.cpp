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
#include <ctime>
#include <algorithm>
#include <fstream>
#include <functional>
#include <iomanip>
#include <limits>
#include <random>
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

    // Parse parameters
    md::Params params;
    md::Params::parse(argc, argv, params);

    // MPI setup and particle decomposition
    md::MPIContext ctx;
    ctx.init(params.N);
    ctx.timingMode = params.timing;

    const bool isHO = (params.mode == "ho");
    const int N = params.N;
    const int equilibrationSteps = isHO ? 0 : std::max(0, params.equilibrationSteps);
    const int nSteps = isHO ? params.steps : std::max(0, params.productionSteps);
    const int nFrames = nSteps + 1;
    const int totalStepsExecuted = nSteps + equilibrationSteps;
    const int productionStartStep = 0;
    int grDiscardSteps = params.grDiscardSteps;
    int grSampleEvery = params.grSampleEvery;
    if (grDiscardSteps < 0) {
        if (ctx.isRoot()) {
            std::fprintf(stderr,
                         "WARNING: --gr-discard-steps=%d is invalid; using 0 instead.\n",
                         grDiscardSteps);
        }
        grDiscardSteps = 0;
    }
    if (grSampleEvery <= 0) {
        if (ctx.isRoot()) {
            std::fprintf(stderr,
                         "WARNING: --gr-sample-every=%d is invalid; using 1 instead.\n",
                         grSampleEvery);
        }
        grSampleEvery = 1;
    }
    const int grStart = productionStartStep + grDiscardSteps;
    const int maxGRFrames = (!isHO && params.gr && grStart <= nSteps)
                                ? (1 + (nSteps - grStart) / grSampleEvery)
                                : 0;

    // Box side length (constant density scaling for LJ)
    // For LJ: scale from Rahman's L=10.229*sigma for N=864 to maintain constant density
    // For HO: L is irrelevant (non-interacting), set to a large value
    double L;
    if (isHO) {
        L = md::constants::L_ho_dummy;  // effectively unused for HO
    } else {
        L = md::constants::L_sigma_rahman * md::constants::sigma *
            std::cbrt(static_cast<double>(N) / md::constants::N_rahman);
    }

    // Generate initial conditions on rank 0, broadcast to all
    std::vector<double> posAll(3 * N, 0.0);
    std::vector<double> velAll(3 * N, 0.0);
    int fccError = 0;  // broadcast from root to all ranks (LJ only)

    if (ctx.isRoot()) {
        if (isHO) {
            if (params.N != 1) {
                std::fprintf(
                    stderr,
                    "WARNING: HO validation expects N=1. Continuing with N>1 treats particles as "
                    "independent copies.\n");
            }
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
                // Single RNG stream for both
                std::mt19937_64 gen(params.seed);
                posAll = md::buildFCCLattice(N, L, gen);
                velAll =
                    md::generateVelocities(N, params.targetTemperature, md::constants::mass, gen);

                double sumV2 = 0.0;
                for (int i = 0; i < 3 * N; ++i) {
                    sumV2 += velAll[i] * velAll[i];
                }
                double eKin0 = 0.5 * md::constants::mass * sumV2;
                double tMeasured0 = md::computeTemperature(eKin0, N);

                std::printf("=== Initial Conditions (Rank 0) ===\n");
                std::printf("Seed used for RNG: %d\n", params.seed);
                std::printf("FCC lattice generated\n");
                std::printf("Perturbation amplitude: %.6e m (%.4f sigma)\n",
                            md::constants::fccPerturbation * md::constants::sigma,
                            md::constants::fccPerturbation);
                std::printf("Box-Muller velocities applied\n");
                std::printf("Initial measured Temperature: %.6f K\n", tMeasured0);
                std::printf("===================================\n");
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

    // Initialise local system state
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

    // Wrap positions into [0, L)
    if (!isHO) {
        sys.wrapPositions();
        ctx.allgatherPositions(sys.pos);
    }

    // Build force function
    double omega = params.omega;
    double mass = md::constants::mass;

    auto evalHO = [omega, mass](md::System& s, const std::vector<double>& pg, double& pe) {
        md::computeHOForces(s, pg, pe, omega, mass);
    };
    auto evalLJ = [mass](md::System& s, const std::vector<double>& pg, double& pe) {
        md::computeLJForces(s, pg, pe, mass);
    };

    enum class IntegratorType { Euler, RK4, Verlet };
    IntegratorType intType = IntegratorType::Verlet;
    if (params.integrator == "euler")
        intType = IntegratorType::Euler;
    else if (params.integrator == "rk4")
        intType = IntegratorType::RK4;
    double localPE = 0.0;

    auto advanceOneStep = [&]() {
        if (intType == IntegratorType::Euler) {
            if (isHO)
                md::stepEuler(sys, ctx, params.dt, evalHO, localPE, isHO);
            else
                md::stepEuler(sys, ctx, params.dt, evalLJ, localPE, isHO);
        } else if (intType == IntegratorType::RK4) {
            if (isHO)
                md::stepRK4(sys, ctx, params.dt, evalHO, localPE, isHO);
            else
                md::stepRK4(sys, ctx, params.dt, evalLJ, localPE, isHO);
        } else {
            if (isHO)
                md::stepVelocityVerlet(sys, ctx, params.dt, evalHO, localPE, isHO);
            else
                md::stepVelocityVerlet(sys, ctx, params.dt, evalLJ, localPE, isHO);
        }
    };

    // Initial force evaluation
    if (isHO) {
        evalHO(sys, ctx.posGlobal, localPE);
    } else {
        evalLJ(sys, ctx.posGlobal, localPE);
    }

    bool finalRescaleApplied = false;
    double startupTempBeforeFinal = std::numeric_limits<double>::quiet_NaN();
    double startupTempAfterFinal = std::numeric_limits<double>::quiet_NaN();

    // LJ startup/equilibration: optional pre-production preparation with rescaling.
    if (!isHO) {
        for (int startupStep = 1; startupStep <= equilibrationSteps; ++startupStep) {
            double localKE = md::computeLocalKineticEnergy(sys, md::constants::mass);
            double totalKE = 0.0, totalPE = 0.0;
            MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
            MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

            double lambda = 1.0;
            if (ctx.isRoot()) {
                double tMeasured = md::computeTemperature(totalKE, N);
                if (tMeasured > md::constants::rescaleGuard) {
                    lambda = std::sqrt(params.targetTemperature / tMeasured);
                }
                if (!params.timing) {
                    std::printf(
                        "Startup rescale step %d/%d: lambda = %.15e, T_before = %.6f K, "
                        "target = %.6f K\n",
                        startupStep, equilibrationSteps, lambda, tMeasured, params.targetTemperature);
                }
            }
            MPI_Bcast(&lambda, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
            for (int i = 0; i < 3 * sys.localN; ++i) {
                sys.vel[i] *= lambda;
            }

            advanceOneStep();
        }

        double localKE = md::computeLocalKineticEnergy(sys, md::constants::mass);
        double totalKE = 0.0, totalPE = 0.0;
        MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
        MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

        if (ctx.isRoot()) {
            startupTempBeforeFinal = md::computeTemperature(totalKE, N);
        }

        if (params.finalRescaleBeforeProduction) {
            double lambda = 1.0;
            if (ctx.isRoot()) {
                if (startupTempBeforeFinal > md::constants::rescaleGuard) {
                    lambda = std::sqrt(params.targetTemperature / startupTempBeforeFinal);
                }
                finalRescaleApplied = std::abs(lambda - 1.0) > 1e-12;
                if (!params.timing) {
                    std::printf("Startup->production rescale: lambda = %.15e, T_before = %.6f K\n",
                                lambda, startupTempBeforeFinal);
                }
            }
            MPI_Bcast(&lambda, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
            for (int i = 0; i < 3 * sys.localN; ++i) {
                sys.vel[i] *= lambda;
            }

            localKE = md::computeLocalKineticEnergy(sys, md::constants::mass);
            totalKE = 0.0;
            MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
            if (ctx.isRoot()) {
                startupTempAfterFinal = md::computeTemperature(totalKE, N);
            }
        } else {
            startupTempAfterFinal = startupTempBeforeFinal;
        }
    }

    // Create output directory and open file on rank 0
    std::ofstream outFile;
    if (params.output && ctx.isRoot()) {
        std::string fname;
        if (!params.outdir.empty()) {
            fname = params.outdir + "/" + params.mode + "_" + params.integrator + ".csv";
        } else {
            mkdir("out", 0755);
            fname = "out/" + params.mode + "_" + params.integrator + ".csv";
        }
        outFile.open(fname);
        if (outFile.is_open()) {
            outFile << std::setprecision(15);
            std::time_t t = std::time(nullptr);
            char tstr[100];
            std::strftime(tstr, sizeof(tstr), "%Y-%m-%dT%H:%M:%SZ", std::gmtime(&t));
            outFile << "# mode: " << params.mode << ", integrator: " << params.integrator
                    << ", N: " << N << ", P: " << ctx.size << ", dt: " << params.dt
                    << ", steps: " << nSteps << ", n_steps: " << nSteps
                    << ", n_frames: " << nFrames
                    << ", step_indexing: 0..steps (includes initial frame)"
                    << ", total_steps_executed: " << totalStepsExecuted
                    << ", seed: " << params.seed << ", L: " << L
                    << ", rcut: " << md::constants::rcut_sigma * md::constants::sigma
                    << ", target_temperature: " << params.targetTemperature
                    << ", equilibration_steps: " << equilibrationSteps
                    << ", production_steps: " << nSteps
                    << ", production_start_step: " << productionStartStep
                    << ", final_rescale_before_production: "
                    << (params.finalRescaleBeforeProduction ? "true" : "false")
                    << ", final_rescale_applied: " << (finalRescaleApplied ? "true" : "false")
                    << ", production_nve: " << (!isHO ? "true" : "false")
                    << ", gr_discard_steps: " << grDiscardSteps
                    << ", gr_sample_every: " << grSampleEvery << ", gr_start: " << grStart;
            if (!isHO && std::isfinite(startupTempBeforeFinal)) {
                outFile << ", startup_temperature_before_final_rescale: " << startupTempBeforeFinal;
            }
            if (!isHO && std::isfinite(startupTempAfterFinal)) {
                outFile << ", startup_temperature_after_final_rescale: " << startupTempAfterFinal;
            }
            if (!isHO) {
                outFile << ", lattice: FCC, velocities: Box-Muller";
            }
            outFile << ", timestamp: " << tstr << "\n";
            if (isHO) {
                // HO: output position, velocity, energy for phase-space & convergence plots
                outFile << "step,time,x,v,E_kin,E_pot,E_total\n";
            } else {
                outFile << "step,time,E_kin,E_pot,E_total,temperature\n";
            }
        }
    }

    // Print simulation info on rank 0
    if (ctx.isRoot() && !params.timing) {
        std::printf("=== MD Solver ===\n");
        std::printf("Mode: %s | Integrator: %s\n", params.mode.c_str(), params.integrator.c_str());
        std::printf(
            "N = %d | P = %d | timesteps = %d | frames = %d (step 0..%d) | dt = %.3e\n", N,
            ctx.size, nSteps, nFrames, nSteps, params.dt);
        if (!isHO) {
            std::printf(
                "LJ semantics: --equilibration-steps prepares the state, --production-steps "
                "controls the reported NVE trajectory.\n");
            std::printf(
                "Output includes the production initial frame at step 0 (n_frames = "
                "production_steps + 1).\n");
            std::printf("L = %.6e m (%.4f sigma)\n", L, L / md::constants::sigma);
            std::printf("Target temperature = %.1f K | seed = %d\n", params.targetTemperature,
                        params.seed);
            std::printf("Startup timesteps = %d | production timesteps = %d | total executed = %d\n",
                        equilibrationSteps, nSteps, totalStepsExecuted);
            std::printf("Production simulated time = %.3e s (= production_steps * dt)\n",
                        nSteps * params.dt);
            std::printf("production_start_step = %d (production-only output)\n", productionStartStep);
            if (std::isfinite(startupTempBeforeFinal)) {
                std::printf("Startup boundary temperature before final rescale: %.6f K\n",
                            startupTempBeforeFinal);
            }
            if (std::isfinite(startupTempAfterFinal)) {
                std::printf("Startup boundary temperature after final rescale: %.6f K\n",
                            startupTempAfterFinal);
            }
            if (params.gr) {
                std::printf(
                    "g(r): production_start_step=%d, gr_start=%d (= production_start_step + "
                    "gr_discard_steps=%d), sample_every=%d\n",
                    productionStartStep, grStart, grDiscardSteps, grSampleEvery);
            }
        } else {
            std::printf(
                "Step semantics: --steps is the number of integration updates; output includes "
                "the initial frame at step 0.\n");
            std::printf("HO mode: periodic box size is not used\n");
        }
        std::printf("==================\n");
    }

    if (params.gr && !isHO && maxGRFrames <= 0 && ctx.isRoot()) {
        if (grStart > nSteps) {
            std::fprintf(stderr,
                         "WARNING: g(r) requested but gr_start=%d is beyond final step=%d. "
                         "No RDF frames will be sampled.\n",
                         grStart, nSteps);
        } else {
            std::fprintf(stderr,
                         "WARNING: g(r) requested but no frames available "
                         "(production_steps=%d, production_start_step=%d, gr_discard_steps=%d).\n",
                         nSteps, productionStartStep, grDiscardSteps);
        }
    }

    // g(r) histogram setup for LJ mode
    // Keep HO mode at zero-sized buffers to avoid meaningless allocations.
    const double grDr = md::constants::grBinWidthSigma * md::constants::sigma;  // bin width
    const double grRMax = isHO ? 0.0 : 0.5 * L;                                  // [0, L/2] for LJ
    const int grNBins = isHO ? 0 : static_cast<int>(grRMax / grDr);
    std::vector<double> grHistLocal(grNBins, 0.0);
    int grFrames = 0;

    // Timing setup
    MPI_Barrier(MPI_COMM_WORLD);
    double tStart = MPI_Wtime();

    // Time-stepping loop
    for (int step = 0; step <= nSteps; ++step) {
        // Compute observables (skip in timing mode)
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

        }

        // Accumulate g(r) histogram in the production window
        if (params.gr && !isHO && step >= grStart && ((step - grStart) % grSampleEvery == 0)) {
            md::accumulateGR(ctx.posGlobal, N, L, ctx.offset, ctx.localN, grDr, grRMax,
                             grHistLocal);
            ++grFrames;
        }

        // Advance one timestep; skip update on the last iteration
        if (step == nSteps)
            break;

        advanceOneStep();
    }

    // Timing completion
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

    // Write g(r) to file for LJ mode
    if (params.gr && !isHO && grFrames > 0) {
        // Reduce histogram across all ranks
        std::vector<double> grHistGlobal(grNBins, 0.0);
        MPI_Reduce(grHistLocal.data(), grHistGlobal.data(), grNBins, MPI_DOUBLE, MPI_SUM, 0,
                   MPI_COMM_WORLD);

        if (ctx.isRoot()) {
            // Normalise: g(r) = (1 / (rho * N)) * count / (4*pi*r^2 * dr * nFrames)
            md::normaliseGR(grHistGlobal, grDr, N, L, grFrames);

            std::string grFname = params.outdir.empty() ? "out/gr.csv" : params.outdir + "/gr.csv";
            std::ofstream grFile(grFname);
            if (grFile.is_open()) {
                std::time_t t = std::time(nullptr);
                char tstr[100];
                std::strftime(tstr, sizeof(tstr), "%Y-%m-%dT%H:%M:%SZ", std::gmtime(&t));
                grFile << "# mode: " << params.mode << ", integrator: " << params.integrator
                       << ", N: " << N << ", P: " << ctx.size << ", dt: " << params.dt
                       << ", steps: " << nSteps << ", n_steps: " << nSteps
                       << ", n_frames: " << nFrames
                       << ", step_indexing: 0..steps (includes initial frame)"
                       << ", total_steps_executed: " << totalStepsExecuted
                       << ", seed: " << params.seed << ", L: " << L
                       << ", rcut: " << md::constants::rcut_sigma * md::constants::sigma
                       << ", target_temperature: " << params.targetTemperature
                       << ", equilibration_steps: " << equilibrationSteps
                       << ", production_steps: " << nSteps
                       << ", production_start_step: " << productionStartStep
                       << ", final_rescale_before_production: "
                       << (params.finalRescaleBeforeProduction ? "true" : "false")
                       << ", final_rescale_applied: " << (finalRescaleApplied ? "true" : "false")
                       << ", production_nve: true"
                       << ", gr_discard_steps: " << grDiscardSteps
                       << ", gr_sample_every: " << grSampleEvery << ", gr_start: " << grStart
                       << ", lattice: FCC, velocities: Box-Muller, timestamp: " << tstr << "\n";
                grFile << "r_sigma,gr\n";
                for (int b = 0; b < grNBins; ++b) {
                    double rMid = (b + 0.5) * grDr;
                    grFile << (rMid / md::constants::sigma) << "," << grHistGlobal[b] << "\n";
                }
                grFile.close();
                if (!params.timing) {
                    std::printf("g(r) written to %s (%d bins, %d frames)\n", grFname.c_str(),
                                grNBins, grFrames);
                }
            }
        }
    } else if (params.gr && !isHO && ctx.isRoot() && !params.timing) {
        std::fprintf(stderr,
                     "WARNING: g(r) skipped because no frames were sampled. "
                     "Adjust --production-steps, --equilibration-steps, --gr-discard-steps, or "
                     "--gr-sample-every.\n");
    }

    // Close output file
    if (outFile.is_open()) {
        outFile.close();
    }

    MPI_Finalize();
    return 0;
}
