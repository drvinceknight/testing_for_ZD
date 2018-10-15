import imp
import re

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")

AXELRODPROJECTKEY = "Knight2018"


def main():
    with open("main.tex", "w") as f:
        for player in parameters.PLAYER_GROUPS["full"]:
            name = player.__repr__().replace("_", "\_")
            docstring = player.__doc__

            reference_keys = re.findall("\[.*?\]_", docstring)
            for i, key in enumerate(reference_keys):
                reference_keys[i] = key[1:-2]
            if len(reference_keys) == 0:
                reference_keys = [AXELRODPROJECTKEY]

            reference_keys = set(reference_keys)
            citation_string = f"\cite{reference_keys}".replace("'", "")

            kind = (
                "Stochastic"
                if player.classifier["stochastic"]
                else "Deterministic"
            )
            memory_length = str(player.classifier["memory_depth"]).replace(
                "inf", "\(\infty\)"
            )

            f.write(
                f"\item {name} - {kind} - Memory length: {memory_length} - {citation_string}\n"
            )


if __name__ == "__main__":
    main()
