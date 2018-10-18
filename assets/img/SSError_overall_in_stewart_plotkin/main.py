import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import imp

parameters = imp.load_source('parameters',
                             '../../../data/raw/parameters.py')


def main(process_data=False):
    players = parameters.PLAYER_GROUPS["stewart_plotkin"]

    player_names = [s.name for s in players]

    if process_data:
        df = pd.read_csv("../../../data/processed/stewart_plotkin/std/overall/main.csv")
        df["Player name"] = df.apply(lambda row: player_names[row["Player index"]], axis=1)
        df["Extort"] = (df["complete"]) & (df["P(C|DD)"] == 0) & (df["chi"] > 1)
        df.sort_values("Win", ascending=False)
        df.to_csv("main.csv", index=False)
    else:
        df = pd.read_csv("main.csv")


    fig, axarr = plt.subplots(1, 2, figsize=(10, 5))


    for i, column in enumerate(("Score", "Win")):
        ax = axarr[i]
        x_tick_locations = range(1, len(players) + 1)

        for index, label, marker in zip([~df["Extort"], df["Extort"]],
                                        [r"$p_4 \ne 0$", "$p_4 = 0$"],
                                        ("o", "+")):
            ranks = df[column].rank(ascending=False, method="first")[df["complete"] & index]
            ax.scatter(ranks, df[df["complete"] & index]["residual"],
                       label=label,
                       marker=marker)
        sorted_indices = sorted(range(len(players)),
                                key=lambda index: -df[column].iloc[index])
        sorted_players = [players[i].name for i in sorted_indices]
        ax.set_xlabel("Strategies")
        ax.set_ylabel("SSerror$")
        ax.legend()
        ax.set_xticks(range(1, len(sorted_players) + 1))
        ax.set_xticklabels(sorted_players, rotation='vertical')
        if column == "Score":
            title = "Sorted by score"
        else:
            title = "Sorted by number of wins"
        ax.set_title(title)
        fig.tight_layout()

    fig.savefig("main.pdf")

if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
