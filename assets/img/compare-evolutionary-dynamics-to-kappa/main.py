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
        cv_kappa = std_kappa / mean_kappa
        df = pd.DataFrame(
            {
                "mean_kappa": mean_kappa,
                "std_kappa": std_kappa,
                "cv_kappa": cv_kappa,
            }
        )
        ts = np.linspace(0, 10, 2 * 10 ** 2)
        x0 = np.array([1 / N for _ in range(N)])
        xs = odeint(func=dx, y0=x0, t=ts, args=(array,))
        df["s_i"] = xs[-1]
        df["survive"] = df["s_i"] >= 10 ** -4
        df.to_csv("main.csv")

    else:
        df = pd.read_csv("main.csv")

    fig, axarr = plt.subplots(2, figsize=(9, 6))
    for ax, var, xlabel in zip(
        axarr,
        ("mean_kappa", "std_kappa"),
        (r"$\mu_{\kappa}$", r"$\sigma_{\kappa}$"),
    ):
        for index, label, marker, color in zip(
            [~df["survive"], df["survive"]],
            [f"$x_i \leq 10 ^{{- 4}}$ ($N={(~df['survive']).sum()}$)", None],
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
            label=f"$y={slope:0.3f}x+{intercept:0.3f}$ ($p={p_value:0.3f}$, $R^2={round(r_value ** 2, 3)}$, $N={N}$)",
            color="black",
        )

        x = df[df["survive"]][var]
        y = df[df["survive"]]["s_i"]
        N = df["survive"].sum()
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        ax.plot(
            df[var],
            slope * df[var] + intercept,
            label=f"$y={slope:0.3f}x+{intercept:0.3f}$ ($p={p_value:0.3f}$, $R^2={round(r_value ** 2, 3)}$, $N={N}$) for $s_i> 10 ^{{-4}}$",
            color="black",
            linestyle=":",
        )

        ax.set_xlabel(xlabel)
        ax.set_ylabel("$s_i$")
        ax.legend(bbox_to_anchor=(0.0, 1.02, 1.0, 0.102))
        epsilon = 10 ** -3
        ax.set_ylim(-epsilon, np.max(df["s_i"]) + epsilon)
    fig.tight_layout()
    fig.savefig("main.pdf")


if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
