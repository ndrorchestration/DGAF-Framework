from __future__ import annotations

import copy
import unittest

from mode_t_continuity_acceptance import (
    ContinuityAcceptanceError,
    EXPECTED_CONTINUITY_CLASS,
    EXPECTED_GO_VERSION,
    EXPECTED_HELPER_PATH,
    EXPECTED_PACKET_CLASS,
    EXPECTED_REPOSITORY,
    EXPECTED_RETENTION_CLASS,
    EXPECTED_TLOCK_SOURCE_COMMIT,
    EXPECTED_TLOCK_VERSION,
    validate_structural_acceptance_packet,
)


def packet() -> dict:
    report_sha = "5" * 64
    return {
        "schema_version": 1,
        "evidence_class": EXPECTED_PACKET_CLASS,
        "repository": EXPECTED_REPOSITORY,
        "control_plane_sha": "a" * 40,
        "helper": {
            "path": EXPECTED_HELPER_PATH,
            "source_blob_sha": "b" * 40,
            "source_sha256": "1" * 64,
            "binary_sha256": "2" * 64,
            "tlock_version": EXPECTED_TLOCK_VERSION,
            "tlock_source_commit": EXPECTED_TLOCK_SOURCE_COMMIT,
            "go_version": EXPECTED_GO_VERSION,
            "target_os": "linux",
            "target_arch": "amd64",
            "goamd64": "v1",
            "cgo_enabled": False,
        },
        "continuity_report": {
            "report_sha256": report_sha,
            "schema_version": 1,
            "evidence_class": EXPECTED_CONTINUITY_CLASS,
            "status": "PASS",
            "control_plane_sha": "a" * 40,
            "github_run_id": "34044978034",
            "github_run_attempt": "1",
            "tlock_version": EXPECTED_TLOCK_VERSION,
            "tlock_source_commit": EXPECTED_TLOCK_SOURCE_COMMIT,
            "strict_chain_enforced": True,
            "ciphertext_sha256": "3" * 64,
            "expected_plaintext_sha256": "4" * 64,
            "plaintext_commitment_match": True,
            "plaintext_persisted": False,
            "plaintext_emitted": False,
            "empirical_data_collection": False,
            "freeze_established": False,
            "pilot_authorized": False,
            "empirical_n": 0,
        },
        "retention_retrieval": {
            "evidence_class": EXPECTED_RETENTION_CLASS,
            "retained_report_sha256": report_sha,
            "retrieved_report_sha256": report_sha,
            "retention_receipt_sha256": "6" * 64,
            "retrieval_receipt_sha256": "7" * 64,
            "sigstore_bundle_sha256": "8" * 64,
            "trusted_root_sha256": "9" * 64,
            "retention_location": "independent://synthetic-fixture/not-a-real-archive",
            "retrieval_actor": "synthetic-independent-reader",
            "producer_actor": "synthetic-producer",
            "cryptographic_bundle_verified": True,
            "independent_retrieval_verified": True,
        },
        "adjudication": {
            "status": "NOT_EXECUTED",
            "reviewer_identity": None,
            "record_sha256": None,
            "final_acceptance": False,
        },
        "freeze_established": False,
        "pilot_authorized": False,
        "empirical_n": 0,
    }


