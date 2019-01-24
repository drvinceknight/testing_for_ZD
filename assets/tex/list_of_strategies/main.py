import imp
import re

parameters = imp.load_source("parameters", "../../../data/raw/parameters.py")

AXELRODPROJECTKEY = "Knight2018"

# Since this research was originally started, an algorithm has been proposed to
# accurately measure the memory of finite state machines:
# https://github.com/Axelrod-Python/Axelrod/pull/1233
# This step manually corrects the known discrepancies but has no effect on the
# results of the work.
# 2018-01-24 - Vince Knight
correct_memory = {
        "Fortress3": 2,
        "Fortress4": 3,
        "Predator": float("inf"),
        "Pun1": float("inf"),
        "Raider": float("inf"),
        "Ripoff": 3,
        "UsuallyCooperates": float("inf"),
        "UsuallyDefects": float("inf"),
        "SolutionB1": 2,
        "SolutionB5": float("inf"),
        "Thumper": float("inf"),
        "Evolved FSM 4": float("inf"),
        "Evolved FSM 16": float("inf"),
        "Evolved FSM 16 Noise 05": float("inf"),
        }

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

            if player.name in correct_memory:
                player.classifier["memory_depth"] = correct_memory[player.name]
            memory_length = str(player.classifier["memory_depth"]).replace(
                "inf", "\(\infty\)"
            )

            f.write(
                f"\item {name} - {kind} - Memory length: {memory_length} - {citation_string}\n"
            )


if __name__ == "__main__":
    main()
