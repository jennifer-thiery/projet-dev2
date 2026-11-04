from domain.player import Player


class Match:
    def __init__(self, id: str, players: list[Player], type: str):

        self.__id = id
        self.__scores = [0, 0]
        self.__players = players
        self.__type = type
        self.__winner = None

    @property
    def id(self) -> str:
        return self.__id

    @property
    def scores(self) -> list:
        return self.__scores

    @property
    def players(self) -> list[Player]:
        return self.__players

    @property
    def type(self) -> str:
        return self.__type

    @property
    def winner(self) -> Player:
        return self.__winner

    def match_overview(self) -> str:
        return (
            f"Poule : {self.__id}\n"
            f"Type : {self.__type}\n"
            f"Scores : {self.__scores}\n"
            f"Joueurs : {[(player.firstname() + ' ' + player.last_name()) for player in self.__players]}\n"
            f"Gagnant : {self.__winner.player_overview() if self.__winner else 'Aucun gagnant'}\n"
        )

    def get_winner(self) -> Player:
        return self.players[0] if self.scores[0] > self.scores[1] else self.players[1]

    def is_played(self) -> bool:
        return False if self.scores is None else True
