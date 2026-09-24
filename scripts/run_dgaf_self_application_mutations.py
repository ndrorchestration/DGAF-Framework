#!/usr/bin/env python3
"""Run bounded DGAF-on-DGAF mutation tests against real repository validators."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "registry" / "dgaf_self_application_mutations_v1.json"

EVIDENCE_CLASS = "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION"
CLAIM_CEILING = {
    "scientific_n_increment": 0,
    "independent_validation": "NOT_ESTABLISHED",
    "external_validation": "NOT_ESTABLISHED",
    "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    "high_assurance": "NOT_AUTHORIZED",
}

VALIDATORS = {
    "claim_hygiene": [sys.executable, "scripts/claim_hygiene_check.py"],
    "control_state": [sys.executable, "scripts/validate_control_state.py"],
    "truth_layer": [
        sys.executable,
        "tools/validate_evidence_truth_layer.py",
        "--claim-surfaces-only",
    ],
    "registry_consistency": [sys.executable, "scripts/registry_consistency_check.py"],
}


def _run(
    command: list[str], cwd: Path, *, check: bool = False
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _replace_once(path: Path, pattern: str, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"mutation target not uniquely resolved: {path} / {pattern}")
    path.write_text(updated, encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def mutate_active_claim_overstatement(root: Path) -> None:
    (root / "SELF_APPLICATION_MUTATION.md").write_text(
        "# Temporary mutation\n\nDGAF is empirically superior.\n",
        encoding="utf-8",
    )


def mutate_apparatus_source_mismatch(root: Path) -> None:
    path = root / "docs" / "CURRENT_STATE.md"
    _replace_once(
        path,
        r"^(\s*-\s+apparatus source:\s*`)[0-9a-f]{40}(`\s*)$",
        r"\g<1>0000000000000000000000000000000000000000\g<2>",
    )


def mutate_authorization_with_n0(root: Path) -> None:
    path = root / "docs" / "governance" / "CONTROL_STATE_2026-08-31.yaml"
    _replace_once(
        path,
        r"^(\s*authorization:\s*)NOT_GRANTED\s*$",
        r"\g<1>GRANTED",
    )


def mutate_registry_representation_drift(root: Path) -> None:
    path = root / "docs" / "ndr_patterns_unified.json"
    path.write_bytes(path.read_bytes() + b"\n")


def mutate_truth_layer_synthetic_promotion(root: Path) -> None:
    path = root / "evidence" / "claims.json"
    data = _load_json(path)
    claims = data.get("claims")
    if not isinstance(claims, list):
        raise RuntimeError("claims registry is missing claims list")
    for claim in claims:
        if isinstance(claim, dict) and claim.get("evidence_mode") == "synthetic":
            claim["status"] = "VERIFIED"
            claim.pop("run_id", None)
            claim.pop("dataset", None)
            _write_json(path, data)
            return
    raise RuntimeError("no synthetic claim available for mutation")


def mutate_truth_layer_duplicate_claim(root: Path) -> None:
    path = root / "evidence" / "claims.json"
    data = _load_json(path)
    claims = data.get("claims")
    if not isinstance(claims, list) or not claims or not isinstance(claims[0], dict):
        raise RuntimeError("claims registry has no duplicable claim")
    claims.append(dict(claims[0]))
    _write_json(path, data)


def mutate_truth_layer_empirical_without_receipts(root: Path) -> None:
    path = root / "evidence" / "claims.json"
    data = _load_json(path)
    claims = data.get("claims")
    if not isinstance(claims, list):
        raise RuntimeError("claims registry is missing claims list")
    claims.append(
        {
            "claim_id": "SELF_APPLICATION_MUTATION_EMPIRICAL_NO_RECEIPTS",
            "statement": "Temporary self-application mutation.",
            "scope": "isolated mutation worktree only",
            "evidence_mode": "empirical",
            "status": "VERIFIED",
            "provenance": {"source": "self-application mutation harness"},
        }
    )
    _write_json(path, data)


def mutate_registry_release_identity_drift(root: Path) -> None:
    path = root / "docs" / "NDR_REGISTRY_RELEASE_MANIFEST.json"
    data = _load_json(path)
    data["registry_release_identity"] = "NDR-REGISTRY-SELF-APPLICATION-MUTATION"
    _write_json(path, data)


MUTATIONS: dict[str, Callable[[Path], None]] = {
    "active_claim_overstatement": mutate_active_claim_overstatement,
    "apparatus_source_mismatch": mutate_apparatus_source_mismatch,
    "authorization_with_n0": mutate_authorization_with_n0,
    "registry_representation_drift": mutate_registry_representation_drift,
    "truth_layer_synthetic_promotion": mutate_truth_layer_synthetic_promotion,
    "truth_layer_duplicate_claim": mutate_truth_layer_duplicate_claim,
    "truth_layer_empirical_without_receipts": mutate_truth_layer_empirical_without_receipts,
    "registry_release_identity_drift": mutate_registry_release_identity_drift,
}


def validate_registry(data: dict[str, Any]) -> list[dict[str, str]]:
    if data.get("version") != 1:
        raise ValueError("mutation registry version must be 1")
    if data.get("evidence_class") != EVIDENCE_CLASS:
        raise ValueError("mutation registry evidence_class mismatch")
    if data.get("claim_ceiling") != CLAIM_CEILING:
        raise ValueError("mutation registry claim ceiling mismatch")

    raw_cases = data.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise ValueError("mutation registry must contain cases")

    cases: list[dict[str, str]] = []
    seen: set[str] = set()
    for raw in raw_cases:
        if not isinstance(raw, dict):
            raise ValueError("mutation case must be an object")
        required = {
            "id",
            "mutation",
            "validator",
            "expected_marker",
            "expected_disposition",
        }
        if set(raw) != required:
            raise ValueError(f"mutation case fields must be exactly {sorted(required)}")
        case = {key: str(raw[key]) for key in required}
        if case["id"] in seen:
            raise ValueError(f"duplicate mutation case id: {case['id']}")
        seen.add(case["id"])
        if case["mutation"] not in MUTATIONS:
            raise ValueError(f"unknown mutation: {case['mutation']}")
        if case["validator"] not in VALIDATORS:
            raise ValueError(f"unknown validator: {case['validator']}")
        if case["expected_disposition"] != "BLOCKED":
            raise ValueError("v1 mutation cases must expect BLOCKED")
        if not case["expected_marker"]:
            raise ValueError("expected_marker must be non-empty")
        cases.append(case)
    return cases


def _source_commit() -> str:
    result = _run(["git", "rev-parse", "HEAD"], ROOT, check=True)
    return result.stdout.strip()


def _output_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run_case(case: dict[str, str], source_commit: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix=f"dgaf-self-{case['id']}-") as tmp:
        worktree = Path(tmp) / "repo"
        add = _run(
            ["git", "worktree", "add", "--detach", str(worktree), source_commit],
            ROOT,
        )
        if add.returncode != 0:
            raise RuntimeError(
                f"could not create isolated worktree for {case['id']}: "
                f"{add.stdout}\n{add.stderr}"
            )
        try:
            MUTATIONS[case["mutation"]](worktree)
            result = _run(VALIDATORS[case["validator"]], worktree)
            combined = result.stdout + result.stderr
            detected = result.returncode != 0 and case["expected_marker"] in combined
            return {
                "case_id": case["id"],
                "mutation": case["mutation"],
                "validator": case["validator"],
                "expected_disposition": case["expected_disposition"],
                "returncode": result.returncode,
                "expected_marker_found": case["expected_marker"] in combined,
                "detected": detected,
                "fail_closed": detected,
                "validator_output_sha256": _output_digest(combined),
                "validator_output": combined,
            }
        finally:
            _run(["git", "worktree", "remove", "--force", str(worktree)], ROOT)
            _run(["git", "worktree", "prune"], ROOT)


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    detected = sum(bool(item["detected"]) for item in results)
    fail_closed = sum(bool(item["fail_closed"]) for item in results)
    return {
        "total_mutations": total,
        "detected_mutations": detected,
        "fail_closed_mutations": fail_closed,
        "mutation_detection_rate": detected / total if total else 0.0,
        "fail_closed_rate": fail_closed / total if total else 0.0,
        "all_expected_mutations_detected": detected == total,
        "all_expected_mutations_fail_closed": fail_closed == total,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "ci-artifacts" / "dgaf-self-application-mutation-results.json",
    )
    args = parser.parse_args()

    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    if not isinstance(registry, dict):
        raise SystemExit("mutation registry must be a JSON object")
    cases = validate_registry(registry)
    source_commit = _source_commit()

    dirty_before = _run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        ROOT,
        check=True,
    ).stdout
    if dirty_before:
        raise SystemExit("source worktree must be clean before self-application mutation testing")

    results = [run_case(case, source_commit) for case in cases]
    dirty_after = _run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        ROOT,
        check=True,
    ).stdout
    if dirty_after:
        raise SystemExit("self-application mutation testing dirtied the source worktree")

    summary = summarize(results)
    evidence = {
        "evidence_class": EVIDENCE_CLASS,
        "source_commit": source_commit,
        "controller_issue": 1022,
        "program_lane": "MUTATION_TESTING_V1",
        "result": (
            "PASS_ALL_PREDECLARED_MUTATIONS_DETECTED"
            if summary["all_expected_mutations_detected"]
            else "FAIL_MUTATION_ESCAPE"
        ),
        "summary": summary,
        "claim_ceiling": CLAIM_CEILING,
        "independent_review_effect": "NONE",
        "scientific_state_effect": "NONE",
        "cases": results,
    }

    output = args.output
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(
        f"{digest}  {output.name}\n",
        encoding="utf-8",
    )

    print(json.dumps({"source_commit": source_commit, **summary}, indent=2))
    print(f"EVIDENCE_CLASS={EVIDENCE_CLASS}")
    print("SCIENTIFIC_N_INCREMENT=0")
    print("INDEPENDENT_VALIDATION=NOT_ESTABLISHED")
    print("EXTERNAL_VALIDATION=NOT_ESTABLISHED")
    print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")
    print("HIGH_ASSURANCE=NOT_AUTHORIZED")

    return 0 if summary["all_expected_mutations_detected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
