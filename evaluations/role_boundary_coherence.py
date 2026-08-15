"""Repository-native deterministic evaluator for Issue #32, first slice.

This evaluator scores a fixture corpus; it does not claim model or real-workload
performance. The fixture's expected roles are independent ground truth, while
predictions are an explicit adapter input so the evaluator can later be wired to
an actual DGAF/model run without changing the scoring contract.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

TARGET = 0.95
DEFAULT_FIXTURE = Path(__file__).parent / "fixtures" / "role_boundary_coherence_v1.json"


def load_fixture(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("evaluation") != "role_boundary_coherence":
        raise ValueError("fixture evaluation must be role_boundary_coherence")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("fixture must contain a non-empty cases list")
    protocol = data.get("protocol", {})
    if protocol.get("trace_length") != 50 or protocol.get("probe_turn") != 48:
        raise ValueError("fixture protocol must use the canonical 50-turn / turn-48 probe")
    for case in cases:
        if not {"id", "expected_role", "predicted_role"}.issubset(case):
            raise ValueError(f"invalid case: {case!r}")
    return data


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(path: Path) -> dict:
    fixture = load_fixture(path)
    cases = fixture["cases"]
    results = []
    correct = 0
    for case in cases:
        passed = case["predicted_role"] == case["expected_role"]
        correct += int(passed)
        results.append(
            {
                "id": case["id"],
                "expected_role": case["expected_role"],
                "predicted_role": case["predicted_role"],
                "correct": passed,
            }
        )

    score = correct / len(cases)
    return {
        "schema_version": "1.0",
        "evaluation": "role_boundary_coherence",
        "evidence_class": fixture["evidence_class"],
        "fixture_version": fixture["fixture_version"],
        "fixture_sha256": sha256_file(path),
        "provenance": fixture["provenance"],
        "protocol": fixture["protocol"],
        "sample_count": len(cases),
        "correct_count": correct,
        "score": score,
        "target": TARGET,
        "passed": score >= TARGET,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "failure_analysis": [r for r in results if not r["correct"]],
        "cases": results,
        "limitations": [
            "Synthetic repository fixture only; not real-world workload evidence.",
            "Predictions are fixture inputs until an actual DGAF/model adapter is wired.",
            "No external benchmark score is used as validation evidence.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = evaluate(args.fixture)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
