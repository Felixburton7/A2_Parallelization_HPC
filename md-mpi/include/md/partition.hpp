/**
 * @file partition.hpp
 * @brief Pure helper for 1D remainder-safe particle decomposition.
 */

#ifndef MD_PARTITION_HPP
#define MD_PARTITION_HPP

#include <algorithm>

namespace md {

/**
 * @brief Compute local particle count and offset for a rank.
 *
 * Particles are distributed as evenly as possible:
 * first (N % size) ranks receive one extra particle.
 */
inline void computePartition(int N, int size, int rank, int& localN, int& offset) {
    localN = N / size + (rank < N % size ? 1 : 0);
    offset = rank * (N / size) + std::min(rank, N % size);
}

}  // namespace md

#endif  // MD_PARTITION_HPP
