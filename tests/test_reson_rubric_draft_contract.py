"""Draft-only contract tests for Reson rubric terminology and documented thresholds.

These tests validate the documentation contract, not production seal enforcement,
construct validity, or independent expert review.
"""
from pathlib import Path
import unittest

RUBRIC = Path(__file__).resolve().parents[1] / "docs/agents/reson/QA_RUBRIC.md"
WEIGHTS = (0.30, 0.25, 0.25, 0.20)
FLOOR = 0.85


def composite(scores):
    if len(scores) != 4:
        raise ValueError("Exactly four scores required")
    if any(not isinstance(v, (int, float)) or isinstance(v, bool) or not 0 <= v <= 1 for v in scores):
        raise ValueError("Scores must be finite numbers in [0,1]")
    return sum(w * v for w, v in zip(WEIGHTS, scores))


def seal_eligible(score):
    if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 1:
        return False
    return score >= FLOOR


class ResonDraftContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = RUBRIC.read_text(encoding="utf-8")

    def test_four_names_and_legacy_aliases(self):
        for new, old in (
            ("Structural Distribution Balance", "Phi-Alignment"),
            ("Workflow State Consistency", "Modal Alignment"),
            ("Semantic Consistency and Contradiction Control", "Semantic Coherence"),
            ("Issue Resolution and State Integrity", "Resolution Cadence"),
        ):
            with self.subTest(new=new):
                self.assertIn(new, self.text)
                self.assertIn(old, self.text)

    def test_weights_and_formula_preserved(self):
        self.assertAlmostEqual(sum(WEIGHTS), 1)
        self.assertIn("harmonic_score = (H1 × 0.30) + (H2 × 0.25) + (H3 × 0.25) + (H4 × 0.20)", self.text)
        self.assertAlmostEqual(composite((1, 1, 1, 1)), 1)
        self.assertAlmostEqual(composite((0, 0, 0, 0)), 0)
        self.assertAlmostEqual(composite((1, 0, 0, 0)), 0.30)

    def test_floor_is_preserved_not_redefined(self):
        self.assertRegex(self.text, r"Seal floor:\*\* 0\.85")
        self.assertIn("issue #1559", self.text)

    def test_boundary_examples_fail_closed(self):
        for score in (0.69, 0.70, 0.79, 0.80, 0.84):
            with self.subTest(score=score):
                self.assertFalse(seal_eligible(score))
        for score in (0.85, 0.89, 0.90):
            with self.subTest(score=score):
                self.assertTrue(seal_eligible(score))

    def test_missing_nan_infinite_and_out_of_range_denied(self):
        for value in (None, float("nan"), float("inf"), float("-inf"), -0.01, 1.01, True, "0.9"):
            with self.subTest(value=value):
                self.assertFalse(seal_eligible(value))

    def test_composite_rejects_invalid_inputs(self):
        for scores in ((1, 1, 1), (1, 1, 1, float("nan")), (1, 1, 1, 1.1), (True, 1, 1, 1)):
            with self.subTest(scores=scores):
                with self.assertRaises(ValueError):
                    composite(scores)

    def test_operationalization_protocol_and_known_gaps(self):
        for phrase in ("NOT_SCORED", "Observation unit", "H1 anchors", "H2 anchors", "H3 anchors", "H4 anchors", "noncompensatory", "held-out comparator", "independent blinded raters"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_draft_is_explicitly_non_authorizing(self):
        self.assertIn("v1.1-DRAFT", self.text)
        self.assertIn("not established psychometric validity", self.text)
        self.assertIn("this draft does not resolve it", self.text)


if __name__ == "__main__":
    unittest.main()
