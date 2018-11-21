from scipy.stats import linregress
import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv("../../../data/processed/full/std/per_opponent/main.csv")
    upper_chi = df["chi"].quantile(q=0.95)
    lower_chi = df["chi"].quantile(q=0.05)
    Y = df[(df["chi"] >= lower_chi) & (df["chi"] <= upper_chi)]["chi"]
    X = df[(df["chi"] >= lower_chi) & (df["chi"] <= upper_chi)]["residual"]

    slope, intercept, r_value, p_value, std_err = linregress(X, Y)

    plt.figure(figsize=(18, 4))
    plt.title(f"$y={slope:0.3f}x+{intercept:0.3f}$ ($p={p_value:0.3f}$, $R^2={round(r_value ** 2, 3)}$, $n={len(X)}$)")
    plt.scatter(X, Y)
    plt.plot(X, slope * X + intercept, color="black")
    plt.xlabel("SSerror")
    plt.ylabel("$\chi$");
    plt.savefig("main.pdf") 

if __name__ == "__main__":
    main()
