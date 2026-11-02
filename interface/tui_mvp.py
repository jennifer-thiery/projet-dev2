from interface.player_form import form_add_player
from lib.tools import ct


def show_option() -> None:
    print("\n=== Gestion du tournoi ===")
    print("1. Ajouter des participants")
    print("2. Gérer la liste des participants")
    print("3. Répartir les joueurs dans les poules")
    print("4. Gestion des scores")
    print("0. Quitter")


def show_menu() -> None:
    while True:
        ct()
        show_option()
        choix = input("\nVotre choix : ").strip()

        match choix:
            case "0":
                print("Au revoir !")
                break
            case "1":
                print("Ajouter des participants : fonctionnalité à venir.")
                form_add_player()
            case "2":
                print("Gérer la liste des participants : fonctionnalité à venir.")
            case "3":
                print("Répartir les joueurs dans les poules : fonctionnalité à venir.")
            case "4":
                print("Gestion des scores : fonctionnalité à venir.")
            case _:
                print("Choix invalide.")
