from __future__ import annotations

import copy
import unittest

from mode_t_retention_contract import (
    EXPECTED_OIDC_ISSUER,
    RetentionContractError,
    TransparencyExpectation,
    VerifiedTransparencyContext,
    verify_analysis_lock_temporal_order,
    verify_transparency_inclusion,
)

RECORD_SHA = "1" * 64
BUNDLE_SHA = "2" * 64
IDENTITY = "https://github.com/ndrorchestration/DGAF-Framework/.github/workflows/p4-mode-t-transparency.yml@refs/heads/main"


def expectation(record_type: str = "PDMAL_MODE_T_AUTHORIZATION_CONSUMPTION") -> TransparencyExpectation:
    return TransparencyExpectation(
        record_type=record_type,
        record_sha256=RECORD_SHA,
        certificate_identity=IDENTITY,
    )


def context() -> VerifiedTransparencyContext:
    return VerifiedTransparencyContext(
        signature_verified=True,
        certificate_chain_verified=True,
        certificate_identity_verified=True,
        transparency_inclusion_verified=True,
        signed_entry_timestamp_verified=True,
        bundle_sha256=BUNDLE_SHA,
        log_id_key_id="synthetic-log-key-id",
        log_index=310,
        integrated_time_unix=1_800_000_000,
        verified_record_sha256=RECORD_SHA,
        certificate_identity=IDENTITY,
        oidc_issuer=EXPECTED_OIDC_ISSUER,
    )


class ModeTRetentionContractTests(unittest.TestCase):
    def test_accepts_normalized_inclusion_without_temporal_promotion(self) -> None:
        result = verify_transparency_inclusion(expectation(), context())
        self.assertEqual(result["retention_contract"], "PASS_NORMALIZED_INCLUSION_ONLY")
        self.assertEqual(result["anti_deletion_inclusion_evidence"], "VERIFIED_NORMALIZED")
        self.assertEqual(result["log_id_key_id"], "synthetic-log-key-id")
        self.assertFalse(result["temporal_order_verified"])
        self.assertFalse(result["external_sigstore_crypto_performed_by_this_module"])
        self.assertFalse(result["real_external_retention_established"])
        self.assertFalse(result["pilot_authorized"])
        self.assertEqual(result["empirical_n"], 0)

    def test_integrated_time_is_retained_only_as_metadata(self) -> None:
        result = verify_transparency_inclusion(expectation(), context())
        self.assertEqual(result["integrated_time_unix_metadata_only"], 1_800_000_000)
        self.assertIn("NOT_ACCEPTED_AS_INDEPENDENT_TIME_AUTHORITY", result["temporal_order_reason"])

    def test_analysis_lock_inclusion_does_not_prove_before_release(self) -> None:
        inclusion = verify_transparency_inclusion(
            expectation("PDMAL_P4_T_ANALYSIS_LOCK"), context()
        )
        result = verify_analysis_lock_temporal_order(inclusion)
        self.assertTrue(result["analysis_lock_inclusion_verified"])
        self.assertFalse(result["temporal_order_verified"])
        self.assertEqual(result["temporal_order_status"], "OPEN")
        self.assertFalse(result["rekor_integrated_time_promoted"])

    def test_rejects_attempt_to_supply_unapproved_time_authority(self) -> None:
        inclusion = verify_transparency_inclusion(
            expectation("PDMAL_P4_T_ANALYSIS_LOCK"), context()
        )
        with self.assertRaisesRegex(RetentionContractError, "no independent temporal-order authority"):
            verify_analysis_lock_temporal_order(
                inclusion,
                independent_time_order_evidence={"before_release": True},
            )

    def test_rejects_unverified_inclusion(self) -> None:
        bad = copy.copy(context())
        bad = VerifiedTransparencyContext(
            **{**bad.__dict__, "transparency_inclusion_verified": False}
        )
        with self.assertRaises(RetentionContractError):
            verify_transparency_inclusion(expectation(), bad)

    def test_rejects_unverified_signature_or_chain_or_identity(self) -> None:
        for field in (
            "signature_verified",
            "certificate_chain_verified",
            "certificate_identity_verified",
            "signed_entry_timestamp_verified",
        ):
            data = dict(context().__dict__)
            data[field] = False
            with self.subTest(field=field), self.assertRaises(RetentionContractError):
                verify_transparency_inclusion(
                    expectation(), VerifiedTransparencyContext(**data)
                )

    def test_rejects_record_digest_mismatch(self) -> None:
        data = dict(context().__dict__)
        data["verified_record_sha256"] = "9" * 64
        with self.assertRaisesRegex(RetentionContractError, "record digest mismatch"):
            verify_transparency_inclusion(
                expectation(), VerifiedTransparencyContext(**data)
            )

    def test_rejects_certificate_identity_mismatch(self) -> None:
        data = dict(context().__dict__)
        data["certificate_identity"] = "https://github.com/example/other/.github/workflows/x.yml@refs/heads/main"
        with self.assertRaisesRegex(RetentionContractError, "certificate identity mismatch"):
            verify_transparency_inclusion(
                expectation(), VerifiedTransparencyContext(**data)
            )

    def test_rejects_wrong_oidc_issuer(self) -> None:
        data = dict(context().__dict__)
        data["oidc_issuer"] = "https://example.invalid"
        with self.assertRaisesRegex(RetentionContractError, "OIDC issuer mismatch"):
            verify_transparency_inclusion(
                expectation(), VerifiedTransparencyContext(**data)
            )

    def test_rejects_unsupported_record_type(self) -> None:
        with self.assertRaisesRegex(RetentionContractError, "unsupported"):
            verify_transparency_inclusion(expectation("UNREVIEWED_RECORD"), context())

    def test_temporal_checker_rejects_non_analysis_lock_record(self) -> None:
        inclusion = verify_transparency_inclusion(expectation(), context())
        with self.assertRaisesRegex(RetentionContractError, "analysis-lock record"):
            verify_analysis_lock_temporal_order(inclusion)


if __name__ == "__main__":
    unittest.main()
