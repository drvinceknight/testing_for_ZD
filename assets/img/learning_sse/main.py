"""
A script to generate the value of SSE over a number of turns and generate a
plot.
"""
import axelrod as axl
import numpy as np
import matplotlib.pyplot as plt

import testzd as zd

C, D = axl.Action.C, axl.Action.D


def counter_to_vector(counter):
    """
    Take a counter object and return a numpy 
    array representation of the memory one vector.
    """
    return np.array(
        [
            counter[((C, C), C)],
            counter[((C, D), C)],
            counter[((D, C), C)],
            counter[((D, D), C)],
        ]
    )


def get_p_over_time(players, turns=1_000, seed=None):
    """
    For a given pair of players output an array for each player
    showing the measured memory one vector of their plays over time.
    """
    if seed is not None:
        axl.seed(seed)
    match = axl.Match(players=players, turns=turns)
    interactions = match.play()
    vectors_over_turns = [[], []]
    for turn in range(1, turns):
        interactions_until_turn = interactions[:turn]
        distributions = (
            axl.interaction_utils.compute_normalised_state_to_action_distribution(
                interactions=interactions_until_turn
            )
        )
        for counter, vectors in zip(distributions, vectors_over_turns):
            vectors.append(counter_to_vector(counter=counter))
    return vectors_over_turns


def get_SSE_over_time(players, turns=1_000, seed=None):
    """
    For a given pair of players output an array for each player
    showing the measured memory one vector of their plays over time.
    """
    vectors_over_turns = get_p_over_time(players=players, turns=turns, seed=seed)
    SSEs_over_turns = [np.array([zd.compute_least_squares(p=p)[1] for p in vectors]) for vectors in vectors_over_turns]
    return SSEs_over_turns


def main(player_pairs, repetitions=20, turns=1_000):
    fig, axarr = plt.subplots(1, len(player_pairs), figsize=(12, 4))
    for ax, players in zip(axarr, player_pairs):
        repeated_SSEs_over_time = []
        for seed in range(repetitions):
            repeated_SSEs_over_time.append(
                    get_SSE_over_time(players=players,
                    turns=turns, 
                    seed=seed,
                    )
                )
        mean_SSEs_over_time = [np.mean(SSEs, axis=0) for SSEs in zip(*repeated_SSEs_over_time)]

        for player, mean, style, color in zip(players, mean_SSEs_over_time, ("-",  "--"), ("grey", "black")):
            ax.plot(mean, label=f"{player.name}", linestyle=style, color=color)
        ax.legend()
        ax.set_title(f"{players[0].name} versus {players[1].name}")
        ax.set_xlabel("Turns")
        ax.set_ylabel(f"Mean SSE per turn ({repetitions} repetitions)")
        ax.set_ylim(0, 1.05)
    plt.tight_layout()
    plt.savefig("main.pdf", bbox_inches="tight")


if __name__ == "__main__":
    player_pairs = (
                (axl.EvolvedLookerUp2_2_2(), axl.ZDExtort2v2()),
                (axl.ZDSet2(), axl.ZDExtort2v2()),
                (axl.ZDSet2(), axl.EvolvedLookerUp2_2_2()),
            )

    main(player_pairs=player_pairs, repetitions=20, turns=150)
