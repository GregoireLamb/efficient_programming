import os
import timeit
from typing import Callable, List

from datetime import datetime
import pandas as pd
from func_timeout import func_timeout, FunctionTimedOut

import numpy as np
import psutil
import pickle


class BenchmarkAnalyzer:
    def __init__(
        self, sort_function: Callable[[List[int]], List[int]], first_n_lists: int = None
    ):
        self._sort_function = sort_function
        self._first_n_lists = first_n_lists
        self._benchmark_instances_path = "../instances/benchmark_instances.pkl"

    def generate_benchmark_instances(self):
        a = 10
        b = 100000000
        sizes = [a]
        while a < b and len(sizes) < 20:
            a *= 2
            sizes.append(a)
        print(f"Sizes: {sizes}")
        benchmark_instances = []
        for size in sizes:
            instance = np.random.randint(0, 1000000, size).tolist()
            benchmark_instances.append(instance)

        print(f"Generated {len(benchmark_instances)} benchmark instances")

        # Save instances to file
        with open(self._benchmark_instances_path, "wb") as f:
            pickle.dump(benchmark_instances, f)

    def load_benchmark_instances(self):
        with open(self._benchmark_instances_path, "rb") as f:
            instances = pickle.load(f)

        if self._first_n_lists is not None:
            instances = instances[: self._first_n_lists]
        print(f"Loaded {len(instances)} benchmark instances")
        return instances

    def run_benchmark(self):
        instances = self.load_benchmark_instances()

        df_custom = self.run_benchmark_for_method(
            instances, method_name=self._sort_function.__name__
        )
        self._sort_function = sorted
        df_sorted = self.run_benchmark_for_method(instances, method_name=f"py_sort")
        df = pd.concat([df_custom, df_sorted])
        # If results dir does not exist, create it
        if not os.path.exists("../results"):
            os.makedirs("../results")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        df.to_csv(f"../results/benchmark_results_{timestamp}.csv", index=False)

        # Final results
        final_avg = self._print_final_results(df)
        return final_avg

    def run_n_benchmarks(self, n=10):
        res = {"elapsed_time": [], "cpu_time": [], "memory_usage": []}
        for i in range(n):
            print(f"Running benchmark {i + 1}/{n}")
            final_avg = self.run_benchmark()
            print(f"Final average: {final_avg}")
            res["elapsed_time"].append(final_avg["elapsed_time_rel_diff"])
            res["cpu_time"].append(final_avg["cpu_time_rel_diff"])
            res["memory_usage"].append(final_avg["memory_usage_rel_diff"])

        dashed_line = "-" * 50
        print(dashed_line)
        print(f'Average of relative_elapsed_time: {np.mean(res["elapsed_time"])}')
        print(f'Average of relative_cpu_time: {np.mean(res["cpu_time"])}')
        print(f'Average of relative_memory_usage: {np.mean(res["memory_usage"])}')

        print(f'Std of {n} relative_elapsed_time: {np.std(res["elapsed_time"])}')
        print(f'Std of {n} relative_cpu_time: {np.std(res["cpu_time"])}')
        print(f'Std of {n} relative_memory_usage: {np.std(res["memory_usage"])}')
        print(dashed_line)

    @staticmethod
    def _print_final_results(df):
        method_name = [a for a in df.method.unique() if a != "py_sort"][0]
        not_finished = df[(df.elapsed_time.isna()) & (method_name == df.method)]
        if len(not_finished) > 0:
            print(
                f"{method_name} could not sort {not_finished}/{len(df[df.method == method_name])} instances"
            )

        # Have method as a column for each instance, have (elapsed_time, cpu_time, memory_usage) as columns
        df = df.pivot(
            index="size",
            columns="method",
            values=["elapsed_time", "cpu_time", "memory_usage"],
        )
        # Compute the relative difference between the two methods
        df["elapsed_time_rel_diff"] = (
            df["elapsed_time"][method_name] / df["elapsed_time"]["py_sort"] - 1
        )
        df["cpu_time_rel_diff"] = (
            df["cpu_time"][method_name] / df["cpu_time"]["py_sort"] - 1
        )
        df["memory_usage_rel_diff"] = (
            df["memory_usage"][method_name] / df["memory_usage"]["py_sort"] - 1
        )

        # Print averages of relative differences
        dashed_line = "-" * 50
        print(dashed_line)
        print(f"Final results: {method_name} vs py_sort")
        print(dashed_line)
        print(f"Average relative differences for method {method_name}")

        final_averages = df[
            ["elapsed_time_rel_diff", "cpu_time_rel_diff", "memory_usage_rel_diff"]
        ].mean(numeric_only=True)
        print(f' -- Elapsed time: {final_averages["elapsed_time_rel_diff"]}')
        print(f' -- CPU time: {final_averages["cpu_time_rel_diff"]}')
        print(f' -- Memory usage: {final_averages["memory_usage_rel_diff"]}')
        print(dashed_line)

        return final_averages

    def run_benchmark_for_method(self, instances, method_name=None):
        results = {
            "method": [method_name if method_name is not None else "py_sorted"]
            * len(instances),
            "size": [len(instance) for instance in instances],
            "elapsed_time": [],
            "cpu_time": [],
            "memory_usage": [],
        }
        for i, instance in enumerate(instances):
            print(
                f"Running benchmark for instance {i + 1}/{len(instances)} of length {len(instance)}"
            )

            # Measure CPU time
            start_cpu_time = psutil.cpu_times()
            start_time = timeit.default_timer()

            try:
                # Run the sort function with a timeout of 10 seconds
                sorted_list = func_timeout(10, self._sort_function, args=(instance,))
                assert (
                    sorted(instance) == sorted_list
                ), f"Error in merge sort. Result is not sorted"
            except FunctionTimedOut:
                print("Sort function exceeded time limit of 10 seconds.")
                print(f" -- Elapsed time: TL")
                print(f" -- CPU time: TL")
                print(f" -- Memory used: NA")
                results["elapsed_time"].append(np.nan)
                results["cpu_time"].append(np.nan)
                results["memory_usage"].append(np.nan)
                continue

            # Measure elapsed time
            elapsed_time = timeit.default_timer() - start_time

            # Measure CPU time again and compute the difference
            end_cpu_time = psutil.cpu_times()
            cpu_time_diff = end_cpu_time.user - start_cpu_time.user

            # Measure memory usage
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()

            print(f" -- Elapsed time: {elapsed_time}")
            print(f" -- CPU time: {cpu_time_diff}")
            print(f" -- Memory used: {memory_info.rss}")

            results["elapsed_time"].append(elapsed_time)
            results["cpu_time"].append(cpu_time_diff)
            results["memory_usage"].append(memory_info.rss)

        return pd.DataFrame(results)


if __name__ == "__main__":
    from merge_sort import merge_sort

    benchmark_analyzer = BenchmarkAnalyzer(sorted, first_n_lists=10)
    # benchmark_analyzer.run_benchmark()
    benchmark_analyzer.run_n_benchmarks(5)
