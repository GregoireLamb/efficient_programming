import multiprocessing as mp
from multiprocessing import Process


class AugmentedMergeSort:
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

    def augmented_merge_sort(self, arr, threshold: int = 10):
        if len(arr) <= threshold:
            return merge_insert_sort(arr)
        arrays = [arr[i::self.n_workers] for i in range(self.n_workers)]  # split the array into n_workers parts
        sorted_list = self.para_merge(self.pool.map(merge_insert_sort, arrays))
        return sorted_list

    def para_merge(self, n_sorted_arr):
        if len(n_sorted_arr) <= 1:
            return n_sorted_arr[0] if n_sorted_arr else []

        mid = len(n_sorted_arr) // 2
        left = self.para_merge(n_sorted_arr[:mid])
        right = self.para_merge(n_sorted_arr[mid:])

        return merge(left, right, [0] * (len(left) + len(right)))


# Merge sort baseline implementation
# def merge_insert_sort(arr, threshold: int = 10):
#     if len(arr) <= 1:
#         return arr
#
#     elif len(arr) <= threshold:
#         return insertionSort(arr)
#
#     else:
#         mid = len(arr) // 2
#         left, right = merge_insert_sort(arr[:mid]), merge_insert_sort(arr[mid:])
#         return merge(left, right, arr.copy())
#
#
# def merge(left, right, merged):
#     left_cursor, right_cursor = 0, 0
#     while left_cursor < len(left) and right_cursor < len(right):
#         if left[left_cursor] <= right[right_cursor]:
#             merged[left_cursor + right_cursor] = left[left_cursor]
#             left_cursor += 1
#         else:
#             merged[left_cursor + right_cursor] = right[right_cursor]
#             right_cursor += 1
#     for left_cursor in range(left_cursor, len(left)):
#         merged[left_cursor + right_cursor] = left[left_cursor]
#     for right_cursor in range(right_cursor, len(right)):
#         merged[left_cursor + right_cursor] = right[right_cursor]
#     return merged


# Insertion sort in Python

def merge_insert_sort(input_arr: [], min_run: int = 32) -> []:
    # Copy array to not sort inplace
    arr = input_arr.copy()
    n = len(input_arr)

    if n <= 1:
        return input_arr

    if n <= min_run:
        insertion_sort(arr, 0, n - 1)
        return arr

    # Step 1: insertion sort on subarrays
    for i in range(0, n, min_run):
        insertion_sort(arr, i, min((i + min_run - 1), n - 1))

    # Step 2: merge sort on sorted subarrays
    window = min_run
    while window < n:
        for left in range(0, n, 2 * window):
            mid = left + window - 1
            right = min((left + 2 * window - 1), (n - 1))
            if mid < right:
                arr[left : right + 1] = merge(
                    arr[left : mid + 1], arr[mid + 1 : right + 1]
                )
        window *= 2
    return arr


def insertion_sort(arr: [], left: int, right: int):
    # insertion sort on slice of array arr[left:right]
    for i in range(left + 1, right + 1):
        key_item = arr[i]
        j = i - 1
        while j >= left and arr[j] > key_item:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item


def merge(arr1: [], arr2: []) -> []:
    # merge to sorted subarrays
    arr_merged = []
    i = j = 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            arr_merged.append(arr1[i])
            i += 1
        else:
            arr_merged.append(arr2[j])
            j += 1

    arr_merged.extend(arr1[i:])
    arr_merged.extend(arr2[j:])
    return arr_merged
