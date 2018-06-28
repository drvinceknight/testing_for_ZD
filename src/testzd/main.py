import numpy as np

def compute_least_squares(p, rstp=np.array([3, 0, 5, 1])):
    """
    Compute the solution via a least squares minimisation problem.

    Returns:

    - xbar
    - residual
    """
    if np.all(np.isfinite(p)):
        R, S, T, P = rstp
        C = np.array([[R - P, R - P],
                      [S - P, T - P],
                      [T - P, S - P]])
        tilde_p = np.array([p[0] - 1, p[1] - 1, p[2]])
        xbar, residuals = np.linalg.lstsq(C, tilde_p, rcond=None)[:2]
        SSError = residuals[0]

        return xbar, SSError
    return (np.nan, np.nan), np.nan

def is_delta_ZD(p, rstp=np.array([3, 0, 5, 1]), delta=10 ** (-7)):
    """
    Check is a strategy p is $\delta$-ZD for a given value of delta
    """
    if np.all(np.isfinite(p)):
        xbar, residual = compute_least_squares(p=p, rstp=rstp)
        return residual <= delta
    return True

def compute_pi(p, q):
    """
    Obtain the steady state distribution for the Markov chain created by two
    memory one players: p and q.
    """
    assert p.shape == (4,)
    assert q.shape == (4,)
    A = np.array([[p[i] * q[j],
                   p[i] * (1 - q[j]),
                   (1 - p[i]) * q[j],
                   (1 - p[i]) * (1 - q[j])]
                   for (i, j) in ((0, 0), (1, 2), (2, 1), (3, 3))])
    val, vec = np.linalg.eig(A.transpose())
    _, pi = val[np.isclose(val, 1)], vec[:, np.isclose(val, 1)]
    return np.real(pi / sum(pi))
