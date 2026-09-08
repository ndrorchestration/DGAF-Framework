from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_track_a_epoch_001_collection_authorization.py"

spec = importlib.util.spec_from_file_location("authorization_validator", VALIDATOR)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

PARENT = "a" * 40


class CollectionAuthorizationValidatorTests(unittest.TestCase):
    def test_exact_record_accepts(self) -> None:
        validator.validate_authorization_record(
            copy.deepcopy(validator.expected_authorization(PARENT)),
            PARENT,
        )

    def test_missing_field_fails_closed(self) -> None:
        record = copy.deepcopy(validator.expected_authorization(PARENT))
        record.pop("authorize_empirical_collection")
        with self.assertRaises(SystemExit):
            validator.validate_authorization_record(record, PARENT)

    def test_extra_field_fails_closed(self) -> None:
        record = copy.deepcopy(validator.expected_authorization(PARENT))
        record["scientific_n_increment"] = 1
        with self.assertRaises(SystemExit):
            validator.validate_authorization_record(record, PARENT)

    def test_mutations_fail_closed(self) -> None:
        mutations = {
            "record_type": "OTHER",
            "schema_version": 1,
            "protocol_id": "OTHER",
            "epoch_id": "TRACK_A_EPOCH_004",
            "authorization_parent_sha": "0" * 40,
            "frozen_candidate_sha": "0" * 40,
            "frozen_candidate_tree_sha": "0" * 40,
            "preflight_blob_sha": "0" * 40,
            "freeze_manifest_blob_sha": "0" * 40,
            "closure_packet_blob_sha": "0" * 40,
            "verification_classification_blob_sha": "0" * 40,
            "preregistration_merge_sha": "0" * 40,
            "analysis_lock_merge_sha": "0" * 40,
            "analysis_blob_sha": "0" * 40,
            "analysis_config_sha256": "0" * 64,
            "requirements_lock_blob_sha": "0" * 40,
            "algorithm_id": "OTHER",
            "seed_start": 20270100,
            "seed_end": 20270151,
            "seed_count": 49,
            "expected_observations": 2249,
            "authorize_empirical_collection": False,
            "authorize_unblinding": True,
            "historical_pooling_allowed": True,
            "epoch_004_substitution_allowed": True,
            "high_assurance_authorized": True,
        }
        for key, value in mutations.items():
            with self.subTest(key=key):
                record = copy.deepcopy(validator.expected_authorization(PARENT))
                record[key] = value
                with self.assertRaises(SystemExit):
                    validator.validate_authorization_record(record, PARENT)

    def test_parent_binding_is_dynamic_and_exact(self) -> None:
        first = validator.expected_authorization(PARENT)
        other_parent = "b" * 40
        second = validator.expected_authorization(other_parent)
        self.assertEqual(first["authorization_parent_sha"], PARENT)
        self.assertEqual(second["authorization_parent_sha"], other_parent)
        self.assertNotEqual(first, second)

    def test_verification_identity_is_exact(self) -> None:
        self.assertEqual(
            validator.VERIFICATION_BLOB_SHA,
            "c67d09052faa7ae50de6eca57691ed50d906a951",
        )
        self.assertEqual(
            validator.EXPECTED_VERIFICATION["verification_class"],
            "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT",
        )
        self.assertIs(validator.EXPECTED_VERIFICATION["independent_verification"], False)
        self.assertIs(validator.EXPECTED_VERIFICATION["same_system_custody"], True)

    def test_authorization_scope_is_exact(self) -> None:
        record = validator.expected_authorization(PARENT)
        self.assertIs(record["authorize_empirical_collection"], True)
        self.assertIs(record["authorize_unblinding"], False)
        self.assertIs(record["historical_pooling_allowed"], False)
        self.assertIs(record["epoch_004_substitution_allowed"], False)
        self.assertIs(record["high_assurance_authorized"], False)
        self.assertNotIn("scientific_n_increment", record)

    def test_panel_and_analysis_lock_are_exact(self) -> None:
        record = validator.expected_authorization(PARENT)
        self.assertEqual(record["seed_start"], 20270101)
        self.assertEqual(record["seed_end"], 20270150)
        self.assertEqual(record["seed_count"], 50)
        self.assertEqual(record["expected_observations"], 2250)
        self.assertEqual(record["algorithm_id"], "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1")
        self.assertEqual(
            record["analysis_config_sha256"],
            "355b164f69e91405819f092d0721b7597b87b06de79394a0c451169410a5ab6d",
        )

    def test_protected_source_set_is_exact(self) -> None:
        self.assertEqual(len(validator.EXPECTED_PROTECTED_SOURCE_BLOBS), 8)
        self.assertEqual(
            validator.EXPECTED_PROTECTED_SOURCE_BLOBS["experiments/pdmal_pilot/run_track_a_epoch_001.py"],
            "d8ef6f31f49da82e4eaf5295bad024c3194f6d15",
        )


if __name__ == "__main__":
    unittest.main()
