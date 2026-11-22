import json
from contextlib import closing, contextmanager
from datetime import datetime

from data.action_db_players import player_from_row
from data.action_db_tounament import (
    PLAYER_FIELDS,
    _bracket_players,
    _pool_players,
    _saved_type,
    _sets,
    _write_bracket,
    _write_matches,
    _write_player,
    to_json_default,
)
from data.database import connect_db
from domain.bracket import Bracket
from domain.enums import BracketType, FederationRanking, MatchType
from domain.match import Match
from domain.pool import Pool


@contextmanager
def _write_db():
    with closing(connect_db()) as db, db:
        db.execute("BEGIN IMMEDIATE")
        yield db


def _ensure_tournament(db):
    db.execute("INSERT INTO tournaments (id) VALUES (1) ON CONFLICT(id) DO NOTHING")


def add_tournament_player(player: dict[str, str | bool]) -> int:
    """Ajoute un profil à la liste sauvegardée du tournoi."""
    datetime.fromisoformat(player["birthdate"])
    FederationRanking(player["federation_ranking"])
    with _write_db() as db:
        _ensure_tournament(db)
        row = db.execute(
            """INSERT INTO tournament_players (
                   tournament_id, roster_position, licence_number, firstname, lastname,
                   birthdate, club, federation_ranking, email, phone_number, second_bracket
               ) VALUES (
                   1, (SELECT COALESCE(MAX(roster_position), -1) + 1
                       FROM tournament_players WHERE tournament_id = 1),
                   :licence_number, :firstname, :lastname, :birthdate, :club,
                   :federation_ranking, :email, :phone_number, :second_bracket
               )""",
            player,
        )
        return row.lastrowid


def update_tournament_player(player_id: int, player: dict[str, str | bool]) -> bool:
    """Modifie un profil sauvegardé en conservant ses liens."""
    datetime.fromisoformat(player["birthdate"])
    FederationRanking(player["federation_ranking"])
    with _write_db() as db:
        row = db.execute(
            """UPDATE tournament_players
               SET licence_number = :licence_number, firstname = :firstname, lastname = :lastname,
                   birthdate = :birthdate, club = :club, federation_ranking = :federation_ranking,
                   email = :email, phone_number = :phone_number, second_bracket = :second_bracket
               WHERE id = :player_id""",
            {**player, "player_id": player_id},
        )
        return row.rowcount == 1


def add_bracket(
    bracket_type: BracketType, current_state: MatchType = MatchType.POOL
) -> int:
    """Ajoute un tableau au tournoi sauvegardé."""
    with _write_db() as db:
        _ensure_tournament(db)
        row = db.execute(
            """INSERT INTO brackets (tournament_id, type, current_state) VALUES (1, ?, ?)""",
            (BracketType(bracket_type), MatchType(current_state)),
        )
        return row.lastrowid


def update_bracket(
    bracket_id: int, bracket_type: BracketType, current_state: MatchType
) -> bool:
    """Modifie la catégorie et la phase d'un tableau."""
    with _write_db() as db:
        row = db.execute(
            "UPDATE brackets SET type = ?, current_state = ? WHERE id = ?",
            (BracketType(bracket_type), MatchType(current_state), bracket_id),
        )
        return row.rowcount == 1


def add_pool(bracket_id: int, label: int | str) -> int:
    """Ajoute une poule à un tableau sauvegardé."""
    with _write_db() as db:
        row = db.execute(
            "INSERT INTO pools (bracket_id, label) VALUES (?, ?)", (bracket_id, label)
        )
        return row.lastrowid


def update_pool(pool_id: int, label: int | str) -> bool:
    """Modifie le numéro ou le libellé d'une poule."""
    with _write_db() as db:
        row = db.execute("UPDATE pools SET label = ? WHERE id = ?", (label, pool_id))
        return row.rowcount == 1


def _add_member(db, table, column, parent_id, player_id):
    # La table et la colonne sont choisies par les fonctions ci-dessous.
    row = db.execute(
        f"""INSERT INTO {table} ({column}, position, player_id)
            SELECT ?, (SELECT COALESCE(MAX(position), -1) + 1 FROM {table} WHERE {column} = ?), ?
            WHERE NOT EXISTS (SELECT 1 FROM {table} WHERE {column} = ? AND player_id = ?)""",
        (parent_id, parent_id, player_id, parent_id, player_id),
    )
    return row.rowcount == 1


