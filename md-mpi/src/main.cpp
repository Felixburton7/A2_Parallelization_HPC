/**
 * @file main.cpp
 * @brief Main entry point for the MPI Molecular Dynamics solver.
 */

#include <mpi.h>
#include <sys/stat.h>

#include <algorithm>
#include <cmath>
#include <cstdio>
#include <ctime>
#include <fstream>
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

namespace {

int buildInitialConditions(const md::Params& params, bool isHO, int N, double L,
                           std::vector<double>& posAll, std::vector<double>& velAll) {
    if (isHO) {
        if (params.N != 1) {
            std::fprintf(
                stderr,
                "WARNING: HO validation expects N=1. Continuing with N>1 treats particles as "
                "independent copies.\n");
        }
        // HO validation state: x(0)=1, v(0)=0 for each particle copy.
        for (int i = 0; i < N; ++i) {
            posAll[3 * i] = 1.0;
            posAll[3 * i + 1] = 0.0;
            posAll[3 * i + 2] = 0.0;
            velAll[3 * i] = 0.0;
            velAll[3 * i + 1] = 0.0;
            velAll[3 * i + 2] = 0.0;
        }
        return 0;
    }

    // FCC lattice requires N = 4*k^3.
    const int k = static_cast<int>(std::round(std::cbrt(N / 4.0)));
    if (4 * k * k * k != N) {
        std::fprintf(stderr,
                     "ERROR: N = %d is not a valid FCC particle count "
                     "(need N = 4*k^3, nearest k = %d gives N = %d)\n",
                     N, k, 4 * k * k * k);
        return 1;
    }

    std::mt19937_64 gen(params.seed);
    posAll = md::buildFCCLattice(N, L, gen);
    velAll = md::generateVelocities(N, params.targetTemperature, md::constants::mass, gen);

    double sumV2 = 0.0;
    for (int i = 0; i < 3 * N; ++i) {
        sumV2 += velAll[i] * velAll[i];
    }
    const double tMeasured0 = md::computeTemperature(0.5 * md::constants::mass * sumV2, N);

    std::printf("=== Initial Conditions (Rank 0) ===\n");
    std::printf("Seed: %d | FCC lattice | Box-Muller velocities\n", params.seed);
    std::printf("Perturbation: %.4f sigma | T_initial: %.6f K\n", md::constants::fccPerturbation,
                tMeasured0);
    std::printf("===================================\n");
    return 0;
}

void writeCSVMetadataLine(std::ostream& out, const md::Params& params, int N, int P, int nSteps,
                          int nFrames, int totalStepsExecuted, int equilibrationSteps,
                          bool finalRescaleApplied, int productionStartStep, int grDiscardSteps,
                          int grSampleEvery, int grStart, double startupTempBeforeFinal,
                          double startupTempAfterFinal, double L, bool productionNVE,
                          bool includeLattice) {
    const std::time_t t = std::time(nullptr);
    char tstr[100];
    std::strftime(tstr, sizeof(tstr), "%Y-%m-%dT%H:%M:%SZ", std::gmtime(&t));

    out << "# mode: " << params.mode << ", integrator: " << params.integrator
        << ", N: " << N << ", P: " << P << ", dt: " << params.dt << ", steps: " << nSteps
        << ", n_steps: " << nSteps << ", n_frames: " << nFrames
        << ", step_indexing: 0..steps (includes initial frame)"
        << ", total_steps_executed: " << totalStepsExecuted << ", seed: " << params.seed
        << ", L: " << L << ", rcut: " << md::constants::rcut_sigma * md::constants::sigma
        << ", target_temperature: " << params.targetTemperature
        << ", equilibration_steps: " << equilibrationSteps
        << ", production_steps: " << nSteps << ", production_start_step: " << productionStartStep
        << ", final_rescale_before_production: "
        << (params.finalRescaleBeforeProduction ? "true" : "false")
        << ", final_rescale_applied: " << (finalRescaleApplied ? "true" : "false")
        << ", production_nve: " << (productionNVE ? "true" : "false")
        << ", gr_discard_steps: " << grDiscardSteps << ", gr_sample_every: " << grSampleEvery
        << ", gr_start: " << grStart;

    if (std::isfinite(startupTempBeforeFinal)) {
        out << ", startup_temperature_before_final_rescale: " << startupTempBeforeFinal;
    }
    if (std::isfinite(startupTempAfterFinal)) {
        out << ", startup_temperature_after_final_rescale: " << startupTempAfterFinal;
    }
    if (includeLattice) {
        out << ", lattice: FCC, velocities: Box-Muller";
    }
    out << ", timestamp: " << tstr << "\n";
}

template <typename AdvanceFn>
void runStartupPhaseLJ(md::System& sys, md::MPIContext& ctx, const md::Params& params, int N,
                       int equilibrationSteps, double& localPE, AdvanceFn&& advanceOneStep,
                       bool& finalRescaleApplied, double& startupTempBeforeFinal,
                       double& startupTempAfterFinal) {
    for (int startupStep = 1; startupStep <= equilibrationSteps; ++startupStep) {
        const double localKE = md::computeLocalKineticEnergy(sys, md::constants::mass);
        double totalKE = 0.0;
        double totalPE = 0.0;
        MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
        MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

        double lambda = 1.0;
        if (ctx.isRoot()) {
            const double tMeasured = md::computeTemperature(totalKE, N);
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
    double totalKE = 0.0;
    double totalPE = 0.0;
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

void printSimulationInfo(const md::Params& params, const md::MPIContext& ctx, bool isHO, int N,
                         int nSteps, int nFrames, int totalStepsExecuted, int equilibrationSteps,
                         double L, int productionStartStep, int grStart, int grDiscardSteps,
                         int grSampleEvery, double startupTempBeforeFinal,
                         double startupTempAfterFinal) {
    if (!ctx.isRoot() || params.timing) {
        return;
    }

    std::printf("=== MD Solver ===\n");
    std::printf("Mode: %s | Integrator: %s\n", params.mode.c_str(), params.integrator.c_str());
    std::printf("N = %d | P = %d | timesteps = %d | frames = %d (step 0..%d) | dt = %.3e\n", N,
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

}  // namespace

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    md::Params params;
    md::Params::parse(argc, argv, params);

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

    const int grDiscardSteps = params.grDiscardSteps;
    const int grSampleEvery = params.grSampleEvery;
    const int grStart = productionStartStep + grDiscardSteps;
    const int maxGRFrames = (!isHO && params.gr && grStart <= nSteps)
                                ? (1 + (nSteps - grStart) / grSampleEvery)
                                : 0;

    // Constant-density LJ scaling from Rahman's N=864 reference state.
    const double L = isHO ? md::constants::L_ho_dummy
                          : md::constants::L_sigma_rahman * md::constants::sigma *
                                std::cbrt(static_cast<double>(N) / md::constants::N_rahman);

    std::vector<double> posAll(3 * N, 0.0);
    std::vector<double> velAll(3 * N, 0.0);
    int fccError = 0;

    if (ctx.isRoot()) {
        fccError = buildInitialConditions(params, isHO, N, L, posAll, velAll);
    }

    if (!isHO) {
        MPI_Bcast(&fccError, 1, MPI_INT, 0, MPI_COMM_WORLD);
        if (fccError) {
            MPI_Finalize();
            return 1;
        }
    }

    // Every rank needs global positions/velocities for force evaluation and integrator state.
    MPI_Bcast(posAll.data(), 3 * N, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(velAll.data(), 3 * N, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    md::System sys;
    sys.init(ctx.localN, ctx.offset, N, L);

    for (int i = 0; i < ctx.localN; ++i) {
        for (int d = 0; d < 3; ++d) {
            sys.pos[3 * i + d] = posAll[3 * (ctx.offset + i) + d];
            sys.vel[3 * i + d] = velAll[3 * (ctx.offset + i) + d];
        }
    }

    ctx.posGlobal = posAll;
    if (!isHO) {
        sys.wrapPositions();
        ctx.allgatherPositions(sys.pos);
    }

    const double omega = params.omega;
    const double mass = md::constants::mass;

    enum class IntegratorType { Euler, RK4, Verlet };
    IntegratorType intType = IntegratorType::Verlet;
    if (params.integrator == "euler") {
        intType = IntegratorType::Euler;
    } else if (params.integrator == "rk4") {
        intType = IntegratorType::RK4;
    }

    auto evalHO = [omega, mass](md::System& s, const std::vector<double>& pg, double& pe) {
        md::computeHOForces(s, pg, pe, omega, mass);
    };
    auto evalLJ = [mass](md::System& s, const std::vector<double>& pg, double& pe) {
        md::computeLJForces(s, pg, pe, mass);
    };

    double localPE = 0.0;
    auto advanceOneStep = [&]() {
        if (intType == IntegratorType::Euler) {
            if (isHO) {
                md::stepEuler(sys, ctx, params.dt, evalHO, localPE, isHO);
            } else {
                md::stepEuler(sys, ctx, params.dt, evalLJ, localPE, isHO);
            }
        } else if (intType == IntegratorType::RK4) {
            if (isHO) {
                md::stepRK4(sys, ctx, params.dt, evalHO, localPE, isHO);
            } else {
                md::stepRK4(sys, ctx, params.dt, evalLJ, localPE, isHO);
            }
        } else {
            if (isHO) {
                md::stepVelocityVerlet(sys, ctx, params.dt, evalHO, localPE, isHO);
            } else {
                md::stepVelocityVerlet(sys, ctx, params.dt, evalLJ, localPE, isHO);
            }
        }
    };

    if (isHO) {
        evalHO(sys, ctx.posGlobal, localPE);
    } else {
        evalLJ(sys, ctx.posGlobal, localPE);
    }

    bool finalRescaleApplied = false;
    double startupTempBeforeFinal = std::numeric_limits<double>::quiet_NaN();
    double startupTempAfterFinal = std::numeric_limits<double>::quiet_NaN();

    if (!isHO) {
        runStartupPhaseLJ(sys, ctx, params, N, equilibrationSteps, localPE, advanceOneStep,
                          finalRescaleApplied, startupTempBeforeFinal, startupTempAfterFinal);
    }

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
            writeCSVMetadataLine(outFile, params, N, ctx.size, nSteps, nFrames,
                                 totalStepsExecuted, equilibrationSteps, finalRescaleApplied,
                                 productionStartStep, grDiscardSteps, grSampleEvery, grStart,
                                 startupTempBeforeFinal, startupTempAfterFinal, L, !isHO, !isHO);
            if (isHO) {
                outFile << "step,time,x,v,E_kin,E_pot,E_total\n";
            } else {
                outFile << "step,time,E_kin,E_pot,E_total,temperature\n";
            }
        }
    }

    printSimulationInfo(params, ctx, isHO, N, nSteps, nFrames, totalStepsExecuted,
                        equilibrationSteps, L, productionStartStep, grStart, grDiscardSteps,
                        grSampleEvery, startupTempBeforeFinal, startupTempAfterFinal);

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

    const double grDr = md::constants::grBinWidthSigma * md::constants::sigma;
    const double grRMax = isHO ? 0.0 : 0.5 * L;
    const int grNBins = isHO ? 0 : static_cast<int>(grRMax / grDr);
    std::vector<double> grHistLocal(grNBins, 0.0);
    int grFrames = 0;

    // Synchronise clocks before timed production loop (exclude startup/output setup).
    MPI_Barrier(MPI_COMM_WORLD);
    const double tStart = MPI_Wtime();

    for (int step = 0; step <= nSteps; ++step) {
        double totalKE = 0.0;
        double totalPE = 0.0;

        if (!params.timing) {
            const double localKE = md::computeLocalKineticEnergy(sys, md::constants::mass);
            MPI_Reduce(&localKE, &totalKE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
            MPI_Reduce(&localPE, &totalPE, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

            if (params.output && ctx.isRoot() && outFile.is_open()) {
                const double totalE = totalKE + totalPE;
                const double time = step * params.dt;
                if (isHO) {
                    const double x = sys.pos[0];
                    const double v = sys.vel[0];
                    outFile << step << "," << time << "," << x << "," << v << "," << totalKE
                            << "," << totalPE << "," << totalE << "\n";
                } else {
                    const double T = md::computeTemperature(totalKE, N);
                    outFile << step << "," << time << "," << totalKE << "," << totalPE << ","
                            << totalE << "," << T << "\n";
                }
            }
        }

        // Sample RDF only on production frames that pass discard/stride filters.
        if (params.gr && !isHO && step >= grStart && ((step - grStart) % grSampleEvery == 0)) {
            md::accumulateGR(ctx.posGlobal, N, L, ctx.offset, ctx.localN, grDr, grRMax,
                             grHistLocal);
            ++grFrames;
        }

        // Step 0 is the production initial condition; advance after writing/sampling.
        if (step == nSteps) {
            break;
        }

        advanceOneStep();
    }

    const double elapsed = MPI_Wtime() - tStart;

    struct {
        double val;
        int rank;
    } localData{elapsed, ctx.rank}, globalData{0.0, 0};
    // Report wall time from the slowest rank; comm time is tracked in MPIContext::allgatherPositions.
    MPI_Allreduce(&localData, &globalData, 1, MPI_DOUBLE_INT, MPI_MAXLOC, MPI_COMM_WORLD);

    const double maxTime = globalData.val;
    const int slowestRank = globalData.rank;

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
            const double computeTime = maxTime - reportedCommTime;
            std::printf("  Comm time: %.6f s (%.1f%%)\n", reportedCommTime,
                        100.0 * reportedCommTime / maxTime);
            std::printf("  Compute time: %.6f s (%.1f%%)\n", computeTime,
                        100.0 * computeTime / maxTime);
        }
    }

    if (params.gr && !isHO && grFrames > 0) {
        std::vector<double> grHistGlobal(grNBins, 0.0);
        MPI_Reduce(grHistLocal.data(), grHistGlobal.data(), grNBins, MPI_DOUBLE, MPI_SUM, 0,
                   MPI_COMM_WORLD);

        if (ctx.isRoot()) {
            // RDF is sampled per frame, then normalised after summing histograms across ranks.
            md::normaliseGR(grHistGlobal, grDr, N, L, grFrames);

            const std::string grFname =
                params.outdir.empty() ? "out/gr.csv" : params.outdir + "/gr.csv";
            std::ofstream grFile(grFname);
            if (grFile.is_open()) {
                writeCSVMetadataLine(grFile, params, N, ctx.size, nSteps, nFrames,
                                     totalStepsExecuted, equilibrationSteps, finalRescaleApplied,
                                     productionStartStep, grDiscardSteps, grSampleEvery, grStart,
                                     startupTempBeforeFinal, startupTempAfterFinal, L, true,
                                     true);
                grFile << "r_sigma,gr\n";
                for (int b = 0; b < grNBins; ++b) {
                    const double rMid = (b + 0.5) * grDr;
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

    if (outFile.is_open()) {
        outFile.close();
    }

    MPI_Finalize();
    return 0;
}
