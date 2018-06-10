import pathlib
import imp

parameters = imp.load_source('parameters',
                             '../../../data/raw/parameters.py')

def main():
    N = len(parameters.PLAYER_GROUPS["stewart_plotkin"])
    with open("main.tex", "w") as f:
        f.write(str(N))

if __name__ == "__main__":
    main()
