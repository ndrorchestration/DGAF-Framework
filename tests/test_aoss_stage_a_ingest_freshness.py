from dataclasses import replace
from datetime import datetime, timezone

import pytest

from scripts.aoss_stage_a.ingest_freshness import (
    IngestFreshnessError,
    canonical_receipt_bytes,
    capture_ingest_reference,
    receipt_sha256,
    validate_ingest_reference,
)


def _clock(value: str):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return lambda: parsed.astimezone(timezone.utc)


def test_capture_records_same_host_ingest_reference_without_collecting():
    reference = capture_ingest_reference(
        "2026-09-21T12:00:00Z",
        clock=_clock("2026-09-21T12:00:05Z"),
    )

    assert reference.freshness == "FRESH"
    assert reference.age_seconds == 5.0
    report = validate_ingest_reference(reference)
    assert report["ingest_reference"] == "PASS_SYNTHETIC_NON_COLLECTING"
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert report["outcomes_generated"] is False
    assert report["scientific_n_increment"] == 0


@pytest.mark.parametrize(
    ("event_time", "ingest_time", "expected"),
    [
        ("2026-09-21T12:00:00Z", "2026-09-21T12:00:30Z", "FRESH"),
        ("2026-09-21T12:00:00Z", "2026-09-21T12:00:30.001Z", "STALE"),
        ("2026-09-21T12:00:02Z", "2026-09-21T12:00:00Z", "FRESH"),
        ("2026-09-21T12:00:02.001Z", "2026-09-21T12:00:00Z", "FUTURE_SKEWED"),
    ],
)
def test_frozen_freshness_boundaries(event_time, ingest_time, expected):
    reference = capture_ingest_reference(event_time, clock=_clock(ingest_time))
    assert reference.freshness == expected
    validate_ingest_reference(reference)


def test_receipt_is_exact_byte_deterministic():
    reference = capture_ingest_reference(
        "2026-09-21T12:00:00Z",
        clock=_clock("2026-09-21T12:00:01Z"),
    )
    first = canonical_receipt_bytes(reference)
    second = canonical_receipt_bytes(reference)

    assert first == second
    assert receipt_sha256(reference) == receipt_sha256(reference)
    assert first.endswith(b"\n")


def test_replay_rejects_freshness_relabeling():
    reference = capture_ingest_reference(
        "2026-09-21T12:00:00Z",
        clock=_clock("2026-09-21T12:01:00Z"),
    )
    tampered = replace(reference, freshness="FRESH")

    with pytest.raises(IngestFreshnessError, match="freshness classification drift"):
        validate_ingest_reference(tampered)


def test_naive_clock_fails_closed():
    with pytest.raises(IngestFreshnessError, match="timezone-aware"):
        capture_ingest_reference(
            "2026-09-21T12:00:00Z",
            clock=lambda: datetime(2026, 9, 21, 12, 0, 0),
        )
