from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane

from domain.tournament import Tournament
from interface.tabs.all_match_tab import AllMatchTab
from interface.tabs.bracket_tab import BracketTab
from interface.tabs.general_tab import GeneralTab


class TableTennisTournamentManager(App):
    BINDINGS = [("q", "quit", "Quitter")]

    CSS_PATH = "style.tcss"

    def __init__(self, tournament: Tournament) -> None:
        super().__init__()
        self.__tournament = tournament

    def compose(self) -> ComposeResult:
        yield Header()

        with TabbedContent(initial="tab-general"):
            with TabPane("Général", id="tab-general"):
                yield GeneralTab(id="container-general", tournament=self.__tournament)
            for bracket in self.__tournament.brackets:
                with TabPane(id=f"tab-{bracket.type.name.lower()}", title=bracket.type.value):
                    yield BracketTab(id=f"container-{bracket.type.name.lower()}", bracket=bracket)
            with TabPane("All match", id="all-match"):
                yield AllMatchTab(id="container-all-matches", tournament=self.__tournament)

        yield Footer()
