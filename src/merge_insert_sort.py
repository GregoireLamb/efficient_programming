# Merge sort baseline implementation
def merge_insert_sort(arr, threshold: int = 10):
    if len(arr) <= 1:
        return arr

    elif len(arr) <= threshold:
        return insertionSort(arr)

    else:
        mid = len(arr) // 2
        left, right = merge_insert_sort(arr[:mid]), merge_insert_sort(arr[mid:])
        return merge_for_insertion(left, right, arr.copy())
#TODO merge two merge function


def merge_for_insertion(left, right, merged):
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
