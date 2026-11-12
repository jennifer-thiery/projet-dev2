from datetime import date


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
        second_bracket: bool,
    ):
        self.__licence_number = licence_number
        self.__firstname = firstname
        self.__lastname = lastname
        self.__birthdate = birthdate
        self.__club = club
        self.__federation_ranking = federation_ranking
        self.__email = email
        self.__phone_number = phone_number
        self.__second_bracket = second_bracket

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

    @property
    def second_bracket(self) -> str:
        return self.__second_bracket

    @second_bracket.setter
    def second_bracket(self, second_bracket):
        self.__second_bracket = second_bracket

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
