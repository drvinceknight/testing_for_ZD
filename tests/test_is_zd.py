import numpy as np

import testzd as zd

def test_is_epsilon_ZD_for_valid_ZD_strategy():
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    assert zd.is_epsilon_ZD(p) == True

def test_is_epsilon_ZD_for_valid_ZD_strategy_with_different_rstp():
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    rstp = np.array([3, 1, 6, 1])
    assert zd.is_epsilon_ZD(p, rstp=rstp) == False

def test_is_epsilon_ZD_for_not_valid_ZD_strategy():
    p = np.array([8 / 9, 1, 1 / 3, 0])
    assert zd.is_epsilon_ZD(p) == False

def test_is_epsilon_ZD_for_not_valid_ZD_strategy_with_high_epsilon():
    p = np.array([8 / 9, 1, 1 / 3, 0])
    assert zd.is_epsilon_ZD(p, epsilon=10) == True
