"""BKRC-001 decision-only preflight; no execution or scientific authority."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from experiments.governance_benchmark.run_benchmark import dgaf
from experiments.governance_benchmark.run_strong_policy_comparator import (
    RULES_PATH,
    rules_sha256,
    strong_policy_as_code,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "experiments/governance_benchmark/fixtures_v1.json"
CASES = ("AUTH_ALLOW", "AUTH_DENY", "CLAIM_ALLOW", "CLAIM_DENY")
EXPECTED = ("ALLOW", "DENY", "ALLOW", "DENY")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def case_bytes(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def inputs() -> list[tuple[str, str, dict[str, Any]]]:
    raw = json.loads(FIXTURES.read_text(encoding="utf-8"))
    fixtures = {x["id"]: x for x in raw["cases"]}
    originals = [copy.deepcopy(fixtures[n]) for n in ("GB-001", "GB-002", "GB-003")]
    claim_positive = copy.deepcopy(originals[2])
    assert claim_positive["claim"]["requested_status"] == "INDEPENDENT_VALIDATION_ESTABLISHED"
    claim_positive["claim"]["requested_status"] = "SAME_SYSTEM_NONINDEPENDENT"
    return [
        ("AUTH_ALLOW", "GB-001", originals[0]),
        ("AUTH_DENY", "GB-002", originals[1]),
        ("CLAIM_ALLOW", "GB-003:ONE_FIELD_MUTATION", claim_positive),
        ("CLAIM_DENY", "GB-003", originals[2]),
    ]


def run() -> dict[str, Any]:
    records = []
    for (label, source, datum), expected in zip(inputs(), EXPECTED, strict=True):
        c3, c3_trace = strong_policy_as_code(copy.deepcopy(datum))
        synthetic, synthetic_trace = dgaf(copy.deepcopy(datum))
        records.append(
            {
                "id": label,
                "origin": source,
                "input_sha256": hashlib.sha256(case_bytes(datum)).hexdigest(),
                "operator_expected": expected,
                "c3": c3,
                "synthetic_d": synthetic,
                "c3_trace": c3_trace,
                "synthetic_d_trace": synthetic_trace,
                "matches_operator_expected": c3 == synthetic == expected,
                "decision_parity": c3 == synthetic,
                "dispatch_observed": "NOT_INSTRUMENTED",
                "effect_observed": "NOT_INSTRUMENTED",
                "enforcement_receipt": None,
                "non_dispatch_proven": False,
                "independent_oracle": "NOT_ESTABLISHED",
            }
        )
    return {
        "schema": "BKRC_001_DECISION_ONLY_FIRST_SLICE_V0_1",
        "status": "SAME_SYSTEM_ENGINEERING_ONLY_NOT_ADMITTED",
        "source_head": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout.strip(),
        "historical_fixture_sha256": digest(FIXTURES),
        "historical_c3_rule_file_sha256": digest(RULES_PATH),
        "historical_c3_canonical_sha256": rules_sha256(),
        "case_count": len(records),
        "c3_synthetic_d_parity": sum(r["decision_parity"] for r in records),
        "matches_operator_expectation": sum(r["matches_operator_expected"] for r in records),
        "observed_effect_count": "NOT_MEASURED",
        "independently_validated_cases": 0,
        "scientific_n_increment": 0,
        "independent_validation": "NOT_ESTABLISHED",
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
        "claim_exclusions": [
            "actual_side_effects",
            "trusted_policy_enforcement",
            "non_dispatch",
            "independent_truth_oracle",
            "incremental_DGAF_or_BKRC_advantage",
        ],
        "cases": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
