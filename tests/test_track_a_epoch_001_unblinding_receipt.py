from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_track_a_epoch_001_unblinding_receipt.py"
spec = importlib.util.spec_from_file_location("unblinding_receipt_validator", VALIDATOR)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class UnblindingReceiptContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent = "a" * 40
        self.receipt = validator.expected_receipt(self.parent)

    def test_receipt_is_exactly_parent_and_authorization_bound(self) -> None:
        self.assertEqual(self.receipt["receipt_parent_sha"], self.parent)
        self.assertEqual(
            self.receipt["unblinding_authorization_commit_sha"],
            validator.UNBLIND_AUTH_COMMIT_SHA,
        )
        self.assertEqual(
            self.receipt["unblinding_authorization_blob_sha"],
            validator.UNBLIND_AUTH_BLOB_SHA,
        )
        self.assertEqual(self.receipt["dataset_lock_blob_sha"], validator.DATASET_LOCK_BLOB_SHA)

    def test_decryption_identity_is_cryptographically_bound_without_private_key(self) -> None:
        self.assertEqual(
            self.receipt["protected_plaintext_tar_sha256"],
            validator.PROTECTED_PLAINTEXT_TAR_SHA256,
        )
        self.assertEqual(
            self.receipt["private_key_public_key_sha256"],
            self.receipt["custody_certificate_public_key_sha256"],
        )
        self.assertFalse(self.receipt["private_key_published"])
        self.assertFalse(self.receipt["mapping_values_published"])

    def test_mapping_set_identity_and_structure_are_fixed(self) -> None:
        self.assertEqual(self.receipt["mapping_file_count"], 50)
        self.assertEqual(self.receipt["mapping_sidecar_count"], 50)
        self.assertEqual(self.receipt["mapping_seed_first"], 20270101)
        self.assertEqual(self.receipt["mapping_seed_last"], 20270150)
        self.assertEqual(
            self.receipt["mapping_set_manifest_sha256"],
            validator.MAPPING_SET_MANIFEST_SHA256,
        )
        self.assertEqual(self.receipt["mapping_sidecar_qc"], "PASS")
        self.assertEqual(self.receipt["mapping_bijection_qc"], "PASS")
        self.assertEqual(self.receipt["registered_topology_set_qc"], "PASS")

    def test_verification_is_explicitly_nonindependent(self) -> None:
        self.assertEqual(
            self.receipt["verification_class"],
            "DEVELOPER_SAME_SYSTEM_NONINDEPENDENT",
        )
        self.assertEqual(
            self.receipt["protected_custody_class"],
            "PROTECTED_SAME_SYSTEM_NONINDEPENDENT",
        )

    def test_receipt_cannot_authorize_or_run_analysis(self) -> None:
        self.assertTrue(self.receipt["unblinding_complete"])
        self.assertFalse(self.receipt["outcome_mapping_join_performed"])
        self.assertFalse(self.receipt["outcome_values_inspected_for_unblinding_receipt"])
        self.assertFalse(self.receipt["outcome_aggregation_performed"])
        self.assertFalse(self.receipt["primary_analysis_authorized"])
        self.assertFalse(self.receipt["primary_analysis_run"])
        self.assertFalse(self.receipt["historical_pooling_allowed"])
        self.assertFalse(self.receipt["epoch_004_substitution_allowed"])
        self.assertEqual(self.receipt["additional_scientific_n_increment"], 0)
        self.assertFalse(self.receipt["high_assurance_authorized"])
        self.assertEqual(self.receipt["canonical_dgaf_efficacy"], "NOT_ESTABLISHED")


if __name__ == "__main__":
    unittest.main()
