"""Synthetic raw-frame normalization fixtures, not official SDK conformance."""

from __future__ import annotations

import copy
import unittest
from dataclasses import replace
from datetime import datetime, timezone

from experiments.akdc.raw_wire_research import (
    ReceiverWitness,
    normalize_a2a_status_update,
    normalize_mcp_tools_call,
)
from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope

NOW = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)
TEST_CAPTURE_KEY = b"TEST-ONLY-NOT-FOR-PRODUCTION-0000000001"
TEST_KEY_ID = "fixture-key-01"


def witness(**changes):
    data = {
        "provider_id": "akdc-external-provider",
        "runtime_id": "raw-wire-test-runtime",
        "source_id": "fixture-source",
        "stream_id": "receiver-stream-one",
        "receipt_number": 1,
        "observed_at": "2026-10-26T12:00:00Z",
    }
    data.update(changes)
    return ReceiverWitness(**data)


def a2a(state="TASK_STATE_WORKING"):
    return {
        "statusUpdate": {
            "taskId": "task-001",
            "contextId": "context-001",
            "status": {"state": state},
        }
    }


def mcp_req():
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"_meta": {}, "name": "read-only", "arguments": {}},
    }


def mcp_resp(**changes):
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {"resultType": "complete", "content": [], "isError": False},
    }
    if "error" in changes and "result" not in changes:
        data.pop("result")
    data.update(changes)
    return data


class TestA2ARawStatus(unittest.TestCase):
    def parse(self, frame=None, obs=None, *, version="1.0.1"):
        return normalize_a2a_status_update(
            frame if frame is not None else a2a(),
            obs or witness(),
            negotiated_version=version,
            capture_key=TEST_CAPTURE_KEY,
            key_id=TEST_KEY_ID,
        )

    def test_status_update_is_observation_not_authorization(self):
        x = self.parse(a2a("TASK_STATE_COMPLETED"))
        self.assertEqual(x.observation.payload["state"], "TASK_STATE_COMPLETED")
        e = x.record_only_envelope()
        result = validate_external_runtime_envelope(e, now=NOW)
        self.assertTrue(result["admitted"])
        self.assertEqual(result["authority_status"], "PRESENTED_NOT_GRANTED")
        self.assertEqual(result["dgaf_verification_class"], "UNVERIFIED_EXTERNAL_ASSERTION")

    def test_receiver_sequence_is_not_a_wire_field(self):
        x = self.parse(obs=witness(receipt_number=17))
        self.assertEqual(x.observation.payload["sequence"], 17)
        self.assertEqual(x.receiver_receipt_number, 17)
        self.assertEqual(x.ordering_basis, "UNVERIFIED_RECEIVER_LOCAL_ORDER")
        self.assertNotIn("sequence", a2a()["statusUpdate"])

    def test_fake_wire_sequence_rejected(self):
        f = a2a()
        f["statusUpdate"]["sequence"] = 2
        with self.assertRaisesRegex(ValueError, "unknown A2A"):
            self.parse(f)

    def test_legacy_wire_shape_rejected(self):
        with self.assertRaisesRegex(ValueError, "only one statusUpdate"):
            self.parse({"kind": "status-update", "taskId": "task-001"})

    def test_multiple_response_branches_rejected(self):
        f = a2a()
        f["artifactUpdate"] = {}
        with self.assertRaisesRegex(ValueError, "only one statusUpdate"):
            self.parse(f)

    def test_version_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError, "unnegotiated A2A"):
            self.parse(version="0.3.0")

    def test_missing_status_and_unknown_state_rejected(self):
        with self.assertRaises(ValueError):
            self.parse({"statusUpdate": {"taskId": "t", "contextId": "c"}})
        with self.assertRaises(ValueError):
            self.parse(a2a("working"))

    def test_local_counter_requires_positive_int_not_bool(self):
        for value in (0, -1, True, "1"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "receipt_number"):
                self.parse(obs=witness(receipt_number=value))

    def test_digest_determinism_and_mutation_proof(self):
        f = a2a()
        first = self.parse(f)
        self.assertEqual(first.canonical_frame_digest, self.parse(copy.deepcopy(f)).canonical_frame_digest)
        self.assertEqual(first.observation.event_id, self.parse(copy.deepcopy(f)).observation.event_id)
        original = copy.deepcopy(first.observation.payload)
        f["statusUpdate"]["status"]["state"] = "TASK_STATE_FAILED"
        self.assertEqual(first.observation.payload, original)
        self.assertNotEqual(first.canonical_frame_digest, self.parse(f).canonical_frame_digest)

    def test_reconnect_local_identity_changes_not_exactly_once(self):
        first = self.parse()
        second = self.parse(obs=witness(stream_id="receiver-stream-two"))
        self.assertNotEqual(first.observation.event_id, second.observation.event_id)
        self.assertEqual(first.canonical_frame_digest, second.canonical_frame_digest)

    def test_capture_reference_is_recorded_and_digest_protected(self):
        captured = self.parse(obs=witness(receipt_number=9))
        envelope = captured.record_only_envelope()
        receipt = envelope["evidence"]["payload"]["capture_reference"]
        self.assertEqual(receipt["canonical_decoded_frame_digest"], captured.canonical_frame_digest)
        self.assertEqual(receipt["receiver_receipt_number"], 9)
        self.assertEqual(receipt["capture_attestation"], "NOT_ESTABLISHED")
        self.assertTrue(validate_external_runtime_envelope(envelope, now=NOW)["admitted"])
        envelope["evidence"]["payload"]["capture_reference"]["receiver_receipt_number"] = 10
        result = validate_external_runtime_envelope(envelope, now=NOW)
        self.assertEqual(result["reason_codes"], ["DGAF_EXT_EVIDENCE_DIGEST_MISMATCH"])

    def test_non_json_value_and_size_rejected(self):
        with self.assertRaises(ValueError):
            self.parse({"statusUpdate": {"taskId": "x", "contextId": "c", "status": {"state": float("nan")}}})
        with self.assertRaisesRegex(ValueError, "exceeds bounded"):
            f = a2a()
            f["statusUpdate"]["metadata"] = {"large": "X" * 70000}
            self.parse(f)


