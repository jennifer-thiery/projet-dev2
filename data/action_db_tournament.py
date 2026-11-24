from contextlib import closing

from data.action_db_players import player_from_row
from data.database import connect_db
from domain.bracket import Bracket
from domain.enums import BracketType, MatchType
from domain.match import Match
from domain.pool import Pool


# Reconstruit le tournoi à partir des données enregistrées dans SQLite.
def load_tournament():
    from domain.tournament import Tournament

    tournament = Tournament()
    with closing(connect_db()) as db, db:
        db.execute("BEGIN")
        players = {}
        for row in db.execute("SELECT * FROM players ORDER BY position"):
            player = player_from_row(row)
            players[player.licence_number] = player
            tournament.all_players.append(player)

        for row in db.execute("SELECT * FROM brackets"):
            bracket_type = BracketType[row["type"]]
            bracket = Bracket(bracket_type, MatchType[row["phase"]])
            tournament.brackets[bracket_type.bracket_index] = bracket

            members = db.execute(
                "SELECT licence_number FROM bracket_players WHERE bracket_type = ? ORDER BY position",
                (bracket_type.name,),
            )
            for member in members:
                bracket.add_player(players[member["licence_number"]])

            pools = {}
            for pool_row in db.execute(
                "SELECT number FROM pools WHERE bracket_type = ? ORDER BY number",
                (bracket_type.name,),
            ):
                pool = Pool(pool_row["number"])
                pools[pool.id] = pool
                bracket.pools.append(pool)
                members = db.execute(
                    """SELECT licence_number FROM pool_players
                       WHERE bracket_type = ? AND pool_number = ? ORDER BY position""",
                    (bracket_type.name, pool.id),
                )
                for member in members:
                    pool.add_player(players[member["licence_number"]])

            for match_row in db.execute(
                "SELECT * FROM matches WHERE bracket_type = ? ORDER BY pool_number, position",
                (bracket_type.name,),
            ):
                match = read_match(db, match_row, players)
                pool_number = match_row["pool_number"]
                if pool_number is None:
                    bracket.matches.append(match)
                else:
                    pools[pool_number].matches.append(match)
    return tournament


# Reconstruit un match et recalcule son score à partir des sets enregistrés.
def read_match(db, row, players):
    match = Match(
        row["label"],
        [
            players[row["first_licence"]],
            players[row["second_licence"]],
        ],
        MatchType[row["type"]],
    )
    sets = [
        (points["first_points"], points["second_points"])
        for points in db.execute(
            """SELECT first_points, second_points FROM match_sets
               WHERE bracket_type = ? AND match_label = ? ORDER BY position""",
            (row["bracket_type"], row["label"]),
        )
    ]
    if sets:
        match.record_result(sets)
    return match


# Remplace le tirage précédent et ses résultats par les nouveaux tableaux.
def save_new_brackets(brackets):
    with closing(connect_db()) as db, db:
        # Les poules et les résultats de l'ancien tirage sont supprimés ensemble.
        db.execute("DELETE FROM brackets")
        licences = {player.licence_number for bracket in brackets for player in bracket.players}
        saved_licences = {row["licence_number"] for row in db.execute("SELECT licence_number FROM players")}
        if licences != saved_licences:
            raise ValueError("La liste des joueurs a changé. Rouvrez le tournoi.")

        for bracket in brackets:
            bracket_type = bracket.type.name
            db.execute(
                "INSERT INTO brackets (type, phase) VALUES (?, ?)",
                (bracket_type, bracket.current_state.name),
            )
            db.executemany(
                "INSERT INTO bracket_players (bracket_type, position, licence_number) VALUES (?, ?, ?)",
                [(bracket_type, position, player.licence_number) for position, player in enumerate(bracket.players)],
            )
            for pool in bracket.pools:
                db.execute(
                    "INSERT INTO pools (bracket_type, number) VALUES (?, ?)",
                    (bracket_type, pool.id),
                )
                db.executemany(
                    """INSERT INTO pool_players (bracket_type, pool_number, position, licence_number)
                       VALUES (?, ?, ?, ?)""",
                    [
                        (bracket_type, pool.id, position, player.licence_number)
                        for position, player in enumerate(pool.players)
                    ],
                )
                for position, match in enumerate(pool.matches):
                    insert_match(db, bracket_type, match, position, pool.id)


# Enregistre un match de poule ou de phase finale avec les licences de ses joueurs.
def insert_match(db, bracket_type, match, position, pool_number=None):
    first, second = match.players
    db.execute(
        """INSERT INTO matches (bracket_type, label, position, pool_number, type,
                                first_licence, second_licence)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            bracket_type,
            match.id,
            position,
            pool_number,
            match.type.name,
            first.licence_number,
            second.licence_number,
        ),
    )


# Enregistre ensemble la nouvelle phase du tableau et ses nouveaux matchs.
def save_final_phase(bracket, phase, new_matches):
    bracket_type = bracket.type.name
    with closing(connect_db()) as db, db:
        row = db.execute(
            "UPDATE brackets SET phase = ? WHERE type = ? AND phase = ?",
            (phase.name, bracket_type, bracket.current_state.name),
        )
        if row.rowcount == 0:
            raise ValueError("Ce tableau a changé. Rouvrez le tournoi.")

        licences = [
            row["licence_number"]
            for row in db.execute(
                "SELECT licence_number FROM bracket_players WHERE bracket_type = ? ORDER BY position",
                (bracket_type,),
            )
        ]
        if licences != [player.licence_number for player in bracket.players]:
            raise ValueError("Les joueurs du tableau ont changé. Rouvrez le tournoi.")
        for position, match in enumerate(new_matches, start=len(bracket.matches)):
            insert_match(db, bracket_type, match, position)


# Enregistre les sets d'un match qui n'a pas encore de résultat.
def save_match_result(bracket_type, match):
    if not match.sets:
        raise ValueError("Validez les sets avant de sauvegarder le résultat.")
    with closing(connect_db()) as db, db:
        db.execute("BEGIN IMMEDIATE")
        first, second = match.players
        row = db.execute(
            """SELECT 1 FROM matches
               WHERE bracket_type = ? AND label = ? AND type = ?
                 AND first_licence = ? AND second_licence = ?""",
            (
                bracket_type.name,
                match.id,
                match.type.name,
                first.licence_number,
                second.licence_number,
            ),
        ).fetchone()
        if row is None:
            raise ValueError(
                f"Ce match n'a pas été retrouvé. Rouvrez le tournoi.{
                    (
                        bracket_type.name,
                        match.id,
                        match.type.name,
                        first.licence_number,
                        second.licence_number,
                    )
                }"
            )
        if db.execute(
            "SELECT 1 FROM match_sets WHERE bracket_type = ? AND match_label = ?",
            (bracket_type.name, match.id),
        ).fetchone():
            raise ValueError("Ce match a déjà un résultat enregistré.")
        db.executemany(
            """INSERT INTO match_sets (bracket_type, match_label, position, first_points, second_points)
               VALUES (?, ?, ?, ?, ?)""",
            [
                (bracket_type.name, match.id, position, first, second)
                for position, (first, second) in enumerate(match.sets)
            ],
        )
