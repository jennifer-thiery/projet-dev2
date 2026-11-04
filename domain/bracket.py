from domain.enums import BracketType, FederationRanking, MatchType
from domain.match import Match
from domain.pool import Pool


def sort_classement(elem) -> int:
    nbr = elem.federation_ranking
    if nbr == "NC":
        nbr = 0
    else:
        match nbr[0]:
            case "E":
                nbr = 10 + 6 - int(nbr[1])
            case "D":
                nbr = 20 + 6 - int(nbr[1])
            case "C":
                nbr = 30 + 6 - int(nbr[1])
            case "B":
                nbr = 40 + 6 - int(nbr[1])

    return nbr


class Braket:
    def __init__(self, type: BracketType):
        self.current_phase = MatchType.POOL
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

    def get_next_match(self) -> Match:
        if self.current_phase == MatchType.POOL:
            return self.__pools[0].get_next_match()
        else:
            return self.matches[0]

    def add_player(self, player) -> None:
        self.players.append(player)

    def remove_player(self, licence_number) -> None:
        for i, player in enumerate(self.players):
            if player.licence_number == licence_number:
                self.players.remove(i)

    def create_pool(self) -> None:
        self.__pools = []
        nbr_play = len(self.players)
        if nbr_play >= 6:
            if nbr_play % 4 != 0:
                nbr_of_3 = int(4 - (nbr_play % 4))
            else:
                nbr_of_3 = 0
            nbr_of_4 = int((nbr_play - (nbr_of_3 * 3)) / 4)
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
        elif nbr_play != 0:
            list_temp = []
            for j in range(0, nbr_play + 1):
                list_temp.append(self.players.pop(0))
            self.__pools.append(Pool(1, list_temp))

    def rank_player_by_ranking(self) -> None:
        self.players.sort(key=sort_classement)
