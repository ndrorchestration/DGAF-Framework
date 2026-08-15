from pathlib import Path

from evaluations.role_boundary_coherence import TARGET, evaluate


FIXTURE = Path(__file__).parents[1] / "evaluations" / "fixtures" / "role_boundary_coherence_v1.json"


def test_role_boundary_fixture_is_deterministic_and_passes():
    first = evaluate(FIXTURE)
    second = evaluate(FIXTURE)

    assert first["fixture_sha256"] == second["fixture_sha256"]
    assert first["sample_count"] == 10
    assert first["correct_count"] == 10
    assert first["score"] == 1.0
    assert first["target"] == TARGET == 0.95
    assert first["passed"] is True
    assert first["evidence_class"] == "SYNTHETIC"
    assert first["failure_analysis"] == []
    assert all(case["correct"] for case in first["cases"])
