from data.action_db_pools import get_pool_from_db, get_pools_from_db
from lib.tools import ct

def pool_manager():

    ct()
    print("Voici la liste des poules disponibles : \n")

    for poule in get_pools_from_db():
        print(f"ID: {poule['id']}")

    # demande un ID de poule à l'utilisateur et verifie que c'est bien un ID de poule existant
    while True:
        poule_id = input("\nEntrez l'ID de la poule que vous souhaitez gérer : ").strip()

        if poule_id == "0" :
            print("ID de poule invalide. Veuillez réessayer.")
        elif poule_id.isdigit():
            break
        else:
            print("ID de poule invalide. Veuillez réessayer.")

    poule = get_pool_from_db(poule_id)
    
    while True:
        ct()
        print(f"\nVous avez choisi la poule : {poule['id']} (Niveau: faut rajouter un truc pour le niveau de la poule)")

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

    print(
        f"\nJoueurs de la poule {poule['id']} (Niveau: faut rajouter un truc pour le niveau de la poule) et matchs restants :"
    )

    for joueur in poule["players"]:
        matchs_joues = sum(
            1 for match in poule["matches"] if joueur in match["players"] and match["winner"] is not None
        )
        matchs_total_a_faire = sum(1 for match in poule["matches"] if joueur in match["players"])

        print(f"  - {joueur['firstname']} {joueur['lastname']} [{matchs_joues}/{matchs_total_a_faire}]")

    print("\n")


"""affiche les matchs restants dans une poule"""


def print_left_matches(poule):

    print("\nMatchs restants dans la poule :")

    for match in poule["matches"]:
        if match["winner"] is None:
            print(
                f"  - {match['players'][0]['firstname']} {match['players'][0]['lastname']} vs {match['players'][1]['firstname']} {match['players'][1]['lastname']} "
            )


"""menu pour modifier les scores d'un match dans une poule selectionner"""


def print_all_matches_and_add_score(poule):
    while True:
        ct()

        print(
            f"\nTous les matchs de la poule {poule['id']} (Niveau: faut rajouter un truc pour le niveau de la poule) :"
        )

        for match in poule["matches"]:
            score_str = (
                f"{match['scores'][0]}-{match['scores'][1]}" if match["winner"] is not None else "Pas encore joué"
            )

            print(
                f"  - {match['players'][0]['firstname']} {match['players'][0]['lastname']} vs {match['players'][1]['firstname']} {match['players'][1]['lastname']} | Score: {score_str}"
            )

        print("\n\n\n------------------------------------------------------------------------------------")

        print("1. ajouter un score à un match (fonctionnalité non inclu dans le mvp)")
        print("0. Retour a l'affichage de la poule")

        choix = input("Entrez votre choix : ").strip()
        match choix:
            case "0":
                break
            case _:
                print("Choix invalide. Veuillez réessayer.")
