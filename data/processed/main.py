"""
Script to take raw interaction data and write data files that contain the
probabilities and measures.
"""
import pathlib
import sys

import dask as da
import dask.dataframe as dd
import tqdm
import numpy as np

import testzd as zd

default_raw_data_path = pathlib.Path("../raw/")


def main(
    player_group="full",
    tournament_type="std",
    raw_data_path=default_raw_data_path,
):

    data_path = raw_data_path / player_group / tournament_type / "main.csv"

    columns = [
        "Player index",
        "Cooperation count",
        "Opponent index",
        "Score",
        "Win",
        "CC count",
        "CD count",
        "DC count",
        "DD count",
        "CC to C count",
        "CC to D count",
        "CD to C count",
        "CD to D count",
        "DC to C count",
        "DC to D count",
        "DD to C count",
        "DD to D count",
    ]
    ddf = dd.read_csv(data_path)[columns]

    groups = ["Player index", "Opponent index"]
    counts = [
        "Score",
        "Cooperation count",
        "Win",
        "CC count",
        "CD count",
        "DC count",
        "DD count",
        "CC to C count",
        "CC to D count",
        "CD to C count",
        "CD to D count",
        "DC to C count",
        "DC to D count",
        "DD to C count",
        "DD to D count",
    ]
    summation = ddf.groupby(groups)[counts].sum()

    print(
        f"Processing {tournament_type} for {player_group} players per opponent"
    )
    df = da.compute(summation, da.get)[0]

    df.reset_index(inplace=True)
    path = pathlib.Path("./")
    out_path = path / f"./{player_group}/{tournament_type}/per_opponent"
    out_path.mkdir(exist_ok=True, parents=True)
    columns = ["Player index", "Opponent index", "complete", "Score", "Win"]
    print("Computing measures")
    write_probabilities_and_measures_to_file(
        df, filename=str(out_path / "main.csv"), columns=columns
    )

    print(f"Processing {tournament_type} for {player_group} players overall")
    df = df.groupby(["Player index"])[counts].sum()

    df.reset_index(inplace=True)
    path = pathlib.Path("./")
    out_path = path / f"./{player_group}/{tournament_type}/overall"
    out_path.mkdir(exist_ok=True, parents=True)
    columns = ["Player index", "complete", "Score", "Win"]
    write_probabilities_and_measures_to_file(
        df, filename=str(out_path / "main.csv"), columns=columns
    )


def write_probabilities_and_measures_to_file(df, filename, columns):
    state_counts = ["CC count", "CD count", "DC count", "DD count"]
    df["complete"] = df[state_counts].min(axis=1) > 0
    probabilities = []
    for state in ("CC", "CD", "DC", "DD"):
        column = f"P(C|{state})"
        probabilities.append(column)
        columns.append(column)
        df[column] = df[f"{state} to C count"] / (
            df[f"{state} to C count"] + df[f"{state} to D count"]
        )

    total_states = (
        df["CC count"] + df["CD count"] + df["DC count"] + df["DD count"]
    )

    df["P(C)"] = df["Cooperation count"] / total_states
    columns.append("P(C)")

    for state in ("CC", "CD", "DC", "DD"):
        column = f"P({state})"
        columns.append(column)
        df[f"P({state})"] = df[f"{state} count"] / total_states

    residuals = []
    alphas = []
    betas = []
    computed_residuals = []
    computed_alphas = []
    computed_betas = []
    number_of_rows = df.shape[0]
    for index, row in tqdm.tqdm(df.iterrows(), total=number_of_rows):
        p = row[probabilities].values.astype("float64")
        p_c = row["P(C)"]

        xbar, residual = zd.get_least_squares(p=p, p_c=p_c)
        computed_xbar, computed_residual = zd.compute_least_squares(p, p_c=p_c)

        alpha, beta = xbar
        computed_alpha, computed_beta = xbar

        residuals.append(residual)
        alphas.append(alpha)
        betas.append(beta)

        computed_residuals.append(computed_residual)
        computed_alphas.append(computed_alpha)
        computed_betas.append(computed_beta)

    df["residual"] = residuals
    columns.append("residual")

    df["alpha"] = alphas
    columns.append("alpha")

    df["beta"] = betas
    columns.append("beta")

    df["chi"] = -df["beta"] / df["alpha"]
    columns.append("chi")

    df["computed_residual"] = computed_residuals
    columns.append("computed_residual")

    df["computed_alpha"] = computed_alphas
    columns.append("computed_alpha")

    df["computed_beta"] = computed_betas
    columns.append("computed_beta")

    df["computed_chi"] = -df["computed_beta"] / df["computed_alpha"]
    columns.append("computed_chi")

    df[columns].to_csv(filename, index=False)


if __name__ == "__main__":

    tournament_type = sys.argv[1]
    player_group = sys.argv[2]
    main(player_group=player_group, tournament_type=tournament_type)
