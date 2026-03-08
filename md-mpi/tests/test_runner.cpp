/**
 * @file test_runner.cpp
 * @brief Homebrew unit test runner.
 */

#include <cstdio>
#include <cstdlib>

extern int testMIC();
extern int testForce();
extern int testIntegrators();
extern int testPartition();

int main() {
    std::printf("=== MD Unit Tests ===\n");

    int totalFailures = 0;

    totalFailures += testMIC();
    totalFailures += testForce();
    totalFailures += testIntegrators();
    totalFailures += testPartition();

    std::printf("=====================\n");

    if (totalFailures == 0) {
        std::printf("ALL TESTS PASSED\n");
        return 0;
    } else {
        std::printf("TOTAL FAILURES: %d\n", totalFailures);
        return 1;
    }
}
