import sys
import imp

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.integrate import odeint

parameters = imp.load_source('parameters',
                             '../../../data/raw/parameters.py')

def dx(x, t, A):
    """
    Define the derivative of x.
    """
    f = np.dot(A, x)
    phi = np.dot(f, x)
    return x * (f - phi)

def main(process_data=False):
    N = len(parameters.PLAYER_GROUPS["full"])
    if process_data:
        df = pd.read_csv("../../../data/processed/full/std/per_opponent/main.csv")
        array = np.zeros((N, N))
        for pair, score in df.groupby(["Player index", "Opponent index"])["Score"]:
            array[pair] = score / (parameters.TURNS * parameters.REPETITIONS)
            if pair[0] == pair[1]:
                array[pair] /= 2

        sorted_indices = np.argsort(-np.mean(array, axis=1))
        sorted_array = array[sorted_indices][:,sorted_indices]
        np.savetxt("main.csv", sorted_array)
    else:
        sorted_array = np.loadtxt("main.csv")

    ts = np.linspace(0, 5, 10 ** 2)
    x0 = np.array([1 / N for _ in range(N)])
    xs = odeint(func=dx, y0=x0, t=ts, args=(sorted_array,))

    plt.figure(figsize=(8, 4))
    plt.stackplot(ts, xs.transpose());
    plt.ylabel("Population distribution")
    plt.xlabel("Time steps")
    plt.savefig("main.pdf")

    with open("main.tex", "w") as f:
        f.write(str(sum(xs[-1] >= 10 ** -2)))

if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
