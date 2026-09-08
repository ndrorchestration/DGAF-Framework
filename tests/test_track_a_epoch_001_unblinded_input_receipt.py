from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_track_a_epoch_001_unblinded_input_receipt.py"


class TrackAUnblindedInputReceiptValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = VALIDATOR.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.text)

    def test_validator_is_syntax_valid(self) -> None:
        self.assertIsInstance(self.tree, ast.Module)

    def test_exact_materializer_and_source_identities_are_bound(self) -> None:
        for value in (
            "f92c251bb8fcf068c644db04ae9d2f855c382caa",
            "d4dd3551dda6413ee4d0b195c6d726e17cb2481a",
            "2e1981870a8455abed36fd72dcb3aaa35e2f9bff",
            "32851068cc61421f756041d0671681823b38c054f06e5082ed26c800bf296231",
            "f52d2144cfb8c699347c56cf92a41c1ac11cba98787fefabb56891c9f680c69f",
        ):
            self.assertIn(value, self.text)

    def test_tooling_mode_requires_receipt_absence(self) -> None:
        self.assertIn("--expect-absent", self.text)
        self.assertIn("require(not Path(RECEIPT_REL).exists()", self.text)

    def test_future_event_is_one_parent_one_file_and_unique_history(self) -> None:
        self.assertIn("require(len(parents) == 2", self.text)
        self.assertIn("require(changed == [RECEIPT_REL]", self.text)
        self.assertIn("require(history == [head]", self.text)

    def test_receipt_preserves_analysis_boundary(self) -> None:
        for text in (
            '"primary_analysis_authorized": False',
            '"primary_analysis_run": False',
            '"outcome_aggregation_performed": False',
            '"historical_pooling_allowed": False',
            '"epoch_004_substitution_allowed": False',
            '"high_assurance_authorized": False',
            '"canonical_dgaf_efficacy": "NOT_ESTABLISHED"',
        ):
            self.assertIn(text, self.text)

    def test_receipt_requires_exact_shape_and_durable_retention(self) -> None:
        self.assertIn("require(set(doc) == exact_keys()", self.text)
        self.assertIn('"paired_seed_units": 50', self.text)
        self.assertIn('"record_count": 2250', self.text)
        self.assertIn('"structure_validation": "PASS"', self.text)
        self.assertIn('"durable_retention_id"', self.text)
        self.assertIn('SHA256_RE.fullmatch(doc["materialized_input_sha256"])', self.text)

    def test_private_key_is_not_a_receipt_field(self) -> None:
        self.assertNotIn('"private_key"', self.text)
        self.assertNotIn('"custody_private_key"', self.text)


if __name__ == "__main__":
    unittest.main()
