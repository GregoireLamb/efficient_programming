def tim_sort(arr: [], min_run: int = 32) -> []:
    # Copy array to not sort inplace
    n = len(arr)

    if n <= 1:
        return arr

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


if __name__ == "__main__":
    test_list = [
        21,
        22,
        23,
        1,
        5,
        6,
        7,
        2,
        3,
        15,
        12,
        13,
        14,
        16,
        17,
        18,
        19,
        4,
        8,
        9,
        10,
        11,
        20,
        24,
        25,
    ]
    print(tim_sort(test_list))
