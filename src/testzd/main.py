import numpy as np

def is_epsilon_ZD(p, rstp=np.array([3, 0, 5, 1]), epsilon=10 ** (-7)):
    """
    Check is a strategy p is epsilon-ZD for a given value of epsilon
    """
    R, S, T, P = rstp
    M = np.array([[R, R, 1],
                  [S, T, 1],
                  [T, S, 1],
                  [P, P, 1]])

    M_bar = M[:3, :3]

    p_tilde = np.array([p[0] - 1, p[1] - 1, p[2], p[3]])
    p_bar = p_tilde[:3]

    x = np.linalg.solve(M_bar, p_bar)

    return np.abs(np.dot(M[3], x) - p_tilde[3]) <= epsilon
