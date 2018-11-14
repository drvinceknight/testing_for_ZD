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
        mean_kappa = df.groupby("Player index")["kappa"].mean()
        std_kappa = df.groupby("Player index")["kappa"].std()
        median_kappa = df.groupby("Player index")["kappa"].median()
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
                "mean_kappa": mean_kappa,
                "median_kappa": median_kappa,
                "std_kappa": std_kappa,
                "mean_fixation": mean_fixation,
                "mean_fixation_N_two": mean_fixation_N_two,
                "mean_fixation_N_not_two": mean_fixation_N_not_two,
            }
        ).dropna()

        df.to_csv("main.csv")
    else:
        df = pd.read_csv("main.csv")

    fig, axarr = plt.subplots(3, 3, figsize=(20, 8))
    for axrow, title, col in zip(
        axarr,
        ("$2\leq N\leq 14$", "$N=2$", "$2<N\leq 14$"),
        ("mean_fixation", "mean_fixation_N_two", "mean_fixation_N_not_two"),
    ):
        for ax, var, xlabel in zip(
            axrow,
            ("mean_kappa", "median_kappa", "std_kappa"),
            (
                r"$\bar\kappa$ (mean)",
                r"$\tilde\kappa$ (median)",
                r"$\sigma_{\kappa}$ (standard deviation)",
            ),
        ):
            ax.scatter(df[var], df[col], color="black", marker="+")

            x = df[var]
            y = df[col]
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            ax.plot(df[var], slope * df[var] + intercept, color="black")
            ax.set_title(
                f"{title}: $y={slope:0.3f}x+{intercept:0.3f}$ ($p={p_value:0.3f}$, $R^2={round(r_value ** 2, 3)}$, $n={x.shape[0]}$)",
                size=13,
            )

            ax.set_xlabel(xlabel, fontsize=18)
            ax.set_ylabel(r"$\overline{(N\cdot x_1)}$ (mean)", fontsize=15)
            epsilon = 10 ** -3
            ax.set_ylim(np.min(df[col]) - epsilon, np.max(df[col]) + epsilon)
    fig.tight_layout()
    fig.savefig("main.pdf")


if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
