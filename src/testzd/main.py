import numpy as np


def is_ZD(p, rstp=np.array([3, 0, 5, 1]), delta=10 ** (-7)):
    """
    Check is a strategy p is ZD.
    """
    if np.all(np.isfinite(p)):
        R, S, T, P = rstp
        tilde_p = np.array([p[0] - 1, p[1] - 1, p[2], p[3]])
        expected_tilde_p1 = (
            P * tilde_p[1] + P * tilde_p[2] - R * tilde_p[1] - R * tilde_p[2]
        ) / (2 * P - S - T)
        chi = (P * tilde_p[1] - P * tilde_p[2] + S * tilde_p[2] - T * tilde_p[1]) / (
            P * tilde_p[1] - P * tilde_p[2] - S * tilde_p[1] + T * tilde_p[2]
        )
        return np.isclose(expected_tilde_p1, tilde_p[0]) and chi > 1 and p[3] == 0
    return True


def compute_least_squares(p, rstp=np.array([3, 0, 5, 1])):
    """
    Compute the solution via a least squares minimisation problem.

    Returns:

    - xbar
    - residual
    """
    if np.all(np.isfinite(p)):
        R, S, T, P = rstp
        C = np.array([[R - P, R - P], [S - P, T - P], [T - P, S - P]])
        tilde_p = np.array([p[0] - 1, p[1] - 1, p[2]])
        xbar, residuals = np.linalg.lstsq(C, tilde_p, rcond=None)[:2]
        SSError = residuals[0]

        return xbar, SSError
    return (np.nan, np.nan), np.nan


def get_least_squares(p, rstp=np.array([3, 0, 5, 1])):
    """
    Obtain the least squares directly

    Returns:

    - xbar
    - residual
    """
    if np.all(np.isfinite(p)):
        R, S, T, P = rstp
        C = np.array([[R - P, R - P], [S - P, T - P], [T - P, S - P]])
        tilde_p = np.array([p[0] - 1, p[1] - 1, p[2]])
        alpha = (
            3 * P ** 2 * tilde_p[1]
            - 3 * P ** 2 * tilde_p[2]
            - 2 * P * R * tilde_p[1]
            + 2 * P * R * tilde_p[2]
            - P * S * tilde_p[0]
            - 3 * P * S * tilde_p[1]
            + P * S * tilde_p[2]
            + P * T * tilde_p[0]
            - P * T * tilde_p[1]
            + 3 * P * T * tilde_p[2]
            + R ** 2 * tilde_p[1]
            - R ** 2 * tilde_p[2]
            + R * S * tilde_p[0]
            - R * T * tilde_p[0]
            + S ** 2 * tilde_p[1]
            + S * T * tilde_p[1]
            - S * T * tilde_p[2]
            - T ** 2 * tilde_p[2]
        ) / (
            6 * P ** 2 * S
            - 6 * P ** 2 * T
            - 4 * P * R * S
            + 4 * P * R * T
            - 4 * P * S ** 2
            + 4 * P * T ** 2
            + 2 * R ** 2 * S
            - 2 * R ** 2 * T
            + S ** 3
            + S ** 2 * T
            - S * T ** 2
            - T ** 3
        )
        beta = (
            -3 * P ** 2 * tilde_p[1]
            + 3 * P ** 2 * tilde_p[2]
            + 2 * P * R * tilde_p[1]
            - 2 * P * R * tilde_p[2]
            - P * S * tilde_p[0]
            + P * S * tilde_p[1]
            - 3 * P * S * tilde_p[2]
            + P * T * tilde_p[0]
            + 3 * P * T * tilde_p[1]
            - P * T * tilde_p[2]
            - R ** 2 * tilde_p[1]
            + R ** 2 * tilde_p[2]
            + R * S * tilde_p[0]
            - R * T * tilde_p[0]
            + S ** 2 * tilde_p[2]
            - S * T * tilde_p[1]
            + S * T * tilde_p[2]
            - T ** 2 * tilde_p[1]
        ) / (
            (S - T)
            * (
                6 * P ** 2
                - 4 * P * R
                - 4 * P * S
                - 4 * P * T
                + 2 * R ** 2
                + S ** 2
                + 2 * S * T
                + T ** 2
            )
        )
        xbar = np.array([alpha, beta])
        SSError = (
            2 * P * tilde_p[0]
            - P * tilde_p[1]
            - P * tilde_p[2]
            + R * tilde_p[1]
            + R * tilde_p[2]
            - S * tilde_p[0]
            - T * tilde_p[0]
        ) ** 2 / (
            6 * P ** 2
            - 4 * P * R
            - 4 * P * S
            - 4 * P * T
            + 2 * R ** 2
            + S ** 2
            + 2 * S * T
            + T ** 2
        )
        return xbar, SSError
    return (np.nan, np.nan), np.nan


def compute_pi(p, q):
    """
    Obtain the steady state distribution for the Markov chain created by two
    memory one players: p and q.
    """
    assert p.shape == (4,)
    assert q.shape == (4,)
    A = np.array(
        [
            [p[i] * q[j], p[i] * (1 - q[j]), (1 - p[i]) * q[j], (1 - p[i]) * (1 - q[j])]
            for (i, j) in ((0, 0), (1, 2), (2, 1), (3, 3))
        ]
    )
    val, vec = np.linalg.eig(A.transpose())
    _, pi = val[np.isclose(val, 1)], vec[:, np.isclose(val, 1)]
    return np.real(pi / sum(pi))
