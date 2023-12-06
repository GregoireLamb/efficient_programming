from merge_sort import merge_sort


def main():
    test_list = [21, 22, 23, 1, 5, 6, 7, 2, 3, 15, 12, 13, 14, 16, 17, 18, 19, 4, 8, 9, 10, 11, 20, 24, 25]
    print("Unsorted list: ", test_list)
    sorted_list = merge_sort(test_list)
    print("Sorted list: ", sorted_list)

    assert sorted(test_list) == sorted_list, f'Error in merge sort. Result is not sorted'


if __name__ == "__main__":
    main()
