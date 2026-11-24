import json
from datetime import datetime
from pathlib import Path
from sqlite3 import Error

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Static

from data.action_db_players import import_players_to_db
from data.database import reset_database
from domain.enums import FederationRanking
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

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            Button("Afficher la sauvegarde du tournoi", id="snapshot"),
            Button("Importer les joueurs depuis all_players.json", id="import"),
            Button("Réinitialiser la base de données", id="reset"),
            Static("", id="snapshot-content", markup=False),
        )
        yield Footer()

    def show_snapshot(self) -> None:
        tournament = self.app.tournament
        lines = [f"Participants inscrits : {len(tournament.all_players)}"]
        for bracket in tournament.brackets:
            if bracket.players:
                matches = bracket.matches.copy()
                for pool in bracket.pools:
                    matches.extend(pool.matches)
                played = sum(match.is_played() for match in matches)
                lines.append(
                    f"{bracket.type.value} · {bracket.current_state.value} · "
                    f"{len(bracket.pools)} poules · {played}/{len(matches)} matchs joués"
                )
        self.query_one("#snapshot-content", Static).update("\n".join(lines))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "snapshot":
                self.app.reload_tournament()
            case "import":
                try:
                    players = import_players_to_db(read_players())
                except (OSError, TypeError, ValueError, Error) as error:
                    self.notify(f"Import impossible ({error}).", severity="error")
                    return
                self.app.reload_tournament()
                self.notify(f"Joueurs importés : {len(players)}. Générez les poules depuis l’onglet Général.")
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
            self.app.reload_tournament()
            self.notify("Base réinitialisée.")
            self.dismiss(True)
