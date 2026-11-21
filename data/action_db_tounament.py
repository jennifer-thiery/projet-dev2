import json
from datetime import date

from data.database import connect_db


def to_json_default(obj):
    return obj.isoformat() if isinstance(obj, date) else vars(obj)


def save_tournament(T):
    # shortcut: une seule sauvegarde complète, séparer les tables si des requêtes par match sont nécessaires.
    snapshot = json.dumps(T, ensure_ascii=False, default=to_json_default)
    db = connect_db()
    try:
        db.execute("REPLACE INTO tournament (id, snapshot) VALUES (1, ?)", (snapshot,))
        db.commit()
    finally:
        db.close()


def load_tournament():
    db = connect_db()
    try:
        row = db.execute("SELECT snapshot FROM tournament WHERE id = 1").fetchone()
    finally:
        db.close()
    return json.loads(row[0]) if row is not None else None
