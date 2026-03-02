/**
 * @file rk4.cpp
 * @brief 4th-order Runge-Kutta integrator.
 *
 * Reformulates the 2nd-order ODE as a first-order system:
 *   y = (x, v)^T,  f(y) = (v, a(x))^T
 *
 * Standard RK4 stages:
 *   k1 = dt * f(y_n)
 *   k2 = dt * f(y_n + k1/2)
 *   k3 = dt * f(y_n + k2/2)
 *   k4 = dt * f(y_n + k3)
 *   y_{n+1} = y_n + (k1 + 2*k2 + 2*k3 + k4) / 6
 *
 * Requires 4 force evaluations per step. Only used for HO verification.
 * Impractical for parallel LJ due to 4 MPI_Allgatherv calls per timestep.
 */

#include "md/integrators.hpp"

namespace md {

void stepRK4(System& sys, MPIContext& ctx, double dt, ForceFunc forceFunc, double& localPE,
             bool isHO) {
    const int n3 = 3 * sys.localN;

    // Save initial state
    std::vector<double> x0(sys.pos);
    std::vector<double> v0(sys.vel);

    // ── Stage 1: k1 = dt * f(y_n) ──
    // Forces already computed from previous step (stored in sys.acc)
    std::vector<double> k1x(n3), k1v(n3);
    for (int i = 0; i < n3; ++i) {
        k1x[i] = dt * sys.vel[i];  // dx/dt = v
        k1v[i] = dt * sys.acc[i];  // dv/dt = a(x)
    }

    // ── Stage 2: k2 = dt * f(y_n + k1/2) ──
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] = x0[i] + 0.5 * k1x[i];
        sys.vel[i] = v0[i] + 0.5 * k1v[i];
    }
    if (!isHO)
        sys.wrapPositions();
    if (!isHO)
        ctx.allgatherPositions(sys.pos);
    forceFunc(sys, ctx.posGlobal, localPE);

    std::vector<double> k2x(n3), k2v(n3);
    for (int i = 0; i < n3; ++i) {
        k2x[i] = dt * sys.vel[i];
        k2v[i] = dt * sys.acc[i];
    }

    // ── Stage 3: k3 = dt * f(y_n + k2/2) ──
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] = x0[i] + 0.5 * k2x[i];
        sys.vel[i] = v0[i] + 0.5 * k2v[i];
    }
    if (!isHO)
        sys.wrapPositions();
    if (!isHO)
        ctx.allgatherPositions(sys.pos);
    forceFunc(sys, ctx.posGlobal, localPE);

    std::vector<double> k3x(n3), k3v(n3);
    for (int i = 0; i < n3; ++i) {
        k3x[i] = dt * sys.vel[i];
        k3v[i] = dt * sys.acc[i];
    }

    // ── Stage 4: k4 = dt * f(y_n + k3) ──
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] = x0[i] + k3x[i];
        sys.vel[i] = v0[i] + k3v[i];
    }
    if (!isHO)
        sys.wrapPositions();
    if (!isHO)
        ctx.allgatherPositions(sys.pos);
    forceFunc(sys, ctx.posGlobal, localPE);

    std::vector<double> k4x(n3), k4v(n3);
    for (int i = 0; i < n3; ++i) {
        k4x[i] = dt * sys.vel[i];
        k4v[i] = dt * sys.acc[i];
    }

    // ── Combine: y_{n+1} = y_n + (k1 + 2*k2 + 2*k3 + k4) / 6 ──
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] = x0[i] + (k1x[i] + 2.0 * k2x[i] + 2.0 * k3x[i] + k4x[i]) / 6.0;
        sys.vel[i] = v0[i] + (k1v[i] + 2.0 * k2v[i] + 2.0 * k3v[i] + k4v[i]) / 6.0;
    }

    // Wrap final positions (LJ only)
    if (!isHO)
        sys.wrapPositions();

    // Recompute forces at final state
    if (!isHO)
        ctx.allgatherPositions(sys.pos);
    forceFunc(sys, ctx.posGlobal, localPE);
}

}  // namespace md
