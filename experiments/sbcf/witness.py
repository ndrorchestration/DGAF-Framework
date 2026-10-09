"""Synthetic off-store high-water witness. Not a remote service or trusted platform."""
import sqlite3
from pathlib import Path
from .durable_evidence import DurableEvidenceVerifier

class WitnessedVerifier:
    def __init__(self, evidence_path: str | Path, witness_path: str | Path, keys: dict, allowed_fields: dict):
        if Path(evidence_path).resolve() == Path(witness_path).resolve():
            raise ValueError("witness must be a separate store")
        self.evidence = DurableEvidenceVerifier(evidence_path, keys, allowed_fields)
        self.witness_path = str(witness_path)
        with sqlite3.connect(self.witness_path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS counters (source TEXT, run TEXT, sequence INTEGER, PRIMARY KEY(source,run))")

    def admit(self, record: dict, *, expected_run: str, expected_policy: str, expected_nonce: str) -> bool:
        if not isinstance(record, dict):
            return False
        source, seq = record.get("source"), record.get("sequence")
        if not isinstance(source, str) or type(seq) is not int:
            return False
        with sqlite3.connect(self.witness_path, isolation_level="IMMEDIATE") as db:
            previous = db.execute("SELECT sequence FROM counters WHERE source=? AND run=?", (source, expected_run)).fetchone()
            if previous and seq <= previous[0]:
                return False
            if not self.evidence.admit(record, expected_run=expected_run, expected_policy=expected_policy, expected_nonce=expected_nonce):
                return False
            db.execute("INSERT INTO counters(source,run,sequence) VALUES (?,?,?) ON CONFLICT(source,run) DO UPDATE SET sequence=excluded.sequence", (source,expected_run,seq))
        return True
