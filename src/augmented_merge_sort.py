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
            return insertionSort(arr)
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
def merge_insert_sort(arr, threshold: int = 10):
    if len(arr) <= 1:
        return arr

    elif len(arr) <= threshold:
        return insertionSort(arr)

    else:
        mid = len(arr) // 2
        left, right = merge_insert_sort(arr[:mid]), merge_insert_sort(arr[mid:])
        return merge(left, right, arr.copy())


def merge(left, right, merged):
    left_cursor, right_cursor = 0, 0
    while left_cursor < len(left) and right_cursor < len(right):
        if left[left_cursor] <= right[right_cursor]:
            merged[left_cursor + right_cursor] = left[left_cursor]
            left_cursor += 1
        else:
            merged[left_cursor + right_cursor] = right[right_cursor]
            right_cursor += 1
    for left_cursor in range(left_cursor, len(left)):
        merged[left_cursor + right_cursor] = left[left_cursor]
    for right_cursor in range(right_cursor, len(right)):
        merged[left_cursor + right_cursor] = right[right_cursor]
    return merged


# Insertion sort in Python


def insertionSort(arr):
    for step in range(1, len(arr)):
        key = arr[step]
        j = step - 1

        # Compare key with each element on the left of it until an element smaller than it is found
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j = j - 1

        # Place key at after the element just smaller than it.
        arr[j + 1] = key
    return arr


if __name__ == "__main__":
    my_array = [38, 45, 43, 3, 9, 82, 10]
    qwerty = [38, 45, 43, 3, 9, 82, 10]

    my_array = AugmentedMergeSort(4).augmented_merge_sort(my_array)
    assert my_array == sorted(qwerty), "Arrays are not equal: {} != {}".format(my_array, sorted(qwerty))
    print(my_array)
