from nicegui import ui

from domain.tournament import Tournament
from interface.menu import menu


def main():
    tournament = Tournament()
    tournament.add_players_to_brackets()
    menu(tournament)


if __name__ == "__mp_main__":
    main()
