import axelrod as axl
import numpy as np
import pandas as pd
from collections import Counter

import testzd.data_collection as dc

C, D = axl.Action.C, axl.Action.D

def test_get_vector_from_counter():
    counter = Counter({((C, C), C): 1 / 2, ((C, D), C): 1, ((D, C), C): 1 / 5})
    p = dc.get_vector_from_counter(counter)
    expected_p = np.array([1 / 2, 1, 1 / 5, 0])
    assert np.allclose(p, expected_p)

def test_obtain_pairwise_epsilons():
    players = axl.Cooperator(), axl.TitForTat(), axl.Defector()
    tournament = axl.Tournament(players, turns=5, repetitions=2)

    results = tournament.play()
    expected_epsilon_array = np.array([[0.3334, 0.6667, 1.0001],
                                       [0.6667, 0.3334, 0.3334],
                                       [0.3334, 0.3334, 0.3334]])
    assert np.allclose(dc.obtain_pairwise_epsilons(results),
                       expected_epsilon_array)

def test_analyse_tournament_behaviour():
    players = axl.Cooperator(), axl.TitForTat(), axl.Defector()
    tournament = axl.Tournament(players, turns=5, repetitions=2)
    epsilons = [0.1, 0.2, 0.3]

    results = tournament.play()
    df = dc.analyse_tournament_behaviour(results, epsilons=epsilons)
    assert type(df) is pd.DataFrame
    assert df.shape == (3, 22)
