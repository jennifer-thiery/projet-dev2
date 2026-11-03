from domain.enums import MatchType
from domain.match import Match
from domain.player import Player


class Pool:
    def __init__(self, id: str, players: list(Player)):
        self.__id = id
        self.__matches = []
        self.__players = players

        self.create_matches()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def matches(self) -> list:
        return self.__matches

    @property
    def players(self) -> list(Player):
        return self.__players

    """affiche les matchs restants dans une poule"""

    def print_left_matches(self) -> str:

        string = ""

        for match in self.__matches:
            if match.score is None:
                string += f"  - {match.player[0].firstname} {match.player[0].lastname} vs {match.player[1].firstname} {match.player[1].lastname} \n"
        return string

    def create_matches(self):
        player_done = 0
        id_nbr = 1
        while player_done != len(Player):
            for i in range(player_done, len(Player)):
                list_temp = [self.players[player_done], self.players[i + 1]]
                Match(f"poule_{self.id}_match_{id_nbr}", list_temp, MatchType.POOL)
                id_nbr += 1
            player_done += 1
