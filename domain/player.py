from datetime import date, datetime

from data.action_db_players import add_player_to_db, get_players_from_db, remove_player_from_db
from domain.enums import BracketType, FederationRanking


class Player:
    def __init__(
        self,
        licence_number: str,
        firstname: str,
        lastname: str,
        birthdate: date,
        club: str,
        federation_ranking: str,
        email: str,
        phone_number: str,
    ):
        self.__licence_number = licence_number
        self.__firstname = firstname
        self.__lastname = lastname
        self.__birthdate = birthdate
        self.__club = club
        self.__federation_ranking = federation_ranking
        self.__email = email
        self.__phone_number = phone_number
        self.__two_bracket = False

    @property
    def licence_number(self) -> str:
        return self.__licence_number

    @licence_number.setter
    def licence_number(self, licence_number):
        self.__licence_number = licence_number

    @property
    def firstname(self) -> str:
        return self.__firstname

    @firstname.setter
    def firstname(self, firstname):
        self.__firstname = firstname

    @property
    def lastname(self) -> str:
        return self.__lastname

    @lastname.setter
    def lastname(self, lastname):
        self.__lastname = lastname

    @property
    def birthdate(self) -> date:
        return self.__birthdate

    @birthdate.setter
    def birthdate(self, birthdate):
        self.__birthdate = birthdate

    @property
    def club(self) -> str:
        return self.__club

    @club.setter
    def club(self, club):
        self.__club = club

    @property
    def federation_ranking(self) -> str:
        return self.__federation_ranking

    @federation_ranking.setter
    def federation_ranking(self, federation_ranking):
        self.__federation_ranking = federation_ranking

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        self.__phone_number = phone_number

    def get_age(self):
        current_year = date.today().year
        return current_year - self.__birthdate.year

    def player_overview(self) -> str:
        return (
            f"Joueur : {self.__firstname} {self.__lastname} ({self.__licence_number})\n"
            f"Date de naissance : {self.__birthdate.strftime('%d/%m/%Y')} ({self.get_age()} ans)\n"
            f"Classement : {self.__federation_ranking}\n"
            f"Club : {self.__club}\n"
            f"Coordonées : {self.__email} | {self.__phone_number}\n"
        )

    def get_brackets(self) -> list:
        """Détermine dans quel(s) tableau(x) le joueur est éligible de jouer en fonction de son classement et du nombre de tableaux qu'il souhaite jouer.
        PRE  :  Le joueur a un classement fédéral valide.
                Le joueur a défini s'il voulait jouer dans un deuxième tableau.
        POST :  Renvoie la liste de types de tableaux (1 ou 2 types) dans lesquels le joueur va jouer.
                Le choix des tableaux est selon le classement du joueur et/ou l'âge (RM-01).
        """
        list_temp = []
        match int(FederationRanking[self.federation_ranking]):
            case x if x <= 7:
                list_temp.append(BracketType.BEGINNER)
            case x if x > 7 and x <= 14:
                list_temp.append(BracketType.INTERMADIATE)
            case _:
                list_temp.append(BracketType.EXPERT)
        if self.__two_bracket:
            match list_temp[0]:
                case BracketType.BEGINNER:
                    list_temp.append(BracketType.INTERMADIATE)
                case BracketType.INTERMADIATE:
                    list_temp.append(BracketType.EXPERT)
                case _:
                    pass
        return list_temp


class PlayerManager:
    def __init__(self):
        self.__all_players = []
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
            )
            self.__all_players.append(player)

    @property
    def all_players(self) -> list[Player]:
        return self.__all_players

    def licence_exists(self, licence_number: str) -> bool:
        """Vérifie si la licence est déjà présente dans la liste des participants.
        PRE  :  La licence introduite doit être composé de 8 chiffres.
        POST :  Renvoie True si la licence est déjà présente, sinon False.
        """
        for player in self.__all_players:
            if player.licence_number == licence_number:
                return True
        return False

    def player_pointer(self, licence_number: str) -> Player:
        """Returns the specified player
        PRE : The licence_number of the player we want to fetch
        POST : Returns the player with the specified licence number
        """
        for player in self.all_players:
            if player.licence_number == licence_number:
                return player

    def add_player(self, new_player: Player) -> None:
        """Ajoute un nouveau joueur à la liste des joueurs.
        PRE  :  Le numéro de la licence (licence_number) doit être composé exactement de 8 chiffres.
                Le numéro de la licence (licence_number) ne doit pas déjà être présent dans la liste des participants.
                Le classement fédéral (federation_ranking) doit être une valeur valide (RM-01).
        POST :  Ajoute un nouveau participant dans la liste des joueurs (aussi directement dans la db).
                Ne revoie rien
        """
        self.__all_players.append(new_player)

        new_player_dict = {
            "licence_number": new_player.licence_number,
            "firstname": new_player.firstname,
            "lastname": new_player.lastname,
            "birthdate": new_player.birthdate.strftime("%Y-%m-%d"),
            "club": new_player.club,
            "federation_ranking": new_player.federation_ranking,
            "email": new_player.email,
            "phone_number": new_player.phone_number,
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
        """Modifies the specified player
        PRE : p_licence_number is the licence number of the player as it is in the player object at the moment of call
              licence_number is the potentially new licence number (can be the same as p_licence_number)
              and all the other parameters values can be the same as the value in player.
        POST : Adds the player into the JSON. Returns nothing.
        """
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

    def delete_player(self, licence_number: str) -> None:
        """Deletes a player from the JSON
        PRE : licence_number as its name implies is the licence
        number of the player to be deleted
        POST : The player is deleted from the JSON. Returns nothing
        """
        for player in self.__all_players:
            if player.licence_number == licence_number:
                self.__all_players.remove(player)
                remove_player_from_db(licence_number)
                break
