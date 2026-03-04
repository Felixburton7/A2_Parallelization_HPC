/**
 * @file system.hpp
 * @brief Particle system state using flat, interleaved std::vector<double> arrays.
 *
 * All kinematic variables (position, velocity, acceleration/force) are stored
 * as contiguous 1D interleaved arrays of size 3*localN. Access pattern:
 *   arr[3*i + d]  for local particle i, dimension d ∈ {0, 1, 2}
 *
 * This layout ensures cache-locality and maps directly to MPI_Allgatherv
 * buffer requirements, eliminating indexing translation errors.
 */

#ifndef MD_SYSTEM_HPP
#define MD_SYSTEM_HPP

#include <cmath>
#include <vector>

namespace md {

/**
 * @brief State of the local particle system on one MPI rank.
 */
struct System {
    int localN;  ///< Number of particles owned by this rank
    int offset;  ///< Starting global index for this rank's particles
    int N;       ///< Total number of particles (global)
    double L;    ///< Box side length [m]

    std::vector<double> pos;  ///< Local positions  [3*localN], interleaved (x,y,z,x,y,z,...)
    std::vector<double> vel;  ///< Local velocities  [3*localN], interleaved
    std::vector<double> acc;  ///< Local accelerations [3*localN], interleaved (a = F/m)

    /**
     * @brief Initialise system arrays for localN particles.
     *
     * @param ln   Number of local particles
     * @param off  Starting global index
     * @param totalN Total particles
     * @param boxL Box side length
     */
    void init(int ln, int off, int totalN, double boxL) {
        localN = ln;
        offset = off;
        N = totalN;
        L = boxL;

        pos.assign(3 * localN, 0.0);
        vel.assign(3 * localN, 0.0);
        acc.assign(3 * localN, 0.0);
    }

    /**
     * @brief Wrap all local positions into the canonical range [0, L).
     *
     * Prevents unbounded coordinate growth and floating-point precision loss.
     * Must be called after every drift (position update) step and before
     * the subsequent MPI_Allgatherv / force evaluation.
     */
    void wrapPositions() {
        double invL = 1.0 / L;
        for (int i = 0; i < 3 * localN; ++i) {
            pos[i] -= L * std::floor(pos[i] * invL);
        }
    }
};

}  // namespace md

#endif  // MD_SYSTEM_HPP
