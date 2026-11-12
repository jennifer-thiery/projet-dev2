from lib.tools import ct


def pool_manager(tournament):
    ct()

    # demande a l'utilisateur de choisir un bracket de pool a gerer
    while True:
        ct()
        print("Niveaux de pools disponibles :")
        print("1. Junior")
        print("2. Débutant")
        print("3. Intermédiaire")
        print("4. Expert")
        bracket = input("Entrez le bracket de pool que vous souhaitez gérer (1-4) : ").strip()
        if bracket.isdigit() and 1 <= int(bracket) <= 4:
            break
        else:
            print("Niveau invalide. Veuillez réessayer.")

    print("Voici la liste des pools disponibles : \n")

    bracket = int(bracket) - 1

    for pool in tournament._Tournament__brackets[bracket].pools:
        print(f"ID: {pool._Pool__id} | Niveau: {tournament._Tournament__brackets[bracket].type}")

    # demande un ID de pool à l'utilisateur et verifie que c'est bien un ID de pool existant
    while True:
        pool_id = input("\nEntrez l'ID de la pool que vous souhaitez gérer ou 0 pour revenir en arrière : ").strip()

        if pool_id == "0":
            return
        elif pool_id.isdigit() and 1 <= int(pool_id) <= len(tournament._Tournament__brackets[bracket].pools):
            break
        else:
            print("ID de pool invalide. Veuillez réessayer.")

    pool = tournament._Tournament__brackets[bracket].pools[int(pool_id) - 1]

    while True:
        ct()
        print(pool)

        print(f"\nVous avez choisi la pool : {pool_id} (Niveau: {tournament._Tournament__brackets[bracket].type})")

        print_player_and_match_left(pool)

        print_left_matches(pool)

        print("\n\n\n------------------------------------------------------------------------------------")

        print("1. afficher tout les matchs de la pool")
        print("0. Retour au menu principal")

        choix = input("Entrez votre choix : ").strip()

        match choix:
            case "0":
                break
            case "1":
                print_all_matches_and_add_score(pool)
                print("temp")
            case _:
                print("Choix invalide. Veuillez réessayer.")

    ct()


def print_player_and_match_left(pool):
    """affiche les joueurs dans une pool et le nombre de matchs joués sur ceux a faire"""

    print(f"\nJoueurs de la pool {pool._Pool__id} :")

    for joueur in pool._Pool__players:
        matchs_joues = sum(
            1 for match in pool._Pool__matches if joueur in match._Match__players and match._Match__winner is not None
        )
        matchs_total_a_faire = sum(1 for match in pool._Pool__matches if joueur in match._Match__players)

        print(f"  - {joueur._Player__firstname} {joueur._Player__lastname} [{matchs_joues}/{matchs_total_a_faire}]")

    print("\n")


def print_left_matches(pool):
    """affiche les matchs restants dans une pool"""

    print("\nMatchs restants dans la pool :")

    for match in pool._Pool__matches:
        if match._Match__winner is None:
            print(
                f"  - {match._Match__players[0]._Player__firstname} {match._Match__players[0]._Player__lastname} vs {match._Match__players[1]._Player__firstname} {match._Match__players[1]._Player__lastname} "
            )


def print_all_matches_and_add_score(pool):
    """menu pour modifier les scores d'un match dans une pool selectionner"""
    while True:
        ct()

        print(f"\nTous les matchs de la pool {pool._Pool__id} :")

        for match in pool._Pool__matches:
            score_str = (
                f"{match._Match__scores[0]}-{match._Match__scores[1]}"
                if match._Match__winner is not None
                else "Pas encore joué"
            )

            print(
                f"  - {match._Match__players[0]._Player__firstname} {match._Match__players[0]._Player__lastname} vs {match._Match__players[1]._Player__firstname} {match._Match__players[1]._Player__lastname} | Score: {score_str}"
            )

        print("\n\n\n------------------------------------------------------------------------------------")

        print("1. ajouter un score à un match (fonctionnalité non inclu dans le mvp)")
        print("0. Retour a l'affichage de la pool")

        choix = input("Entrez votre choix : ").strip()
        match choix:
            case "0":
                break
            case _:
                print("Choix invalide. Veuillez réessayer.")
