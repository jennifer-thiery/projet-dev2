from sqlite3 import Error

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane

from data.action_db_tournament import load_tournament
from domain.tournament import Tournament
from interface.screens.database_screen import DatabaseScreen
from interface.screens.player_screens import PlayerScreen
from interface.tabs.all_match_tab import AllMatchTab
from interface.tabs.bracket_tab import BracketTab
from interface.tabs.general_tab import GeneralTab


class TableTennisTournamentManager(App):
    BINDINGS = [("q", "quit", "Quitter")]

    CSS_PATH = "style.tcss"

    def __init__(self, tournament: Tournament) -> None:
        super().__init__()
        self.tournament = tournament

    def reload_tournament(self, saved: bool | None = True) -> None:
        if not saved:
            return
        try:
            self.tournament = load_tournament()
        except (Error, ValueError) as error:
            self.notify(f"Actualisation impossible ({error}).", severity="error")
            return

        main_screen = self.screen_stack[0]
        for tab in main_screen.query(BracketTab):
            tab.call_later(tab.refresh_view)
        main_screen.query_one(AllMatchTab).refresh_matches()

        if isinstance(self.screen, PlayerScreen):
            self.screen.update_players()
        elif isinstance(self.screen, DatabaseScreen):
            self.screen.show_snapshot()

    def compose(self) -> ComposeResult:
        yield Header()

        with TabbedContent(initial="tab-general"):
            with TabPane("Général", id="tab-general"):
                yield GeneralTab(id="container-general")
            for bracket in self.tournament.brackets:
                with TabPane(id=f"tab-{bracket.type.name.lower()}", title=bracket.type.value):
                    yield BracketTab(
                        id=f"container-{bracket.type.name.lower()}",
                        bracket_type=bracket.type,
                    )
            with TabPane("All match", id="all-match"):
                yield AllMatchTab(id="container-all-matches")

        yield Footer()
