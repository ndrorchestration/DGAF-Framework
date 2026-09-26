"""Deterministic metamorphic mutations for the governance benchmark.

Mutations begin from legitimate seed cases and change one governance predicate
at a time. This is synthetic engineering evidence only.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures_v1.json"
RUNNER = ROOT / "run_benchmark.py"

spec = importlib.util.spec_from_file_location("governance_benchmark_runner", RUNNER)
assert spec and spec.loader
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

BASELINES = runner.BASELINES


def load_cases() -> dict[str, dict[str, Any]]:
    payload = json.loads(FIXTURES.read_text(encoding="utf-8"))
    return {case["id"]: case for case in payload["cases"]}


def authority_mutations(seed: dict[str, Any]) -> list[dict[str, Any]]:
    fields = {
        "delegated_requester_authorized": False,
        "token_replay_detected": True,
        "request_bound_to_authorized_intent": False,
        "workload_attested": False,
        "child_scope_subset": False,
    }
    mutations: list[dict[str, Any]] = []
    for field, value in fields.items():
        case = copy.deepcopy(seed)
        case["mutation_id"] = f"M-AUTH-{field}"
        case["mutated_field"] = f"authority_context.{field}"
        case["authority_context"][field] = value
        mutations.append(case)
    return mutations


def claim_mutations(seed: dict[str, Any]) -> list[dict[str, Any]]:
    mutations: list[dict[str, Any]] = []
    changes = (
        ("evidence_present", False),
        ("evidence_fresh", False),
        ("verification_class", "SAME_SYSTEM_NONINDEPENDENT"),
    )
    for field, value in changes:
        case = copy.deepcopy(seed)
        case["mutation_id"] = f"M-CLAIM-{field}"
        case["mutated_field"] = f"claim.{field}"
        case["claim"][field] = value
        mutations.append(case)
    return mutations


def flow_mutations(seed: dict[str, Any]) -> list[dict[str, Any]]:
    mutations: list[dict[str, Any]] = []
    changes = (
        ("provenance_known", False),
        ("composition_authorized", False),
    )
    for field, value in changes:
        case = copy.deepcopy(seed)
        case["mutation_id"] = f"M-FLOW-{field}"
        case["mutated_field"] = f"flow.{field}"
        case["flow"][field] = value
        mutations.append(case)
    return mutations


def generate_mutations() -> list[dict[str, Any]]:
    cases = load_cases()
    mutations: list[dict[str, Any]] = []
    mutations.extend(authority_mutations(cases["GB-011"]))
    mutations.extend(claim_mutations(cases["GB-009"]))
    mutations.extend(flow_mutations(cases["GB-010"]))
    return mutations


def expected_decision(mutation: dict[str, Any], baseline: str) -> str:
    field = mutation["mutated_field"]
    if field.startswith("authority_context."):
        if baseline == "C1_MINIMAL_POLICY_AS_CODE":
            return "ALLOW"
        return "DENY"

    if field.startswith("claim.") or field.startswith("flow."):
        if baseline == "D_DGAF":
            return "DENY"
        return "ALLOW"

    raise ValueError(f"unclassified mutation field: {field}")


def run_mutations() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for mutation in generate_mutations():
        for baseline, decision_fn in BASELINES.items():
            decision, steps = decision_fn(mutation)
            expected = expected_decision(mutation, baseline)
            rows.append(
                {
                    "mutation_id": mutation["mutation_id"],
                    "seed_case_id": mutation["id"],
                    "mutated_field": mutation["mutated_field"],
                    "baseline": baseline,
                    "decision": decision,
                    "expected_decision": expected,
                    "pass": decision == expected,
                    "decision_steps": steps,
                }
            )

    return {
        "version": "DGAF_GOVERNANCE_MUTATION_SUITE_V1",
        "evidence_class": "SYNTHETIC_METAMORPHIC_ENGINEERING_EVIDENCE",
        "claim_ceiling": [
            "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED",
            "INDEPENDENT_VALIDATION_NOT_ESTABLISHED",
            "STATE_OF_THE_ART_NOT_ESTABLISHED",
        ],
        "mutation_count": len(generate_mutations()),
        "rows": rows,
        "all_pass": all(row["pass"] for row in rows),
    }


def main() -> int:
    print(json.dumps(run_mutations(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
