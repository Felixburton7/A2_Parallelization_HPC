/**
 * @file integrators.hpp
 * @brief Forward Euler, RK4, and Velocity-Verlet integrators.
 */

#ifndef MD_INTEGRATORS_HPP
#define MD_INTEGRATORS_HPP

#include <vector>

#include "md/system.hpp"

namespace md {

/**
 * @brief Advance one time-step with the Forward Euler method.
 *
 * For
 *   dx/dt = v,   dv/dt = a(x),
 * Euler uses
 *   x_{n+1} = x_n + dt * v_n,
 *   v_{n+1} = v_n + dt * a_n.
 *
 * This is first-order accurate. It is simple, but for MD it is not
 * time-reversible or symplectic, so  often shows energy drift.
 */
template <typename RefreshForceFn>
inline void stepEuler(System& sys, double dt, RefreshForceFn refreshForces) {
    const int n3 = 3 * sys.localN;

    // x_{n+1} = x_n + dt * v_n
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] += sys.vel[i] * dt;
    }

    // v_{n+1} = v_n + dt * a_n
    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += sys.acc[i] * dt;
    }

    // Update forces/accelerations at the new positions.
    refreshForces();
}

/**
 * @brief Advance one time-step with classical fourth-order Runge-Kutta.
 *
 * RK4 combines four stages as
 *   y_{n+1} = y_n + (k1 + 2k2 + 2k3 + k4)/6,
 * where y = (x, v) and
 *   dx/dt = v,   dv/dt = a(x).
 *
 * RK4 is fourth-order accurate and works well for short-time trajectory
 * accuracy, but it is not symplectic, so less suitable for long MD runs
 * than Velocity-Verlet .
 */
template <typename RefreshForceFn>
inline void stepRK4(System& sys, double dt, RefreshForceFn refreshForces) {
    const int n3 = 3 * sys.localN;

    // Store the initial state.
    std::vector<double> x0(sys.pos);
    std::vector<double> v0(sys.vel);

    auto evalStage = [&](std::vector<double>& kx, std::vector<double>& kv, double weight,
                         const std::vector<double>& prevKx, const std::vector<double>& prevKv) {
        if (weight > 0.0) {
            // Intermediate stage: y_stage = y_n + weight * previous increment
            for (int i = 0; i < n3; ++i) {
                sys.pos[i] = x0[i] + weight * prevKx[i];
                sys.vel[i] = v0[i] + weight * prevKv[i];
            }
            refreshForces();
        }

        // For y' = (v, a): kx = dt * v, kv = dt * a
        for (int i = 0; i < n3; ++i) {
            kx[i] = sys.vel[i] * dt;
            kv[i] = sys.acc[i] * dt;
        }
    };

    std::vector<double> k1x(n3), k1v(n3);
    evalStage(k1x, k1v, 0.0, k1x, k1v);

    std::vector<double> k2x(n3), k2v(n3);
    evalStage(k2x, k2v, 0.5, k1x, k1v);

    std::vector<double> k3x(n3), k3v(n3);
    evalStage(k3x, k3v, 0.5, k2x, k2v);

    std::vector<double> k4x(n3), k4v(n3);
    evalStage(k4x, k4v, 1.0, k3x, k3v);

    // x_{n+1} and v_{n+1} from the RK4 weighted sum
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] = x0[i] + (k1x[i] + 2.0 * k2x[i] + 2.0 * k3x[i] + k4x[i]) / 6.0;
        sys.vel[i] = v0[i] + (k1v[i] + 2.0 * k2v[i] + 2.0 * k3v[i] + k4v[i]) / 6.0;
    }

    // Make stored accelerations consistent with the final state.
    refreshForces();
}

/**
 * @brief Advance one time-step with the Velocity-Verlet method.
 *
 * Velocity-Verlet uses
 *   v_{n+1/2} = v_n + (dt/2) a_n,
 *   x_{n+1}   = x_n + dt * v_{n+1/2},
 *   v_{n+1}   = v_{n+1/2} + (dt/2) a_{n+1}.
 *
 * It is  second-order accurate, time-reversible, and symplectic .
 */
template <typename RefreshForceFn>
inline void stepVelocityVerlet(System& sys, double dt, RefreshForceFn refreshForces) {
    const int n3 = 3 * sys.localN;
    const double halfDt = 0.5 * dt;

    // First half-step for velocity.
    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += halfDt * sys.acc[i];
    }

    // Position update using the half-step velocity.
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] += dt * sys.vel[i];
    }

    // Update forces/accelerations at the new positions.
    refreshForces();

    // Second half-step for velocity.
    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += halfDt * sys.acc[i];
    }
}

}  // namespace md

#endif  // MD_INTEGRATORS_HPP