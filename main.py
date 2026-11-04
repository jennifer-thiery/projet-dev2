from data.action_db_tounament import save_tournament
from domain.tournament import Tournament
from interface.tui_mvp import show_menu


def main():
    tournament = Tournament("2019-12-04", "2019-12-06")
    tournament.create_brackets()

    print(tournament.get_all_pools())
    save_tournament(tournament)
    # show_menu()


if __name__ == "__main__":
    main()
