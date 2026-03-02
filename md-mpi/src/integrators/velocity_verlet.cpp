/**
 * @file velocity_verlet.cpp
 * @brief Velocity-Verlet integrator (half-kick / drift / half-kick form).
 *
 * MPI-aware sequence (v4 lock-in, §2.3):
 *   Step 1 (half-kick):  v_{n+1/2} = v_n + 0.5 * a_n * dt
 *   Step 2 (drift):      x_{n+1}   = x_n + v_{n+1/2} * dt
 *   Step 3 (wrap):       Wrap x into [0, L)
 *   Step 4 (gather):     MPI_Allgatherv to sync global positions
 *   Step 5 (force eval): Compute a_{n+1} from global positions
 *   Step 6 (half-kick):  v_{n+1}   = v_{n+1/2} + 0.5 * a_{n+1} * dt
 *
 * The Allgatherv is placed immediately after the position update and
 * wrap, but before the force evaluation, to guarantee that all ranks
 * compute forces against a consistent, globally-synchronised snapshot.
 *
 * Global truncation error: O(dt^2). Symplectic and time-reversible.
 */

#include "md/integrators.hpp"

namespace md {

void stepVelocityVerlet(System& sys, MPIContext& ctx, double dt, ForceFunc forceFunc,
                        double& localPE, bool isHO) {
    const int n3 = 3 * sys.localN;
    const double halfDt = 0.5 * dt;

    // Step 1: Half-kick — v_{n+1/2} = v_n + 0.5 * a_n * dt
    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += halfDt * sys.acc[i];
    }

    // Step 2: Drift — x_{n+1} = x_n + v_{n+1/2} * dt
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] += dt * sys.vel[i];
    }

    // Step 3: Wrap positions into [0, L) (LJ only — wrapping corrupts HO oscillation)
    if (!isHO) {
        sys.wrapPositions();
    }

    // Step 4: Gather global positions (skipped for HO — no inter-particle interaction)
    if (!isHO) {
        ctx.allgatherPositions(sys.pos);
    }

    // Step 5: Compute forces from updated positions
    forceFunc(sys, ctx.posGlobal, localPE);

    // Step 6: Half-kick — v_{n+1} = v_{n+1/2} + 0.5 * a_{n+1} * dt
    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += halfDt * sys.acc[i];
    }
}

}  // namespace md
