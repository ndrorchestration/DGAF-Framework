"""Validate actual official SDK v2 in-process frames through Gate 9 AKDC ingress.

No network peer, no real tool effect, no trusted or scientific observation.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from experiments.akdc.raw_wire_research import ReceiverWitness, normalize_mcp_tools_call
from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope

NOW = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)
TEST_ONLY_CAPTURE_KEY = b"AKDC-SDK-SYNTHETIC-FIXTURE-NOT-SECRET-2026"


def main() -> None:
    path = Path(__file__).with_name("evidence") / "sdk_wire_synthetic.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("negotiated_version") != "2026-07-28":
        raise AssertionError("SDK did not negotiate pinned version")
    pairs = raw.get("framePairs")
    if not isinstance(pairs, list) or len(pairs) != 2:
        raise AssertionError("expected two official SDK tools/call wire captures")
    seen = set()
    for index, pair in enumerate(pairs, start=1):
        if not isinstance(pair, dict):
            raise AssertionError("bad wire pair")
        request, response = pair["request"], pair["response"]
        if request["id"] != response["id"] or request["method"] != "tools/call":
            raise AssertionError("raw SDK request/response mismatch")
        name = request["params"]["name"]
        if name not in {"akdc-read-only", "akdc-mrtr-state-only"}:
            raise AssertionError("unexpected SDK wire fixture tool")
        seen.add(name)
        witness = ReceiverWitness(
            provider_id="synthetic-sdk-probe",
            runtime_id="inprocess-2026-07-28",
            source_id="local-test-only",
            stream_id="single-test-session",
            receipt_number=index,
            observed_at="2026-10-26T12:00:00Z",
        )
        observed = normalize_mcp_tools_call(
            request, response, witness, negotiated_version="2026-07-28",
            capture_key=TEST_ONLY_CAPTURE_KEY, key_id="test-ephemeral-not-secret",
        )
        result = validate_external_runtime_envelope(observed.record_only_envelope(), now=NOW)
        if not result["admitted"] or result["authority_status"] != "PRESENTED_NOT_GRANTED":
            raise AssertionError("DGAF ingress denied SDK-derived record-only observation")
        normalized = json.dumps(observed.record_only_envelope())
        if "TEST-FIXTURE-COMPLETE" in normalized or "SYNTHETIC-MRTR-STATE-ONLY" in normalized:
            raise AssertionError("raw SDK test content leaked into DGAF minimized record")
    if seen != {"akdc-read-only", "akdc-mrtr-state-only"}:
        raise AssertionError("both SDK wire modes not observed")
    print("AKDC SDK v2 -> record-only DGAF ingress: two synthetic in-process pairs PASSED")


if __name__ == "__main__":
    main()
