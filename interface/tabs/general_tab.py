from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Button

from domain.tournament import Tournament
from interface.screens.player_screens import PlayerScreen


class GeneralTab(Container):
    def __init__(self, id, tournament: Tournament) -> None:
        super().__init__(id=id)
        self.__tournament = tournament

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Button("Gérer les participants", id="players")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "players":
                self.app.push_screen(PlayerScreen(tournament=self.__tournament))
