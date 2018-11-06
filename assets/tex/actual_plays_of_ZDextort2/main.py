import axelrod as axl
import pandas as pd

def main():
    player = axl.ZDExtort2()
    opponent = axl.Alternator()
    axl.seed(0)
    match = axl.Match(players=(player, opponent), turns=20)
    interactions = match.play()
    df = pd.DataFrame(interactions, columns=["(8/9, 1/2, 1/3, 0)", "Alternator"])
    df["Turn"] = df.index + 1
    df = df[["Turn", "(8/9, 1/2, 1/3, 0)", "Alternator"]]
    df = df.transpose()
    string = df.to_latex(header=False).replace("\\\\", "\\\\\\midrule", 1)
    with open("main.tex", "w") as f:
        f.write(string)

if __name__ == "__main__":
    main()
