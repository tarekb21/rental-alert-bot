"""Simple SQLite storage for listings and history."""
import sqlite3
from typing import List, Dict
from pathlib import Path
import json
import datetime


DB_PATH = Path(__file__).parent.parent / "data" / "listings.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


class Storage:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(self.db_path))
        self._ensure_tables()

    def _ensure_tables(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS listings (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id TEXT,
                change_type TEXT,
                old_data TEXT,
                new_data TEXT,
                created_at TEXT
            )
            """
        )
        self.conn.commit()

    def upsert_listings(self, listings: List[Dict]) -> List[Dict]:
        """Upsert listings and return list of changes detected.

        Change dict contains: listing_id, change_type, old, new
        """
        cur = self.conn.cursor()
        changes = []
        for l in listings:
            lid = l['id']
            cur.execute("SELECT data FROM listings WHERE id = ?", (lid,))
            row = cur.fetchone()
            now = datetime.datetime.utcnow().isoformat()
            as_json = json.dumps(l, sort_keys=True)
            if not row:
                cur.execute(
                    "INSERT INTO listings(id, data, updated_at) VALUES (?, ?, ?)",
                    (lid, as_json, now),
                )
                cur.execute(
                    "INSERT INTO history(listing_id, change_type, old_data, new_data, created_at) VALUES (?, ?, ?, ?, ?)",
                    (lid, 'new', None, as_json, now),
                )
                changes.append({'listing_id': lid, 'change_type': 'new', 'old': None, 'new': l})
            else:
                old_json = row[0]
                if old_json != as_json:
                    cur.execute(
                        "UPDATE listings SET data = ?, updated_at = ? WHERE id = ?",
                        (as_json, now, lid),
                    )
                    cur.execute(
                        "INSERT INTO history(listing_id, change_type, old_data, new_data, created_at) VALUES (?, ?, ?, ?, ?)",
                        (lid, 'updated', old_json, as_json, now),
                    )
                    changes.append({'listing_id': lid, 'change_type': 'updated', 'old': json.loads(old_json), 'new': l})
        self.conn.commit()
        return changes

    def close(self):
        self.conn.close()
