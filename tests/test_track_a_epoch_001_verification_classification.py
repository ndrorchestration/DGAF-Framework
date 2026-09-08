from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_track_a_epoch_001_verification_classification.py"

spec = importlib.util.spec_from_file_location("verification_validator", VALIDATOR)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class VerificationClassificationValidatorTests(unittest.TestCase):
    def test_exact_record_accepts(self) -> None:
        validator.validate_verification_record(copy.deepcopy(validator.EXPECTED_VERIFICATION))

    def test_missing_field_fails_closed(self) -> None:
        record = copy.deepcopy(validator.EXPECTED_VERIFICATION)
        record.pop("verification_class")
        with self.assertRaises(SystemExit):
            validator.validate_verification_record(record)

    def test_extra_field_fails_closed(self) -> None:
        record = copy.deepcopy(validator.EXPECTED_VERIFICATION)
        record["external_review"] = True
        with self.assertRaises(SystemExit):
            validator.validate_verification_record(record)

    def test_mutations_fail_closed(self) -> None:
        mutations = {
            "record_type": "OTHER",
            "schema_version": 2,
            "protocol_id": "OTHER",
            "frozen_candidate_sha": "0" * 40,
            "closure_packet_blob_sha": "0" * 40,
            "verification_status": "FAIL",
            "verification_class": "INDEPENDENT_EXTERNAL",
            "independent_verification": True,
            "same_system_custody": False,
            "scientific_n_increment": 1,
            "collection_authorized": True,
            "unblinding_authorized": True,
            "high_assurance_authorized": True,
        }
        for key, value in mutations.items():
            with self.subTest(key=key):
                record = copy.deepcopy(validator.EXPECTED_VERIFICATION)
                record[key] = value
                with self.assertRaises(SystemExit):
                    validator.validate_verification_record(record)

    def test_closure_identity_is_exact(self) -> None:
        self.assertEqual(
            validator.CLOSURE_PACKET_BLOB_SHA,
            "c32d89385c29c9e5cd0a706630c1955fb3f5f1c8",
        )
        self.assertEqual(
            validator.EXPECTED_VERIFICATION["closure_packet_blob_sha"],
            validator.CLOSURE_PACKET_BLOB_SHA,
        )

    def test_verification_is_explicitly_nonindependent(self) -> None:
        record = validator.EXPECTED_VERIFICATION
        self.assertEqual(record["verification_status"], "PASS")
        self.assertEqual(
            record["verification_class"], "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
        )
        self.assertIs(record["independent_verification"], False)
        self.assertIs(record["same_system_custody"], True)

    def test_verification_remains_non_authorizing(self) -> None:
        record = validator.EXPECTED_VERIFICATION
        self.assertEqual(record["scientific_n_increment"], 0)
        self.assertIs(record["collection_authorized"], False)
        self.assertIs(record["unblinding_authorized"], False)
        self.assertIs(record["high_assurance_authorized"], False)

    def test_protected_source_set_is_exact(self) -> None:
        self.assertEqual(len(validator.EXPECTED_PROTECTED_SOURCE_BLOBS), 8)
        self.assertEqual(
            validator.EXPECTED_PROTECTED_SOURCE_BLOBS[
                "experiments/pdmal_pilot/run_track_a_epoch_001.py"
            ],
            "d8ef6f31f49da82e4eaf5295bad024c3194f6d15",
        )


if __name__ == "__main__":
    unittest.main()
