# ──────────────────────────────────────────────────────────────────
# Makefile — WA2: MPI Parallelisation of Molecular Dynamics
# ──────────────────────────────────────────────────────────────────
# Targets:
#   make          Build the md_solver executable
#   make test     Build and run unit tests (exits non-zero on failure)
#   make clean    Remove object files and binaries
#   make dist     Create submission tarball (excludes out/, ai/, etc.)
# ──────────────────────────────────────────────────────────────────

CXX       = mpicxx
CXXFLAGS  = -std=c++17 -O3 -march=native -Wall -Wextra -pedantic
INCLUDES  = -Iinclude

# Source files
SRC_MAIN      = src/main.cpp
SRC_EULER     = src/integrators/euler.cpp
SRC_RK4       = src/integrators/rk4.cpp
SRC_VERLET    = src/integrators/velocity_verlet.cpp
SRC_HARMONIC  = src/potentials/harmonic.cpp
SRC_LJ        = src/potentials/lennard_jones.cpp

SRCS = $(SRC_MAIN) $(SRC_EULER) $(SRC_RK4) $(SRC_VERLET) $(SRC_HARMONIC) $(SRC_LJ)
OBJS = $(SRCS:.cpp=.o)

# Test files
TEST_SRCS = tests/test_runner.cpp tests/test_mic.cpp tests/test_force.cpp
TEST_OBJS = $(TEST_SRCS:.cpp=.o)
# Tests also need the LJ potential (for test_force.cpp)
TEST_DEPS = src/potentials/lennard_jones.o src/potentials/harmonic.o

TARGET    = md_solver
TEST_BIN  = test_runner

TARBALL   = candidate_BCN_wa2.tar.gz

# ──────────────────────────────────────────────────────────────────
# Default target
# ──────────────────────────────────────────────────────────────────
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ $^

# ──────────────────────────────────────────────────────────────────
# Compilation rules
# ──────────────────────────────────────────────────────────────────
%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c -o $@ $<

# ──────────────────────────────────────────────────────────────────
# Unit tests (homebrew, no third-party libraries)
# ──────────────────────────────────────────────────────────────────
test: $(TEST_BIN)
	./$(TEST_BIN)

$(TEST_BIN): $(TEST_OBJS) $(TEST_DEPS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ $^

# ──────────────────────────────────────────────────────────────────
# Clean
# ──────────────────────────────────────────────────────────────────
clean:
	rm -f $(OBJS) $(TEST_OBJS) $(TEST_DEPS) $(TARGET) $(TEST_BIN)
	rm -f src/integrators/*.o src/potentials/*.o tests/*.o

# ──────────────────────────────────────────────────────────────────
# Submission tarball
# ──────────────────────────────────────────────────────────────────
dist: clean
	tar -czvf $(TARBALL) \
		include/ src/ tests/ scripts/ \
		Makefile README.md .clang-format
	@echo ""
	@echo "Created $(TARBALL)"
	@echo "Contents:"
	@tar -tzvf $(TARBALL) | head -30

# ──────────────────────────────────────────────────────────────────
# Create output directory
# ──────────────────────────────────────────────────────────────────
out:
	mkdir -p out

.PHONY: all clean test dist
