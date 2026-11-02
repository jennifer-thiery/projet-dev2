from domain.enums import BracketType, MatchType
from domain.pool import Pool


class Braket:
    def __init__(self, type):
        self.current_phase = MatchType[0]
        self.matches = []
        self.players = []
        self.__pools = []
        self.__type = type

    @property
    def get_pools(self) -> list:
        return self.__pools

    @property
    def type(self) -> str:
        return self.__type

    def get_next_match(self):  # manque -> match
        if self.current_phase == MatchType[0]:
            return self.__pools[0].get_next_match()
        else:
            return self.matches[0]

    def add_player_to_bracket(self, player) -> None:
        self.players.append(player)

    def remove_player_from_bracket(self, licence_number) -> None:
        for i, player in enumerate(self.players):
            if player.licence_number == licence_number:
                self.players.remove(i)

    def create_pool(self) -> None:

        nbr_play = len(self.players)
        if nbr_play >= 6:
            if nbr_play % 4 != 0:
                nbr_of_3 = 4 - (nbr_play % 4)
            else:
                nbr_of_3 = 0
            nbr_of_4 = (nbr_play - (nbr_of_3 * 3)) / 4
            self.rank_player_by_ranking()

            for i in range(1, nbr_of_3 + nbr_of_4 + 1):
                if nbr_of_3 != 0:
                    list_temp = []
                    for j in range(0, 3):
                        list_temp.append(self.players.pop(0))
                    nbr_of_3 -= 1
                    self.__pools.append(Pool(i, list_temp))
                else:
                    list_temp = []
                    for j in range(0, 4):
                        list_temp.append(self.players.pop(0))
                    nbr_of_4 -= 1
                    self.__pools.append(Pool(i, list_temp))
        else:
            if self.type == BracketType[0]:
                pass  # add BracketType[1]
            elif self.type == BracketType[len(BracketType) - 1]:
                pass  # add BracketType[len(BracketType)-2]
            else:
                pass  # add to BracketType[me+1]
            print(
                "aled je dois add mes players au voisin mais j'ai peur de faire une bétise du coup je mets ça pour le moment"
            )

    def rank_player_by_ranking(self) -> None:
        pass  # Pas encore intégrer (raison = flemme)
