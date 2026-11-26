from math import ceil, log2

from domain.enums import BracketType, MatchType
from domain.group import Group
from domain.match import Match
from domain.player import Player
from domain.pool import Pool


class Bracket:
    def __init__(self, type: BracketType, phase: MatchType = MatchType.POOL):
        self.__type = type
        self.__players: list[Player] | list[Group] = []
        self.__pools: list[Pool] = []
        self.__matches = []
        self.__current_state = phase
        self.__double = type == BracketType.DOUBLE

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
        if self.__double:
            for i, players in enumerate(self.players):
                for player in players:
                    if player.licence_number == licence_number:
                        return i
            return -1
        for i, player in enumerate(self.players):
            if player.licence_number == licence_number:
                return i
        return -1

    def remove_player(self, licence_number) -> None:
        index = self.is_player_in(licence_number)
        if index != -1:
            self.players.remove(index)

    def add_player(self, player: Group | Player) -> None:
        self.__players.append(player)

    def clear(self) -> None:
        self.__players.clear()
        self.__pools.clear()
        self.__matches.clear()
        self.__current_state = MatchType.POOL
        self.__double.clear()

    def create_pools(self) -> None:
        """Crée la poule en serpentin.

        PRE : aucune.
        POST : Crée le nombre adéquat de poule de 4 et 3 joueurs. Ajoute ensuite les joueurs en fonction de leur niveau en serpentin
        """
        self.__pools = []

        self.__players.sort(key=lambda p: p.ranking_weight, reverse=True)
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

    def create_matches_of_pools(self) -> None:
        for pool in self.__pools:
            pool.create_matches()

    def create_matches_from_qualified(self) -> bool:
        from data.action_db_tournament import save_final_phase

        phase = self.next_phase()
        if phase == self.__current_state:
            return False
        players = self.get_all_qualified()
        if not players or len(players) % 2 or None in players:
            return False

        matches = []
        for i in range(0, len(players), 2):
            matches.append(Match(f"{phase.name.lower()}-match-{i // 2 + 1}", players[i : i + 2], phase))
        save_final_phase(self, phase, matches)
        return True

    def get_all_qualified(self, preview_pool_qualified: bool = False) -> list[Player | Group | None]:
        if self.__current_state == MatchType.POOL:
            qualified, _ = self.pool_qualifiers(preview_pool_qualified)
            return qualified

        matches = self.get_all_matches_from_type(self.__current_state)
        winners = [match.winner for match in matches]
        if self.__current_state == self.first_final_round():
            _, waiting = self.pool_qualifiers()
            middle = len(winners) // 2
            return winners[:middle] + waiting + winners[middle:]
        return winners

    def get_preview_qualified(self, phase: MatchType) -> list[Player | Group | None]:
        if self.__current_state == MatchType.POOL:
            first_round = self.first_final_round()
            if phase == first_round:
                return self.get_all_qualified(preview_pool_qualified=True)
            if first_round is not None and phase.index == first_round.index + 1:
                qualified, waiting = self.pool_qualifiers(preview=True)
                winner_count = len(qualified) // 2
                middle = winner_count // 2
                return [None] * middle + waiting + [None] * (winner_count - middle)
        elif phase.index == self.__current_state.index + 1:
            return self.get_all_qualified()

        return [None] * 2 ** (MatchType.FINAL.index - phase.index + 1)

    def pool_qualifiers(self, preview: bool = False) -> tuple[list[Player | Group | None], list[Player | Group | None]]:
        pool_results = []
        for pool in self.__pools:
            if pool.nbr_matches_left() == 0:
                ranking = pool.ranking()
                pool_results.append((ranking[0][0], ranking[1][0], ranking[0][4]))
            elif preview:
                pool_results.append((None, None, -1))
            else:
                return [], []

        if not pool_results:
            return [], []

        player_count = len(pool_results) * 2
        full_round_size = 2 ** int(log2(player_count))
        # Chaque match préliminaire retire un joueur du tour suivant.
        waiting_count = 2 * full_round_size - player_count if player_count != full_round_size else 0
        both_can_wait = waiting_count > len(pool_results)
        split_pools = player_count - waiting_count if both_can_wait else waiting_count
        pool_results.sort(key=lambda result: result[2], reverse=both_can_wait)

        qualified = []
        waiting = []
        for index, (first, second, _) in enumerate(pool_results):
            if index < split_pools:
                first_list, second_list = waiting, qualified
            elif both_can_wait:
                first_list = second_list = waiting
            else:
                first_list = second_list = qualified
            if index % 2 == 0:
                first_list.insert(0, first)
                second_list.append(second)
            else:
                first_list.append(first)
                second_list.insert(0, second)
        return qualified, waiting

    def get_all_matches_from_type(self, match_type) -> list[Match]:
        all_matches_from_type = []
        for match in self.__matches:
            if match.type == match_type:
                all_matches_from_type.append(match)
        return all_matches_from_type

    def first_final_round(self) -> MatchType | None:
        qualifiers = len(self.__pools) * 2
        if 0 < qualifiers <= 32:
            return MatchType.get_type_from_index(index=-ceil(log2(qualifiers)))
        return None

    def next_phase(self) -> MatchType:
        if self.__current_state == MatchType.POOL:
            first_round = self.first_final_round()
            if first_round is not None and all(pool.nbr_matches_left() == 0 for pool in self.__pools):
                return first_round
        elif self.__current_state != MatchType.FINAL:
            matches = self.get_all_matches_from_type(self.__current_state)
            if matches and all(match.is_played() for match in matches):
                return MatchType.get_type_from_index(index=self.__current_state.index + 1)
        return self.__current_state