class ModeTContinuityAcceptanceTests(unittest.TestCase):
    def test_validates_complete_structural_binding_without_closure(self) -> None:
        result = validate_structural_acceptance_packet(packet())
        self.assertEqual(result["status"], "PASS_STRUCTURAL_BINDING_ONLY")
        self.assertTrue(result["independent_retrieval_digest_match"])
        self.assertEqual(result["final_independent_adjudication"], "NOT_EXECUTED")
        self.assertFalse(result["issue_295_closed"])
        self.assertFalse(result["p4_closed"])
        self.assertFalse(result["freeze_established"])
        self.assertFalse(result["pilot_authorized"])
        self.assertEqual(result["empirical_n"], 0)

    def test_rejects_control_plane_mismatch(self) -> None:
        value = packet()
        value["continuity_report"]["control_plane_sha"] = "c" * 40
        with self.assertRaisesRegex(ContinuityAcceptanceError, "control-plane SHA mismatch"):
            validate_structural_acceptance_packet(value)

    def test_rejects_retained_or_retrieved_digest_mismatch(self) -> None:
        for field in ("retained_report_sha256", "retrieved_report_sha256"):
            value = packet()
            value["retention_retrieval"][field] = "0" * 64
            with self.subTest(field=field), self.assertRaisesRegex(
                ContinuityAcceptanceError,
                "report digest mismatch",
            ):
                validate_structural_acceptance_packet(value)

    def test_rejects_same_producer_and_retrieval_actor(self) -> None:
        value = packet()
        value["retention_retrieval"]["retrieval_actor"] = value["retention_retrieval"][
            "producer_actor"
        ]
        with self.assertRaisesRegex(ContinuityAcceptanceError, "must differ"):
            validate_structural_acceptance_packet(value)

    def test_rejects_missing_crypto_or_independent_retrieval(self) -> None:
        for field in ("cryptographic_bundle_verified", "independent_retrieval_verified"):
            value = packet()
            value["retention_retrieval"][field] = False
            with self.subTest(field=field), self.assertRaises(ContinuityAcceptanceError):
                validate_structural_acceptance_packet(value)

    def test_rejects_helper_or_tool_identity_drift(self) -> None:
        cases = (
            ("path", "other.go"),
            ("tlock_version", "v1.2.1"),
            ("tlock_source_commit", "c" * 40),
            ("go_version", "1.23.0"),
            ("target_arch", "arm64"),
            ("cgo_enabled", True),
        )
        for field, replacement in cases:
            value = packet()
            value["helper"][field] = replacement
            with self.subTest(field=field), self.assertRaises(ContinuityAcceptanceError):
                validate_structural_acceptance_packet(value)

    def test_rejects_secret_surface_or_state_promotion(self) -> None:
        mutations = (
            ("continuity_report", "plaintext_persisted", True),
            ("continuity_report", "plaintext_emitted", True),
            ("continuity_report", "empirical_data_collection", True),
            ("continuity_report", "freeze_established", True),
            ("continuity_report", "pilot_authorized", True),
            ("continuity_report", "empirical_n", 1),
            (None, "freeze_established", True),
            (None, "pilot_authorized", True),
            (None, "empirical_n", 1),
        )
        for section, field, replacement in mutations:
            value = packet()
            target = value if section is None else value[section]
            target[field] = replacement
            with self.subTest(section=section, field=field), self.assertRaises(
                ContinuityAcceptanceError
            ):
                validate_structural_acceptance_packet(value)

    def test_rejects_self_asserted_adjudication(self) -> None:
        for field, replacement in (
            ("status", "PASS"),
            ("reviewer_identity", "self-asserted-reviewer"),
            ("record_sha256", "f" * 64),
            ("final_acceptance", True),
        ):
            value = packet()
            value["adjudication"][field] = replacement
            with self.subTest(field=field), self.assertRaises(ContinuityAcceptanceError):
                validate_structural_acceptance_packet(value)

    def test_rejects_schema_extension_or_omission(self) -> None:
        added = packet()
        added["authority_override"] = True
        with self.assertRaisesRegex(ContinuityAcceptanceError, "keys changed"):
            validate_structural_acceptance_packet(added)

        missing = packet()
        del missing["helper"]["binary_sha256"]
        with self.assertRaisesRegex(ContinuityAcceptanceError, "keys changed"):
            validate_structural_acceptance_packet(missing)

    def test_input_is_not_mutated(self) -> None:
        value = packet()
        before = copy.deepcopy(value)
        validate_structural_acceptance_packet(value)
        self.assertEqual(value, before)


if __name__ == "__main__":
    unittest.main()
