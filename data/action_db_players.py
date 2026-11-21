from data.database import connect_db

INSERT_PLAYER = """
    INSERT INTO players (licence_number, firstname, lastname, birthdate, club,
                         federation_ranking, email, phone_number, second_bracket)
    VALUES (:licence_number, :firstname, :lastname, :birthdate, :club,
            :federation_ranking, :email, :phone_number, :second_bracket)
"""


def get_players_from_db():
    players = []
    db = connect_db()
    try:
        for row in db.execute("SELECT * FROM players ORDER BY rowid"):
            players.append(dict(row, second_bracket=bool(row["second_bracket"])))
    finally:
        db.close()
    return players


def add_player_to_db(new_player):
    db = connect_db()
    try:
        db.execute(INSERT_PLAYER, new_player)
        db.commit()
    finally:
        db.close()


def remove_player_from_db(player_to_remove: str):
    db = connect_db()
    try:
        db.execute("DELETE FROM players WHERE licence_number = ?", (player_to_remove,))
        db.commit()
    finally:
        db.close()


def update_player_in_db(old_licence, player):
    db = connect_db()
    try:
        db.execute(
            """UPDATE players SET licence_number = :licence_number, firstname = :firstname,
               lastname = :lastname, birthdate = :birthdate, club = :club,
               federation_ranking = :federation_ranking, email = :email, phone_number = :phone_number
               WHERE licence_number = :old_licence""",
            {**player, "old_licence": old_licence},
        )
        db.commit()
    finally:
        db.close()


def import_players_to_db(players):
    sql = INSERT_PLAYER + "ON CONFLICT(licence_number) DO NOTHING"
    db = connect_db()
    try:
        count = db.executemany(sql, players).rowcount
        db.commit()
        return count
    finally:
        db.close()
