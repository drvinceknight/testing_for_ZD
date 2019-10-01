import sys

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from axelrod.action import Action


import imp

import testzd as zd

C, D = Action.C, Action.D

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")


def get_chi(four_vector, p_c):
    """
    Return the value of chi for a given row
    """
    p = np.array(
        [
            four_vector[(C, C)],
            four_vector[(C, D)],
            four_vector[(D, C)],
            four_vector[(D, D)],
        ]
    )
    xbar, residual = zd.get_least_squares(p=p, p_c=p_c)
    alpha, beta = xbar
    return -beta / alpha


def main():
    players = parameters.PLAYER_GROUPS["full"]
    player_names = [p.name for p in players]
    zd_player_names = [
        p.name
        for p in players
        if hasattr(p, "_four_vector") and p.name != "ZD-Mischief"
    ]
    zd_player_names_to_chi = {
        p.name: p._four_vector for p in players if hasattr(p, "_four_vector")
    }

    df = pd.read_csv("../../../data/processed/full/std/overall/main.csv")
    df["Name"] = df.apply(lambda row: player_names[row["Player index"]], axis=1)

    df = df[df["Name"].isin(zd_player_names)]

    df["Known chi"] = df.apply(
        lambda row: get_chi(
            four_vector=zd_player_names_to_chi[row["Name"]], p_c=row["P(C)"]
        ),
        axis=1,
    )

    df["Measured chi"] = df["chi"]
    df["SSE"] = df["residual"]

    df = df[["Name", "Measured chi", "Known chi", "SSE"]].round(4)
    latex = df.to_latex(index=False)
    with open("main.tex", "w") as f:
        f.write(latex)


if __name__ == "__main__":
    main()
