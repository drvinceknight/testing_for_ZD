"""
Script to take raw interaction data and write data files that contain the
probabilities and delta values.
"""
import pathlib

import dask as da
import dask.dataframe as dd

default_raw_data_path = pathlib.Path("../raw/")

def main(player_group="full",
         tournament_type="std",
         raw_data_path=default_raw_data_path):

    data_path = raw_data_path / player_group / tournament_type / "main.py"

    columns = ["Player index",
               "Opponent index",
               "Score",
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
               "DD to D count",]
    ddf = dd.read_csv(data_path)[columns]

    groups = ["Player index", "Opponent index"]
    counts = ["Score",
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
              "DD to D count",]
    summation = ddf.groupby(groups)[counts].sum()

    print(f"Processing {tournament_type} for {player_group} players per opponent")
    df = da.compute(summation, da.get)[0]
    df.reset_index(inplace=True)
    path = pathlib.Path("./")
    out_path = path / f"./{player_group}/{tournament_type}/per_opponent"
    out_path.mkdir(exist_ok=True, parents=True)
    columns = ["Player index", "Opponent index", "complete", "Score"]
    write_probabilities_and_deltas_to_file(df,
                                           filename=str(out_path / "main.csv"),
                                           columns=columns)

    print(f"Processing {tournament_type} for {player_group} players overall")
    df = df.groupby(["Player index"])[counts].sum()
    df.reset_index(inplace=True)
    path = pathlib.Path("./")
    out_path = path / f"./{player_group}/{tournament_type}/overall"
    out_path.mkdir(exist_ok=True, parents=True)
    columns = ["Player index", "complete", "Score"]
    write_probabilities_and_deltas_to_file(df,
                                           filename=str(out_path / "main.csv"),
                                           columns=columns)



def write_probabilities_and_deltas_to_file(df, filename, columns):
    df["complete"] = df["CC count"] * df["CD count"] * df["DC count"] *  df["DD count"] > 0
    probabilities = []
    for state in ("CC", "CD", "DC", "DD"):
        column = f"P(C|{state})"
        probabilities.append(column)
        columns.append(column)
        df[column] = df[f"{state} to C count"] / (df[f"{state} to C count"] + df[f"{state} to D count"])
    df = df[columns]
    df.to_csv(filename)

if __name__ == "__main__":

    tournament_type = sys.argv[1]
    player_group = sys.argv[2]
    main(player_group=player_group, tournament_type=tournament_type)
