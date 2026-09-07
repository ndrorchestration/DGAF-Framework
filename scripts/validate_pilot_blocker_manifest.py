#!/usr/bin/env python3
"""Validate the v0.7.6 pilot-blocker manifest without promoting external facts."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/GOVERNANCE/PILOT_BLOCKER_MANIFEST_V0.7.6.json"
EXPECTED_ISSUES = {277, 295, 309, 310, 316, 320}
EXPECTED_CHECKPOINT = "597c637787bea7f87a45b4c1057d9cb1dc9dae8b"


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate(data: dict[str, Any]) -> None:
    require(data.get("record_type") == "DGAF_PDMAL_V0_7_6_PILOT_BLOCKER_MANIFEST", "wrong record type")
    require(data.get("schema_version") == 1, "wrong schema version")
    checkpoint = data.get("checkpoint", {})
    require(checkpoint.get("repository") == "ndrorchestration/DGAF-Framework", "wrong repository")
    require(checkpoint.get("main_commit_sha") == EXPECTED_CHECKPOINT, "checkpoint SHA drift")

    state = data.get("controlling_state", {})
    require(state == {
        "candidate": "NOT_DESIGNATED",
        "freeze": "NOT_ESTABLISHED",
        "pilot_authorization": "NOT_GRANTED",
        "empirical_n": 0,
    }, "controlling state promoted or malformed")

    testability = data.get("testability", {})
    require(testability.get("v0_7_6_contract_rehearsal") == "AVAILABLE_NON_EMPIRICAL", "contract rehearsal status drift")
    require(testability.get("merged_main_live_regression") == "PASS_AT_CHECKPOINT", "runtime evidence status drift")
    require(testability.get("empirical_pilot_execution") == "PROHIBITED", "empirical pilot unexpectedly permitted")

    blockers = data.get("blockers")
    require(isinstance(blockers, list), "blockers must be a list")
    issues = {item.get("issue") for item in blockers if isinstance(item, dict)}
    require(issues == EXPECTED_ISSUES, "blocker issue set drift")
    require(len(blockers) == len(EXPECTED_ISSUES), "duplicate or missing blocker record")
    for item in blockers:
        require(isinstance(item, dict), "blocker must be an object")
        issue = item.get("issue")
        require(item.get("status") == "OPEN", f"#{issue} status promoted")
        require(item.get("satisfied") is False, f"#{issue} unexpectedly satisfied")
        require(bool(item.get("repo_preparation")), f"#{issue} missing repo preparation classification")
        require(bool(item.get("required_external_fact")), f"#{issue} missing required external fact")
        require(bool(item.get("closure_authority")), f"#{issue} missing closure authority")
        require(isinstance(item.get("blocks"), list) and item["blocks"], f"#{issue} missing downstream block list")

    sequence = data.get("required_sequence")
    require(isinstance(sequence, list) and len(sequence) >= 8, "required sequence incomplete")
    require(sequence[0] == "close_or_accept_applicable_external_and_admin_blockers", "sequence must begin with blockers")
    require("grant_separate_explicit_pilot_authorization" in sequence, "separate authorization step missing")
    require(sequence.index("grant_separate_explicit_pilot_authorization") < sequence.index("execute_blinded_pilot"), "pilot precedes authorization")

    effects = data.get("non_effects", {})
    require(effects == {
        "final_candidate_designated": False,
        "p4_closed": False,
        "freeze_established": False,
        "pilot_authorized": False,
        "empirical_execution_performed": False,
        "empirical_n": 0,
    }, "non-effects promoted or malformed")


def self_test(data: dict[str, Any]) -> None:
    cases: list[tuple[str, dict[str, Any]]] = []

    mutated = copy.deepcopy(data)
    mutated["blockers"][0]["satisfied"] = True
    cases.append(("external blocker promotion", mutated))

    mutated = copy.deepcopy(data)
    mutated["controlling_state"]["pilot_authorization"] = "GRANTED"
    cases.append(("authorization promotion", mutated))

    mutated = copy.deepcopy(data)
    mutated["testability"]["empirical_pilot_execution"] = "PERMITTED"
    cases.append(("empirical execution promotion", mutated))

    mutated = copy.deepcopy(data)
    mutated["required_sequence"].remove("grant_separate_explicit_pilot_authorization")
    cases.append(("authorization sequence removal", mutated))

    for label, case in cases:
        try:
            validate(case)
        except ValidationError:
            continue
        raise ValidationError(f"negative control did not fail closed: {label}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    validate(data)
    if args.self_test:
        self_test(data)
    print("pilot blocker manifest: PASS (open/fail-closed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
