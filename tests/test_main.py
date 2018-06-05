import numpy as np

import testzd as zd

def test_create_Mbar_i():
    M = np.array([[3, 3, 1], [0, 5, 1], [5, 0, 1], [1, 1, 1]])
    expected_Mbar_i = np.array([[3, 3, 1], [5, 0, 1], [1, 1, 1]])
    assert np.array_equal(zd.main.create_Mbar_i(M, i=1), expected_Mbar_i)

def test_create_pbar_i():
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    expected_pbar_i = np.array([8 / 9, 1 / 2, 0])
    assert np.allclose(zd.main.create_pbar_i(p, i=2), expected_pbar_i)

def test_find_xbar():
    M = np.array([[3, 3, 1], [0, 5, 1], [5, 0, 1], [1, 1, 1]])
    p = np.array([8 / 9, 1 / 2, 1 / 3, 0])
    expected_xbar_i = np.array([0.25555556, 0.18888889, -0.44444444])
    assert np.allclose(zd.main.find_xbar_i(M, p, i=2), expected_xbar_i)