def add_player_to_bracket(bracket_id: int, player_id: int) -> bool:
    """Inscrit un profil sauvegardé dans un tableau."""
    with _write_db() as db:
        return _add_member(db, "bracket_players", "bracket_id", bracket_id, player_id)


def add_player_to_pool(pool_id: int, player_id: int) -> bool:
    """Inscrit un profil sauvegardé dans une poule et son tableau."""
    with _write_db() as db:
        pool = db.execute(
            "SELECT bracket_id FROM pools WHERE id = ?", (pool_id,)
        ).fetchone()
        if pool is None:
            raise ValueError("Poule introuvable.")
        _add_member(db, "bracket_players", "bracket_id", pool["bracket_id"], player_id)
        return _add_member(db, "pool_players", "pool_id", pool_id, player_id)


def add_match(
    bracket_id: int,
    label: str,
    match_type: MatchType,
    player_ids: tuple[int, int],
    *,
    pool_id: int | None = None,
) -> int:
    """Ajoute un match sans résultat entre deux joueurs déjà inscrits."""
    match_type = MatchType(match_type)
    if (pool_id is not None) != (match_type == MatchType.POOL):
        raise ValueError("Un match de type Poule doit être associé à une poule.")
    first_player_id, second_player_id = player_ids
    with _write_db() as db:
        members = (
            _bracket_players(db, bracket_id)
            if pool_id is None
            else _pool_players(db, pool_id)
        )
        member_ids = {row["player_id"] for row in members}
        if first_player_id == second_player_id or not member_ids.issuperset(player_ids):
            raise ValueError(
                "Le match doit opposer deux joueurs inscrits dans la poule ou le tableau."
            )
        row = db.execute(
            """INSERT INTO matches (
                   bracket_id, pool_id, label, type, first_player_id, second_player_id,
                   first_score, second_score, has_legacy_winner
               ) VALUES (?, ?, ?, ?, ?, ?, 0, 0, 0)""",
            (bracket_id, pool_id, label, match_type, first_player_id, second_player_id),
        )
        if pool_id is None:
            db.execute(
                "UPDATE brackets SET current_state = ? WHERE id = ? AND current_state IS NULL",
                (MatchType.POOL, bracket_id),
            )
        return row.lastrowid


def rename_match(match_id: int, label: str) -> bool:
    """Modifie le libellé d'un match."""
    with _write_db() as db:
        row = db.execute("UPDATE matches SET label = ? WHERE id = ?", (label, match_id))
        return row.rowcount == 1


def save_bracket_matches(bracket_id: int | None, bracket: Bracket) -> bool:
    """Sauvegarde les matchs hors poule. Avec None, recherche ou crée le tableau par catégorie."""
    with _write_db() as db:
        if bracket_id is None:
            bracket_id = _bracket_id_by_type(db, bracket.type)
            if bracket_id is None:
                _save_new_bracket(db, bracket)
                return True
        else:
            row = db.execute(
                "SELECT type FROM brackets WHERE id = ?", (bracket_id,)
            ).fetchone()
            if row is None:
                return False
            if _saved_type(BracketType, row["type"]) != bracket.type:
                raise ValueError(
                    "Le tableau fourni ne correspond pas au tableau sauvegardé."
                )

        players = db.execute(
            """SELECT player.licence_number, MIN(player.id) AS id
               FROM bracket_players AS member
               JOIN tournament_players AS player ON player.id = member.player_id
               WHERE member.bracket_id = ?
               GROUP BY player.licence_number
               HAVING COUNT(DISTINCT player.id) = 1""",
            (bracket_id,),
        )
        player_ids = {row["licence_number"]: row["id"] for row in players}

        def player_id(player):
            if player is None:
                return None
            licence = player.licence_number
            if licence not in player_ids:
                raise ValueError(
                    f"La licence {licence} doit identifier un joueur du tableau sauvegardé."
                )
            return player_ids[licence]

        db.execute(
            "DELETE FROM matches WHERE bracket_id = ? AND pool_id IS NULL",
            (bracket_id,),
        )
        _write_matches(db, map(vars, bracket.matches), bracket_id, player_id)
        db.execute(
            "UPDATE brackets SET current_state = ? WHERE id = ?",
            (bracket.current_state, bracket_id),
        )
        return True


