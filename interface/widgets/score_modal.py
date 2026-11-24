from copy import copy
from sqlite3 import Error

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static

from data.action_db_tournament import save_match_result
from domain.enums import BracketType
from domain.match import Match


class ScoreModal(ModalScreen[bool]):
    BINDINGS = [("escape", "app.pop_screen", "Annuler")]

    def __init__(self, match: Match, bracket_type: BracketType) -> None:
        super().__init__()
        self.__match = match
        self.__bracket_type = bracket_type

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="modal-content"):
            yield Label("Score du match")
            player1, player2 = self.__match.players
            yield Label(f"{player1.firstname} {player1.lastname} – {player2.firstname} {player2.lastname}")
            if self.__match.is_played():
                yield Label(" ".join(f"{first}-{second}" for first, second in self.__match.sets))
                return

            yield Label("Saisissez les scores des sets dans l’ordre des joueurs.")
            yield Input(placeholder="11-8 11-9 12-10", id="scores")
            yield Static("", id="error")
            yield Button("Valider le résultat définitif")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        error = self.query_one("#error", Static)
        sets = []
        try:
            for score in self.query_one("#scores", Input).value.split():
                first, second = score.split("-")
                sets.append((int(first), int(second)))
        except ValueError:
            error.update("Format attendu : 11-8 11-9 12-10.")
            return

        try:
            result = copy(self.__match)
            result.record_result(sets)
            save_match_result(self.__bracket_type, result)
        except ValueError as validation_error:
            error.update(str(validation_error))
            return
        except (Error, OverflowError) as save_error:
            error.update(f"Sauvegarde impossible ({save_error}).")
            return
        self.dismiss(True)
