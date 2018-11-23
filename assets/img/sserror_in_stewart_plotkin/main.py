import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import imp

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")


def main():
    players = parameters.PLAYER_GROUPS["stewart_plotkin"]

    player_names = [s.name for s in players]

    df = pd.read_csv(
        "../../../data/processed/stewart_plotkin/std/per_opponent/main.csv"
    )
    df["Player name"] = df.apply(
        lambda row: player_names[row["Player index"]], axis=1
    )
    df["Extort"] = df["chi"] > 1
    df.sort_values("Win", ascending=False)

    summary_df = df.groupby("Player index")["Win", "Score"].sum()

    fig, axarr = plt.subplots(2, 2, figsize=(10, 10))

    for axrow, var, var_title, in zip(axarr, ("residual", "chi"), ("SSE", "$\chi$")):
        for ax, column in zip(axrow, ("Score", "Win")):

            sorted_indices = summary_df.sort_values(column, ascending=False).index
            data = [df[df["Player index"] == player_index][var] for player_index in sorted_indices]
            ax.violinplot(data)
            ax.boxplot(data)

            if var == "chi":
                ax.axhline(1, linestyle="--", color="black")

            sorted_players = [players[i].name for i in sorted_indices]
            ax.set_xlabel("Strategies")
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
