import numpy as np

def merge_sort_ds(arr):
    arr = np.array(arr)
    if len(arr) <= 1:
        return arr.tolist()  # Convert back to a list for consistency with the input type
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

# # Example usage:
# arr = [38, 27, 43, 3, 9, 82, 10]
# sorted_arr = merge_sort(arr)
# print(sorted_arr)


# The input array is converted to a NumPy array at the beginning of the merge_sort function for better array manipulation and performance.
# The merge function now uses a list for the merged result instead of modifying the input array in place. This improves readability and avoids the need for copying the input array.
# Instead of using array slices, the extend method is used to append the remaining elements of left and right to the merged list.
# The final sorted result is converted back to a list before returning for consistency with the input type.