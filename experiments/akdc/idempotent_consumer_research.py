"""AKDC Gate 15: two-local-DB synthetic idempotent consumer / sender ACK boundary.

A receiver-local durable idempotency receipt is atomic with its own simulated
effect marker. The sender outbox uses a separate SQLite DB with NO global
transaction. No network, authorization, real side effect, or exactly-once claim.
"""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
from contextlib import closing
from pathlib import Path

from experiments.akdc.mrtr_outbox_research import SQLiteOutboxResearch


class ConsumerRefusal(ValueError):
    """Malformed idempotency identity, conflicting binding, or damaged schema."""


class SQLiteIdempotentConsumerResearch:
    """Separate local SQLite receiver; a test receipt is not a real external effect."""

    TABLES = (
        """CREATE TABLE inbox (
            idempotency_key TEXT NOT NULL PRIMARY KEY,
            payload_tag TEXT NOT NULL
        )""",
        """CREATE TABLE receiver_effect (
            idempotency_key TEXT NOT NULL PRIMARY KEY REFERENCES inbox(idempotency_key),
            outcome TEXT NOT NULL CHECK(outcome = 'SYNTHETIC_RECEIVER_MARKER')
        )""",
    )

    def __init__(self, path: str | Path):
        if str(path) == ":memory:":
            raise ConsumerRefusal("file-backed consumer DB required")
        self.path = str(path)
        with closing(self._connect()) as conn:
            try:
                conn.execute("BEGIN IMMEDIATE")
                version = conn.execute("PRAGMA user_version").fetchone()[0]
                tables = {
                    row[0]
                    for row in conn.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                    )
                }
                if version == 0 and not tables:
                    for sql in self.TABLES:
                        conn.execute(sql)
                    conn.execute("PRAGMA user_version=1")
                elif version != 1:
                    raise ConsumerRefusal("unversioned or unsupported inbox schema")
                self._check(conn)
                conn.execute("COMMIT")
            except BaseException:
                if conn.in_transaction:
                    conn.execute("ROLLBACK")
                raise

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=20, isolation_level=None)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA busy_timeout=20000")
        return conn

    @staticmethod
    def _check(conn: sqlite3.Connection) -> None:
        names = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
        }
        if names != {"inbox", "receiver_effect"}:
            raise ConsumerRefusal("inbox table set differs from contract")
        inbox = [(r[1], r[2].upper(), r[3], r[5]) for r in conn.execute("PRAGMA table_info(inbox)")]
        effects = [(r[1], r[2].upper(), r[3], r[5]) for r in conn.execute("PRAGMA table_info(receiver_effect)")]
        if inbox != [("idempotency_key", "TEXT", 1, 1), ("payload_tag", "TEXT", 1, 0)]:
            raise ConsumerRefusal("inbox key or binding shape weakened")
        if effects != [("idempotency_key", "TEXT", 1, 1), ("outcome", "TEXT", 1, 0)]:
            raise ConsumerRefusal("receiver effect key shape weakened")
        sql = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='receiver_effect'"
        ).fetchone()[0]
        if "CHECK(OUTCOME='SYNTHETIC_RECEIVER_MARKER')" not in "".join(sql.upper().split()):
            raise ConsumerRefusal("receiver effect outcome restriction missing")
        fk = conn.execute("PRAGMA foreign_key_list(receiver_effect)").fetchall()
        if len(fk) != 1 or fk[0][2:5] != ("inbox", "idempotency_key", "idempotency_key"):
            raise ConsumerRefusal("receiver effect foreign-key constraint missing")
        if conn.execute("PRAGMA foreign_key_check").fetchone():
            raise ConsumerRefusal("receiver effect referential integrity damaged")

    def accept(self, *, key: str, payload: str, crash: str = "") -> str:
        """One simulated receiver marker across duplicate requests under same key."""
        if not re.fullmatch(r"[0-9a-f]{64}", key) or not re.fullmatch(r"[0-9a-f]{64}", payload):
            raise ConsumerRefusal("expected test-only 64-digit hexadecimal key/payload tags")
        if crash not in ("", "before_commit", "after_commit"):
            raise ConsumerRefusal("unsupported injected consumer crash")
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            self._check(conn)
            previous = conn.execute("SELECT payload_tag FROM inbox WHERE idempotency_key=?", (key,)).fetchone()
            if previous:
                if previous[0] != payload:
                    raise ConsumerRefusal("same idempotency key with different bound payload")
                result = "DUPLICATE_RECEIVER_MARKER"
            else:
                conn.execute("INSERT INTO inbox VALUES (?, ?)", (key, payload))
                conn.execute("INSERT INTO receiver_effect VALUES (?, 'SYNTHETIC_RECEIVER_MARKER')", (key,))
                result = "FIRST_RECEIVER_MARKER"
            if crash == "before_commit":
                os._exit(71)
            conn.execute("COMMIT")
            if crash == "after_commit":
                os._exit(72)
            return result
        except BaseException:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    def counts(self) -> tuple[int, int]:
        with closing(self._connect()) as conn:
            self._check(conn)
            return (
                conn.execute("SELECT COUNT(*) FROM inbox").fetchone()[0],
                conn.execute("SELECT COUNT(*) FROM receiver_effect").fetchone()[0],
            )


def deliver_one(
    producer: SQLiteOutboxResearch,
    receiver: SQLiteIdempotentConsumerResearch,
    *,
    crash: str = "",
) -> str:
    """Receiver commit happens before separate producer ACK (no two-DB atomicity).

    Simulate the sender dying between receiver commit and producer ACK. Recovery
    redrives the same idempotency key; receiver's marker must not duplicate.
    """
    if crash not in ("", "after_receiver_before_ack", "after_sender_ack"):
        raise ConsumerRefusal("unsupported sender crash boundary")
    conn = producer._connect()
    try:
        conn.execute("BEGIN IMMEDIATE")
        producer._check_schema(conn)
        row = conn.execute("SELECT tag, payload FROM outbox WHERE status='PENDING' ORDER BY rowid LIMIT 1").fetchone()
        if row is None:
            conn.execute("COMMIT")
            return "NO_PENDING"
        key, payload = row
        receiver_result = receiver.accept(key=key, payload=payload)
        if crash == "after_receiver_before_ack":
            os._exit(73)
        conn.execute("INSERT INTO local_effect VALUES (?, 'SYNTHETIC_DB_MARKER')", (key,))
        conn.execute("UPDATE outbox SET status='APPLIED' WHERE tag=?", (key,))
        conn.execute("UPDATE receipt SET status='APPLIED' WHERE tag=?", (key,))
        conn.execute("COMMIT")
        if crash == "after_sender_ack":
            os._exit(74)
        return receiver_result
    except BaseException:
        if conn.in_transaction:
            conn.execute("ROLLBACK")
        raise
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="two-DB synthetic nonauthorizing redrive test")
    parser.add_argument("--producer", required=True)
    parser.add_argument("--consumer", required=True)
    parser.add_argument("--crash", default="")
    args = parser.parse_args()
    secret = bytes.fromhex(os.environ.get("AKDC_RESEARCH_OUTBOX_KEY_HEX", ""))
    sender = SQLiteOutboxResearch(args.producer, secret)
    receiver = SQLiteIdempotentConsumerResearch(args.consumer)
    print(deliver_one(sender, receiver, crash=args.crash))


if __name__ == "__main__":
    main()
