import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def generate_histograms(prefix="method", metric="elapsed_time", csv_path='../results/para.csv', parallel=False):
    # import results/all.csv as df
    df = pd.read_csv(csv_path)

    # keep only the columns we need
    if parallel:
        df = df[['size', metric, 'method', 'cores']]
        df['method'] = df.apply(lambda row: f'{row["method"]} ({row["cores"]} cores)' if row["method"] == "para_merge_sort" else row["method"], axis=1)

    df = df[['size', metric, 'method']]
    df = df.groupby(['size', 'method']).mean().reset_index()


    df['size'] = df['size'].astype('category')


    # Might change merge_sort to Baseline (depend on the bencmark)
    #baseline_times = df[df['method'] == 'merge_sort'].set_index('size')[metric]
    baseline_times = df[df['method'] == 'baseline'].groupby('size')['elapsed_time'].mean()

    df['relative_improvement'] = df.apply(lambda row: (row[metric] / baseline_times[row['size']] - 1), axis=1)

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # Create the histogram for absolute values
    sns.barplot(x="size", y=metric, hue="method", data=df)
    plt.xlabel("Size")
    plt.xticks(rotation=45)
    plt.ylabel("Elapsed Time")
    plt.title("Histogram of Elapsed Time")
    plt.savefig(f'../hists/{metric}_absolute_{prefix}.png')
    plt.show()
    # save the plot

    # Create the histogram for relative values
    sns.barplot(x="size", y="relative_improvement", hue="method", data=df)
    plt.xlabel("Size")
    plt.xticks(rotation=45)
    plt.ylabel("Relative Difference with Baseline")
    plt.title("Histogram of Elapsed Time Relative Difference with Baseline")
    plt.savefig(f'../hists/{metric}_relative_{prefix}.png')
    plt.show()

    # Create the histogram for relative values Zoom in
    sns.barplot(x="size", y="relative_improvement", hue="method", data=df)
    plt.xlabel("Size")
    plt.xticks(rotation=45)
    plt.ylim(-1.2, 2)
    plt.ylabel("Relative Difference with Baseline")
    plt.title("Histogram of Elapsed Time Relative Difference with Baseline")
    plt.savefig(f'../hists/{metric}_rel_zoom_{prefix}.png')
    plt.show()


if __name__ == "__main__":
    generate_histograms(prefix="data_structures", metric='elapsed_time', csv_path='../results/benchmark_results_2023-12-13_16-30-15.csv', parallel=False)
#results\benchmark_results_2023-12-13_16-30-15.csv
#results\benchmark_results_2023-12-13_16-29-24.csv
