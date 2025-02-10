from mpi4py import MPI
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
import matplotlib.cm
import time

@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius: float = 2.0

    def convergence(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.count_iterations(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex, smooth=False) -> int | float:
        z = 0
        for iter in range(self.max_iterations):
            z = z * z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z))) / log(2)
                return iter
        return self.max_iterations

# MPI 初始化
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# 记录总时间
total_start_time = time.time()

# 参数设置
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024
scaleX = 3.0 / width
scaleY = 2.25 / height

# 计算每个进程处理的行范围
rows_per_proc = height // size
extra_rows = height % size

# 计算起始和结束行
if rank < extra_rows:
    start_row = rank * (rows_per_proc + 1)
    end_row = start_row + rows_per_proc + 1
else:
    start_row = rank * rows_per_proc + extra_rows
    end_row = start_row + rows_per_proc

num_rows = end_row - start_row
local_convergence = np.empty((num_rows, width), dtype=np.double)

# 计算曼德布罗特集合
start_time = time.time()
for i, y in enumerate(range(start_row, end_row)):
    for x in range(width):
        c = complex(-2.0 + scaleX * x, -1.125 + scaleY * y)
        local_convergence[i, x] = mandelbrot_set.convergence(c, smooth=True)
end_time = time.time()
print(f"Rank {rank} computation time: {end_time - start_time:.2f} s")

# 进程 0 收集所有数据
start_time = time.time()
all_data = comm.gather((start_row, local_convergence), root=0)
data_gathering_end_time = time.time()

if rank == 0:
    print(f"Data gathering time: {data_gathering_end_time - start_time:.2f} s")
    full_convergence = np.empty((height, width), dtype=np.double)
    
    # 按照 start_row 进行排序，确保数据按行拼接
    for start_row, data in sorted(all_data, key=lambda x: x[0]):
        full_convergence[start_row:start_row + data.shape[0], :] = data
    
    # 记录总时间（不包括图像保存）
    total_end_time = time.time()
    print(f"Total execution time (excluding image saving): {total_end_time - total_start_time:.2f} s")
    
    # 保存图像
    image_start_time = time.time()
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(full_convergence) * 255))
    image.save("mandelbrot_parallel_output.png")
    image_end_time = time.time()
    print(f"Image saving time: {image_end_time - image_start_time:.2f} s")
