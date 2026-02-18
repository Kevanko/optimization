/*
 * Lab 1: MPI bandwidth benchmark.
 * Measures average time of MPI_Isend/MPI_Irecv exchange for message size m over n iterations.
 * Output: m_bytes,t_sec (one line to stdout; rank 0 only).
 */

#define _GNU_SOURCE
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void usage(const char *prog)
{
    fprintf(stderr, "Usage: %s <m_bytes> [n_iterations]\n", prog);
    fprintf(stderr, "  m_bytes       Message size in bytes\n");
    fprintf(stderr, "  n_iterations  Number of iterations for averaging (default: 100)\n");
}

int main(int argc, char **argv)
{
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (argc < 2) {
        if (rank == 0)
            usage(argv[0]);
        MPI_Finalize();
        return 1;
    }

    size_t m = (size_t)atol(argv[1]);
    int n = (argc >= 3) ? atoi(argv[2]) : 100;
    if (m == 0 || n <= 0) {
        if (rank == 0)
            usage(argv[0]);
        MPI_Finalize();
        return 1;
    }

    /* Pair exchange: each process talks to partner = rank ^ 1 (0<->1, 2<->3, ...) */
    if (size % 2 != 0) {
        if (rank == 0)
            fprintf(stderr, "Error: number of processes must be even\n");
        MPI_Finalize();
        return 1;
    }

    int partner = rank ^ 1;
    char *send_buf = (char *)malloc(m);
    char *recv_buf = (char *)malloc(m);
    if (!send_buf || !recv_buf) {
        if (rank == 0)
            fprintf(stderr, "Error: failed to allocate buffers\n");
        free(send_buf);
        free(recv_buf);
        MPI_Finalize();
        return 1;
    }
    memset(send_buf, 0, m);

    MPI_Request reqs[2];

    /* Warm-up: one exchange without timing */
    MPI_Isend(send_buf, (int)m, MPI_BYTE, partner, 0, MPI_COMM_WORLD, &reqs[0]);
    MPI_Irecv(recv_buf, (int)m, MPI_BYTE, partner, 0, MPI_COMM_WORLD, &reqs[1]);
    MPI_Waitall(2, reqs, MPI_STATUSES_IGNORE);
    MPI_Barrier(MPI_COMM_WORLD);

    double t_start = MPI_Wtime();
    for (int i = 0; i < n; i++) {
        MPI_Isend(send_buf, (int)m, MPI_BYTE, partner, 0, MPI_COMM_WORLD, &reqs[0]);
        MPI_Irecv(recv_buf, (int)m, MPI_BYTE, partner, 0, MPI_COMM_WORLD, &reqs[1]);
        MPI_Waitall(2, reqs, MPI_STATUSES_IGNORE);
    }
    MPI_Barrier(MPI_COMM_WORLD);
    double t_end = MPI_Wtime();

    double t_total = t_end - t_start;
    double t_avg = t_total / (double)n;

    /* Rank 0 prints single line: m_bytes,t_sec for parsing */
    if (rank == 0) {
        printf("%zu,%.9g\n", m, t_avg);
    }

    free(send_buf);
    free(recv_buf);
    MPI_Finalize();
    return 0;
}
