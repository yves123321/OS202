# Bucket Sort en MPI

##### Qizheng WANG

## Description
Ce projet implémente l'algorithme Bucket Sort en utilisant MPI.

## Fonctionnement
L'algorithme suit les demandes dans le sujet :
1. **Le process 0 génère un tableau de nombres aléatoires**.
2. **Chaque processus trie sa partie en utilisant l'algorithme Bucket Sort**.
3. **Les données triées sont envoyées au process 0 et le process 0 rassemblé les résultats.**

## Exécution
Pour exécuter:
mpirun -n 4 python bucket_sort_mpi.py


