from domain.enums import BracketType, FederationRanking, MatchType
from domain.player import Player
from domain.pool import Pool


class Bracket:
    def __init__(self, type: BracketType):
        self.__type = type
        self.__players: list[Player] = []
        self.__pools: list[Pool] = []
        self.__matches = []
        self.__current_state = MatchType.POOL

    @property
    def type(self):
        return self.__type

    @property
    def players(self):
        return self.__players

    @property
    def pools(self) -> list[Pool]:
        return self.__pools

    @property
    def matches(self):
        return self.__matches

    def is_player_in(self, licence_number):
        for i, player in enumerate(self.players):
            if player.licence_number == licence_number:
                return i
        return -1

    def remove_player(self, licence_number) -> None:
        index = self.is_player_in(licence_number)
        if index != -1:
            self.players.remove(index)

    def add_player(self, player: Player) -> None:
        self.__players.append(player)

    def create_pools(self) -> None:
        """Crée la poule en serpentin.

        PRE : aucune.
        POST : Crée le nombre adéquat de poule de 4 et 3 joueurs. Ajoute ensuite les joueurs en fonction de leur niveau en serpentin
        """
        self.__pools = []

        self.__players.sort(key=lambda p: FederationRanking(p.federation_ranking).ranking_weight, reverse=True)
        temp_list = self.__players.copy()

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

            while nbr_in_pool != len(self.__players):
                self.__pools[nbr_in_list].add_player(self.__players[nbr_in_pool])
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
            self.__pools.append(Pool(1))
            while len(temp_list) > 0:
                self.__pools[0].add_player(temp_list.pop(0))

        self.create_matches_of_pools()

    def create_matches_of_pools(self):
        for pool in self.__pools:
            pool.create_matches()
