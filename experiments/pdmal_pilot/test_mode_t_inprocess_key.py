from __future__ import annotations

import hashlib
import hmac
import pickle
import unittest
from unittest import mock

from mode_t_confidential_space_attestation import (
    AttestationExpectation,
    VerifiedTokenContext,
    verify_confidential_space_attestation,
)
from mode_t_inprocess_key import KEY_BYTES, ModeTKeyError, acquire_mode_t_key


C_SHA = "1" * 64
MANIFEST_SHA = "2" * 64
TOKEN_SHA = "3" * 64
IMAGE_DIGEST = "sha256:" + ("4" * 64)
NOW = 1_800_000_000
TEST_KEY = bytes(range(KEY_BYTES))


def admitted_attestation() -> dict:
    claims = {
        "iss": "https://confidentialcomputing.googleapis.com",
        "swname": "CONFIDENTIAL_SPACE",
        "hwmodel": "GCP_INTEL_TDX",
        "dbgstat": "disabled-since-boot",
        "iat": NOW - 30,
        "nbf": NOW - 30,
        "exp": NOW + 300,
        "eat_nonce": [C_SHA, MANIFEST_SHA],
        "submods": {
            "confidential_space": {"support_attributes": ["STABLE"]},
            "container": {
                "image_digest": IMAGE_DIGEST,
                "cmd_override": [],
                "env": {"DGAF_RUN_BINDING": "synthetic-run-310"},
                "env_override": {},
                "restart_policy": "Never",
            },
        },
    }
    expectation = AttestationExpectation(
        image_digest=IMAGE_DIGEST,
        authorization_consumption_sha256=C_SHA,
        output_manifest_sha256=MANIFEST_SHA,
        expected_env={"DGAF_RUN_BINDING": "synthetic-run-310"},
    )
    context = VerifiedTokenContext(
        signature_verified=True,
        token_sha256=TOKEN_SHA,
        verified_at_unix=NOW,
    )
    return verify_confidential_space_attestation(claims, expectation, context)


