"""
Script to run tournament over full set of strategies in the Axelrod tournament.

Outputs two data sets:

    - ./pairwise_epsilon/<type>/main.csv: a matrix showing the value of epsilon that
      ensures each player plays as an epsilon-ZD strategy
    - ./behaviour/<type>/main.csv: a data frame describing a number of statistics for
      a range of values of epsilon.
"""
import pathlib
import imp
import sys

import axelrod as axl
import numpy as np
import pandas as pd

import parameters

def main(players,
         tournament_type="std",
         turns=parameters.TURNS,
         noise=parameters.NOISE,
         prob_end=parameters.PROBEND,
         repetitions=parameters.REPETITIONS,
         seed=parameters.SEED):

    tournaments = {"std": axl.Tournament(players,
                                         turns=turns,
                                         repetitions=repetitions),
                   "noisy": axl.Tournament(players,
                                           turns=turns,
                                           noise=noise,
                                           repetitions=repetitions),
                   "probend": axl.Tournament(players,
                                             prob_end=prob_end,
                                             repetitions=repetitions)}

    stewart_and_plotkin_players = [axl.Cooperator(),
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
    full_players = [s() for s in axl.strategies
                    if not s.classifier["long_run_time"]]

    players_sets = {"stewart_plotkin": stewart_and_plotkin_players,
                    "full": full_players}

    path = pathlib.Path("./")
    tournament = tournaments[tournament_type]
    out_path = path / f"./{players}/{tournament_type}"
    out_path.mkdir(exist_ok=True, parents=True)

    axl.seed(seed)

    results = tournament.play(processes=0, filename=str(out_path / "main.csv"))
    results.write_summary(filename=str(out_path / "summary.csv"))

if __name__ == "__main__":

    tournament_type = sys.argv[1]
    players = sys.argv[2]
    main(players=players, tournament_type=tournament_type)
