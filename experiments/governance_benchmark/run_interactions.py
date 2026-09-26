"""Deterministic two-factor interaction mutations for DGAF governance tests.

These cases combine two previously isolated governance degradations. They test
stability under interacting conditions, not emergent or general robustness.
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


def mutate_pair(
    seed: dict[str, Any],
    interaction_id: str,
    changes: tuple[tuple[str, str, Any], tuple[str, str, Any]],
) -> dict[str, Any]:
    case = copy.deepcopy(seed)
    fields: list[str] = []
    for section, field, value in changes:
        case[section][field] = value
        fields.append(f"{section}.{field}")
    case["interaction_id"] = interaction_id
    case["mutated_fields"] = fields
    return case


def generate_interactions() -> list[dict[str, Any]]:
    cases = load_cases()
    authority_seed = cases["GB-011"]
    claim_seed = cases["GB-009"]
    flow_seed = cases["GB-010"]

    return [
        mutate_pair(
            authority_seed,
            "I-AUTH-REQUESTER-REPLAY",
            (
                ("authority_context", "delegated_requester_authorized", False),
                ("authority_context", "token_replay_detected", True),
            ),
        ),
        mutate_pair(
            authority_seed,
            "I-AUTH-INTENT-WORKLOAD",
            (
                ("authority_context", "request_bound_to_authorized_intent", False),
                ("authority_context", "workload_attested", False),
            ),
        ),
        mutate_pair(
            authority_seed,
            "I-AUTH-REPLAY-SCOPE",
            (
                ("authority_context", "token_replay_detected", True),
                ("authority_context", "child_scope_subset", False),
            ),
        ),
        mutate_pair(
            claim_seed,
            "I-CLAIM-MISSING-STALE",
            (
                ("claim", "evidence_present", False),
                ("claim", "evidence_fresh", False),
            ),
        ),
        mutate_pair(
            claim_seed,
            "I-CLAIM-STALE-NONINDEPENDENT",
            (
                ("claim", "evidence_fresh", False),
                ("claim", "verification_class", "SAME_SYSTEM_NONINDEPENDENT"),
            ),
        ),
        mutate_pair(
            claim_seed,
            "I-CLAIM-MISSING-NONINDEPENDENT",
            (
                ("claim", "evidence_present", False),
                ("claim", "verification_class", "SAME_SYSTEM_NONINDEPENDENT"),
            ),
        ),
        mutate_pair(
            flow_seed,
            "I-FLOW-PROVENANCE-COMPOSITION",
            (
                ("flow", "provenance_known", False),
                ("flow", "composition_authorized", False),
            ),
        ),
    ]


def expected_decision(interaction: dict[str, Any], baseline: str) -> str:
    fields = interaction["mutated_fields"]
    authority_only = all(field.startswith("authority_context.") for field in fields)

    if authority_only:
        if baseline == "C1_MINIMAL_POLICY_AS_CODE":
            return "ALLOW"
        return "DENY"

    if baseline == "D_DGAF":
        return "DENY"
    return "ALLOW"


def run_interactions() -> dict[str, Any]:
    interactions = generate_interactions()
    rows: list[dict[str, Any]] = []

    for interaction in interactions:
        for baseline, decision_fn in BASELINES.items():
            decision, steps = decision_fn(interaction)
            expected = expected_decision(interaction, baseline)
            rows.append(
                {
                    "interaction_id": interaction["interaction_id"],
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
        "version": "DGAF_GOVERNANCE_INTERACTION_SUITE_V1",
        "evidence_class": "SYNTHETIC_TWO_FACTOR_ENGINEERING_EVIDENCE",
        "claim_ceiling": [
            "NO_EMERGENT_ROBUSTNESS_CLAIM",
            "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED",
            "INDEPENDENT_VALIDATION_NOT_ESTABLISHED",
            "STATE_OF_THE_ART_NOT_ESTABLISHED",
        ],
        "interaction_count": len(interactions),
        "rows": rows,
        "all_pass": all(row["pass"] for row in rows),
    }


def main() -> int:
    print(json.dumps(run_interactions(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
