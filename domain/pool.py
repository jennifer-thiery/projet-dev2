from domain.enums import MatchType
from domain.match import Match


class Pool:
    def __init__(self, id: str):
        self.__id = id
        self.__matches = []
        self.__players = []

        self.create_matches()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def matches(self) -> list:
        return self.__matches

    @property
    def players(self) -> list:
        return self.__players

    def add_player(self, player):
        self.__players.append(player)

    """affiche les matchs restants dans une poule"""

    def left_matches(self) -> str:

        string = ""

        for match in self.__matches:
            if match.scores == [0, 0]:
                string += f"  - {match.players[0].firstname} {match.players[0].lastname} vs {match.players[1].firstname} {match.players[1].lastname} \n"
        return string

    def create_matches(self):
        player_done = 0
        id_nbr = 1
        while player_done != len(self.__players):
            for i in range(player_done, len(self.__players) - 1):
                list_temp = [self.__players[player_done], self.__players[i + 1]]
                self.__matches.append(Match(f"poule_{self.__id}_match_{id_nbr}", list_temp, MatchType.POOL))
                id_nbr += 1

            player_done += 1
