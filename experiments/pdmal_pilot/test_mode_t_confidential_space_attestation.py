from __future__ import annotations

import copy
import unittest

from mode_t_confidential_space_attestation import (
    AttestationContractError,
    AttestationExpectation,
    VerifiedTokenContext,
    verify_confidential_space_attestation,
)


C_SHA = "1" * 64
MANIFEST_SHA = "2" * 64
TOKEN_SHA = "3" * 64
IMAGE_DIGEST = "sha256:" + ("4" * 64)
NOW = 1_800_000_000


def good_claims() -> dict:
    return {
        "iss": "https://confidentialcomputing.googleapis.com",
        "swname": "CONFIDENTIAL_SPACE",
        "hwmodel": "GCP_INTEL_TDX",
        "dbgstat": "disabled-since-boot",
        "iat": NOW - 30,
        "nbf": NOW - 30,
        "exp": NOW + 300,
        "eat_nonce": [C_SHA, MANIFEST_SHA],
        "submods": {
            "confidential_space": {"support_attributes": ["LATEST", "STABLE", "USABLE"]},
            "container": {
                "image_digest": IMAGE_DIGEST,
                "cmd_override": [],
                "env": {"DGAF_RUN_BINDING": "synthetic-run-310"},
                "env_override": {},
                "restart_policy": "Never",
            },
        },
    }


def expectation() -> AttestationExpectation:
    return AttestationExpectation(
        image_digest=IMAGE_DIGEST,
        authorization_consumption_sha256=C_SHA,
        output_manifest_sha256=MANIFEST_SHA,
        expected_env={"DGAF_RUN_BINDING": "synthetic-run-310"},
    )


def token_context() -> VerifiedTokenContext:
    return VerifiedTokenContext(signature_verified=True, token_sha256=TOKEN_SHA, verified_at_unix=NOW)


class ConfidentialSpaceAttestationContractTests(unittest.TestCase):
    def assert_rejected(self, mutate) -> None:
        claims = good_claims()
        exp = expectation()
        context = token_context()
        claims, exp, context = mutate(claims, exp, context)
        with self.assertRaises(AttestationContractError):
            verify_confidential_space_attestation(claims, exp, context)

    def test_accepts_exact_contract(self) -> None:
        result = verify_confidential_space_attestation(good_claims(), expectation(), token_context())
        self.assertEqual(result["attestation_contract"], "PASS")
        self.assertTrue(result["signature_verified"])
        self.assertFalse(result["freeze_established"])
        self.assertFalse(result["pilot_authorized"])
        self.assertFalse(result["empirical_data_collection"])
        self.assertEqual(result["empirical_n"], 0)

    def test_nonce_order_is_not_semantic(self) -> None:
        claims = good_claims()
        claims["eat_nonce"] = [MANIFEST_SHA, C_SHA]
        result = verify_confidential_space_attestation(claims, expectation(), token_context())
        self.assertEqual(result["attestation_contract"], "PASS")

    def test_rejects_unverified_signature(self) -> None:
        self.assert_rejected(lambda c, e, t: (c, e, VerifiedTokenContext(False, t.token_sha256, t.verified_at_unix)))

    def test_rejects_wrong_issuer(self) -> None:
        def mutate(c, e, t):
            c["iss"] = "https://example.invalid"
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_wrong_software_identity(self) -> None:
        def mutate(c, e, t):
            c["swname"] = "NOT_CONFIDENTIAL_SPACE"
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_wrong_hardware_model(self) -> None:
        def mutate(c, e, t):
            c["hwmodel"] = "GCP_AMD_SEV"
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_debug_image(self) -> None:
        def mutate(c, e, t):
            c["dbgstat"] = "enabled"
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_missing_stable_support(self) -> None:
        def mutate(c, e, t):
            c["submods"]["confidential_space"]["support_attributes"] = ["USABLE"]
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_wrong_image_digest(self) -> None:
        def mutate(c, e, t):
            c["submods"]["container"]["image_digest"] = "sha256:" + ("5" * 64)
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_command_override(self) -> None:
        def mutate(c, e, t):
            c["submods"]["container"]["cmd_override"] = ["/bin/sh"]
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_unexpected_explicit_environment(self) -> None:
        def mutate(c, e, t):
            c["submods"]["container"]["env"]["PDMAL_BLINDING_KEY"] = "forbidden"
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_environment_override(self) -> None:
        def mutate(c, e, t):
            c["submods"]["container"]["env_override"] = {"DGAF_RUN_BINDING": "altered"}
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_restart_policy(self) -> None:
        def mutate(c, e, t):
            c["submods"]["container"]["restart_policy"] = "OnFailure"
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_wrong_consumption_nonce(self) -> None:
        def mutate(c, e, t):
            c["eat_nonce"] = ["6" * 64, MANIFEST_SHA]
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_wrong_manifest_nonce(self) -> None:
        def mutate(c, e, t):
            c["eat_nonce"] = [C_SHA, "7" * 64]
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_duplicate_nonce(self) -> None:
        def mutate(c, e, t):
            c["eat_nonce"] = [C_SHA, C_SHA]
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_missing_nonce(self) -> None:
        def mutate(c, e, t):
            c["eat_nonce"] = [C_SHA]
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_expired_token(self) -> None:
        def mutate(c, e, t):
            c["exp"] = NOW - 120
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_not_yet_valid_token(self) -> None:
        def mutate(c, e, t):
            c["nbf"] = NOW + 120
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_future_issue_time(self) -> None:
        def mutate(c, e, t):
            c["iat"] = NOW + 120
            return c, e, t
        self.assert_rejected(mutate)

    def test_rejects_invalid_token_digest(self) -> None:
        self.assert_rejected(lambda c, e, t: (c, e, VerifiedTokenContext(True, "not-a-digest", t.verified_at_unix)))

    def test_rejects_missing_container_claim_group(self) -> None:
        def mutate(c, e, t):
            del c["submods"]["container"]
            return c, e, t
        self.assert_rejected(mutate)

    def test_input_claims_are_not_mutated(self) -> None:
        claims = good_claims()
        original = copy.deepcopy(claims)
        verify_confidential_space_attestation(claims, expectation(), token_context())
        self.assertEqual(claims, original)


if __name__ == "__main__":
    unittest.main()
