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

    strategies_of_interest = [
        "ZD-GTFT-2",
        "ZD-GEN-2",
        "ZD-Extort-2",
        "EvolvedLookerUp2_2_2",
        "Evolved ANN 5",
        "Tit For Tat",
        "Win-Stay Lose-Shift",
    ]
    df = pd.read_csv("../../../data/processed/full/std/overall/main.csv")
    df["Name"] = df.apply(
        lambda row: player_names[row["Player index"]], axis=1
    )
    df["P(Win)"] = df["Win"] / (len(player_names) * parameters.REPETITIONS)
    df["Rank"] = df["Score"].rank(ascending=False).astype(int)

    strategies_of_interest += list(df.sort_values("residual").head(5)["Name"])
    strategies_of_interest += list(df.sort_values("residual").tail(5)["Name"])
    strategies_of_interest += list(df.sort_values("P(Win)").tail(2)["Name"])
    strategies_of_interest += list(df.sort_values("P(CC)").tail(2)["Name"])
    strategies_of_interest += list(df.sort_values("Score").head(5)["Name"])
    strategies_of_interest += list(df.sort_values("Score").tail(5)["Name"])

    df = pd.read_csv("../../../data/processed/full/std/per_opponent/main.csv")
    df["Name"] = df.apply(
        lambda row: player_names[row["Player index"]], axis=1
    )
    df = df[df["Name"].isin(strategies_of_interest)]

    df["Extort"] = df["chi"] > 1
    df.sort_values("Win", ascending=False)

    summary_df = df.groupby("Player index")["Win", "Score"].sum()
    X = range(1, len(set(strategies_of_interest)) + 1)

    fig, axarr = plt.subplots(1, 2, figsize=(10, 5))

    for ax, column in zip(axarr, ("Score", "Win")):

        sorted_indices = summary_df.sort_values(column, ascending=False).index
        data = [df[df["Player index"] == player_index]["residual"] for player_index in sorted_indices]

        ax.scatter(X, list(map(np.mean, data)), color="black", label="Mean")
        ax.scatter(X, list(map(skew, data)), color="black", marker="+", label="Skew")
        ax.axhline(0, color="black", linestyle="--")
        ax.legend()

        sorted_players = [players[i].name for i in sorted_indices]
        ax.set_xlabel("Strategies")
        ax.set_xticks(X)
        ax.set_xticklabels(sorted_players, rotation="vertical")
        if column == "Score":
            title = f"SSE sorted by score"
        else:
            title = f"SSE sorted by number of wins"
        ax.set_title(title)
    fig.tight_layout()

    fig.savefig("main.pdf")


if __name__ == "__main__":
    main()
