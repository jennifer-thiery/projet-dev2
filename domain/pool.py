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
        """Ajoute un joueur à la poule.

        PRE : player est une instance de joueur valide (possédant au moins
              les attributs firstname et lastname).
        POST : ajoute player à la fin de la liste des joueurs de la poule
               (self.__players). Ne renvoie rien.
        """
        self.__players.append(player)

    def create_matches(self):
        """Génère les matchs de la poule pour toutes les paires de joueurs.

        Chaque joueur de la poule affronte une unique fois chacun des
        autres joueurs inscrits (tournoi toutes rondes).

        PRE : aucune.
        POST : crée et ajoute à self.__matches une instance de Match de
               type MatchType.POOL pour chaque paire unique de joueurs de
               self.__players, avec un identifiant séquentiel de la forme
               "poule_<id>_match_<n>" (où n commence à 1). Si moins de
               2 joueurs sont inscrits, aucun match n'est ajouté.
               Ne renvoie rien.
        """
        player_done = 0
        id_nbr = 1
        while player_done != len(self.__players):
            for i in range(player_done, len(self.__players) - 1):
                list_temp = [self.__players[player_done], self.__players[i + 1]]
                self.__matches.append(Match(f"poule_{self.__id}_match_{id_nbr}", list_temp, MatchType.POOL))
                id_nbr += 1

            player_done += 1
