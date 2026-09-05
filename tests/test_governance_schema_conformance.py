from evaluations.governance_schema_conformance import (
    DEFAULT_SCHEMA,
    SEED,
    TARGET,
    build_corpus,
    evaluate,
)


def test_corpus_is_deterministic():
    first = build_corpus(1000)
    second = build_corpus(1000)
    assert first == second
    assert len(first) == 1000
    assert sum(case["expected_valid"] for case in first) == 500


def test_schema_conformance_expected_classification():
    result = evaluate(DEFAULT_SCHEMA, 1000)
    assert result["seed"] == SEED
    assert result["sample_count"] == 1000
    assert result["score"] == 1.0
    assert result["correct_count"] == 1000
    assert result["target"] == TARGET == 0.99
    assert result["passed"] is True
    assert result["evidence_class"] == "SYNTHETIC"
    assert result["failure_analysis"] == []
