/**
 * @file test_partition.cpp
 * @brief Unit tests for remainder-safe particle decomposition.
 */

#include <cstdio>
#include <cstdlib>
#include <vector>

#include "md/partition.hpp"

namespace {

int checkCase(int N, int P, const std::vector<int>& expectedLocalN,
              const std::vector<int>& expectedOffset) {
    int failures = 0;

    if (static_cast<int>(expectedLocalN.size()) != P || static_cast<int>(expectedOffset.size()) != P) {
        std::printf("FAIL: partition test fixture size mismatch for N=%d, P=%d\n", N, P);
        return 1;
    }

    int sumLocalN = 0;
    for (int rank = 0; rank < P; ++rank) {
        int localN = -1;
        int offset = -1;
        md::computePartition(N, P, rank, localN, offset);
        sumLocalN += localN;

        if (localN != expectedLocalN[rank]) {
            std::printf("FAIL: partition localN mismatch N=%d P=%d rank=%d got=%d expected=%d\n", N,
                        P, rank, localN, expectedLocalN[rank]);
            ++failures;
        }
        if (offset != expectedOffset[rank]) {
            std::printf("FAIL: partition offset mismatch N=%d P=%d rank=%d got=%d expected=%d\n", N,
                        P, rank, offset, expectedOffset[rank]);
            ++failures;
        }
    }

    if (sumLocalN != N) {
        std::printf("FAIL: partition count conservation N=%d P=%d sum_localN=%d\n", N, P, sumLocalN);
        ++failures;
    }

    return failures;
}

}  // namespace

int testPartition() {
    int failures = 0;

    failures += checkCase(32, 2, {16, 16}, {0, 16});
    failures += checkCase(10, 3, {4, 3, 3}, {0, 4, 7});
    failures += checkCase(3, 5, {1, 1, 1, 0, 0}, {0, 1, 2, 3, 3});
    failures += checkCase(1, 4, {1, 0, 0, 0}, {0, 1, 1, 1});
    failures += checkCase(17, 6, {3, 3, 3, 3, 3, 2}, {0, 3, 6, 9, 12, 15});

    if (failures == 0) {
        std::printf("  Partition tests: ALL PASSED\n");
    } else {
        std::printf("  Partition tests: %d FAILED\n", failures);
    }

    return failures;
}
