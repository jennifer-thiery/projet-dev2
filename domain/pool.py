from domain.player import Player


class Pool:
    def __init__(self, id: str, matches: list(), players: list(Player)):
        self.__id = id
        self.__matches = matches
        self.__players = players

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
