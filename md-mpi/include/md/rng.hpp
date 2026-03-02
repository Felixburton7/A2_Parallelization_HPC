/**
 * @file rng.hpp
 * @brief FCC lattice construction and Box-Muller velocity initialisation.
 *
 * All random number generation uses std::mt19937_64 with a fixed seed,
 * executed ONLY on rank 0 for bitwise reproducibility across all MPI
 * configurations. Does NOT use rand() or std::rand().
 */

#ifndef MD_RNG_HPP
#define MD_RNG_HPP

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <vector>

#include "md/constants.hpp"

namespace md {

/**
 * @brief Construct an FCC lattice with N = 4k^3 particles in a cubic box.
 *
 * Four basis atoms per unit cell at fractional coordinates:
 *   (0.0, 0.0, 0.0), (0.5, 0.5, 0.0), (0.5, 0.0, 0.5), (0.0, 0.5, 0.5)
 *
 * A small random zero-mean perturbation (~0.01*sigma per coordinate) is
 * applied to break exact symmetry and prevent force singularities.
 *
 * @param N     Total number of particles (must be 4*k^3 for integer k)
 * @param L     Box side length [m]
 * @param seed  RNG seed for perturbation
 * @return      Flat interleaved position array of size 3*N
 */
inline std::vector<double> buildFCCLattice(int N, double L, int seed) {
    // Determine k such that N = 4*k^3
    int k = static_cast<int>(std::round(std::cbrt(N / 4.0)));

    // Validate: N must equal 4*k^3 for a valid FCC lattice
    if (4 * k * k * k != N) {
        std::fprintf(stderr,
                     "ERROR: N = %d is not a valid FCC particle count (need N = 4*k^3, "
                     "nearest k = %d gives N = %d)\n",
                     N, k, 4 * k * k * k);
        std::exit(1);
    }

    std::vector<double> positions(3 * N);

    // Unit cell side length
    double a = L / k;

    // FCC basis vectors (fractional coordinates)
    const double basis[4][3] = {{0.0, 0.0, 0.0}, {0.5, 0.5, 0.0}, {0.5, 0.0, 0.5}, {0.0, 0.5, 0.5}};

    // Perturbation magnitude (zero-mean uniform distribution)
    double pertMag = 0.01 * constants::sigma;
    std::mt19937_64 gen(seed);
    std::uniform_real_distribution<double> pertDist(-pertMag, pertMag);

    int idx = 0;
    for (int ix = 0; ix < k; ++ix) {
        for (int iy = 0; iy < k; ++iy) {
            for (int iz = 0; iz < k; ++iz) {
                for (int b = 0; b < 4; ++b) {
                    positions[3 * idx + 0] = (ix + basis[b][0]) * a + pertDist(gen);
                    positions[3 * idx + 1] = (iy + basis[b][1]) * a + pertDist(gen);
                    positions[3 * idx + 2] = (iz + basis[b][2]) * a + pertDist(gen);
                    ++idx;
                }
            }
        }
    }

    return positions;
}

/**
 * @brief Generate Maxwell-Boltzmann velocities using Box-Muller transform.
 *
 * Generates 3N velocity components from a Gaussian distribution with
 * standard deviation sigma_v = sqrt(k_B * T / m). Uses pairs of uniform
 * deviates to produce pairs of normal deviates via the Box-Muller method.
 *
 * After generation:
 *   1. Centre-of-mass drift is removed (subtract mean velocity)
 *   2. Velocities are rescaled to exactly match the target temperature
 *
 * @param N      Total number of particles
 * @param T      Target temperature [K]
 * @param mass   Particle mass [kg]
 * @param seed   RNG seed
 * @return       Flat interleaved velocity array of size 3*N
 */
inline std::vector<double> generateVelocities(int N, double T, double mass, int seed) {
    std::vector<double> vel(3 * N);

    double sigmaV = std::sqrt(constants::kB * T / mass);

    // Use a separate seed stream for velocities (offset from lattice seed)
    std::mt19937_64 gen(seed + 1000);
    std::uniform_real_distribution<double> uDist(0.0, 1.0);

    int totalComponents = 3 * N;

    // Box-Muller: generate pairs of normal deviates
    for (int i = 0; i < totalComponents; i += 2) {
        double u1, u2;
        // Ensure u1 > 0 to avoid log(0)
        do {
            u1 = uDist(gen);
        } while (u1 == 0.0);
        u2 = uDist(gen);

        double mag = sigmaV * std::sqrt(-2.0 * std::log(u1));
        double z1 = mag * std::cos(2.0 * constants::pi * u2);
        double z2 = mag * std::sin(2.0 * constants::pi * u2);

        vel[i] = z1;
        if (i + 1 < totalComponents) {
            vel[i + 1] = z2;
        }
    }

    // Remove centre-of-mass drift
    double vxMean = 0.0, vyMean = 0.0, vzMean = 0.0;
    for (int i = 0; i < N; ++i) {
        vxMean += vel[3 * i + 0];
        vyMean += vel[3 * i + 1];
        vzMean += vel[3 * i + 2];
    }
    vxMean /= N;
    vyMean /= N;
    vzMean /= N;

    for (int i = 0; i < N; ++i) {
        vel[3 * i + 0] -= vxMean;
        vel[3 * i + 1] -= vyMean;
        vel[3 * i + 2] -= vzMean;
    }

    // Rescale to exact target temperature: lambda = sqrt(T_target / T_measured)
    // T_measured = (2 / (N_dof * kB)) * E_kin, where N_dof = 3*(N-1)
    double eKin = 0.0;
    for (int i = 0; i < 3 * N; ++i) {
        eKin += vel[i] * vel[i];
    }
    eKin *= 0.5 * mass;

    int nDof = 3 * (N - 1);  // degrees of freedom after CoM removal
    double tMeasured = (2.0 * eKin) / (nDof * constants::kB);
    double lambda = std::sqrt(T / tMeasured);

    for (int i = 0; i < 3 * N; ++i) {
        vel[i] *= lambda;
    }

    return vel;
}

}  // namespace md

#endif  // MD_RNG_HPP
