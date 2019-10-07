import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import skew

import imp

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")


def main():
    players = parameters.PLAYER_GROUPS["full"]
    player_names = [s.name for s in players]

    df = pd.read_csv("../../../data/processed/full/std/overall/main.csv")
    df["Name"] = df.apply(
        lambda row: player_names[row["Player index"]], axis=1
    )
    df["P(Win)"] = df["Win"] / (len(player_names) * parameters.REPETITIONS)
    df["Rank"] = df["Score"].rank(ascending=False).astype(int)

    df = pd.read_csv("../../../data/processed/full/std/per_opponent/main.csv")
    df["Name"] = df.apply(
        lambda row: player_names[row["Player index"]], axis=1
    )

    df["Extort"] = df["chi"] > 1
    df.sort_values("Win", ascending=True)

    summary_df = df.groupby("Player index")["Win", "Score"].sum()

    fig, axarr = plt.subplots(1, 2, figsize=(20, 7))
    X = range(1, len(players) + 1)

    for ax, column in zip(axarr, ("Score", "Win")):

        sorted_indices = summary_df.sort_values(column, ascending=False).index
        data = [df[df["Player index"] == player_index]["residual"] for player_index in sorted_indices]

        ax.scatter(X, list(map(skew, data)), color="black")
        ax.axhline(0, color="black", linestyle="--")

        ax.set_xlabel("Strategy ranks")
        if column == "Score":
            title = f"Skew of SSE sorted by score"
        else:
            title = f"Skew of SSE sorted by number of wins"
        ax.set_title(title, size=20)
    fig.tight_layout()

    fig.savefig("main.pdf")


if __name__ == "__main__":
    main()
