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

    def add_player(self, player: Player) -> None:
        """Ajoute un joueur à la poule.

        PRE : player est une instance de joueur valide (possédant au moins
              les attributs firstname et lastname).
        POST : ajoute player à la fin de la liste des joueurs de la poule
               (self.__players). Ne renvoie rien.
        """
        self.__players.append(player)

    def create_matches(self) -> None:
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
        id_nbr = 1
        if len(self.__players) == 4:  # 4 joueurs dans la poule
            for i in range(3):
                a = i % 2
                b = 1 + int(i / 2)
                c = -1 - a * 2 - b
                self.__matches.append(
                    Match(
                        f"poule_{self.__id}_match_{id_nbr}", [self.__players[a], self.__players[a + b]], MatchType.POOL
                    )
                )
                id_nbr += 1
                self.__matches.append(
                    Match(
                        f"poule_{self.__id}_match_{id_nbr}",
                        [self.__players[c], self.__players[3]],
                        MatchType.POOL,
                    )
                )
                id_nbr += 1
                # Si vous comprenez pas la logique tkt c'est des maths
        elif len(self.__players) == 3:  # 3 joueurs dans la poule
            for i in range(3):
                self.__matches.append(
                    Match(
                        f"poule_{self.__id}_match_{id_nbr}", [self.__players[-1 + i], self.__players[i]], MatchType.POOL
                    )
                )
                id_nbr += 1

    def ranking(self) -> list[tuple]:
        stats = {}
        for player in self.__players:
            stats[player.licence_number] = {"player": player, "played": 0, "wins": 0, "losses": 0, "points": 0}

        for match in self.__matches:
            winner = match.winner
            if winner is None:
                continue

            loser = match.players[0] if winner == match.players[1] else match.players[1]

            winner_stats = stats[winner.licence_number]
            loser_stats = stats[loser.licence_number]

            winner_stats["played"] += 1
            winner_stats["wins"] += 1

            loser_stats["played"] += 1
            loser_stats["losses"] += 1

            if winner == match.players[0]:
                winner_stats["points"] += match.scores[0]
                loser_stats["points"] += match.scores[1]
            else:
                winner_stats["points"] += match.scores[1]
                loser_stats["points"] += match.scores[0]

        final_ranking = sorted(stats.values(), key=lambda p: p["points"], reverse=True)
        p_list = []

        for p in final_ranking:
            p_list.append((p["player"], p["played"], p["wins"], p["losses"], p["points"]))

        return p_list

    def nbr_matches_left(self) -> int:
        nbr = 0
        for match in self.__matches:
            if match.scores == [0, 0]:
                nbr += 1
        return nbr
