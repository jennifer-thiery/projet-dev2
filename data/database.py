import sqlite3
from pathlib import Path

FILE_PATH = Path(__file__).resolve().with_name("tournament.sqlite3")


def connect_db():
    db = sqlite3.connect(FILE_PATH)
    try:
        db.row_factory = sqlite3.Row
        db.execute("""
            CREATE TABLE IF NOT EXISTS players (
                licence_number TEXT PRIMARY KEY NOT NULL,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                birthdate TEXT NOT NULL,
                club TEXT NOT NULL,
                federation_ranking TEXT NOT NULL,
                email TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                second_bracket INTEGER NOT NULL CHECK (second_bracket IN (0, 1))
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS tournament (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                snapshot TEXT NOT NULL
            )
        """)
    except BaseException:
        db.close()
        raise
    return db


def reset_database():
    db = connect_db()
    try:
        db.execute("DELETE FROM tournament")
        db.execute("DELETE FROM players")
        db.commit()
    finally:
        db.close()
