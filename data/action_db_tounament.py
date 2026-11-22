import json
from datetime import date

from data.action_db_players import player_from_row
from data.database import connect_db
from domain.bracket import Bracket
from domain.enums import BracketType, MatchType
from domain.match import Match
from domain.player import Player
from domain.pool import Pool

PLAYER_FIELDS = (
    "licence_number",
    "firstname",
    "lastname",
    "birthdate",
    "club",
    "federation_ranking",
    "email",
    "phone_number",
    "second_bracket",
)


def to_json_default(obj):
    return obj.isoformat() if isinstance(obj, date) else vars(obj)


def save_tournament(T):
    snapshot = json.loads(json.dumps(T, ensure_ascii=False, default=to_json_default))
    db = connect_db()
    try:
        with db:
            write_tournament(db, snapshot)
    finally:
        db.close()


def load_tournament():
    db = connect_db()
    try:
        with db:
            db.execute("BEGIN")
            return read_tournament(db)
    finally:
        db.close()


def get_tournament_player_from_db(player_id: int) -> Player | None:
    """Renvoie le profil sauvegardé correspondant à tournament_players.id."""
    db = connect_db()
    try:
        row = db.execute(
            "SELECT * FROM tournament_players WHERE id = ?", (player_id,)
        ).fetchone()
        return player_from_row(row) if row is not None else None
    finally:
        db.close()


def get_bracket_from_db(bracket_id: int) -> Bracket | None:
    """Renvoie le tableau correspondant à brackets.id, avec ses poules et matchs."""
    return _get_saved_object(
        "SELECT * FROM brackets WHERE id = ?", bracket_id, _bracket_from_row
    )


def get_pool_from_db(pool_id: int) -> Pool | None:
    """Renvoie la poule correspondant à pools.id, avec ses joueurs et matchs."""
    return _get_saved_object(
        "SELECT * FROM pools WHERE id = ?", pool_id, _pool_from_row
    )


def get_match_from_db(match_id: int) -> Match | None:
    """Renvoie le match correspondant à matches.id, avec ses joueurs et sets."""
    return _get_saved_object(
        "SELECT * FROM matches WHERE id = ?", match_id, _match_from_row
    )


def _get_saved_object(query, object_id, from_row):
    db = connect_db()
    try:
        with db:
            db.execute("BEGIN")
            row = db.execute(query, (object_id,)).fetchone()
            if row is None:
                return None

            players = {None: None}

            def read_player(player_id):
                if player_id not in players:
                    player = db.execute(
                        "SELECT * FROM tournament_players WHERE id = ?", (player_id,)
                    ).fetchone()
                    players[player_id] = player_from_row(player)
                return players[player_id]

            return from_row(db, row, read_player)
    finally:
        db.close()


def _bracket_from_row(db, row, read_player):
    bracket_id = row["id"]
    bracket = Bracket(_saved_type(BracketType, row["type"]))
    if row["current_state"] is not None:
        vars(bracket)["_Bracket__current_state"] = _saved_type(
            MatchType, row["current_state"]
        )
    bracket.players.extend(
        read_player(p["player_id"]) for p in _bracket_players(db, bracket_id)
    )
    bracket.pools.extend(
        _pool_from_row(db, p, read_player) for p in _pools(db, bracket_id)
    )
    bracket.matches.extend(
        _match_from_row(db, m, read_player) for m in _matches(db, bracket_id)
    )
    return bracket


def _pool_from_row(db, row, read_player):
    pool_id = row["id"]
    pool = Pool(row["label"])
    pool.players.extend(read_player(p["player_id"]) for p in _pool_players(db, pool_id))
    pool.matches.extend(
        _match_from_row(db, m, read_player)
        for m in _matches(db, row["bracket_id"], pool_id)
    )
    return pool


