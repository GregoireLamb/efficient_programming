import os
import timeit
from typing import Callable, List

from datetime import datetime
import pandas as pd
from func_timeout import func_timeout

from merge_sort import merge_sort

import numpy as np
import psutil
import pickle


class BenchmarkAnalyzer:
    def __init__(self, function_to_assess: Callable[[List[int]], List[int]], first_n_lists: int = None,
                 baseline_function: Callable[[List[int]], List[int]] = merge_sort):
        self._sort_function = None
        self._function_to_assess = function_to_assess
        self._method_name = function_to_assess.__name__
        self._baseline_function = baseline_function
        self._first_n_lists = first_n_lists
        self._benchmark_instances_path = '../instances/benchmark_instances.pkl'

    def generate_benchmark_instances(self):
        a = 10
        b = 100000000
        sizes = [a]
        while a < b and len(sizes) < 20:
            a *= 2
            sizes.append(a)
        print(f'Sizes: {sizes}')
        benchmark_instances = []
        for size in sizes:
            instance = np.random.randint(0, 1000000, size).tolist()
            benchmark_instances.append(instance)

        print(f'Generated {len(benchmark_instances)} benchmark instances')

        # Save instances to file
        with open(self._benchmark_instances_path, 'wb') as f:
            pickle.dump(benchmark_instances, f)

    def load_benchmark_instances(self):
        with open(self._benchmark_instances_path, 'rb') as f:
            instances = pickle.load(f)

        if self._first_n_lists is not None:
            instances = instances[:self._first_n_lists]
        print(f'Loaded {len(instances)} benchmark instances')
        return instances

    def run_benchmark(self):
        instances = self.load_benchmark_instances()

        self._sort_function = self._function_to_assess
        df_custom = self.run_benchmark_for_method(instances, method_name=self._method_name)
        self._sort_function = sorted
        df_sorted = self.run_benchmark_for_method(instances, method_name=f'py_sort')
        self._sort_function = self._baseline_function
        df_baseline = self.run_benchmark_for_method(instances, method_name=f'baseline')
        df = pd.concat([df_custom, df_sorted, df_baseline])
        # If results dir does not exist, create it
        if not os.path.exists('../results'):
            os.makedirs('../results')
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        df.to_csv(f'../results/benchmark_results_{timestamp}.csv', index=False)

        # Final results
        final_avg = self._print_final_results(df)
        return final_avg

    def run_n_benchmarks(self, n=10):
        res = {
            'elapsed_time_pysort': [],
            'memory_usage_pysort': [],
            'elapsed_time_baseline': [],
            'memory_usage_baseline': []
        }
        for i in range(n):
            print(f'Running benchmark {i + 1}/{n}')
            final_avg = self.run_benchmark()
            print(f'Final average: {final_avg}')
            res['elapsed_time_pysort'].append(final_avg['elapsed_time_rel_diff_pysort'])
            res['memory_usage_pysort'].append(final_avg['memory_usage_rel_diff_pysort'])
            res['elapsed_time_baseline'].append(final_avg['elapsed_time_rel_diff_baseline'])
            res['memory_usage_baseline'].append(final_avg['memory_usage_rel_diff_baseline'])

        dashed_line = '-' * 50
        print(dashed_line)
        print(f'Average of relative_elapsed_time:\n'
              f'\tPySort {np.mean(res["elapsed_time_pysort"])}\n\tBaseline {np.mean(res["elapsed_time_baseline"])}')
        print(
            f'Average of relative_memory_usage: \n\tPySort {np.mean(res["memory_usage_pysort"])} \n\tBaseline {np.mean(res["memory_usage_baseline"])}')

        print(
            f'Std of {n} relative_elapsed_time: \n\tPySort {np.std(res["elapsed_time_pysort"])} \n\tBaseline {np.std(res["elapsed_time_baseline"])}')
        print(
            f'Std of {n} relative_memory_usage: \n\tPySort {np.std(res["memory_usage_pysort"])} \n\tBaseline {np.std(res["memory_usage_baseline"])}')
        print(dashed_line)

    def _print_final_results(self, df):
        not_finished = df[(df.elapsed_time.isna())]
        if len(not_finished) > 0:
            print(f'Following instances did not finish in time: \n{not_finished}')

        # Remove instances that did not finish in time
        df = df[(df.elapsed_time.notna())]

        # Have method as a column for each instance, have (elapsed_time, memory_usage) as columns
        df = df.pivot(index='size', columns='method', values=['elapsed_time', 'memory_usage'])
        # Compute the relative difference with py_sort
        df['elapsed_time_rel_diff_pysort'] = df['elapsed_time'][self._method_name] / df['elapsed_time']['py_sort'] - 1
        df['memory_usage_rel_diff_pysort'] = df['memory_usage'][self._method_name] / df['memory_usage']['py_sort'] - 1
        # Compute the relative difference with baseline
        df['elapsed_time_rel_diff_baseline'] = df['elapsed_time'][self._method_name] / df['elapsed_time']['baseline'] - 1
        df['memory_usage_rel_diff_baseline'] = df['memory_usage'][self._method_name] / df['memory_usage']['baseline'] - 1

        # Print averages of relative differences
        dashed_line = '-' * 50
        print(dashed_line)
        print(f'Final results: {self._method_name}')
        print(dashed_line)
        print(f'Average relative differences for method {self._method_name}')

        final_averages = (
            df[['elapsed_time_rel_diff_pysort', 'memory_usage_rel_diff_pysort',
                'elapsed_time_rel_diff_baseline', 'memory_usage_rel_diff_baseline']].mean(numeric_only=True))
        print(f' -- Against     : PySort         Baseline')
        print(f' -- Elapsed time: {final_averages["elapsed_time_rel_diff_pysort"].item():.4f},        '
              f'{final_averages["elapsed_time_rel_diff_baseline"].item():.4f}')
        print(f' -- Memory usage: {final_averages["memory_usage_rel_diff_pysort"].item():.4f},        '
              f'{final_averages["memory_usage_rel_diff_baseline"].item():.4f}')
        print(dashed_line)

        return final_averages

    def run_benchmark_for_method(self, instances, method_name=None):
        results = {
            'method': [method_name] * len(instances),
            'size': [len(instance) for instance in instances],
            'elapsed_time': [],
            'memory_usage': []
        }
        for i, instance in enumerate(instances):
            # print(f'Running benchmark for instance {i + 1}/{len(instances)} of length {len(instance)}')

            start_time = timeit.default_timer()

            try:
                # Run the sort function with a timeout of 10 seconds
                func_timeout(10, self._sort_function, args=(instance,))
            except Exception as e:
                pass

            # Measure elapsed time
            elapsed_time = timeit.default_timer() - start_time

            # Measure memory usage
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()

            # print(f" -- Elapsed time: {elapsed_time}")
            # print(f" -- Memory used: {memory_info.rss}")

            results['elapsed_time'].append(elapsed_time)
            results['memory_usage'].append(memory_info.rss)

        return pd.DataFrame(results)


if __name__ == '__main__':
    # from merge_sort import merge_sort
    from parallel import Parallel
    from inplace import merge_sort_inplace
    from merge_insert_sort import merge_insert_sort
    from data_structures import merge_sort_ds

    # set cpus as half of the available cpus
    cpus = psutil.cpu_count(logical=False) // 2 + 2

    benchmark_analyzer = BenchmarkAnalyzer(merge_sort_ds, first_n_lists=15)
    # benchmark_analyzer.run_benchmark()
    benchmark_analyzer.run_n_benchmarks(5)
