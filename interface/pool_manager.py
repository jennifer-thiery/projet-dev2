from lib.tools import ct

debug_poule = False


def pool_manager(tournoit):

    ct()

    # demande a l'utilisateur de choisir un niveau de poule a gerer
    while True:
        ct()
        print("Niveaux de poules disponibles :")
        print("1. Junior")
        print("2. Débutant")
        print("3. Intermédiaire")
        print("4. Expert")
        niveau = input("Entrez le niveau de poule que vous souhaitez gérer (1-4) : ").strip()
        if niveau.isdigit() and 1 <= int(niveau) <= 4:
            break
        else:
            print("Niveau invalide. Veuillez réessayer.")

    print("Voici la liste des poules disponibles : \n")

    niveau = int(niveau) - 1

    for poule in tournoit._Tournament__brackets[niveau].get_pools:
        print(f"ID: {poule._Pool__id} | Niveau: {tournoit._Tournament__brackets[niveau].type}")
        if debug_poule:
            liste = []
            for play in poule.players:
                liste.append(play.federation_ranking)
            print(liste)

    # demande un ID de poule à l'utilisateur et verifie que c'est bien un ID de poule existant
    while True:
        poule_id = input("\nEntrez l'ID de la poule que vous souhaitez gérer ou 0 pour revenir en arrière : ").strip()

        if poule_id == "0":
            return
        elif poule_id.isdigit() and 1 <= int(poule_id) <= len(tournoit._Tournament__brackets[niveau].get_pools):
            break
        else:
            print("ID de poule invalide. Veuillez réessayer.")

    poule = tournoit._Tournament__brackets[niveau].get_pools[int(poule_id) - 1]

    while True:
        ct()
        print(poule)

        print(f"\nVous avez choisi la poule : {poule_id} (Niveau: {tournoit._Tournament__brackets[niveau].type})")

        print_player_and_match_left(poule)

        print_left_matches(poule)

        print("\n\n\n------------------------------------------------------------------------------------")

        print("1. afficher tout les matchs de la poule")
        print("0. Retour au menu principal")

        choix = input("Entrez votre choix : ").strip()

        match choix:
            case "0":
                break
            case "1":
                print_all_matches_and_add_score(poule)
                print("temp")
            case _:
                print("Choix invalide. Veuillez réessayer.")

    ct()


"""affiche les joueurs dans une poule et le nombre de matchs joués sur ceux a faire"""


def print_player_and_match_left(poule):

    print(f"\nJoueurs de la poule {poule._Pool__id} :")

    for joueur in poule._Pool__players:
        matchs_joues = sum(
            1 for match in poule._Pool__matches if joueur in match._Match__players and match._Match__winner is not None
        )
        matchs_total_a_faire = sum(1 for match in poule._Pool__matches if joueur in match._Match__players)

        print(f"  - {joueur._Player__firstname} {joueur._Player__lastname} [{matchs_joues}/{matchs_total_a_faire}]")

    print("\n")


"""affiche les matchs restants dans une poule"""


def print_left_matches(poule):

    print("\nMatchs restants dans la poule :")

    for match in poule._Pool__matches:
        if match._Match__winner is None:
            print(
                f"  - {match._Match__players[0]._Player__firstname} {match._Match__players[0]._Player__lastname} vs {match._Match__players[1]._Player__firstname} {match._Match__players[1]._Player__lastname} "
            )


"""Menu pour afficher les matchs et saisir un score."""


def print_all_matches_and_add_score(poule):
    while True:
        ct()

        print(f"\nTous les matchs de la poule {poule._Pool__id} :")

        for numero, match in enumerate(poule.matches, start=1):
            joueur1, joueur2 = match.players
            scores = match.scores
            score_str = f"{scores[0]}-{scores[1]}" if match.is_played() else "Pas encore joué"
            print(
                f"  {numero}. {joueur1.firstname} {joueur1.lastname} vs "
                f"{joueur2.firstname} {joueur2.lastname} | Score: {score_str}"
            )

        print("\n\n\n------------------------------------------------------------------------------------")

        print("1. Ajouter un score à un match")
        print("0. Retour a l'affichage de la poule")

        choix = input("Entrez votre choix : ").strip()
        match choix:
            case "0":
                break
            case "1":
                add_match_score(poule)
            case _:
                print("Choix invalide. Veuillez réessayer.")


def add_match_score(poule):
    try:
        numero = int(input("Numéro du match (0 pour annuler) : "))
    except ValueError:
        input("Numéro de match invalide. Appuyez sur Entrée.")
        return

    if numero == 0:
        return
    if not 1 <= numero <= len(poule.matches):
        input("Numéro de match invalide. Appuyez sur Entrée.")
        return

    match = poule.matches[numero - 1]
    if match.is_played():
        input("Ce match a déjà un résultat. Appuyez sur Entrée.")
        return

    saisie = input("Scores des sets dans l'ordre des joueurs (ex. 11-8 11-9 12-10) : ").split()
    if not saisie:
        return

    sets = []
    try:
        for score in saisie:
            points1, points2 = score.split("-")
            sets.append((int(points1), int(points2)))
    except ValueError:
        input("Format invalide. Appuyez sur Entrée.")
        return

    confirmation = input("Validez-vous ce résultat définitif ? [O/N] : ").strip().upper()
    if confirmation != "O":
        return

    try:
        match.record_result(sets)
    except ValueError as error:
        input(f"{error} Appuyez sur Entrée.")
        return

    input("Score enregistré pour cette session. Appuyez sur Entrée.")
