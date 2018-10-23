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
        df.sort_values("Score per turn", ascending=False, inplace=True)
        df = df.round(3)

        df["SSError"] = sserror
        columns = [
            "Rank",
            "Name",
            "Score per turn",
            "P(Win)",
            "P(CC)",
            "P(C|CC)",
            "P(C|CD)",
            "P(C|DC)",
            "P(C|DD)",
            "SSError",
            "alpha",
            "beta",
            "chi",
        ]

        df = df[df["Name"].isin(strategies_of_interest)][columns]
        df.rename(
            columns={
                "P(Win)": "$P($Win$)$",
                "P(CC)": "$P(CC)$",
                "P(C|CC)": "$P(C|CC)$",
                "P(C|CD)": "$P(C|CD)$",
                "P(C|DC)": "$P(C|DC)$",
                "P(C|DD)": "$P(C|DD)$",
                "alpha": r"$\alpha$",
                "beta": r"$\beta$",
                "chi": r"$\chi$",
            },
            inplace=True,
        )
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
