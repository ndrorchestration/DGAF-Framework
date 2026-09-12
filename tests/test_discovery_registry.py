import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from dgaf_discovery.assumptions import (
    AssumptionRecord,
    EvidenceValidityClass,
    assess_expiry,
    validate_assumption,
)
from dgaf_discovery.ledger import BlindSpotRecord, validate_blindspot_record


def test_version_bound_assumption_expires_only_on_declared_trigger():
    assumption = AssumptionRecord(
        assumption_id="ASM-001",
        statement="Validator behavior remains stable for the bound dependency version.",
        evidence_refs=("evidence://validator-v1",),
        validity_class=EvidenceValidityClass.VERSION_BOUND,
        invalidation_triggers=("dependency_version_changed",),
        falsification_test="Re-run the validator contract suite after a version change.",
    )
    validate_assumption(assumption)
    assert assess_expiry(assumption, observed_triggers=set()).expired is False
    result = assess_expiry(assumption, observed_triggers={"dependency_version_changed"})
    assert result.expired is True
    assert result.reasons == ("dependency_version_changed",)


def test_temporal_assumption_requires_and_honors_revalidation_deadline():
    with pytest.raises(ValueError):
        validate_assumption(
            AssumptionRecord(
                assumption_id="ASM-002",
                statement="A time-sensitive external condition remains current.",
                evidence_refs=("evidence://external-check",),
                validity_class=EvidenceValidityClass.TEMPORAL,
                invalidation_triggers=(),
                falsification_test="Repeat the external check.",
            )
        )

    assumption = AssumptionRecord(
        assumption_id="ASM-003",
        statement="A time-sensitive external condition remains current.",
        evidence_refs=("evidence://external-check",),
        validity_class=EvidenceValidityClass.TEMPORAL,
        invalidation_triggers=(),
        falsification_test="Repeat the external check.",
        revalidate_after="2026-09-12T00:00:00+00:00",
    )
    result = assess_expiry(
        assumption,
        observed_triggers=set(),
        now=datetime(2026, 9, 12, 0, 0, 1, tzinfo=timezone.utc),
    )
    assert result.expired is True
    assert result.reasons == ("revalidation_deadline_reached",)


def test_immutable_evidence_does_not_decay_merely_with_time():
    assumption = AssumptionRecord(
        assumption_id="ASM-004",
        statement="A content-addressed artifact digest identifies immutable bytes.",
        evidence_refs=("sha256:abc",),
        validity_class=EvidenceValidityClass.IMMUTABLE,
        invalidation_triggers=(),
        falsification_test="Recompute the digest over the retained bytes.",
    )
    validate_assumption(assumption)
    result = assess_expiry(
        assumption,
        observed_triggers={"time_passed"},
        now=datetime(2036, 1, 1, tzinfo=timezone.utc),
    )
    assert result.expired is False


def test_blindspot_record_is_non_authorizing_and_requires_disjoint_methods():
    record = BlindSpotRecord(
        finding_id="BS-001",
        discovered_by=frozenset({"mutation"}),
        missed_by=frozenset({"static_sweep"}),
        reproduction_evidence=("test://mutation-001",),
        generated_detector="metamorphic:MR-001",
    )
    validate_blindspot_record(record)
    assert record.authoritative_effect == "NONE"
    assert record.review_status == "CANDIDATE"

    with pytest.raises(ValueError):
        validate_blindspot_record(
            BlindSpotRecord(
                finding_id="BS-002",
                discovered_by=frozenset({"mutation"}),
                missed_by=frozenset({"mutation"}),
                reproduction_evidence=("test://mutation-002",),
            )
        )


def test_registry_seed_files_are_non_authorizing_and_non_exhaustive():
    root = Path(__file__).resolve().parents[1]
    assumption_registry = json.loads((root / "docs/governance/ASSUMPTION_REGISTRY_V1.json").read_text())
    blindspot_ledger = json.loads((root / "docs/governance/BLIND_SPOT_LEDGER_V1.json").read_text())
    assert assumption_registry["authoritative_effect"] == "NONE"
    assert assumption_registry["completeness_claim"] is False
    assert assumption_registry["assumptions"] == []
    assert blindspot_ledger["authoritative_effect"] == "NONE"
    assert blindspot_ledger["completeness_claim"] is False
    assert blindspot_ledger["findings"] == []
