from math import log2

from domain.enums import BracketType, FederationRanking, MatchType
from domain.match import Match
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

    @property
    def current_state(self):
        return self.__current_state

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

    def create_matches_from_qualified(self):
        from data.action_db_write import save_bracket_matches

        qualified_players = self.get_all_qualified()
        nbr_matches = len(qualified_players) / 2
        previous_state = self.__current_state
        previous_match_count = len(self.__matches)
        self.change_state()

        all_matches = []
        i = 1
        while len(qualified_players) > 0:
            if self.__current_state == MatchType.get_type_from_index(index=-1):
                self.__matches.append(
                    Match(
                        f"{self.__current_state.name.lower()}-match-1",
                        [qualified_players.pop(0), qualified_players.pop(0)],
                        self.__current_state,
                    )
                )
                break
            else:
                all_matches.insert(
                    0,
                    Match(
                        f"{self.__current_state.name.lower()}-match-{i}",
                        [qualified_players.pop(0), qualified_players.pop(2)],
                        self.__current_state,
                    ),
                )
                all_matches.insert(
                    -1,
                    Match(
                        f"{self.__current_state.name.lower()}-match-{nbr_matches - i + 1}",
                        [qualified_players.pop(0), qualified_players.pop(0)],
                        self.__current_state,
                    ),
                )
                i += 2
        self.__matches += all_matches
        if len(self.__matches) > previous_match_count:
            try:
                save_bracket_matches(None, self)
            except Exception:
                del self.__matches[previous_match_count:]
                self.__current_state = previous_state
                raise

    def get_all_qualified(self):
        if self.__current_state == MatchType.POOL:
            qualified_players = []
            for pool in self.__pools:
                taby = pool.ranking()
                qualified_players += [taby[0][0], taby[1][0]]
            return qualified_players[0 : 2 ** int(log2(len(self.__pools) * 2))]

        else:
            qualified_players = []
            for match in self.get_all_matches_from_type(self.__current_state):
                qualified_players.append(match.winner)

        return qualified_players

    def get_all_matches_from_type(self, match_type):
        all_matches_from_type = []
        for match in self.__matches:
            if match.type == match_type:
                all_matches_from_type.append(match)
        return all_matches_from_type

    def change_state(self):
        if self.__current_state == MatchType.POOL:
            all_done = True
            for pool in self.__pools:
                for match in self.__matches:
                    if not match.is_played():
                        all_done = False
                        break
                if not all_done:
                    break
            if all_done and len(self.__pools) * 2 <= 32:
                self.__current_state = MatchType.get_type_from_index(index=-int(log2(len(self.__pools) * 2)))
        else:
            self.__current_state = MatchType.get_type_from_index(index=self.__current_state.index - 1)
