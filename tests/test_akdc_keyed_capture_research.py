"""Gate 9 HMAC capture commitment tests; synthetic fixture only."""

import hashlib
import hmac
import json
import unittest

from test_akdc_raw_wire_research import (
    NOW,
    TEST_CAPTURE_KEY,
    TEST_KEY_ID,
    a2a,
    mcp_req,
    mcp_resp,
    witness,
)

from experiments.akdc.akdc_ingress_bridge import canonical_bytes
from experiments.akdc.raw_wire_research import normalize_a2a_status_update, normalize_mcp_tools_call
from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope


class TestKeyedCaptureContracts(unittest.TestCase):
    def capture(self, *, key=TEST_CAPTURE_KEY, key_id=TEST_KEY_ID, request=None, response=None):
        return normalize_mcp_tools_call(
            mcp_req() if request is None else request,
            mcp_resp() if response is None else response,
            witness(),
            negotiated_version="2026-07-28",
            capture_key=key,
            key_id=key_id,
        )

    def test_key_is_mandatory(self):
        with self.assertRaises(TypeError):
            normalize_mcp_tools_call(mcp_req(), mcp_resp(), witness(), negotiated_version="2026-07-28")
        with self.assertRaises(TypeError):
            normalize_a2a_status_update(a2a(), witness(), negotiated_version="1.0.1")

    def test_weak_key_and_nonbytes_refused(self):
        for value in (b"", b"short", bytearray(TEST_CAPTURE_KEY), None):
            with self.subTest(type=type(value).__name__), self.assertRaisesRegex(ValueError, "capture_key"):
                self.capture(key=value)

    def test_unusable_key_id_refused(self):
        for value in ("", "with space", "opaque:secret", "äccent", "x" * 49):
            with self.subTest(key_id=value), self.assertRaisesRegex(ValueError, "key ID"):
                self.capture(key_id=value)

    def test_deterministic_replay_under_same_key_and_receipt(self):
        first, repeated = self.capture(), self.capture()
        self.assertEqual(first.canonical_frame_digest, repeated.canonical_frame_digest)
        self.assertEqual(first.observation.event_id, repeated.observation.event_id)
        self.assertEqual(first.observation.effect_id, repeated.observation.effect_id)
        self.assertEqual(first.commitment_key_id, TEST_KEY_ID)

    def test_key_rotation_changes_both_digest_and_identity(self):
        old = self.capture()
        rotated = self.capture(key=b"RESEARCH-ROTATED-UNSAFE-NOT-A-REAL-KEY-001")
        self.assertNotEqual(old.canonical_frame_digest, rotated.canonical_frame_digest)
        self.assertNotEqual(old.observation.event_id, rotated.observation.event_id)

    def test_key_id_changes_identity_not_hmac_frame(self):
        old = self.capture()
        new = self.capture(key_id="fixture-key-02")
        self.assertEqual(old.canonical_frame_digest, new.canonical_frame_digest)
        self.assertNotEqual(old.observation.event_id, new.observation.event_id)
        self.assertEqual(new.commitment_key_id, "fixture-key-02")

    def test_unkeyed_hash_does_not_equal_frame_hmac(self):
        raw = {"request": mcp_req(), "response": mcp_resp()}
        source_sha = hashlib.sha256(canonical_bytes(raw)).hexdigest()
        captured = self.capture()
        self.assertTrue(captured.canonical_frame_digest.startswith("hmac-sha256:"))
        self.assertNotEqual(captured.canonical_frame_digest.removeprefix("hmac-sha256:"), source_sha)
        expected = hmac.new(
            TEST_CAPTURE_KEY, canonical_bytes(["AKDC-FRAME-V1", "mcp", "2026-07-28", raw]), hashlib.sha256
        ).hexdigest()
        self.assertEqual(captured.canonical_frame_digest, "hmac-sha256:" + expected)

    def test_original_request_id_is_discarded(self):
        request, response = mcp_req(), mcp_resp()
        request["id"] = "low_entropy_id"
        response["id"] = "low_entropy_id"
        captured = self.capture(request=request, response=response)
        self.assertEqual(captured.observation.payload["response"]["id"], "correlation-withheld")
        self.assertNotIn("low_entropy_id", json.dumps(captured.record_only_envelope()))
        self.assertTrue(validate_external_runtime_envelope(captured.record_only_envelope(), now=NOW)["admitted"])

    def test_secret_not_stored_and_metadata_tampering_refused(self):
        captured = self.capture()
        envelope = captured.record_only_envelope()
        rendered = json.dumps(envelope)
        self.assertNotIn(TEST_CAPTURE_KEY.decode(), rendered)
        self.assertEqual(envelope["evidence"]["payload"]["capture_reference"]["commitment_key_id"], TEST_KEY_ID)
        self.assertEqual(
            envelope["evidence"]["payload"]["capture_reference"]["commitment_scheme"],
            "HMAC-SHA256-V1-RESEARCH",
        )
        envelope["evidence"]["payload"]["capture_reference"]["commitment_key_id"] = "changed"
        denial = validate_external_runtime_envelope(envelope, now=NOW)
        self.assertEqual(denial["reason_codes"], ["DGAF_EXT_EVIDENCE_DIGEST_MISMATCH"])

    def test_a2a_uses_keyed_commitment_and_non_authorizing_ingress(self):
        captured = normalize_a2a_status_update(
            a2a(), witness(), negotiated_version="1.0.1",
            capture_key=TEST_CAPTURE_KEY, key_id=TEST_KEY_ID,
        )
        self.assertTrue(captured.canonical_frame_digest.startswith("hmac-sha256:"))
        self.assertTrue(validate_external_runtime_envelope(captured.record_only_envelope(), now=NOW)["admitted"])


if __name__ == "__main__":
    unittest.main()
