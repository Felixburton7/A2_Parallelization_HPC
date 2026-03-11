/**
 * @file test_integrators.cpp
 * @brief Deterministic HO checks for Euler, Verlet, and RK4.
 */

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <vector>

#include "md/constants.hpp"
#include "md/integrators.hpp"
#include "md/potentials.hpp"
#include "md/system.hpp"

namespace {

enum class IntegratorKind { Euler, Verlet, RK4 };

double runHOAndGetError(IntegratorKind kind, double dt, int steps) {
    md::System sys;
    sys.init(1, 0, 1, md::constants::L_ho_dummy);
    sys.pos[0] = 1.0;
    sys.pos[1] = 0.0;
    sys.pos[2] = 0.0;
    sys.vel[0] = 0.0;
    sys.vel[1] = 0.0;
    sys.vel[2] = 0.0;

    std::vector<double> posGlobal(3, 0.0);

    const double omega = 1.0;
    const double mass = md::constants::mass;
    auto evalHO = [omega, mass](md::System& s, const std::vector<double>& pg, double& pe) {
        md::computeHOForces(s, pg, pe, omega, mass);
    };

    double localPE = 0.0;
    auto refreshForces = [&]() { evalHO(sys, posGlobal, localPE); };
    refreshForces();

    for (int step = 0; step < steps; ++step) {
        if (kind == IntegratorKind::Euler) {
            md::stepEuler(sys, dt, refreshForces);
        } else if (kind == IntegratorKind::Verlet) {
            md::stepVelocityVerlet(sys, dt, refreshForces);
        } else {
            md::stepRK4(sys, dt, refreshForces);
        }
    }

    const double t = steps * dt;
    const double xExact = std::cos(omega * t);
    const double vExact = -omega * std::sin(omega * t);
    const double dx = sys.pos[0] - xExact;
    const double dv = sys.vel[0] - vExact;
    return std::sqrt(dx * dx + dv * dv);
}

}  // namespace

int testIntegrators() {
    int failures = 0;

    const double dt = 0.01;
    const int steps = 1000;
    const double errEuler = runHOAndGetError(IntegratorKind::Euler, dt, steps);
    const double errVerlet = runHOAndGetError(IntegratorKind::Verlet, dt, steps);
    const double errRK4 = runHOAndGetError(IntegratorKind::RK4, dt, steps);

    if (!std::isfinite(errEuler) || !std::isfinite(errVerlet) || !std::isfinite(errRK4)) {
        std::printf("FAIL: integrator error contains non-finite value\n");
        ++failures;
    }

    if (!(errRK4 < errVerlet && errVerlet < errEuler)) {
        std::printf("FAIL: expected RK4 < Verlet < Euler errors, got Euler=%e Verlet=%e RK4=%e\n",
                    errEuler, errVerlet, errRK4);
        ++failures;
    }

    if (errRK4 > 1e-7) {
        std::printf("FAIL: RK4 HO error too large: %e\n", errRK4);
        ++failures;
    }

    if (failures == 0) {
        std::printf("  Integrator tests: ALL PASSED (Euler=%e Verlet=%e RK4=%e)\n", errEuler,
                    errVerlet, errRK4);
    } else {
        std::printf("  Integrator tests: %d FAILED\n", failures);
    }

    return failures;
}
