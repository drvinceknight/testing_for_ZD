"""
Script to analyse data from tournament runs, making it ready for analysis.
"""
import pathlib

import pandas as pd
import numpy as np

import testzd as zd

def analyse_tournament_summary(df, epsilons):
    """
    Obtain a pandas data from that tests the behaviour of a tournament for a
    range of epsilons.
    """
    columns = ["CC_to_C_rate", "CD_to_C_rate", "DC_to_C_rate", "DD_to_C_rate"]

    counts = []

    data = {"epsilon":epsilons,
            "counts":[],
            "five_percent_quantile_ranks":[],
            "min_ranks":[],
            "median_ranks":[],
            "ninetyfive_percent_quantile_ranks":[],
            "max_ranks":[],
            "min_score_per_turn":[],
            "five_percent_quantile_score_per_turn":[],
            "mean_score_per_turn":[],
            "ninetyfive_percent_quantile_score_per_turn":[],
            "max_score_per_turn":[],
            "min_number_of_wins":[],
            "five_percent_quantile_number_of_wins":[],
            "median_number_of_wins":[],
            "ninetyfive_percent_quantile_number_of_wins":[],
            "max_number_of_wins":[],
            "min_cooperation_rate":[],
            "five_percent_quantile_cooperation_rate":[],
            "mean_cooperation_rate":[],
            "ninetyfive_percent_quantile_cooperation_rate":[],
            "max_cooperation_rate":[]}

    for epsilon in epsilons:
        played_ZD = []

        for _, row in df.iterrows():
            p = np.array(row[columns])
            played_ZD.append(zd.is_epsilon_ZD(p, epsilon=epsilon))

        data["counts"].append(sum(played_ZD))

        zd_df = df[played_ZD]

        data["min_ranks"].append(zd_df["Rank"].min())
        data["five_percent_quantile_ranks"].append(zd_df["Rank"].quantile(q=0.05))
        data["median_ranks"].append(zd_df["Rank"].median())
        data["ninetyfive_percent_quantile_ranks"].append(zd_df["Rank"].quantile(q=0.95))
        data["max_ranks"].append(zd_df["Rank"].max())

        data["min_score_per_turn"].append(zd_df["Median_score"].min())
        data["five_percent_quantile_score_per_turn"].append(zd_df["Median_score"].quantile(q=0.05))
        data["mean_score_per_turn"].append(zd_df["Median_score"].mean())
        data["ninetyfive_percent_quantile_score_per_turn"].append(zd_df["Median_score"].quantile(q=0.95))
        data["max_score_per_turn"].append(zd_df["Median_score"].max())

        data["min_number_of_wins"].append(zd_df["Wins"].min())
        data["five_percent_quantile_number_of_wins"].append(zd_df["Wins"].quantile(q=0.05))
        data["median_number_of_wins"].append(zd_df["Wins"].median())
        data["ninetyfive_percent_quantile_number_of_wins"].append(zd_df["Wins"].quantile(q=0.95))
        data["max_number_of_wins"].append(zd_df["Wins"].max())

        data["min_cooperation_rate"].append(zd_df["Cooperation_rating"].min())
        data["five_percent_quantile_cooperation_rate"].append(zd_df["Cooperation_rating"].quantile(q=0.05))
        data["mean_cooperation_rate"].append(zd_df["Cooperation_rating"].mean())
        data["ninetyfive_percent_quantile_cooperation_rate"].append(zd_df["Cooperation_rating"].quantile(q=0.95))
        data["max_cooperation_rate"].append(zd_df["Cooperation_rating"].max())
    return pd.DataFrame(data)

def main():
    epsilons = 10 ** np.linspace(0, -5, 100)
    path = pathlib.Path("./../")
    for tournament_type in ["std", "noisy", "probend"]:

        out_path = path / f"./processed/summary/{tournament_type}"
        out_path.mkdir(exist_ok=True, parents=True)

        summary_df = pd.read_csv(path / f"summary/{tournament_type}/main.csv")
        df = analyse_tournament_summary(df=summary_df, epsilons=epsilons)
        df.to_csv(out_path / "main.csv")

if __name__ == "__main__":
    main()
