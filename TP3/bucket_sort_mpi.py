from mpi4py import MPI 
import numpy as np


def bucket_sort(arr, num_buckets):
    " 执行桶排序 "
    " Exécuter le tri par compartiments "
    min_val, max_val = min(arr), max(arr)
    bucket_size = (max_val - min_val) / num_buckets

    # 创建桶
    # Créer des compartiments
    buckets = [[] for _ in range(num_buckets)]
    for num in arr:
        index = int((num - min_val) / bucket_size)
        if index == num_buckets:  # 确保最大值归入最后一个桶
            # Assurez-vous que la valeur maximale est placée dans le dernier compartiment
            index -= 1
        buckets[index].append(num)

    # 对每个桶内部排序
    # Trier chaque compartiment individuellement
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(sorted(bucket))
    return sorted_arr

# 初始化 MPI 环境
# Initialiser l'environnement MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# 设定数组大小
# Définir la taille du tableau
N = 100  # 生成 100 个随机数
# Générer 100 nombres aléatoires
num_buckets = size  # 让进程数与桶的数量一致
# Faire correspondre le nombre de processus au nombre de compartiments

if rank == 0:
    # 进程 0 生成随机数
    # Le processus 0 génère des nombres aléatoires
    data = np.random.rand(N) * 100  # 生成 [0, 100] 范围内的随机数
    # Générer des nombres aléatoires dans l'intervalle [0, 100]
    print(f"Unsorted Data: {data}\n")

    # 数据划分（均匀分配到所有进程）
    # Diviser les données (distribution uniforme à tous les processus)
    split_data = np.array_split(data, size)
else:
    split_data = None

# 广播数据，使每个进程接收自己的一部分数据
# Diffuser les données pour que chaque processus reçoive sa part
local_data = comm.scatter(split_data, root=0)

# 进程内部进行桶排序
# Chaque processus effectue le tri par compartiments
sorted_local_data = bucket_sort(local_data, num_buckets)

# 收集所有进程排序后的数据
# Collecter les données triées de tous les processus
gathered_data = comm.gather(sorted_local_data, root=0)

if rank == 0:
    # 合并所有进程的数据
    # Fusionner les données de tous les processus
    final_sorted_data = np.concatenate(gathered_data)
    print(f"Sorted Data: {final_sorted_data}")

