import numpy as np


def create_Mbar_i(M, i=3):
    """
    Create the matrix $\bar M^{(i)}$ which is the matrix $M$ with the $i$th row
    removed.
    """
    return np.delete(M, i, axis=0)

def create_pbar_i(p, i=3):
    """
    Create the vector $\bar p^{(i)}$ which is the vector $p$ with the $i$th
    element removed.
    """
    return np.delete(p, i, axis=0)

def find_xbar_i(M, p, i=3):
    """
    Obtain $\bar x ^ {(i)}$: the solution to the equation:

    $\bar M ^{(i)} x^{(i)} = \bar p^{(i)}$
    """
    Mbar_i = create_Mbar_i(M, i=i)
    pbar_i = create_pbar_i(p, i=i)
    return np.linalg.solve(Mbar_i, pbar_i)

def is_epsilon_ZD(p, rstp=np.array([3, 0, 5, 1]), epsilon=10 ** (-7)):
    """
    Check is a strategy p is epsilon-ZD for a given value of epsilon
    """
    R, S, T, P = rstp
    M = np.array([[R, R, 1],
                  [S, T, 1],
                  [T, S, 1],
                  [P, P, 1]])
    p_tilde = np.array([p[0] - 1, p[1] - 1, p[2], p[3]])

    xbars = (find_xbar_i(M, p_tilde, i) for i in range(4))

    return np.min([np.abs(np.dot(M[i], x) - p_tilde[i])
                   for i, x in enumerate(xbars)]) <= epsilon


def find_lowest_epsilon(p, step= 10 ** -4):
    """
    Find the lowest value of $\epsilon$
    for which p is $\epsilon$-ZD.
    """
    epsilon = 0

    while not is_epsilon_ZD(p, epsilon=epsilon):
        epsilon += step

    assert is_epsilon_ZD(p, epsilon=epsilon)

    return epsilon
