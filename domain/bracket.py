from domain.enums import BracketType, FederationRanking, MatchType
from domain.match import Match
from domain.pool import Pool


def sort_classement(elem) -> int:
    return int(FederationRanking[elem.federation_ranking])


class Braket:
    def __init__(self, type: BracketType):
        self.current_phase = MatchType.POOL
        self.matches = []
        self.players = []
        self.__pools = []
        self.__type = type
        self.current_pool = 0

    @property
    def get_pools(self) -> list:
        return self.__pools

    @property
    def type(self) -> str:
        return self.__type

    def get_next_match(self) -> Match:
        """Renvoie le prochain match à jouer du tableau
        PRE : aucune.
        POST : Si on est en phase de poule : renvoie le prochain match de la poule en cour.
               Si on est en mode tournoi il renvoie le premier match non jouer.
               Si Il n'y a pas de match ou plus de match à jouer il renvoi l'erreur ValueError
        """
        if self.current_phase == MatchType.POOL:
            if self.__pools[self.current_pool].nbr_matches_left() == 0:
                self.current_pool += 1
            return self.__pools[self.current_pool].get_next_match()
        else:
            if len(self.matches) != 0:
                for match in self.matches:
                    if match.scores == [0, 0]:
                        return self.matches[0]
        raise ValueError

    def add_player(self, player) -> None:
        self.players.append(player)

    def remove_player(self, licence_number) -> None:
        for i, player in enumerate(self.players):
            if player.licence_number == licence_number:
                self.players.remove(i)

    def create_pool(self) -> None:
        """Crée la poule en serpentin.

        PRE : aucune.
        POST : Crée le nombre adéquat de poule de 4 et 3 joueurs. Ajoute ensuite les joueurs en fonction de leur niveau en serpentin
        """
        self.__pools = []
        self.rank_player_by_ranking()
        temp_list = self.players.copy()
        nbr_play = len(temp_list)
        if nbr_play >= 6:
            if nbr_play % 4 != 0:
                nbr_of_3 = int(4 - (nbr_play % 4))
            else:
                nbr_of_3 = 0
            nbr_of_4 = int((nbr_play - (nbr_of_3 * 3)) / 4)

            reverse = False
            all_pools = nbr_of_3 + nbr_of_4

            for i in range(1, all_pools + 1):
                self.__pools.append(Pool(i))

            nbr_in_pool = 0
            nbr_in_list = 0

            while nbr_in_pool != len(self.players):
                self.__pools[nbr_in_list].add_player(self.players[nbr_in_pool])
                if not reverse:
                    if not (nbr_in_list == all_pools - 1):
                        nbr_in_list += 1
                    else:
                        reverse = True

                else:
                    if not (nbr_in_list == 0):
                        nbr_in_list -= 1
                    else:
                        reverse = False
                nbr_in_pool += 1

        elif nbr_play != 0:
            list_temp = []
            for j in range(0, nbr_play + 1):
                list_temp.append(temp_list.pop(0))
            self.__pools.append(Pool(1, list_temp))
        for pool in self.__pools:
            pool.create_matches()

    def rank_player_by_ranking(self) -> None:
        self.players.sort(key=sort_classement)


if __name__ == "__main__":
    print("hey")
