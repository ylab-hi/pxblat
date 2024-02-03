import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rc

rc("font", weight="bold")


def main():
    """Plot the performance comparison between PxBLAT and BLAT."""
    data_df = pd.read_csv("./performance_table.tsv", sep="\t")
    data = data_df["Data"]
    pxblat = data_df["PxBLAT (s)"]
    blat = data_df["BLAT (s)"]

    # Creating scatter plot
    plt.scatter(x=data, y=pxblat, alpha=0.5, color="blue", label="PxBLAT")
    plt.scatter(x=data, y=blat, alpha=0.5, color="red", label="BLAT")

    # Calculating trend lines
    z_pxblat = np.polyfit(data, pxblat, 1)
    p_pxblat = np.poly1d(z_pxblat)
    plt.plot(data, p_pxblat(data), "b--", linewidth=1.2, markersize=12)

    z_blat = np.polyfit(data, blat, 1)
    p_blat = np.poly1d(z_blat)
    plt.plot(data, p_blat(data), "r--", linewidth=1.2, markersize=12)

    # Calculate and annotate average speedup for each data group
    avg_speedup_per_data_group = data_df.groupby("Data")["Speedup"].mean()
    for data_point, avg_speedup in avg_speedup_per_data_group.items():
        plt.annotate(
            f"{avg_speedup:.2f}x",
            (data_point, min(data_df[data_df["Data"] == data_point]["PxBLAT (s)"])),
            textcoords="offset points",
            xytext=(0, -12),
            ha="center",
            fontsize=8,
            color="darkgreen",
        )

    plt.xticks([50, 100, 200, 300, 400, 500, 600])
    plt.ylim(0, 200)

    plt.xlabel("Data")
    plt.ylabel("Time (s)")
    plt.legend(loc="upper left")

    # Displaying the plot
    plt.savefig("performance.png", format="png", bbox_inches="tight", dpi=300)
    plt.close()


if __name__ == "__main__":
    main()
