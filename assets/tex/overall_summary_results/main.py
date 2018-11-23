import sys
import imp

import pandas as pd

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")


def main(process_data=False):
    if process_data:
        player_names = [s.name for s in parameters.PLAYER_GROUPS["full"]]

        strategies_of_interest = [
            "ZD-GTFT-2",
            "ZD-GEN-2",
            "ZD-Extort-2",
            "EvolvedLookerUp2_2_2",
            "Evolved ANN 5",
            "Tit For Tat",
            "Win-Stay Lose-Shift",
        ]
        df = pd.read_csv("../../../data/processed/full/std/overall/main.csv")
        df["Score per turn"] = df["Score"] / (
            parameters.TURNS * parameters.REPETITIONS * (len(player_names))
        )
        df["Name"] = player_names
        df["P(Win)"] = df["Win"] / (len(player_names) * parameters.REPETITIONS)
        df["Rank"] = df["Score"].rank(ascending=False).astype(int)
        sserror = df["residual"].round(4)
        df["residual"] = sserror

        strategies_of_interest += list(df.sort_values("residual").head(5)["Name"])
        strategies_of_interest += list(df.sort_values("residual").tail(5)["Name"])
        strategies_of_interest += list(df.sort_values("P(Win)").tail(2)["Name"])
        strategies_of_interest += list(df.sort_values("P(CC)").tail(2)["Name"])
        strategies_of_interest += list(df.sort_values("Score").head(5)["Name"])
        strategies_of_interest += list(df.sort_values("Score").tail(5)["Name"])

        columns = ["Rank", "Name", "Score per turn", "P(Win)", "P(CC)"]
        df = df[columns]

        df.rename(
            columns={
                "P(Win)": "$P($Win$)$",
                "P(CC)": "$P(CC)$",
            },
            inplace=True,
        )

        per_opponent_df = pd.read_csv(
            "../../../data/processed/full/std/per_opponent/main.csv"
        )
        mean_sserror = per_opponent_df.groupby("Player index")["residual"].mean()
        median_chi = per_opponent_df.groupby("Player index")["chi"].median()
        ninety_fifth_quantile_sserror = per_opponent_df.groupby("Player index")[
            "residual"
        ].quantile(0.95)
        fifth_quantile_sserror = per_opponent_df.groupby("Player index")[
            "residual"
        ].quantile(0.05)
        std_sserror = per_opponent_df.groupby("Player index")["residual"].std()
        per_opponent_df = pd.DataFrame(
            {
                "Name": player_names,
                "Median $\chi$": median_chi,
                "5% CI SSE": fifth_quantile_sserror,
                "Mean SSE": mean_sserror,
                "Std SSE": std_sserror,
                "95% CI SSE": ninety_fifth_quantile_sserror,
            }
        )

        df = df.merge(per_opponent_df, on="Name")

        df = df[df["Name"].isin(strategies_of_interest)]
        df.sort_values("Score per turn", ascending=False, inplace=True)
        df = df.round(3)
        df = df.dropna()

        df.to_csv("main.csv", index=False)
    else:
        df = pd.read_csv("main.csv")

    latex = df.to_latex(index=False)
    latex = latex.replace("\$", "$").replace("textbackslash ", "")
    with open("main.tex", "w") as f:
        f.write(latex)


if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
