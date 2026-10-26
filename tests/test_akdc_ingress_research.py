"""AKDC research tests: real DGAF ingress validator; no execution or custody."""

from __future__ import annotations

import copy
import unittest
from datetime import datetime, timedelta, timezone

from experiments.akdc.akdc_ingress_bridge import (
    OrderingGate,
    ProtocolObservation,
    classify,
    content_digest,
    make_dgaf_envelope,
)
from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope

NOW = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)


def a2a(seq=1, state="TASK_STATE_WORKING", **kwargs):
    data = dict(
        protocol="a2a",
        version="1.0.1",
        provider_id="synthetic-akdc",
        runtime_id="fixture-run-01",
        source_id="source-akdc-01",
        event_id=f"evt-akdc-{seq}",
        effect_id=f"effect-akdc-{seq}",
        observed_at="2026-10-26T12:00:00Z",
        payload=dict(task_id="task-akdc-1", context_id="context-akdc-1", state=state, sequence=seq),
    )
    data.update(kwargs)
    return ProtocolObservation(**data)


def mcp(result=None, error=None, **kwargs):
    response = {"jsonrpc": "2.0", "id": 10}
    if error is not None:
        response["error"] = error
    else:
        response["result"] = (
            result
            if result is not None
            else {
                "resultType": "complete",
                "content": [],
                "isError": False,
            }
        )
    data = dict(
        protocol="mcp",
        version="2026-07-28",
        provider_id="synthetic-akdc",
        runtime_id="fixture-run-01",
        source_id="mcp-akdc-1",
        event_id="evt-mcp-akdc-1",
        effect_id="effect-mcp-akdc-1",
        observed_at="2026-10-26T12:00:00Z",
        payload={"method": "tools/call", "response": response},
    )
    data.update(kwargs)
    return ProtocolObservation(**data)


