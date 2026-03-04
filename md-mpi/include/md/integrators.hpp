/**
 * @file integrators.hpp
 * @brief Forward Euler, RK4, and Velocity-Verlet integrators.
 */

#ifndef MD_INTEGRATORS_HPP
#define MD_INTEGRATORS_HPP

#include <vector>

#include "md/mpi_context.hpp"
#include "md/system.hpp"

namespace md {

template <typename ForceFunctor>
inline void stepEuler(System& sys, MPIContext& ctx, double dt, ForceFunctor computeForce,
                      double& localPE, bool isHO) {
    const int n3 = 3 * sys.localN;

    for (int i = 0; i < n3; ++i) {
        sys.pos[i] += sys.vel[i] * dt;
    }

    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += sys.acc[i] * dt;
    }

    if (!isHO) {
        sys.wrapPositions();
        ctx.allgatherPositions(sys.pos);
    }

    computeForce(sys, ctx.posGlobal, localPE);
}

template <typename ForceFunctor>
inline void stepRK4(System& sys, MPIContext& ctx, double dt, ForceFunctor computeForce,
                    double& localPE, bool isHO) {
    const int n3 = 3 * sys.localN;

    std::vector<double> x0(sys.pos);
    std::vector<double> v0(sys.vel);

    auto evalStage = [&](std::vector<double>& kx, std::vector<double>& kv, double weight,
                         const std::vector<double>& prevKx, const std::vector<double>& prevKv) {
        if (weight > 0.0) {
            for (int i = 0; i < n3; ++i) {
                sys.pos[i] = x0[i] + weight * prevKx[i];
                sys.vel[i] = v0[i] + weight * prevKv[i];
            }
            if (!isHO) {
                sys.wrapPositions();
                ctx.allgatherPositions(sys.pos);
            }
            computeForce(sys, ctx.posGlobal, localPE);
        }
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

    for (int i = 0; i < n3; ++i) {
        sys.pos[i] = x0[i] + (k1x[i] + 2.0 * k2x[i] + 2.0 * k3x[i] + k4x[i]) / 6.0;
        sys.vel[i] = v0[i] + (k1v[i] + 2.0 * k2v[i] + 2.0 * k3v[i] + k4v[i]) / 6.0;
    }

    if (!isHO) {
        sys.wrapPositions();
        ctx.allgatherPositions(sys.pos);
    }
    computeForce(sys, ctx.posGlobal, localPE);
}

template <typename ForceFunctor>
inline void stepVelocityVerlet(System& sys, MPIContext& ctx, double dt, ForceFunctor computeForce,
                               double& localPE, bool isHO) {
    const int n3 = 3 * sys.localN;
    const double halfDt = 0.5 * dt;

    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += halfDt * sys.acc[i];
    }
    for (int i = 0; i < n3; ++i) {
        sys.pos[i] += dt * sys.vel[i];
    }

    if (!isHO) {
        sys.wrapPositions();
        ctx.allgatherPositions(sys.pos);
    }

    computeForce(sys, ctx.posGlobal, localPE);

    for (int i = 0; i < n3; ++i) {
        sys.vel[i] += halfDt * sys.acc[i];
    }
}

}  // namespace md

#endif  // MD_INTEGRATORS_HPP
