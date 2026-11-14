from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static

from domain.bracket import Bracket


class BracketTab(Container):
    def __init__(self, id, bracket: Bracket) -> None:
        super().__init__(id=id)
        self.__bracket = bracket

    def compose(self) -> ComposeResult:
        yield Static(self.__bracket.type.value)