def _match_from_row(db, row, read_player):
    match = Match(
        row["label"],
        [read_player(row["first_player_id"]), read_player(row["second_player_id"])],
        _saved_type(MatchType, row["type"]),
    )
    # On restaure les scores enregistrés, y compris ceux des matchs non joués.
    vars(match)["_Match__scores"] = [row["first_score"], row["second_score"]]
    vars(match)["_Match__sets"] = tuple(
        tuple(points) for points in _sets(db, row["id"])
    )
    return match


def _saved_type(enum, value):
    # Les premières sauvegardes utilisaient les noms anglais des énumérations.
    name = value.upper()
    return enum[name] if name in enum.__members__ else enum(value)


def _bracket_players(db, bracket_id):
    return db.execute(
        "SELECT player_id FROM bracket_players WHERE bracket_id = ? ORDER BY position",
        (bracket_id,),
    )


def _pools(db, bracket_id):
    return db.execute(
        "SELECT * FROM pools WHERE bracket_id = ? ORDER BY id", (bracket_id,)
    )


def _pool_players(db, pool_id):
    return db.execute(
        "SELECT player_id FROM pool_players WHERE pool_id = ? ORDER BY position",
        (pool_id,),
    )


def _matches(db, bracket_id, pool_id=None):
    return db.execute(
        "SELECT * FROM matches WHERE bracket_id = ? AND pool_id IS ? ORDER BY id",
        (bracket_id, pool_id),
    )


def _sets(db, match_id):
    return db.execute(
        "SELECT first_points, second_points FROM match_sets WHERE match_id = ? ORDER BY position",
        (match_id,),
    )


def _write_matches(db, matches, bracket_id, player_id, pool_id=None):
    for match in matches:
        first_player, second_player = match["_Match__players"]
        first_score, second_score = match["_Match__scores"]
        row = db.execute(
            """INSERT INTO matches (
                       bracket_id, pool_id, label, type, first_player_id, second_player_id,
                       first_score, second_score, has_legacy_winner, legacy_winner_id
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                bracket_id,
                pool_id,
                match["_Match__id"],
                match["_Match__type"],
                player_id(first_player),
                player_id(second_player),
                first_score,
                second_score,
                "_Match__winner" in match,
                player_id(match.get("_Match__winner")),
            ),
        )
        db.executemany(
            "INSERT INTO match_sets (match_id, position, first_points, second_points) VALUES (?, ?, ?, ?)",
            (
                (row.lastrowid, position, *points)
                for position, points in enumerate(match["_Match__sets"])
            ),
        )


def _write_player(db, player_ids, player, roster_position=None):
    if player is None:
        return None
    # Un même numéro de licence peut avoir deux profils si le joueur a été remplacé.
    fields = tuple(player[f"_Player__{field}"] for field in PLAYER_FIELDS)
    if roster_position is None and fields in player_ids:
        return player_ids[fields]
    row = db.execute(
        """INSERT INTO tournament_players (
               tournament_id, roster_position, licence_number, firstname, lastname, birthdate,
               club, federation_ranking, email, phone_number, second_bracket
           ) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (roster_position, *fields),
    )
    player_ids.setdefault(fields, row.lastrowid)
    return row.lastrowid


def _write_bracket(db, bracket, player_id):
    row = db.execute(
        """INSERT INTO brackets (tournament_id, type, current_state, legacy_current_pool)
           VALUES (1, ?, ?, ?)""",
        (
            bracket["_Bracket__type"],
            bracket.get("_Bracket__current_state", bracket.get("current_phase")),
            bracket.get("current_pool"),
        ),
    )
    bracket_id = row.lastrowid
    players = bracket.get("_Bracket__players", bracket.get("players", []))
    db.executemany(
        "INSERT INTO bracket_players (bracket_id, position, player_id) VALUES (?, ?, ?)",
        (
            (bracket_id, position, player_id(player))
            for position, player in enumerate(players)
        ),
    )
    for pool in bracket["_Bracket__pools"]:
        row = db.execute(
            "INSERT INTO pools (bracket_id, label) VALUES (?, ?)",
            (bracket_id, pool["_Pool__id"]),
        )
        pool_id = row.lastrowid
        db.executemany(
            "INSERT INTO pool_players (pool_id, position, player_id) VALUES (?, ?, ?)",
            (
                (pool_id, position, player_id(player))
                for position, player in enumerate(pool["_Pool__players"])
            ),
        )
        _write_matches(db, pool["_Pool__matches"], bracket_id, player_id, pool_id)
    _write_matches(
        db,
        bracket.get("_Bracket__matches", bracket.get("matches", [])),
        bracket_id,
        player_id,
    )
    return bracket_id


