from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Button

from data.action_db_tounament import save_tournament
from domain.tournament import Tournament
from interface.screens.database_screen import DatabaseScreen
from interface.screens.player_screens import PlayerScreen
from interface.tabs.bracket_tab import BracketTab
from test.generate_result import generate_for_pools


class GeneralTab(Container):
    def __init__(self, id, tournament: Tournament) -> None:
        super().__init__(id=id)
        self.__tournament = tournament

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Button("Gérer les participants", id="players")
            yield Button("Générer les poules", id="pools")
            yield Button("Gérer la base de données", id="database")
            yield Button("Générer resultat des poules", id="pool-generator")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "players":
                self.app.push_screen(PlayerScreen(tournament=self.__tournament))
            case "pools":
                self.__tournament.add_players_to_brackets()
                save_tournament(self.__tournament)
                await self.refresh_brackets(True)
                self.notify("Poules générées et tournoi sauvegardé.")
            case "database":
                self.app.push_screen(DatabaseScreen(self.__tournament), self.refresh_brackets)
            case "pool-generator":
                await generate_for_pools(self.__tournament)
                self.notify("Les résultat des poules générées.")

    async def refresh_brackets(self, changed: bool | None) -> None:
        if changed:
            for bracket_tab in self.app.query(BracketTab):
                await bracket_tab.recompose()
