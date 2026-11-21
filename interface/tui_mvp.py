from time import sleep

from data.action_db_tounament import save_tournament
from data.database import connect_db
from domain.tournament import Tournament
from interface.database_manager import show_database_menu
from interface.player.menu import show_player_menu
from interface.pool_manager import pool_manager
from lib.tools import ct


def show_option() -> None:
    print("\n=== Gestion du tournoi ===")
    print("1. Gérer les participants")
    print("2. Répartir les joueurs dans les poules")
    print("3. Gérer les poules")
    print("4. Base de données")
    print("0. Quitter")


def show_menu() -> None:
    # Crée les tables SQLite dès le premier démarrage.
    connect_db().close()
    tournament = None
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
                    # Recharge les joueurs depuis SQLite avant de recalculer les poules.
                    tournament = Tournament()
                    tournament.generate_brackets()
                    save_tournament(tournament)
                case "3":
                    # Prépare les poules à la première ouverture pour préserver les scores ensuite.
                    if tournament is None:
                        tournament = Tournament()
                        tournament.generate_brackets()
                    pool_manager(tournament)
                case "4":
                    if show_database_menu():
                        # Efface aussi les anciennes poules conservées en mémoire après la réinitialisation.
                        tournament = None
                case _:
                    print("Choix invalide.")
                    sleep(0.5)
    except KeyboardInterrupt:
        print("\nAu revoir !")
