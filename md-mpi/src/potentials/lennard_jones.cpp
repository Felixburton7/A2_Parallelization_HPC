/**
 * @file lennard_jones.cpp
 * @brief Lennard-Jones force/energy kernel with optimised intermediates.
 *
 * Uses the shared-intermediate approach (no pow, no sqrt in the force loop):
 *   inv_r2 → inv_r6 → inv_r12
 *
 * Applies branch-predictor-friendly minimum image convention and hard
 * cutoff at rcut = 2.25*sigma.
 *
 * Potential energy is accumulated unconditionally for all j != i (no i<j
 * branch in the inner loop). The local sum is multiplied by 0.5 AFTER
 * the loop to correct for double-counting, guaranteeing pipeline
 * efficiency on superscalar CPUs.
 */

#include "md/constants.hpp"
#include "md/potentials.hpp"

namespace md {

void computeLJForces(System& sys, const std::vector<double>& posGlobal, double& localPE,
                     double mass) {
    const double L = sys.L;
    const double halfL = 0.5 * L;
    const int N = sys.N;
    const int offset = sys.offset;
    const int localN = sys.localN;

    // Pre-computed constants (from constants.hpp)
    const double s6 = constants::sigma6;
    const double s12 = constants::sigma12;
    const double fe = constants::four_eps;
    const double te = constants::twentyfour_eps;
    const double rc2 = constants::rcut2;
    const double inv_mass = 1.0 / mass;

    // Zero local forces and PE
    for (int i = 0; i < 3 * localN; ++i) {
        sys.acc[i] = 0.0;
    }
    localPE = 0.0;

    for (int i = 0; i < localN; ++i) {
        int gi = offset + i;  // global index

        double xi = posGlobal[3 * gi + 0];
        double yi = posGlobal[3 * gi + 1];
        double zi = posGlobal[3 * gi + 2];

        double fx = 0.0, fy = 0.0, fz = 0.0;
        double pei = 0.0;

        for (int j = 0; j < N; ++j) {
            // Skip self-interaction to avoid r^2 = 0 singularity
            if (j == gi)
                continue;

            double dx = xi - posGlobal[3 * j + 0];
            double dy = yi - posGlobal[3 * j + 1];
            double dz = zi - posGlobal[3 * j + 2];

            // Branch-predictor-friendly MIC (avoids std::round overhead in O(N^2) loop)
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

            double r2 = dx * dx + dy * dy + dz * dz;

            if (r2 >= rc2)
                continue;  // hard cutoff

            double inv_r2 = 1.0 / r2;
            double inv_r6 = inv_r2 * inv_r2 * inv_r2;
            double inv_r12 = inv_r6 * inv_r6;

            // Potential energy (accumulate unconditionally — multiply by 0.5 after loop)
            pei += fe * (s12 * inv_r12 - s6 * inv_r6);

            // Force scalar: f/r = 24*eps/r^2 * [2*(sigma/r)^12 - (sigma/r)^6]
            double fScalar = te * inv_r2 * (2.0 * s12 * inv_r12 - s6 * inv_r6);

            fx += fScalar * dx;
            fy += fScalar * dy;
            fz += fScalar * dz;
        }

        // Store as acceleration: a = F/m
        sys.acc[3 * i + 0] = fx * inv_mass;
        sys.acc[3 * i + 1] = fy * inv_mass;
        sys.acc[3 * i + 2] = fz * inv_mass;

        localPE += pei;
    }

    // Correct for double-counting: each pair (i,j) counted once from i's side
    // and once from j's side, so multiply by 0.5
    localPE *= 0.5;
}

}  // namespace md