class TestMCPRawPair(unittest.TestCase):
    def parse(self, req=None, resp=None, obs=None, *, version="2026-07-28"):
        return normalize_mcp_tools_call(
            req or mcp_req(),
            resp or mcp_resp(),
            obs or witness(),
            negotiated_version=version,
            capture_key=TEST_CAPTURE_KEY,
            key_id=TEST_KEY_ID,
        )

    def test_success_is_record_only(self):
        x = self.parse()
        self.assertEqual(x.observation.payload["response"]["result"]["resultType"], "complete")
        e = x.record_only_envelope()
        result = validate_external_runtime_envelope(e, now=NOW)
        self.assertTrue(result["admitted"])
        self.assertEqual(result["authority_status"], "PRESENTED_NOT_GRANTED")

    def test_tool_error_distinct_from_protocol_error(self):
        tool_error = self.parse(resp=mcp_resp(result={"resultType": "complete", "content": [], "isError": True}))
        protocol_error = self.parse(resp=mcp_resp(error={"code": -32601, "message": "unknown method"}))
        self.assertIn("result", tool_error.observation.payload["response"])
        self.assertIn("error", protocol_error.observation.payload["response"])
        for x in (tool_error, protocol_error):
            self.assertTrue(validate_external_runtime_envelope(x.record_only_envelope(), now=NOW)["admitted"])

    def test_request_response_correlation_rejects_other_method(self):
        f = mcp_req()
        f["method"] = "resources/read"
        with self.assertRaisesRegex(ValueError, "tools/call request"):
            self.parse(req=f)

    def test_mismatch_id_rejected(self):
        with self.assertRaisesRegex(ValueError, "correlate"):
            self.parse(resp=mcp_resp(id=2))
        with self.assertRaisesRegex(ValueError, "correlate"):
            self.parse(resp=mcp_resp(id=True))

    def test_missing_result_type_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "resultType"):
            self.parse(resp=mcp_resp(result={"content": []}))

    def test_unknown_result_type_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "resultType"):
            self.parse(resp=mcp_resp(result={"resultType": "task", "content": []}))

    def test_protocol_version_mismatch(self):
        with self.assertRaisesRegex(ValueError, "MCP version"):
            self.parse(version="2025-11-25")

    def test_both_result_and_error_rejected(self):
        f = mcp_resp(result={"resultType": "complete", "content": []}, error={"code": -32600, "message": "error"})
        with self.assertRaisesRegex(ValueError, "exactly one"):
            self.parse(resp=f)

    def test_missing_request_meta_rejected(self):
        f = mcp_req()
        del f["params"]["_meta"]
        with self.assertRaisesRegex(ValueError, "params._meta"):
            self.parse(req=f)

    def test_wire_pair_digest_binds_request(self):
        first = self.parse()
        request = mcp_req()
        request["params"]["name"] = "other-tool"
        second = self.parse(req=request)
        self.assertNotEqual(first.canonical_frame_digest, second.canonical_frame_digest)
        self.assertNotEqual(first.observation.event_id, second.observation.event_id)

    def test_older_sdk_public_result_missing_result_type_not_accepted(self):
        with self.assertRaisesRegex(ValueError, "resultType"):
            self.parse(resp={"jsonrpc": "2.0", "id": 1, "result": {"content": []}})

    def test_input_required_with_opaque_state_observed(self):
        x = self.parse(resp=mcp_resp(result={"resultType": "input_required", "requestState": "opaque"}))
        self.assertEqual(x.observation.payload["response"]["result"]["resultType"], "input_required")
        self.assertTrue(validate_external_runtime_envelope(x.record_only_envelope(), now=NOW)["admitted"])

    def test_hybrid_input_required_rejected(self):
        with self.assertRaisesRegex(ValueError, "hybrid"):
            self.parse(resp=mcp_resp(result={"resultType": "input_required", "content": []}))

    def test_never_assert_authenticated_principal(self):
        first = self.parse()
        rotated = self.parse(obs=replace(witness(), runtime_id="untrusted-rotated-runtime"))
        self.assertNotEqual(first.observation.effect_id, rotated.observation.effect_id)
        self.assertEqual(first.canonical_frame_digest, rotated.canonical_frame_digest)


if __name__ == "__main__":
    unittest.main()
