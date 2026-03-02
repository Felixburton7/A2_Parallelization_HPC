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
    bool timing = false;                ///< Enable wall-clock timing (disables output)
    bool gr = false;                    ///< Enable g(r) accumulation
    int gr_discard = 500;               ///< Number of equilibration steps to discard before g(r)
    int gr_interval = 10;               ///< Sample g(r) every N steps after discard

    /**
     * @brief Parse command-line arguments into a Params struct.
     *
     * Supported flags:
     *   --N <int>          Number of particles
     *   --steps <int>      Number of timesteps
     *   --dt <double>      Timestep
     *   --T <double>       Initial temperature [K]
     *   --omega <double>   HO angular frequency
     *   --integrator <str> euler, rk4, verlet
     *   --mode <str>       ho, lj
     *   --no-output        Disable CSV output
     *   --seed <int>       RNG seed
     *   --rescale-step <int> Step for optional velocity rescale
     *   --timing           Enable timing mode (implies --no-output)
     *   --help             Print usage and exit
     *
     * @param argc Argument count
     * @param argv Argument values
     * @return Parsed Params struct
     */
    static Params parse(int argc, char* argv[]) {
        Params p;
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg == "--help") {
                printUsage(argv[0]);
                std::exit(0);
            } else if (arg == "--N" && i + 1 < argc) {
                p.N = std::atoi(argv[++i]);
            } else if (arg == "--steps" && i + 1 < argc) {
                p.steps = std::atoi(argv[++i]);
            } else if (arg == "--dt" && i + 1 < argc) {
                p.dt = std::atof(argv[++i]);
            } else if (arg == "--T" && i + 1 < argc) {
                p.T_init = std::atof(argv[++i]);
            } else if (arg == "--omega" && i + 1 < argc) {
                p.omega = std::atof(argv[++i]);
            } else if (arg == "--integrator" && i + 1 < argc) {
                p.integrator = argv[++i];
            } else if (arg == "--mode" && i + 1 < argc) {
                p.mode = argv[++i];
            } else if (arg == "--no-output") {
                p.output = false;
            } else if (arg == "--seed" && i + 1 < argc) {
                p.seed = std::atoi(argv[++i]);
            } else if (arg == "--rescale-step" && i + 1 < argc) {
                p.rescale_step = std::atoi(argv[++i]);
            } else if (arg == "--timing") {
                p.timing = true;
                p.output = false;
            } else if (arg == "--gr") {
                p.gr = true;
            } else if (arg == "--gr-discard" && i + 1 < argc) {
                p.gr_discard = std::atoi(argv[++i]);
            } else if (arg == "--gr-interval" && i + 1 < argc) {
                p.gr_interval = std::atoi(argv[++i]);
            } else {
                std::cerr << "Unknown argument: " << arg << "\n";
                printUsage(argv[0]);
                std::exit(1);
            }
        }
        return p;
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
            << "  --rescale-step <int> Step for optional velocity rescale (default: disabled)\n"
            << "  --timing             Enable timing mode (implies --no-output)\n"
            << "  --gr                 Enable g(r) accumulation (LJ only)\n"
            << "  --gr-discard <int>   Equilibration steps to discard (default: 500)\n"
            << "  --gr-interval <int>  Sample g(r) every N steps (default: 10)\n"
            << "  --help               Print this message and exit\n";
    }
};

}  // namespace md

#endif  // MD_PARAMS_HPP
