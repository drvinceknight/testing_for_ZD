import sys
import imp

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.integrate import odeint
from scipy.stats import linregress

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")


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

        mean_kappa = df.groupby("Player index")["kappa"].mean()
        std_kappa = df.groupby("Player index")["kappa"].std()
        median_kappa = df.groupby("Player index")["kappa"].median()
        df = pd.DataFrame(
            {
                "mean_kappa": mean_kappa,
                "std_kappa": std_kappa,
                "median_kappa": median_kappa,
            }
        )
        ts = np.linspace(0, 10, 2 * 10 ** 2)
        x0 = np.array([1 / N for _ in range(N)])
        xs = odeint(func=dx, y0=x0, t=ts, args=(array,))
        df["s_i"] = xs[-1]
        df["survive"] = df["s_i"] >= 1 / N
        df.to_csv("main.csv")

    else:
        df = pd.read_csv("main.csv")

    fig, axarr = plt.subplots(1, 3, figsize=(19.6, 4))
    for ax, var, xlabel in zip(
        axarr,
        ("mean_kappa", "median_kappa", "std_kappa"),
        (
            r"$\bar{\kappa}$ (mean)",
            r"$\tilde{\kappa}$ (median)",
            r"$\sigma_{\kappa}$ (standard deviation)",
        ),
    ):
        for index, label, marker, color in zip(
            [~df["survive"], df["survive"]],
            [f"$s_i \leq 1 / N$ ($n={(~df['survive']).sum()}$)", None],
            (".", "+"),
            ("grey", "black"),
        ):
            ax.scatter(
                df[index][var],
                df[index]["s_i"],
                label=label,
                color=color,
                marker=marker,
            )

        x = df[var]
        y = df["s_i"]
        N = df.shape[0]
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        ax.plot(
            df[var],
            slope * df[var] + intercept,
            label=f"$y={slope:0.3f}x+{intercept:0.3f}$ ($p={p_value:0.3f}$, $R^2={round(r_value ** 2, 3)}$, $n={N}$)",
            color="black",
        )

        x = df[df["survive"]][var]
        y = df[df["survive"]]["s_i"]
        N = df["survive"].sum()
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        ax.plot(
            df[var],
            slope * df[var] + intercept,
            label=f"$y={slope:0.3f}x+{intercept:0.3f}$ ($p={p_value:0.3f}$, $R^2={round(r_value ** 2, 3)}$, $n={N}$) for $s_i> 1 / N$",
            color="black",
            linestyle=":",
        )

        ax.set_xlabel(xlabel, fontsize=20)
        ax.set_ylabel("$s_i$", fontsize=18)
        ax.legend(bbox_to_anchor=(0.0, 1.02, 1.0, 0.102))
        epsilon = 10 ** -3
        ax.set_ylim(-epsilon, np.max(df["s_i"]) + epsilon)
    fig.tight_layout()
    fig.savefig("main.pdf")


if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
