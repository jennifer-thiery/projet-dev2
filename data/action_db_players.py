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


def remove_player_from_db(player_to_remove):
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        player_list = json.load(file)

    for i, player in enumerate(player_list):
        if player["licence_number"] == player_to_remove:
            player_list.pop(i)
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(player_list, file, indent=4, ensure_ascii=False)
