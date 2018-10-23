"""
Plot the measured probabilities versus the theoretic ones
"""
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import tqdm

import imp

import testzd as zd

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")


def main(process_data):

    if process_data:
        rates = ["P(C|CC)", "P(C|CD)", "P(C|DC)", "P(C|DD)"]
        probabilities = ["P(CC)", "P(CD)", "P(DC)", "P(DD)"]

        df = pd.concat(
            (
                pd.read_csv(
                    "../../../data/processed/full/std/per_opponent/main.csv"
                ),
                pd.read_csv(
                    "../../../data/processed/stewart_plotkin/std/per_opponent/main.csv"
                ),
            )
        )

        player_pair_vectors = {}
        player_pair_probabilities = {}
        for _, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
            pair = tuple(row[["Player index", "Opponent index"]])
            if pair[::-1] in player_pair_vectors:
                player_pair_vectors[pair[::-1]].append(tuple(row[rates]))
            else:
                player_pair_vectors[pair] = [tuple(row[rates])]
                player_pair_probabilities[pair] = tuple(row[probabilities])

        data = []
        player_pair_theoretic_probabilities = {}
        for i, j in player_pair_probabilities:

            try:
                p, q = player_pair_vectors[i, j]
            except ValueError:
                p = player_pair_vectors[i, j][0]
                q = p

            try:
                pi = zd.compute_pi(np.array(p), np.array(q))[:, 0]
            except np.linalg.LinAlgError:
                pi = [np.nan, np.nan, np.nan, np.nan]
            data.append([i, j, *pi, *player_pair_probabilities[i, j]])

        df = pd.DataFrame(
            data,
            columns=[
                "Player index",
                "Opponent index",
                "theoretic P(CC)",
                "theoretic P(CD)",
                "theoretic P(DC)",
                "theoretic P(DD)",
                "P(CC)",
                "P(CD)",
                "P(DC)",
                "P(DD)",
            ],
        )

        df.dropna(inplace=True)
        df.to_csv("main.csv", index=False)
    else:
        df = pd.read_csv("main.csv")

    fig, axarr = plt.subplots(nrows=2, ncols=2, sharex="col", sharey="row")
    index = (
        np.isfinite(df["P(CC)"])
        & np.isfinite(df["P(CD)"])
        & np.isfinite(df["P(DC)"])
        & np.isfinite(df["P(DD)"])
        & (df[f"theoretic P(CC)"] >= 0)
        & (df[f"theoretic P(CC)"] <= 1)
        & (df[f"theoretic P(CD)"] >= 0)
        & (df[f"theoretic P(CD)"] <= 1)
        & (df[f"theoretic P(DC)"] >= 0)
        & (df[f"theoretic P(DC)"] <= 1)
        & (df[f"theoretic P(DD)"] >= 0)
        & (df[f"theoretic P(DD)"] <= 1)
    )

    for i, state in enumerate(("CC", "CD", "DC", "DD")):
        ax = axarr[int(i / 2), i % 2]
        prob = f"P({state})"
        y = df[index][prob]
        x = df[index][f"theoretic {prob}"]
        ax.scatter(x, y, label=prob)

        x_for_model = sm.add_constant(x)
        model = sm.OLS(y, x_for_model)
        results = model.fit()
        b, a = results.params

        ax.plot([0, 1], [b, a + b], color="black")
        if i in [2, 3]:
            ax.set_xlabel("Computed probabilities")
        if i in [0, 2]:
            ax.set_ylabel("Measured probabilities")
        ax.set_title(
            f"P({state}) ($N={int(results.nobs)},\;R^2={round(results.rsquared, 3)}$)"
        )

    fig.tight_layout()
    fig.savefig("main.pdf")


if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
