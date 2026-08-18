#!/usr/bin/env python3
"""P2 live runtime behavior matrix for DGAF /api/orchestrate.

Usage:
  python scripts/p2_runtime_matrix.py https://example.test

The runner records exact request/response metadata and never promotes a
result to VERIFIED by itself. Use the generated JSON as execution evidence.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from http.client import RemoteDisconnected
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


CASES = [
    {
        "id": "case-1-valid-audit-missing",
        "payload": {"mandate": "P2 live verification", "turn": 0},
        "expected_status": 503,
        "expected_decision": "BLOCKED",
    },
    {
        "id": "case-2-invalid-body-shape",
        "payload": {"foo": "bar"},
        "expected_status": 400,
        "expected_decision": "REJECT",
    },
    {
        "id": "case-3-confidence-out-of-range",
        "payload": {"mandate": "P2 live verification", "confidence": 2.0},
        "expected_status": 400,
        "expected_decision": "REJECT",
    },
    {
        "id": "case-4-invalid-turn",
        "payload": {"mandate": "P2 live verification", "turn": -1},
        "expected_status": 400,
        "expected_decision": "REJECT",
    },
]


def request_json(url: str, payload: dict) -> tuple[int, str, dict | None]:
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = None
            return response.status, raw, parsed
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = None
        return exc.code, raw, parsed
    except (URLError, RemoteDisconnected, TimeoutError) as exc:
        return 0, f"transport_error: {exc}", None


def request_malformed_json(url: str) -> tuple[int, str, dict | None]:
    request = Request(
        url,
        data=b"{",
        method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = None
            return response.status, raw, parsed
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = None
        return exc.code, raw, parsed
    except (URLError, RemoteDisconnected, TimeoutError) as exc:
        return 0, f"transport_error: {exc}", None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url", help="Base URL of a running DGAF deployment")
    parser.add_argument(
        "--output",
        default="artifacts/p2_runtime_matrix.json",
        help="Evidence JSON output path",
    )
    parser.add_argument("--commit", default="unknown")
    parser.add_argument("--environment", default="unknown")
    args = parser.parse_args()

    endpoint = args.base_url.rstrip("/") + "/api/orchestrate"
    started = datetime.now(timezone.utc).isoformat()
    results: list[dict] = []

    for case in CASES:
        ts = datetime.now(timezone.utc).isoformat()
        status, raw, parsed = request_json(endpoint, case["payload"])
        decision = parsed.get("decision") if isinstance(parsed, dict) else None
        passed = status == case["expected_status"] and decision == case["expected_decision"]
        results.append(
            {
                "case_id": case["id"],
                "timestamp": ts,
                "request": case["payload"],
                "expected": {
                    "status": case["expected_status"],
                    "decision": case["expected_decision"],
                },
                "actual": {
                    "status": status,
                    "decision": decision,
                    "body": parsed if parsed is not None else raw,
                },
                "passed": passed,
            }
        )
        print(
            f"{'PASS' if passed else 'FAIL'} {case['id']}: "
            f"expected {case['expected_status']}/{case['expected_decision']} "
            f"got {status}/{decision}"
        )

    malformed_timestamp = datetime.now(timezone.utc).isoformat()
    status, raw, parsed = request_malformed_json(endpoint)
    malformed_decision = parsed.get("decision") if isinstance(parsed, dict) else None
    malformed_passed = status == 400 and malformed_decision == "REJECT"
    results.append(
        {
            "case_id": "case-5-malformed-json",
            "timestamp": malformed_timestamp,
            "request_raw": "{",
            "expected": {"status": 400, "decision": "REJECT"},
            "actual": {
                "status": status,
                "decision": malformed_decision,
                "body": parsed if parsed is not None else raw,
            },
            "passed": malformed_passed,
        }
    )
    print(
        f"{'PASS' if malformed_passed else 'FAIL'} case-5-malformed-json: "
        f"expected 400/REJECT got {status}/{malformed_decision}"
    )

    payload = {
        "evidence_class": "P2_RUNTIME_MATRIX_EXECUTION",
        "status": "PASS" if all(item["passed"] for item in results) else "FAIL",
        "execution": {
            "started_at": started,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "base_url": args.base_url,
            "endpoint": endpoint,
            "environment": args.environment,
            "commit": args.commit,
        },
        "cases": results,
        "epistemic_boundary": "Execution evidence applies only to this endpoint, deployment, environment, and commit; it does not establish broad DGAF efficacy.",
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Evidence written to {output}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
