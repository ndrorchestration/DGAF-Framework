"""Synthetic-only ingest-time freshness contract for AOSS Stage A.

This module captures an explicit same-host ingest reference for supplied synthetic
observations and classifies freshness against the frozen Stage-A bounds. It does
not execute ACP, collect study outcomes, or establish collection readiness.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from typing import Callable

MAX_AGE_SECONDS = 30.0
MAX_FUTURE_SKEW_SECONDS = 2.0


class IngestFreshnessError(ValueError):
    """Raised when an ingest reference is malformed or violates the contract."""


@dataclass(frozen=True)
class IngestReference:
    event_time: str
    ingest_time: str
    age_seconds: float
    freshness: str
    max_age_seconds: float = MAX_AGE_SECONDS
    max_future_skew_seconds: float = MAX_FUTURE_SKEW_SECONDS
    status: str = "SYNTHETIC_FIXTURE_NON_COLLECTING"
    collection_execution_readiness: str = "NOT_ESTABLISHED"
    outcomes_generated: bool = False
    scientific_n_increment: int = 0


def _parse_utc(value: str, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise IngestFreshnessError(f"{field} must be a non-empty ISO-8601 string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise IngestFreshnessError(f"{field} is not valid ISO-8601") from exc
    if parsed.tzinfo is None:
        raise IngestFreshnessError(f"{field} must be timezone-aware")
    return parsed.astimezone(timezone.utc)


def _iso_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def classify_freshness(event_time: str, ingest_time: str) -> tuple[str, float]:
    """Return the frozen freshness classification and signed event age."""

    event = _parse_utc(event_time, "event_time")
    ingest = _parse_utc(ingest_time, "ingest_time")
    age = (ingest - event).total_seconds()
    if age < -MAX_FUTURE_SKEW_SECONDS:
        return "FUTURE_SKEWED", age
    if age > MAX_AGE_SECONDS:
        return "STALE", age
    return "FRESH", age


def capture_ingest_reference(
    event_time: str,
    *,
    clock: Callable[[], datetime] | None = None,
) -> IngestReference:
    """Capture one same-process ingest reference for a supplied synthetic event."""

    now = (clock or (lambda: datetime.now(timezone.utc)))()
    if not isinstance(now, datetime) or now.tzinfo is None:
        raise IngestFreshnessError("clock must return a timezone-aware datetime")
    ingest_time = _iso_z(now)
    freshness, age = classify_freshness(event_time, ingest_time)
    return IngestReference(
        event_time=_iso_z(_parse_utc(event_time, "event_time")),
        ingest_time=ingest_time,
        age_seconds=age,
        freshness=freshness,
    )


def canonical_receipt_bytes(reference: IngestReference) -> bytes:
    """Serialize the retained ingest reference deterministically for replay."""

    return (
        json.dumps(asdict(reference), sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def receipt_sha256(reference: IngestReference) -> str:
    return hashlib.sha256(canonical_receipt_bytes(reference)).hexdigest()


def validate_ingest_reference(reference: IngestReference) -> dict[str, object]:
    """Recompute freshness and verify the fail-closed non-collecting boundary."""

    freshness, age = classify_freshness(reference.event_time, reference.ingest_time)
    if reference.freshness != freshness:
        raise IngestFreshnessError("freshness classification drift")
    if abs(reference.age_seconds - age) > 1e-9:
        raise IngestFreshnessError("age_seconds drift")
    if reference.max_age_seconds != MAX_AGE_SECONDS:
        raise IngestFreshnessError("max_age_seconds drift")
    if reference.max_future_skew_seconds != MAX_FUTURE_SKEW_SECONDS:
        raise IngestFreshnessError("max_future_skew_seconds drift")
    if reference.status != "SYNTHETIC_FIXTURE_NON_COLLECTING":
        raise IngestFreshnessError("status boundary drift")
    if reference.collection_execution_readiness != "NOT_ESTABLISHED":
        raise IngestFreshnessError("collection readiness promoted prematurely")
    if reference.outcomes_generated is not False:
        raise IngestFreshnessError("outcome generation promoted prematurely")
    if reference.scientific_n_increment != 0:
        raise IngestFreshnessError("scientific N changed")

    return {
        "ingest_reference": "PASS_SYNTHETIC_NON_COLLECTING",
        "freshness": freshness,
        "receipt_sha256": receipt_sha256(reference),
        "collection_execution_readiness": "NOT_ESTABLISHED",
        "outcomes_generated": False,
        "scientific_n_increment": 0,
    }
