"""Characterize frozen C1/C2/D/C3 behind a shared candidate input envelope."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Callable

from experiments.governance_benchmark.run_benchmark import (
    dgaf,
    hardened_policy_as_code,
    minimal_policy_as_code,
)
from experiments.governance_benchmark.run_strong_policy_comparator import (
    strong_policy_as_code,
)
from experiments.governance_benchmark.v3.input_envelope import (
    contract_sha256,
    evaluate_all,
)

OPA_VERSION = "1.21.2"
OPA_SHA256 = "830ab11f61ffec760b5e19db0d7ad02bf037e13f5ef4d665faeaf17632177527"

ROOT = Path(__file__).resolve().parents[3]
FIXTURES = ROOT / "experiments/governance_benchmark/fixtures_v1.json"


def comparators():
    return {
        "C1_HISTORICAL": minimal_policy_as_code,
        "C2_HISTORICAL": hardened_policy_as_code,
        "D_SYNTHETIC_HISTORICAL": dgaf,
        "C3_HISTORICAL": strong_policy_as_code,
    }


def optional_real_opa(binary: Path, policy: Path) -> Callable[[dict[str, Any]], tuple[str, list[str]]]:
    if not binary.is_file() or not policy.is_file():
        raise ValueError("BLOCKED_REAL_OPA_OR_REGO_FILE_MISSING")
    if hashlib.sha256(binary.read_bytes()).hexdigest() != OPA_SHA256:
        raise ValueError("BLOCKED_REAL_OPA_SHA256_MISMATCH")
    version = subprocess.run([str(binary), "version"], check=True, capture_output=True, text=True, timeout=20).stdout
    if not version.startswith(f"Version: {OPA_VERSION}\n"):
        raise ValueError("BLOCKED_REAL_OPA_VERSION_MISMATCH")

    def run(case: dict[str, Any]) -> tuple[str, list[str]]:
        proc = subprocess.run(
            [
                str(binary),
                "eval",
                "--strict",
                "--format=json",
                "-I",
                "-d",
                str(policy),
                "data.dgaf.comparator_v2.allow",
            ],
            input=json.dumps(case, allow_nan=False),
            text=True,
            capture_output=True,
            check=True,
            timeout=20,
        )
        output = json.loads(proc.stdout)
        vals = output["result"][0]["expressions"]
        if len(vals) != 1 or type(vals[0]["value"]) is not bool:
            raise ValueError("BLOCKED_OPA_UNEXPECTED_RESULT_SHAPE")
        return ("ALLOW" if vals[0]["value"] else "DENY"), ["REAL_OPA_C3_ENGINE"]

    return run


def characterize(
    cases: list[Any], external_comparators: dict[str, Callable[[dict[str, Any]], tuple[str, list[str]]]] | None = None
) -> dict[str, Any]:
    comparisons = comparators()
    if external_comparators:
        if any(key in comparisons for key in external_comparators):
            raise ValueError("DUPLICATE_COMPARATOR_NAME")
        comparisons.update(external_comparators)
    entries = []
    for index, case in enumerate(cases):
        entry = evaluate_all(case, comparisons)
        entry["ordinal"] = index
        entry["case_id"] = case.get("id") if type(case) is dict and type(case.get("id")) is str else None
        entries.append(entry)
    statuses = [r["input_state"] for r in entries]
    admitted = [r for r in entries if r["input_state"] == "ADMITTED_FOR_COMPARISON"]
    return {
        "contract": "DGAF_GOVERNANCE_BENCHMARK_V3_INPUT_ENVELOPE_CANDIDATE_1",
        "state": "DESIGN_ONLY_NOT_ADMITTED",
        "source_head": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout.strip(),
        "contract_sha256": contract_sha256(),
        "cases_sha256": hashlib.sha256(json.dumps(cases, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "summary": {
            "cases": len(entries),
            "admitted": statuses.count("ADMITTED_FOR_COMPARISON"),
            "input_rejected": statuses.count("INPUT_REJECTED"),
            "four_way_parity_on_admitted": sum(len(set(r["policy_results"].values())) == 1 for r in admitted),
        },
        "results": entries,
        "comparison_names": list(comparisons),
        "real_opa_executed": "OPA_C3_PINNED" in comparisons,
        "evidence_class": "OPERATOR_LOCAL_SAME_SYSTEM_ENGINEERING_ONLY",
        "scientific_n_increment": 0,
        "independent_validation": "NOT_ESTABLISHED",
        "canonical_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=FIXTURES)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--opa-bin", type=Path)
    parser.add_argument("--opa-policy", type=Path)
    args = parser.parse_args()
    raw = json.loads(args.input.read_text(encoding="utf-8"))
    cases = raw["cases"] if type(raw) is dict and type(raw.get("cases")) is list else None
    if cases is None:
        raise SystemExit("BLOCKED_EXPECTED_CASES_ARRAY")
    if (args.opa_bin is None) != (args.opa_policy is None):
        raise SystemExit("BLOCKED_OPA_BINARY_AND_POLICY_MUST_BOTH_BE_SUPPLIED")
    extra = {}
    if args.opa_bin is not None and args.opa_policy is not None:
        extra["OPA_C3_PINNED"] = optional_real_opa(args.opa_bin, args.opa_policy)
    report = characterize(cases, extra)
    if args.opa_policy is not None:
        report["opa_policy_sha256"] = hashlib.sha256(args.opa_policy.read_bytes()).hexdigest()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
