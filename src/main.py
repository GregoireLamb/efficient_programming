from merge_sort import merge_sort
from src.benchmark_analyzer import BenchmarkAnalyzer
from src.parallel import Parallel


def main():
    test_list = [21, 22, 23, 1, 5, 6, 7, 2, 3, 15, 12, 13, 14, 16, 17, 18, 19, 4, 8, 9, 10, 11, 20, 24, 25]
    # print("Unsorted list: ", test_list)
    # sorted_list = merge_sort(test_list)
    # print("Sorted list: ", sorted_list)
    #
    # assert sorted(test_list) == sorted_list, f'Error in merge sort. Result is not sorted'

    p = Parallel(4)
    BenchmarkAnalyzer.run_benchmark(p.para_merge_sort(test_list))
    # p.para_merge_sort(test_list)
    # p2 = Parallel(0)
    # p3 = Parallel(-1)
    # p4 = Parallel(100)

if __name__ == "__main__":
    main()
