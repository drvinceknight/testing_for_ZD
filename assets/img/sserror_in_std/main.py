import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import skew

import imp

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")


def main():
    player_names = [s.name for s in parameters.PLAYER_GROUPS["full"]]
    df = pd.read_csv("../../../data/processed/full/std/overall/main.csv")
    df["Score per turn"] = df["Score"] / (
        parameters.TURNS * parameters.REPETITIONS * (len(player_names))
    )
    df["Name"] = player_names
    df["P(Win)"] = df["Win"] / (len(player_names) * parameters.REPETITIONS)
    sserror = df["residual"].round(4)
    df["residual"] = sserror

    columns = ["Name", "Score per turn", "P(Win)"]
    df = df[columns]

    per_opponent_df = pd.read_csv(
        "../../../data/processed/full/std/per_opponent/main.csv"
    )
    skewness = per_opponent_df.groupby("Player index")["residual"].skew()
    df["Skew"] = skewness

    fig, axarr = plt.subplots(1, 2, figsize=(10, 4))
    for ax, column in zip(axarr, ("Score per turn", "P(Win)")):

        ax.scatter(df[column], df["Skew"], color="black")
        ax.axhline(0, color="black", linestyle="--")

        ax.set_xlabel(f"{column}")
        if column == "Score per turn":
            title = f"Skew of SSE against score"
        else:
            title = f"Skew of SSE against number of wins"
        ax.set_title(title)
    fig.tight_layout()

    fig.savefig("main.pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
