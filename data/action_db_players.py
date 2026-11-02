import json
from pathlib import Path

FILE_NAME = "all_players.json"
FILE_PATH = Path(__file__).resolve().parent / FILE_NAME
# print("path:", FILE_PATH)


def get_players_from_db():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Le fichier {FILE_NAME} existe pas")
        data = []

    return data


def add_player_to_db(new_player):
    data = get_players_from_db()
    data.append(new_player)

    try:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        print(f"Le fichier {FILE_NAME} existe pas")
