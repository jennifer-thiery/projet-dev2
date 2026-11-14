from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header

from domain.tournament import Tournament
from interface.player_screens import PlayerScreen


class TableTennisTournamentManager(App):
    BINDINGS = [("q", "quit", "Quitter")]

    def __init__(self, tournament: Tournament) -> None:
        super().__init__()
        self.__tournament = tournament

    def compose(self) -> ComposeResult:
        yield Header()
        yield Button("Gérer les participants", id="players")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "players":
                self.app.push_screen(PlayerScreen(tournament=self.__tournament))
