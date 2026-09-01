import json
import os
from pathlib import Path

from scripts.completion_controller import Predicate, evaluate, load_registry, render_report

# In CI, bind exact-candidate tests to the commit actually under test. The
# fallback keeps local unit tests deterministic without pretending to identify
# a repository commit.
CANDIDATE = os.environ.get("GITHUB_SHA", "candidate-under-test")
HISTORICAL_CANDIDATE = "86d839947e9d29d58dabc6a9c91c9ff678f148c6"


def test_stale_verified_evidence_cannot_promote():
    predicates = [
        Predicate(
            id="P3",
            name="artifact contract",
            required=True,
            status="VERIFIED",
            candidate_sha=HISTORICAL_CANDIDATE,
            run_id="123",
            artifact_id="456",
            artifact_sha256="a" * 64,
        )
    ]
    decisions, ok = evaluate(predicates, CANDIDATE)
    p3 = next(d for d in decisions if d.predicate == "P3")
    assert ok is False
    assert p3.promotable is False
    assert "exact candidate" in p3.reason


def test_exact_p3_evidence_promotes_only_p3():
    predicates = [
        Predicate(
            id="P3",
            name="artifact contract",
            required=True,
            status="VERIFIED",
            candidate_sha=CANDIDATE,
            run_id="123",
            artifact_id="456",
            artifact_sha256="b" * 64,
        )
    ]
    report = render_report(
        CANDIDATE,
        predicates,
        {"freeze_authorized": False, "pilot_authorized": False},
        {"schema_version": 1},
    )
    p3 = next(d for d in report["decisions"] if d["predicate"] == "P3")
    assert p3["promotable"] is True
    assert report["required_predicates_verified"] is False
    assert report["freeze_allowed_by_controller"] is False
    assert report["pilot_allowed_by_controller"] is False
    assert report["authorization_is_external"] is True


def test_p6_requires_custody_verification():
    predicates = [
        Predicate(
            id="P6",
            name="durable evidence custody",
            required=True,
            status="VERIFIED",
            candidate_sha=CANDIDATE,
            run_id="123",
            artifact_id="456",
            artifact_sha256="c" * 64,
            custody_verified=False,
        )
    ]
    decisions, ok = evaluate(predicates, CANDIDATE)
    p6 = next(d for d in decisions if d.predicate == "P6")
    assert ok is False
    assert p6.promotable is False
    assert "custody" in p6.reason


def test_verified_artifact_id_requires_digest():
    predicates = [
        Predicate(
            id="P3",
            name="artifact contract",
            required=True,
            status="VERIFIED",
            candidate_sha=CANDIDATE,
            run_id="123",
            artifact_id="456",
        )
    ]
    _, ok = evaluate(predicates, CANDIDATE)
    assert ok is False


def test_registry_candidate_must_match(tmp_path: Path):
    path = tmp_path / "registry.json"
    path.write_text(
        json.dumps({"schema_version": 1, "candidate_sha": "other", "predicates": []}),
        encoding="utf-8",
    )
    try:
        load_registry(path, CANDIDATE)
    except ValueError as exc:
        assert "does not match actual candidate" in str(exc)
    else:
        raise AssertionError("candidate mismatch was accepted")
