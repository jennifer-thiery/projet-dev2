from domain.enums import MatchType
from domain.match import Match


class Pool:
    def __init__(self, id: str):
        self.__id = id
        self.__matches = []
        self.__players = []

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
        """Ajoute un joueur à la poule.

        PRE : player est une instance de joueur valide (possédant au moins
              les attributs firstname et lastname).
        POST : ajoute player à la fin de la liste des joueurs de la poule
               (self.__players). Ne renvoie rien.
        """
        self.__players.append(player)

    def nbr_matches_left(self) -> int:
        return sum(not match.is_played() for match in self.__matches)

    def left_matches(self) -> str:
        """Formate la liste des matchs restants à jouer dans la poule.

        Un match reste à jouer tant qu'aucun résultat n'a été enregistré.

        PRE : aucune.
        POST : renvoie une chaîne de caractères listant les matchs restants
               (un par ligne, au format
               "  - <prénom1> <nom1> vs <prénom2> <nom2> \n"), ou une
               chaîne vide s'il n'y a aucun match restant. Ne modifie rien.
        """

        string = ""

        for match in self.__matches:
            if not match.is_played():
                string += f"  - {match.players[0].firstname} {match.players[0].lastname} vs {match.players[1].firstname} {match.players[1].lastname} \n"
        return string

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
