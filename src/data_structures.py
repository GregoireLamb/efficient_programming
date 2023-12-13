import numpy as np

def merge_sort_ds(arr):
    arr = np.array(arr)
    if len(arr) <= 1:
        return arr.tolist()  
    mid = len(arr) // 2
    left, right = merge_sort_ds(arr[:mid]), merge_sort_ds(arr[mid:])
    return merge_ds(left, right)

def merge_ds(left, right):
    merged = []
    left_cursor, right_cursor = 0, 0
    while left_cursor < len(left) and right_cursor < len(right):
        if left[left_cursor] <= right[right_cursor]:
            merged.append(left[left_cursor])
            left_cursor += 1
        else:
            merged.append(right[right_cursor])
            right_cursor += 1
    merged.extend(left[left_cursor:])
    merged.extend(right[right_cursor:])
    return merged