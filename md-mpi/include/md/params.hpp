/**
 * @file params.hpp
 * @brief Runtime parameter struct and CLI argument parser.
 *
 * All simulation parameters are configurable via command-line arguments.
 * No recompilation is needed to change N, dt, integrator, etc.
 */

#ifndef MD_PARAMS_HPP
#define MD_PARAMS_HPP

#include <cstdlib>
#include <iostream>
#include <string>

namespace md {

/// Parse result status (avoids std::exit before MPI_Finalize)
enum class ParseStatus { Ok, Help, Error };

static bool nextVal(int& i, int argc, const char* flag) {
    if (++i >= argc) {
        std::cerr << "Missing value for " << flag << "\n";
        return false;
    }
    return true;
}

/**
 * @brief Simulation parameters, parsed from command-line arguments.
 */
struct Params {
    int N = 864;                        ///< Number of particles
    int steps = 100;                    ///< Number of timesteps
    double dt = 1.0e-14;                ///< Timestep [s] (for LJ) or dimensionless (for HO)
    double T_init = 94.4;               ///< Initial temperature [K]
    double omega = 1.0;                 ///< HO angular frequency (only for mode "ho")
    std::string integrator = "verlet";  ///< "euler", "rk4", "verlet"
    std::string mode = "lj";            ///< "ho" or "lj"
    bool output = true;                 ///< Enable CSV output
    int seed = 42;                      ///< RNG seed for reproducibility
    int rescaleStep = -1;               ///< Step at which to apply optional rescale (-1 = disabled)
    bool timing = false;                ///< Enable wall-clock timing (disables output)
    bool gr = false;                    ///< Enable g(r) accumulation
    int grDiscard = 500;                ///< Steps to discard AFTER production_start before g(r)
    int grInterval = 10;                ///< Sample g(r) every N steps after discard
    std::string outdir = "";            ///< Output directory for per-run namespaces

    /**
     * @brief Parse command-line arguments into a Params struct.
     *
     * Validates mode ∈ {ho, lj} and integrator ∈ {euler, rk4, verlet}.
     *
     * @param argc   Argument count
     * @param argv   Argument values
     * @param[out] p Parsed Params struct
     * @return ParseStatus::Ok on success, Help or Error otherwise
     */
    static ParseStatus parse(int argc, char* argv[], Params& p) {
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg == "--help") {
                printUsage(argv[0]);
                return ParseStatus::Help;
            } else if (arg == "--N") {
                if (nextVal(i, argc, "--N"))
                    p.N = std::atoi(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--steps") {
                if (nextVal(i, argc, "--steps"))
                    p.steps = std::atoi(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--dt") {
                if (nextVal(i, argc, "--dt"))
                    p.dt = std::atof(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--T") {
                if (nextVal(i, argc, "--T"))
                    p.T_init = std::atof(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--omega") {
                if (nextVal(i, argc, "--omega"))
                    p.omega = std::atof(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--integrator") {
                if (nextVal(i, argc, "--integrator"))
                    p.integrator = argv[i];
                else
                    return ParseStatus::Error;
            } else if (arg == "--mode") {
                if (nextVal(i, argc, "--mode"))
                    p.mode = argv[i];
                else
                    return ParseStatus::Error;
            } else if (arg == "--no-output") {
                p.output = false;
            } else if (arg == "--seed") {
                if (nextVal(i, argc, "--seed"))
                    p.seed = std::atoi(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--outdir") {
                if (nextVal(i, argc, "--outdir"))
                    p.outdir = argv[i];
                else
                    return ParseStatus::Error;
            } else if (arg == "--rescale-step") {
                if (nextVal(i, argc, "--rescale-step"))
                    p.rescaleStep = std::atoi(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--timing") {
                p.timing = true;
                p.output = false;
            } else if (arg == "--gr") {
                p.gr = true;
            } else if (arg == "--gr-discard") {
                if (nextVal(i, argc, "--gr-discard"))
                    p.grDiscard = std::atoi(argv[i]);
                else
                    return ParseStatus::Error;
            } else if (arg == "--gr-interval") {
                if (nextVal(i, argc, "--gr-interval"))
                    p.grInterval = std::atoi(argv[i]);
                else
                    return ParseStatus::Error;
            } else {
                std::cerr << "Unknown argument: " << arg << "\n";
                return ParseStatus::Error;
            }
        }

        // Validate mode
        if (p.mode != "ho" && p.mode != "lj") {
            std::cerr << "Invalid --mode '" << p.mode << "' (must be 'ho' or 'lj')\n";
            return ParseStatus::Error;
        }

        // Validate integrator
        if (p.integrator != "euler" && p.integrator != "rk4" && p.integrator != "verlet") {
            std::cerr << "Invalid --integrator '" << p.integrator
                      << "' (must be 'euler', 'rk4', or 'verlet')\n";
            return ParseStatus::Error;
        }

        return ParseStatus::Ok;
    }

    /**
     * @brief Print usage information to stdout.
     * @param progName Name of the executable.
     */
    static void printUsage(const char* progName) {
        std::cout << "Usage: mpirun -np P " << progName << " [options]\n"
                  << "\nOptions:\n"
                  << "  --N <int>            Number of particles (default: 864)\n"
                  << "  --steps <int>        Number of timesteps (default: 100)\n"
                  << "  --dt <double>        Timestep (default: 1e-14)\n"
                  << "  --T <double>         Initial temperature [K] (default: 94.4)\n"
                  << "  --omega <double>     HO angular frequency (default: 1.0)\n"
                  << "  --integrator <str>   euler, rk4, verlet (default: verlet)\n"
                  << "  --mode <str>         ho, lj (default: lj)\n"
                  << "  --no-output          Disable CSV output\n"
                  << "  --seed <int>         RNG seed (default: 42)\n"
                  << "  --rescale-step <int> Step for single velocity rescale (default: disabled)\n"
                  << "  --timing             Enable timing mode (implies --no-output)\n"
                  << "  --gr                 Enable g(r) accumulation (LJ only)\n"
                  << "  --gr-discard <int>   Steps to discard after production_start before g(r) (default: 500)\n"
                  << "  --gr-interval <int>  Sample g(r) every N steps (default: 10)\n"
                  << "  --outdir <str>       Output directory for generated CSVs\n"
                  << "  --help               Print this message and exit\n";
    }
};

}  // namespace md

#endif  // MD_PARAMS_HPP
