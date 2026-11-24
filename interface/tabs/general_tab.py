from sqlite3 import Error

from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Button

from interface.screens.database_screen import DatabaseScreen
from interface.screens.player_screens import PlayerScreen
from test.generate_result import generate_for_pools


class GeneralTab(Container):
    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Button("Gérer les participants", id="players")
            yield Button("Générer les poules", id="pools")
            yield Button("Gérer la base de données", id="database")
            yield Button("Enregistrer des scores aléatoires", id="pool-generator")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "players":
                self.app.push_screen(PlayerScreen())
            case "pools":
                try:
                    self.app.tournament.add_players_to_brackets()
                except (Error, ValueError) as error:
                    self.notify(f"Génération impossible ({error}).", severity="error")
                    return
                self.app.reload_tournament()
                self.notify("Poules générées et tournoi sauvegardé.")
            case "database":
                self.app.push_screen(DatabaseScreen())
            case "pool-generator":
                try:
                    generate_for_pools(self.app.tournament)
                except (Error, ValueError) as error:
                    self.notify(f"Génération interrompue ({error}).", severity="error")
                else:
                    self.notify("Génération des résultats terminée.")
                self.app.reload_tournament()
