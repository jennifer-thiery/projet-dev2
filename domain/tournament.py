from datetime import date, datetime
from time import sleep

from data.action_db_players import add_player_to_db, get_players_from_db, remove_player_from_db
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
        self.__all_players.append(new_player)

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
        # Loop in all_players to find the player with the wanted licence_number and modify each of the informations
        for player in self.__all_players:  # player references the dict Player inside of all_players
            if player.licence_number == p_licence_number:
                remove_player_from_db(p_licence_number)
                player.licence_number = licence_number
                player.firstname = firstname
                player.lastname = lastname
                player.birthdate = birthdate
                player.club = club
                player.federation_ranking = federation_ranking
                player.email = email
                player.phone_number = phone_number
                self.add_player(player)
                break

    def delete_player_from_tournament(self, licence_number: str) -> None:
        for player in self.__all_players:
            if player.licence_number == licence_number:
                self.__all_players.remove(player)
                remove_player_from_db(licence_number)
                break

    # Bracket/Pool Manager
    @property
    def brackets(self):
        return self.__brackets

    def create_pools_of_brackets(self) -> None:
        self.check_enough_players()
        for bracket in self.__brackets:
            if len(bracket.players) > 6:
                bracket.create_pools()
                print

    def check_enough_players(self):
        for bracket in self.__brackets:
            if len(bracket.players) <= 6:
                new_index = bracket.type.bracket_index + 1
                if new_index == len(self.__brackets):
                    new_index -= 2
                for player in bracket.players:
                    if self.__brackets[new_index].is_player_in(player.licence_number) >= 0:
                        self.__brackets[new_index].add_player()

    def generate_brackets(self) -> None:
        """Ajoute chaque joueur dans les tableaux où il est inscrit et les poules de chaque tableau sont créée.

        PRE : aucune.
        POST : les participants on été ajouter à leur bracket. Ensuite chaque tableau crée ses poules.
        """
        for player in self.__all_players:
            for bracket in player.get_brackets():
                self.__brackets[bracket.bracket_index].add_player(player)
        self.create_pools_of_brackets()
