import numpy as np

def compute_least_squares(p, rstp=np.array([3, 0, 5, 1])):
    """
    Compute the solution via a least squares minimisation problem.

    Returns:

    - xbar
    - residual
    """
    R, S, T, P = rstp
    M = np.array([[R, R, 1],
                  [S, T, 1],
                  [T, S, 1],
                  [P, P, 1]])
    tilde_p = np.array([p[0] - 1, p[1] - 1, p[2], p[3]])
    xbar, residuals = np.linalg.lstsq(M, tilde_p, rcond=None)[:2]

    return xbar, residuals[0]

def is_delta_ZD(p, rstp=np.array([3, 0, 5, 1]), delta=10 ** (-7)):
    """
    Check is a strategy p is $\delta$-ZD for a given value of delta
    """
    if np.all(np.isfinite(p)):
        xbar, residual = compute_least_squares(p=p, rstp=rstp)
        return residual <= delta
    return True
