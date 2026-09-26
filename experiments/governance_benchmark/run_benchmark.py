"""Deterministic first-slice governance comparison.

This is synthetic engineering evidence only. It does not establish DGAF efficacy,
state-of-the-art status, independent validation, or scientific evidence.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent
DEFAULT_FIXTURES = ROOT / "fixtures_v1.json"


def policy_as_code(case: dict[str, Any]) -> tuple[str, list[str]]:
    """Baseline C: action-level allow/deny policy only."""
    steps: list[str] = []
    action = case["action"]

    steps.append("CHECK_AUTHORIZED")
    if not action["authorized"]:
        return "DENY", steps

    steps.append("CHECK_TOOL")
    if not action["tool_allowed"]:
        return "DENY", steps

    steps.append("CHECK_TARGET")
    if not action["target_allowed"]:
        return "DENY", steps

    return "ALLOW", steps


def dgaf(case: dict[str, Any]) -> tuple[str, list[str]]:
    """Baseline D: action admission plus epistemic/composition guards."""
    action_decision, steps = policy_as_code(case)
    steps = list(steps)

    if action_decision != "ALLOW":
        return action_decision, steps

    claim = case.get("claim")
    if claim is not None:
        steps.append("CHECK_CLAIM_EVIDENCE")
        if not claim["evidence_present"] or not claim["evidence_fresh"]:
            return "DENY", steps

        steps.append("CHECK_VERIFICATION_CLASS")
        if (
            claim["requested_status"] == "INDEPENDENT_VALIDATION_ESTABLISHED"
            and claim["verification_class"] != "INDEPENDENT"
        ):
            return "DENY", steps

    flow = case.get("flow")
    if flow is not None:
        steps.append("CHECK_FLOW_PROVENANCE")
        if not flow["provenance_known"]:
            return "DENY", steps

        steps.append("CHECK_COMPOSED_AUTHORITY")
        protected_egress = (
            flow["source_classification"] in {"CONFIDENTIAL", "RESTRICTED"}
            and flow["destination_class"] == "EXTERNAL"
        )
        if protected_egress and not flow["composition_authorized"]:
            return "DENY", steps

    return "ALLOW", steps


BASELINES: dict[str, Callable[[dict[str, Any]], tuple[str, list[str]]]] = {
    "C_POLICY_AS_CODE": policy_as_code,
    "D_DGAF": dgaf,
}


def classify(case: dict[str, Any], decision: str) -> dict[str, int]:
    expected = case["expected_safe_outcome"]
    unsafe_admit = int(expected == "DENY" and decision == "ALLOW")
    false_block = int(expected == "ALLOW" and decision == "DENY")
    unsupported_claim_admit = int(
        case["family"] == "epistemic_authority" and unsafe_admit
    )
    return {
        "unsafe_action_or_flow_admitted": unsafe_admit,
        "unsupported_claim_admitted": unsupported_claim_admit,
        "false_block": false_block,
        "task_correct": int(decision == expected),
    }


def run(fixtures_path: Path = DEFAULT_FIXTURES) -> dict[str, Any]:
    payload = json.loads(fixtures_path.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []

    for case in payload["cases"]:
        for baseline_id, decision_fn in BASELINES.items():
            started = time.perf_counter_ns()
            decision, steps = decision_fn(case)
            elapsed_ns = time.perf_counter_ns() - started
            row = {
                "case_id": case["id"],
                "family": case["family"],
                "baseline": baseline_id,
                "decision": decision,
                "expected_safe_outcome": case["expected_safe_outcome"],
                "decision_steps": steps,
                "decision_step_count": len(steps),
                "elapsed_ns_informational": elapsed_ns,
            }
            row.update(classify(case, decision))
            results.append(row)

    summary: dict[str, dict[str, int]] = {}
    for baseline_id in BASELINES:
        rows = [row for row in results if row["baseline"] == baseline_id]
        summary[baseline_id] = {
            "cases": len(rows),
            "task_correct": sum(row["task_correct"] for row in rows),
            "unsafe_action_or_flow_admitted": sum(
                row["unsafe_action_or_flow_admitted"] for row in rows
            ),
            "unsupported_claim_admitted": sum(
                row["unsupported_claim_admitted"] for row in rows
            ),
            "false_block": sum(row["false_block"] for row in rows),
            "decision_steps": sum(row["decision_step_count"] for row in rows),
        }

    return {
        "benchmark_version": payload["version"],
        "evidence_class": payload["status"],
        "claim_ceiling": [
            "SYNTHETIC_ENGINEERING_EVIDENCE_ONLY",
            "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED",
            "INDEPENDENT_VALIDATION_NOT_ESTABLISHED",
            "STATE_OF_THE_ART_NOT_ESTABLISHED",
        ],
        "results": results,
        "summary": summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = run(args.fixtures)
    encoded = json.dumps(report, indent=2, sort_keys=True)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
