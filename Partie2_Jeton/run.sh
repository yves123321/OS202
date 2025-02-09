mpicc -o jeton jeton.c
mpirun -np 1 ./jeton
mpirun -np 2 ./jeton
mpirun -np 4 ./jeton
mpirun -np 8 ./jeton

gcc -o jeton_openmp jeton_openmp.c -fopenmp
export OMP_NUM_THREADS=1 && ./jeton_openmp
export OMP_NUM_THREADS=2 && ./jeton_openmp
export OMP_NUM_THREADS=4 && ./jeton_openmp
export OMP_NUM_THREADS=8 && ./jeton_openmp

mpirun -np 1 python3 jeton.py
mpirun -np 2 python3 jeton.py
mpirun -np 4 python3 jeton.py
mpirun -np 8 python3 jeton.py

