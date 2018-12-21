import sys
import imp

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.integrate import odeint

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


def main(process_data=False):
    if process_data:
        N = len(all_strategies)

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

        array = array[indices_of_interest][:, indices_of_interest]
        N = array.shape[0]

        sorted_indices = np.argsort(-np.mean(array, axis=1))
        sorted_array = array[sorted_indices][:, sorted_indices]

        ts = np.linspace(0, 10, 6 * 10 ** 4)
        x0 = np.array([1 / N for _ in range(N)])
        while not np.allclose(dx(x0, t=0, S=sorted_array), 0):
            xs = odeint(func=dx, y0=x0, t=ts, args=(sorted_array,))
            x0 = xs[-1]

        df = pd.DataFrame(
            {
                "name": strategies_of_interest,
                "stationary": x0,
                "sorted_indices": sorted_indices,
            }
        )
        df.to_csv("main.csv", index=False)
    else:
        df = pd.read_csv("main.csv")
        x0 = df["stationary"].values
        sorted_indices = df["sorted_indices"]

    N = x0.shape[0]
    plt.figure(figsize=(8, 4))
    plt.scatter(range(1, N + 1), x0, color="black")
    plt.ylabel("Stationary distribution")
    plt.xlabel("Strategies sorted by score")
    plt.ylim(0, np.max(x0) * 1.1)
    plt.tight_layout()
    plt.savefig("main.pdf", bbox_inches="tight")

    with open("main.tex", "w") as f:
        f.write(str(sum(x0 >= 10 ** -2)))


if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
