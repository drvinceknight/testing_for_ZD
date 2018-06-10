import numpy as np

import testzd as zd

def test_compute_least_squares():
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    _, residual = zd.compute_least_squares(p)
    assert np.isclose(residual, 0)

def test_compute_least_squares_with_high_residual():
    p = np.array([8 / 9, 1, 1 / 3, 0])
    _, residual = zd.compute_least_squares(p)
    assert np.isclose(residual, 5 / 90)

def test_is_delta_ZD_for_valid_ZD_strategy():
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    assert zd.is_delta_ZD(p) == True

def test_is_delta_ZD_for_valid_ZD_strategy_with_missing_states():
    p = np.array([8 / 9, np.nan, 1 / 3, np.nan])
    assert zd.is_delta_ZD(p) == True

def test_is_delta_ZD_for_valid_ZD_strategy_with_different_rstp():
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    rstp = np.array([3, 1, 6, 1])
    assert zd.is_delta_ZD(p, rstp=rstp) == False

def test_is_delta_ZD_for_not_valid_ZD_strategy():
    p = np.array([8 / 9, 1, 1 / 3, 0])
    assert zd.is_delta_ZD(p) == False

def test_is_delta_ZD_for_not_valid_ZD_strategy_with_high_delta():
    p = np.array([8 / 9, 1, 1 / 3, 0])
    assert zd.is_delta_ZD(p, delta=10) == True
