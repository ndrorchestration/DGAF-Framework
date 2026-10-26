"""AKDC Gate 8: bounded MCP evidence minimization; no privacy certification."""

import json
import unittest

from experiments.akdc.raw_wire_research import normalize_mcp_tools_call
from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope
from tests.test_akdc_raw_wire_research import NOW, mcp_req, mcp_resp, witness


class TestAKDCCaptureMinimization(unittest.TestCase):
    def capture(self, request=None, response=None):
        return normalize_mcp_tools_call(
            request if request is not None else mcp_req(),
            response if response is not None else mcp_resp(),
            witness(),
            negotiated_version="2026-07-28",
        )

    def assert_not_retained(self, captured, *secrets):
        text = json.dumps(captured.record_only_envelope())
        local = json.dumps(captured.observation.payload)
        for secret in secrets:
            self.assertNotIn(secret, text)
            self.assertNotIn(secret, local)

    def test_tool_text_arguments_and_structured_content_not_retained(self):
        req = mcp_req()
        req["params"]["arguments"] = {"token": "sensitive_request_0719"}
        resp = mcp_resp(
            result={
                "resultType": "complete",
                "content": [{"type": "text", "text": "sensitive_tool_output_3A12"}],
                "structuredContent": {"private": "secret_structured_1ABF"},
            }
        )
        captured = self.capture(request=req, response=resp)
        self.assert_not_retained(captured, "sensitive_request_0719", "sensitive_tool_output_3A12",
                                 "secret_structured_1ABF")
        self.assertEqual(captured.observation.payload["response"]["result"]["content"], [])
        evidence = captured.record_only_envelope()["evidence"]["payload"]
        self.assertEqual(evidence["capture_reference"]["retention_policy"], "CLASSIFICATION_ONLY_NO_RAW_CONTENT")
        self.assertTrue(validate_external_runtime_envelope(captured.record_only_envelope(), now=NOW)["admitted"])

    def test_protocol_error_text_and_data_not_retained(self):
        resp = mcp_resp(error={"code": -32602, "message": "error_secret_1ABC",
                               "data": {"auth": "error_data_secret_5F21"}})
        captured = self.capture(response=resp)
        self.assert_not_retained(captured, "error_secret_1ABC", "error_data_secret_5F21")
        self.assertEqual(captured.observation.payload["response"]["error"]["code"], -32602)
        self.assertTrue(validate_external_runtime_envelope(captured.record_only_envelope(), now=NOW)["admitted"])

    def test_mrtr_state_and_input_request_names_not_retained(self):
        resp = mcp_resp(result={
            "resultType": "input_required",
            "requestState": "mrtr_secret_6621",
            "inputRequests": {"user_private_id": {"method": "sampling/createMessage"}},
        })
        captured = self.capture(response=resp)
        self.assert_not_retained(captured, "mrtr_secret_6621", "user_private_id", "sampling/createMessage")
        self.assertTrue(validate_external_runtime_envelope(captured.record_only_envelope(), now=NOW)["admitted"])

    def test_raw_request_id_is_not_persisted(self):
        req = mcp_req()
        resp = mcp_resp()
        req["id"] = "sensitive_req_id_314159"
        resp["id"] = req["id"]
        captured = self.capture(request=req, response=resp)
        self.assert_not_retained(captured, "sensitive_req_id_314159")
        self.assertTrue(captured.observation.payload["response"]["id"].startswith("correlation-"))

    def test_non_object_arguments_rejected(self):
        req = mcp_req()
        req["params"]["arguments"] = ["not-object"]
        with self.assertRaisesRegex(ValueError, "arguments must be object"):
            self.capture(request=req)

    def test_invalid_request_state_type_rejected(self):
        req = mcp_req()
        req["params"]["requestState"] = 123
        with self.assertRaisesRegex(ValueError, "requestState must be string"):
            self.capture(request=req)

    def test_malformed_content_blocks_rejected(self):
        for bad in (7, {"type": "text"}, {"type": "image", "data": "abc"},
                    {"type": "unknown", "text": "raw"}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.capture(response=mcp_resp(result={"resultType": "complete", "content": [bad]}))

    def test_different_input_creates_different_capture_digest_without_retention(self):
        a, b = mcp_req(), mcp_req()
        a["params"]["arguments"] = {"value": "secret_A"}
        b["params"]["arguments"] = {"value": "secret_B"}
        first, second = self.capture(request=a), self.capture(request=b)
        self.assertNotEqual(first.canonical_frame_digest, second.canonical_frame_digest)
        self.assertNotEqual(first.observation.event_id, second.observation.event_id)
        self.assert_not_retained(first, "secret_A")
        self.assert_not_retained(second, "secret_B")


if __name__ == "__main__":
    unittest.main()
