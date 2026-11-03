from time import sleep

from interface.player.forms import form_add_player, form_player_manager
from interface.player.view import show_players
from lib.tools import ct


def show_player_options() -> None:
    print("\n=== Gestion des participants ===")
    print("1. Afficher la liste de tous les participants")
    print("2. Ajouter un participant")
    print("3. Modifier ou supprimer un participant")
    print("0. Revenir au menu principal")


def show_player_menu() -> None:
    while True:
        ct()
        show_player_options()
        choix = input("\nVotre choix : ").strip()

        match choix:
            case "0":
                break
            case "1":
                show_players()
            case "2":
                form_add_player()
            case "3":
                form_player_manager()
            case _:
                print("Choix invalide.")
                sleep(0.5)
