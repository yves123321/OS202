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

# Produit Matrice-Vecteur par lignes
Nloc = N // size  # Nombre de lignes par processus
start_row = rank * Nloc
end_row = (rank + 1) * Nloc

comm.Barrier()
start_time = time()
local_result = np.zeros(Nloc)
for i in range(start_row, end_row):
    local_result[i - start_row] = np.dot(A[i, :], u)

# Rassemblement des résultats vers le processus 0
if rank == 0:
    result = np.zeros(N)
    result[start_row:end_row] = local_result
    for i in range(1, size):
        recv_data = np.zeros(Nloc)
        comm.Recv(recv_data, source=i, tag=99)
        result[i * Nloc:(i + 1) * Nloc] = recv_data
    print(f"Résultat v (par lignes) = {result}")
    total_time = time() - start_time
    print(f"Temps total d'exécution ({size} processus) : {total_time:.4f} secondes")
else:
    comm.Send(local_result, dest=0, tag=99)
