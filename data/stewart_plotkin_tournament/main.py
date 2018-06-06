import imp
main = imp.load_source('main', '../full_tournament/main.py')


if __name__ == "__main__":
    import axelrod as axl

    stewart_and_plotkin_players = [axl.Cooperator(),
                                   axl.Defector(),
                                   axl.ZDExtort2(),
                                   axl.HardGoByMajority(),
                                   axl.Joss(),
                                   axl.HardTitForTat(),
                                   axl.HardTitFor2Tats(),
                                   axl.TitForTat(),
                                   axl.Grudger(),
                                   axl.GTFT(),
                                   axl.TitFor2Tats(),
                                   axl.WinStayLoseShift(),
                                   axl.Random(),
                                   axl.ZDGTFT2()]
    for tournament_type in ("std", "noisy", "probend"):
        main.main(players=stewart_and_plotkin_players,
                  tournament_type=tournament_type)
