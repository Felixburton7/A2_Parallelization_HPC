#include "md/observables.hpp"

#include <cmath>

#include "md/constants.hpp"

namespace md {

double computeLocalKineticEnergy(const System& sys, double mass) {
    double eKin = 0.0;
    for (int i = 0; i < 3 * sys.localN; ++i) {
        eKin += sys.vel[i] * sys.vel[i];
    }
    return 0.5 * mass * eKin;
}

double computeTemperature(double eKinTotal, int N) {
    int nDof = 3 * (N - 1);  // degrees of freedom after CoM removal
    return (2.0 * eKinTotal) / (nDof * constants::kB);
}

void accumulateGR(const std::vector<double>& posGlobal, int N, double L, int offset, int localN,
                  double dr, double rMax, std::vector<double>& histogram) {
    int nBins = static_cast<int>(histogram.size());
    const double invL = 1.0 / L;  // constant per call

    for (int i = offset; i < offset + localN; ++i) {
        for (int j = i + 1; j < N; ++j) {
            double dx = posGlobal[3 * i + 0] - posGlobal[3 * j + 0];
            double dy = posGlobal[3 * i + 1] - posGlobal[3 * j + 1];
            double dz = posGlobal[3 * i + 2] - posGlobal[3 * j + 2];

            // Minimum image convention
            dx -= L * std::round(dx * invL);
            dy -= L * std::round(dy * invL);
            dz -= L * std::round(dz * invL);

            double r = std::sqrt(dx * dx + dy * dy + dz * dz);
            if (r < rMax) {
                int bin = static_cast<int>(r / dr);
                if (bin < nBins) {
                    histogram[bin] += 1.0;
                }
            }
        }
    }
}

void normaliseGR(std::vector<double>& histogram, double dr, int N, double L, int nFrames) {
    double V = L * L * L;
    // Finite-N correction: reference density is (N-1)/V because a particle cannot pair with itself.
    // This differs from the N/V convention in some textbooks; the report must state this choice
    // explicitly.
    double rho = static_cast<double>(N - 1) / V;

    for (int bin = 0; bin < static_cast<int>(histogram.size()); ++bin) {
        double rLow = bin * dr;
        double rInner = rLow;
        double rOuter = rLow + dr;
        double shellVol =
            (4.0 / 3.0) * M_PI * (rOuter * rOuter * rOuter - rInner * rInner * rInner);

        // Factor of 2: unordered pairs (i<j) → ordered pair convention
        if (shellVol > 0.0 && nFrames > 0) {
            histogram[bin] *= 2.0 / (rho * static_cast<double>(N) * shellVol * nFrames);
        }
    }
}

}  // namespace md
