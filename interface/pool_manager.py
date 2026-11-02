from lib.tools import ct


def pool_manager():

    ct()
    # print_all_pool()

    # poule = get_poule_by_id()

    while True:
        ct()
        print(f"\nVous avez choisi la poule : {poule['nom']} (Niveau: {poule['niveau']})")

        # print_player_and_match_left(poule)

        # print_left_matches(poule)

        print("\n\n\n------------------------------------------------------------------------------------")

        print("1. afficher tout les matchs de la poule")
        print("0. Retour au menu principal")

        choix = input("Entrez votre choix : ").strip()

        match choix:
            case "0":
                break
            case "1":
                # print_all_matches_and_add_score(poule)
                print("temp")
            case _:
                print("Choix invalide. Veuillez réessayer.")

    ct()
