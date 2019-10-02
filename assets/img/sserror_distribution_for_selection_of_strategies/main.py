import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import skew

import imp

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")
selection_of_players = ["EvolvedLookerUp2_2_2",
        "Tit For Tat",
        "ZD-Extort-2"
        ]

def main():
    players = parameters.PLAYER_GROUPS["full"]
    player_names = [s.name for s in players]
    df = pd.read_csv("../../../data/processed/full/std/per_opponent/main.csv")
    df["Name"] = df.apply(
        lambda row: player_names[row["Player index"]], axis=1
    )

    df = df[df["Name"].isin(selection_of_players)]

    fig, axarr = plt.subplots(1, 3, figsize=(25, 5))

    for ax, name in zip(axarr, selection_of_players):

        data = df[df["Name"] == name]["residual"] 

        ax.hist(data, bins=20, color="black")

        ax.set_title(f"SSE distribution for {name}", size=20)
        ax.set_xlabel("SSE")
        ax.set_ylabel("Count")
    fig.tight_layout()

    fig.savefig("main.pdf")


if __name__ == "__main__":
    main()
