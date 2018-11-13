import sys
import pathlib

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import numpy as np
import tqdm


def get_sorted_indices(df, column):
    ranked_indices = list(
        map(int, (df[column].rank(method="first", ascending=False) - 1))
    )
    return sorted(range(len(ranked_indices)), key=lambda x: ranked_indices[x])


def main(process_data=False):
    if process_data:
        overall_df = pd.read_csv(
            "../../../data/processed/full/std/overall/main.csv"
        )
        df = pd.read_csv(
            "../../../data/processed/full/std/per_opponent/main.csv"
        )

        df["Extort"] = df["chi"] > 1

        number_of_players = len(overall_df.index)
        kappa_array = np.zeros((number_of_players, number_of_players))
        probability_arrays = {
            "P(CC)": np.zeros((number_of_players, number_of_players)),
            "P(CD)": np.zeros((number_of_players, number_of_players)),
            "P(DC)": np.zeros((number_of_players, number_of_players)),
            "P(DD)": np.zeros((number_of_players, number_of_players)),
        }

        kappa_array.fill(np.nan)
        for array in probability_arrays.values():
            array.fill(np.nan)

        for index, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
            if row["Extort"]:
                kappa_array[row["Player index"], row["Opponent index"]] = row[
                    "kappa"
                ]
            for state, array in probability_arrays.items():
                array[row["Player index"], row["Opponent index"]] = row[state]

        for column in ["Win", "Score"]:

            sorted_indices = get_sorted_indices(overall_df, column)
            sorted_arrays = {}
            for key, array in probability_arrays.items():
                sorted_arrays[key] = array[sorted_indices][:, sorted_indices]
            sorted_kappa_array = kappa_array[sorted_indices][:, sorted_indices]

            path = pathlib.Path(f"./data/p_cc_by_{column}/")
            path.mkdir(exist_ok=True, parents=True)
            np.savetxt(str(path / "main.csv"), sorted_arrays["P(CC)"])

            path = pathlib.Path(f"./data/p_cd_by_{column}/")
            path.mkdir(exist_ok=True, parents=True)
            np.savetxt(str(path / "main.csv"), sorted_arrays["P(CD)"])

            path = pathlib.Path(f"./data/p_dc_by_{column}/")
            path.mkdir(exist_ok=True, parents=True)
            np.savetxt(str(path / "main.csv"), sorted_arrays["P(DC)"])

            path = pathlib.Path(f"./data/p_dd_by_{column}/")
            path.mkdir(exist_ok=True, parents=True)
            np.savetxt(str(path / "main.csv"), sorted_arrays["P(DD)"])

            path = pathlib.Path(f"./data/kappa_by_{column}/")
            path.mkdir(exist_ok=True, parents=True)
            np.savetxt(str(path / "main.csv"), sorted_kappa_array)

    fig, axarr = plt.subplots(nrows=2, ncols=4, figsize=(15, 15))
    for i, column in enumerate(["Win", "Score"]):
        probability_arrays = {}
        probability_arrays["P(CC)"] = np.loadtxt(
            f"./data/p_cc_by_{column}/main.csv"
        )
        probability_arrays["P(CD)"] = np.loadtxt(
            f"./data/p_cd_by_{column}/main.csv"
        )
        probability_arrays["P(DC)"] = np.loadtxt(
            f"./data/p_dc_by_{column}/main.csv"
        )
        probability_arrays["P(DD)"] = np.loadtxt(
            f"./data/p_dd_by_{column}/main.csv"
        )
        kappa_array = np.loadtxt(f"./data/kappa_by_{column}/main.csv")

        im = axarr[i, 0].imshow(kappa_array)
        axarr[i, 0].set_title("$\kappa$")
        axarr[i, 0].set_xlabel(f"Ranks by {column}")
        axarr[i, 0].set_ylabel(f"Ranks by {column}")
        divider = make_axes_locatable(axarr[i, 0])
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(im, cax=cax)
        fig.tight_layout()

        im = axarr[i, 1].imshow(probability_arrays["P(CC)"])
        axarr[i, 1].set_title("$P(CC)$")
        axarr[i, 1].set_xlabel(f"Ranks by {column}")
        divider = make_axes_locatable(axarr[i, 1])
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(im, cax=cax)
        fig.tight_layout()

        im = axarr[i, 2].imshow(probability_arrays["P(CD)"])
        axarr[i, 2].set_title("$P(CD)$")
        axarr[i, 2].set_xlabel(f"Ranks by {column}")
        divider = make_axes_locatable(axarr[i, 2])
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(im, cax=cax)
        fig.tight_layout()

        im = axarr[i, 3].imshow(probability_arrays["P(DD)"])
        axarr[i, 3].set_title("$P(DD)$")
        axarr[i, 3].set_xlabel(f"Ranks by {column}")
        divider = make_axes_locatable(axarr[i, 3])
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(im, cax=cax)
        fig.tight_layout()

    fig.savefig("main.pdf", bbox_inches="tight")


if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)