from domain.bracket import Bracket
from domain.enums import BracketType
from domain.player import PlayerManager


class Tournament:
    def __init__(self):
        self.__brackets = [
            Bracket(BracketType.JUNIOR),
            Bracket(BracketType.BEGINNER),
            Bracket(BracketType.INTERMEDIATE),
            Bracket(BracketType.EXPERT),
        ]

    @property
    def brackets(self):
        return self.__brackets

    def add_players_to_brackets(self) -> None:
        for player in PlayerManager().all_players:
            for bracket in self.__brackets:
                bracket.add_player(player)

    def create_pools_of_brackets(self) -> None:
        for bracket in self.__brackets:
            bracket.create_pools()
