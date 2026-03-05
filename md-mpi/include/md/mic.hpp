#ifndef MD_MIC_HPP
#define MD_MIC_HPP

#include <cmath>

namespace md {

/// Apply the minimum image convention to a single displacement component.
/// Maps dx into (-L/2, +L/2] using the round-based minimum image convention.
/// Tie behavior from std::round: +L/2 -> -L/2 and -L/2 -> +L/2.
inline double applyMIC(double dx, double L) {
    double invL = 1.0 / L;
    dx -= L * std::round(dx * invL);
    return dx;
}

}  // namespace md

#endif
