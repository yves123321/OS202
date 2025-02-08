#include <stdio.h>
#include <omp.h>

#define N_ITER 10000  // Nombre d'itérations

int main() {
    int token = 1;
    double start_time, end_time;

    // Début du chrono
    start_time = omp_get_wtime();

    #pragma omp parallel
    {
        int nb_threads = omp_get_num_threads();  // Récupérer le vrai nombre de threads
        #pragma omp single
        {
            printf("Nombre de threads utilisés: %d\n", nb_threads);
        }

        for (int iter = 0; iter < N_ITER; iter++) {
            #pragma omp atomic
            token += 1;
        }
    }

    // Fin du chrono
    end_time = omp_get_wtime();

    printf("Jeton final après %d itérations: %d\n", N_ITER, token);
    printf("Temps d'exécution OpenMP avec %d itérations : %f secondes\n", 
           N_ITER, end_time - start_time);

    return 0;
}
