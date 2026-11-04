import json
from datetime import date, datetime
from pathlib import Path

from domain.tournament import Tournament

FILE_NAME = "tournament.json"
FILE_PATH = Path(__file__).resolve().parent / FILE_NAME


def to_json_default(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")


def save_tournament(T):
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(T, file, indent=4, ensure_ascii=False, default=to_json_default)
    except FileNotFoundError:
        print(f"Le fichier {FILE_NAME} existe pas")


def load_tournament():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            jason = json.load(file)
            return jason
    except FileNotFoundError:
        print(f"Le fichier {FILE_NAME} existe pas")
