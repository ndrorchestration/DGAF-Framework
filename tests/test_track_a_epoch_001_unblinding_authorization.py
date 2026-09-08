from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_track_a_epoch_001_unblinding_authorization.py"
spec = importlib.util.spec_from_file_location("unblinding_authorization_validator", VALIDATOR)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class UnblindingAuthorizationContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent = "a" * 40
        self.auth = validator.expected_authorization(self.parent)

    def test_authorization_is_exactly_parent_bound(self) -> None:
        self.assertEqual(self.auth["authorization_parent_sha"], self.parent)
        self.assertEqual(self.auth["dataset_lock_commit_sha"], validator.DATASET_LOCK_COMMIT_SHA)
        self.assertEqual(self.auth["dataset_lock_blob_sha"], validator.DATASET_LOCK_BLOB_SHA)

    def test_locked_scientific_sources_are_bound(self) -> None:
        self.assertEqual(self.auth["preregistration_blob_sha"], validator.PREREG_BLOB_SHA)
        self.assertEqual(self.auth["analysis_lock_blob_sha"], validator.ANALYSIS_LOCK_BLOB_SHA)
        self.assertEqual(self.auth["analysis_blob_sha"], validator.ANALYSIS_BLOB_SHA)
        self.assertEqual(self.auth["requirements_lock_blob_sha"], validator.REQUIREMENTS_BLOB_SHA)

    def test_scope_is_mapping_release_only(self) -> None:
        self.assertEqual(
            self.auth["authorization_scope"],
            "TRACK_A_EPOCH_001_MAPPING_RELEASE_ONLY",
        )
        self.assertTrue(self.auth["key_release_authorized"])
        self.assertTrue(self.auth["protected_artifact_decryption_authorized"])
        self.assertTrue(self.auth["unblinding_authorized"])
        self.assertFalse(self.auth["primary_analysis_authorized"])
        self.assertFalse(self.auth["outcome_aggregation_authorized"])
        self.assertFalse(self.auth["primary_analysis_run"])

    def test_authorization_is_explicitly_nonindependent(self) -> None:
        self.assertEqual(
            self.auth["authorization_class"],
            "HUMAN_REPOSITORY_OWNER_SAME_SYSTEM_NONINDEPENDENT",
        )
        self.assertFalse(self.auth["independent_authorization"])

    def test_no_claim_or_sample_promotion(self) -> None:
        self.assertFalse(self.auth["historical_pooling_allowed"])
        self.assertFalse(self.auth["epoch_004_substitution_allowed"])
        self.assertEqual(self.auth["additional_scientific_n_increment"], 0)
        self.assertFalse(self.auth["high_assurance_authorized"])
        self.assertEqual(self.auth["canonical_dgaf_efficacy"], "NOT_ESTABLISHED")


if __name__ == "__main__":
    unittest.main()
