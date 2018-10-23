"""
Parameters used for the numerical experiments
"""
import axelrod as axl

REPETITIONS = 60
TURNS = 2000
NOISE = 0.05
PROBEND = 1 / 1000
SEED = 0
PLAYER_GROUPS = {
    "full": [s() for s in axl.strategies if not s.classifier["long_run_time"]],
    "stewart_plotkin": [
        axl.ZDGTFT2(),
        axl.GTFT(),
        axl.TitForTat(),
        axl.TitFor2Tats(),
        axl.HardProber(),
        axl.HardTitFor2Tats(),
        axl.WinStayLoseShift(),
        axl.Random(),
        axl.Prober2(),
        axl.Cooperator(),
        axl.Grudger(),
        axl.HardTitForTat(),
        axl.HardGoByMajority(),
        axl.Calculator(),
        axl.Prober(),
        axl.Joss(),
        axl.Prober3(),
        axl.ZDExtort2(),
        axl.Defector(),
    ],
}
