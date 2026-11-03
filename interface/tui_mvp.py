from interface.player.menu import show_player_menu
from interface.pool_manager import pool_manager
from lib.tools import ct


def show_option() -> None:
    print("\n=== Gestion du tournoi ===")
    print("1. Gérer les participants")
    print("2. Répartir les joueurs dans les poules")
    print("3. Gestion des scores")
    print("4. Gérer les poules")
    print("0. Quitter")


def show_menu() -> None:
    try:
        while True:
            ct()
            show_option()
            choix = input("\nVotre choix : ").strip()

            match choix:
                case "0":
                    print("Au revoir !")
                    break
                case "1":
                    show_player_menu()
                case "2":
                    print("Gérer la liste des participants : fonctionnalité à venir.")
                case "3":
                    print("Répartir les joueurs dans les poules : fonctionnalité à venir.")
                case "4":
                    pool_manager()
                case _:
                    print("Choix invalide.")
    except KeyboardInterrupt:
        print("\nAu revoir !")
