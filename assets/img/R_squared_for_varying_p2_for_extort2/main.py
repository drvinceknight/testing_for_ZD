"""
Script to plot the value of R^2 for p=(8/9, p_2, 1/3, 0) for varying value of
p_2
"""
import numpy as np
import matplotlib.pyplot as plt

import testzd as zd

def main():
    p2s = np.linspace(0, 1, 500)
    func = np.vectorize(lambda p2: zd.compute_least_squares(
                                            np.array([8/9, p2, 1/3, 0]))[1])
    r_squared = func(p2s)
    plt.figure()
    plt.plot(p2s, r_squared)
    plt.axvline(1/2, color="red", linestyle="dashed", label="$p_2=1/2$")
    plt.xlabel("$p_2$")
    plt.ylabel("$R^2$")
    plt.legend()
    plt.savefig("main.pdf")

if __name__ == "__main__":
    main()
