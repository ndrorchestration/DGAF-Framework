from __future__ import annotations

import copy
import inspect
import unittest

from cryptography.hazmat.primitives.asymmetric import rsa

from mode_t_admission_policy import (
    ModeTAdmissionPolicyError,
    admission_policy_sha256,
    admit_and_acquire_mode_t_key_synthetic_policy_bound,
    canonical_admission_policy,
    require_production_retained_policy_verifier,
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


class SyntheticCrash(RuntimeError):
    pass


def expectation(
    *,
    phase: str,
    binding: str,
    audience: str = AUDIENCE,
    subject: str = SUBJECT,
    service_accounts: tuple[str, ...] = SERVICE_ACCOUNTS,
    image_digest: str = IMAGE_DIGEST,
    args: tuple[str, ...] = CONTAINER_ARGS,
    env: dict[str, str] | None = None,
    cmd_override: tuple[str, ...] = (),
    skew: int = 60,
) -> AttestationExpectation:
    return AttestationExpectation(
        phase=phase,
        audience=audience,
        subject=subject,
        expected_service_accounts=service_accounts,
        image_digest=image_digest,
        binding_sha256=binding,
        expected_args=args,
        expected_env=ENV if env is None else env,
        expected_cmd_override=cmd_override,
        max_clock_skew_seconds=skew,
    )


def policy_expectation(**changes) -> AttestationExpectation:
    values = {
        "phase": PRE_EXECUTION,
        "binding": "0" * 64,
        "audience": AUDIENCE,
        "subject": SUBJECT,
        "service_accounts": SERVICE_ACCOUNTS,
        "image_digest": IMAGE_DIGEST,
        "args": CONTAINER_ARGS,
        "env": dict(ENV),
        "cmd_override": (),
        "skew": 60,
    }
    values.update(changes)
    return expectation(**values)


class IntegratedModeTLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.signing_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cls.kid = "synthetic-google-kid"

    def new_records(self, authorization_id: str, *, policy=None):
        policy = policy or policy_expectation()
        policy_sha = admission_policy_sha256(policy)
        reservation = make_synthetic_reservation(
            freeze_commit_sha=FREEZE_COMMIT_SHA,
            freeze_sha256=FREEZE_SHA,
            workflow_sha256=WORKFLOW_SHA,
            admission_policy_sha256=policy_sha,
            github_run_id=RUN_ID,
            github_sha=CANDIDATE_SHA,
        )
        authorization = make_synthetic_authorization(
            reservation,
            authorization_id=authorization_id,
        )
        return reservation, authorization, SyntheticAuthorizationConsumptionLedger(), policy_sha

    def verifier(self) -> GoogleOIDCVerifier:
        source = FakeGoogleKeySource([public_jwk(self.signing_key, self.kid)])
        return GoogleOIDCVerifier(fetcher=source.fetch)

    def pre_token(self, c_sha: str, *, claims_changes=None) -> str:
        claims = good_claims()
        claims["eat_nonce"] = [c_sha]
        if claims_changes:
            claims.update(claims_changes)
        return sign_token(self.signing_key, self.kid, claims)

    def admitted_pre(self, c_sha: str, *, verifier=None, exp=None):
        verifier = verifier or self.verifier()
        exp = exp or expectation(phase=PRE_EXECUTION, binding=c_sha)
        verified = verifier.verify(self.pre_token(c_sha), verified_at_unix=NOW)
        self.assertEqual(verified.key_source.transport_authentication, SYNTHETIC_TRANSPORT)
        admission = verify_confidential_space_attestation(
            verified.claims,
            exp,
            verified.token_context,
        )
        return verified, admission

    def synthetic_acquisition(self, consumption, *, verifier=None, exp=None, environment=None):
        verifier = verifier or self.verifier()
        c_sha = consumption["consumption_evidence_sha256"]
        exp = exp or expectation(phase=PRE_EXECUTION, binding=c_sha)
        return admit_and_acquire_mode_t_key_synthetic_policy_bound(
            self.pre_token(c_sha),
            exp,
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

    def test_production_key_entry_is_fail_closed_pending_retained_policy_verifier(self) -> None:
        with self.assertRaisesRegex(ModeTKeyError, "independently retained C/policy verifier"):
            admit_and_acquire_mode_t_key(
                "synthetic.invalid.token",
                policy_expectation(),
                environment={},
            )
        with self.assertRaisesRegex(
            ModeTAdmissionPolicyError,
            "independently retained C/policy evidence verifier",
        ):
            require_production_retained_policy_verifier()

    def test_policy_identity_excludes_run_specific_C_but_covers_security_fields(self) -> None:
        p1 = policy_expectation(binding="1" * 64)
        p2 = policy_expectation(binding="2" * 64)
        self.assertEqual(admission_policy_sha256(p1), admission_policy_sha256(p2))

        variants = (
            policy_expectation(audience="other-audience"),
            policy_expectation(subject=SUBJECT + "-other"),
            policy_expectation(service_accounts=("other@example.iam.gserviceaccount.com",)),
            policy_expectation(image_digest="sha256:" + ("9" * 64)),
            policy_expectation(args=("/app/other",)),
            policy_expectation(env={"DGAF_RUN_BINDING": "other"}),
            policy_expectation(cmd_override=("/bin/other",)),
            policy_expectation(skew=61),
        )
        base = admission_policy_sha256(p1)
        for variant in variants:
            self.assertNotEqual(base, admission_policy_sha256(variant))

        policy = canonical_admission_policy(p1)
        self.assertFalse(policy["environment_override_allowed"])
        self.assertFalse(policy["operational_secret_environment_allowed"])
        self.assertEqual(policy["hardware_model"], "GCP_INTEL_TDX")
        self.assertEqual(policy["restart_policy"], "Never")

    def test_R_A_C_carry_exact_policy_digest(self) -> None:
        reservation, authorization, ledger, policy_sha = self.new_records("A-policy-chain")
        consumption = ledger.consume(reservation, authorization)
        self.assertEqual(reservation["admission_policy_sha256"], policy_sha)
        self.assertEqual(authorization["admission_policy_sha256"], policy_sha)
        self.assertEqual(consumption["admission_policy_sha256"], policy_sha)

    def test_policy_substitution_after_C_is_rejected_before_key_generation(self) -> None:
        reservation, authorization, ledger, _ = self.new_records("A-policy-substitution")
        consumption = ledger.consume(reservation, authorization)
        c_sha = consumption["consumption_evidence_sha256"]
        substituted = expectation(
            phase=PRE_EXECUTION,
            binding=c_sha,
            image_digest="sha256:" + ("9" * 64),
        )
        with self.assertRaisesRegex(ModeTAdmissionPolicyError, "pre-authorized admission policy"):
            self.synthetic_acquisition(consumption, exp=substituted)

    def test_each_material_policy_field_mutation_is_rejected(self) -> None:
        reservation, authorization, ledger, _ = self.new_records("A-policy-fields")
        consumption = ledger.consume(reservation, authorization)
        c_sha = consumption["consumption_evidence_sha256"]
        variants = (
            expectation(phase=PRE_EXECUTION, binding=c_sha, audience="other"),
            expectation(phase=PRE_EXECUTION, binding=c_sha, subject=SUBJECT + "-other"),
            expectation(
                phase=PRE_EXECUTION,
                binding=c_sha,
                service_accounts=("other@example.iam.gserviceaccount.com",),
            ),
            expectation(
                phase=PRE_EXECUTION,
                binding=c_sha,
                image_digest="sha256:" + ("9" * 64),
            ),
            expectation(phase=PRE_EXECUTION, binding=c_sha, args=("/app/other",)),
            expectation(phase=PRE_EXECUTION, binding=c_sha, env={"DGAF_RUN_BINDING": "other"}),
            expectation(phase=PRE_EXECUTION, binding=c_sha, cmd_override=("/bin/other",)),
            expectation(phase=PRE_EXECUTION, binding=c_sha, skew=61),
        )
        for variant in variants:
            with self.assertRaises(ModeTAdmissionPolicyError):
                self.synthetic_acquisition(consumption, exp=variant)

    def test_tampered_or_promoted_synthetic_C_is_rejected(self) -> None:
        reservation, authorization, ledger, _ = self.new_records("A-C-tamper")
        consumption = ledger.consume(reservation, authorization)
        c_sha = consumption["consumption_evidence_sha256"]
        exp = expectation(phase=PRE_EXECUTION, binding=c_sha)

        tampered = copy.deepcopy(consumption)
        tampered["admission_policy_sha256"] = "9" * 64
        with self.assertRaisesRegex(ModeTAdmissionPolicyError, "digest does not match"):
            self.synthetic_acquisition(tampered, exp=exp)

        promoted = copy.deepcopy(consumption)
        promoted["retention_status"] = "INDEPENDENTLY_RETAINED"
        # Recompute seal to prove even a self-consistent caller-made promoted record is rejected.
        core = dict(promoted)
        core.pop("consumption_evidence_sha256")
        import hashlib
        promoted["consumption_evidence_sha256"] = hashlib.sha256(canonical_json_bytes(core)).hexdigest()
        exp2 = expectation(
            phase=PRE_EXECUTION,
            binding=promoted["consumption_evidence_sha256"],
        )
        with self.assertRaisesRegex(ModeTAdmissionPolicyError, "retention marker"):
            self.synthetic_acquisition(promoted, exp=exp2)

    def test_full_synthetic_lifecycle_connects_policy_and_attestation_boundaries(self) -> None:
        reservation, authorization, ledger, policy_sha = self.new_records("A-integrated-success")
        consumption = ledger.consume(reservation, authorization)
        c_sha = consumption["consumption_evidence_sha256"]
        self.assertEqual(consumption["secret_instantiation_status"], "NOT_EXECUTED_AT_CONSUMPTION")
        self.assertIn("NOT_INDEPENDENTLY_RETAINED", consumption["retention_status"])

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
        _, post = self.admitted_post(manifest_sha, verifier=verifier)
        final = finalize_two_phase_lifecycle(pre, post, manifest_bundle)
        self.assertEqual(final["integrated_lifecycle"], "PASS_SYNTHETIC_ONLY")
        self.assertEqual(final["authorization_consumption_sha256"], c_sha)
        self.assertEqual(final["admission_policy_sha256"], policy_sha)
        self.assertEqual(final["output_manifest_sha256"], manifest_sha)
        self.assertFalse(final["real_confidential_space_admission"])
        self.assertFalse(final["independent_retention_verified"])
        self.assertFalse(final["pilot_authorized"])
        self.assertEqual(final["empirical_n"], 0)

        with self.assertRaises(ModeTLifecycleError):
            SyntheticAuthorizationConsumptionLedger(ledger.snapshot()).consume(
                reservation, authorization
            )

    def test_crash_boundaries_preserve_consumption(self) -> None:
        for suffix in ("after-C", "after-pre", "after-key", "after-output"):
            reservation, authorization, ledger, _ = self.new_records(f"A-crash-{suffix}")
            consumption = ledger.consume(reservation, authorization)
            if suffix == "after-pre":
                self.admitted_pre(consumption["consumption_evidence_sha256"])
            elif suffix == "after-key":
                acquisition = self.synthetic_acquisition(consumption)
                with self.assertRaises(SyntheticCrash):
                    with acquisition.lease:
                        raise SyntheticCrash("simulated crash after key generation")
                self.assertTrue(acquisition.lease.destroyed)
            elif suffix == "after-output":
                acquisition = self.synthetic_acquisition(consumption)
                with acquisition.lease as lease:
                    blinded = build_synthetic_blinded_artifact(lease, ["one", "two"])
                self.assertEqual(blinded["empirical_n"], 0)
            with self.assertRaises(ModeTLifecycleError):
                SyntheticAuthorizationConsumptionLedger(ledger.snapshot()).consume(
                    reservation, authorization
                )

    def test_key_generation_rejects_post_execution_circular_or_runtime_tampering(self) -> None:
        reservation, authorization, ledger, _ = self.new_records("A-key-boundary")
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

        runtime_drift = copy.deepcopy(pre)
        runtime_drift["runtime_identity"]["image_digest"] = "sha256:" + ("9" * 64)
        with self.assertRaisesRegex(ModeTKeyError, "runtime identity digest"):
            acquire_mode_t_key_synthetic_from_verified(runtime_drift, verified, environment={})

    def test_key_generation_rejects_verified_token_digest_mismatch(self) -> None:
        reservation, authorization, ledger, _ = self.new_records("A-token-mismatch")
        consumption = ledger.consume(reservation, authorization)
        verified, pre = self.admitted_pre(consumption["consumption_evidence_sha256"])
        tampered = copy.deepcopy(pre)
        tampered["token_sha256"] = "9" * 64
        with self.assertRaisesRegex(ModeTKeyError, "verified token digest"):
            acquire_mode_t_key_synthetic_from_verified(tampered, verified, environment={})

    def test_external_operational_secret_environment_is_rejected(self) -> None:
        reservation, authorization, ledger, _ = self.new_records("A-secret-env")
        consumption = ledger.consume(reservation, authorization)
        with self.assertRaises(ModeTKeyError):
            self.synthetic_acquisition(
                consumption,
                environment={"PDMAL_BLINDING_KEY": "forbidden"},
            )


if __name__ == "__main__":
    unittest.main()
