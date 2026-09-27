"""Exhaustive bounded semantic-equivalence falsification for C3 policy vs DGAF.

This enumerates the current declared Boolean/categorical input schema. It tests
decision equivalence only; it does not establish architectural equivalence,
production safety, efficacy, independence, or SOTA status.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parent
BENCHMARK_PATH = ROOT / "run_benchmark.py"
STRONG_PATH = ROOT / "run_strong_policy_comparator.py"

benchmark_spec = importlib.util.spec_from_file_location("governance_benchmark_runner", BENCHMARK_PATH)
assert benchmark_spec and benchmark_spec.loader
benchmark = importlib.util.module_from_spec(benchmark_spec)
benchmark_spec.loader.exec_module(benchmark)

strong_spec = importlib.util.spec_from_file_location("strong_policy_runner", STRONG_PATH)
assert strong_spec and strong_spec.loader
strong = importlib.util.module_from_spec(strong_spec)
strong_spec.loader.exec_module(strong)


def authority_states() -> list[dict[str, bool] | None]:
    keys = (
        "delegated_requester_authorized",
        "token_replay_detected",
        "request_bound_to_authorized_intent",
        "workload_attested",
        "child_scope_subset",
    )
    states: list[dict[str, bool] | None] = [None]
    for values in itertools.product((False, True), repeat=len(keys)):
        states.append(dict(zip(keys, values)))
    return states


def claim_states() -> list[dict[str, Any] | None]:
    states: list[dict[str, Any] | None] = [None]
    for requested_status, evidence_present, evidence_fresh, verification_class in itertools.product(
        ("INDEPENDENT_VALIDATION_ESTABLISHED", "ENGINEERING_PASS"),
        (False, True),
        (False, True),
        ("INDEPENDENT", "SAME_SYSTEM_NONINDEPENDENT"),
    ):
        states.append(
            {
                "requested_status": requested_status,
                "evidence_present": evidence_present,
                "evidence_fresh": evidence_fresh,
                "verification_class": verification_class,
            }
        )
    return states


def flow_states() -> list[dict[str, Any] | None]:
    states: list[dict[str, Any] | None] = [None]
    for source, provenance_known, destination, composition_authorized in itertools.product(
        ("PUBLIC", "CONFIDENTIAL", "RESTRICTED"),
        (False, True),
        ("INTERNAL", "EXTERNAL"),
        (False, True),
    ):
        states.append(
            {
                "source_classification": source,
                "provenance_known": provenance_known,
                "destination_class": destination,
                "composition_authorized": composition_authorized,
            }
        )
    return states


def generated_cases() -> Iterator[dict[str, Any]]:
    action_keys = ("authorized", "tool_allowed", "target_allowed")
    case_index = 0
    for action_values, authority, claim, flow in itertools.product(
        itertools.product((False, True), repeat=3),
        authority_states(),
        claim_states(),
        flow_states(),
    ):
        case_index += 1
        yield {
            "id": f"EQ-{case_index:06d}",
            "family": "semantic_equivalence_enumeration",
            "action": dict(zip(action_keys, action_values)),
            "authority_context": authority,
            "claim": claim,
            "flow": flow,
        }


def run() -> dict[str, Any]:
    total = 0
    differences: list[dict[str, Any]] = []
    strong_allow = 0
    dgaf_allow = 0

    for case in generated_cases():
        total += 1
        strong_decision, strong_steps = strong.strong_policy_as_code(case)
        dgaf_decision, dgaf_steps = benchmark.dgaf(case)
        strong_allow += int(strong_decision == "ALLOW")
        dgaf_allow += int(dgaf_decision == "ALLOW")
        if strong_decision != dgaf_decision:
            differences.append(
                {
                    "case_id": case["id"],
                    "case": case,
                    "strong_policy_decision": strong_decision,
                    "dgaf_decision": dgaf_decision,
                    "strong_policy_steps": strong_steps,
                    "dgaf_steps": dgaf_steps,
                }
            )

    return {
        "version": "DGAF_C3_SEMANTIC_EQUIVALENCE_ENUMERATION_V1",
        "evidence_class": "SYNTHETIC_EXHAUSTIVE_BOUNDED_FALSIFICATION_EVIDENCE",
        "enumeration_scope": {
            "action_states": 8,
            "authority_states": len(authority_states()),
            "claim_states": len(claim_states()),
            "flow_states": len(flow_states()),
            "total_cases": total,
        },
        "summary": {
            "difference_count": len(differences),
            "parity_count": total - len(differences),
            "strong_policy_allow_count": strong_allow,
            "dgaf_allow_count": dgaf_allow,
            "semantically_equivalent_on_enumerated_schema": not differences,
        },
        "differences": differences[:100],
        "difference_retention_note": "At most first 100 differences retained in report.",
        "interpretation_boundary": [
            "Zero differences would establish decision-function equivalence only over this enumerated bounded schema.",
            (
                "It would not establish architectural equivalence, equal provenance guarantees, "
                "equal recovery semantics, or equal operator burden."
            ),
            "The enumeration does not represent production distributions or scientific sampling.",
            "Any difference requires case-level analysis and is not automatically evidence of superiority.",
        ],
        "claim_ceiling": [
            "SCIENTIFIC_N_INCREMENT_0",
            "INDEPENDENT_VALIDATION_NOT_ESTABLISHED",
            "CANONICAL_DGAF_EFFICACY_NOT_ESTABLISHED",
            "STATE_OF_THE_ART_NOT_ESTABLISHED",
            "HIGH_ASSURANCE_NOT_AUTHORIZED",
        ],
    }


def main() -> int:
    print(json.dumps(run(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
