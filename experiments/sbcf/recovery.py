"""Conservative read-only consistency gate for synthetic two-store custody.

It NEVER repairs, authorizes production execution or establishes remote trust.
"""
from dataclasses import dataclass
from enum import Enum
import sqlite3


class Disposition(str, Enum):
    CONSISTENT = "CONSISTENT_SYNTHETIC"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class RecoveryCheck:
    disposition: Disposition
    reason: str
    evidence_sequence: int | None
    witness_sequence: int | None


def _counter(path: str, table: str, source: str, run: str) -> int | None:
    # Opening SQLite read-only ensures an absent database is not silently created.
    from pathlib import Path
    p = Path(path).resolve()
    with sqlite3.connect(p.as_uri() + "?mode=ro", uri=True, timeout=3) as db:
        row = db.execute(
            f"SELECT sequence FROM {table} WHERE source=? AND run=?",
            (source, run),
        ).fetchone()
    return None if row is None else row[0]


def reconcile_stores(evidence_path: str, witness_path: str, *, source: str, run: str) -> RecoveryCheck:
    """Fail closed for absent, divergent, corrupt or invalid counters."""
    try:
        a = _counter(evidence_path, "high_water", source, run)
        b = _counter(witness_path, "counters", source, run)
    except (OSError, sqlite3.Error, ValueError) as exc:
        return RecoveryCheck(Disposition.BLOCKED, "STORAGE_UNAVAILABLE_OR_INVALID", None, None)
    if type(a) is not int or type(b) is not int or a < 0 or b < 0:
        return RecoveryCheck(Disposition.BLOCKED, "MISSING_OR_INVALID_COUNTER", a, b)
    if a != b:
        return RecoveryCheck(Disposition.BLOCKED, "COUNTER_MISMATCH", a, b)
    return RecoveryCheck(Disposition.CONSISTENT, "MATCHED_COUNTERS_ONLY", a, b)
