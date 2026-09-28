"""Live bounded verification for the Tektite DGAF proof-of-operation.

This script runs only against an already deployed DGAF runtime and preserves the
first observed response for each declared demo scenario. It does not repair,
retry, or promote failed results.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import httpx

SCENARIOS = {
    "authorized": {
        "first_status": "updated",
        "first_reason": None,
        "attempts": 1,
        "receipt": True,
    },
    "revoked": {
        "first_status": "denied",
        "first_reason": "AUTHORIZATION_REVOKED",
        "attempts": 1,
        "receipt": False,
    },
    "missing_scope": {
        "first_status": "denied",
        "first_reason": "REQUIRED_SCOPE_MISSING",
        "attempts": 1,
        "receipt": False,
    },
    "tampered_action": {
        "first_status": "denied",
        "first_reason": "ACTION_DIGEST_MISMATCH",
        "attempts": 1,
        "receipt": False,
    },
    "replay": {
        "first_status": "updated",
        "first_reason": None,
        "attempts": 2,
        "receipt": True,
        "second_status": "denied",
        "second_reason": "AAR_REPLAY",
    },
}

EXPECTED_BOUNDARY = {
    "scientific_n_increment": 0,
    "independent_validation": "NOT_ESTABLISHED",
    "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    "high_assurance": "NOT_AUTHORIZED",
    "demo_effect": "NON_SCIENTIFIC_EPHEMERAL_AUDIT_COUNTER_UPDATE_ONLY",
}


def main() -> int:
    base_url = os.environ["DGAF_URL"].rstrip("/")
    bypass = os.environ["VERCEL_AUTOMATION_BYPASS_SECRET"]
    source = os.environ.get("GITHUB_SHA", "UNKNOWN")
    headers = {
        "content-type": "application/json",
        "x-vercel-protection-bypass": bypass,
    }

    evidence: dict[str, object] = {
        "evidence_class": "TEKTITE_PROOF_OF_OPERATION_V1",
        "source_commit": source,
        "deployment_url": base_url,
        "scenarios": {},
        "claim_boundary": EXPECTED_BOUNDARY,
        "result": "FAIL",
    }

    failures: list[str] = []
    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        for scenario, expected in SCENARIOS.items():
            response = client.post(
                f"{base_url}/api/tektite-demo",
                headers=headers,
                json={"scenario": scenario},
            )
            observed: dict[str, object] = {
                "http_status": response.status_code,
                "body": None,
            }
            try:
                body = response.json()
            except Exception:
                body = {"_raw": response.text}
            observed["body"] = body
            evidence["scenarios"][scenario] = observed  # type: ignore[index]

            if response.status_code != 200:
                failures.append(f"{scenario}: HTTP {response.status_code}")
                continue
            if body.get("claim_boundary") != EXPECTED_BOUNDARY:
                failures.append(f"{scenario}: claim boundary mismatch")
                continue

            attempts = body.get("attempts")
            if not isinstance(attempts, list) or len(attempts) != expected["attempts"]:
                failures.append(f"{scenario}: attempt count mismatch")
                continue

            first = attempts[0].get("result", {}) if attempts else {}
            if first.get("status") != expected["first_status"]:
                failures.append(f"{scenario}: first status {first.get('status')!r}")
            if first.get("reason") != expected["first_reason"]:
                failures.append(f"{scenario}: first reason {first.get('reason')!r}")

            receipt = first.get("execution_receipt")
            if expected["receipt"]:
                if not isinstance(receipt, dict):
                    failures.append(f"{scenario}: execution receipt missing")
                elif receipt.get("postcondition") != "VERIFIED":
                    failures.append(f"{scenario}: postcondition not VERIFIED")
            elif receipt is not None:
                failures.append(f"{scenario}: denial unexpectedly emitted receipt")

            if scenario == "replay" and len(attempts) == 2:
                second = attempts[1].get("result", {})
                if second.get("status") != expected["second_status"]:
                    failures.append(f"{scenario}: second status {second.get('status')!r}")
                if second.get("reason") != expected["second_reason"]:
                    failures.append(f"{scenario}: second reason {second.get('reason')!r}")

    evidence["failures"] = failures
    evidence["result"] = "PASS" if not failures else "FAIL"
    Path("tektite_proof_of_operation.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
