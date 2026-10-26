"""AKDC Gate 13: atomic SQLite *observation receipts* for verified synthetic MRTR retries.

NONRELEASE. No identity authentication, effect execution, transactionally coupled
external outbox, exactly-once claim, or production custody. All identity inputs
are caller assertions; use only after independently verified requestState.
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


class MRTRReceiptRefusal(ValueError):
    """Unsupported state, weakened schema or mismatched retry identity."""


class SQLiteMRTRReceiptResearch:
    """Local shared-file receipt ledger. DB receipts are NOT executed effects."""

    VERSION = 1
    CREATE = """CREATE TABLE mrtr_receipt (
        token_tag TEXT NOT NULL PRIMARY KEY,
        bound_claim TEXT NOT NULL,
        status TEXT NOT NULL CHECK (status = 'RECORD_ONLY'),
        outcome TEXT NOT NULL CHECK (outcome = 'SYNTHETIC_COMPLETE')
    )"""

    def __init__(self, path: str | Path, key: bytes):
        if str(path) == ":memory:":
            raise MRTRReceiptRefusal("file-backed shared DB required")
        if type(key) is not bytes or len(key) < 32:
            raise MRTRReceiptRefusal("key must be >=32-byte bytes")
        self.path = str(path)
        self._key = key
        with closing(self._connect()) as conn:
            try:
                conn.execute("BEGIN IMMEDIATE")
                version = conn.execute("PRAGMA user_version").fetchone()[0]
                tables = {
                    row[0] for row in conn.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                    )
                }
                if version == 0 and not tables:
                    conn.execute(self.CREATE)
                    conn.execute("PRAGMA user_version=1")
                elif version != self.VERSION:
                    raise MRTRReceiptRefusal("unknown or unversioned receipt schema")
                self._assert_shape(conn)
                conn.execute("COMMIT")
            except BaseException:
                if conn.in_transaction:
                    conn.execute("ROLLBACK")
                raise

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=15.0, isolation_level=None)
        conn.execute("PRAGMA busy_timeout=15000")
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL")
        return conn

    @staticmethod
    def _assert_shape(conn: sqlite3.Connection) -> None:
        actual = {
            row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
        }
        if actual != {"mrtr_receipt"}:
            raise MRTRReceiptRefusal("unexpected receipt schema tables")
        info = conn.execute("PRAGMA table_info(mrtr_receipt)").fetchall()
        shape = [(r[1], r[2].upper(), r[3], r[5]) for r in info]
        if shape != [
            ("token_tag", "TEXT", 1, 1), ("bound_claim", "TEXT", 1, 0),
            ("status", "TEXT", 1, 0), ("outcome", "TEXT", 1, 0)
        ]:
            raise MRTRReceiptRefusal("weakened receipt table columns or primary key")
        sql = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='mrtr_receipt'"
        ).fetchone()[0]
        norm = " ".join(sql.upper().split())
        if "CHECK (STATUS = 'RECORD_ONLY')" not in norm or "CHECK (OUTCOME = 'SYNTHETIC_COMPLETE')" not in norm:
            raise MRTRReceiptRefusal("missing fixed-outcome CHECK constraints")

    def _commitment(self, label: str, parts: list[str]) -> str:
        data = json.dumps([label, *parts], ensure_ascii=True, separators=(",", ":")).encode("ascii")
        return hmac.new(self._key, data, hashlib.sha256).hexdigest()

    def count(self) -> int:
        with closing(self._connect()) as conn:
            self._assert_shape(conn)
            return conn.execute("SELECT COUNT(*) FROM mrtr_receipt").fetchone()[0]

    def record(
        self,
        *,
        nonce: str,
        principal_claim: str,
        action: str,
        operation_digest: str,
        crash: str = "",
    ) -> str:
        """Atomic receipt for a previously verified SDK state, not authorization.

        On duplicate, return a stable synthetic recorded outcome. On different
        bound claims for one nonce, reject. Crashes are injected ONLY in tests.
        """
        if not re.fullmatch(r"[0-9a-f]{32}", nonce):
            raise MRTRReceiptRefusal("32-char lowercase synthetic nonce required")
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", principal_claim):
            raise MRTRReceiptRefusal("bounded unverified principal label required")
        if action != "akdc-confirm-fixture" or not re.fullmatch(r"[0-9a-f]{64}", operation_digest):
            raise MRTRReceiptRefusal("fixed fixture method and SHA-256 operation digest required")
        if crash not in ("", "before_commit", "after_commit"):
            raise MRTRReceiptRefusal("unknown injected crash mode")
        token_tag = self._commitment("AKDC-MRTR-NONCE-V1", [nonce])
        bound = self._commitment("AKDC-MRTR-BIND-V1", [principal_claim, action, operation_digest])
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            old = conn.execute(
                "SELECT bound_claim, status, outcome FROM mrtr_receipt WHERE token_tag=?", (token_tag,)
            ).fetchone()
            if old:
                if old != (bound, "RECORD_ONLY", "SYNTHETIC_COMPLETE"):
                    raise MRTRReceiptRefusal("binding collision or invalid stored outcome")
                conn.execute("COMMIT")
                return "DUPLICATE_RECORDED"
            conn.execute(
                "INSERT INTO mrtr_receipt VALUES (?, ?, 'RECORD_ONLY', 'SYNTHETIC_COMPLETE')",
                (token_tag, bound),
            )
            if crash == "before_commit":
                os._exit(35)
            conn.execute("COMMIT")
            if crash == "after_commit":
                os._exit(36)
            return "FIRST_RECORDED"
        except BaseException:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()


def main() -> None:
    p = argparse.ArgumentParser(description="non-authorizing AKDC MRTR receipt fixture")
    p.add_argument("--db", required=True)
    p.add_argument("--nonce", required=True)
    p.add_argument("--principal", required=True)
    p.add_argument("--action", required=True)
    p.add_argument("--operation-digest", required=True)
    p.add_argument("--crash", choices=("before_commit", "after_commit"), default="")
    a = p.parse_args()
    keyhex = os.environ.get("AKDC_RESEARCH_RECEIPT_KEY_HEX", "")
    try:
        key = bytes.fromhex(keyhex)
        store = SQLiteMRTRReceiptResearch(a.db, key)
        result = store.record(
            nonce=a.nonce,
            principal_claim=a.principal,
            action=a.action,
            operation_digest=a.operation_digest,
            crash=a.crash,
        )
        print(json.dumps({"receipt": result, "authority": "NOT_GRANTED", "outcome": "SYNTHETIC_COMPLETE"}))
    except (MRTRReceiptRefusal, ValueError) as exc:
        print(json.dumps({"error": str(exc), "authority": "NOT_GRANTED"}))
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
