import sqlite3
from contextlib import closing
from pathlib import Path

FILE_PATH = Path(__file__).with_name("tournament.sqlite3")

SCHEMA = """
CREATE TABLE IF NOT EXISTS players (
    licence_number TEXT PRIMARY KEY,
    position INTEGER NOT NULL UNIQUE,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    birthdate TEXT NOT NULL,
    club TEXT NOT NULL,
    federation_ranking TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    second_bracket INTEGER NOT NULL CHECK (second_bracket IN (0, 1))
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS brackets (
    type TEXT PRIMARY KEY,
    phase TEXT NOT NULL
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS bracket_players (
    bracket_type TEXT NOT NULL REFERENCES brackets(type) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    licence_number TEXT NOT NULL REFERENCES players(licence_number)
        ON UPDATE CASCADE,
    PRIMARY KEY (bracket_type, licence_number),
    UNIQUE (bracket_type, position)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS pools (
    bracket_type TEXT NOT NULL REFERENCES brackets(type) ON DELETE CASCADE,
    number INTEGER NOT NULL,
    PRIMARY KEY (bracket_type, number)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS pool_players (
    bracket_type TEXT NOT NULL,
    pool_number INTEGER NOT NULL,
    position INTEGER NOT NULL,
    licence_number TEXT NOT NULL,
    PRIMARY KEY (bracket_type, pool_number, licence_number),
    UNIQUE (bracket_type, pool_number, position),
    FOREIGN KEY (bracket_type, pool_number) REFERENCES pools(bracket_type, number)
        ON DELETE CASCADE,
    FOREIGN KEY (bracket_type, licence_number) REFERENCES bracket_players(bracket_type, licence_number)
        ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS matches (
    bracket_type TEXT NOT NULL REFERENCES brackets(type) ON DELETE CASCADE,
    label TEXT NOT NULL,
    position INTEGER NOT NULL,
    pool_number INTEGER,
    type TEXT NOT NULL,
    first_licence TEXT NOT NULL,
    second_licence TEXT NOT NULL,
    PRIMARY KEY (bracket_type, label),
    FOREIGN KEY (bracket_type, pool_number) REFERENCES pools(bracket_type, number)
        ON DELETE CASCADE,
    FOREIGN KEY (bracket_type, first_licence) REFERENCES bracket_players(bracket_type, licence_number)
        ON UPDATE CASCADE,
    FOREIGN KEY (bracket_type, second_licence) REFERENCES bracket_players(bracket_type, licence_number)
        ON UPDATE CASCADE,
    CHECK (first_licence != second_licence),
    CHECK ((type = 'POOL') = (pool_number IS NOT NULL))
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS match_sets (
    bracket_type TEXT NOT NULL,
    match_label TEXT NOT NULL,
    position INTEGER NOT NULL,
    first_points INTEGER NOT NULL CHECK (first_points >= 0),
    second_points INTEGER NOT NULL CHECK (second_points >= 0),
    PRIMARY KEY (bracket_type, match_label, position),
    FOREIGN KEY (bracket_type, match_label) REFERENCES matches(bracket_type, label)
        ON DELETE CASCADE
) WITHOUT ROWID;
"""


def connect_db():
    db = sqlite3.connect(FILE_PATH)
    try:
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        version = db.execute("PRAGMA user_version").fetchone()[0]
        if version == 0 and db.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' LIMIT 1").fetchone() is None:
            db.executescript("BEGIN IMMEDIATE;\n" + SCHEMA + "PRAGMA user_version = 5; COMMIT;")
        elif version not in (3, 4, 5):
            raise sqlite3.DatabaseError("Ce fichier de tournoi utilise un schéma incompatible.")
        elif version == 3 and db.execute("SELECT 1 FROM players WHERE active = 0 LIMIT 1").fetchone():
            raise sqlite3.DatabaseError("Cette ancienne base contient des joueurs retirés.")
    except sqlite3.Error:
        db.close()
        raise
    return db


def reset_database():
    with closing(connect_db()) as db, db:
        # SQLite efface les poules, les matchs et les sets liés aux tableaux.
        db.execute("DELETE FROM brackets")
        db.execute("DELETE FROM players")
