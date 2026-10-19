"""Atomic local synthetic witness. Not independent custody or a trusted platform."""

import sqlite3
from contextlib import closing
from pathlib import Path

from .durable_evidence import DurableEvidenceVerifier
from .signed_evidence import EvidenceVerifier


class WitnessedVerifier:
    def __init__(self, evidence_path: str | Path, witness_path: str | Path, keys: dict, allowed_fields: dict):
        if any(str(path) in ("", ":memory:") for path in (evidence_path, witness_path)):
            raise ValueError("witness admission requires two persistent stores")
        evidence_path, witness_path = Path(evidence_path).resolve(), Path(witness_path).resolve()
        if evidence_path == witness_path or (
            evidence_path.exists() and witness_path.exists() and evidence_path.samefile(witness_path)
        ):
            raise ValueError("witness must be a separate store")
        # Private implementation dependency: callers must use witnessed admission.
        # Python attribute privacy is not a security boundary; tests retain that counterexample.
        self._evidence = DurableEvidenceVerifier(evidence_path, keys, allowed_fields)
        self.witness_path = str(witness_path)
        with closing(sqlite3.connect(self.witness_path)) as db, db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS counters "
                "(source TEXT, run TEXT, sequence INTEGER, PRIMARY KEY(source,run))"
            )

    def admit(self, record: dict, *, expected_run: str, expected_policy: str, expected_nonce: str) -> bool:
        if not isinstance(record, dict) or type(record.get("state")) is not dict:
            return False
        source = record.get("source")
        if not isinstance(source, str) or source not in self._evidence.allowed_fields:
            return False
        if not set(record["state"]).issubset(self._evidence.allowed_fields[source]):
            return False
        try:
            if not EvidenceVerifier(self._evidence.keys).admit(
                record, expected_run=expected_run, expected_policy=expected_policy, expected_nonce=expected_nonce
            ):
                return False
        except (TypeError, ValueError, OverflowError):
            return False

        # mode=rw prevents a missing store being silently recreated during admission.
        evidence_uri = Path(self._evidence.path).as_uri() + "?mode=rw"
        witness_uri = Path(self.witness_path).as_uri() + "?mode=rw"
        try:
            with closing(sqlite3.connect(evidence_uri, uri=True, timeout=10, isolation_level=None)) as db:
                db.execute("ATTACH DATABASE ? AS witness", (witness_uri,))
                # Attached databases are atomic as a set only with persistent main
                # and rollback journals. Reject WAL instead of changing its mode.
                for schema in ("main", "witness"):
                    db.execute(f"PRAGMA {schema}.synchronous=FULL")
                db.execute("BEGIN IMMEDIATE")
                for schema in ("main", "witness"):
                    if db.execute(f"PRAGMA {schema}.journal_mode").fetchone()[0] != "delete":
                        return False
                current = db.execute(
                    "SELECT sequence FROM main.high_water WHERE source=? AND run=?", (source, expected_run)
                ).fetchone()
                previous = db.execute(
                    "SELECT sequence FROM witness.counters WHERE source=? AND run=?", (source, expected_run)
                ).fetchone()
                # Never heal divergent counters by admitting a larger sequence.
                # Reconciliation needs evidence outside this admission API.
                if current != previous or (current and (type(current[0]) is not int or current[0] < 0)):
                    return False
                seq = record["sequence"]
                if current and seq <= current[0]:
                    return False
                db.execute(
                    "INSERT INTO main.admission(source,run,sequence) VALUES (?,?,?)", (source, expected_run, seq)
                )
                db.execute(
                    "INSERT INTO main.high_water(source,run,sequence) VALUES (?,?,?) "
                    "ON CONFLICT(source,run) DO UPDATE SET sequence=excluded.sequence",
                    (source, expected_run, seq),
                )
                db.execute(
                    "INSERT INTO witness.counters(source,run,sequence) VALUES (?,?,?) "
                    "ON CONFLICT(source,run) DO UPDATE SET sequence=excluded.sequence",
                    (source, expected_run, seq),
                )
                db.commit()
            return True
        except (sqlite3.DatabaseError, OverflowError):
            # Closing rolls back an uncommitted transaction in both stores.
            return False
