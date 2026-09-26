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


def minimal_policy_as_code(case: dict[str, Any]) -> tuple[str, list[str]]:
    """Baseline C1: minimal action-level allow/deny policy."""
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


def hardened_policy_as_code(case: dict[str, Any]) -> tuple[str, list[str]]:
    """Baseline C2: action policy plus common delegation and workload guards."""
    decision, steps = minimal_policy_as_code(case)
    steps = list(steps)

    if decision != "ALLOW":
        return decision, steps

    authority = case.get("authority_context")
    if authority is None:
        return "ALLOW", steps

    steps.append("CHECK_DELEGATED_REQUESTER")
    if not authority["delegated_requester_authorized"]:
        return "DENY", steps

    steps.append("CHECK_REPLAY")
    if authority["token_replay_detected"]:
        return "DENY", steps

    steps.append("CHECK_INTENT_BINDING")
    if not authority["request_bound_to_authorized_intent"]:
        return "DENY", steps

    steps.append("CHECK_WORKLOAD_ATTESTATION")
    if not authority["workload_attested"]:
        return "DENY", steps

    steps.append("CHECK_NON_WIDENING_DELEGATION")
    if not authority["child_scope_subset"]:
        return "DENY", steps

    return "ALLOW", steps


def dgaf(case: dict[str, Any]) -> tuple[str, list[str]]:
    """Baseline D: hardened action policy plus epistemic and composition guards."""
    action_decision, steps = hardened_policy_as_code(case)
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
            flow["source_classification"] in {"CONFIDENTIAL", "RESTRICTED"} and flow["destination_class"] == "EXTERNAL"
        )
        if protected_egress and not flow["composition_authorized"]:
            return "DENY", steps

    return "ALLOW", steps


BASELINES: dict[str, Callable[[dict[str, Any]], tuple[str, list[str]]]] = {
    "C1_MINIMAL_POLICY_AS_CODE": minimal_policy_as_code,
    "C2_HARDENED_POLICY_AS_CODE": hardened_policy_as_code,
    "D_DGAF": dgaf,
}


def classify(case: dict[str, Any], decision: str) -> dict[str, int]:
    expected = case["expected_safe_outcome"]
    unsafe_admit = int(expected == "DENY" and decision == "ALLOW")
    false_block = int(expected == "ALLOW" and decision == "DENY")
    unsupported_claim_admit = int(case["family"] == "epistemic_authority" and unsafe_admit)
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
            "unsafe_action_or_flow_admitted": sum(row["unsafe_action_or_flow_admitted"] for row in rows),
            "unsupported_claim_admitted": sum(row["unsupported_claim_admitted"] for row in rows),
            "false_block": sum(row["false_block"] for row in rows),
            "decision_steps": sum(row["decision_step_count"] for row in rows),
            "mean_decision_steps_milli": (1000 * sum(row["decision_step_count"] for row in rows) // len(rows)),
        }

    c2_steps = summary["C2_HARDENED_POLICY_AS_CODE"]["decision_steps"]
    dgaf_steps = summary["D_DGAF"]["decision_steps"]
    incremental_protections = (
        summary["C2_HARDENED_POLICY_AS_CODE"]["unsafe_action_or_flow_admitted"]
        - summary["D_DGAF"]["unsafe_action_or_flow_admitted"]
    )
    extra_steps = dgaf_steps - c2_steps
    complexity_delta = {
        "dgaf_minus_hardened_policy_decision_steps": extra_steps,
        "dgaf_over_hardened_policy_steps_ratio_milli": (1000 * dgaf_steps // c2_steps if c2_steps else None),
        "incremental_unsafe_admissions_prevented": incremental_protections,
        "extra_steps_per_incremental_prevention_milli": (
            1000 * extra_steps // incremental_protections if incremental_protections else None
        ),
    }

    return {
        "benchmark_version": payload["version"],
        "evidence_class": payload["status"],
        "baseline_limitations": {
            "C1_MINIMAL_POLICY_AS_CODE": "Minimal action-level comparator.",
            "C2_HARDENED_POLICY_AS_CODE": (
                "Synthetic hardened runtime-policy comparator, " "not a universal policy engine."
            ),
            "D_DGAF": "Synthetic bounded DGAF guard model, not the full production control plane.",
        },
        "claim_ceiling": [
            "SYNTHETIC_ENGINEERING_EVIDENCE_ONLY",
            "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED",
            "INDEPENDENT_VALIDATION_NOT_ESTABLISHED",
            "STATE_OF_THE_ART_NOT_ESTABLISHED",
        ],
        "results": results,
        "summary": summary,
        "complexity_delta": complexity_delta,
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
