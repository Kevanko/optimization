#define _GNU_SOURCE
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const size_t MSG_SIZES[] = {
    4096,      16384,     65536,    262144,
    1048576,   2097152,   4194304,  8388608
};

static void usage(const char *prog)
{
    fprintf(stderr,
            "Usage:\n"
            "  %s                # run built-in sweep of message sizes (default n=100)\n"
            "  %s <m_bytes> [n]  # single message size (compat mode)\n",
            prog, prog);
}

static double run_exchange(size_t m, int n, int rank, int partner)
{
    char *send_buf = (char *)malloc(m);
    char *recv_buf = (char *)malloc(m);
    if (!send_buf || !recv_buf) {
        if (rank == 0)
            fprintf(stderr, "Error: failed to allocate %zu-byte buffers\n", m);
        free(send_buf);
        free(recv_buf);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }
    memset(send_buf, 0, m);

    MPI_Request reqs[2];

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

    free(send_buf);
    free(recv_buf);

    return (rank == 0) ? t_avg : 0.0;
}

int main(int argc, char **argv)
{
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size % 2 != 0) {
        if (rank == 0)
            fprintf(stderr, "Error: number of processes must be even\n");
        MPI_Finalize();
        return 1;
    }
    int partner = rank ^ 1;

    if (argc >= 2) {
        size_t m = (size_t)atol(argv[1]);
        int n = (argc >= 3) ? atoi(argv[2]) : 100;
        if (m == 0 || n <= 0) {
            if (rank == 0)
                usage(argv[0]);
            MPI_Finalize();
            return 1;
        }

        double t_avg = run_exchange(m, n, rank, partner);
        if (rank == 0) {
            printf("%zu,%.9g\n", m, t_avg);
            fflush(stdout);
        }

        MPI_Finalize();
        return 0;
    }

    const int n_iters = 100;

    for (size_t i = 0; i < sizeof(MSG_SIZES) / sizeof(MSG_SIZES[0]); ++i) {
        size_t m = MSG_SIZES[i];
        double t_avg = run_exchange(m, n_iters, rank, partner);
        if (rank == 0) {
            printf("%zu,%.9g\n", m, t_avg);
            fflush(stdout);
        }
    }

    MPI_Finalize();
    return 0;
}
