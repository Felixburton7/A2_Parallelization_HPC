/**
 * @file constants.hpp
 * @brief Physical constants for Molecular Dynamics simulation.
 *
 * Physical constants and derived LJ parameters (SI units).
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

// ── Magic numbers extracted from codebase ──

/// Fraction of sigma for random initial position perturbation
constexpr double fccPerturbation = 0.01;

/// g(r) histogram bin width in units of sigma
constexpr double grBinWidthSigma = 0.02;

/// Box size for HO mode (non-periodic; effectively unused but kept finite as a safety guard)
constexpr double L_ho_dummy = 1.0e10;

/// Lower bound numerical guard for temperature rescaling
constexpr double rescaleGuard = 1e-30;

// ── Rahman (1964) reference state point ──

/// Number of particles in Rahman's simulation
constexpr int N_rahman = 864;

/// FCC lattice repeats for N=864 (4 * 6^3 = 864)
constexpr int k_rahman = 6;

/// Box side length for N=864 in units of sigma
constexpr double L_sigma_rahman = 10.229;

/// Box side length for N=864 [m]
constexpr double L_rahman = L_sigma_rahman * sigma;

}  // namespace constants
}  // namespace md

#endif  // MD_CONSTANTS_HPP
