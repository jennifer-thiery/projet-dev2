from datetime import date

from domain.bracket import Braket
from domain.enums import BracketType
from domain.player import PlayerManager
from domain.pool import Pool


class Tournament:
    def __init__(self, start_date: date, end_date: date):
        self.__start_date = start_date
        self.__end_date = end_date
        self.__players = PlayerManager()
        self.__brackets = [
            Braket(BracketType.JUNIOR),
            Braket(BracketType.BEGINNER),
            Braket(BracketType.INTERMADIATE),
            Braket(BracketType.EXPERT),
        ]

    @property
    def players(self):
        return self.__players

    def get_state(self) -> bool:
        return self.__end_date > date.today()

    def add_player(self, player, bracket) -> None:
        match bracket:
            case BracketType.JUNIOR:
                self.__brackets[0].add_player(player)
            case BracketType.BEGINNER:
                self.__brackets[1].add_player(player)
            case BracketType.INTERMADIATE:
                self.__brackets[2].add_player(player)
            case BracketType.EXPERT:
                self.__brackets[3].add_player(player)

    def remove_player(self, licence_number, bracket) -> None:
        match bracket:
            case BracketType.JUNIOR:
                self.__brackets[0].remove_player(licence_number)
            case BracketType.BEGINNER:
                self.__brackets[1].remove_player(licence_number)
            case BracketType.INTERMADIATE:
                self.__brackets[2].remove_player(licence_number)
            case BracketType.EXPERT:
                self.__brackets[3].remove_player(licence_number)

    def create_all_pools(self) -> None:
        for bracket in self.__brackets:
            bracket.create_pool()

    def create_brackets(self) -> None:
        for player in self.__players.all_players:
            for bracket in player.get_brackets():
                self.add_player(player, bracket)
        self.create_all_pools()


if __name__ == "__main__":
    Tournament(date.fromisoformat("2019-12-04"), date.fromisoformat("2019-12-06"))
