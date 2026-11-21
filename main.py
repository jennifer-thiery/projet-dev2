from domain.tournament import Tournament
from interface.tui_textual import TableTennisTournamentManager


def main():
    tournament = Tournament()
    tournament.add_players_to_brackets()

    TableTennisTournamentManager(tournament=tournament).run()


if __name__ == "__main__":
    main()
