import sys
import imp

import pandas as pd

import sklearn
from sklearn.feature_selection import RFE, f_regression
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from scipy.integrate import odeint

import numpy as np

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")
player_names = [
    player.__repr__() for player in parameters.PLAYER_GROUPS["full"]
]

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")
# These three strategies always win because they make use of the length of the
# matches.
strategies_not_of_interest = [
    s.name
    for s in parameters.PLAYER_GROUPS["full"]
    if "length" in s.classifier["makes_use_of"]
]

all_strategies = [s.name for s in parameters.PLAYER_GROUPS["full"]]
strategies_of_interest = [
    name for name in all_strategies if name not in strategies_not_of_interest
]
indices_of_interest = np.array(
    [i for i, s in enumerate(all_strategies) if s in strategies_of_interest]
)


def dx(x, t, S):
    """
    Define the derivative of x.
    """
    f = S @ x
    phi = f @ x
    return x * (f - phi)


def carry_out_recursive_feature_elimination(n_features_to_select, Y, X):
    model = LinearRegression()
    rfe = RFE(model, n_features_to_select=n_features_to_select)
    fit = rfe.fit(X, Y)

    columns = [var for i, var in enumerate(X.columns) if fit.support_[i]]

    X = sm.add_constant(X[columns])
    model = sm.OLS(Y, X).fit()

    return model


def main(process_data=False):
    if process_data:
        N = len(parameters.PLAYER_GROUPS["full"])

        df = pd.read_csv(
            "../../../data/processed/full/std/per_opponent/main.csv"
        )

        df = df[
            (df["Player index"].isin(indices_of_interest))
            & (df["Opponent index"].isin(indices_of_interest))
        ]

        array = np.zeros((N, N))
        for pair, score in df.groupby(["Player index", "Opponent index"])[
            "Score"
        ]:
            array[pair] = score / (parameters.TURNS * parameters.REPETITIONS)
            if pair[0] == pair[1]:
                array[pair] /= 2

        array = array[indices_of_interest][:, indices_of_interest]
        N = array.shape[0]
        ts = np.linspace(0, 10, 6 * 10 ** 4)
        x0 = np.array([1 / N for _ in range(N)])
        while not np.allclose(dx(x0, t=0, S=array), 0):
            xs = odeint(func=dx, y0=x0, t=ts, args=(array,))
            x0 = xs[-1]

        aggregate_df = df.groupby("Player index").agg(
            ["mean", "median", "std", "max", "min", "var", "skew"]
        )
        aggregate_df["$s_i$"] = x0

        df = aggregate_df
        df.to_csv("main.csv")
    else:
        df = pd.read_csv("main.csv")

    Y = df["$s_i$"]
    X = df[["residual", "chi"]]

    model = carry_out_recursive_feature_elimination(
        n_features_to_select=3, Y=Y, X=X
    )
    with open("main.tex", "w") as f:
        for table in model.summary().tables:
            f.write(table.as_latex_tabular())


if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
