from __future__ import annotations

import copy
import inspect
import unittest
from dataclasses import replace
from unittest.mock import patch

from cryptography.hazmat.primitives.asymmetric import rsa

from mode_t_admission_policy import (
    AdmissionPolicyError,
    admission_policy_sha256,
    verify_synthetic_consumption_policy_binding,
)
from mode_t_confidential_space_attestation import (
    AttestationExpectation,
    POST_EXECUTION,
    PRE_EXECUTION,
    verify_confidential_space_attestation,
)
from mode_t_google_oidc_verifier import GoogleOIDCVerifier, SYNTHETIC_TRANSPORT
from mode_t_inprocess_key import (
    ModeTKeyError,
    acquire_mode_t_key_synthetic_from_verified,
    admit_and_acquire_mode_t_key,
)
from mode_t_integrated_lifecycle import (
    ModeTLifecycleError,
    SyntheticAuthorizationConsumptionLedger,
    build_output_manifest,
    build_synthetic_blinded_artifact,
    canonical_json_bytes,
    finalize_two_phase_lifecycle,
    make_synthetic_authorization,
    make_synthetic_reservation,
)
from mode_t_policy_bound_key import (
    admit_and_acquire_mode_t_key_synthetic_from_consumption,
)
from test_mode_t_google_oidc_verifier import (
    AUDIENCE,
    CONTAINER_ARGS,
    ENV,
    IMAGE_DIGEST,
    NOW,
    SERVICE_ACCOUNTS,
    SUBJECT,
    FakeGoogleKeySource,
    good_claims,
    public_jwk,
    sign_token,
)

CANDIDATE_SHA = "a" * 40
FREEZE_COMMIT_SHA = "b" * 40
FREEZE_SHA = "c" * 64
WORKFLOW_SHA = "d" * 64
TLOCK_CLIENT_SHA = "e" * 64
TIMLOCK_CIPHERTEXT_SHA = "f" * 64
TLOCK_CHAIN_HASH = "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971"
RUN_ID = 310001
POLICY_BINDING_PLACEHOLDER = "0" * 64


class SyntheticCrash(RuntimeError):
    pass


def expectation(*, phase: str, binding: str) -> AttestationExpectation:
    return AttestationExpectation(
        phase=phase,
        audience=AUDIENCE,
        subject=SUBJECT,
        expected_service_accounts=SERVICE_ACCOUNTS,
        image_digest=IMAGE_DIGEST,
        binding_sha256=binding,
        expected_args=CONTAINER_ARGS,
        expected_env=ENV,
    )


def static_policy_sha() -> str:
    return admission_policy_sha256(
        expectation(phase=PRE_EXECUTION, binding=POLICY_BINDING_PLACEHOLDER)
    )


class IntegratedModeTLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.signing_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cls.kid = "synthetic-google-kid"

    def new_records(self, authorization_id: str):
        policy_sha = static_policy_sha()
        reservation = make_synthetic_reservation(
            freeze_commit_sha=FREEZE_COMMIT_SHA,
            freeze_sha256=FREEZE_SHA,
            workflow_sha256=WORKFLOW_SHA,
            github_run_id=RUN_ID,
            github_sha=CANDIDATE_SHA,
            admission_policy_sha256=policy_sha,
        )
        authorization = make_synthetic_authorization(
            reservation,
            authorization_id=authorization_id,
        )
        return reservation, authorization, SyntheticAuthorizationConsumptionLedger()

    def verifier(self) -> GoogleOIDCVerifier:
        source = FakeGoogleKeySource([public_jwk(self.signing_key, self.kid)])
        return GoogleOIDCVerifier(fetcher=source.fetch)

    def pre_token(self, c_sha: str) -> str:
        claims = good_claims()
        claims["eat_nonce"] = [c_sha]
        return sign_token(self.signing_key, self.kid, claims)

    def admitted_pre(self, c_sha: str, *, verifier=None):
        verifier = verifier or self.verifier()
        verified = verifier.verify(self.pre_token(c_sha), verified_at_unix=NOW)
        self.assertEqual(verified.key_source.transport_authentication, SYNTHETIC_TRANSPORT)
        admission = verify_confidential_space_attestation(
            verified.claims,
            expectation(phase=PRE_EXECUTION, binding=c_sha),
            verified.token_context,
        )
        return verified, admission

    def synthetic_acquisition(
        self,
        consumption,
        *,
        verifier=None,
        environment=None,
        expectation_override: AttestationExpectation | None = None,
    ):
        verifier = verifier or self.verifier()
        c_sha = consumption["consumption_evidence_sha256"]
        expected = expectation_override or expectation(phase=PRE_EXECUTION, binding=c_sha)
        return admit_and_acquire_mode_t_key_synthetic_from_consumption(
            self.pre_token(c_sha),
            expected,
            consumption,
            verifier=verifier,
            environment={} if environment is None else environment,
            verified_at_unix=NOW,
        )

    def admitted_post(self, manifest_sha: str, *, verifier: GoogleOIDCVerifier):
        claims = good_claims()
        claims["eat_nonce"] = [manifest_sha]
        claims["iat"] = NOW + 10
        claims["nbf"] = NOW + 10
        claims["exp"] = NOW + 310
        token = sign_token(self.signing_key, self.kid, claims)
        verified = verifier.verify(token, verified_at_unix=NOW + 20)
        admission = verify_confidential_space_attestation(
            verified.claims,
            expectation(phase=POST_EXECUTION, binding=manifest_sha),
            verified.token_context,
        )
        return verified, admission

    def test_production_key_entry_exposes_no_verification_time_override(self) -> None:
        signature = inspect.signature(admit_and_acquire_mode_t_key)
        self.assertNotIn("verified_at_unix", signature.parameters)

    def test_full_synthetic_lifecycle_connects_all_reviewed_boundaries(self) -> None:
        reservation, authorization, ledger = self.new_records("A-integrated-success")
        consumption = ledger.consume(reservation, authorization)
        c_sha = consumption["consumption_evidence_sha256"]
        policy_sha = consumption["admission_policy_sha256"]
        self.assertEqual(reservation["admission_policy_sha256"], policy_sha)
        self.assertEqual(authorization["admission_policy_sha256"], policy_sha)
        self.assertEqual(policy_sha, static_policy_sha())
        self.assertEqual(consumption["secret_instantiation_status"], "NOT_EXECUTED_AT_CONSUMPTION")
        self.assertIn("NOT_INDEPENDENTLY_RETAINED", consumption["retention_status"])

        policy_binding = verify_synthetic_consumption_policy_binding(
            consumption,
            expectation(phase=PRE_EXECUTION, binding=c_sha),
        )
        self.assertEqual(policy_binding["admission_policy_binding"], "PASS_SYNTHETIC_ONLY")
        self.assertEqual(policy_binding["admission_policy_sha256"], policy_sha)
        self.assertFalse(policy_binding["independent_retention_verified"])
        self.assertFalse(policy_binding["production_policy_complete"])
        self.assertFalse(policy_binding["pilot_authorized"])

        verifier = self.verifier()
        acquisition = self.synthetic_acquisition(consumption, verifier=verifier)
        pre = acquisition.pre_execution
        lease = acquisition.lease
        with lease:
            blinded = build_synthetic_blinded_artifact(
                lease,
                ["synthetic-condition-alpha", "synthetic-condition-beta"],
            )
            key_commitment = lease.key_commitment(b"synthetic-commitment-nonce-0001")
            manifest_bundle = build_output_manifest(
                candidate_sha=CANDIDATE_SHA,
                freeze_sha256=FREEZE_SHA,
                consumption_sha256=c_sha,
                admission_policy_sha256=policy_sha,
                runtime_identity_sha256=pre["runtime_identity_sha256"],
                workload_image_digest=IMAGE_DIGEST,
                tlock_client_sha256=TLOCK_CLIENT_SHA,
                tlock_chain_hash=TLOCK_CHAIN_HASH,
                blinded_artifact_sha256=blinded["artifact_sha256"],
                timelock_ciphertext_sha256=TIMLOCK_CIPHERTEXT_SHA,
                key_commitment_sha256=key_commitment,
                pre_execution_token_sha256=lease.token_sha256,
                execution_started_unix=NOW + 1,
                execution_completed_unix=NOW + 9,
            )
        self.assertTrue(lease.destroyed)
        blinded_bytes = canonical_json_bytes(blinded)
        self.assertNotIn(b"synthetic-condition-alpha", blinded_bytes)
        self.assertNotIn(b"synthetic-condition-beta", blinded_bytes)
        self.assertNotIn(b"PDMAL_BLINDING_KEY", blinded_bytes)

        manifest_sha = manifest_bundle["manifest_sha256"]
        self.assertEqual(manifest_bundle["manifest"]["admission_policy_sha256"], policy_sha)
        _, post = self.admitted_post(manifest_sha, verifier=verifier)
        final = finalize_two_phase_lifecycle(pre, post, manifest_bundle)
        self.assertEqual(final["integrated_lifecycle"], "PASS_SYNTHETIC_ONLY")
        self.assertEqual(final["authorization_consumption_sha256"], c_sha)
        self.assertEqual(final["admission_policy_sha256"], policy_sha)
        self.assertEqual(final["output_manifest_sha256"], manifest_sha)
        self.assertFalse(final["real_confidential_space_admission"])
        self.assertFalse(final["independent_retention_verified"])
        self.assertFalse(final["production_policy_complete"])
        self.assertFalse(final["pilot_authorized"])
        self.assertEqual(final["empirical_n"], 0)

        with self.assertRaises(ModeTLifecycleError):
            SyntheticAuthorizationConsumptionLedger(ledger.snapshot()).consume(
                reservation, authorization
            )

    def test_policy_bound_key_bridge_rejects_alternate_valid_expectation(self) -> None:
        reservation, authorization, ledger = self.new_records("A-policy-substitution")
        consumption = ledger.consume(reservation, authorization)
        c_sha = consumption["consumption_evidence_sha256"]
        alternate = replace(
            expectation(phase=PRE_EXECUTION, binding=c_sha),
            subject=SUBJECT + "-alternate",
        )
        with self.assertRaisesRegex(AdmissionPolicyError, "different admission policy"):
            self.synthetic_acquisition(
                consumption,
                expectation_override=alternate,
            )

    def test_policy_bound_key_bridge_rejects_wrong_pre_C_binding(self) -> None:
        reservation, authorization, ledger = self.new_records("A-wrong-C-binding")
        consumption = ledger.consume(reservation, authorization)
        wrong = expectation(phase=PRE_EXECUTION, binding="9" * 64)
        with self.assertRaisesRegex(AdmissionPolicyError, "exact synthetic C"):
            self.synthetic_acquisition(
                consumption,
                expectation_override=wrong,
            )

    def test_policy_bound_key_bridge_rejects_tampered_C_seal(self) -> None:
        reservation, authorization, ledger = self.new_records("A-tampered-C")
        consumption = ledger.consume(reservation, authorization)
        tampered = copy.deepcopy(consumption)
        tampered["admission_policy_sha256"] = "9" * 64
        with self.assertRaisesRegex(AdmissionPolicyError, "does not match C record"):
            self.synthetic_acquisition(tampered)

    def test_crash_after_C_before_pre_attestation_cannot_retry(self) -> None:
        reservation, authorization, ledger = self.new_records("A-crash-after-C")
        ledger.consume(reservation, authorization)
        with self.assertRaises(ModeTLifecycleError):
            SyntheticAuthorizationConsumptionLedger(ledger.snapshot()).consume(
                reservation, authorization
            )

    def test_crash_after_pre_attestation_before_key_cannot_retry(self) -> None:
        reservation, authorization, ledger = self.new_records("A-crash-after-pre")
        consumption = ledger.consume(reservation, authorization)
        self.admitted_pre(consumption["consumption_evidence_sha256"])
        with self.assertRaises(ModeTLifecycleError):
            SyntheticAuthorizationConsumptionLedger(ledger.snapshot()).consume(
                reservation, authorization
            )

    def test_crash_after_key_generation_zeroizes_and_cannot_retry(self) -> None:
        reservation, authorization, ledger = self.new_records("A-crash-after-key")
        consumption = ledger.consume(reservation, authorization)
        acquisition = self.synthetic_acquisition(consumption)
        with self.assertRaises(SyntheticCrash):
            with acquisition.lease:
                raise SyntheticCrash("simulated crash after key generation")
        self.assertTrue(acquisition.lease.destroyed)
        with self.assertRaises(ModeTLifecycleError):
            SyntheticAuthorizationConsumptionLedger(ledger.snapshot()).consume(
                reservation, authorization
            )

    def test_crash_after_blinded_output_before_post_attestation_cannot_retry(self) -> None:
        reservation, authorization, ledger = self.new_records("A-crash-after-output")
        consumption = ledger.consume(reservation, authorization)
        acquisition = self.synthetic_acquisition(consumption)
        with acquisition.lease as lease:
            blinded = build_synthetic_blinded_artifact(lease, ["one", "two"])
        self.assertEqual(blinded["empirical_n"], 0)
        with self.assertRaises(ModeTLifecycleError):
            SyntheticAuthorizationConsumptionLedger(ledger.snapshot()).consume(
                reservation, authorization
            )

    def test_key_generation_rejects_post_execution_or_circular_manifest_binding(self) -> None:
        reservation, authorization, ledger = self.new_records("A-key-boundary")
        consumption = ledger.consume(reservation, authorization)
        verified, pre = self.admitted_pre(consumption["consumption_evidence_sha256"])

        post_like = copy.deepcopy(pre)
        post_like["attestation_phase"] = POST_EXECUTION
        with self.assertRaises(ModeTKeyError):
            acquire_mode_t_key_synthetic_from_verified(post_like, verified, environment={})

        circular = copy.deepcopy(pre)
        circular["output_manifest_sha256"] = "9" * 64
        with self.assertRaises(ModeTKeyError):
            acquire_mode_t_key_synthetic_from_verified(circular, verified, environment={})

    def test_key_generation_rejects_runtime_identity_digest_tampering(self) -> None:
        reservation, authorization, ledger = self.new_records("A-runtime-drift")
        consumption = ledger.consume(reservation, authorization)
        verified, pre = self.admitted_pre(consumption["consumption_evidence_sha256"])
        tampered = copy.deepcopy(pre)
        tampered["runtime_identity"]["image_digest"] = "sha256:" + ("9" * 64)
        with self.assertRaisesRegex(ModeTKeyError, "runtime identity digest"):
            acquire_mode_t_key_synthetic_from_verified(tampered, verified, environment={})

    def test_production_key_entry_rejects_synthetic_verifier_result(self) -> None:
        reservation, authorization, ledger = self.new_records("A-no-promotion")
        consumption = ledger.consume(reservation, authorization)
        c_sha = consumption["consumption_evidence_sha256"]
        verified, _ = self.admitted_pre(c_sha)
        with patch(
            "mode_t_inprocess_key.verify_google_confidential_space_token",
            return_value=verified,
        ):
            with self.assertRaisesRegex(ModeTKeyError, "production Google key source"):
                admit_and_acquire_mode_t_key(
                    self.pre_token(c_sha),
                    expectation(phase=PRE_EXECUTION, binding=c_sha),
                    environment={},
                )

    def test_key_generation_rejects_verified_token_digest_mismatch(self) -> None:
        reservation, authorization, ledger = self.new_records("A-token-mismatch")
        consumption = ledger.consume(reservation, authorization)
        verified, pre = self.admitted_pre(consumption["consumption_evidence_sha256"])
        tampered = copy.deepcopy(pre)
        tampered["token_sha256"] = "9" * 64
        with self.assertRaisesRegex(ModeTKeyError, "verified token digest"):
            acquire_mode_t_key_synthetic_from_verified(tampered, verified, environment={})

    def test_external_operational_secret_environment_is_rejected(self) -> None:
        reservation, authorization, ledger = self.new_records("A-secret-env")
        consumption = ledger.consume(reservation, authorization)
        with self.assertRaises(ModeTKeyError):
            self.synthetic_acquisition(
                consumption,
                environment={"PDMAL_BLINDING_KEY": "forbidden"},
            )


if __name__ == "__main__":
    unittest.main()
