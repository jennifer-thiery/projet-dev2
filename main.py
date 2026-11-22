from domain.tournament import Tournament
from interface.menu import menu


def main():
    tournament = Tournament()
    tournament.add_players_to_brackets()
    menu()


if __name__ == "__main__":
    main()
