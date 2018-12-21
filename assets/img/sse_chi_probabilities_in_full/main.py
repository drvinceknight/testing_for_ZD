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
        sserror_array = np.zeros((number_of_players, number_of_players))
        chi_array = np.zeros((number_of_players, number_of_players))
        probability_arrays = {
            "P(CC)": np.zeros((number_of_players, number_of_players)),
            "P(CD)": np.zeros((number_of_players, number_of_players)),
            "P(DC)": np.zeros((number_of_players, number_of_players)),
            "P(DD)": np.zeros((number_of_players, number_of_players)),
        }

        for array in probability_arrays.values():
            array.fill(np.nan)

        for index, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
            sserror_array[row["Player index"], row["Opponent index"]] = row[
                "residual"
            ]
            chi_array[row["Player index"], row["Opponent index"]] = row[
                "Extort"
            ]
            for state, array in probability_arrays.items():
                array[row["Player index"], row["Opponent index"]] = row[state]

        for column in ["Win", "Score"]:

            sorted_indices = get_sorted_indices(overall_df, column)
            sorted_arrays = {}
            for key, array in probability_arrays.items():
                sorted_arrays[key] = array[sorted_indices][:, sorted_indices]
            sorted_sserror_array = sserror_array[sorted_indices][:, sorted_indices]
            sorted_chi_array = chi_array[sorted_indices][:, sorted_indices]

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

            path = pathlib.Path(f"./data/sserror_by_{column}/")
            path.mkdir(exist_ok=True, parents=True)
            np.savetxt(str(path / "main.csv"), sorted_sserror_array)

            path = pathlib.Path(f"./data/chi_by_{column}/")
            path.mkdir(exist_ok=True, parents=True)
            np.savetxt(str(path / "main.csv"), sorted_chi_array)

    fig, axarr = plt.subplots(nrows=1, ncols=4, figsize=(15, 15))
    for i, column in enumerate(["Win", "Score"]):
        sserror_array = np.loadtxt(f"./data/sserror_by_{column}/main.csv")
        pdd_array = np.loadtxt(f"./data/p_dd_by_{column}/main.csv")

        im = axarr[2 * i].imshow(sserror_array)
        axarr[2 * i].set_title("SSE")
        axarr[2 * i].set_xlabel(f"Ranks by {column}")
        axarr[2 * i].set_ylabel(f"Ranks by {column}")
        divider = make_axes_locatable(axarr[2 * i])
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(im, cax=cax)
        fig.tight_layout()

        im = axarr[2 * i + 1].imshow(pdd_array)
        axarr[2 * i + 1].set_title("P(DD)")
        axarr[2 * i + 1].set_xlabel(f"Ranks by {column}")
        axarr[2 * i + 1].set_ylabel(f"Ranks by {column}")
        divider = make_axes_locatable(axarr[2 * i + 1])
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(im, cax=cax)
        fig.tight_layout()

    fig.savefig("main.pdf", bbox_inches="tight")


if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
