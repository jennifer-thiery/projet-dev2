from time import sleep

from nicegui import ui

from data.action_db_tounament import load_saved_brackets
from domain.tournament import Tournament
from interface.menu import menu


def main():
    tournament = Tournament()
    saved = load_saved_brackets(tournament.all_players)
    if any(bracket.type not in saved for bracket in tournament.brackets):
        tournament.add_players_to_brackets()
    tournament.brackets[:] = [saved.get(bracket.type, bracket) for bracket in tournament.brackets]
    menu(tournament)


if __name__ == "__main__":
    main()
