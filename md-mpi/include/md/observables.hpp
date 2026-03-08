/**
 * @file observables.hpp
 * @brief Thermodynamic observables: energy, temperature, and g(r).
 */

#ifndef MD_OBSERVABLES_HPP
#define MD_OBSERVABLES_HPP

#include <cmath>
#include <vector>

#include "md/constants.hpp"
#include "md/system.hpp"

namespace md {

/**
 * @brief Compute local kinetic energy for this rank's particles.
 *
 * E_kin_local = 0.5 * m * sum_i |v_i|^2
 *
 * Must be followed by MPI_Reduce(MPI_SUM) to rank 0 for the global total.
 *
 * @param sys   System state (reads velocities)
 * @param mass  Particle mass [kg]
 * @return      Local kinetic energy [J]
 */
double computeLocalKineticEnergy(const System& sys, double mass);

/**
 * @brief Compute temperature from total kinetic energy.
 *
 * T = (2 / (N_dof * k_B)) * E_kin_total
 *
 * Uses N_dof = 3*(N-1) (after CoM drift removal) for thermodynamic accuracy.
 * The difference from 3*N is <0.35% for N=864.
 *
 * @param eKinTotal Total kinetic energy (from MPI_Reduce) [J]
 * @param N         Total number of particles
 * @return          Instantaneous temperature [K]
 */
double computeTemperature(double eKinTotal, int N);

// NOTE: Velocity rescaling is performed directly in main.cpp using
// computeTemperature() + MPI_Bcast(lambda) for MPI-correct thermostatting.
// No standalone rescaleVelocities() helper — avoids duplication.

/**
 * @brief Accumulate pair distances into a g(r) histogram.
 *
 * Uses unordered pairs (i < j) from this rank's local particles against
 * all global particles. Bin width = dr, range [0, rMax).
 * The result must be reduced via MPI_Reduce(MPI_SUM) across all ranks,
 * then normalised by the ideal gas shell volume and number of frames.
 *
 * @param posGlobal  Global positions (3*N doubles)
 * @param N          Total number of particles
 * @param L          Box side length
 * @param offset     Starting global index for this rank
 * @param localN     Number of local particles
 * @param dr         Bin width
 * @param rMax       Maximum distance to bin
 * @param histogram  Output histogram (must be pre-sized)
 */
void accumulateGR(const std::vector<double>& posGlobal, int N, double L, int offset, int localN,
                  double dr, double rMax, std::vector<double>& histogram);

/**
 * @brief Normalise the accumulated g(r) histogram.
 *
 * Since we count unordered pairs (i < j), each pair appears exactly once.
 * The standard formula uses ordered pairs (factor of N*(N-1) total), so we
 * multiply by 2 to compensate:
 *   g(r) = 2 * count / (rho * N * 4*pi*r^2 * dr * nFrames)
 *
 * @param histogram  Accumulated histogram (modified in-place to g(r))
 * @param dr         Bin width
 * @param N          Total number of particles
 * @param L          Box side length
 * @param nFrames    Number of frames accumulated
 */
void normaliseGR(std::vector<double>& histogram, double dr, int N, double L, int nFrames);

}  // namespace md

#endif  // MD_OBSERVABLES_HPP
