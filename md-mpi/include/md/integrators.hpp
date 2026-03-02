/**
 * @file integrators.hpp
 * @brief Forward Euler (AMM Eqn 4.27), RK4, and Velocity-Verlet integrators.
 *
 * Each integrator advances the system state by one timestep, including:
 *   - Position/velocity updates
 *   - Position wrapping into [0, L)
 *   - MPI_Allgatherv for global position synchronisation (LJ mode only)
 *   - Force recomputation from updated positions
 *
 * The MPI_Allgatherv placement follows §2.3 of the project charter:
 *   Velocity-Verlet: half-kick → drift → wrap → Allgatherv → force → half-kick
 *   Euler:           drift → vel update → wrap → Allgatherv → force (for next step)
 */

#ifndef MD_INTEGRATORS_HPP
#define MD_INTEGRATORS_HPP

#include <functional>
#include <string>
#include <vector>

#include "md/mpi_context.hpp"
#include "md/system.hpp"

namespace md {

/// Force computation function signature
using ForceFunc = std::function<void(System&, const std::vector<double>&, double&)>;

/**
 * @brief Forward Euler integrator (AMM Handout Eqn 4.27).
 *
 * Position update: x_{n+1} = x_n + v_n * dt + 0.5 * a_n * dt^2
 *   (2nd-order Taylor expansion for position)
 * Velocity update: v_{n+1} = v_n + a_n * dt
 *   (1st-order for velocity — this is the global error bottleneck)
 *
 * Global truncation error: O(dt). NOT symplectic. Energy drifts.
 *
 * MPI sequence: drift → vel update → wrap → Allgatherv → force (for next step)
 *
 * @param sys        System state
 * @param ctx        MPI context (for Allgatherv)
 * @param dt         Timestep
 * @param forceFunc  Force computation function
 * @param localPE    Output: local potential energy
 * @param isHO       If true, skip MPI_Allgatherv (HO communication bypass)
 */
void stepEuler(System& sys, MPIContext& ctx, double dt, ForceFunc forceFunc, double& localPE,
               bool isHO);

/**
 * @brief RK4 integrator (classical 4th-order Runge-Kutta).
 *
 * Reformulates the 2nd-order ODE as a first-order system:
 *   y = (x, v)^T,  f(y) = (v, a(x))^T
 *
 * Applies standard RK4 stages (k1, k2, k3, k4) and combines them
 * with the 1/6 weighting.
 *
 * Global truncation error: O(dt^4). NOT symplectic.
 * Requires 4 force evaluations per step.
 *
 * NOTE: Only used for HO verification. Impractical for LJ production
 * due to 4 MPI_Allgatherv calls per timestep.
 *
 * @param sys        System state
 * @param ctx        MPI context (for Allgatherv, if needed)
 * @param dt         Timestep
 * @param forceFunc  Force computation function
 * @param localPE    Output: local potential energy
 * @param isHO       If true, skip MPI_Allgatherv (HO communication bypass)
 */
void stepRK4(System& sys, MPIContext& ctx, double dt, ForceFunc forceFunc, double& localPE,
             bool isHO);

/**
 * @brief Velocity-Verlet integrator (half-kick / drift / half-kick form).
 *
 * Step 1 (half-kick):  v_{n+1/2} = v_n + 0.5 * a_n * dt
 * Step 2 (drift):      x_{n+1}   = x_n + v_{n+1/2} * dt
 * Step 3 (wrap):       Wrap x into [0, L)
 * Step 4 (gather):     MPI_Allgatherv to sync global positions
 * Step 5 (force eval): Compute a_{n+1} from global positions
 * Step 6 (half-kick):  v_{n+1}   = v_{n+1/2} + 0.5 * a_{n+1} * dt
 *
 * Global truncation error: O(dt^2). Symplectic and time-reversible.
 * Energy oscillates with bounded fluctuations (no drift).
 *
 * @param sys        System state
 * @param ctx        MPI context (for Allgatherv)
 * @param dt         Timestep
 * @param forceFunc  Force computation function
 * @param localPE    Output: local potential energy
 * @param isHO       If true, skip MPI_Allgatherv (HO communication bypass)
 */
void stepVelocityVerlet(System& sys, MPIContext& ctx, double dt, ForceFunc forceFunc,
                        double& localPE, bool isHO);

}  // namespace md

#endif  // MD_INTEGRATORS_HPP
