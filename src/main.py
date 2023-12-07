from merge_sort import merge_sort
from src.benchmark_analyzer import BenchmarkAnalyzer
from src.parallel import Parallel


def main():
    # test = [50225, 53140, 253216, 401075, 561048, 773174, 812371, 817001, 938804, 961661]
    p = Parallel(4)
    benchmarkAnalyzer = BenchmarkAnalyzer(p.para_merge_sort, first_n_lists=10)
    benchmarkAnalyzer.run_n_benchmarks(5)
    # p.para_merge_sort(test)


if __name__ == "__main__":
    main()
