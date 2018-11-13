import numpy as np

def approximate_p(p, p_emptyset=1/2):
    """
    Approximate missing state probabilities with p_emptyset
    """
    p[~np.isfinite(p)] = p_emptyset
    return p

def is_ZD(p, p_emptyset=1/2, rstp=np.array([3, 0, 5, 1]), delta=10 ** (-7)):
    """
    Check is a strategy p is ZD.
    """
    p = approximate_p(p=p, p_emptyset=p_emptyset)
    R, S, T, P = rstp
    tilde_p = np.array([p[0] - 1, p[1] - 1, p[2], p[3]])
    expected_tilde_p1 = (
        P * tilde_p[1] + P * tilde_p[2] - R * tilde_p[1] - R * tilde_p[2]
    ) / (2 * P - S - T)
    chi = (
        P * tilde_p[1] - P * tilde_p[2] + S * tilde_p[2] - T * tilde_p[1]
    ) / (P * tilde_p[1] - P * tilde_p[2] - S * tilde_p[1] + T * tilde_p[2])
    return (
        np.isclose(expected_tilde_p1, tilde_p[0]) and chi > 1 and p[3] == 0
    )


def compute_least_squares(p, p_emptyset=1/2, rstp=np.array([3, 0, 5, 1])):
    """
    Compute the solution via a least squares minimisation problem.

    Returns:

    - xstar
    - residual
    """
    p = approximate_p(p=p, p_emptyset=p_emptyset)
    R, S, T, P = rstp
    C = np.array([[R - P, R - P], [S - P, T - P], [T - P, S - P]])
    tilde_p = np.array([p[0] - 1, p[1] - 1, p[2]])
    xstar, residuals = np.linalg.lstsq(C, tilde_p, rcond=None)[:2]
    SSError = residuals[0]

    return xstar, SSError


def get_least_squares(p, p_emptyset=1/2, rstp=np.array([3, 0, 5, 1])):
    """
    Obtain the least squares directly

    Returns:

    - xstar
    - residual
    """
    p = approximate_p(p=p, p_emptyset=p_emptyset)
    R, S, T, P = rstp
    C = np.array([[R - P, R - P], [S - P, T - P], [T - P, S - P]])
    tilde_p = np.array([p[0] - 1, p[1] - 1, p[2]])
    xstar = np.linalg.inv(C.transpose() @ C) @ C.transpose() @ tilde_p
    SSError = tilde_p.transpose() @ tilde_p - tilde_p @ C @ xstar
    return xstar, SSError


def compute_pi(p, q):
    """
    Obtain the steady state distribution for the Markov chain created by two
    memory one players: p and q.
    """
    assert p.shape == (4,)
    assert q.shape == (4,)
    A = np.array(
        [
            [
                p[i] * q[j],
                p[i] * (1 - q[j]),
                (1 - p[i]) * q[j],
                (1 - p[i]) * (1 - q[j]),
            ]
            for (i, j) in ((0, 0), (1, 2), (2, 1), (3, 3))
        ]
    )
    val, vec = np.linalg.eig(A.transpose())
    _, pi = val[np.isclose(val, 1)], vec[:, np.isclose(val, 1)]
    return np.real(pi / sum(pi))
