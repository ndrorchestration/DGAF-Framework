from __future__ import annotations

import copy
import unittest

from mode_t_confidential_space_attestation import (
    AttestationContractError,
    AttestationExpectation,
    POST_EXECUTION,
    PRE_EXECUTION,
    VerifiedTokenContext,
    verify_confidential_space_attestation,
    verify_two_phase_attestation_binding,
)


C_SHA = "1" * 64
MANIFEST_SHA = "2" * 64
PRE_TOKEN_SHA = "3" * 64
POST_TOKEN_SHA = "8" * 64
IMAGE_DIGEST = "sha256:" + ("4" * 64)
AUDIENCE = "dgaf-mode-t-admission-v1"
CONTAINER_ARGS = ("/app/dgaf-mode-t",)
NOW = 1_800_000_000


def good_claims(*, binding_sha256: str = C_SHA, issued_at: int = NOW - 30) -> dict:
    return {
        "iss": "https://confidentialcomputing.googleapis.com",
        "aud": AUDIENCE,
        "swname": "CONFIDENTIAL_SPACE",
        "hwmodel": "GCP_INTEL_TDX",
        "attester_tcb": ["INTEL"],
        "secboot": True,
        "dbgstat": "disabled-since-boot",
        "iat": issued_at,
        "nbf": issued_at,
        "exp": NOW + 300,
        "eat_nonce": [binding_sha256],
        "submods": {
            "confidential_space": {
                "support_attributes": ["LATEST", "STABLE", "USABLE"],
                "monitoring_enabled": {"memory": False},
            },
            "container": {
                "image_digest": IMAGE_DIGEST,
                "args": list(CONTAINER_ARGS),
                "cmd_override": [],
                "env": {"DGAF_RUN_BINDING": "synthetic-run-310"},
                "env_override": {},
                "restart_policy": "Never",
            },
        },
    }


def expectation(
    *,
    phase: str = PRE_EXECUTION,
    binding_sha256: str = C_SHA,
    expected_args: tuple[str, ...] = CONTAINER_ARGS,
) -> AttestationExpectation:
    return AttestationExpectation(
        phase=phase,
        audience=AUDIENCE,
        image_digest=IMAGE_DIGEST,
        binding_sha256=binding_sha256,
        expected_args=expected_args,
        expected_env={"DGAF_RUN_BINDING": "synthetic-run-310"},
    )


def token_context(
    *,
    token_sha256: str = PRE_TOKEN_SHA,
    verified_at: int = NOW,
) -> VerifiedTokenContext:
    return VerifiedTokenContext(
        signature_verified=True,
        token_sha256=token_sha256,
        verified_at_unix=verified_at,
    )


def pre_result() -> dict:
    return verify_confidential_space_attestation(
        good_claims(binding_sha256=C_SHA, issued_at=NOW - 30),
        expectation(phase=PRE_EXECUTION, binding_sha256=C_SHA),
        token_context(token_sha256=PRE_TOKEN_SHA, verified_at=NOW),
    )


def post_result() -> dict:
    return verify_confidential_space_attestation(
        good_claims(binding_sha256=MANIFEST_SHA, issued_at=NOW + 10),
        expectation(phase=POST_EXECUTION, binding_sha256=MANIFEST_SHA),
        token_context(token_sha256=POST_TOKEN_SHA, verified_at=NOW + 20),
    )


