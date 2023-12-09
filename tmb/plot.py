from typing import Optional

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colors import BoundaryNorm

plt.rcParams["font.size"] = 6


def plot(df: pd.DataFrame, save_loc: Optional[str]):
    """
    Plots the availability of refuges over time.

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe containing the availability of refuges over time.
        Index are the refuges, columns are the dates, values are the
        number of available beds.
    save_loc: str
        Location to save the plot.
    """
    width, height = [v / 6 for v in df.T.shape]
    _, ax = plt.subplots(1, 1, figsize=(width, height))

    # Setup colormap encoding
    colors = ["red", "orange", "yellow", "green"]
    cmap = ListedColormap(colors)
    boundaries = [0, 1, 2, 6, df.values.max()]
    norm = BoundaryNorm(boundaries, cmap.N, clip=True)

    sns.heatmap(
        df,
        annot=True,
        fmt="d",
        cmap=cmap,
        norm=norm,
        linewidths=0.5,
        linecolor="black",
        ax=ax,
    )

    ax.set_title("Refuge availability")
    ax.set_ylabel("Place")
    ax.set_xlabel("Date")

    if save_loc:
        plt.savefig(save_loc, dpi=300, bbox_inches="tight")
    else:
        plt.show()
