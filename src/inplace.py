def merge_sort_inplace(arr, left=None, right=None):
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1

    if left < right:
        mid = left + (right - left) // 2
        merge_sort_inplace(arr, left, mid)
        merge_sort_inplace(arr, mid + 1, right)
        merge_inplace(arr, left, mid, right)


def merge_inplace(arr, left, mid, right):
    left_size = mid - left + 1
    right_size = right - mid

    left_temp = arr[left:mid + 1]
    right_temp = arr[mid + 1:right + 1]

    i, j, k = 0, 0, left

    while i < left_size and j < right_size:
        if left_temp[i] <= right_temp[j]:
            arr[k] = left_temp[i]
            i += 1
        else:
            arr[k] = right_temp[j]
            j += 1
        k += 1

    while i < left_size:
        arr[k] = left_temp[i]
        i += 1
        k += 1

    while j < right_size:
        arr[k] = right_temp[j]
        j += 1
        k += 1


if __name__ == "__main__":
    my_array = [38, 45, 43, 3, 9, 82, 10]
    qwerty = [38, 45, 43, 3, 9, 82, 10]

    merge_sort_inplace(my_array)
    assert my_array == sorted(qwerty)
    print(my_array)