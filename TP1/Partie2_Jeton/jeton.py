from mpi4py import MPI

N_ITER = 10000  # Nombre d'itérations

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

start_time = MPI.Wtime()  # Début du chrono

if size == 1:
    token = 1
    print(f"Avec 1 seul processus, jeton final : {token}")
else:
    for _ in range(N_ITER):
        if rank == 0:
            if _ == 0:
                token = 1  # Initialisation
            comm.send(token, dest=1, tag=0)
            token = comm.recv(source=size - 1, tag=0)
        else:
            token = comm.recv(source=rank - 1, tag=0)
            token += 1
            comm.send(token, dest=(rank + 1) % size, tag=0)

end_time = MPI.Wtime()  # Fin du chrono

if rank == 0:
    print(f"Processus 0 a reçu le jeton final: {token} après {N_ITER} itérations")
    print(f"Temps d'exécution MPI avec {size} processus et {N_ITER} itérations : {end_time - start_time:.6f} secondes")
