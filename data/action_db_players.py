from contextlib import closing
from datetime import date

from data.database import connect_db
from domain.player import Player

INSERT_PLAYER = """
    INSERT INTO players (licence_number, position, firstname, lastname, birthdate, club,
                         federation_ranking, email, phone_number, second_bracket)
    VALUES (:licence_number, (SELECT COALESCE(MAX(position), 0) + 1 FROM players),
            :firstname, :lastname, :birthdate, :club,
            :federation_ranking, :email, :phone_number, :second_bracket)
    ON CONFLICT(licence_number) DO NOTHING
"""


def player_from_row(row) -> Player:
    return Player(
        licence_number=row["licence_number"],
        firstname=row["firstname"],
        lastname=row["lastname"],
        birthdate=date.fromisoformat(row["birthdate"]),
        club=row["club"],
        federation_ranking=row["federation_ranking"],
        email=row["email"],
        phone_number=row["phone_number"],
        second_bracket=bool(row["second_bracket"]),
    )


def add_player_to_db(new_player) -> None:
    with closing(connect_db()) as db, db:
        if db.execute(INSERT_PLAYER, new_player).rowcount == 0:
            raise ValueError("Ce participant est déjà inscrit.")


def remove_player_from_db(licence_number: str) -> None:
    with closing(connect_db()) as db, db:
        row = db.execute(
            """DELETE FROM players WHERE licence_number = ?
               AND NOT EXISTS (
                   SELECT 1 FROM bracket_players WHERE licence_number = players.licence_number
               )""",
            (licence_number,),
        )
        if row.rowcount == 0:
            raise ValueError("Ce participant est introuvable ou déjà affecté à un tableau.")


def update_player_in_db(old_licence: str, player) -> None:
    with closing(connect_db()) as db, db:
        row = db.execute(
            """UPDATE players SET licence_number = :licence_number, firstname = :firstname,
               lastname = :lastname, birthdate = :birthdate, club = :club,
               federation_ranking = :federation_ranking, email = :email, phone_number = :phone_number
               WHERE licence_number = :old_licence""",
            {**player, "old_licence": old_licence},
        )
        if row.rowcount == 0:
            raise ValueError("Ce participant est introuvable.")


def import_players_to_db(players) -> list[Player]:
    added = []
    sql = INSERT_PLAYER + "RETURNING *"
    with closing(connect_db()) as db, db:
        for player in players:
            row = db.execute(sql, player).fetchone()
            if row is not None:
                added.append(player_from_row(row))
    return added
