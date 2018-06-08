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

def main(player_group="full",
         tournament_type="std",
         turns=parameters.TURNS,
         noise=parameters.NOISE,
         prob_end=parameters.PROBEND,
         repetitions=parameters.REPETITIONS,
         seed=parameters.SEED):

    if player_group == "full":
        players = [s() for s in axl.strategies
                   if not s.classifier["long_run_time"]]
    if player_group == "stewart_plotkin":
        players = [axl.Cooperator(),
                   axl.Defector(),
                   axl.ZDExtort2(),
                   axl.HardGoByMajority(),
                   axl.Joss(),
                   axl.HardTitForTat(),
                   axl.HardTitFor2Tats(),
                   axl.TitForTat(),
                   axl.Grudger(),
                   axl.GTFT(),
                   axl.TitFor2Tats(),
                   axl.WinStayLoseShift(),
                   axl.Random(),
                   axl.ZDGTFT2()]

    if tournament_type == "std":
        tournament = axl.Tournament(players,
                                    turns=turns,
                                    repetitions=repetitions)
    if tournament_type == "noisy":
        tournament = axl.Tournament(players,
                                    turns=turns,
                                    noise=noise,
                                    repetitions=repetitions)
    if tournament_type == "probend":
        tournament = axl.Tournament(players,
                                    prob_end=prob_end,
                                    repetitions=repetitions)

    path = pathlib.Path("./")
    out_path = path / f"./{player_group}/{tournament_type}"
    out_path.mkdir(exist_ok=True, parents=True)

    axl.seed(seed)

    results = tournament.play(processes=0, filename=str(out_path / "main.csv"))
    results.write_summary(filename=str(out_path / "summary.csv"))

if __name__ == "__main__":

    tournament_type = sys.argv[1]
    player_group = sys.argv[2]
    print(f"""

Playing {tournament_type} tournament with {player_group} players

     turns={parameters.TURNS}
     noise={parameters.NOISE}
     prob_end={parameters.PROBEND}
     repetitions={parameters.REPETITIONS}
     seed={parameters.SEED}

            """)
    main(player_group=player_group, tournament_type=tournament_type)
