import numpy as np

def is_delta_ZD(p, rstp=np.array([3, 0, 5, 1]), delta=10 ** (-7)):
    """
    Check is a strategy p is $\delta$-ZD for a given value of epsilon
    """
    R, S, T, P = rstp
    M = np.array([[R, R, 1],
                  [S, T, 1],
                  [T, S, 1],
                  [P, P, 1]])
    tilde_p = np.array([p[0] - 1, p[1] - 1, p[2], p[3]])

    tilde_p = tilde_p[np.isfinite(p)]
    M = M[np.isfinite(p)]

    xbar = np.linalg.lstsq(M, tilde_p, rcond=None)[0]

    return np.linalg.norm(np.dot(M, xbar) - tilde_p) ** 2 <= delta

def find_lowest_delta(p, step= 10 ** -4):
    """
    Find the lowest value of $\delta$
    for which p is $\delta$-ZD.
    """
    delta = 0

    while not is_delta_ZD(p, delta=delta):
        delta += step

    assert is_delta_ZD(p, delta=delta)

    return delta
