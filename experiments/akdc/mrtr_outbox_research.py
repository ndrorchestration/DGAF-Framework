"""AKDC Gate 14: research-only synthetic SQLite receipt/outbox and crash witness.

Local database effect marker can commit atomically with the receipt/outbox.
An OUTSIDE-FILE append cannot: the explicit fault injection demonstrates the
external exactly-once gap. No authorization, remote effect or verified identity.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import sqlite3
from contextlib import closing
from pathlib import Path


class OutboxRefusal(ValueError):
    """Receipt, binding or schema cannot safely be accepted as research data."""


class SQLiteOutboxResearch:
    """One local SQLite file and caller-asserted identity; not a control plane."""

    VERSION = 1
    TABLES = (
        """CREATE TABLE receipt (
          tag TEXT NOT NULL PRIMARY KEY, binding TEXT NOT NULL,
          status TEXT NOT NULL CHECK(status IN ('PENDING','APPLIED'))
        )""",
        """CREATE TABLE outbox (
          tag TEXT NOT NULL PRIMARY KEY REFERENCES receipt(tag),
          payload TEXT NOT NULL,
          status TEXT NOT NULL CHECK(status IN ('PENDING','APPLIED'))
        )""",
        """CREATE TABLE local_effect (
          tag TEXT NOT NULL PRIMARY KEY REFERENCES receipt(tag),
          outcome TEXT NOT NULL CHECK(outcome = 'SYNTHETIC_DB_MARKER')
        )""",
    )
    SHAPES = {
        "receipt": (("tag", "TEXT", 1, 1), ("binding", "TEXT", 1, 0), ("status", "TEXT", 1, 0)),
        "outbox": (("tag", "TEXT", 1, 1), ("payload", "TEXT", 1, 0), ("status", "TEXT", 1, 0)),
        "local_effect": (("tag", "TEXT", 1, 1), ("outcome", "TEXT", 1, 0)),
    }

    def __init__(self, path: str | Path, key: bytes):
        if str(path) == ":memory:":
            raise OutboxRefusal("file-backed DB required")
        if type(key) is not bytes or len(key) < 32:
            raise OutboxRefusal("caller-supplied 32+ byte bytes key required")
        self.path, self._key = str(path), key
        with closing(self._connect()) as conn:
            try:
                conn.execute("BEGIN IMMEDIATE")
                version = conn.execute("PRAGMA user_version").fetchone()[0]
                tables = {
                    r[0]
                    for r in conn.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                    )
                }
                if version == 0 and not tables:
                    for statement in self.TABLES:
                        conn.execute(statement)
                    conn.execute(f"PRAGMA user_version={self.VERSION}")
                elif version != self.VERSION:
                    raise OutboxRefusal("unversioned, partial or unsupported database")
                self._check_schema(conn)
                conn.execute("COMMIT")
            except BaseException:
                if conn.in_transaction:
                    conn.execute("ROLLBACK")
                raise

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=20.0, isolation_level=None)
        conn.execute("PRAGMA busy_timeout=20000")
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    @classmethod
    def _check_schema(cls, conn: sqlite3.Connection) -> None:
        tables = {
            r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
        }
        if tables != set(cls.SHAPES):
            raise OutboxRefusal("missing or unexpected outbox table")
        for name, shape in cls.SHAPES.items():
            rows = conn.execute(f"PRAGMA table_info({name})").fetchall()
            actual = tuple((r[1], r[2].upper(), r[3], r[5]) for r in rows)
            if actual != shape:
                raise OutboxRefusal("weakened outbox table shape")
            sql = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone()[0]
            normalized = "".join(sql.upper().split())
            if name == "receipt" and "CHECK(STATUSIN('PENDING','APPLIED'))" not in normalized:
                raise OutboxRefusal("missing receipt CHECK constraint")
            if name == "outbox" and "CHECK(STATUSIN('PENDING','APPLIED'))" not in normalized:
                raise OutboxRefusal("missing outbox CHECK constraint")
            if name == "local_effect" and "CHECK(OUTCOME='SYNTHETIC_DB_MARKER')" not in normalized:
                raise OutboxRefusal("missing effect CHECK constraint")
            if name in ("outbox", "local_effect"):
                foreign = conn.execute(f"PRAGMA foreign_key_list({name})").fetchall()
                if len(foreign) != 1 or foreign[0][2:5] != ("receipt", "tag", "tag"):
                    raise OutboxRefusal("missing receipt foreign key")
        if conn.execute("PRAGMA foreign_key_check").fetchone() is not None:
            raise OutboxRefusal("broken foreign-key integrity")

    def _tag(self, domain: str, *parts: str) -> str:
        raw = json.dumps([domain, *parts], ensure_ascii=True, separators=(",", ":")).encode("ascii")
        return hmac.new(self._key, raw, hashlib.sha256).hexdigest()

    @staticmethod
    def _validate(nonce: str, principal: str, action: str, operation_digest: str) -> None:
        if not re.fullmatch(r"[0-9a-f]{32}", nonce):
            raise OutboxRefusal("invalid synthetic nonce")
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", principal):
            raise OutboxRefusal("invalid unverified principal claim")
        if action != "akdc-confirm-fixture" or not re.fullmatch(r"[0-9a-f]{64}", operation_digest):
            raise OutboxRefusal("only fixed synthetic operation allowed")

    def submit(self, *, nonce: str, principal: str, action: str, operation_digest: str, crash: str = "") -> str:
        self._validate(nonce, principal, action, operation_digest)
        if crash not in ("", "before_commit", "after_commit"):
            raise OutboxRefusal("unsupported submit crash mode")
        tag = self._tag("AKDC-OUTBOX-NONCE-V1", nonce)
        binding = self._tag("AKDC-OUTBOX-BINDING-V1", principal, action, operation_digest)
        payload = self._tag("AKDC-OUTBOX-PAYLOAD-V1", action, operation_digest)
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT binding, status FROM receipt WHERE tag=?", (tag,)).fetchone()
            if row:
                if row[0] != binding:
                    raise OutboxRefusal("nonce rebinding collision")
                result = "EXISTING_" + row[1]
            else:
                conn.execute("INSERT INTO receipt VALUES (?, ?, 'PENDING')", (tag, binding))
                conn.execute("INSERT INTO outbox VALUES (?, ?, 'PENDING')", (tag, payload))
                result = "ENQUEUED"
            if crash == "before_commit":
                os._exit(51)
            conn.execute("COMMIT")
            if crash == "after_commit":
                os._exit(52)
            return result
        except BaseException:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    def dispatch_one(self, *, sink: str | Path | None = None, crash: str = "") -> str:
        """Local DB effect is atomic; optional test-file sink exposes external gap."""
        if crash not in ("", "before_local_commit", "after_local_commit", "after_sink_before_commit"):
            raise OutboxRefusal("unsupported dispatch crash mode")
        if crash == "after_sink_before_commit" and sink is None:
            raise OutboxRefusal("sink required for external failure experiment")
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT tag FROM outbox WHERE status='PENDING' ORDER BY rowid LIMIT 1").fetchone()
            if row is None:
                conn.execute("COMMIT")
                return "NO_PENDING"
            tag = row[0]
            conn.execute("INSERT INTO local_effect VALUES (?, 'SYNTHETIC_DB_MARKER')", (tag,))
            if sink is not None:
                # Deliberate external I/O outside the SQLite transaction's atomic scope.
                with open(sink, "a", encoding="ascii") as stream:
                    stream.write("SYNTHETIC_NONAUTHORIZING_EFFECT\n")
                    stream.flush()
                    os.fsync(stream.fileno())
            if crash in ("before_local_commit", "after_sink_before_commit"):
                os._exit(53)
            conn.execute("UPDATE outbox SET status='APPLIED' WHERE tag=?", (tag,))
            conn.execute("UPDATE receipt SET status='APPLIED' WHERE tag=?", (tag,))
            conn.execute("COMMIT")
            if crash == "after_local_commit":
                os._exit(54)
            return "LOCAL_MARKER_COMMITTED"
        except BaseException:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    def counts(self) -> tuple[int, int, int]:
        with closing(self._connect()) as conn:
            self._check_schema(conn)
            receipts = conn.execute("SELECT COUNT(*) FROM receipt").fetchone()[0]
            pending = conn.execute("SELECT COUNT(*) FROM outbox WHERE status='PENDING'").fetchone()[0]
            effects = conn.execute("SELECT COUNT(*) FROM local_effect").fetchone()[0]
            return receipts, pending, effects


def main() -> None:
    parser = argparse.ArgumentParser(description="AKDC nonauthorizing synthetic outbox fixture")
    parser.add_argument("--db", required=True)
    parser.add_argument("--mode", choices=("submit", "dispatch", "counts"), required=True)
    parser.add_argument("--nonce", default="a" * 32)
    parser.add_argument("--principal", default="fixture-only")
    parser.add_argument("--operation-digest", default="b" * 64)
    parser.add_argument("--crash", default="")
    parser.add_argument("--sink", default="")
    args = parser.parse_args()
    key = bytes.fromhex(os.environ.get("AKDC_RESEARCH_OUTBOX_KEY_HEX", ""))
    store = SQLiteOutboxResearch(args.db, key)
    if args.mode == "submit":
        answer = store.submit(nonce=args.nonce, principal=args.principal, action="akdc-confirm-fixture",
                              operation_digest=args.operation_digest, crash=args.crash)
    elif args.mode == "dispatch":
        answer = store.dispatch_one(sink=args.sink or None, crash=args.crash)
    else:
        answer = store.counts()
    print(json.dumps({"result": answer, "authority": "NOT_GRANTED"}))


if __name__ == "__main__":
    main()
