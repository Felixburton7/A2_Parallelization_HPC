/**
 * @file observables.hpp
 * @brief Thermodynamic observables: energies, temperature, g(r) binning.
 *
 * Provides functions for computing kinetic energy (local), measuring
 * temperature from the equipartition theorem, and accumulating the
 * radial distribution function g(r) histogram.
 */

#ifndef MD_OBSERVABLES_HPP
#define MD_OBSERVABLES_HPP

#include <cmath>
#include <cstdio>
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
inline double computeLocalKineticEnergy(const System& sys, double mass) {
    double eKin = 0.0;
    for (int i = 0; i < 3 * sys.localN; ++i) {
        eKin += sys.vel[i] * sys.vel[i];
    }
    return 0.5 * mass * eKin;
}

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
inline double computeTemperature(double eKinTotal, int N) {
    int nDof = 3 * (N - 1);  // degrees of freedom after CoM removal
    return (2.0 * eKinTotal) / (nDof * constants::kB);
}

/**
 * @brief Rescale velocities to match a target temperature.
 *
 * Computes lambda = sqrt(T_target / T_measured) and scales all velocity
 * components by this factor. Records the scaling factor to stdout for
 * traceability.
 *
 * @param sys        System state (velocities modified in-place)
 * @param mass       Particle mass [kg]
 * @param tTarget    Target temperature [K]
 * @param eKinTotal  Total kinetic energy (from MPI_Reduce) [J]
 * @param N          Total number of particles
 * @param step       Current timestep (for logging)
 * @param rank       MPI rank (only rank 0 logs)
 */
inline void rescaleVelocities(System& sys, double /*mass*/, double tTarget, double eKinTotal, int N,
                              int step, int rank) {
    double tMeasured = computeTemperature(eKinTotal, N);
    if (tMeasured < 1e-30)
        return;  // avoid division by zero
    double lambda = std::sqrt(tTarget / tMeasured);

    for (int i = 0; i < 3 * sys.localN; ++i) {
        sys.vel[i] *= lambda;
    }

    if (rank == 0) {
        std::printf("Rescale at step %d: lambda = %.15e, T_before = %.6f K, T_after = %.6f K\n",
                    step, lambda, tMeasured, tTarget);
    }
}

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
inline void accumulateGR(const std::vector<double>& posGlobal, int N, double L, int offset,
                         int localN, double dr, double rMax, std::vector<double>& histogram) {
    double halfL = 0.5 * L;
    int nBins = static_cast<int>(histogram.size());

    for (int i = offset; i < offset + localN; ++i) {
        for (int j = i + 1; j < N; ++j) {
            double dx = posGlobal[3 * i + 0] - posGlobal[3 * j + 0];
            double dy = posGlobal[3 * i + 1] - posGlobal[3 * j + 1];
            double dz = posGlobal[3 * i + 2] - posGlobal[3 * j + 2];

            // Minimum image convention (branch-predictor friendly)
            if (dx > halfL)
                dx -= L;
            else if (dx < -halfL)
                dx += L;
            if (dy > halfL)
                dy -= L;
            else if (dy < -halfL)
                dy += L;
            if (dz > halfL)
                dz -= L;
            else if (dz < -halfL)
                dz += L;

            double r = std::sqrt(dx * dx + dy * dy + dz * dz);
            if (r < rMax) {
                int bin = static_cast<int>(r / dr);
                if (bin < nBins) {
                    histogram[bin] += 1.0;
                }
            }
        }
    }
}

/**
 * @brief Normalise the accumulated g(r) histogram.
 *
 * Uses the unordered-pair formula:
 *   g(r) = (1 / (rho * N)) * n(r, r+dr) / (4 * pi * r^2 * dr * nFrames)
 *
 * @param histogram  Accumulated histogram (modified in-place to g(r))
 * @param dr         Bin width
 * @param N          Total number of particles
 * @param L          Box side length
 * @param nFrames    Number of frames accumulated
 */
inline void normaliseGR(std::vector<double>& histogram, double dr, int N, double L, int nFrames) {
    double V = L * L * L;
    double rho = N / V;

    for (int bin = 0; bin < static_cast<int>(histogram.size()); ++bin) {
        double rLow = bin * dr;
        double rMid = rLow + 0.5 * dr;
        double shellVol = 4.0 * constants::pi * rMid * rMid * dr;

        // Normalise: (1 / (rho * N)) * count / (shellVol * nFrames)
        if (shellVol > 0.0 && nFrames > 0) {
            histogram[bin] /= (rho * N * shellVol * nFrames);
        }
    }
}

}  // namespace md

#endif  // MD_OBSERVABLES_HPP