class AKDCResearchIngress(unittest.TestCase):
    def test_a2a_states_explicit_not_authority(self):
        states = (
            "SUBMITTED",
            "WORKING",
            "COMPLETED",
            "FAILED",
            "CANCELED",
            "INPUT_REQUIRED",
            "REJECTED",
            "AUTH_REQUIRED",
            "UNSPECIFIED",
        )
        for s in states:
            with self.subTest(s=s):
                obs = a2a(state=f"TASK_STATE_{s}")
                self.assertEqual(classify(obs), f"A2A_OBSERVED_TASK_STATE_{s}")
                envelope = make_dgaf_envelope(obs)
                self.assertEqual(envelope["request"]["requested_transition"], "RECORD_ONLY")
                result = validate_external_runtime_envelope(envelope, now=NOW)
                self.assertTrue(result["admitted"])
                self.assertEqual(result["authority_status"], "PRESENTED_NOT_GRANTED")
                self.assertEqual(result["dgaf_verification_class"], "UNVERIFIED_EXTERNAL_ASSERTION")

    def test_mcp_wire_requires_result_type(self):
        with self.assertRaises(ValueError):
            classify(mcp({"content": [], "isError": False}))

    def test_mcp_success_tool_error_protocol_error_are_distinct(self):
        self.assertEqual(classify(mcp()), "MCP_TOOL_RESULT_OBSERVED")
        self.assertEqual(
            classify(mcp({"resultType": "complete", "content": [], "isError": True})), "MCP_TOOL_ERROR_OBSERVED"
        )
        self.assertEqual(classify(mcp(error={"code": -32602, "message": "bad request"})), "MCP_PROTOCOL_ERROR_OBSERVED")
        self.assertEqual(classify(mcp({"resultType": "input_required"})), "MCP_INPUT_REQUIRED_OBSERVED")

    def test_protocol_completion_never_grants_execution(self):
        for obs in (a2a(state="TASK_STATE_COMPLETED"), mcp()):
            e = make_dgaf_envelope(obs)
            self.assertEqual(e["request"]["action_class"], "NON_CONSEQUENTIAL_RECORD_INGRESS")
            self.assertEqual(e["request"]["requested_transition"], "RECORD_ONLY")
            self.assertEqual(e["assertions"]["authority"]["status"], "EXTERNAL_OBSERVED_NOT_GRANTED")

    def test_unknown_version_and_legacy_state_rejected(self):
        for obs in (a2a(version="2.0.0"), a2a(state="working"), mcp(version="2025-11-25")):
            with self.assertRaises(ValueError):
                make_dgaf_envelope(obs)

    def test_external_provider_cannot_impersonate_dgaf(self):
        e = make_dgaf_envelope(a2a(provider_id="dgaf-superuser"))
        self.assertEqual(
            validate_external_runtime_envelope(e, now=NOW)["reason_codes"], ["DGAF_EXT_PROVIDER_SUBSTITUTION"]
        )

    def test_external_authority_claim_rejected(self):
        e = make_dgaf_envelope(a2a())
        e["assertions"]["authority"]["status"] = "DGAF_GRANTED"
        result = validate_external_runtime_envelope(e, now=NOW)
        self.assertFalse(result["admitted"])
        self.assertEqual(result["reason_codes"], ["DGAF_EXT_AUTHORITY_MISMATCH"])

    def test_digest_tampering_rejected(self):
        e = make_dgaf_envelope(a2a())
        e["evidence"]["payload"]["observed_state"] = "A2A_OBSERVED_TASK_STATE_COMPLETED"
        self.assertEqual(
            validate_external_runtime_envelope(e, now=NOW)["reason_codes"], ["DGAF_EXT_EVIDENCE_DIGEST_MISMATCH"]
        )

    def test_mutable_input_does_not_mutate_record(self):
        obs = a2a()
        e = make_dgaf_envelope(obs)
        baseline = copy.deepcopy(e)
        obs.payload["state"] = "TASK_STATE_FAILED"
        self.assertEqual(e, baseline)
        self.assertEqual(e["evidence"]["content_digest"], content_digest(e["evidence"]["payload"]))

    def test_stale_rejected_without_advancing_toy_state(self):
        gate = OrderingGate()
        self.assertFalse(
            gate.admit(a2a(), validate_external_runtime_envelope, now=NOW + timedelta(hours=2))["admitted"]
        )
        self.assertTrue(gate.admit(a2a(), validate_external_runtime_envelope, now=NOW)["admitted"])

    def test_replay_and_out_of_order_refused(self):
        gate = OrderingGate()
        self.assertTrue(gate.admit(a2a(seq=2), validate_external_runtime_envelope, now=NOW)["admitted"])
        for obs in (a2a(seq=2), a2a(seq=1), a2a(seq=3, effect_id="effect-akdc-2")):
            with self.assertRaises(ValueError):
                gate.admit(obs, validate_external_runtime_envelope, now=NOW)

    def test_terminal_a2a_task_cannot_resume(self):
        gate = OrderingGate()
        self.assertTrue(
            gate.admit(a2a(state="TASK_STATE_COMPLETED"), validate_external_runtime_envelope, now=NOW)["admitted"]
        )
        with self.assertRaises(ValueError):
            gate.admit(a2a(seq=2), validate_external_runtime_envelope, now=NOW)

    def test_event_collision_rejected(self):
        gate = OrderingGate()
        self.assertTrue(gate.admit(a2a(), validate_external_runtime_envelope, now=NOW)["admitted"])
        with self.assertRaises(ValueError):
            gate.admit(a2a(seq=2, event_id="evt-akdc-1"), validate_external_runtime_envelope, now=NOW)

    def test_same_input_is_digest_stable(self):
        obs = a2a()
        self.assertEqual(content_digest(make_dgaf_envelope(obs)), content_digest(make_dgaf_envelope(obs)))


if __name__ == "__main__":
    unittest.main()
