import json
from datetime import datetime
from pathlib import Path

from data.action_db_players import import_players_to_db
from data.action_db_tounament import load_tournament
from data.database import reset_database
from domain.enums import FederationRanking
from lib.tools import ct

PLAYERS_FILE = Path(__file__).resolve().parents[1] / "data" / "all_players.json"


def import_players():
    fields = (
        "licence_number",
        "firstname",
        "lastname",
        "birthdate",
        "club",
        "federation_ranking",
        "email",
        "phone_number",
    )
    rankings = list(FederationRanking)
    try:
        players = json.loads(PLAYERS_FILE.read_text(encoding="utf-8-sig"))
        if not isinstance(players, list):
            raise TypeError("Le fichier doit contenir une liste de joueurs.")
        for number, player in enumerate(players, start=1):
            if (
                not isinstance(player, dict)
                or any(not isinstance(player.get(field), str) for field in fields)
                or not isinstance(player.get("second_bracket"), bool)
                or len(player["licence_number"]) != 8
                or not player["licence_number"].isdigit()
                or player["federation_ranking"] not in rankings
            ):
                raise ValueError(f"Joueur {number} invalide.")
            datetime.strptime(player["birthdate"], "%Y-%m-%d")
    except (OSError, TypeError, ValueError) as error:
        print(f"Import impossible ({error}).")
        return

    count = import_players_to_db(players)
    print(
        f"Joueurs importés : {count}. Utilisez l’option 2 du menu principal pour mettre à jour les poules."
    )


def show_database_options() -> None:
    print("\n=== Base de données ===")
    print("1. Afficher la sauvegarde du tournoi")
    print("2. Importer les joueurs depuis all_players.json")
    print("3. Réinitialiser la base de données")
    print("0. Revenir au menu principal")


def show_database_menu() -> bool:
    while True:
        ct()
        show_database_options()
        choix = input("\nVotre choix : ").strip()

        match choix:
            case "0":
                return False
            case "1":
                snapshot = load_tournament()
                print(snapshot if snapshot is not None else "Aucun tournoi sauvegardé.")
            case "2":
                import_players()
            case "3":
                confirmation = input(
                    "Effacer tous les joueurs et la sauvegarde du tournoi ? [O/N] : "
                )
                if confirmation.strip().upper() == "O":
                    reset_database()
                    input(
                        "Base réinitialisée. Appuyez sur Entrée pour revenir au menu principal."
                    )
                    return True
                print("Réinitialisation annulée.")
            case _:
                print("Choix invalide.")
        input("Appuyez sur Entrée pour revenir au menu Base de données.")
