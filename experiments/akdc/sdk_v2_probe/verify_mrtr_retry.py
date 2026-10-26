"""Gate 12: independently classify the SDK's four real in-process MRTR wire pairs.

The trace is synthetic and read-only. An HMAC signature by the server is not
authentication of an external peer and cannot establish single-use effects.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from experiments.akdc.raw_wire_research import ReceiverWitness, normalize_mcp_tools_call
from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope

NOW = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)
TEST_KEY = b"AKDC-MRTR-TEST-ONLY-NO-SECRETS-2026-000000"


def main() -> None:
    evidence = Path(__file__).resolve().parent / "evidence"
    trace = json.loads((evidence / "sdk_mrtr_retry_synthetic.json").read_text(encoding="utf-8"))
    manifest = json.loads((evidence / "mrtr_retry_manifest.json").read_text(encoding="utf-8"))
    assert trace["negotiated_version"] == "2026-07-28"
    assert trace["fixture_data"] == "SYNTHETIC_ONLY"
    pairs = trace["raw_frame_pairs"]
    assert isinstance(pairs, list) and len(pairs) == 4
    expected = ["input_required", "protocol_error", "complete", "complete"]
    assert manifest["classifications"] == expected
    assert manifest["tampered_state_refused_before_handler"] is True
    assert manifest["valid_state_replay_accepted_negative_control"] is True

    states = [pair["request"]["params"].get("requestState") for pair in pairs]
    assert states[0] is None
    assert isinstance(states[1], str) and isinstance(states[2], str) and isinstance(states[3], str)
    assert states[1] != states[2]
    assert states[2] == states[3]  # signed MRTR state is replayable absent external one-time policy

    kinds = []
    for index, pair in enumerate(pairs, start=1):
        request, response = pair["request"], pair["response"]
        assert request["method"] == "tools/call"
        assert type(request["id"]) is type(response["id"]) and request["id"] == response["id"]
        witness = ReceiverWitness(
            provider_id="synthetic-official-sdk",
            runtime_id="local-sdk-v2-mrtr",
            source_id="test-inprocess-only",
            stream_id="one-session-no-network",
            receipt_number=index,
            observed_at="2026-10-26T12:00:00Z",
        )
        captured = normalize_mcp_tools_call(
            request,
            response,
            witness,
            negotiated_version="2026-07-28",
            capture_key=TEST_KEY,
            key_id="test-only-no-custody",
        )
        envelope = captured.record_only_envelope()
        validated = validate_external_runtime_envelope(envelope, now=NOW)
        assert validated["admitted"] is True
        assert validated["authority_status"] == "PRESENTED_NOT_GRANTED"
        safe = json.dumps(envelope)
        assert "SYNTHETIC-CONFIRMATION-ONLY" not in safe
        assert "Confirm a no-effect synthetic fixture" not in safe
        for state in states[1:]:
            assert state not in safe
        assert "inputResponses" not in safe
        category = "protocol_error" if "error" in response else response["result"]["resultType"]
        kinds.append(category)
    assert kinds == expected
    assert pairs[1]["response"]["error"]["code"] == -32602
    print("AKDC Gate 12 SDK MRTR retry -> four record-only DGAF observations PASS")
    print("Negative control: repeated valid requestState is not single-use; authorization NOT GRANTED")


if __name__ == "__main__":
    main()
