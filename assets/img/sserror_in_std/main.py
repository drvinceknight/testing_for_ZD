import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
    df.sort_values("Win", ascending=False)

    summary_df = df.groupby("Player index")["Win", "Score"].sum()

    fig, axarr = plt.subplots(1, 2, figsize=(30, 35))

    for ax, column in zip(axarr, ("Score", "Win")):

        sorted_indices = summary_df.sort_values(column, ascending=False).index
        data = [df[df["Player index"] == player_index]["residual"] for player_index in sorted_indices]

        ax.violinplot(data, vert=False)
        ax.boxplot(data, vert=False, showmeans=True)

        sorted_players = [players[i].name for i in sorted_indices]
        ax.set_ylabel("Strategies")
        ax.set_yticks(range(1, len(sorted_players) + 1))
        ax.set_yticklabels(sorted_players)
        if column == "Score":
            title = f"SSE sorted by score"
        else:
            title = f"SSE sorted by number of wins"
        ax.set_title(title, size=20)
    fig.tight_layout()

    fig.savefig("main.pdf")


if __name__ == "__main__":
    main()
