#!/usr/bin/env python3
"""Validate the v0.7.6 split pilot-blocker manifest without promoting facts."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/GOVERNANCE/PILOT_BLOCKER_MANIFEST_V0.7.6.json"
EXPECTED_ISSUES = {277, 295, 309, 310, 316, 320}
EXPECTED_CHECKPOINT = "d9919fce77588786f36ffa455baa4f2233fad9e7"


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate(data: dict[str, Any]) -> None:
    require(data.get("record_type") == "DGAF_PDMAL_V0_7_6_PILOT_BLOCKER_MANIFEST", "wrong record type")
    require(data.get("schema_version") == 2, "wrong schema version")
    checkpoint = data.get("checkpoint", {})
    require(checkpoint.get("repository") == "ndrorchestration/DGAF-Framework", "wrong repository")
    require(checkpoint.get("high_assurance_checkpoint_main_sha") == EXPECTED_CHECKPOINT, "checkpoint SHA drift")

    high = data.get("high_assurance_controlling_state", {})
    require(high == {
        "candidate": "NOT_DESIGNATED",
        "freeze": "NOT_ESTABLISHED",
        "pilot_authorization": "NOT_GRANTED",
        "empirical_n": 0,
    }, "high-assurance state promoted or malformed")

    solo = data.get("solo_controlling_state", {})
    require(solo == {
        "track": "AVAILABLE_NOT_EXECUTED",
        "freeze": "NOT_ESTABLISHED",
        "self_authorization": "NOT_GRANTED",
        "limitations_acknowledged": False,
        "empirical_n": 0,
    }, "solo state promoted or malformed")

    testability = data.get("testability", {})
    require(testability.get("v0_7_6_contract_rehearsal") == "AVAILABLE_NON_EMPIRICAL", "contract rehearsal status drift")
    require(testability.get("merged_main_live_regression") == "PASS_AT_CHECKPOINT", "runtime evidence status drift")
    require(testability.get("solo_pilot_execution") == "SEPARATELY_GOVERNED_BY_SOLO_PILOT_TRACK", "solo track boundary drift")
    require(testability.get("high_assurance_empirical_pilot_execution") == "PROHIBITED", "high-assurance pilot unexpectedly permitted")

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
        require(item.get("blocks_solo_pilot") is False, f"#{issue} unexpectedly blocks Solo Pilot")
        require(bool(item.get("repo_preparation")), f"#{issue} missing repo preparation classification")
        require(bool(item.get("required_external_fact")), f"#{issue} missing required external fact")
        require(bool(item.get("closure_authority")), f"#{issue} missing closure authority")
        require(isinstance(item.get("blocks"), list) and item["blocks"], f"#{issue} missing downstream block list")

    high_sequence = data.get("high_assurance_required_sequence")
    require(isinstance(high_sequence, list) and len(high_sequence) >= 8, "high-assurance sequence incomplete")
    require(high_sequence[0] == "close_or_accept_applicable_external_and_admin_blockers", "high-assurance sequence must begin with blockers")
    require("grant_separate_explicit_high_assurance_pilot_authorization" in high_sequence, "high-assurance authorization missing")
    require(high_sequence.index("grant_separate_explicit_high_assurance_pilot_authorization") < high_sequence.index("execute_high_assurance_blinded_pilot"), "high-assurance pilot precedes authorization")

    solo_sequence = data.get("solo_required_sequence")
    require(isinstance(solo_sequence, list) and len(solo_sequence) >= 7, "solo sequence incomplete")
    require(solo_sequence[0] == "select_exact_clean_commit", "solo sequence must begin with exact commit selection")
    require("acknowledge_solo_limitations" in solo_sequence, "solo limitations acknowledgement missing")
    require("grant_explicit_solo_self_authorization" in solo_sequence, "solo self-authorization missing")
    require(solo_sequence.index("grant_explicit_solo_self_authorization") < solo_sequence.index("execute_blinded_solo_pilot"), "solo pilot precedes self-authorization")

    effects = data.get("non_effects_at_definition", {})
    require(effects == {
        "high_assurance_final_candidate_designated": False,
        "high_assurance_p4_closed": False,
        "high_assurance_freeze_established": False,
        "high_assurance_pilot_authorized": False,
        "high_assurance_empirical_execution_performed": False,
        "high_assurance_empirical_n": 0,
        "solo_empirical_execution_performed": False,
        "solo_empirical_n": 0,
    }, "definition non-effects promoted or malformed")


def self_test(data: dict[str, Any]) -> None:
    cases: list[tuple[str, dict[str, Any]]] = []

    mutated = copy.deepcopy(data)
    mutated["blockers"][0]["satisfied"] = True
    cases.append(("external blocker promotion", mutated))

    mutated = copy.deepcopy(data)
    mutated["high_assurance_controlling_state"]["pilot_authorization"] = "GRANTED"
    cases.append(("high-assurance authorization promotion", mutated))

    mutated = copy.deepcopy(data)
    mutated["testability"]["high_assurance_empirical_pilot_execution"] = "PERMITTED"
    cases.append(("high-assurance empirical execution promotion", mutated))

    mutated = copy.deepcopy(data)
    mutated["blockers"][0]["blocks_solo_pilot"] = True
    cases.append(("external blocker incorrectly blocks solo", mutated))

    mutated = copy.deepcopy(data)
    mutated["solo_required_sequence"].remove("acknowledge_solo_limitations")
    cases.append(("solo limitations acknowledgement removal", mutated))

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
    print("pilot blocker manifest: PASS (solo split / high-assurance fail-closed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
