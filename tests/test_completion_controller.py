from scripts.completion_controller import Predicate, evaluate, render_report

CANDIDATE = "de7ad83701c4fcc1052bb31d0a2818e59404414f"


def test_stale_verified_evidence_cannot_promote():
    predicates = [
        Predicate(
            id="P3",
            name="artifact contract",
            required=True,
            status="VERIFIED",
            candidate_sha="historical-sha",
            run_id="123",
            artifact_id="456",
            artifact_sha256="a" * 64,
        )
    ]
    decisions, ok = evaluate(predicates, CANDIDATE)
    assert ok is False
    assert decisions[0].promotable is False
    assert "exact candidate" in decisions[0].reason


def test_exact_evidence_can_promote_predicate_but_not_authorization():
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
    )
    assert report["required_predicates_verified"] is True
    assert report["freeze_allowed_by_controller"] is False
    assert report["pilot_allowed_by_controller"] is False
    assert report["authorization_is_external"] is True


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
