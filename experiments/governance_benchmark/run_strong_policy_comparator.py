"""Strong policy-as-code falsification comparator for the DGAF synthetic benchmark.

This comparator is deliberately allowed the same declared fixture inputs used by
the bounded DGAF model wherever ordinary policy-as-code can reasonably express
the rule. Parity is a valid falsification outcome.
"""

from __future__ import annotations

import hashlib
import importlib.util
from functools import cache
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
RULES_PATH = ROOT / "strong_policy_rules_v1.json"
BENCHMARK_PATH = ROOT / "run_benchmark.py"

spec = importlib.util.spec_from_file_location("governance_benchmark_runner", BENCHMARK_PATH)
assert spec and spec.loader
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)


def _get(case: dict[str, Any], dotted: str) -> tuple[bool, Any]:
    current: Any = case
    for part in dotted.split("."):
        if current is None or not isinstance(current, dict) or part not in current:
            return False, None
        current = current[part]
    return True, current


@cache
def load_rules() -> dict[str, Any]:
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


def rules_sha256() -> str:
    canonical = json.dumps(load_rules(), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def strong_policy_as_code(case: dict[str, Any]) -> tuple[str, list[str]]:
    rules = load_rules()["rules"]
    steps: list[str] = []

    for rule in rules:
        rule_id = rule["id"]
        kind = rule["kind"]

        if kind == "require_true":
            present, value = _get(case, rule["field"])
            steps.append(rule_id)
            if not present or value is not True:
                return "DENY", steps

        elif kind == "require_true_if_present":
            present, value = _get(case, rule["field"])
            if not present:
                continue
            steps.append(rule_id)
            if value is not True:
                return "DENY", steps

        elif kind == "require_false_if_present":
            present, value = _get(case, rule["field"])
            if not present:
                continue
            steps.append(rule_id)
            if value is not False:
                return "DENY", steps

        elif kind == "require_all_true_if_present":
            values: list[bool] = []
            any_present = False
            for field in rule["fields"]:
                present, value = _get(case, field)
                any_present = any_present or present
                values.append(present and value is True)
            if not any_present:
                continue
            steps.append(rule_id)
            if not all(values):
                return "DENY", steps

        elif kind == "require_equal_if":
            condition_present, condition_value = _get(case, rule["if_field"])
            if not condition_present or condition_value != rule["if_value"]:
                continue
            steps.append(rule_id)
            present, value = _get(case, rule["field"])
            if not present or value != rule["value"]:
                return "DENY", steps

        elif kind == "require_true_if":
            condition_matches = True
            for field, accepted_values in rule["if_all"]:
                present, value = _get(case, field)
                if not present or value not in accepted_values:
                    condition_matches = False
                    break
            if not condition_matches:
                continue
            steps.append(rule_id)
            present, value = _get(case, rule["field"])
            if not present or value is not True:
                return "DENY", steps

        else:
            raise ValueError(f"unsupported policy rule kind: {kind}")

    return "ALLOW", steps


def run() -> dict[str, Any]:
    fixtures = json.loads(benchmark.DEFAULT_FIXTURES.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []

    for case in fixtures["cases"]:
        strong_decision, strong_steps = strong_policy_as_code(case)
        dgaf_decision, dgaf_steps = benchmark.dgaf(case)
        rows.append(
            {
                "case_id": case["id"],
                "family": case["family"],
                "expected_safe_outcome": case["expected_safe_outcome"],
                "strong_policy_decision": strong_decision,
                "dgaf_decision": dgaf_decision,
                "parity": strong_decision == dgaf_decision,
                "strong_policy_step_count": len(strong_steps),
                "dgaf_step_count": len(dgaf_steps),
                "strong_policy_steps": strong_steps,
                "dgaf_steps": dgaf_steps,
            }
        )

    policy = load_rules()
    parity_count = sum(int(row["parity"]) for row in rows)
    policy_bytes = len(json.dumps(policy, sort_keys=True, separators=(",", ":")).encode("utf-8"))

    return {
        "version": "DGAF_STRONG_POLICY_COMPARATOR_V1",
        "evidence_class": "SYNTHETIC_FALSIFICATION_ENGINEERING_EVIDENCE",
        "ruleset_version": policy["version"],
        "ruleset_sha256": rules_sha256(),
        "rules_frozen_before_result_inspection": policy["status"] == "FROZEN_BEFORE_RESULT_INSPECTION",
        "configuration_complexity": {
            "rule_count": len(policy["rules"]),
            "canonical_policy_bytes": policy_bytes,
        },
        "results": rows,
        "summary": {
            "cases": len(rows),
            "parity_count": parity_count,
            "difference_count": len(rows) - parity_count,
            "strong_policy_task_correct": sum(
                int(row["strong_policy_decision"] == row["expected_safe_outcome"]) for row in rows
            ),
            "dgaf_task_correct": sum(int(row["dgaf_decision"] == row["expected_safe_outcome"]) for row in rows),
            "strong_policy_false_blocks": sum(
                int(row["expected_safe_outcome"] == "ALLOW" and row["strong_policy_decision"] == "DENY") for row in rows
            ),
            "dgaf_false_blocks": sum(
                int(row["expected_safe_outcome"] == "ALLOW" and row["dgaf_decision"] == "DENY") for row in rows
            ),
        },
        "falsification_outcome": (
            "PARITY_ON_CURRENT_FIXED_FIXTURES" if parity_count == len(rows) else "NON_PARITY_ON_CURRENT_FIXED_FIXTURES"
        ),
        "interpretation_boundary": [
            "Parity weakens any claim that the current fixed fixtures demonstrate unique DGAF protection.",
            "Parity does not show architectural equivalence, equal operational burden, or equal production safety.",
            "Non-parity would require case-level analysis before any comparative inference.",
            (
                "This synthetic result does not establish efficacy, SOTA status, "
                "independent validation, compliance, or scientific evidence."
            ),
        ],
        "claim_ceiling": policy["claim_ceiling"],
    }


def main() -> int:
    print(json.dumps(run(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
