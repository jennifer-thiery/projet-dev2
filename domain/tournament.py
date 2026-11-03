from datetime import date

from domain.bracket import Braket
from domain.enums import BracketType
from domain.pool import Pool


class Tournament:
    def __init__(self, start_date: date, end_date: date):
        self.__start_date = start_date
        self.__end_date = end_date
        self.brackets = [
            Braket(BracketType.JUNIOR),
            Braket(BracketType.BEGINNER),
            Braket(BracketType.INTERMADIATE),
            Braket(BracketType.EXPERT),
        ]

    def get_state(self) -> bool:
        return self.__end_date < date.today

    def add_player(self, player, bracket) -> None:
        match bracket:
            case BracketType.JUNIOR:
                self.brackets[0].add_player(player)
            case BracketType.BEGINNER:
                self.brackets[1].add_player(player)
            case BracketType.INTERMADIATE:
                self.brackets[2].add_player(player)
            case BracketType.EXPERT:
                self.brackets[3].add_player(player)

    def remove_player(self, licence_number, bracket) -> None:
        match bracket:
            case BracketType.JUNIOR:
                self.brackets[0].add_player(licence_number)
            case BracketType.BEGINNER:
                self.brackets[1].add_player(licence_number)
            case BracketType.INTERMADIATE:
                self.brackets[2].add_player(licence_number)
            case BracketType.EXPERT:
                self.brackets[3].add_player(licence_number)

    def get_all_pools(self) -> list(Pool):
        all_pool = []
        for bracket in self.brackets:
            bracket.create_pool()
            all_pool += bracket.get_pools()
        return all_pool
