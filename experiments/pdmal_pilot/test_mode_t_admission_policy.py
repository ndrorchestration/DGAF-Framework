from __future__ import annotations

from dataclasses import replace
import unittest

from mode_t_admission_policy import (
    AdmissionPolicyError,
    TOKEN_LIFETIME_POLICY,
    admission_policy_identity,
    admission_policy_sha256,
    verify_synthetic_consumption_policy_binding,
)
from mode_t_confidential_space_attestation import (
    AttestationExpectation,
    POST_EXECUTION,
    PRE_EXECUTION,
)

C_SHA = "1" * 64
MANIFEST_SHA = "2" * 64
IMAGE_DIGEST = "sha256:" + ("3" * 64)
AUDIENCE = "dgaf-mode-t-admission-v1"
SUBJECT = "https://www.googleapis.com/compute/v1/projects/dgaf/zones/us-central1-a/instances/310"
SERVICE_ACCOUNTS = ("dgaf-mode-t@dgaf.iam.gserviceaccount.com",)
ARGS = ("/app/dgaf-mode-t",)
ENV = {"DGAF_RUN_BINDING": "synthetic-run-310"}


def expectation(*, phase: str = PRE_EXECUTION, binding: str = C_SHA) -> AttestationExpectation:
    return AttestationExpectation(
        phase=phase,
        audience=AUDIENCE,
        subject=SUBJECT,
        expected_service_accounts=SERVICE_ACCOUNTS,
        image_digest=IMAGE_DIGEST,
        binding_sha256=binding,
        expected_args=ARGS,
        expected_env=ENV,
    )


class AdmissionPolicyTests(unittest.TestCase):
    def test_policy_identity_is_static_across_pre_and_post_bindings(self) -> None:
        pre = expectation(phase=PRE_EXECUTION, binding=C_SHA)
        post = expectation(phase=POST_EXECUTION, binding=MANIFEST_SHA)
        self.assertEqual(admission_policy_sha256(pre), admission_policy_sha256(post))
        identity = admission_policy_identity(pre)
        self.assertNotIn("phase", identity)
        self.assertNotIn("binding_sha256", identity)
        self.assertFalse(identity["production_policy_complete"])
        self.assertIsNone(identity["token_lifetime_upper_bound_seconds"])
        self.assertEqual(identity["token_lifetime_policy"], TOKEN_LIFETIME_POLICY)

    def test_every_security_critical_expectation_change_changes_policy_digest(self) -> None:
        base = expectation()
        base_sha = admission_policy_sha256(base)
        variants = (
            replace(base, audience="other-audience"),
            replace(base, subject=SUBJECT + "-other"),
            replace(base, expected_service_accounts=("other@dgaf.iam.gserviceaccount.com",)),
            replace(base, image_digest="sha256:" + ("4" * 64)),
            replace(base, expected_args=("/bin/sh",)),
            replace(base, expected_env={"DGAF_RUN_BINDING": "other"}),
            replace(base, expected_cmd_override=("/bin/sh",)),
            replace(base, max_clock_skew_seconds=61),
        )
        for variant in variants:
            with self.subTest(variant=variant):
                self.assertNotEqual(base_sha, admission_policy_sha256(variant))

    def test_service_account_order_is_canonical_but_duplicates_fail(self) -> None:
        a = replace(
            expectation(),
            expected_service_accounts=(
                "alpha@dgaf.iam.gserviceaccount.com",
                "beta@dgaf.iam.gserviceaccount.com",
            ),
        )
        b = replace(
            a,
            expected_service_accounts=tuple(reversed(a.expected_service_accounts)),
        )
        self.assertEqual(admission_policy_sha256(a), admission_policy_sha256(b))
        with self.assertRaises(AdmissionPolicyError):
            admission_policy_sha256(
                replace(a, expected_service_accounts=(a.expected_service_accounts[0],) * 2)
            )

    def test_synthetic_consumption_binding_accepts_exact_policy_without_promotion(self) -> None:
        policy_sha = admission_policy_sha256(expectation())
        consumption = {
            "admission_policy_sha256": policy_sha,
            "retention_status": "SYNTHETIC_MODEL_ONLY_NOT_INDEPENDENTLY_RETAINED",
            "synthetic_only": True,
        }
        result = verify_synthetic_consumption_policy_binding(consumption, expectation())
        self.assertEqual(result["admission_policy_binding"], "PASS_SYNTHETIC_ONLY")
        self.assertEqual(result["admission_policy_sha256"], policy_sha)
        self.assertFalse(result["independent_retention_verified"])
        self.assertFalse(result["production_policy_complete"])
        self.assertFalse(result["pilot_authorized"])
        self.assertEqual(result["empirical_n"], 0)

    def test_synthetic_consumption_binding_rejects_alternate_valid_policy(self) -> None:
        policy_sha = admission_policy_sha256(expectation())
        consumption = {
            "admission_policy_sha256": policy_sha,
            "retention_status": "SYNTHETIC_MODEL_ONLY_NOT_INDEPENDENTLY_RETAINED",
            "synthetic_only": True,
        }
        alternate = replace(expectation(), subject=SUBJECT + "-other")
        with self.assertRaisesRegex(AdmissionPolicyError, "different admission policy"):
            verify_synthetic_consumption_policy_binding(consumption, alternate)

    def test_synthetic_consumption_binding_rejects_promotable_or_unknown_retention(self) -> None:
        policy_sha = admission_policy_sha256(expectation())
        for retention, synthetic in (
            ("INDEPENDENTLY_RETAINED", True),
            ("SYNTHETIC_MODEL_ONLY_NOT_INDEPENDENTLY_RETAINED", False),
        ):
            with self.subTest(retention=retention, synthetic=synthetic):
                with self.assertRaises(AdmissionPolicyError):
                    verify_synthetic_consumption_policy_binding(
                        {
                            "admission_policy_sha256": policy_sha,
                            "retention_status": retention,
                            "synthetic_only": synthetic,
                        },
                        expectation(),
                    )


if __name__ == "__main__":
    unittest.main()
