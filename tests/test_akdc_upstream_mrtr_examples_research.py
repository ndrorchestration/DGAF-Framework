"""Source-pinned MCP MRTR golden examples, not live SDK traces."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from typing import Any

from test_akdc_raw_wire_research import (
    NOW,
    TEST_CAPTURE_KEY,
    TEST_KEY_ID,
    mcp_req,
    witness,
)

from experiments.akdc.mrtr_upstream_fixture_research import observe_mrtr_example
from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope

FIXTURE_DIR = Path(__file__).resolve().parents[1] / "experiments/akdc/fixtures/mcp-2026-07-28"
UPSTREAM_SHA = {
    "input-required-result-with-request-state-only.json": "7f1dec1f69d35db2428079a52911ade51f86451f",
    "input-required-result-with-elicitation-and-sampling-and-request-state.json": (
        "6ffc95394446982b375e13c4bf6a23eb4e3d7ced"
    ),
}
ALL_DECLARED = frozenset({"elicitation/create", "sampling/createMessage"})


def load_example(name: str) -> dict[str, Any]:
    raw = (FIXTURE_DIR / name).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
    if blob != UPSTREAM_SHA[name]:
        raise ValueError("upstream published fixture Git blob digest mismatch")
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise ValueError("upstream example is not JSON object")
    return obj


def captured(result: dict[str, Any], declared: frozenset[str] = frozenset()):
    return observe_mrtr_example(
        mcp_req(),
        {"jsonrpc": "2.0", "id": 1, "result": result},
        witness(),
        negotiated_version="2026-07-28",
        capture_key=TEST_CAPTURE_KEY,
        key_id=TEST_KEY_ID,
        declared_methods=declared,
    )


class TestUpstreamMRTROnly(unittest.TestCase):
    def test_published_git_blobs_match_exact_source(self):
        for name in UPSTREAM_SHA:
            with self.subTest(name=name):
                self.assertEqual(load_example(name)["resultType"], "input_required")

    def test_published_request_state_only_is_observed_without_capabilities(self):
        result = load_example("input-required-result-with-request-state-only.json")
        x = captured(result)
        self.assertTrue(validate_external_runtime_envelope(x.record_only_envelope(), now=NOW)["admitted"])
        self.assertEqual(x.observation.payload["response"]["result"]["requestState"], "REDACTED")

    def test_published_mixed_example_fails_closed_without_capabilities(self):
        result = load_example("input-required-result-with-elicitation-and-sampling-and-request-state.json")
        with self.assertRaisesRegex(ValueError, "not declared"):
            captured(result)

    def test_published_mixed_example_requires_both_methods(self):
        result = load_example("input-required-result-with-elicitation-and-sampling-and-request-state.json")
        with self.assertRaisesRegex(ValueError, "not declared"):
            captured(result, frozenset({"elicitation/create"}))

    def test_published_mixed_example_only_with_declared_methods_recorded(self):
        result = load_example("input-required-result-with-elicitation-and-sampling-and-request-state.json")
        x = captured(result, ALL_DECLARED)
        record = json.dumps(x.record_only_envelope())
        self.assertNotIn("Please provide your GitHub username", record)
        self.assertNotIn("capital_of_france", record)
        self.assertNotIn(result["requestState"], record)
        self.assertTrue(validate_external_runtime_envelope(x.record_only_envelope(), now=NOW)["admitted"])

    def test_unknown_method_is_refused_even_when_declared(self):
        result = {"resultType": "input_required", "inputRequests": {"x": {"method": "private/unsafe", "params": {}}}}
        with self.assertRaisesRegex(ValueError, "unsupported"):
            captured(result, frozenset({"private/unsafe"}))

    def test_malformed_nested_input_request_is_refused(self):
        result = {"resultType": "input_required", "inputRequests": {"x": {"method": "elicitation/create"}}}
        with self.assertRaisesRegex(ValueError, "params"):
            captured(result, ALL_DECLARED)

    def test_declared_methods_requires_explicit_frozenset(self):
        result = load_example("input-required-result-with-request-state-only.json")
        with self.assertRaisesRegex(ValueError, "frozenset"):
            captured(result, {"elicitation/create"})  # type: ignore[arg-type]

    def test_opaque_state_changes_hmac_without_retaining_it(self):
        result = load_example("input-required-result-with-request-state-only.json")
        first = captured(result)
        changed = dict(result, requestState="STATE-WAS-CHANGED")
        second = captured(changed)
        self.assertNotEqual(first.canonical_frame_digest, second.canonical_frame_digest)
        self.assertNotIn("STATE-WAS-CHANGED", json.dumps(second.record_only_envelope()))

    def test_fixture_rejects_non_mrtr_complete_result(self):
        with self.assertRaisesRegex(ValueError, "input_required"):
            captured({"resultType": "complete", "content": []})


if __name__ == "__main__":
    unittest.main()
