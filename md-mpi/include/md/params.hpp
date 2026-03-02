/**
 * @file params.hpp
 * @brief Runtime parameter struct and CLI argument parser.
 *
 * All simulation parameters are configurable via command-line arguments.
 * No recompilation is needed to change N, dt, integrator, etc.
 *
 * The parser never calls std::exit() — it returns a ParseStatus so the
 * caller can handle MPI_Finalize() cleanly before exiting.
 */

#ifndef MD_PARAMS_HPP
#define MD_PARAMS_HPP

#include <cstdlib>
#include <iostream>
#include <string>

namespace md {

/// Parse result status (avoids std::exit before MPI_Finalize).
enum class ParseStatus { Ok, Help, Error };

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
    int rescale_step = -1;              ///< Step at which to apply optional rescale (-1 = disabled)
    int rescale_freq = 0;               ///< Rescale every N steps during equilibration (0 = off)
    int rescale_end = 0;                ///< Stop rescaling after this step (0 = off)
    bool timing = false;                ///< Enable wall-clock timing (disables output)
    bool gr = false;                    ///< Enable g(r) accumulation
    int gr_discard = 500;               ///< Number of equilibration steps to discard before g(r)
    int gr_interval = 10;               ///< Sample g(r) every N steps after discard

    /**
     * @brief Parse command-line arguments into a Params struct.
     *
     * Does NOT call std::exit(). Returns a ParseStatus so the caller
     * can call MPI_Finalize() before exiting.
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
                return ParseStatus::Help;
            } else if (arg == "--N") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --N\n";
                    return ParseStatus::Error;
                }
                p.N = std::atoi(argv[++i]);
            } else if (arg == "--steps") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --steps\n";
                    return ParseStatus::Error;
                }
                p.steps = std::atoi(argv[++i]);
            } else if (arg == "--dt") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --dt\n";
                    return ParseStatus::Error;
                }
                p.dt = std::atof(argv[++i]);
            } else if (arg == "--T") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --T\n";
                    return ParseStatus::Error;
                }
                p.T_init = std::atof(argv[++i]);
            } else if (arg == "--omega") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --omega\n";
                    return ParseStatus::Error;
                }
                p.omega = std::atof(argv[++i]);
            } else if (arg == "--integrator") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --integrator\n";
                    return ParseStatus::Error;
                }
                p.integrator = argv[++i];
            } else if (arg == "--mode") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --mode\n";
                    return ParseStatus::Error;
                }
                p.mode = argv[++i];
            } else if (arg == "--no-output") {
                p.output = false;
            } else if (arg == "--seed") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --seed\n";
                    return ParseStatus::Error;
                }
                p.seed = std::atoi(argv[++i]);
            } else if (arg == "--rescale-step") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --rescale-step\n";
                    return ParseStatus::Error;
                }
                p.rescale_step = std::atoi(argv[++i]);
            } else if (arg == "--rescale-freq") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --rescale-freq\n";
                    return ParseStatus::Error;
                }
                p.rescale_freq = std::atoi(argv[++i]);
            } else if (arg == "--rescale-end") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --rescale-end\n";
                    return ParseStatus::Error;
                }
                p.rescale_end = std::atoi(argv[++i]);
            } else if (arg == "--timing") {
                p.timing = true;
                p.output = false;
            } else if (arg == "--gr") {
                p.gr = true;
            } else if (arg == "--gr-discard") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --gr-discard\n";
                    return ParseStatus::Error;
                }
                p.gr_discard = std::atoi(argv[++i]);
            } else if (arg == "--gr-interval") {
                if (i + 1 >= argc) {
                    std::cerr << "Missing value for --gr-interval\n";
                    return ParseStatus::Error;
                }
                p.gr_interval = std::atoi(argv[++i]);
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
        std::cout
            << "Usage: mpirun -np P " << progName << " [options]\n"
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
            << "  --rescale-freq <int> Rescale every N steps during equilibration (default: 0 = "
               "off)\n"
            << "  --rescale-end <int>  Stop continuous rescaling after this step (default: 0)\n"
            << "  --timing             Enable timing mode (implies --no-output)\n"
            << "  --gr                 Enable g(r) accumulation (LJ only)\n"
            << "  --gr-discard <int>   Equilibration steps to discard (default: 500)\n"
            << "  --gr-interval <int>  Sample g(r) every N steps (default: 10)\n"
            << "  --help               Print this message and exit\n";
    }
};

}  // namespace md

#endif  // MD_PARAMS_HPP
