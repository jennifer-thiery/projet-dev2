from time import sleep

from data.action_db_tounament import save_tournament
from domain.tournament import Tournament
from interface.player.menu import show_player_menu
from interface.pool.manager import pool_manager
from interface.pool.view import show_pools
from lib.tools import ct

tournament = Tournament()
tournament.add_players_to_brackets()
tournament.create_pools_of_brackets()


def show_option() -> None:
    print("\n=== Gestion du tournoi ===")
    print("1. Gérer les participants")
    print("2. Répartir les joueurs dans les poules")
    print("3. Gérer les poules")
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
                    show_player_menu(tournament)
                case "2":
                    show_pools(tournament)
                    save_tournament(tournament)
                case "3":
                    pool_manager(tournament)
                case _:
                    print("Choix invalide.")
                    sleep(0.5)
    except KeyboardInterrupt:
        print("\nAu revoir !")
