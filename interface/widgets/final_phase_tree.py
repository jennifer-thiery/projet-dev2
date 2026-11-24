from math import ceil, log2

from textual.app import ComposeResult
from textual.containers import Horizontal, HorizontalScroll, Vertical
from textual.widgets import Label, Static

from domain.enums import MatchType
from domain.player import Player


class MatchCard(Static):
    def __init__(
        self, player_1: Player | None, sets_1: int | None, player_2: Player | None, sets_2: int | None
    ) -> None:
        super().__init__()
        self.__player_1 = player_1
        self.__sets_1 = sets_1
        self.__player_2 = player_2
        self.__sets_2 = sets_2

    def compose(self) -> ComposeResult:
        with Horizontal(classes="player-row"):
            player_1 = (
                f"{self.__player_1.firstname} {self.__player_1.lastname}"
                if self.__player_1 is not None
                else "À déterminer"
            )
            sets_1 = self.__sets_1 if self.__sets_1 is not None else 0
            yield Label(player_1, classes="name")
            yield Label(str(sets_1), classes="score")

        with Horizontal(classes="player-row"):
            player_2 = (
                f"{self.__player_2.firstname} {self.__player_2.lastname}"
                if self.__player_2 is not None
                else "À déterminer"
            )
            sets_2 = self.__sets_2 if self.__sets_2 is not None else 0
            yield Label(player_2, classes="name")
            yield Label(str(sets_2), classes="score")


class FinalPhaseTree(HorizontalScroll):
    def __init__(self, bracket):
        super().__init__()
        self.__bracket = bracket
        self.__preview_pool_qualified = any(pool.nbr_matches_left() != 0 for pool in self.__bracket.pools)

        if self.__preview_pool_qualified:
            self.__first_round = MatchType.get_type_from_index(index=-ceil(log2(len(self.__bracket.pools))))
            self.__pool_preview_players = self.__bracket.get_all_qualified(preview_pool_qualified=True)

        else:
            self.__first_round = MatchType.FINAL
            for i in range(MatchType.ROUND_OF_32.index, MatchType.FINAL.index + 1):
                match_type = MatchType.get_type_from_index(i)
                if self.__bracket.get_all_matches_from_type(match_type):
                    self.__first_round = match_type
                    break

    def compose(self) -> ComposeResult:
        if self.__preview_pool_qualified:
            nbr_matches_type = len(self.__pool_preview_players) // 2
        else:
            nbr_matches_type = len(self.__bracket.get_all_matches_from_type(self.__first_round))

        for i in range(self.__first_round.index, MatchType.FINAL.index + 1):
            match_type = MatchType.get_type_from_index(i)

            with Vertical():
                yield Static(match_type)

                # for match in matchs:
                #     yield MatchCard(match.players[0], match.scores[0], match.players[1], match.scores[1])

                # # Add temperary (empty) matches for next phases
                # temp_matches = nbr_matches_type - len(matchs)
                # for i in range(temp_matches):
                #     yield MatchCard(None, None, None, None)

                if self.__preview_pool_qualified and i == self.__first_round.index:
                    for j in range(0, len(self.__pool_preview_players), 2):
                        p1 = self.__pool_preview_players[j]
                        p2 = self.__pool_preview_players[j + 1]
                        yield MatchCard(p1, None, p2, None)

            nbr_matches_type = nbr_matches_type // 2
