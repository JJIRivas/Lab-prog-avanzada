import heapq
import time
from collections import Counter

scores = [34, 78, 12, 45, 99, 67, 23, 88, 50, 99, 12, 12]

heapq.heapify(scores)
# print(scores)

k = input("K: ")

knum = int(k)

min_k = heapq.nsmallest(knum, scores)
top_k = heapq.nlargest(knum, scores)

print(f"min: {min_k}" + f" max: {top_k}")

freq = Counter(scores).most_common(knum)

print(f"freq {freq}")

nums = [3, 2, 1, 5, 6, 4]
heapq.heapify(nums)

knum = int(input("k: "))


def masGrande(nums: list, k: int) -> int:
    heap = []
    for n in nums:
        heapq.heappush(heap, n)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


def top_k_products(productos, k):
    heap = []
    for nombre, score in productos:
        heapq.heappush(heap, (score, nombre))
        if len(heap) > k:
            heapq.heappop(heap)  
    return [nombre for score, nombre in sorted(heap, reverse=True)]


productos = [("Laptop", 95), ("Mouse", 80), ("Teclado", 85)]
print(top_k_products(productos, k=2))  # 'Laptop', 'Teclado']

import random

data = random.sample(range(100_000), 10_000)
k = 10

t0 = time.perf_counter()
heapq.nlargest(k, data)
t1 = time.perf_counter()
sorted(data, reverse=True)[:k]
t2 = time.perf_counter()

print(f"heapq.nlargest: {(t1 - t0) * 1000:.3f} ms")
print(f"sorted: {(t2 - t1) * 1000:.3f} ms")

print(f"Heap: {nums}")
print("K mas grande:")
print(masGrande(nums, knum))

ls1 = [1, 4, 5]
ls2 = [1, 3, 4]
ls3 = [2, 6]

newls = list(heapq.merge(ls1, ls2, ls3))

print(f"lista mezc: {newls}")
