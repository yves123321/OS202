from mpi4py import MPI
import numpy as np
from time import time

# Définition de la taille de la matrice et du vecteur
N = 5760  # La taille peut être ajustée

# Initialisation de la matrice A et du vecteur u
A = np.array([[(i + j) % N + 1. for i in range(N)] for j in range(N)])
u = np.array([i + 1. for i in range(N)])

# Initialisation de MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Vérification que N est divisible par size
if N % size != 0:
    if rank == 0:
        print("Erreur : La taille de la matrice N doit être divisible par le nombre de processus MPI.")
    MPI.Finalize()
    exit()

# Produit Matrice-Vecteur par colonnes
Nloc = N // size  # Nombre de colonnes par processus
start_col = rank * Nloc
end_col = (rank + 1) * Nloc

comm.Barrier()
start_time = time()
partial_result = np.zeros(N)
for j in range(start_col, end_col):
    partial_result += A[:, j] * u[j]

# Rassemblement des résultats vers le processus 0
if rank == 0:
    result = np.copy(partial_result)
    for i in range(1, size):
        partial = comm.recv(source=i, tag=99)
        result += partial
    print(f"Résultat v (par colonnes) = {result}")
    total_time = time() - start_time
    print(f"Temps total d'exécution ({size} processus) : {total_time:.4f} secondes")
else:
    comm.send(partial_result, dest=0, tag=99)
