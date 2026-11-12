from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header

from interface.player_screens import PlayerMenu


class TableTennisTournamentManager(App):
    BINDINGS = [("q", "quit", "Quitter")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Button("Gérer les participants", id="players")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "players":
                self.app.push_screen(PlayerMenu())
