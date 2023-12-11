# Optimizing Merge Sort

**Course**: 185.190 Efficient Programs

**Team Members**: 
  - Grégoire de Lambertye 
  - Joan Salvà
  - Bernardo Aceves
  - Antone Melone
  - Aleksandar Manov

## Project Description

In this project, our objective is to enhance the performance of a baseline merge sort algorithm. We will explore a variety of methods and thoroughly evaluate their effectiveness.

## How to develop

1. Clone the repository
2. Create a python virtual environment (conda, venv, etc.)
3. Install the requirements: `pip install -r requirements.txt`
4. Try to run the main file, it is just a simple test of the sort function: `python src/main.py`
5. **Create a new branch!!** This is key. Do not code in the main branch.
6. Develop your code in the new branch. For this, you should modify the merge_sort function in the `merge_sort.py` file. You can also add new files if you need to.
7. How to test it: use the benchmarking script `benchmark.py`.
   - It will run the merge sort function with different input sizes and different number of repetitions.
   - It will also run the baseline merge sort function and compare the results.
   - ``BenchmarkAnalyzer.run_benchmark()`` will run the benchmark and save the results in a csv file.
   - ``BenchmarkAnalyzer.run_n_benchmarks(n)`` will run the benchmark n times and save the results in a csv file (separately). It also prints averages and std.
8. You should not change the benchmarking script. If you need to change something, please discuss it with the team.
9. Let's discuss on **Monday** how everything is going! It would be good to already have the results of how improvements work
