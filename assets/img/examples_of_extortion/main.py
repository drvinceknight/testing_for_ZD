"""
Script to plot R^2 for strategies of the form p = (x, p2, p3, 0) where x in
[2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9, 1] that extort their opponents.
"""
import matplotlib.pyplot as plt
import numpy as np

import testzd as zd

def main(N=500, max_r_squared = 10 ** -6):
    fig, axarr = plt.subplots(2, 5, figsize=(15, 15))
    data = []
    xs = ("1/10", "2/10", "3/10", "4/10", "5/10", "6/10", "7/10", "8/10", "9/10", "1")
    for x in xs:
        ps = np.linspace(0, 1, N)
        valid_x = []
        valid_y = []

        array = np.zeros((N, N))
        array.fill(np.nan)
        for i, p2 in enumerate(ps):
            for j, p3 in enumerate(ps):
                p = np.array([eval(x), p2, p3, 0])
                x_bar, r_squared = zd.compute_least_squares(p)
                alpha, beta, gamma = x_bar
                if -beta / alpha > 1:
                    array[i, j] = r_squared
                    if r_squared < max_r_squared:
                        valid_x.append(j)
                        valid_y.append(i)
        data.append((array, valid_x, valid_y))

    R_squared_values = [value for array, _, _ in data
                              for value in array[np.isfinite(array)]]
    max_value_of_R_squared = np.max(R_squared_values)
    min_value_of_R_squared = np.min(R_squared_values)

    for i, (array, valid_x, valid_y) in enumerate(data):
        ax = axarr[int(i / 5), i % 5]
        im = ax.imshow(array,
                       vmin=min_value_of_R_squared,
                       vmax=max_value_of_R_squared)
        ax.plot(valid_x, valid_y, color="black")
        ax.set_title(f"$p_1={xs[i]}$")

        ax.set_xticks([0, N / 2, N])
        ax.set_xticklabels((0, 1/2, 1))
        ax.set_xlabel("$p_2$")

        ax.set_yticks([0, N / 2, N])
        ax.set_yticklabels((0, 1/2, 1))
        ax.set_ylabel("$p_3$")

    fig.tight_layout()
    fig.colorbar(im, ax=axarr)
    fig.savefig("main.pdf")

if __name__ == "__main__":
    main()
