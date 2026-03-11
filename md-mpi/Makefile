CXX = mpicxx
OPT ?= -O3
MARCH ?=
CXXFLAGS = -std=c++17 $(OPT) $(MARCH) -g -Wall -Wextra -pedantic
INCLUDES = -Iinclude

SRC_MAIN = src/main.cpp
SRC_HARMONIC = src/potentials/harmonic.cpp
SRC_LJ = src/potentials/lennard_jones.cpp
SRC_OBSERVABLES = src/observables.cpp

SRCS = $(SRC_MAIN) $(SRC_HARMONIC) $(SRC_LJ) $(SRC_OBSERVABLES)
OBJS = $(SRCS:.cpp=.o)

TEST_SRCS = tests/test_runner.cpp tests/test_mic.cpp tests/test_force.cpp \
            tests/test_integrators.cpp tests/test_partition.cpp
TEST_OBJS = $(TEST_SRCS:.cpp=.o)
TEST_DEPS = src/potentials/lennard_jones.o src/potentials/harmonic.o src/observables.o

TARGET = md_solver
TEST_BIN = test_runner

BCN ?= 4316J
TARBALL = $(BCN)_wa2.tar.gz

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c -o $@ $<

test: $(TEST_BIN)
	./$(TEST_BIN)

$(TEST_BIN): $(TEST_OBJS) $(TEST_DEPS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ $^

clean:
	rm -f $(OBJS) $(TEST_OBJS) $(TARGET) $(TEST_BIN)
	rm -f src/potentials/*.o tests/*.o

dist: clean
	@test "$(BCN)" != "4316J_PLACEHOLDER" || (echo "ERROR: Set BCN" && false)
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
	rm -f test_runner wa2-results-*.out
	tar -czvf $(TARBALL) \
		--exclude='__pycache__' --exclude='*.pyc' \
		include/ src/ tests/ scripts/ \
		Makefile README.md .clang-format
	@echo ""
	@echo "Created $(TARBALL)"
	@echo "Contents:"
	@tar -tzvf $(TARBALL) | head -40

out:
	mkdir -p out

.PHONY: all clean test dist out
