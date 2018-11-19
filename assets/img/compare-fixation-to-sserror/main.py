import sys
import imp

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import linregress

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")
player_names = [
    player.__repr__() for player in parameters.PLAYER_GROUPS["full"]
]


def find_index(name, player_names=player_names):
    try:
        return int(player_names.index(name))
    except ValueError:
        return -1


def main(process_data=False):
    if process_data:
        df = pd.read_csv(
            "../../../data/processed/full/std/per_opponent/main.csv"
        )

        moran_df = pd.read_csv("data/main.csv")
        moran_df["Player index"] = moran_df["player"].map(find_index)
        moran_df["Opponent index"] = moran_df["opponent"].map(find_index)
        moran_df["Normalised fixation"] = moran_df["$p_1$"] * moran_df["N"]

        df = moran_df.merge(
            df, on=("Player index", "Opponent index"), how="right"
        )
        mean_sserror = df.groupby("Player index")["residual"].mean()
        var_sserror = df.groupby("Player index")["residual"].var()
        mean_fixation = df.groupby("Player index")["Normalised fixation"].mean()
        mean_fixation_N_two = (
            df[df["N"] == 2]
            .groupby("Player index")["Normalised fixation"]
            .mean()
        )
        mean_fixation_N_not_two = (
            df[df["N"] != 2]
            .groupby("Player index")["Normalised fixation"]
            .mean()
        )
        mean_fixation_N_four = (
            df[df["N"] == 4]
            .groupby("Player index")["Normalised fixation"]
            .mean()
        )
        mean_fixation_N_six = (
            df[df["N"] == 6]
            .groupby("Player index")["Normalised fixation"]
            .mean()
        )
        mean_fixation_N_eight = (
            df[df["N"] == 8]
            .groupby("Player index")["Normalised fixation"]
            .mean()
        )
        mean_fixation_N_ten = (
            df[df["N"] == 10]
            .groupby("Player index")["Normalised fixation"]
            .mean()
        )
        mean_fixation_N_twelve = (
            df[df["N"] == 12]
            .groupby("Player index")["Normalised fixation"]
            .mean()
        )
        mean_fixation_N_fourteen = (
            df[df["N"] == 14]
            .groupby("Player index")["Normalised fixation"]
            .mean()
        )

        df = pd.DataFrame(
            {
                "mean_sserror": mean_sserror,
                "var_sserror": var_sserror,
                "mean_fixation": mean_fixation,
                "mean_fixation_N_two": mean_fixation_N_two,
                "mean_fixation_N_not_two": mean_fixation_N_not_two,
            }
        ).dropna()

        df.to_csv("main.csv")
    else:
        df = pd.read_csv("main.csv")

    fig, axarr = plt.subplots(2, 2, figsize=(20, 8))
    for axrow, title, col in zip(
        axarr,
        ("$N=2$", "$2<N\leq 14$"),
        ("mean_fixation_N_two", "mean_fixation_N_not_two"),
    ):
        y = df[col]
        for ax, var, xlabel in zip(
            axrow,
            ("mean_sserror", "var_sserror"),
            (
                r"Mean SSerror",
                r"Variance SSerror",
            ),
        ):
            x = df[var]
            ax.scatter(x, y, color="black", marker="+")

            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            ax.plot(x, slope * x + intercept, color="black")
            ax.set_title(
                f"{title}: $y={slope:0.3f}x+{intercept:0.3f}$ ($p={p_value:0.3f}$, $R^2={round(r_value ** 2, 3)}$, $n={x.shape[0]}$)",
                size=13,
            )

            ax.set_xlabel(xlabel, fontsize=18)
            ax.set_ylabel(r"Mean $(N\cdot x_1)$", fontsize=15)
            epsilon = 10 ** -3
            ax.set_ylim(np.min(df[col]) - epsilon, np.max(df[col]) + epsilon)
    fig.tight_layout()
    fig.savefig("main.pdf")


if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
