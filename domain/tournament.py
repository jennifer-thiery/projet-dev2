from datetime import date

from data.action_db_players import (
    add_player_to_db,
    remove_player_from_db,
    update_player_in_db,
)
from data.action_db_tournament import save_new_brackets
from domain.bracket import Bracket
from domain.enums import BracketType
from domain.player import Player


class Tournament:
    def __init__(self):
        self.__all_players: list[Player] = []
        self.__brackets = [Bracket(bracket_type) for bracket_type in BracketType]

    @property
    def all_players(self) -> list[Player]:
        return self.__all_players

    @property
    def brackets(self) -> list[Bracket]:
        return self.__brackets

    def licence_exists(self, licence_number: str) -> bool:
        return self.player_pointer(licence_number) is not None

    def player_pointer(self, licence_number: str) -> Player | None:
        for player in self.__all_players:
            if player.licence_number == licence_number:
                return player
        return None

    def add_player_to_tournament(self, new_player: Player) -> None:
        add_player_to_db(
            {
                "licence_number": new_player.licence_number,
                "firstname": new_player.firstname,
                "lastname": new_player.lastname,
                "birthdate": new_player.birthdate.strftime("%Y-%m-%d"),
                "club": new_player.club,
                "federation_ranking": new_player.federation_ranking,
                "email": new_player.email,
                "phone_number": new_player.phone_number,
                "second_bracket": new_player.second_bracket,
            }
        )

    def edit_player(
        self,
        p_licence_number: str,
        licence_number: str,
        firstname: str,
        lastname: str,
        birthdate: date,
        club: str,
        federation_ranking: str,
        email: str,
        phone_number: str,
    ) -> None:
        update_player_in_db(
            p_licence_number,
            {
                "licence_number": licence_number,
                "firstname": firstname,
                "lastname": lastname,
                "birthdate": birthdate.strftime("%Y-%m-%d"),
                "club": club,
                "federation_ranking": federation_ranking,
                "email": email,
                "phone_number": phone_number,
            },
        )

    def delete_player_from_tournament(self, licence_number: str) -> None:
        remove_player_from_db(licence_number)

    def add_players_to_brackets(self) -> None:
        """Prépare le nouveau tirage, puis le sauvegarde avant de l'afficher."""
        brackets = [Bracket(bracket_type) for bracket_type in BracketType]
        for player in self.__all_players:
            for bracket_type in player.get_brackets():
                brackets[bracket_type.bracket_index].add_player(player)
        self.check_enough_players(brackets)
        for bracket in brackets:
            if len(bracket.players) > 6:
                bracket.create_pools()
        save_new_brackets(brackets)

    def check_enough_players(self, brackets: list[Bracket]) -> None:
        for bracket in brackets:
            if len(bracket.players) < 6:
                new_index = bracket.type.bracket_index + 1
                if new_index == len(brackets):
                    new_index -= 2
                for player in bracket.players:
                    if brackets[new_index].is_player_in(player.licence_number) == -1:
                        brackets[new_index].add_player(player)