def _bracket_id_by_type(db, bracket_type):
    rows = db.execute(
        "SELECT id FROM brackets WHERE type IN (?, ?) LIMIT 2",
        (bracket_type, bracket_type.name.lower()),
    ).fetchall()
    if len(rows) > 1:
        raise ValueError("Plusieurs tableaux sauvegardés ont cette catégorie.")
    return rows[0]["id"] if rows else None


def _save_new_bracket(db, bracket):
    _ensure_tournament(db)
    snapshot = json.loads(json.dumps(bracket, default=to_json_default))
    player_ids = {
        tuple(row[field] for field in PLAYER_FIELDS): row["id"]
        for row in db.execute(
            "SELECT * FROM tournament_players WHERE tournament_id = 1"
        )
    }

    def player_id(player):
        return _write_player(db, player_ids, player)

    return _write_bracket(db, snapshot, player_id)


def save_pool_match_result(bracket: Bracket, pool: Pool, match: Match) -> None:
    """Enregistre le résultat validé d'un match de poule identifié par ses joueurs."""
    if not match.is_played():
        raise ValueError("Validez le résultat du match avant de l'enregistrer.")
    first, second = match.players
    with _write_db() as db:
        bracket_id = _bracket_id_by_type(db, bracket.type)
        if bracket_id is None:
            bracket_id = _save_new_bracket(db, bracket)
        rows = db.execute(
            """SELECT m.* FROM matches AS m
               JOIN pools AS p ON p.id = m.pool_id
               JOIN tournament_players AS first ON first.id = m.first_player_id
               JOIN tournament_players AS second ON second.id = m.second_player_id
               WHERE m.bracket_id = ? AND p.label = ? AND m.label = ?
                 AND first.licence_number = ? AND second.licence_number = ?
               LIMIT 2""",
            (
                bracket_id,
                pool.id,
                match.id,
                first.licence_number,
                second.licence_number,
            ),
        ).fetchall()
        if len(rows) != 1:
            raise ValueError(
                "Le match ne correspond pas à une rencontre unique dans la sauvegarde."
            )

        row = rows[0]
        if row["first_score"] != row["second_score"]:
            saved_sets = tuple(tuple(points) for points in _sets(db, row["id"]))
            if match.sets != saved_sets:
                raise ValueError("Un autre résultat est déjà sauvegardé pour ce match.")
            return
        _write_match_result(db, row, match)


def update_match_result(match_id: int, sets: list[tuple[int, int]]) -> bool:
    """Enregistre ou corrige un résultat en appliquant les règles de Match."""
    with _write_db() as db:
        row = db.execute("SELECT * FROM matches WHERE id = ?", (match_id,)).fetchone()
        if row is None:
            return False
        player_ids = (row["first_player_id"], row["second_player_id"])
        if None in player_ids:
            raise ValueError(
                "Les deux joueurs doivent être connus pour enregistrer un résultat."
            )
        players = [
            player_from_row(
                db.execute(
                    "SELECT * FROM tournament_players WHERE id = ?", (player_id,)
                ).fetchone()
            )
            for player_id in player_ids
        ]
        match = Match(row["label"], players, _saved_type(MatchType, row["type"]))
        match.record_result(sets)
        _write_match_result(db, row, match)
        return True


def _write_match_result(db, row, match):
    match_id = row["id"]
    first_score, second_score = match.scores
    winner_id = (
        row["first_player_id"]
        if first_score > second_score
        else row["second_player_id"]
    )
    db.execute(
        """UPDATE matches SET first_score = ?, second_score = ?,
               legacy_winner_id = CASE WHEN has_legacy_winner THEN ? END
           WHERE id = ?""",
        (first_score, second_score, winner_id, match_id),
    )
    db.execute("DELETE FROM match_sets WHERE match_id = ?", (match_id,))
    db.executemany(
        "INSERT INTO match_sets (match_id, position, first_points, second_points) VALUES (?, ?, ?, ?)",
        ((match_id, position, *points) for position, points in enumerate(match.sets)),
    )
