#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define N_POINTS 100000000  // Nombre de points générés

double estimate_pi(int num_points) {
    int count_in_circle = 0;
    for (int i = 0; i < num_points; i++) {
        double x = (rand() / (double)RAND_MAX) * 2.0 - 1.0;
        double y = (rand() / (double)RAND_MAX) * 2.0 - 1.0;
        if (x * x + y * y <= 1.0) {
            count_in_circle++;
        }
    }
    return 4.0 * count_in_circle / num_points;
}

int main() {
    srand(time(NULL));
    clock_t start = clock();

    double pi = estimate_pi(N_POINTS);

    clock_t end = clock();
    double time_taken = (double)(end - start) / CLOCKS_PER_SEC;

    printf("Estimation de Pi = %f\n", pi);
    printf("Temps d'exécution (séquentiel) : %f secondes\n", time_taken);

    return 0;
}
