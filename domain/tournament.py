from datetime import date

from domain.bracket import Braket
from domain.enums import BracketType
from domain.enums import FederationRanking as F_R
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

    def create_brackets(self) -> None:
        for player in PlayerManager().all_players():
            match player.federation_ranking:
                case (
                    F_R.NC.value
                    | F_R.E0.value
                    | F_R.E1.value
                    | F_R.E2.value
                    | F_R.E3.value
                    | F_R.E4.value
                    | F_R.E5.value
                    | F_R.E6.value
                ):
                    self.add_player(player, BracketType.BEGINNER)
                case (
                    F_R.D0.value
                    | F_R.D1.value
                    | F_R.D2.value
                    | F_R.D3.value
                    | F_R.D4.value
                    | F_R.D5.value
                    | F_R.D6.value
                ):
                    self.add_player(player, BracketType.INTERMADIATE)
                case _:
                    self.add_player(player, BracketType.EXPERT)
