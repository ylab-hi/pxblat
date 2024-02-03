from pathlib import Path

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import rc

rc("font", weight="bold")


def get_fa_seq_len(file: Path):
    """Get the length of the sequence in a fasta file."""
    with file.open() as f:
        content = f.readlines()
        seq = content[1]
        return len(seq)


def collect_fa_len(data_dirs):
    """Collect the length of the sequences in the fasta files."""
    result = {}
    for dir in data_dirs:
        for fa in Path(dir).glob("*fa"):
            result[fa.stem] = get_fa_seq_len(fa)
    return result


def plot_fas_len(data_dirs, file_name, figure_size=(20, 20)):
    """Plot the length of the sequences in the fasta files."""
    # plt.rc("font", family="Arial")

    fig, axs = plt.subplots(3, 3, figsize=figure_size)
    axs = axs.flatten()
    tick_labelsize = 14
    labelsize = 18
    titlesize = 18
    color = "tab:cyan"
    numbers = ["a", "b", "c", "d", "e", "f", "g"]

    for ind, data in enumerate(data_dirs):
        sample = data.name.split("_")[1]
        fa_len = collect_fa_len([data])
        ax = axs[ind]

        # Hide the right and top spines
        # sns.kdeplot(x = list(fa_len.values()), fill=True, color=color, ax=ax)
        sns.histplot(
            x=list(fa_len.values()),
            color=color,
            binwidth=40,
            ax=ax,
        )

        # ax.axhline(0, color="k", clip_on=False)
        _ = ax.set_xlabel(r"Length of Fasta Data", fontsize=labelsize)
        _ = ax.set_ylabel(r"Count", fontsize=labelsize)
        ax.set_title(f"{sample} samples", {"fontsize": titlesize})
        # ax.set_yticks(list(range(0, 12, 2)))
        ax.tick_params(axis="y", labelsize=tick_labelsize)
        ax.tick_params(axis="x", labelsize=tick_labelsize)
        ax.text(
            ax.get_xlim()[0] - 100,
            ax.get_ylim()[1] * 1.1,
            f"{numbers[ind]}",
            fontsize=28,
        )

    # Finalize the plot
    for a in axs[ind + 1 :]:
        a.set_visible(False)
    sns.despine()
    plt.tight_layout()
    # _ = ax1.set_ylim(0, 200)
    # plt.xticks(rotation=30)

    plt.savefig(f"{file_name}", bbox_inches="tight", dpi=300)
    plt.close()


def main():
    range_data = Path("../benchmark/fas/")
    range_folders = [i for i in range_data.glob("range_*") if i.is_dir()]
    [i.stem for i in Path("../benchmark/fas/range_600").rglob("*fa")]
    pd.read_csv("benchmark_fas_all_chps.txt", header=None, sep="\t")

    range_folders.sort(key=lambda x: int(x.name.split("_")[1]))
    plot_fas_len(range_folders, "fas_len_ranges.png")


if __name__ == "__main__":
    main()
