from datetime import date, datetime

from data.action_db_players import (
    add_player_to_db,
    get_players_from_db,
    remove_player_from_db,
    update_player_in_db,
)
from domain.bracket import Bracket
from domain.enums import BracketType
from domain.player import Player


class Tournament:
    def __init__(self):
        self.__all_players: list[Player] = []
        for data in get_players_from_db():
            player = Player(
                licence_number=data["licence_number"],
                firstname=data["firstname"],
                lastname=data["lastname"],
                birthdate=datetime.strptime(data["birthdate"], "%Y-%m-%d"),
                club=data["club"],
                federation_ranking=data["federation_ranking"],
                email=data["email"],
                phone_number=data["phone_number"],
                second_bracket=data["second_bracket"],
            )
            self.__all_players.append(player)

        self.__brackets = [
            Bracket(BracketType.JUNIOR),
            Bracket(BracketType.BEGINNER),
            Bracket(BracketType.INTERMEDIATE),
            Bracket(BracketType.EXPERT),
        ]

    # PlayerManager
    @property
    def all_players(self) -> list[Player]:
        return self.__all_players

    def licence_exists(self, licence_number: str) -> bool:
        for player in self.__all_players:
            if player.licence_number == licence_number:
                return True
        return False

    def player_pointer(self, licence_number: str) -> Player:
        for player in self.all_players:
            if player.licence_number == licence_number:
                return player

    def add_player_to_tournament(self, new_player: Player) -> None:
        # Add player to db
        new_player_dict = {
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
        add_player_to_db(new_player_dict)
        self.__all_players.append(new_player)

    def edit_player(
        self,
        p_licence_number: str,  # the current licence number
        licence_number: str,  # The potentially changed licence number
        firstname: str,
        lastname: str,
        birthdate: date,
        club: str,
        federation_ranking: str,
        email: str,
        phone_number: str,
    ) -> None:
        for player in self.__all_players:
            if player.licence_number == p_licence_number:
                changes = {
                    "licence_number": licence_number,
                    "firstname": firstname,
                    "lastname": lastname,
                    "birthdate": birthdate,
                    "club": club,
                    "federation_ranking": federation_ranking,
                    "email": email,
                    "phone_number": phone_number,
                }
                update_player_in_db(
                    p_licence_number,
                    {**changes, "birthdate": birthdate.strftime("%Y-%m-%d")},
                )
                for field, value in changes.items():
                    setattr(player, field, value)
                break

    def delete_player_from_tournament(self, licence_number: str) -> None:
        for player in self.__all_players:
            if player.licence_number == licence_number:
                remove_player_from_db(licence_number)
                self.__all_players.remove(player)
                break

    # Bracket/Pool Manager
    @property
    def brackets(self):
        return self.__brackets

    def add_player_to_bracket(self, player, bracket) -> None:
        match bracket:
            case BracketType.JUNIOR:
                self.__brackets[0].add_player(player)
            case BracketType.BEGINNER:
                self.__brackets[1].add_player(player)
            case BracketType.INTERMEDIATE:
                self.__brackets[2].add_player(player)
            case BracketType.EXPERT:
                self.__brackets[3].add_player(player)

    def create_pools_of_brackets(self) -> None:
        for bracket in self.__brackets:
            bracket.create_pools()

    def generate_brackets(self) -> None:
        """Ajoute chaque joueur dans les tableaux où il est inscrit et les poules de chaque tableau sont créée.

        PRE : aucune.
        POST : les participants on été ajouter à leur bracket. Ensuite chaque tableau crée ses poules.
        """
        for player in self.__all_players:
            for bracket in player.get_brackets():
                self.add_player_to_bracket(player, bracket)
        for bracket in self.__brackets:
            bracket.create_pools()
