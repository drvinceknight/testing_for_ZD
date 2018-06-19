import matplotlib.pyplot as plt

import pandas as pd
import numpy as np


def main():
    df = pd.read_csv("../../../data/processed/full/std/overall/main.csv")
    ranked_indices = list(map(int, (df["Score"].rank(method="first", ascending=False) - 1)))
    sorted_indices = sorted(range(len(ranked_indices)), key=lambda x:ranked_indices[x])

    df = pd.read_csv("../../../data/processed/full/std/per_opponent/main.csv")

    df["Extort"] = (df["complete"]) & (df["P(C|DD)"] == 0) & (df["chi"] > 1)
    delta_array = np.zeros((len(sorted_indices), len(sorted_indices)))
    probability_arrays = {"P(CC)": np.zeros((len(sorted_indices), len(sorted_indices))),
                          "P(CD)": np.zeros((len(sorted_indices), len(sorted_indices))),
                          "P(DC)": np.zeros((len(sorted_indices), len(sorted_indices))),
                          "P(DD)": np.zeros((len(sorted_indices), len(sorted_indices)))}

    delta_array.fill(np.nan)
    for array in probability_arrays.values():
        array.fill(np.nan)

    for index, row in df.iterrows():
        if row["Extort"]:
            delta_array[row["Player index"], row["Opponent index"]] = row["residual"]
        for state, array in probability_arrays.items():
            array[row["Player index"], row["Opponent index"]] = row[state]

    fig, axarr = plt.subplots(2, 2)

    axarr[0, 0].imshow(delta_array[sorted_indices][:,sorted_indices])
    axarr[0, 0].set_title("SSError")

    axarr[0, 1].imshow(probability_arrays["P(CC)"][sorted_indices][:,sorted_indices])
    axarr[0, 1].set_title("$P(CC)$")

    axarr[1, 0].imshow(probability_arrays["P(CD)"][sorted_indices][:,sorted_indices])
    axarr[1, 0].set_title("$P(CD)$")

    im = axarr[1, 1].imshow(probability_arrays["P(DD)"][sorted_indices][:,sorted_indices])
    axarr[1, 1].set_title("$P(DD)$")

    fig.tight_layout()
    fig.colorbar(im, ax=axarr)
    fig.savefig("main.pdf") 

if __name__ == "__main__":
    main()
