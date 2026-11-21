import json
from datetime import datetime
from pathlib import Path
from sqlite3 import Error

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Static

from data.action_db_players import import_players_to_db
from data.action_db_tounament import load_tournament
from data.database import reset_database
from domain.enums import FederationRanking
from domain.tournament import Tournament
from interface.widgets.confirm_modal import ConfirmModal

PLAYERS_FILE = Path(__file__).resolve().parents[2] / "data" / "all_players.json"


def read_players():
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
    return players


class DatabaseScreen(Screen[bool]):
    TITLE = "Base de données"
    BINDINGS = [("escape", "app.pop_screen", "Retour")]

    def __init__(self, tournament: Tournament):
        super().__init__()
        self.__tournament = tournament

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            Button("Afficher la sauvegarde du tournoi", id="snapshot"),
            Button("Importer les joueurs depuis all_players.json", id="import"),
            Button("Réinitialiser la base de données", id="reset"),
            Static("", id="snapshot-content", markup=False),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "snapshot":
                snapshot = load_tournament()
                content = (
                    json.dumps(snapshot, ensure_ascii=False, indent=2)
                    if snapshot is not None
                    else "Aucun tournoi sauvegardé."
                )
                self.query_one("#snapshot-content", Static).update(content)
            case "import":
                try:
                    count = import_players_to_db(read_players())
                    self.__tournament.load_players()
                except (OSError, TypeError, ValueError, Error) as error:
                    self.notify(f"Import impossible ({error}).", severity="error")
                    return
                self.notify(f"Joueurs importés : {count}. Générez les poules depuis l’onglet Général.")
            case "reset":
                self.app.push_screen(
                    ConfirmModal("Effacer tous les joueurs et la sauvegarde du tournoi ?"), self.reset_confirmed
                )

    def reset_confirmed(self, confirmed: bool | None) -> None:
        if confirmed:
            try:
                reset_database()
            except Error as error:
                self.notify(f"Réinitialisation impossible ({error}).", severity="error")
                return
            self.__tournament.clear()
            self.notify("Base réinitialisée.")
            self.dismiss(True)
