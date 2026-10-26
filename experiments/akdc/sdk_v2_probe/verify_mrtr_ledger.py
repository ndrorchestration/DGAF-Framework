"""Gate 13 official SDK/SQLite fixture evidence -> DGAF record-only integration.

No external principal validation, action execution, production key custody or
independent network trace. All source fields are synthetic and unverified.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from experiments.akdc.raw_wire_research import ReceiverWitness, normalize_mcp_tools_call
from scripts.validate_external_runtime_adapter import validate_external_runtime_envelope

NOW = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)
TEST_CAPTURE_KEY = b"AKDC-SYNTHETIC-G13-FIXTURE-NO-CUSTODY-0001"


def main() -> None:
    root = Path(__file__).resolve().parent / "evidence"
    raw = (root / "sdk_mrtr_ledger_synthetic.json").read_bytes()
    wire = json.loads(raw)
    manifest = json.loads((root / "mrtr_ledger_manifest.json").read_text(encoding="utf-8"))
    assert hashlib.sha256(raw).hexdigest() == manifest["wire_sha256"]
    assert wire["negotiated_version"] == "2026-07-28"
    assert wire["authority"] == manifest["authority"] == "NOT_GRANTED"
    pairs = wire["raw_frame_pairs"]
    assert len(pairs) == manifest["request_count"] == 8
    expected = ["input_required", "protocol_error"] + ["complete"] * 6
    assert manifest["categories"] == expected
    assert manifest["persistent_receipts"] == 1
    assert manifest["ledger_first_records"] == 1
    assert manifest["ledger_duplicate_records"] == 5

    classified = []
    for index, pair in enumerate(pairs, 1):
        request, response = pair["request"], pair["response"]
        assert request["method"] == "tools/call"
        assert request["id"] == response["id"] and type(request["id"]) is type(response["id"])
        witness = ReceiverWitness(
            provider_id="synthetic-sdk-gate13",
            runtime_id="in-process-fixture-g13",
            source_id="local-test-only",
            stream_id="in-process-fixture",
            receipt_number=index,
            observed_at="2026-10-26T12:00:00Z",
        )
        captured = normalize_mcp_tools_call(
            request, response, witness,
            negotiated_version="2026-07-28",
            capture_key=TEST_CAPTURE_KEY,
            key_id="fixture-not-trusted",
        )
        envelope = captured.record_only_envelope()
        validation = validate_external_runtime_envelope(envelope, now=NOW)
        assert validation["admitted"] is True
        assert validation["authority_status"] == "PRESENTED_NOT_GRANTED"
        assert validation["requested_transition"] == "RECORD_ONLY"
        saved = json.dumps(envelope)
        assert "SYNTHETIC-RECORD-ONLY-COMPLETE" not in saved
        assert "inputResponses" not in saved
        assert "Accept synthetic no-effect fixture only?" not in saved
        for other in pairs[1:]:
            signed = other["request"]["params"].get("requestState")
            if signed:
                assert signed not in saved
        category = "protocol_error" if "error" in response else response["result"]["resultType"]
        classified.append(category)
    assert classified == expected
    assert pairs[1]["response"]["error"]["code"] == -32602
    print("AKDC Gate 13 SDK eight pairs -> only DGAF record receipts VERIFIED")
    print("One atomic fixture receipt, five duplicate receipts, zero verified identity or effects")


if __name__ == "__main__":
    main()
