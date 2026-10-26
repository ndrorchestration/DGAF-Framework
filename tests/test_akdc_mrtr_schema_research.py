"""MCP July 2026 MRTR counterexamples: structural fixture, not SDK conformance."""

import unittest

from test_akdc_raw_wire_research import TEST_CAPTURE_KEY, TEST_KEY_ID

from experiments.akdc.akdc_ingress_bridge import ProtocolObservation, classify
from experiments.akdc.raw_wire_research import ReceiverWitness, normalize_mcp_tools_call


def _fixture(result):
    response = {"jsonrpc": "2.0", "id": 1, "result": result}
    observation = ProtocolObservation(
        protocol="mcp",
        version="2026-07-28",
        provider_id="external-test",
        runtime_id="runtime-test",
        source_id="source-test",
        event_id="event-one",
        effect_id="effect-one",
        observed_at="2026-10-26T12:00:00Z",
        payload={"method": "tools/call", "response": response},
    )
    witness = ReceiverWitness(
        provider_id="external-test",
        runtime_id="runtime-test",
        source_id="source-test",
        stream_id="receiver-stream",
        receipt_number=1,
        observed_at="2026-10-26T12:00:00Z",
    )
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"_meta": {}, "name": "fixture", "arguments": {}},
    }
    return observation, witness, request, response


def _both_layers(result):
    observation, witness, request, response = _fixture(result)
    return [
        lambda: classify(observation),
        lambda: normalize_mcp_tools_call(
            request,
            response,
            witness,
            negotiated_version="2026-07-28",
            capture_key=TEST_CAPTURE_KEY,
            key_id=TEST_KEY_ID,
        ),
    ]


class TestMCPInputRequiredRequiredFields(unittest.TestCase):
    def test_bare_discriminator_fails_closed(self):
        for parser in _both_layers({"resultType": "input_required"}):
            with self.assertRaisesRegex(ValueError, "inputRequests or requestState"):
                parser()

    def test_opaque_request_state_supported_as_unverified_observation(self):
        for parser in _both_layers({"resultType": "input_required", "requestState": "opaque"}):
            self.assertIsNotNone(parser())

    def test_input_requests_structural_subset_supported(self):
        # Nested InputRequest type/capability validation is out of scope.
        for parser in _both_layers({"resultType": "input_required", "inputRequests": {}}):
            self.assertIsNotNone(parser())

    def test_malformed_and_hybrid_fields_fail_closed(self):
        invalid = [
            {"resultType": "input_required", "requestState": 123},
            {"resultType": "input_required", "inputRequests": []},
            {"resultType": "input_required", "requestState": "opaque", "content": []},
        ]
        for result in invalid:
            for parser in _both_layers(result):
                with self.subTest(result=result), self.assertRaises(ValueError):
                    parser()


if __name__ == "__main__":
    unittest.main()
