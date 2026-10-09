"""SQLite-backed synthetic evidence admission; NOT independently trusted custody."""
import sqlite3
from pathlib import Path
from .signed_evidence import EvidenceVerifier

class DurableEvidenceVerifier:
    def __init__(self, path: str | Path, keys: dict[str, bytes], allowed_fields: dict[str, frozenset[str]]):
        self.path = str(path)
        self.keys = keys
        self.allowed_fields = allowed_fields
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS admission (source TEXT NOT NULL, run TEXT NOT NULL, sequence INTEGER NOT NULL, PRIMARY KEY (source, run, sequence))")
            db.execute("CREATE TABLE IF NOT EXISTS high_water (source TEXT NOT NULL, run TEXT NOT NULL, sequence INTEGER NOT NULL, PRIMARY KEY (source, run))")

    def admit(self, record: dict, *, expected_run: str, expected_policy: str, expected_nonce: str) -> bool:
        if not isinstance(record, dict) or not isinstance(record.get("state"), dict):
            return False
        source = record.get("source")
        if source not in self.allowed_fields or not set(record["state"]).issubset(self.allowed_fields[source]):
            return False
        # First verify integrity in a throwaway verifier; do not commit in-memory admission state.
        verifier = EvidenceVerifier(self.keys)
        if not verifier.admit(record, expected_run=expected_run, expected_policy=expected_policy, expected_nonce=expected_nonce):
            return False
        try:
            with sqlite3.connect(self.path, timeout=10, isolation_level="IMMEDIATE") as db:
                current = db.execute("SELECT sequence FROM high_water WHERE source=? AND run=?", (source, expected_run)).fetchone()
                seq = record["sequence"]
                if current is not None and seq <= current[0]:
                    return False
                db.execute("INSERT INTO admission (source,run,sequence) VALUES (?,?,?)", (source, expected_run, seq))
                db.execute("INSERT INTO high_water (source,run,sequence) VALUES (?,?,?) ON CONFLICT(source,run) DO UPDATE SET sequence=excluded.sequence", (source, expected_run, seq))
            return True
        except sqlite3.IntegrityError:
            return False
