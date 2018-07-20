import numpy as np

import testzd as zd

def test_get_least_squares():
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    xbar, residual = zd.get_least_squares(p)
    assert np.isclose(residual, 0)
    assert np.isclose(xbar[0], 0.055555555555555525)
    assert np.isclose(xbar[1], -0.11111111111111113)

def test_get_least_squares_with_high_residual():
    p = np.array([0, 1 / 2, 1 / 3, 0])
    xbar, residual = zd.get_least_squares(p)
    assert np.isclose(residual, 0.41830065359477125)
    assert np.isclose(xbar[0], -0.04901960784313727)
    assert np.isclose(xbar[1], -0.2156862745098039)

def test_get_least_squares_with_missing_values():
    p = np.array([8 / 9, 1, 1 / 3, np.nan])
    xbar, residual = zd.get_least_squares(p)
    assert np.isnan(residual)
    assert np.isnan(xbar[0])
    assert np.isnan(xbar[1])

def test_compute_least_squares():
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    xbar, residual = zd.compute_least_squares(p)
    assert np.isclose(residual, 0)
    assert np.isfinite(residual)
    assert np.isfinite(xbar[0])
    assert np.isfinite(xbar[1])

def test_compute_least_squares_with_high_residual():
    p = np.array([8 / 9, 1, 1 / 3, 0])
    xbar, residual = zd.compute_least_squares(p)
    assert np.isclose(residual, 0.0588235)
    assert np.isfinite(residual)
    assert np.isfinite(xbar[0])
    assert np.isfinite(xbar[1])

def test_compute_least_squares_with_missing_values():
    p = np.array([8 / 9, 1, 1 / 3, np.nan])
    xbar, residual = zd.compute_least_squares(p)
    assert np.isnan(residual)
    assert np.isnan(xbar[0])
    assert np.isnan(xbar[1])

def test_is_ZD_for_valid_ZD_strategy():
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    assert zd.is_ZD(p) == True

def test_is_ZD_for_valid_ZD_strategy_with_missing_states():
    p = np.array([8 / 9, np.nan, 1 / 3, np.nan])
    assert zd.is_ZD(p) == True

def test_is_ZD_for_valid_ZD_strategy_with_different_rstp():
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    rstp = np.array([3, 1, 6, 1])
    assert zd.is_ZD(p, rstp=rstp) == False

def test_is_ZD_for_not_valid_ZD_strategy():
    p = np.array([8 / 9, 1, 1 / 3, 0])
    assert zd.is_ZD(p) == False

def test_steady_state_distribution_with_specific_players():
    p = np.array([1 / 2, 1 / 3, 7 / 8, 1 / 3])
    q = np.array([1 / 5, 2 / 3, 1 / 8, 1 / 2])
    pi = zd.compute_pi(p, q)
    expected_result = np.array([[0.19402406],
                                [0.2674945 ],
                                [0.17694994],
                                [0.3615315]])
    assert np.allclose(pi, expected_result)

def test_steady_state_distribution_with_tft_v_alternator():
    p = np.array([1, 0, 1, 0])
    q = np.array([0, 1, 0, 1])
    pi = zd.compute_pi(p, q)
    expected_result = np.array([[0.25],
                                [0.25],
                                [0.25],
                                [0.25]])
    assert np.allclose(pi, expected_result)

def test_steady_state_distribution_with_specific_player_v_defector():
    p = np.array([1, 1, .25, .5])
    q = np.array([0, 0, 0, 0])
    pi = zd.compute_pi(p, q)
    expected_result = np.array([[0],
                                [1],
                                [0],
                                [0]])
    assert np.allclose(pi, expected_result)
