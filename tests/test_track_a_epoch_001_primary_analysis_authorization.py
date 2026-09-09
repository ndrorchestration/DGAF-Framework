from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_track_a_epoch_001_primary_analysis_authorization.py"
spec = importlib.util.spec_from_file_location(
    "primary_analysis_authorization_validator", VALIDATOR
)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class PrimaryAnalysisAuthorizationContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent = "a" * 40
        self.receipt_commit = "b" * 40
        self.receipt_blob = "c" * 40
        self.receipt = {
            "materialized_input_sha256": "d" * 64,
            "materialized_input_sidecar_sha256": "e" * 64,
            "durable_retention_type": "LOCAL_CUSTODY_ARCHIVE",
            "durable_retention_id": "track-a-epoch-001-unblinded-input",
        }
        self.auth = validator.expected_authorization(
            self.parent,
            self.receipt_commit,
            self.receipt_blob,
            self.receipt,
        )

    def test_authorization_binds_exact_parent_and_receipt(self) -> None:
        self.assertEqual(self.auth["authorization_parent_sha"], self.parent)
        self.assertEqual(
            self.auth["unblinded_input_receipt_commit_sha"],
            self.receipt_commit,
        )
        self.assertEqual(
            self.auth["unblinded_input_receipt_blob_sha"],
            self.receipt_blob,
        )
        self.assertEqual(
            self.auth["materialized_input_sha256"],
            self.receipt["materialized_input_sha256"],
        )
        self.assertEqual(
            self.auth["durable_retention_id"],
            self.receipt["durable_retention_id"],
        )

    def test_locked_analysis_sources_are_bound(self) -> None:
        self.assertEqual(
            self.auth["preregistration_blob_sha"],
            validator.PREREG_BLOB_SHA,
        )
        self.assertEqual(
            self.auth["analysis_lock_blob_sha"],
            validator.ANALYSIS_LOCK_BLOB_SHA,
        )
        self.assertEqual(self.auth["analysis_blob_sha"], validator.ANALYSIS_BLOB_SHA)
        self.assertEqual(
            self.auth["analysis_config_sha256"],
            validator.ANALYSIS_CONFIG_SHA256,
        )
        self.assertEqual(
            self.auth["requirements_lock_blob_sha"],
            validator.REQUIREMENTS_BLOB_SHA,
        )

    def test_scope_is_locked_primary_analysis_only(self) -> None:
        self.assertEqual(
            self.auth["authorization_scope"],
            "TRACK_A_EPOCH_001_LOCKED_PRIMARY_ANALYSIS_ONLY",
        )
        self.assertTrue(self.auth["primary_analysis_authorized"])
        self.assertFalse(self.auth["primary_analysis_run"])
        self.assertTrue(self.auth["outcome_aggregation_authorized"])
        self.assertEqual(
            self.auth["outcome_aggregation_scope"],
            "LOCKED_PRIMARY_ANALYSIS_ONLY",
        )
        self.assertFalse(self.auth["exploratory_analysis_authorized"])

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
        self.assertEqual(
            self.auth["canonical_dgaf_efficacy"],
            "NOT_ESTABLISHED",
        )
        self.assertFalse(self.auth["high_assurance_authorized"])


if __name__ == "__main__":
    unittest.main()