def write_tournament(db, snapshot):
    db.execute("DELETE FROM tournaments WHERE id = 1")
    db.execute("INSERT INTO tournaments (id) VALUES (1)")
    player_ids = {}

    def player_id(player, roster_position=None):
        return _write_player(db, player_ids, player, roster_position)

    for position, player in enumerate(snapshot["_Tournament__all_players"]):
        player_id(player, position)

    for bracket in snapshot["_Tournament__brackets"]:
        _write_bracket(db, bracket, player_id)


def read_tournament(db):
    if db.execute("SELECT id FROM tournaments WHERE id = 1").fetchone() is None:
        return None

    players = {None: None}
    roster = []
    for row in db.execute(
        "SELECT * FROM tournament_players WHERE tournament_id = 1 ORDER BY roster_position"
    ):
        player = {f"_Player__{field}": row[field] for field in PLAYER_FIELDS}
        player["_Player__second_bracket"] = bool(row["second_bracket"])
        players[row["id"]] = player
        if row["roster_position"] is not None:
            roster.append(player.copy())

    def read_player(player_id):
        player = players[player_id]
        return player.copy() if player is not None else None

    def read_matches(bracket_id, pool_id=None):
        matches = []
        for row in _matches(db, bracket_id, pool_id):
            match = {
                "_Match__id": row["label"],
                "_Match__scores": [row["first_score"], row["second_score"]],
                "_Match__sets": [list(points) for points in _sets(db, row["id"])],
                "_Match__players": [
                    read_player(row["first_player_id"]),
                    read_player(row["second_player_id"]),
                ],
                "_Match__type": row["type"],
            }
            if row["has_legacy_winner"]:
                match["_Match__winner"] = read_player(row["legacy_winner_id"])
            matches.append(match)
        return matches

    brackets = []
    for bracket in db.execute(
        "SELECT * FROM brackets WHERE tournament_id = 1 ORDER BY id"
    ):
        bracket_id = bracket["id"]
        bracket_players = [
            read_player(row["player_id"]) for row in _bracket_players(db, bracket_id)
        ]
        pools = []
        for pool in _pools(db, bracket_id):
            pool_players = [
                read_player(row["player_id"]) for row in _pool_players(db, pool["id"])
            ]
            pools.append(
                {
                    "_Pool__id": pool["label"],
                    "_Pool__players": pool_players,
                    "_Pool__matches": read_matches(bracket_id, pool["id"]),
                }
            )

        # Les premières sauvegardes utilisaient des attributs publics pour le tableau.
        if bracket["legacy_current_pool"] is not None:
            brackets.append(
                {
                    "current_phase": bracket["current_state"],
                    "matches": read_matches(bracket_id),
                    "players": bracket_players,
                    "_Bracket__pools": pools,
                    "_Bracket__type": bracket["type"],
                    "current_pool": bracket["legacy_current_pool"],
                }
            )
        else:
            data = {
                "_Bracket__type": bracket["type"],
                "_Bracket__players": bracket_players,
                "_Bracket__pools": pools,
            }
            if bracket["current_state"] is not None:
                data["_Bracket__matches"] = read_matches(bracket_id)
                data["_Bracket__current_state"] = bracket["current_state"]
            brackets.append(data)

    return {"_Tournament__all_players": roster, "_Tournament__brackets": brackets}
