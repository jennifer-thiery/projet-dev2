from domain.enums import MatchType
from domain.match import Match
from domain.player import Player


class Pool:
    def __init__(self, id: str):
        self.__id = id
        self.__players: list[Player] = []
        self.__matches: list[Match] = []

    @property
    def id(self) -> str:
        return self.__id

    @property
    def players(self) -> list[Player]:
        return self.__players

    @property
    def matches(self) -> list[Match]:
        return self.__matches

    def add_player(self, player: Player):
        self.__players.append(player)

    def create_matches(self):
        player_done = 0
        id_nbr = 1
        while player_done != len(self.__players):
            for i in range(player_done, len(self.__players) - 1):
                list_temp = [self.__players[player_done], self.__players[i + 1]]
                self.__matches.append(Match(f"poule_{self.__id}_match_{id_nbr}", list_temp, MatchType.POOL))
                id_nbr += 1

            player_done += 1

    def left_matches(self) -> str:
        """affiche les matchs restants dans une poule"""
        string = ""

        for match in self.__matches:
            if match.scores == [0, 0]:
                string += f"  - {match.players[0].firstname} {match.players[0].lastname} vs {match.players[1].firstname} {match.players[1].lastname} \n"
        return string
