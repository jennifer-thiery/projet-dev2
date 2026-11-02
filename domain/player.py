class Player:
    def __init__(
        self,
        licence_number: str,
        firstname: str,
        lastname: str,
        club: str,
        federation_ranking: str,
        email: str,
        phone_number: str,
    ):
        self.__licence_number = licence_number
        self.__firstname = firstname
        self.__lastname = lastname
        self.__club = club
        self.__federation_ranking = federation_ranking
        self.__email = email
        self.__phone_number = phone_number

    @property
    def licence_number(self) -> str:
        return self.__licence_number

    @property
    def firstname(self) -> str:
        return self.__firstname

    @property
    def lastname(self) -> str:
        return self.__lastname

    @property
    def club(self) -> str:
        return self.__club

    @property
    def federation_ranking(self) -> str:
        return self.__federation_ranking

    @property
    def email(self) -> str:
        return self.__email

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    def player_overview(self) -> str:
        return (
            f"Joueur : {self.__firstname} {self.__lastname} ({self.__licence_number})\n"
            f"Classement : {self.__federation_ranking}\n"
            f"Club : {self.__club}\n"
            f"Coordonées : {self.__email} | {self.__phone_number}\n"
        )


class PlayerManager:
    def __init__(self):
        self.__all_players = []
        for data in get_players_from_db():
            player = Player(
                licence_number=data["licence_number"],
                firstname=data["firstname"],
                lastname=data["lastname"],
                club=data["club"],
                federation_ranking=data["federation_ranking"],
                email=data["email"],
                phone_number=data["phone_number"],
            )
            self.__all_players.append(player)

    def add_player(self, new_player: Player) -> None:
        new_player_dict = {
            "licence_number": new_player.licence_number,
            "firstname": new_player.firstname,
            "lastname": new_player.lastname,
            "club": new_player.club,
            "federation_ranking": new_player.federation_ranking,
            "email": new_player.email,
            "phone_number": new_player.phone_number,
        }

        self.__all_players.append(new_player)
    def edit_player(self, licence_number: str) -> None:
        return ""

    def delete_player(self, licence_number: str) -> None:
        return ""
