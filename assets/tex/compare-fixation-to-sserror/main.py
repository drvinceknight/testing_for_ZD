import sys
import imp

import pandas as pd

import sklearn
from sklearn.feature_selection import RFE, f_regression
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")
player_names = [
    player.__repr__() for player in parameters.PLAYER_GROUPS["full"]
]


def find_index(name, player_names=player_names):
    try:
        return int(player_names.index(name))
    except ValueError:
        return -1


def carry_out_recursive_feature_elimination(n_features_to_select, Y, X):
    model = LinearRegression()
    rfe = RFE(model, n_features_to_select=n_features_to_select)
    fit = rfe.fit(X, Y)

    columns = [var for i, var  in enumerate(X.columns) if fit.support_[i]]

    X = sm.add_constant(X[columns])
    model = sm.OLS(Y, X).fit()

    return model

def main(process_data=False):
    if process_data:
        df = pd.read_csv("../../../data/processed/full/std/per_opponent/main.csv")
        moran_df = pd.read_csv("../../img/compare-fixation-to-sserror/data/main.csv")
        moran_df["Player index"] = moran_df["player"].map(find_index)
        moran_df["Opponent index"] = moran_df["opponent"].map(find_index)
        moran_df["Normalised fixation"] = moran_df["$p_1$"] * moran_df["N"]
        df = moran_df.merge(df, on=("Player index", "Opponent index"), how="right")
        df.to_csv("main.csv")
    else:
        df = pd.read_csv("main.csv")

    aggregate_df = df.groupby("Player index").agg(["mean", "median", "std", "max", "min", "var"]).dropna()
    Y = aggregate_df["Normalised fixation"]["mean"]
    X = aggregate_df[["residual", "chi"]]

    model = carry_out_recursive_feature_elimination(n_features_to_select=2, Y=Y, X=X)
    with open("main.tex", "w") as f:
        for table in model.summary().tables:
            f.write(table.as_latex_tabular())



if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
