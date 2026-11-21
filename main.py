from data.action_db_tounament import save_tournament
from domain.tournament import Tournament
from interface.tui_textual import TableTennisTournamentManager


def main():
    tournament = Tournament()
    tournament.add_players_to_brackets()
    tournament.create_pools_of_brackets()
    save_tournament(tournament)

    # TODO : put generating of brackets and pools in a button

    TableTennisTournamentManager(tournament=tournament).run()


if __name__ == "__main__":
    main()
