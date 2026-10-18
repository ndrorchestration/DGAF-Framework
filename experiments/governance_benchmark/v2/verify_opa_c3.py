"""Fail-closed OPA/C3/DGAF fixed-fixture calibration, NOT operational research."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
V2 = Path(__file__).resolve().parent
POLICY = V2 / "opa_c3_v1.rego"
FIXTURES = ROOT / "experiments/governance_benchmark/fixtures_v1.json"
C3_PATH = ROOT / "experiments/governance_benchmark/run_strong_policy_comparator.py"
OPA_VERSION = "1.21.2"
OPA_LINUX_AMD64_STATIC_SHA256 = "830ab11f61ffec760b5e19db0d7ad02bf037e13f5ef4d665faeaf17632177527"
CEILINGS = (
    "SCIENTIFIC_N_INCREMENT=0",
    "INDEPENDENT_VALIDATION=NOT_ESTABLISHED",
    "CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED",
    "HIGH_ASSURANCE=NOT_AUTHORIZED",
    "STATE_OF_THE_ART=NOT_ESTABLISHED",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def c3_module():
    spec = importlib.util.spec_from_file_location("v2_c3_reference", C3_PATH)
    if not spec or not spec.loader:
        raise RuntimeError("C3_SOURCE_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_binary(opa: Path) -> dict[str, str]:
    if not opa.is_file():
        raise RuntimeError("BLOCKED_OPA_BINARY_MISSING")
    result = subprocess.run([str(opa), "version"], capture_output=True, text=True, timeout=20, check=True)
    first = result.stdout.splitlines()[0] if result.stdout else ""
    if first != f"Version: {OPA_VERSION}":
        raise RuntimeError(f"BLOCKED_OPA_VERSION_MISMATCH: {first!r}")
    digest = sha256(opa)
    if digest != OPA_LINUX_AMD64_STATIC_SHA256:
        raise RuntimeError("BLOCKED_OPA_BINARY_SHA256_MISMATCH")
    return {"opa_version": OPA_VERSION, "opa_binary_sha256": digest}


def opa_allow(opa: Path, case: dict[str, Any]) -> bool:
    cmd = [
        str(opa),
        "eval",
        "--strict",
        "--format=json",
        "--data",
        str(POLICY),
        "--stdin-input",
        "data.dgaf.comparator_v2.allow",
    ]
    result = subprocess.run(cmd, input=json.dumps(case), capture_output=True, text=True, timeout=20)
    if result.returncode != 0:
        raise RuntimeError(f"BLOCKED_OPA_EVAL_ERROR: {result.stderr.strip()[:400]}")
    try:
        entries = json.loads(result.stdout)["result"]
        if len(entries) != 1 or len(entries[0]["expressions"]) != 1:
            raise ValueError("non-singular OPA response")
        value = entries[0]["expressions"][0]["value"]
        if type(value) is not bool:
            raise ValueError("non-boolean OPA result")
        return value
    except (ValueError, TypeError, KeyError, IndexError) as exc:
        raise RuntimeError("BLOCKED_OPA_RESULT_UNDETERMINED") from exc


def run(opa: Path) -> dict[str, Any]:
    identity = verify_binary(opa)
    c3 = c3_module()
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    rows = []
    for case in fixtures["cases"]:
        decision = "ALLOW" if opa_allow(opa, case) else "DENY"
        c3_decision, _ = c3.strong_policy_as_code(case)
        dgaf_decision, _ = c3.benchmark.dgaf(case)
        rows.append(
            {
                "case_id": case["id"],
                "expected_safe_outcome": case["expected_safe_outcome"],
                "opa_decision": decision,
                "c3_decision": c3_decision,
                "dgaf_decision": dgaf_decision,
                "three_way_parity": len({decision, c3_decision, dgaf_decision}) == 1,
            }
        )
    clean = not bool(
        subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    )
    return {
        "version": "DGAF_OPA_C3_FIXED_FIXTURE_EQUIVALENCE_V2_CANDIDATE",
        "evidence_class": "SAME_SYSTEM_SANDBOX_ENGINEERING_CHARACTERIZATION_ONLY",
        "candidate_state": "UNCOMMITTED_NOT_ADMITTED",
        "source_baseline": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip(),
        "working_tree_clean": clean,
        "fixture_sha256": sha256(FIXTURES),
        "rego_policy_sha256": sha256(POLICY),
        "c3_rules_sha256": c3.rules_sha256(),
        **identity,
        "results": rows,
        "summary": {
            "cases": len(rows),
            "three_way_parity": sum(row["three_way_parity"] for row in rows),
            "non_parity": sum(not row["three_way_parity"] for row in rows),
            "opa_false_blocks": sum(
                r["expected_safe_outcome"] == "ALLOW" and r["opa_decision"] == "DENY" for r in rows
            ),
            "dgaf_false_blocks": sum(
                r["expected_safe_outcome"] == "ALLOW" and r["dgaf_decision"] == "DENY" for r in rows
            ),
        },
        "claim_ceiling": list(CEILINGS),
        "interpretation": (
            "Fixed synthetic decisions only; no operational value, independent validation, "
            "safety superiority, or collection authority."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--opa", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        out = run(args.opa)
    except (RuntimeError, subprocess.SubprocessError, OSError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc), "claim_ceiling": list(CEILINGS)}))
        return 2
    encoded = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0 if out["summary"]["non_parity"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
