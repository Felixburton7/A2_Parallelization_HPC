/**
 * @file mpi_context.hpp
 * @brief MPI rank/size management, particle decomposition, and Allgatherv setup.
 *
 * Encapsulates all MPI-specific state: rank, size, local particle count,
 * offset, recvcounts/displs arrays for MPI_Allgatherv, and the permanent
 * global position buffer. All MPI array arguments use int type as required
 * by the MPI standard.
 */

#ifndef MD_MPI_CONTEXT_HPP
#define MD_MPI_CONTEXT_HPP

#include <mpi.h>

#include <algorithm>
#include <vector>

namespace md {

/**
 * @brief MPI context: decomposition and Allgatherv helpers.
 */
class MPIContext {
   public:
    int rank;    ///< This process's rank
    int size;    ///< Total number of MPI processes
    int N;       ///< Total number of particles (global)
    int localN;  ///< Number of particles owned by this rank
    int offset;  ///< Starting global index for this rank's particles

    std::vector<int> recvcounts;    ///< Number of doubles received from each rank (3 * localN[r])
    std::vector<int> displs;        ///< Displacement in doubles for each rank (3 * offset[r])
    std::vector<double> posGlobal;  ///< Permanent global position buffer (size 3*N)

    double commTime = 0.0;    ///< Accumulated MPI_Allgatherv wall time [s] (timing mode only)
    bool timingMode = false;  ///< When true, measure communication time

    /**
     * @brief Initialise MPI context with particle decomposition.
     *
     * Distributes N particles across P ranks as evenly as possible.
     * Rank r owns particles [offset_r, offset_r + localN_r).
     * The first (N % P) ranks each get one extra particle.
     *
     * Also pre-computes recvcounts and displs arrays for MPI_Allgatherv,
     * and allocates the permanent posGlobal buffer.
     *
     * @param totalN Total number of particles
     */
    void init(int totalN) {
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        MPI_Comm_size(MPI_COMM_WORLD, &size);
        N = totalN;

        // Remainder-safe decomposition
        localN = N / size + (rank < N % size ? 1 : 0);
        offset = rank * (N / size) + std::min(rank, N % size);

        // Pre-compute Allgatherv parameters (int arrays, values in doubles)
        recvcounts.resize(size);
        displs.resize(size);
        for (int r = 0; r < size; ++r) {
            int ln = N / size + (r < N % size ? 1 : 0);
            int off = r * (N / size) + std::min(r, N % size);
            recvcounts[r] = 3 * ln;
            displs[r] = 3 * off;
        }

        // Permanent global position buffer
        posGlobal.resize(3 * N, 0.0);
    }

    /**
     * @brief Gather local positions from all ranks into posGlobal.
     *
     * Each rank sends its local positions (3*localN doubles) and receives
     * the complete global position array (3*N doubles). This is the ONLY
     * collective communication in the time-stepping loop for LJ mode.
     *
     * When timingMode is true, the wall time spent in MPI_Allgatherv is
     * accumulated in commTime for compute-vs-communication analysis.
     *
     * @param posLocal Local position array (3*localN doubles, interleaved)
     */
    void allgatherPositions(const std::vector<double>& posLocal) {
        double t0 = timingMode ? MPI_Wtime() : 0.0;
        MPI_Allgatherv(posLocal.data(), 3 * localN, MPI_DOUBLE, posGlobal.data(), recvcounts.data(),
                       displs.data(), MPI_DOUBLE, MPI_COMM_WORLD);
        if (timingMode)
            commTime += (MPI_Wtime() - t0);
    }

    /**
     * @brief Check if this rank is the root (rank 0).
     * @return true if rank == 0
     */
    bool isRoot() const { return rank == 0; }
};

}  // namespace md

#endif  // MD_MPI_CONTEXT_HPP
