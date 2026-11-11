from domain.enums import BracketType
from domain.enums import FederationRanking as FR
from domain.player import Player
from domain.pool import Pool


class Bracket:
    def __init__(self, type: BracketType):
        self.__type = type
        self.__players: list[Player] = []
        self.__pools: list[Pool] = []

    @property
    def type(self):
        return self.__type

    @property
    def players(self):
        return self.__players

    @property
    def pools(self) -> list[Pool]:
        return self.__pools

    def accepts_player(self, player: Player) -> bool:
        p_ranking_weight = FR(player.federation_ranking).ranking_weight

        is_junior = player.get_age() <= 15
        is_beginner = FR.NC.ranking_weight <= p_ranking_weight <= FR.E0.ranking_weight
        is_intermediate = FR.D6.ranking_weight <= p_ranking_weight <= FR.D0.ranking_weight
        is_expert = FR.C6.ranking_weight <= p_ranking_weight

        match self.type:
            case BracketType.JUNIOR:
                return is_junior
            case BracketType.BEGINNER:
                return is_beginner or (is_junior and player.second_bracket and is_beginner)
            case BracketType.INTERMEDIATE:
                return (
                    is_intermediate
                    or (player.second_bracket and is_beginner)
                    or (is_junior and player.second_bracket and is_intermediate)
                )
            case BracketType.EXPERT:
                return (
                    is_expert
                    or (player.second_bracket and is_intermediate)
                    or (is_junior and player.second_bracket and is_expert)
                )
            case _:
                return False

    def add_player(self, player: Player) -> None:
        if self.accepts_player(player):
            self.__players.append(player)

    def create_pools(self) -> None:
        self.__pools = []

        self.__players.sort(key=lambda p: FR(p.federation_ranking).ranking_weight, reverse=True)
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
            list_temp = []
            for _ in range(0, nbr_play + 1):
                list_temp.append(temp_list.pop(0))
            self.__pools.append(Pool(1, list_temp))

        self.create_matches_of_pools()

    def create_matches_of_pools(self):
        for pool in self.__pools:
            pool.create_matches()
