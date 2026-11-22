import json
import sqlite3
from pathlib import Path

FILE_PATH = Path(__file__).resolve().with_name("tournament.sqlite3")


def connect_db():
    db = sqlite3.connect(FILE_PATH)
    try:
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        if db.execute("PRAGMA user_version").fetchone()[0] == 0:
            initialize_database(db)
    except BaseException:
        db.close()
        raise
    return db


def initialize_database(db):
    with db:
        db.executescript("""
            BEGIN IMMEDIATE;
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
            );
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY CHECK (id = 1)
            );
            CREATE TABLE IF NOT EXISTS tournament_players (
                id INTEGER PRIMARY KEY,
                tournament_id INTEGER NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
                roster_position INTEGER,
                licence_number TEXT NOT NULL,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                birthdate TEXT NOT NULL,
                club TEXT NOT NULL,
                federation_ranking TEXT NOT NULL,
                email TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                second_bracket INTEGER NOT NULL CHECK (second_bracket IN (0, 1)),
                UNIQUE (tournament_id, roster_position)
            );
            CREATE TABLE IF NOT EXISTS brackets (
                id INTEGER PRIMARY KEY,
                tournament_id INTEGER NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
                type TEXT NOT NULL,
                current_state TEXT,
                legacy_current_pool INTEGER
            );
            CREATE TABLE IF NOT EXISTS bracket_players (
                bracket_id INTEGER NOT NULL REFERENCES brackets(id) ON DELETE CASCADE,
                position INTEGER NOT NULL,
                player_id INTEGER NOT NULL REFERENCES tournament_players(id) ON DELETE CASCADE,
                PRIMARY KEY (bracket_id, position)
            );
            CREATE TABLE IF NOT EXISTS pools (
                id INTEGER PRIMARY KEY,
                bracket_id INTEGER NOT NULL REFERENCES brackets(id) ON DELETE CASCADE,
                label NOT NULL,
                UNIQUE (bracket_id, id)
            );
            CREATE TABLE IF NOT EXISTS pool_players (
                pool_id INTEGER NOT NULL REFERENCES pools(id) ON DELETE CASCADE,
                position INTEGER NOT NULL,
                player_id INTEGER NOT NULL REFERENCES tournament_players(id) ON DELETE CASCADE,
                PRIMARY KEY (pool_id, position)
            );
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY,
                bracket_id INTEGER NOT NULL REFERENCES brackets(id) ON DELETE CASCADE,
                pool_id INTEGER,
                label TEXT NOT NULL,
                type TEXT NOT NULL,
                first_player_id INTEGER REFERENCES tournament_players(id),
                second_player_id INTEGER REFERENCES tournament_players(id),
                first_score INTEGER NOT NULL,
                second_score INTEGER NOT NULL,
                has_legacy_winner INTEGER NOT NULL CHECK (has_legacy_winner IN (0, 1)),
                legacy_winner_id INTEGER REFERENCES tournament_players(id),
                FOREIGN KEY (bracket_id, pool_id) REFERENCES pools(bracket_id, id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS matches_by_bracket_and_pool ON matches (bracket_id, pool_id);
            CREATE TABLE IF NOT EXISTS match_sets (
                match_id INTEGER NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
                position INTEGER NOT NULL,
                first_points INTEGER NOT NULL,
                second_points INTEGER NOT NULL,
                PRIMARY KEY (match_id, position)
            );
        """)
        legacy_table = db.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'tournament'"
        ).fetchone()
        if legacy_table is not None:
            from data.action_db_tounament import write_tournament

            row = db.execute("SELECT snapshot FROM tournament WHERE id = 1").fetchone()
            if row is not None:
                write_tournament(db, json.loads(row["snapshot"]))
            db.execute("DROP TABLE tournament")
        db.execute("PRAGMA user_version = 1")


def reset_database():
    db = connect_db()
    try:
        db.execute("DELETE FROM tournaments")
        db.execute("DELETE FROM players")
        db.commit()
    finally:
        db.close()
