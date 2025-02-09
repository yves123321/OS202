#include <mpi.h>
#include <stdio.h>

#define N_ITER 10000  // Nombre de tours du jeton

int main(int argc, char* argv[]) {
    int rank, size;
    int token;
    double start_time, end_time;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Début du chrono
    start_time = MPI_Wtime();

    if (size == 1) {
        // Cas particulier : pas d'échange MPI possible
        token = 1;
        printf("Avec 1 seul processus, jeton final : %d\n", token);
    } else {
        for (int iter = 0; iter < N_ITER; iter++) {
            if (rank == 0) {
                if (iter == 0) {
                    token = 1;  // Initialisation du jeton au premier tour
                }
                MPI_Send(&token, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
                MPI_Recv(&token, 1, MPI_INT, size - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            } else {
                MPI_Recv(&token, 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                token += 1;
                MPI_Send(&token, 1, MPI_INT, (rank + 1) % size, 0, MPI_COMM_WORLD);
            }
        }
    }

    // Fin du chrono
    end_time = MPI_Wtime();
    if (rank == 0) {
        printf("Processus 0 a reçu le jeton final: %d après %d itérations\n", token, N_ITER);
        printf("Temps d'exécution MPI avec %d processus et %d itérations : %f secondes\n", size, N_ITER, end_time - start_time);
    }

    MPI_Finalize();
    return 0;
}
