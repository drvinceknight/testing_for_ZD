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

import axelrod as axl
import numpy as np

import testzd.data_collection as dc

parameters = imp.load_source('paremeters', '../paremeters.py')

def main(players,
         turns=parameters.TURNS,
         noise=parameters.NOISE,
         prob_end=parameters.PROBEND,
         epsilons=parameters.EPSILONS,
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
    for key, tournament in tournaments.items():
        axl.seed(seed)
        result_set = tournament.play(processes=0)

        out_path = path / f"./pairwise_epsilon/{key}"
        out_path.mkdir(exist_ok=True, parents=True)
        pairwise_epsilon = dc.obtain_pairwise_epsilons(result_set)
        np.savetxt(str(out_path / "main.csv"), pairwise_epsilon)

        out_path = path / f"./behaviour/{key}"
        out_path.mkdir(exist_ok=True, parents=True)
        behaviour = dc.analyse_tournament_behaviour(result_set,
                                                    epsilons=epsilons)
        behaviour.to_csv(str(out_path / "main.csv"), index=False)


if __name__ == "__main__":
    players = [s() for s in axl.strategies]
    main(players)
