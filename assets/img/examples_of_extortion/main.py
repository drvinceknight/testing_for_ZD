"""
Script to plot R^2 for strategies of the form p = (x, p2, p3, 0) for a range of
values of 1/10<=x<=1.

"""
import sys
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import tqdm

import testzd as zd

def main(N=750, max_r_squared = 10 ** -6, process_data=False):


    if process_data:
        data = []
        for k in tqdm.trange(10):
            ps = np.linspace(0, 1, N)

            array = np.zeros((N, N))
            array.fill(np.nan)
            for i, p2 in tqdm.tqdm(enumerate(ps), total=N):
                for j, p3 in enumerate(ps):
                    p = np.array([(k + 1) / 10, p2, p3, 0])
                    x_bar, r_squared = zd.compute_least_squares(p)
                    alpha, beta, gamma = x_bar
                    if -beta / alpha > 1:
                        array[i, j] = r_squared

            path = pathlib.Path(f"./data/{k}")
            path.mkdir(exist_ok=True, parents=True)
            np.savetxt(str(path / "main.csv"), array)

            data.append(array)
    else:
        data = [np.loadtxt(f"./data/{k}/main.csv") for k in range(10)]

    R_squared_values = [value for array in data
                              for value in array[np.isfinite(array)]]
    max_value_of_R_squared = np.max(R_squared_values)
    min_value_of_R_squared = np.min(R_squared_values)

    fig, axarr = plt.subplots(nrows=2, ncols=5, figsize=(15, 15),
                              sharex='col', sharey='row')
    for i, array in enumerate(data):
        ax = axarr[int(i / 5), i % 5]
        im = ax.imshow(array,
                       vmin=min_value_of_R_squared,
                       vmax=max_value_of_R_squared)
        valid_y, valid_x = np.where(array <= max_r_squared)
        ax.plot(valid_x, valid_y, color="black")
        ax.set_title(f"$p_1={round((i + 1)/10, 1)}$")
        fig.tight_layout()

        if i > 5:
            ax.set_xticks([0, N / 2, N])
            ax.set_xticklabels((0, 1/2, 1))
            ax.set_xlabel("$p_2$")

        if i in [0, 5]:
            ax.set_yticks([0, N / 2, N])
            ax.set_yticklabels((0, 1/2, 1))
            ax.set_ylabel("$p_3$")

    fig.tight_layout()

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.3, 0.05, 0.4])
    fig.colorbar(im, cax=cbar_ax)
    fig.savefig("main.pdf", bbox_inches='tight')

if __name__ == "__main__":
    process_data = "process_data" in sys.argv
    main(process_data=process_data)
