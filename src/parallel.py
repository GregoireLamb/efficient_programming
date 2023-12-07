import multiprocessing as mp
from multiprocessing import Process
from src.merge_sort import merge_sort, merge


class Parallel:
    def __init__(self, n_workers: int, strategy='first_split'):
        self.n_workers = n_workers
        self.strategy = strategy
        if n_workers > mp.cpu_count():
            print(f'Number of workers specified is greater than number of cores. Using {mp.cpu_count()} workers')
            self.pool = mp.Pool(mp.cpu_count())
        elif n_workers <= 0:
            print(f'Number of workers specified is invalid. Using {mp.cpu_count()} workers')
            self.pool = mp.Pool(mp.cpu_count())
        else:
            print(f'Number of workers specified is {n_workers} workers')
            self.pool = mp.Pool(n_workers)

    def para_merge_sort(self, arr):
        # TODO improve this
        arrays = []
        for i in range(self.n_workers):
            arrays.append(arr[i::self.n_workers]) # split the array into n_workers parts
        n_sorted_arr = self.pool.map(merge_sort, arrays)
        sorted_list = self.para_merge(n_sorted_arr)
        return sorted_list

    def para_merge(self, n_sorted_arr):
        # make 2 groups
        if len(n_sorted_arr) > 2:
            mid = len(n_sorted_arr) // 2
            left = self.para_merge(n_sorted_arr[mid:])
            right = self.para_merge(n_sorted_arr[:mid])
            return merge(left, right, [0] * (len(left)+len(right)))
        elif len(n_sorted_arr) == 1:
            return n_sorted_arr[0]
        else:
            return merge(n_sorted_arr[0], n_sorted_arr[1], [0] * (len(n_sorted_arr[0])+len(n_sorted_arr[1])))
