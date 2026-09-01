#!/usr/bin/env python3
"""Deterministic completion-state controller for DGAF/PDMAL.

The controller is an evidence evaluator, not an authorization mechanism. It
consumes an observed workflow/artifact evidence registry and requires verified
predicates to carry exact candidate/run/artifact identity.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import argparse
import json
from pathlib import Path
from typing import Iterable

VERIFIED = "VERIFIED"
EXPECTED_PREDICATES = ("P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9")


@dataclass(frozen=True)
class Predicate:
    id: str
    name: str
    required: bool
    status: str
    candidate_sha: str | None = None
    run_id: str | None = None
    artifact_id: str | None = None
    artifact_sha256: str | None = None
    deployment: str | None = None
    notes: str = ""
    custody_verified: bool = False
    source_workflow: str | None = None
    evidence: dict | None = None

    def exact_identity_complete(self, candidate_sha: str) -> bool:
        if self.status != VERIFIED:
            return False
        if self.candidate_sha != candidate_sha:
            return False
        if not self.run_id:
            return False
        if self.artifact_id and not self.artifact_sha256:
            return False
        return True


@dataclass(frozen=True)
class Decision:
    predicate: str
    status: str
    promotable: bool
    reason: str


def evaluate(predicates: Iterable[Predicate], candidate_sha: str) -> tuple[list[Decision], bool]:
    decisions: list[Decision] = []
    required_ok = True
    by_id = {p.id: p for p in predicates}

    for predicate_id in EXPECTED_PREDICATES:
        p = by_id.get(predicate_id)
        if p is None:
            required_ok = False
            decisions.append(Decision(predicate_id, "OPEN", False, "no authoritative evidence record present"))
            continue

        if not p.required:
            decisions.append(Decision(p.id, p.status, False, "non-required predicate"))
            continue

        if p.status != VERIFIED:
            required_ok = False
            decisions.append(Decision(p.id, p.status, False, f"status is {p.status}; fresh evidence required"))
            continue

        if not p.exact_identity_complete(candidate_sha):
            required_ok = False
            decisions.append(
                Decision(
                    p.id,
                    p.status,
                    False,
                    "verified claim is not fully bound to the exact candidate/run/artifact identity",
                )
            )
            continue

        if p.id == "P6" and not p.custody_verified:
            required_ok = False
            decisions.append(Decision(p.id, p.status, False, "custody verification is not recorded"))
            continue

        decisions.append(Decision(p.id, p.status, True, "exact candidate evidence present"))

    return decisions, required_ok


def build_predicates(raw: list[dict]) -> list[Predicate]:
    return [Predicate(**item) for item in raw]


def load_registry(path: Path, actual_candidate_sha: str | None = None) -> tuple[str, list[Predicate], dict, dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    candidate_sha = payload["candidate_sha"]
    if actual_candidate_sha and candidate_sha != actual_candidate_sha:
        raise ValueError(
            f"registry candidate_sha {candidate_sha} does not match actual candidate {actual_candidate_sha}"
        )
    predicates = build_predicates(payload.get("predicates", []))
    controls = payload.get("controls", {})
    return candidate_sha, predicates, controls, payload


def render_report(candidate_sha: str, predicates: list[Predicate], controls: dict, registry: dict) -> dict:
    decisions, all_required_verified = evaluate(predicates, candidate_sha)
    freeze_allowed = all_required_verified and controls.get("freeze_authorized", False)
    pilot_allowed = freeze_allowed and controls.get("pilot_authorized", False)
    return {
        "candidate_sha": candidate_sha,
        "registry_schema_version": registry.get("schema_version"),
        "required_predicates_verified": all_required_verified,
        "freeze_allowed_by_controller": freeze_allowed,
        "pilot_allowed_by_controller": pilot_allowed,
        "authorization_is_external": True,
        "empirical_execution_requested": False,
        "decisions": [asdict(d) for d in decisions],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path, help="observed workflow/artifact evidence registry JSON")
    parser.add_argument("--actual-candidate-sha", help="checked-out commit SHA, normally GITHUB_SHA")
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    args = parser.parse_args()

    candidate_sha, predicates, controls, registry = load_registry(args.registry, args.actual_candidate_sha)
    report = render_report(candidate_sha, predicates, controls, registry)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"

    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    return 0 if report["required_predicates_verified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
