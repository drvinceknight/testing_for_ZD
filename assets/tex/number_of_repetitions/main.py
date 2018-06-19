import pathlib
import imp

parameters = imp.load_source('parameters',
                             '../../../data/raw/parameters.py')

def main():
    with open("main.tex", "w") as f:
        f.write(str(parameters.REPETITIONS))

if __name__ == "__main__":
    main()
