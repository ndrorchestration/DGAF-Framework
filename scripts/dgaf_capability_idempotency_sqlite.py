from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from scripts.dgaf_capability_idempotency import (
    IdempotencyConflict,
    IdempotencyInFlight,
    IdempotencyOutcomeUnknown,
    IdempotencyRecord,
    IdempotencyReplayBlocked,
    IdempotencyState,
)


class SQLiteIdempotencyLedger:
    """Bounded durable reference ledger.

    This implementation demonstrates local persistence and SQLite transaction
    contention semantics. It is not a distributed consensus or production
    idempotency service.
    """

    SCHEMA_VERSION = 1

    def __init__(self, path: str | Path, *, busy_timeout_ms: int = 5000) -> None:
        self.path = Path(path)
        self.busy_timeout_ms = busy_timeout_ms
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.path,
            timeout=self.busy_timeout_ms / 1000,
            isolation_level=None,
        )
        connection.execute(f"PRAGMA busy_timeout={self.busy_timeout_ms}")
        connection.execute("PRAGMA journal_mode=WAL")
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS idempotency_records (
                    key TEXT PRIMARY KEY,
                    action_digest TEXT NOT NULL,
                    state TEXT NOT NULL,
                    result_json TEXT
                )
                """)
            connection.execute(f"PRAGMA user_version={self.SCHEMA_VERSION}")

    @staticmethod
    def _serialize_result(result: Any) -> str:
        return json.dumps(
            result,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )

    @staticmethod
    def _deserialize_result(value: str | None) -> Any | None:
        if value is None:
            return None
        return json.loads(value)

    @staticmethod
    def _record(row: sqlite3.Row) -> IdempotencyRecord:
        return IdempotencyRecord(
            key=row["key"],
            action_digest=row["action_digest"],
            state=IdempotencyState(row["state"]),
            result=SQLiteIdempotencyLedger._deserialize_result(row["result_json"]),
        )

    def _read_locked(
        self,
        connection: sqlite3.Connection,
        key: str,
    ) -> sqlite3.Row | None:
        return connection.execute(
            """
            SELECT key, action_digest, state, result_json
            FROM idempotency_records
            WHERE key = ?
            """,
            (key,),
        ).fetchone()

    def claim(self, key: str, action_digest: str) -> Any | None:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            row = self._read_locked(connection, key)
            if row is None:
                connection.execute(
                    """
                    INSERT INTO idempotency_records
                        (key, action_digest, state, result_json)
                    VALUES (?, ?, ?, NULL)
                    """,
                    (key, action_digest, IdempotencyState.RESERVED.value),
                )
                connection.commit()
                return None

            record = self._record(row)
            if record.action_digest != action_digest:
                raise IdempotencyConflict("idempotency key is already bound to a different action digest")
            if record.state == IdempotencyState.COMPLETED:
                connection.commit()
                return record.result
            if record.state == IdempotencyState.OUTCOME_UNKNOWN:
                raise IdempotencyOutcomeUnknown(
                    "idempotency outcome is unknown; reconciliation is required before retry"
                )
            raise IdempotencyInFlight("idempotency key is already reserved by an in-flight transaction")
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _require_matching(
        self,
        connection: sqlite3.Connection,
        key: str,
        action_digest: str,
    ) -> IdempotencyRecord:
        row = self._read_locked(connection, key)
        if row is None:
            raise IdempotencyReplayBlocked("idempotency key is not reserved")
        record = self._record(row)
        if record.action_digest != action_digest:
            raise IdempotencyConflict("idempotency key is bound to a different action digest")
        return record

    def mark_completed(self, key: str, action_digest: str, result: Any) -> None:
        encoded = self._serialize_result(result)
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            record = self._require_matching(connection, key, action_digest)
            if record.state != IdempotencyState.RESERVED:
                raise IdempotencyReplayBlocked("only a reserved idempotency record may be completed")
            connection.execute(
                """
                UPDATE idempotency_records
                SET state = ?, result_json = ?
                WHERE key = ?
                """,
                (IdempotencyState.COMPLETED.value, encoded, key),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def mark_unknown(self, key: str, action_digest: str) -> None:
        self._transition_reserved(
            key,
            action_digest,
            IdempotencyState.OUTCOME_UNKNOWN,
        )

    def _transition_reserved(
        self,
        key: str,
        action_digest: str,
        target: IdempotencyState,
    ) -> None:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            record = self._require_matching(connection, key, action_digest)
            if record.state != IdempotencyState.RESERVED:
                raise IdempotencyReplayBlocked("only a reserved idempotency record may transition")
            connection.execute(
                """
                UPDATE idempotency_records
                SET state = ?, result_json = NULL
                WHERE key = ?
                """,
                (target.value, key),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def release_denied(self, key: str, action_digest: str) -> None:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            record = self._require_matching(connection, key, action_digest)
            if record.state != IdempotencyState.RESERVED:
                raise IdempotencyReplayBlocked("only a reserved idempotency record may be released after denial")
            connection.execute(
                "DELETE FROM idempotency_records WHERE key = ?",
                (key,),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def reconcile_completed(
        self,
        key: str,
        action_digest: str,
        result: Any,
    ) -> None:
        encoded = self._serialize_result(result)
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            record = self._require_matching(connection, key, action_digest)
            if record.state != IdempotencyState.OUTCOME_UNKNOWN:
                raise IdempotencyReplayBlocked("only an unknown outcome may be reconciled to completed")
            connection.execute(
                """
                UPDATE idempotency_records
                SET state = ?, result_json = ?
                WHERE key = ?
                """,
                (IdempotencyState.COMPLETED.value, encoded, key),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def reconcile_failed(self, key: str, action_digest: str) -> None:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            record = self._require_matching(connection, key, action_digest)
            if record.state != IdempotencyState.OUTCOME_UNKNOWN:
                raise IdempotencyReplayBlocked("only an unknown outcome may be reconciled to failed")
            connection.execute(
                "DELETE FROM idempotency_records WHERE key = ?",
                (key,),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def get(self, key: str) -> IdempotencyRecord | None:
        with self._connect() as connection:
            row = self._read_locked(connection, key)
            if row is None:
                return None
            return self._record(row)
