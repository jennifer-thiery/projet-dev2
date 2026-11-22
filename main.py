from data.action_db_tounament import load_saved_brackets
from domain.tournament import Tournament
from interface.tui_textual import TableTennisTournamentManager


def main():
    tournament = Tournament()
    saved = load_saved_brackets(tournament.all_players)
    if any(bracket.type not in saved for bracket in tournament.brackets):
        tournament.add_players_to_brackets()
    tournament.brackets[:] = [
        saved.get(bracket.type, bracket) for bracket in tournament.brackets
    ]

    TableTennisTournamentManager(tournament=tournament).run()


if __name__ == "__main__":
    main()
