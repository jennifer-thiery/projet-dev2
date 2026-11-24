import json
from pathlib import Path

from data.action_db_players import import_players_to_db
from data.action_db_tounament import load_saved_brackets
from domain.tournament import Tournament
from interface.menu import menu

PROJECT_ROOT = Path(__file__).resolve().parent


def seed_players_from_json() -> None:
    matches = list(PROJECT_ROOT.rglob("all_players.json"))
    if not matches:
        raise FileNotFoundError(f"all_players.json not found under {PROJECT_ROOT}")
    with matches[0].open(encoding="utf-8") as file:
        import_players_to_db(json.load(file))


def main():
    seed_players_from_json()
    tournament = Tournament()
    print(f"Loaded {len(tournament.all_players)} players from database.")

    saved = load_saved_brackets(tournament.all_players)
    if any(bracket.type not in saved for bracket in tournament.brackets):
        tournament.add_players_to_brackets()
    tournament.brackets[:] = [saved.get(bracket.type, bracket) for bracket in tournament.brackets]
    menu(tournament)


if __name__ in {"__main__", "__mp_main__"}:
    main()
