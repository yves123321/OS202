#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

#define N_POINTS 100000000  // Nombre de points générés

double estimate_pi(int num_points) {
    int count_in_circle = 0;

    #pragma omp parallel
    {
        int local_count = 0;
        unsigned int seed = omp_get_thread_num(); // Seed unique par thread

        #pragma omp for
        for (int i = 0; i < num_points; i++) {
            double x = (rand_r(&seed) / (double)RAND_MAX) * 2.0 - 1.0;
            double y = (rand_r(&seed) / (double)RAND_MAX) * 2.0 - 1.0;
            if (x * x + y * y <= 1.0) {
                local_count++;
            }
        }
        #pragma omp atomic
        count_in_circle += local_count;
    }

    return 4.0 * count_in_circle / num_points;
}

int main() {
    srand(time(NULL));
    double start_time = omp_get_wtime();

    double pi = estimate_pi(N_POINTS);

    double end_time = omp_get_wtime();
    printf("Estimation de Pi = %f\n", pi);
    printf("Temps d'exécution OpenMP : %f secondes\n", end_time - start_time);

    return 0;
}
