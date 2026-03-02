/**
 * @file potentials.hpp
 * @brief Harmonic Oscillator and Lennard-Jones force/energy kernels.
 *
 * Both potentials implement a common interface:
 *   computeForces(system, posGlobal, localPE)
 *
 * The HO potential computes F = -omega^2 * x purely locally, ignoring
 * the global position data. The LJ potential uses the global positions
 * from MPI_Allgatherv with minimum image convention and hard cutoff.
 */

#ifndef MD_POTENTIALS_HPP
#define MD_POTENTIALS_HPP

#include <vector>

#include "md/system.hpp"

namespace md {

/**
 * @brief Compute harmonic oscillator forces for local particles.
 *
 * F_i = -omega^2 * x_i  (independent, non-interacting particles)
 *
 * This kernel operates purely on local data and does NOT require any
 * global position information. The MPI_Allgatherv call should be
 * bypassed entirely in HO mode to eliminate unnecessary O(N)
 * communication overhead.
 *
 * @param[in,out] sys       System state (forces written to sys.acc)
 * @param[in]     posGlobal Ignored for HO (may be empty)
 * @param[out]    localPE   Local potential energy contribution
 * @param[in]     omega     Angular frequency
 * @param[in]     mass      Particle mass [kg]
 */
void computeHOForces(System& sys, const std::vector<double>& posGlobal, double& localPE,
                     double omega, double mass);

/**
 * @brief Compute Lennard-Jones forces for local particles against all particles.
 *
 * Uses the optimised kernel with shared intermediates (no pow, no sqrt).
 * Applies branch-predictor-friendly minimum image convention and hard
 * cutoff at rcut. Accumulates potential energy unconditionally for all
 * j != i; the local sum is multiplied by 0.5 AFTER the loop to correct
 * for double-counting.
 *
 * Force formula (Rahman Appendix, brief Eqn 3):
 *   a_i = (24*eps/m) * sum_{j!=i} (x_i - x_j)/r^2_ij
 *         * [2*(sigma/r_ij)^12 - (sigma/r_ij)^6]
 *
 * @param[in,out] sys       System state (forces written to sys.acc)
 * @param[in]     posGlobal Global positions (3*N doubles, from Allgatherv)
 * @param[out]    localPE   Local PE contribution (pre-halved for this rank's pairs)
 * @param[in]     mass      Particle mass [kg]
 */
void computeLJForces(System& sys, const std::vector<double>& posGlobal, double& localPE,
                     double mass);

}  // namespace md

#endif  // MD_POTENTIALS_HPP
