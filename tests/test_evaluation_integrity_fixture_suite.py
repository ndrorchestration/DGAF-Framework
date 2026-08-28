from evaluations.evaluation_integrity_fixture_suite import CASES, THREATS, evaluate, validate_fixture_set


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


def test_invalid_threat_is_rejected() -> None:
    case = CASES[0].__class__("not_a_real_threat", ("x",), False)
    try:
        evaluate([case])
    except ValueError as exc:
        assert "unsupported threat" in str(exc)
    else:
        raise AssertionError("unsupported threat was accepted")
