import sys
import imp

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.integrate import odeint

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")

strategies = [s.name for s in parameters.PLAYER_GROUPS["full"]]
strategies_of_interest = [
    "ZD-GTFT-2",
    "ZD-GEN-2",
    "ZD-Extort-2",
    "EvolvedLookerUp2_2_2",
    "Evolved ANN 5",
    "Tit For Tat",
    "Win-Stay Lose-Shift",
]
strategies_of_interest_indices = np.array(
    [i for i, s in enumerate(strategies) if s in strategies_of_interest]
)


def dx(x, t, S):
    """
    Define the derivative of x.
    """
    f = S @ x
    phi = f @ x
    return x * (f - phi)


def main(process_data=False):
    N = len(parameters.PLAYER_GROUPS["full"])
    if process_data:
        df = pd.read_csv(
            "../../../data/processed/full/std/per_opponent/main.csv"
        )
        array = np.zeros((N, N))
        for pair, score in df.groupby(["Player index", "Opponent index"])[
            "Score"
        ]:
            array[pair] = score / (parameters.TURNS * parameters.REPETITIONS)
            if pair[0] == pair[1]:
                array[pair] /= 2

        np.savetxt("main.csv", array)
    else:
        array = np.loadtxt("main.csv")

    sorted_indices = np.argsort(-np.mean(array, axis=1))
    sorted_array = array[sorted_indices][:, sorted_indices]
    rank_of_strategies_of_interest = [
        np.where(sorted_indices == ele)[0][0]
        for ele in strategies_of_interest_indices
    ]

    ts = np.linspace(0, 5, 10 ** 2)
    x0 = np.array([1 / N for _ in range(N)])
    xs = odeint(func=dx, y0=x0, t=ts, args=(sorted_array,))

    plt.figure(figsize=(8, 4))
    plt.stackplot(ts, xs.transpose())
    plt.ylabel("Population distribution")
    plt.xlabel("Time units")

    for rank, indx in zip(
        rank_of_strategies_of_interest, strategies_of_interest_indices
    ):
        name = strategies[indx]
        long_run_prob = xs[-1][rank]
        y = np.cumsum(xs[-1])[rank] - xs[-1][rank] / 2
        plt.annotate(
            f"{name}: $x_{{{rank + 1}}}={round(long_run_prob, 3)}$",
            xy=(4.95, y),
            xycoords="data",
            xytext=(5.5, y),
            textcoords="data",
            arrowprops=dict(facecolor="black", shrink=0.05),
            horizontalalignment="left",
            verticalalignment="middle",
        )

    plt.tight_layout()
    plt.savefig("main.pdf", bbox_inches="tight")

    with open("main.tex", "w") as f:
        f.write(str(sum(xs[-1] >= 10 ** -2)))


if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
