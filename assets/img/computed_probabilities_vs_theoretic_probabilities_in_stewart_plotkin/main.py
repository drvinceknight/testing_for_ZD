"""
Plot the measured probabilities versus the theoretic ones
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

import imp

import testzd as zd

parameters = imp.load_source('parameters',
                             '../../../data/raw/parameters.py')

def main():

    players = parameters.PLAYER_GROUPS["stewart_plotkin"]

    player_names = [s.name for s in players]
    rates = ["P(C|CC)", "P(C|CD)", "P(C|DC)", "P(C|DD)"]
    probabilities = ["P(CC)", "P(CD)", "P(DC)", "P(DD)"]

    df = pd.read_csv("../../../data/processed/stewart_plotkin/std/per_opponent/main.csv")

    player_pair_vectors = {}
    player_pair_probabilities = {}
    for _, row in df.iterrows():
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

    df = pd.DataFrame(data, columns=["Player index",
                                     "Opponent index",
                                     "theoretic P(CC)",
                                     "theoretic P(CD)",
                                     "theoretic P(DC)",
                                     "theoretic P(DD)",
                                     "P(CC)",
                                     "P(CD)",
                                     "P(DC)",
                                     "P(DD)",
                                    ])

    df.dropna(inplace=True)

    fig, axarr = plt.subplots(2, 2)
    for i, state in enumerate(("CC", "CD", "DC", "DD")):
        ax = axarr[int(i / 2), i % 2]
        prob = f"P({state})"
        index = np.isfinite(df[prob]) & (df[f"theoretic {prob}"] >= 0) & (df[f"theoretic {prob}"] <= 1)
        y = df[index][prob]
        x = df[index][f"theoretic {prob}"]
        ax.scatter(x, y, label=prob)

        x_for_model = sm.add_constant(x)
        model = sm.OLS(y, x_for_model)
        results = model.fit()
        b, a = results.params

        ax.plot([0, 1], [b, a + b], color="black")
        ax.set_xlabel("Computed probabilities")
        ax.set_ylabel("Measured probabilities")
        ax.set_title(f"P({state}) ($N={int(results.nobs)},\;R^2={round(results.rsquared, 3)}$)")

    fig.tight_layout()
    fig.savefig("main.pdf")

if __name__ == "__main__":
    main()
