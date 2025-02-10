from mpi4py import MPI
import numpy as np
import random
import time

N_POINTS = 100000000

def estimate_pi(num_points, seed):
    random.seed(seed)
    count_in_circle = sum(1 for _ in range(num_points) 
                          if (random.uniform(-1, 1) ** 2 + random.uniform(-1, 1) ** 2) <= 1)
    return count_in_circle

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

points_per_proc = N_POINTS // size
start_time = time.time()

local_count = estimate_pi(points_per_proc, rank)
total_count = comm.reduce(local_count, op=MPI.SUM, root=0)

if rank == 0:
    pi = 4.0 * total_count / N_POINTS
    end_time = time.time()
    print(f"Estimation de Pi = {pi}")
    print(f"Temps d'exécution MPI avec {size} processus : {end_time - start_time:.6f} secondes")
