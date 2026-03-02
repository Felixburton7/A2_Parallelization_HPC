/**
 * @file constants.hpp
 * @brief Physical constants for Molecular Dynamics simulation.
 *
 * All constants are defined as constexpr values in SI units unless
 * otherwise noted. No magic numbers should appear anywhere else in
 * the codebase — reference this header instead.
 */

#ifndef MD_CONSTANTS_HPP
#define MD_CONSTANTS_HPP

namespace md {
namespace constants {

/// Boltzmann constant [J/K]
constexpr double kB = 1.380649e-23;

/// Lennard-Jones well depth / kB [K] (for Argon)
constexpr double eps_over_kB = 120.0;

/// Lennard-Jones well depth [J]
constexpr double epsilon = kB * eps_over_kB;

/// Lennard-Jones length scale (sigma) [m]
constexpr double sigma = 3.4e-10;

/// Argon atomic mass [kg]
constexpr double mass = 66.904265e-27;

/// Interaction cutoff in units of sigma
constexpr double rcut_sigma = 2.25;

/// Interaction cutoff [m]
constexpr double rcut = rcut_sigma * sigma;

/// Pi
constexpr double pi = 3.14159265358979323846;

// ── Derived quantities for optimised LJ kernel ──

/// sigma^2
constexpr double sigma2 = sigma * sigma;

/// sigma^6
constexpr double sigma6 = sigma2 * sigma2 * sigma2;

/// sigma^12
constexpr double sigma12 = sigma6 * sigma6;

/// Squared cutoff distance
constexpr double rcut2 = rcut * rcut;

/// 4 * epsilon (energy prefactor)
constexpr double four_eps = 4.0 * epsilon;

/// 24 * epsilon (force prefactor)
constexpr double twentyfour_eps = 24.0 * epsilon;

// ── Rahman (1964) reference state point ──

/// Number of particles in Rahman's simulation
constexpr int N_rahman = 864;

/// FCC lattice repeats for N=864 (4 * 6^3 = 864)
constexpr int k_rahman = 6;

/// Box side length for N=864 in units of sigma
constexpr double L_sigma_rahman = 10.229;

/// Box side length for N=864 [m]
constexpr double L_rahman = L_sigma_rahman * sigma;

/// Initial temperature [K]
constexpr double T_init = 94.4;

/// Timestep [s]
constexpr double dt_rahman = 1.0e-14;

/// Total simulation time [s]
constexpr double T_sim = 1.0e-12;

/// Number of timesteps (T_sim / dt)
constexpr int steps_rahman = 100;

}  // namespace constants
}  // namespace md

#endif  // MD_CONSTANTS_HPP
