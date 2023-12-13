import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def generate_histograms(prefix="method", csv_path='../results/para.csv', parallel=False):
    # import results/all.csv as df
    df = pd.read_csv(csv_path)

    # keep only the columns we need
    if parallel:
        df = df[['size', 'elapsed_time', 'method', 'cores']]
        df['method'] = df.apply(lambda row: f'{row["method"]} ({row["cores"]} cores)' if row["method"] == "para_merge_sort" else row["method"], axis=1)

    df = df[['size', 'elapsed_time', 'method']]
    df = df.groupby(['size', 'method']).mean().reset_index()


    df['size'] = df['size'].astype('category')


    baseline_times = df[df['method'] == 'baseline'].set_index('size')['elapsed_time']
    df['relative_improvement'] = df.apply(lambda row: (row['elapsed_time'] / baseline_times[row['size']] - 1), axis=1)

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # Create the histogram for absolute values
    sns.barplot(x="size", y="elapsed_time", hue="method", data=df)
    plt.xlabel("Size")
    plt.xticks(rotation=45)
    plt.ylabel("Elapsed Time")
    plt.title("Histogram of Elapsed Time")
    plt.savefig(f'../hists/elapsed_time_absolute_{prefix}.png')
    plt.show()
    # save the plot

    # Create the histogram for relative values
    sns.barplot(x="size", y="relative_improvement", hue="method", data=df)
    plt.xlabel("Size")
    plt.xticks(rotation=45)
    plt.ylabel("Relative Difference with Baseline")
    plt.title("Histogram of Elapsed Time Relative Difference with Baseline")
    plt.savefig(f'../hists/elapsed_time_relative_{prefix}.png')
    plt.show()

    # Create the histogram for relative values Zoom in
    sns.barplot(x="size", y="relative_improvement", hue="method", data=df)
    plt.xlabel("Size")
    plt.xticks(rotation=45)
    plt.ylim(-1.2, 2)
    plt.ylabel("Relative Difference with Baseline")
    plt.title("Histogram of Elapsed Time Relative Difference with Baseline")
    plt.savefig(f'../hists/elapsed_time_rel_zoom_{prefix}.png')
    plt.show()


if __name__ == "__main__":
    generate_histograms(prefix="parallel", csv_path='../results/para4c.csv', parallel=False)
