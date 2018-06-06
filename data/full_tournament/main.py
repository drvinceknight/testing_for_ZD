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

parameters = imp.load_source('paremeters', '../paremeters.py')

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

    path = pathlib.Path("./")
    tournament = tournaments[tournament_type]
    out_path = path / f"./interactions/{tournament_type}"
    out_path.mkdir(exist_ok=True, parents=True)

    axl.seed(seed)
    results = tournament.play(processes=0, filename=str(out_path / "main.csv"))

    out_path = path / f"./summary/{tournament_type}"
    out_path.mkdir(exist_ok=True, parents=True)
    df = pd.DataFrame(results.summarise())
    df.to_csv(str(out_path / "main.csv"), index=False)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        tournament_type = sys.argv[1]
    else:
        tournament_type = "std"
    players = [s() for s in axl.strategies]
    main(players=players, tournament_type=tournament_type)
