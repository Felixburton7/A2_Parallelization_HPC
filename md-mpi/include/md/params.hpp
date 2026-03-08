/**
 * @file params.hpp
 * @brief Runtime parameters.
 */

#ifndef MD_PARAMS_HPP
#define MD_PARAMS_HPP

#include <cstdlib>
#include <string>

namespace md {

/// @brief Runtime parameters parsed from command-line arguments.
struct Params {
    int N = 864;                        ///< Number of particles
    int steps = 100;                    ///< Number of timesteps (HO) / legacy alias for LJ production_steps
    double dt = 1.0e-14;                ///< Timestep [s] (for LJ) or dimensionless (for HO)
    double T_init = 94.4;               ///< Legacy alias of targetTemperature [K]
    double targetTemperature = 94.4;    ///< Target temperature for LJ startup/production handoff [K]
    int equilibrationSteps = 50;        ///< LJ startup timesteps before production (with optional rescaling)
    int productionSteps = 100;          ///< LJ production timesteps (NVE after startup/final rescale)
    bool finalRescaleBeforeProduction = true;  ///< Apply one exact rescale at startup->production boundary
    double omega = 1.0;                 ///< HO angular frequency (only for mode "ho")
    std::string integrator = "verlet";  ///< "euler", "rk4", "verlet"
    std::string mode = "lj";            ///< "ho" or "lj"
    bool output = true;                 ///< Enable CSV output
    int seed = 42;                      ///< RNG seed for reproducibility
    int rescaleStep = -1;               ///< Legacy alias for equilibrationSteps (for CLI compatibility)
    bool timing = false;                ///< Enable wall-clock timing (disables output)
    bool gr = false;                    ///< Enable g(r) accumulation
    int grDiscardSteps = 200;           ///< Steps to discard after production_start_step before g(r)
    int grSampleEvery = 5;              ///< Sample g(r) every N steps after discard
    std::string outdir = "";            ///< Output directory for per-run namespaces

    static void parse(int argc, char* argv[], Params& p) {
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg == "--N" && i + 1 < argc)
                p.N = std::atoi(argv[++i]);
            else if (arg == "--steps" && i + 1 < argc) {
                p.steps = std::atoi(argv[++i]);
                p.productionSteps = p.steps;
            } else if (arg == "--production-steps" && i + 1 < argc)
                p.productionSteps = std::atoi(argv[++i]);
            else if (arg == "--equilibration-steps" && i + 1 < argc)
                p.equilibrationSteps = std::atoi(argv[++i]);
            else if (arg == "--dt" && i + 1 < argc)
                p.dt = std::atof(argv[++i]);
            else if ((arg == "--T" || arg == "--target-temperature") && i + 1 < argc) {
                p.T_init = std::atof(argv[++i]);
                p.targetTemperature = p.T_init;
            } else if (arg == "--omega" && i + 1 < argc)
                p.omega = std::atof(argv[++i]);
            else if (arg == "--integrator" && i + 1 < argc)
                p.integrator = argv[++i];
            else if (arg == "--mode" && i + 1 < argc)
                p.mode = argv[++i];
            else if (arg == "--no-output")
                p.output = false;
            else if (arg == "--seed" && i + 1 < argc)
                p.seed = std::atoi(argv[++i]);
            else if (arg == "--outdir" && i + 1 < argc)
                p.outdir = argv[++i];
            else if (arg == "--rescale-step" && i + 1 < argc) {
                p.rescaleStep = std::atoi(argv[++i]);
                p.equilibrationSteps = p.rescaleStep < 0 ? 0 : p.rescaleStep;
            } else if (arg == "--final-rescale-before-production")
                p.finalRescaleBeforeProduction = true;
            else if (arg == "--no-final-rescale-before-production")
                p.finalRescaleBeforeProduction = false;
            else if (arg == "--timing") {
                p.timing = true;
                p.output = false;
            } else if (arg == "--gr")
                p.gr = true;
            else if ((arg == "--gr-discard-steps" || arg == "--gr-discard") && i + 1 < argc)
                p.grDiscardSteps = std::atoi(argv[++i]);
            else if ((arg == "--gr-sample-every" || arg == "--gr-interval") && i + 1 < argc)
                p.grSampleEvery = std::atoi(argv[++i]);
        }
    }
};

}  // namespace md

#endif  // MD_PARAMS_HPP
