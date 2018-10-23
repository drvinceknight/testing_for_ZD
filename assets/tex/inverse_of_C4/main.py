import sympy as sym


def main():
    R, S, T, P = sym.S(3), sym.S(0), sym.S(5), sym.S(1)
    tilde_p = sym.Matrix(
        [sym.S(8) / 9 - 1, sym.S(1) / 2 - 1, sym.S(1) / 3, sym.S(0)]
    )
    M = sym.Matrix([[R, R, 1], [S, T, 1], [T, S, 1], [P, P, 1]])
    with open("main.tex", "w") as f:
        f.write(sym.latex(M[:3, :].inv()))
        M[:3, :].inv()


if __name__ == "__main__":
    main()
