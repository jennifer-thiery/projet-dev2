def show_pools(tournament):
    for bracket in tournament.brackets:
        print(f"\nTableau {bracket.type}")
        print("-" * 80)

        for pool in bracket.pools:
            print(f"\nPoule {pool.id} :")

            for player in pool.players:
                print(f"{player.firstname} {player.lastname} ({player.licence_number}) - {player.federation_ranking}")

    input("\n[Enter] pour revenir au menu principal")
