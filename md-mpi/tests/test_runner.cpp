/**
 * @file test_runner.cpp
 * @brief Homebrew unit test runner (no third-party libraries).
 *
 * Calls all test functions and exits with code 0 if all pass,
 * non-zero if any fail. Intended to be invoked via `make test`.
 */

#include <cstdio>
#include <cstdlib>

// Test function declarations (defined in separate .cpp files)
extern int testMIC();
extern int testForce();

int main() {
    std::printf("=== MD Unit Tests ===\n");

    int totalFailures = 0;

    totalFailures += testMIC();
    totalFailures += testForce();

    std::printf("=====================\n");

    if (totalFailures == 0) {
        std::printf("ALL TESTS PASSED\n");
        return 0;
    } else {
        std::printf("TOTAL FAILURES: %d\n", totalFailures);
        return 1;
    }
}