class ConfidentialSpaceAttestationContractTests(unittest.TestCase):
    def assert_rejected(self, mutate) -> None:
        claims = good_claims()
        exp = expectation()
        context = token_context()
        claims, exp, context = mutate(claims, exp, context)
        with self.assertRaises(AttestationContractError):
            verify_confidential_space_attestation(claims, exp, context)

    def test_accepts_exact_pre_execution_contract(self) -> None:
        result = pre_result()
        self.assertEqual(result["attestation_contract"], "PASS")
        self.assertEqual(result["attestation_phase"], PRE_EXECUTION)
        self.assertEqual(result["authorization_consumption_sha256"], C_SHA)
        self.assertIsNone(result["output_manifest_sha256"])
        self.assertTrue(result["signature_verified"])
        self.assertFalse(result["freeze_established"])
        self.assertFalse(result["pilot_authorized"])
        self.assertFalse(result["empirical_data_collection"])
        self.assertEqual(result["empirical_n"], 0)

    def test_accepts_exact_post_execution_contract(self) -> None:
        result = post_result()
        self.assertEqual(result["attestation_contract"], "PASS")
        self.assertEqual(result["attestation_phase"], POST_EXECUTION)
        self.assertIsNone(result["authorization_consumption_sha256"])
        self.assertEqual(result["output_manifest_sha256"], MANIFEST_SHA)

    def test_two_phase_binding_accepts_same_runtime_lineage(self) -> None:
        result = verify_two_phase_attestation_binding(
            pre_result(),
            post_result(),
            authorization_consumption_sha256=C_SHA,
            output_manifest_sha256=MANIFEST_SHA,
        )
        self.assertEqual(result["two_phase_attestation_binding"], "PASS")
        self.assertEqual(result["authorization_consumption_sha256"], C_SHA)
        self.assertEqual(result["output_manifest_sha256"], MANIFEST_SHA)
        self.assertFalse(result["pilot_authorized"])
        self.assertEqual(result["empirical_n"], 0)

    def test_rejects_circular_two_nonce_pre_execution_request(self) -> None:
        def mutate(c, e, t):
            c["eat_nonce"] = [C_SHA, MANIFEST_SHA]
            return c, e, t

        self.assert_rejected(mutate)

    def test_rejects_unknown_phase(self) -> None:
        def mutate(c, e, t):
            e = AttestationExpectation(
                phase="UNKNOWN",
                audience=e.audience,
                image_digest=e.image_digest,
                binding_sha256=e.binding_sha256,
                expected_args=e.expected_args,
                expected_env=e.expected_env,
            )
            return c, e, t

        self.assert_rejected(mutate)

    def test_rejects_unverified_signature(self) -> None:
        self.assert_rejected(
            lambda c, e, t: (
                c,
                e,
                VerifiedTokenContext(False, t.token_sha256, t.verified_at_unix),
            )
        )

    def test_rejects_wrong_issuer(self) -> None:
        def mutate(c, e, t):
            c["iss"] = "https://example.invalid"
            return c, e, t

        self.assert_rejected(mutate)

    def test_rejects_wrong_audience(self) -> None:
        def mutate(c, e, t):
            c["aud"] = "wrong-audience"
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

    def test_rejects_wrong_attester_tcb(self) -> None:
        def mutate(c, e, t):
            c["attester_tcb"] = ["AMD"]
            return c, e, t

        self.assert_rejected(mutate)

    def test_rejects_secure_boot_false(self) -> None:
        def mutate(c, e, t):
            c["secboot"] = False
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

    def test_rejects_memory_monitoring_enabled(self) -> None:
        def mutate(c, e, t):
            c["submods"]["confidential_space"]["monitoring_enabled"] = {
                "memory": True,
            }
            return c, e, t

        self.assert_rejected(mutate)

    def test_rejects_wrong_image_digest(self) -> None:
        def mutate(c, e, t):
            c["submods"]["container"]["image_digest"] = "sha256:" + ("5" * 64)
            return c, e, t

        self.assert_rejected(mutate)

    def test_rejects_wrong_container_args(self) -> None:
        def mutate(c, e, t):
            c["submods"]["container"]["args"] = ["/bin/sh"]
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
            c["submods"]["container"]["env_override"] = {
                "DGAF_RUN_BINDING": "altered",
            }
            return c, e, t

        self.assert_rejected(mutate)

    def test_rejects_restart_policy(self) -> None:
        def mutate(c, e, t):
            c["submods"]["container"]["restart_policy"] = "OnFailure"
            return c, e, t

        self.assert_rejected(mutate)

    def test_rejects_wrong_phase_binding_nonce(self) -> None:
        def mutate(c, e, t):
            c["eat_nonce"] = [MANIFEST_SHA]
            return c, e, t

        self.assert_rejected(mutate)

    def test_rejects_missing_nonce(self) -> None:
        def mutate(c, e, t):
            c["eat_nonce"] = []
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
        self.assert_rejected(
            lambda c, e, t: (
                c,
                e,
                VerifiedTokenContext(True, "not-a-digest", t.verified_at_unix),
            )
        )

    def test_rejects_missing_container_claim_group(self) -> None:
        def mutate(c, e, t):
            del c["submods"]["container"]
            return c, e, t

        self.assert_rejected(mutate)

    def test_pair_rejects_runtime_identity_drift(self) -> None:
        post = post_result()
        post["runtime_identity_sha256"] = "9" * 64
        with self.assertRaises(AttestationContractError, msg="runtime identity"):
            verify_two_phase_attestation_binding(
                pre_result(),
                post,
                authorization_consumption_sha256=C_SHA,
                output_manifest_sha256=MANIFEST_SHA,
            )

    def test_pair_rejects_same_token_replay(self) -> None:
        post = post_result()
        post["token_sha256"] = PRE_TOKEN_SHA
        with self.assertRaises(AttestationContractError, msg="distinct"):
            verify_two_phase_attestation_binding(
                pre_result(),
                post,
                authorization_consumption_sha256=C_SHA,
                output_manifest_sha256=MANIFEST_SHA,
            )

    def test_pair_rejects_reversed_phases(self) -> None:
        with self.assertRaises(AttestationContractError, msg="PRE_EXECUTION"):
            verify_two_phase_attestation_binding(
                post_result(),
                pre_result(),
                authorization_consumption_sha256=C_SHA,
                output_manifest_sha256=MANIFEST_SHA,
            )

    def test_pair_rejects_post_token_that_predates_pre_token(self) -> None:
        post = post_result()
        post["issued_at_unix"] = NOW - 60
        with self.assertRaises(AttestationContractError, msg="predates"):
            verify_two_phase_attestation_binding(
                pre_result(),
                post,
                authorization_consumption_sha256=C_SHA,
                output_manifest_sha256=MANIFEST_SHA,
            )

    def test_pair_rejects_wrong_expected_c(self) -> None:
        with self.assertRaises(AttestationContractError, msg="C binding"):
            verify_two_phase_attestation_binding(
                pre_result(),
                post_result(),
                authorization_consumption_sha256="6" * 64,
                output_manifest_sha256=MANIFEST_SHA,
            )

    def test_pair_rejects_wrong_expected_manifest(self) -> None:
        with self.assertRaises(AttestationContractError, msg="manifest binding"):
            verify_two_phase_attestation_binding(
                pre_result(),
                post_result(),
                authorization_consumption_sha256=C_SHA,
                output_manifest_sha256="7" * 64,
            )

    def test_input_claims_are_not_mutated(self) -> None:
        claims = good_claims()
        original = copy.deepcopy(claims)
        verify_confidential_space_attestation(
            claims,
            expectation(),
            token_context(),
        )
        self.assertEqual(claims, original)


if __name__ == "__main__":
    unittest.main()
