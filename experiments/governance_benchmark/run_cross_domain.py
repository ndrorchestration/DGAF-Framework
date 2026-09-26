"""Deterministic cross-domain governance interaction tests.

These cases combine degradations across distinct governance domains. They test
compositional stability within the bounded synthetic model only.
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


def compose(seed: dict[str, Any], interaction_id: str, changes: tuple[tuple[str, str, Any], ...]) -> dict[str, Any]:
    case = copy.deepcopy(seed)
    fields: list[str] = []
    for section, field, value in changes:
        if case.get(section) is None:
            if section == "authority_context":
                case[section] = {
                    "delegated_requester_authorized": True,
                    "token_replay_detected": False,
                    "request_bound_to_authorized_intent": True,
                    "workload_attested": True,
                    "child_scope_subset": True,
                }
            elif section == "claim":
                case[section] = {
                    "requested_status": "INDEPENDENT_VALIDATION_ESTABLISHED",
                    "evidence_present": True,
                    "verification_class": "INDEPENDENT",
                    "evidence_fresh": True,
                }
            elif section == "flow":
                case[section] = {
                    "source_classification": "CONFIDENTIAL",
                    "provenance_known": True,
                    "destination_class": "EXTERNAL",
                    "composition_authorized": True,
                }
        case[section][field] = value
        fields.append(f"{section}.{field}")
    case["cross_interaction_id"] = interaction_id
    case["mutated_fields"] = fields
    return case


def generate_cross_domain_interactions() -> list[dict[str, Any]]:
    cases = load_cases()
    return [
        compose(
            cases["GB-011"],
            "X-AUTH-CLAIM-INTENT-STALE",
            (
                ("authority_context", "request_bound_to_authorized_intent", False),
                ("claim", "evidence_fresh", False),
            ),
        ),
        compose(
            cases["GB-011"],
            "X-AUTH-CLAIM-REPLAY-NONINDEPENDENT",
            (
                ("authority_context", "token_replay_detected", True),
                ("claim", "verification_class", "SAME_SYSTEM_NONINDEPENDENT"),
            ),
        ),
        compose(
            cases["GB-011"],
            "X-AUTH-FLOW-WORKLOAD-PROVENANCE",
            (
                ("authority_context", "workload_attested", False),
                ("flow", "provenance_known", False),
            ),
        ),
        compose(
            cases["GB-011"],
            "X-AUTH-FLOW-SCOPE-COMPOSITION",
            (
                ("authority_context", "child_scope_subset", False),
                ("flow", "composition_authorized", False),
            ),
        ),
        compose(
            cases["GB-009"],
            "X-CLAIM-FLOW-STALE-PROVENANCE",
            (
                ("claim", "evidence_fresh", False),
                ("flow", "provenance_known", False),
            ),
        ),
        compose(
            cases["GB-009"],
            "X-CLAIM-FLOW-NONINDEPENDENT-COMPOSITION",
            (
                ("claim", "verification_class", "SAME_SYSTEM_NONINDEPENDENT"),
                ("flow", "composition_authorized", False),
            ),
        ),
    ]


def expected_decision(interaction: dict[str, Any], baseline: str) -> str:
    fields = interaction["mutated_fields"]
    has_authority_failure = any(field.startswith("authority_context.") for field in fields)
    has_dgaf_only_failure = any(field.startswith(("claim.", "flow.")) for field in fields)

    if baseline == "C1_MINIMAL_POLICY_AS_CODE":
        return "ALLOW"
    if baseline == "C2_HARDENED_POLICY_AS_CODE":
        return "DENY" if has_authority_failure else "ALLOW"
    if baseline == "D_DGAF":
        return "DENY" if has_authority_failure or has_dgaf_only_failure else "ALLOW"
    raise ValueError(f"unknown baseline: {baseline}")


def run_cross_domain_interactions() -> dict[str, Any]:
    interactions = generate_cross_domain_interactions()
    rows: list[dict[str, Any]] = []
    for interaction in interactions:
        for baseline, decision_fn in BASELINES.items():
            decision, steps = decision_fn(interaction)
            expected = expected_decision(interaction, baseline)
            rows.append(
                {
                    "cross_interaction_id": interaction["cross_interaction_id"],
                    "seed_case_id": interaction["id"],
                    "mutated_fields": interaction["mutated_fields"],
                    "baseline": baseline,
                    "decision": decision,
                    "expected_decision": expected,
                    "pass": decision == expected,
                    "decision_steps": steps,
                }
            )

    return {
        "version": "DGAF_GOVERNANCE_CROSS_DOMAIN_SUITE_V1",
        "evidence_class": "SYNTHETIC_CROSS_DOMAIN_ENGINEERING_EVIDENCE",
        "claim_ceiling": [
            "NO_GENERAL_COMPOSITIONAL_ROBUSTNESS_CLAIM",
            "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED",
            "INDEPENDENT_VALIDATION_NOT_ESTABLISHED",
            "STATE_OF_THE_ART_NOT_ESTABLISHED",
        ],
        "interaction_count": len(interactions),
        "rows": rows,
        "all_pass": all(row["pass"] for row in rows),
    }


def main() -> int:
    print(json.dumps(run_cross_domain_interactions(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
