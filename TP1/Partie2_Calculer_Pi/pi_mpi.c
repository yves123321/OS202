#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>

#define N_POINTS 100000000  // Nombre total de points

double estimate_pi(int num_points, int rank) {
    int count_in_circle = 0;
    unsigned int seed = rank + 1; // Seed unique pour chaque processus

    for (int i = 0; i < num_points; i++) {
        double x = (rand_r(&seed) / (double)RAND_MAX) * 2.0 - 1.0;
        double y = (rand_r(&seed) / (double)RAND_MAX) * 2.0 - 1.0;
        if (x * x + y * y <= 1.0) {
            count_in_circle++;
        }
    }
    return (double)count_in_circle;
}

int main(int argc, char *argv[]) {
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int points_per_proc = N_POINTS / size;
    double start_time = MPI_Wtime();

    double local_count = estimate_pi(points_per_proc, rank);
    double total_count;

    MPI_Reduce(&local_count, &total_count, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        double pi = 4.0 * total_count / N_POINTS;
        double end_time = MPI_Wtime();
        printf("Estimation de Pi = %f\n", pi);
        printf("Temps d'exécution MPI avec %d processus : %f secondes\n", size, end_time - start_time);
    }

    MPI_Finalize();
    return 0;
}
