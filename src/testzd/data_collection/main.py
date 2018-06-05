import axelrod as axl
import pandas as pd
import numpy as np

import testzd as zd

C, D = axl.Action.C, axl.Action.D


def get_vector_from_counter(counter):
    return np.array([counter[((C, C), C)],
                     counter[((C, D), C)],
                     counter[((D, C), C)],
                     counter[((D, D), C)]])

def obtain_pairwise_epsilons(result_set):
    """
    Given a matrix of lowest values of $\epsilon$ for which each row strategy is
    $\epsilon$-ZD
    """
    return np.array([[zd.find_lowest_epsilon(get_vector_from_counter(opponent))
                      for opponent in player]
                     for player in
                     result_set.normalised_state_to_action_distribution])

def analyse_tournament_behaviour(result_set, epsilons):
    """
    Obtain a pandas data from that tests the behaviour of a tournament for a
    range of epsilons.
    """
    columns = ["CC_to_C_rate", "CD_to_C_rate", "DC_to_C_rate", "DD_to_C_rate"]

    df = pd.DataFrame(result_set.summarise())

    counts = []

    data = {"epsilon":epsilons,
            "counts":[],
            "min_ranks":[],
            "median_ranks":[],
            "max_ranks":[],
            "min_score_per_turn":[],
            "mean_score_per_turn":[],
            "max_score_per_turn":[],
            "min_number_of_wins":[],
            "median_number_of_wins":[],
            "max_number_of_wins":[],
            "min_cooperation_rate":[],
            "mean_cooperation_rate":[],
            "max_cooperation_rate":[]}

    for epsilon in epsilons:
        played_ZD = []

        for _, row in df.iterrows():
            p = np.array(row[columns])
            played_ZD.append(zd.is_epsilon_ZD(p, epsilon=epsilon))

        data["counts"].append(sum(played_ZD))

        zd_df = df[played_ZD]

        data["min_ranks"].append(zd_df["Rank"].min())
        data["median_ranks"].append(zd_df["Rank"].median())
        data["max_ranks"].append(zd_df["Rank"].max())

        data["min_score_per_turn"].append(zd_df["Median_score"].min())
        data["mean_score_per_turn"].append(zd_df["Median_score"].mean())
        data["max_score_per_turn"].append(zd_df["Median_score"].max())

        data["min_number_of_wins"].append(zd_df["Wins"].min())
        data["median_number_of_wins"].append(zd_df["Wins"].median())
        data["max_number_of_wins"].append(zd_df["Wins"].max())

        data["min_cooperation_rate"].append(zd_df["Cooperation_rating"].min())
        data["mean_cooperation_rate"].append(zd_df["Cooperation_rating"].mean())
        data["max_cooperation_rate"].append(zd_df["Cooperation_rating"].max())
    return pd.DataFrame(data)
