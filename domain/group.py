from domain.player import Player


class Group:
    def __init__(self, players: list[Player], ranking_weight: int):
        self.__players = players
        self.__ranking_weight = ranking_weight

    @property
    def ranking_weight(self) -> int:
        return self.__ranking_weight

    @property
    def licence_number(self):
        licence_numbers = []
        for player in self.__players:
            licence_numbers.append(player.licence_number)
        return licence_numbers

    def affichage(self) -> str:
        slip = []
        for player in self.__players:
            slip.append(f"{player.firstname} {player.lastname}")
        return " & ".join(slip)