class ModeTInProcessKeyTests(unittest.TestCase):
    @mock.patch("mode_t_inprocess_key.secrets.token_bytes", return_value=TEST_KEY)
    def test_exact_admission_generates_256_bit_key_without_external_secret(self, token_bytes: mock.Mock) -> None:
        lease = acquire_mode_t_key(admitted_attestation(), environment={})
        self.assertFalse(lease.destroyed)
        token_bytes.assert_called_once_with(KEY_BYTES)
        self.assertEqual(lease.token_sha256, TOKEN_SHA)
        self.assertEqual(lease.authorization_consumption_sha256, C_SHA)
        self.assertEqual(lease.output_manifest_sha256, MANIFEST_SHA)
        lease.destroy()

    @mock.patch("mode_t_inprocess_key.secrets.token_bytes", return_value=TEST_KEY)
    def test_hmac_operation_matches_reference_without_raw_key_return(self, _token_bytes: mock.Mock) -> None:
        message = b"PDMAL-BLINDED-CONDITION-ID-v1|dgaf"
        with acquire_mode_t_key(admitted_attestation(), environment={}) as lease:
            expected = hmac.new(TEST_KEY, message, hashlib.sha256).digest()
            self.assertEqual(lease.hmac_sha256(message), expected)
            self.assertNotIn(TEST_KEY.hex(), repr(lease))
            self.assertIn("material=<redacted>", repr(lease))

    @mock.patch("mode_t_inprocess_key.secrets.token_bytes", return_value=TEST_KEY)
    def test_context_exit_zeroizes_owned_buffer(self, _token_bytes: mock.Mock) -> None:
        lease = acquire_mode_t_key(admitted_attestation(), environment={})
        owned_buffer = lease._material  # synthetic regression inspection only
        with lease:
            self.assertEqual(bytes(owned_buffer), TEST_KEY)
        self.assertTrue(lease.destroyed)
        self.assertEqual(bytes(owned_buffer), b"\x00" * KEY_BYTES)

    @mock.patch("mode_t_inprocess_key.secrets.token_bytes", return_value=TEST_KEY)
    def test_destroyed_lease_cannot_compute_hmac_or_reenter(self, _token_bytes: mock.Mock) -> None:
        lease = acquire_mode_t_key(admitted_attestation(), environment={})
        lease.destroy()
        lease.destroy()
        with self.assertRaises(ModeTKeyError, msg="destroyed"):
            lease.hmac_sha256(b"message")
        with self.assertRaises(ModeTKeyError, msg="destroyed"):
            lease.__enter__()

    @mock.patch("mode_t_inprocess_key.secrets.token_bytes", return_value=TEST_KEY)
    def test_serialization_is_prohibited(self, _token_bytes: mock.Mock) -> None:
        lease = acquire_mode_t_key(admitted_attestation(), environment={})
        with self.assertRaises(TypeError, msg="serialization"):
            pickle.dumps(lease)
        lease.destroy()

    def test_external_legacy_blinding_key_is_rejected_before_generation(self) -> None:
        with mock.patch("mode_t_inprocess_key.secrets.token_bytes") as token_bytes:
            with self.assertRaises(ModeTKeyError, msg="PDMAL_BLINDING_KEY"):
                acquire_mode_t_key(admitted_attestation(), environment={"PDMAL_BLINDING_KEY": "injected"})
            token_bytes.assert_not_called()

    def test_external_mode_t_key_is_rejected_before_generation(self) -> None:
        with mock.patch("mode_t_inprocess_key.secrets.token_bytes") as token_bytes:
            with self.assertRaises(ModeTKeyError, msg="PDMAL_MODE_T_KEY"):
                acquire_mode_t_key(admitted_attestation(), environment={"PDMAL_MODE_T_KEY": "injected"})
            token_bytes.assert_not_called()

    def test_unadmitted_attestation_is_rejected_before_generation(self) -> None:
        admission = admitted_attestation()
        admission["attestation_contract"] = "FAIL"
        with mock.patch("mode_t_inprocess_key.secrets.token_bytes") as token_bytes:
            with self.assertRaises(ModeTKeyError, msg="not PASS"):
                acquire_mode_t_key(admission, environment={})
            token_bytes.assert_not_called()

    def test_unverified_signature_is_rejected_before_generation(self) -> None:
        admission = admitted_attestation()
        admission["signature_verified"] = False
        with mock.patch("mode_t_inprocess_key.secrets.token_bytes") as token_bytes:
            with self.assertRaises(ModeTKeyError, msg="not verified"):
                acquire_mode_t_key(admission, environment={})
            token_bytes.assert_not_called()

    def test_wrong_hardware_is_rejected_before_generation(self) -> None:
        admission = admitted_attestation()
        admission["hardware_model"] = "GCP_AMD_SEV"
        with mock.patch("mode_t_inprocess_key.secrets.token_bytes") as token_bytes:
            with self.assertRaises(ModeTKeyError, msg="GCP_INTEL_TDX"):
                acquire_mode_t_key(admission, environment={})
            token_bytes.assert_not_called()

    def test_debug_state_is_rejected_before_generation(self) -> None:
        admission = admitted_attestation()
        admission["debug_status"] = "enabled"
        with mock.patch("mode_t_inprocess_key.secrets.token_bytes") as token_bytes:
            with self.assertRaises(ModeTKeyError, msg="not production"):
                acquire_mode_t_key(admission, environment={})
            token_bytes.assert_not_called()

    def test_restart_policy_is_rejected_before_generation(self) -> None:
        admission = admitted_attestation()
        admission["restart_policy"] = "OnFailure"
        with mock.patch("mode_t_inprocess_key.secrets.token_bytes") as token_bytes:
            with self.assertRaises(ModeTKeyError, msg="not Never"):
                acquire_mode_t_key(admission, environment={})
            token_bytes.assert_not_called()

    def test_malformed_binding_digest_is_rejected_before_generation(self) -> None:
        admission = admitted_attestation()
        admission["authorization_consumption_sha256"] = "not-a-digest"
        with mock.patch("mode_t_inprocess_key.secrets.token_bytes") as token_bytes:
            with self.assertRaises(ModeTKeyError, msg="SHA-256"):
                acquire_mode_t_key(admission, environment={})
            token_bytes.assert_not_called()

    @mock.patch("mode_t_inprocess_key.secrets.token_bytes", return_value=b"short")
    def test_wrong_csprng_length_is_rejected(self, _token_bytes: mock.Mock) -> None:
        with self.assertRaises(ModeTKeyError, msg="unexpected key length"):
            acquire_mode_t_key(admitted_attestation(), environment={})

    @mock.patch("mode_t_inprocess_key.secrets.token_bytes", return_value=bytearray(TEST_KEY))
    def test_non_bytes_csprng_result_is_rejected(self, _token_bytes: mock.Mock) -> None:
        with self.assertRaises(ModeTKeyError, msg="did not return bytes"):
            acquire_mode_t_key(admitted_attestation(), environment={})

    @mock.patch("mode_t_inprocess_key.secrets.token_bytes", side_effect=[TEST_KEY, bytes(reversed(TEST_KEY))])
    def test_separate_leases_do_not_reuse_material(self, _token_bytes: mock.Mock) -> None:
        first = acquire_mode_t_key(admitted_attestation(), environment={})
        second = acquire_mode_t_key(admitted_attestation(), environment={})
        message = b"domain|payload"
        self.assertNotEqual(first.hmac_sha256(message), second.hmac_sha256(message))
        first.destroy()
        second.destroy()


if __name__ == "__main__":
    unittest.main()
