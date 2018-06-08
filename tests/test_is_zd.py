import numpy as np

import testzd as zd

def test_is_delta_ZD_for_valid_ZD_strategy():
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    assert zd.is_delta_ZD(p) == True

def test_is_delta_ZD_for_valid_ZD_strategy_with_different_rstp():
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    rstp = np.array([3, 1, 6, 1])
    assert zd.is_delta_ZD(p, rstp=rstp) == False

def test_is_delta_ZD_for_not_valid_ZD_strategy():
    p = np.array([8 / 9, 1, 1 / 3, 0])
    assert zd.is_delta_ZD(p) == False

def test_is_delta_ZD_for_not_valid_ZD_strategy_with_high_epsilon():
    p = np.array([8 / 9, 1, 1 / 3, 0])
    assert zd.is_delta_ZD(p, delta=10) == True

def test_find_lowest_delta():
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    assert zd.find_lowest_delta(p) == 0.0001

def test_find_lowest_delta_with_non_ZD():
    p = np.array([8 / 9, 1, 1 / 3, 0])
    assert np.isclose(zd.find_lowest_delta(p), 0.0556)
