from domain.player import Player


class Match:
    def __init__(
        self,
        id: str,
        scores: list(2),
        players: list(Player),
        type: str,
        winner: Player,
    ):

        self.__id = id
        self.__scores = scores
        self.__players = players
        self.__type = type
        self.__winner = winner

    @property
    def id(self) -> str:
        return self.__id

    @property
    def scores(self) -> list(2):
        return self.__scores

    @property
    def players(self) -> list(Player):
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
            f"Joueurs : {[(player.first_name() + ' ' + player.last_name()) for player in self.__players]}\n"
            f"Gagnant : {self.__winner.player_overview() if self.__winner else 'Aucun gagnant'}\n"
        )

    def get_winner(self) -> str:
        return self.players[0] if self.scores[0] > self.scores[1] else self.players[1]

    def is_played(self) -> bool:
        return False if self.scores is None else True
