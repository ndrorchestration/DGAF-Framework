from pathlib import Path

from evaluations.evaluation_integrity_fixture_suite import (
    CASES,
    THREATS,
    build_report,
    evaluate,
    main,
    validate_fixture_set,
)


def test_fixture_set_covers_declared_threats() -> None:
    validate_fixture_set(CASES)
    assert {case.threat for case in CASES} == set(THREATS)


def test_fixture_suite_is_deterministically_perfect() -> None:
    assert evaluate(CASES) == {
        "cases": 12,
        "correct": 12,
        "incorrect": 0,
        "accuracy": 1.0,
    }


def test_build_report_is_synthetic_and_bounded() -> None:
    report = build_report()
    assert report["evidence_class"] == "SYNTHETIC"
    assert report["case_count"] == 12
    assert report["passed"] is True
    assert report["limitations"]


def test_cli_writes_machine_readable_output(tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "integrity.json"
    monkeypatch.setattr("sys.argv", ["evaluation_integrity_fixture_suite", "--output", str(output)])
    assert main() == 0
    assert output.exists()
    assert '"evaluation": "evaluation_integrity_fixture_suite"' in output.read_text(encoding="utf-8")


def test_invalid_threat_is_rejected() -> None:
    case = CASES[0].__class__("not_a_real_threat", ("x",), False)
    try:
        evaluate([case])
    except ValueError as exc:
        assert "unsupported threat" in str(exc)
    else:
        raise AssertionError("unsupported threat was accepted")
