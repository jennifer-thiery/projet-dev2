from time import sleep

from data.action_db_tounament import load_tournament, save_tournament
from domain.tournament import Tournament
from interface.player.menu import show_player_menu
from interface.pool_manager import pool_manager
from lib.tools import ct

tournament = Tournament("2019-12-04", "2019-12-06")
tournament.create_brackets()
save_tournament(tournament)


def show_option() -> None:
    print("\n=== Gestion du tournoi ===")
    print("1. Gérer les participants")
    print("2. Répartir les joueurs dans les poules")
    print("3. Gérer les poules")
    print("4. Afficher fichier")
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
                    tournament.create_brackets()
                    save_tournament(tournament)
                case "3":
                    pool_manager(tournament)
                case "4":
                    print(load_tournament())
                    sleep(20)
                case _:
                    print("Choix invalide.")
                    sleep(0.5)
    except KeyboardInterrupt:
        print("\nAu revoir !")
