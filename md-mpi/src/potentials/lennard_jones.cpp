/**
 * @file lennard_jones.cpp
 * @brief Lennard-Jones force and potential energy kernel.
 *
 * Implements U(r) = 4*eps*[(sigma/r)^12 - (sigma/r)^6] via
 * invR2 → invR6 → invR12 (no pow, no sqrt in force loop).
 *
 * Hard cutoff at rcut = 2.25*sigma with round-based minimum image convention.
 * PE is summed over all j != i (both directions) and multiplied by 0.5
 * after the loop to correct for double-counting.
 */

#include <cmath>

#include "md/constants.hpp"
#include "md/mic.hpp"
#include "md/potentials.hpp"

namespace md {

void computeLJForces(System& sys, const std::vector<double>& posGlobal, double& localPE,
                     double mass) {
    const double L = sys.L;
    const int N = sys.N;
    const int offset = sys.offset;
    const int localN = sys.localN;

    // Pre-computed constants (from constants.hpp)
    const double s6 = constants::sigma6;
    const double s12 = constants::sigma12;
    const double fe = constants::four_eps;
    const double te = constants::twentyfour_eps;
    const double rc2 = constants::rcut2;
    const double tiny = 1e-30 * constants::sigma2;
    const double invMass = 1.0 / mass;

    // Zero local forces and PE
    for (int i = 0; i < 3 * localN; ++i) {
        sys.acc[i] = 0.0;
    }
    localPE = 0.0;
    for (int i = 0; i < localN; ++i) {
        int gi = offset + i;  // global index

        // Local particle from sys.pos; remote particles from posGlobal
        double xi = sys.pos[3 * i + 0];
        double yi = sys.pos[3 * i + 1];
        double zi = sys.pos[3 * i + 2];

        double fx = 0.0, fy = 0.0, fz = 0.0;
        double pei = 0.0;

        for (int j = 0; j < N; ++j) {
            // Skip self-interaction to avoid r^2 = 0 singularity
            if (j == gi)
                continue;

            double dx = xi - posGlobal[3 * j + 0];
            double dy = yi - posGlobal[3 * j + 1];
            double dz = zi - posGlobal[3 * j + 2];

            // Minimum image convention
            dx = md::applyMIC(dx, L);
            dy = md::applyMIC(dy, L);
            dz = md::applyMIC(dz, L);

            double r2 = dx * dx + dy * dy + dz * dz;

            if (r2 < tiny)
                continue;

            if (r2 >= rc2)
                continue;  // hard cutoff

            double invR2 = 1.0 / r2;
            double invR6 = invR2 * invR2 * invR2;
            double invR12 = invR6 * invR6;

            // Potential energy (accumulate unconditionally — multiply by 0.5 after loop)
            pei += fe * (s12 * invR12 - s6 * invR6);

            // Force scalar: f/r = 24*eps/r^2 * [2*(sigma/r)^12 - (sigma/r)^6]
            double fScalar = te * invR2 * (2.0 * s12 * invR12 - s6 * invR6);

            fx += fScalar * dx;
            fy += fScalar * dy;
            fz += fScalar * dz;
        }

        // Store as acceleration: a = F/m
        sys.acc[3 * i + 0] = fx * invMass;
        sys.acc[3 * i + 1] = fy * invMass;
        sys.acc[3 * i + 2] = fz * invMass;

        localPE += pei;
    }

    // Each rank loops its local particles i against all N particles j≠i, accumulating V(r_ij).
    // Across all ranks, every ordered pair (i,j) with j≠i is visited exactly once. Since V(r_ij) =
    // V(r_ji), this double-counts each unordered pair, so halve.
    localPE *= 0.5;
}

}  // namespace md
