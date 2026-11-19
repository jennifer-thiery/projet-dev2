from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static


class ScoreModal(ModalScreen):
    BINDINGS = [("escape", "app.pop_screen", "Annuler")]

    def __init__(self, match):
        super().__init__()
        self.__match = match

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="modal-content"):
            yield Label("Score du match")
            yield Label(f"\n{self.__match.players[0].firstname} {self.__match.players[0].lastname}")
            yield Input(type="integer", id="score-p1")
            yield Label(f"\n{self.__match.players[1].firstname} {self.__match.players[1].lastname}")
            yield Input(type="integer", id="score-p2")

            yield Static("", id="error")
            yield Button("Valider")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        pass
