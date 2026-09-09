from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_track_a_epoch_001_collection_receipt.py"
spec = importlib.util.spec_from_file_location("collection_receipt_validator", VALIDATOR)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class CollectionReceiptContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent = "a" * 40
        self.receipt = validator.expected_receipt(self.parent)

    def test_receipt_is_exactly_parent_bound(self) -> None:
        self.assertEqual(self.receipt["receipt_parent_sha"], self.parent)
        self.assertEqual(self.receipt["authorization_commit_sha"], validator.AUTHORIZATION_COMMIT_SHA)
        self.assertEqual(self.receipt["authorization_blob_sha"], validator.AUTHORIZATION_BLOB_SHA)

    def test_statistical_unit_is_seed_not_raw_trial(self) -> None:
        self.assertEqual(self.receipt["paired_seed_units"], 50)
        self.assertEqual(self.receipt["blinded_observations"], 2250)

    def test_artifact_identities_are_immutable(self) -> None:
        self.assertEqual(self.receipt["public_artifact_id"], 10070586413)
        self.assertEqual(self.receipt["protected_artifact_id"], 10070587302)
        for key in (
            "public_artifact_archive_sha256",
            "protected_artifact_archive_sha256",
            "protected_ciphertext_sha256",
            "protected_plaintext_tar_sha256",
            "custody_certificate_sha256",
        ):
            value = self.receipt[key]
            self.assertEqual(len(value), 64)
            int(value, 16)

    def test_receipt_cannot_promote_analysis_or_unblinding(self) -> None:
        self.assertFalse(self.receipt["outcome_values_inspected_for_receipt"])
        self.assertFalse(self.receipt["outcome_aggregation_performed"])
        self.assertFalse(self.receipt["primary_analysis_run"])
        self.assertFalse(self.receipt["unblinding_authorized"])
        self.assertFalse(self.receipt["historical_pooling_allowed"])
        self.assertFalse(self.receipt["epoch_004_substitution_allowed"])
        self.assertFalse(self.receipt["high_assurance_authorized"])
        self.assertEqual(self.receipt["canonical_dgaf_efficacy"], "NOT_ESTABLISHED")

    def test_custody_is_explicitly_nonindependent(self) -> None:
        self.assertEqual(self.receipt["custody_class"], "DEVELOPER_SAME_SYSTEM_NONINDEPENDENT")
        self.assertFalse(self.receipt["independent_custody"])
        self.assertFalse(self.receipt["private_key_published"])
        self.assertTrue(self.receipt["analysis_label_blinding_preserved"])


if __name__ == "__main__":
    unittest.main()
