import json
from pathlib import Path

FILE_NAME = "all_pool.json"
FILE_PATH = Path(__file__).resolve().parent / FILE_NAME


def get_pools_from_db():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Le fichier {FILE_NAME} existe pas")
        data = []

    return data


def get_pool_from_db(pool_id):
    for pool in get_pools_from_db():
        if str(pool["id"]) == str(pool_id):
            return pool

    return None
