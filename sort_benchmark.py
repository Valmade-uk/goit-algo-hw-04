"""
Task 3: Compare Insertion Sort, Merge Sort, and Timsort.
"""
from __future__ import annotations
import argparse
import random
import timeit
import csv
from typing import List, Callable
from dataclasses import dataclass

def insertion_sort(arr: List[int]) -> List[int]:
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = key
    return a

def merge_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left: List[int], right: List[int]) -> List[int]:
    i = j = 0
    result: List[int] = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def timsort(arr: List[int]) -> List[int]:
    return sorted(arr)

def make_random(n: int) -> List[int]:
    return [random.randint(-10**9, 10**9) for _ in range(n)]

def make_sorted(n: int) -> List[int]:
    return list(range(n))

def make_reversed(n: int) -> List[int]:
    return list(range(n, 0, -1))

def make_nearly_sorted(n: int, swaps: int | None = None) -> List[int]:
    if swaps is None:
        swaps = max(1, n // 100)
    arr = list(range(n))
    for _ in range(swaps):
        i, j = random.randrange(n), random.randrange(n)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

DATASETS = {
    "random": make_random,
    "sorted": make_sorted,
    "reversed": make_reversed,
    "nearly_sorted": make_nearly_sorted,
}

@dataclass
class Result:
    algo: str
    dataset: str
    size: int
    best: float
    avg: float

def time_algo(fn: Callable[[List[int]], List[int]], data: List[int], repeats: int):
    stmt = lambda: fn(data)
    times = timeit.repeat(stmt, number=1, repeat=repeats)
    return min(times), sum(times)/len(times)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", type=int, nargs="+", default=[1000, 5000, 10000])
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--output", type=str, default="results.csv")
    args = parser.parse_args()

    algos = {"insertion": insertion_sort, "merge": merge_sort, "timsort": timsort}
    results: list[Result] = []
    random.seed(42)

    for size in args.sizes:
        base_data = {name: gen(size) for name, gen in DATASETS.items()}
        for dname, data in base_data.items():
            for aname, fn in algos.items():
                if aname == "insertion" and size > 20000:
                    continue
                best, avg = time_algo(fn, data, args.repeats)
                results.append(Result(aname, dname, size, best, avg))
                print(f"{aname:10s} | {dname:13s} | n={size:6d} | best={best:.6f}s | avg={avg:.6f}s")

    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["algorithm", "dataset", "size", "best_sec", "avg_sec"])
        for r in results:
            writer.writerow([r.algo, r.dataset, r.size, f"{r.best:.9f}", f"{r.avg:.9f}"])
    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()