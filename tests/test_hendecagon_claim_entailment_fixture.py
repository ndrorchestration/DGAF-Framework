"""Check only deterministic reference facts for the proposed H11 research fixture.

These tests are not model evaluations or independent claim adjudication.
"""

import json
from math import gcd, pi, sin
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "docs" / "research" / "fixtures" / "hendecagon_claim_entailment.v0.1.json"

EXPECTED = {
    "H11-01": "RETAIN",
    "H11-02": "RETAIN",
    "H11-03": "RETAIN",
    "H11-04": "REJECT",
    "H11-05": "REJECT",
    "H11-06": "WITHHOLD",
    "H11-07": "REJECT",
    "H11-08": "WITHHOLD",
    "H11-09": "REJECT",
    "H11-10": "RETAIN",
}


def _discriminant(a, b, c, d):
    """Discriminant of a*x**3 + b*x**2 + c*x + d."""
    return b * b * c * c - 4 * a * c**3 - 4 * b**3 * d - 27 * a * a * d * d + 18 * a * b * c * d


def test_fixture_has_provisional_labels_and_resolved_source_ids():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert fixture["status"] == "DESIGN_ONLY_UNREVIEWED_NO_MODEL_EVALUATION"
    assert fixture["scientific_n_increment"] == 0
    assert fixture["independent_validation"] == "NOT_ESTABLISHED"
    assert fixture["dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert "NOT_INDEPENDENT_GOLD" in fixture["label_authority"]
    source_ids = {source["id"] for source in fixture["sources"]}
    assert source_ids == {"S1", "S2", "S3"}
    cases = fixture["cases"]
    assert len(cases) == len(EXPECTED)
    assert {case["id"] for case in cases} == set(EXPECTED)
    for case in cases:
        assert case["proposed_disposition"] == EXPECTED[case["id"]]
        assert case["claim"] and case["reason"]
        assert case["source_ids"]
        assert set(case["source_ids"]) <= source_ids


def test_regular_hendecagon_circumradius_display():
    radius = 1.0 / (2.0 * sin(pi / 11.0))
    assert format(radius, ".10f") == "1.7747327664"
    cubic_at_radius = 25 * radius**3 - 40 * radius**2 + 21 * radius - 2
    assert abs(cubic_at_radius) > 40


def test_modular_factorization_does_not_imply_real_repeated_root():
    # Coefficients are ordered from constant term through cubic term.
    cubic_coefficients = (-2, 21, -40, 25)
    factor_coefficients = (9, 21, 15, 3)
    assert tuple(x % 11 for x in cubic_coefficients) == tuple(x % 11 for x in factor_coefficients)
    assert _discriminant(25, -40, 21, -2) == -44000
    assert -44000 % 11 == 0
    assert -44000 != 0


def test_distinct_cubics_and_finite_field_power_map():
    assert _discriminant(1, 2, 2, 2) == -44
    assert _discriminant(25, -40, 21, -2) == -44000
    assert gcd(3, 10) == 1
    assert len({pow(x, 3, 11) for x in range(11)}) == 11
