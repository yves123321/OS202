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
mandelbrot_set = MandelbrotSet(max_iterations=200, escape_radius=10)
width, height = 1024, 1024
scaleX = 3.0 / width
scaleY = 2.25 / height

if size == 1:
    # 单进程模式：主进程自己计算整个图像
    print("[INFO] Running in single-process mode.")
    global_convergence = np.empty((width, height), dtype=np.double)
    start_time = time.time()
    for x in range(width):
        for y in range(height):
            c = complex(-2.0 + scaleX * x, -1.125 + scaleY * y)
            global_convergence[x, y] = mandelbrot_set.convergence(c, smooth=True)
    total_compute_time = time.time() - start_time
    print(f"Total computation time: {total_compute_time:.2f} s")
    
    # 保存图像
    image_start_time = time.time()
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(global_convergence.T) * 255))
    image.save("mandelbrot_single_output.png")
    image_end_time = time.time()
    print(f"Image saving time: {image_end_time - image_start_time:.2f} s")
    exit(0)

if rank == 0:
    # 多进程模式 - 主进程（Master）
    global_convergence = np.empty((width, height), dtype=np.double)
    task_queue = list(range(width))  # 任务池（列索引）
    active_workers = size - 1  # 活跃的从进程数

    # 接收从进程的“准备好”信号（tag=1）
    for _ in range(size - 1):
        comm.recv(source=MPI.ANY_SOURCE, tag=1)

    # 初始任务分配
    for worker in range(1, size):
        if task_queue:
            col = task_queue.pop(0)
            comm.send(col, dest=worker, tag=0)
        else:
            comm.send(-1, dest=worker, tag=0)  # 终止信号
            active_workers -= 1

    # 任务调度循环
    while task_queue or active_workers > 0:
        stat = MPI.Status()
        data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=stat)
        source = stat.Get_source()
        tag = stat.Get_tag()

        if tag == 1:  # 从进程请求任务
            if task_queue:
                col = task_queue.pop(0)
                comm.send(col, dest=source, tag=0)
            else:
                comm.send(-1, dest=source, tag=0)  # 无任务，终止
                active_workers -= 1
        elif tag == 0:  # 接收计算结果
            col, col_data = data
            global_convergence[col, :] = col_data

    # 收集从进程计算时间
    compute_times = []
    for worker in range(1, size):
        comm.send(None, dest=worker, tag=3)  # 请求计算时间
        compute_time = comm.recv(source=worker, tag=2)
        compute_times.append(compute_time)

    total_compute_time = sum(compute_times)
    total_end_time = time.time()
    print(f"Total computation time (all slaves): {total_compute_time:.2f} s")
    print(f"Total execution time (excluding image saving): {total_end_time - total_start_time:.2f} s")

    # 生成和保存图像
    image_start_time = time.time()
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(global_convergence.T) * 255))
    image.save("mandelbrot_parallel_master_slave_columns_output.png")
    image_end_time = time.time()
    print(f"Image saving time: {image_end_time - image_start_time:.2f} s")
else:
    # 从进程（Slave）
    compute_time = 0.0

    while True:
        comm.send(None, dest=0, tag=1)  # 发送“准备好”信号
        col = comm.recv(source=0, tag=0)
        
        if col == -1:
            break  # 终止信号

        # 计算该列的曼德布罗特值
        start_time = time.time()
        col_data = np.empty(height, dtype=np.double)
        for y in range(height):
            c = complex(-2.0 + scaleX * col, -1.125 + scaleY * y)
            col_data[y] = mandelbrot_set.convergence(c, smooth=True)
        compute_time += time.time() - start_time

        comm.send((col, col_data), dest=0, tag=0)  # 发送结果

    # 发送计算时间
    comm.recv(source=0, tag=3)
    comm.send(compute_time, dest=0, tag=2)
