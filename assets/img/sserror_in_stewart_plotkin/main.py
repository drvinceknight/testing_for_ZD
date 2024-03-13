import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import skew

import imp

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")


def main():
    players = parameters.PLAYER_GROUPS["stewart_plotkin"]

    player_names = [s.name for s in players]

    df = pd.read_csv(
        "../../../data/processed/stewart_plotkin/std/per_opponent/main.csv"
    )
    df["Player name"] = df.apply(lambda row: player_names[row["Player index"]], axis=1)
    df["Extort"] = df["chi"] > 1
    df.sort_values("Win", ascending=False)

    summary_df = df.groupby("Player index")["Win", "Score"].sum()
    X = range(1, len(players) + 1)

    plt.rcParams.update({"font.size": 14})
    fig, axarr = plt.subplots(2, 2, figsize=(10, 10))

    for (
        axrow,
        var,
        var_title,
    ) in zip(axarr, ("residual", "chi"), ("SSE", "Mean $\chi$")):
        for ax, column in zip(axrow, ("Score", "Win")):
            sorted_indices = summary_df.sort_values(column, ascending=False).index
            data = [
                df[df["Player index"] == player_index][var]
                for player_index in sorted_indices
            ]

            if var == "chi":
                ax.axhline(1, linestyle="--", color="black")
                ax.scatter(X, list(map(np.mean, data)), color="black")
            else:
                ax.scatter(X, list(map(np.mean, data)), color="black", label="Mean")
                ax.scatter(
                    X, list(map(skew, data)), color="black", marker="+", label="Skew"
                )
                ax.axhline(0, color="black", linestyle="--")
                ax.legend()

            sorted_players = [players[i].name for i in sorted_indices]
            ax.set_xlabel("Strategies")
            ax.set_ylabel(var_title)
            ax.set_xticks(range(1, len(sorted_players) + 1))
            ax.set_xticklabels(sorted_players, rotation="vertical")
            if column == "Score":
                title = f"{var_title} sorted by score"
            else:
                title = f"{var_title} sorted by number of wins"
            ax.set_title(title)
        fig.tight_layout()

    fig.savefig("main.pdf")


if __name__ == "__main__":
    main()
