RUN = 32  # defines threshold for running insertion sort on subsets


def merge_insert_sort(arr: [], min_run=RUN):
    """Hybrid Implementation of mergesort and insertion sort"""

    n = len(arr)

    # sort smaller subarrays independently with insertion sort
    for idx in range(0, n, min_run):
        insertion_sort(arr, idx, min((idx + min_run - 1), n - 1))

    # Merges every subarray using Merge Sort
    while min_run < n:
        left = 0

        while left < n:
            mid = min(left + size - 1, n - 1)
            right = min(left + 2 * size - 1, n - 1)

            merge(arr, left, mid, right)

            left += size * 2

        size *= 2

    return arr


def insertion_sort(arr: [], left: int, right: int):
    if right is None:
        right = len(arr) - 1

    for i in range(left + 1, right + 1):
        key_item = arr[i]
        j = i - 1
        while j >= left and arr[j] > key_item:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item


def merge(unsorted: [], left: int, middle: int, right: int) -> None:
    len1 = middle - left + 1
    len2 = right - middle
    left_side = unsorted[left : middle + 1]
    right_side = unsorted[middle + 1 : right + 1]

    i = j = 0
    k = left
    out = []
    while i < len1 and j < len2:
        if left_side[i] <= right_side[j]:
            out.append(left_side[i])
            i += 1
        else:
            out.append(right_side[j])
            j += 1
        k += 1
    out.extend(left_side[i:])
    out.extend(right_side[j:])
    unsorted[:] = out


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
    print(merge_insert_sort(test_list))
