import json
from datetime import date, datetime
from pathlib import Path

FILE_NAME = "tournament.json"
FILE_PATH = Path(__file__).resolve().parent / FILE_NAME


def to_json_default(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    if hasattr(o, "__dict__"):
        return o.__dict__
    raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")


def save_tournament(t):
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(t, file, indent=4, ensure_ascii=False, default=to_json_default)
    except FileNotFoundError:
        print(f"Le fichier {FILE_NAME} existe pas")
