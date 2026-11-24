from itertools import zip_longest

from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.widgets import Label, Static

from domain.bracket import Bracket
from domain.enums import BracketType, MatchType
from domain.match import Match
from domain.player import Player
from interface.widgets.score_modal import ScoreModal


class MatchCard(Static):
    def __init__(
        self,
        player_1: Player | None,
        sets_1: int | None,
        player_2: Player | None,
        sets_2: int | None,
        match: Match | None = None,
        bracket_type: BracketType | None = None,
    ) -> None:
        super().__init__()
        self.__player_1 = player_1
        self.__sets_1 = sets_1
        self.__player_2 = player_2
        self.__sets_2 = sets_2
        self.__match = match
        self.__bracket_type = bracket_type

    def compose(self) -> ComposeResult:
        with Horizontal(classes="player-row"):
            player_1 = (
                f"{self.__player_1.firstname} {self.__player_1.lastname}"
                if self.__player_1 is not None
                else "À déterminer"
            )
            sets_1 = self.__sets_1 if self.__sets_1 is not None else 0
            yield Label(player_1, classes="name tbd" if self.__player_1 is None else "name")
            yield Label(str(sets_1), classes="score")

        with Horizontal(classes="player-row"):
            player_2 = (
                f"{self.__player_2.firstname} {self.__player_2.lastname}"
                if self.__player_2 is not None
                else "À déterminer"
            )
            sets_2 = self.__sets_2 if self.__sets_2 is not None else 0
            yield Label(player_2, classes="name tbd" if self.__player_2 is None else "name")
            yield Label(str(sets_2), classes="score")

    def on_click(self):
        if self.__match is not None:
            self.app.push_screen(ScoreModal(self.__match, self.__bracket_type), self.app.reload_tournament)


class FinalPhaseTree(ScrollableContainer):
    def __init__(self, bracket: Bracket):
        super().__init__()
        self.__bracket = bracket
        self.__first_round = (
            bracket.matches[0].type if bracket.matches else bracket.first_final_round()
        ) or MatchType.FINAL

    def compose(self) -> ComposeResult:
        for i in range(self.__first_round.index, MatchType.FINAL.index + 1):
            match_type = MatchType.get_type_from_index(i)

            with Vertical():
                yield Static(match_type.value)
                matches = self.__bracket.get_all_matches_from_type(match_type)
                if matches:
                    for match in matches:
                        first, second = match.players
                        first_score, second_score = match.scores
                        yield MatchCard(first, first_score, second, second_score, match, self.__bracket.type)
                else:
                    players = self.__bracket.get_preview_qualified(match_type)
                    for first, second in zip_longest(players[::2], players[1::2]):
                        yield MatchCard(first, None, second, None)
