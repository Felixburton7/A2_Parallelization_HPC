/**
 * @file euler.cpp
 * @brief Forward Euler integrator (AMM Handout Eqn 4.27).
 *
 * Position update: x_{n+1} = x_n + v_n * dt + 0.5 * a_n * dt^2
 *   (2nd-order Taylor expansion for position)
 * Velocity update: v_{n+1} = v_n + a_n * dt
 *   (1st-order for velocity — global error bottleneck)
 *
 * MPI sequence (v4 lock-in):
 *   1. Drift:  x_{n+1} = x_n + v_n * dt + 0.5 * a_n * dt^2
 *   2. Vel:    v_{n+1} = v_n + a_n * dt
 *   3. Wrap:   x into [0, L)
 *   4. Gather: MPI_Allgatherv (skipped for HO mode)
 *   5. Force:  Compute a_{n+1} for next timestep
 */

#include "md/integrators.hpp"

namespace md {

void stepEuler(System& sys, MPIContext& ctx, double dt, ForceFunc forceFunc, double& localPE,
               bool isHO) {
    const int n3 = 3 * sys.localN;

    // Step 1: Drift — x_{n+1} = x_n + v_n * dt + 0.5 * a_n * dt^2
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] += sys.vel[i] * dt + 0.5 * sys.acc[i] * dt * dt;
    }

    // Step 2: Velocity update — v_{n+1} = v_n + a_n * dt
    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += sys.acc[i] * dt;
    }

    // Step 3: Wrap positions into [0, L) (LJ only — wrapping corrupts HO oscillation)
    if (!isHO) {
        sys.wrapPositions();
    }

    // Step 4: Gather global positions (skipped for HO — no inter-particle interaction)
    if (!isHO) {
        ctx.allgatherPositions(sys.pos);
    }

    // Step 5: Compute forces from updated positions (a_{n+1} for next step)
    forceFunc(sys, ctx.posGlobal, localPE);
}

}  // namespace md
