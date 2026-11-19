from domain.player import Player


class Match:
    def __init__(self, id: str, players: list[Player], type: str):

        self.__id = id
        self.__scores = [0, 0]
        self.__sets: tuple[tuple[int, int], ...] = ()
        self.__players = players
        self.__type = type
        self.__winner = None

    @property
    def id(self) -> str:
        return self.__id

    @property
    def scores(self) -> list[int]:
        return self.__scores.copy()

    @property
    def sets(self) -> tuple[tuple[int, int], ...]:
        return self.__sets

    @property
    def players(self) -> list[Player]:
        return self.__players

    @property
    def type(self) -> str:
        return self.__type

    @property
    def winner(self) -> Player | None:
        return self.__winner

    # La liste contient un tuple (points du joueur 1, points du joueur 2) par set.
    def record_result(self, sets: list[tuple[int, int]]) -> None:
        if self.is_played():
            raise ValueError("Ce match a déjà un résultat.")

        if not 3 <= len(sets) <= 5:
            raise ValueError("Un match terminé doit comporter de 3 à 5 sets.")

        # wins[0] compte les sets gagnés par le premier joueur et wins[1] ceux du second.
        wins = [0, 0]
        validated_sets = []
        for points in sets:
            # Dès qu'un joueur a gagné trois sets, tout set supplémentaire est invalide.
            if 3 in wins:
                raise ValueError("Le match s'arrête dès qu'un joueur gagne trois sets.")
            # Vérifie les deux scores avant de les comparer.
            if len(points) != 2 or any(type(score) is not int or score < 0 for score in points):
                raise ValueError("Un set doit avoir deux scores entiers positifs ou nuls.")

            first, second = points
            lower, higher = sorted(points)
            # Le set se termine à 11 points ou avec deux points d'avance à partir de 10-10.
            if higher != max(11, lower + 2):
                raise ValueError("Ce score ne correspond pas à un set terminé.")

            # Ajoute la victoire au bon joueur et conserve les points dans l'ordre de saisie.
            wins[0 if first > second else 1] += 1
            validated_sets.append((first, second))

        # Des sets valides peuvent former un match incomplet, par exemple à deux sets partout.
        if 3 not in wins:
            raise ValueError("Un joueur doit avoir gagné trois sets.")

        self.__winner = self.players[wins.index(3)]
        self.__scores = wins
        self.__sets = tuple(validated_sets)

    def match_overview(self) -> str:
        return (
            f"Poule : {self.__id}\n"
            f"Type : {self.__type}\n"
            f"Scores : {self.__scores}\n"
            f"Joueurs : {[(player.firstname() + ' ' + player.last_name()) for player in self.__players]}\n"
            f"Gagnant : {self.__winner.player_overview() if self.__winner else 'Aucun gagnant'}\n"
        )

    def get_winner(self) -> Player | None:
        return self.winner

    def is_played(self) -> bool:
        return self.winner is not None
