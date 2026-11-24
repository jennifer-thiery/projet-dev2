from sqlite3 import Error

from data.action_db_tournament import load_tournament
from interface.tui_textual import TableTennisTournamentManager


def main():
    try:
        tournament = load_tournament()
    except Error as error:
        raise SystemExit(
            f"Impossible d'ouvrir la base du tournoi ({error})."
        ) from error

    TableTennisTournamentManager(tournament=tournament).run()


if __name__ == "__main__":
    main()
