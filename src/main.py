from merge_sort import merge_sort
from src.benchmark_analyzer import BenchmarkAnalyzer
from src.merge_sort import merge_sort
from src.parallel import Parallel
from src.inplace import merge_sort_inplace
from data_structures import merge_sort_ds


def main():
    # test = [50225, 53140, 253216, 401075, 561048, 773174, 812371, 817001, 938804, 961661]
    p = Parallel(4)
    benchmarkAnalyzer = BenchmarkAnalyzer(merge_sort_ds, first_n_lists=None)
    benchmarkAnalyzer.run_n_benchmarks(5)
    # p.para_merge_sort(test)


if __name__ == "__main__":
    main()
