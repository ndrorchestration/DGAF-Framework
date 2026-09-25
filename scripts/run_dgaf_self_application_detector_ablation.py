#!/usr/bin/env python3
"""Dependency-aware detector ablation for the accepted DGAF mutation corpus.

Engineering diagnostic only. This harness never mutates protected main or accepted evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any

_MUTATION_SCRIPT = Path(__file__).resolve().parent / "run_dgaf_self_application_mutations.py"
_SPEC = importlib.util.spec_from_file_location("run_dgaf_self_application_mutations", _MUTATION_SCRIPT)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("could not load mutation runner")
mutation = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(mutation)

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_CLASS = mutation.EVIDENCE_CLASS
CLAIM_CEILING = mutation.CLAIM_CEILING


def _detected(result: Any) -> bool:
    return result.returncode != 0


def run_matrix(cases: list[dict[str, str]], source_commit: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for case in cases:
        with tempfile.TemporaryDirectory(prefix=f"dgaf-ablation-{case['id']}-") as tmp:
            worktree = Path(tmp) / "repo"
            add = mutation._run(["git", "worktree", "add", "--detach", str(worktree), source_commit], ROOT)
            if add.returncode != 0:
                raise RuntimeError(f"could not create isolated worktree for {case['id']}")
            try:
                mutation.MUTATIONS[case["mutation"]](worktree)
                detector_results: dict[str, dict[str, Any]] = {}
                for detector, command in mutation.VALIDATORS.items():
                    result = mutation._run(command, worktree)
                    combined = result.stdout + result.stderr
                    detector_results[detector] = {
                        "detected": _detected(result),
                        "returncode": result.returncode,
                        "output_sha256": hashlib.sha256(combined.encode("utf-8")).hexdigest(),
                    }
                baseline_detected = any(v["detected"] for v in detector_results.values())
                ablations = {}
                for ablated in mutation.VALIDATORS:
                    remaining = {k: v for k, v in detector_results.items() if k != ablated}
                    detected = any(v["detected"] for v in remaining.values())
                    ablations[ablated] = {
                        "detected": detected,
                        "escaped": baseline_detected and not detected,
                    }
                records.append({
                    "case_id": case["id"],
                    "mutation": case["mutation"],
                    "baseline_detected": baseline_detected,
                    "detectors": detector_results,
                    "ablations": ablations,
                })
            finally:
                mutation._run(["git", "worktree", "remove", "--force", str(worktree)], ROOT)
                mutation._run(["git", "worktree", "prune"], ROOT)
    return records


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    baseline = sum(bool(r["baseline_detected"]) for r in records)
    unique: dict[str, int] = {name: 0 for name in mutation.VALIDATORS}
    for record in records:
        for detector, result in record["ablations"].items():
            if result["escaped"]:
                unique[detector] += 1
    return {
        "total_mutations": len(records),
        "baseline_detected": baseline,
        "baseline_detection_rate": baseline / len(records) if records else 0.0,
        "unique_escape_count_by_ablated_detector": unique,
        "interpretation": "Zero unique escapes does not imply a detector is removable; overlap may be intentional.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "ci-artifacts" / "dgaf-self-application-detector-ablation.json")
    args = parser.parse_args()

    registry = json.loads(mutation.DEFAULT_REGISTRY.read_text(encoding="utf-8"))
    cases = mutation.validate_registry(registry)
    source_commit = mutation._source_commit()

    dirty_before = mutation._run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], ROOT, check=True
    ).stdout
    if dirty_before:
        raise SystemExit("source worktree must be clean before detector ablation")

    records = run_matrix(cases, source_commit)

    dirty_after = mutation._run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], ROOT, check=True
    ).stdout
    if dirty_after:
        raise SystemExit("detector ablation dirtied the source worktree")

    summary = summarize(records)
    evidence = {
        "evidence_class": EVIDENCE_CLASS,
        "source_commit": source_commit,
        "controller_issue": 1022,
        "program_lane": "DETECTOR_ABLATION_V1",
        "ablation_scope": "HARNESS_LEVEL_ONE_DETECTOR_AT_A_TIME",
        "summary": summary,
        "claim_ceiling": CLAIM_CEILING,
        "scientific_state_effect": "NONE",
        "independent_review_effect": "NONE",
        "records": records,
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    print(json.dumps({"source_commit": source_commit, "summary": summary}, sort_keys=True))
    return 0 if summary["baseline_detected"] == summary["total_mutations"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
