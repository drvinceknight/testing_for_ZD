"""
Script to run tournament over full set of strategies in the Axelrod tournament.
"""
import pathlib
import imp
import sys

import axelrod as axl
import numpy as np
import pandas as pd

import parameters


def main(
    group="full",
    tournament_type="std",
    turns=parameters.TURNS,
    noise=parameters.NOISE,
    prob_end=parameters.PROBEND,
    repetitions=parameters.REPETITIONS,
    seed=parameters.SEED,
    player_groups=parameters.PLAYER_GROUPS,
):

    players = player_groups[group]

    if tournament_type == "std":
        tournament = axl.Tournament(
            players, turns=turns, repetitions=repetitions
        )

        assert tournament.turns == turns
        assert tournament.noise == 0
        assert tournament.prob_end is None

    if tournament_type == "noisy":
        tournament = axl.Tournament(
            players, turns=turns, noise=noise, repetitions=repetitions
        )

        assert tournament.turns == turns
        assert tournament.noise == noise
        assert tournament.prob_end is None

    if tournament_type == "probend":
        tournament = axl.Tournament(
            players, prob_end=prob_end, repetitions=repetitions
        )

        assert tournament.turns is None
        assert tournament.noise == 0
        assert tournament.prob_end == prob_end

    path = pathlib.Path("./")
    out_path = path / f"./{group}/{tournament_type}"
    out_path.mkdir(exist_ok=True, parents=True)

    axl.seed(seed)
    assert repetitions == tournament.repetitions

    print(
        f"""

{tournament_type} tournament: {len(tournament.players)} {group} players

     turns={tournament.turns}
     noise={tournament.noise}
     prob_end={tournament.prob_end}
     repetitions={tournament.repetitions}
     seed={seed}

            """
    )

    results = tournament.play(processes=0, filename=str(out_path / "main.csv"))
    results.write_summary(filename=str(out_path / "summary.csv"))


if __name__ == "__main__":

    tournament_type = sys.argv[1]
    group = sys.argv[2]
    main(group=group, tournament_type=tournament_type)
