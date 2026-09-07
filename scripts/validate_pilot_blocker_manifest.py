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
EXPECTED_ISSUES = {277, 295, 309, 310, 316, 320, 369}
EXPECTED_CHECKPOINT = "d9919fce77588786f36ffa455baa4f2233fad9e7"


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate(data: dict[str, Any]) -> None:
    require(data.get("record_type") == "DGAF_PDMAL_V0_7_6_PILOT_BLOCKER_MANIFEST", "wrong record type")
    require(data.get("schema_version") == 3, "wrong schema version")
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
        "track": "EXPERIMENT_001_APPARATUS_FALSIFICATION_FUTURE_EPOCH_NOT_AUTHORIZED",
        "experiment_001_retained_observations": 9000,
        "experiment_001_efficacy_eligible": False,
        "scientific_n_for_efficacy": 0,
        "future_epoch_freeze": "NOT_ESTABLISHED",
        "future_epoch_authorization": "NOT_GRANTED",
        "authority_record": "docs/GOVERNANCE/SOLO_EPOCH_AUTHORITY_V1.json",
        "blocking_issue": 369,
    }, "solo state promoted or malformed")

    testability = data.get("testability", {})
    require(testability.get("v0_7_6_contract_rehearsal") == "AVAILABLE_NON_EMPIRICAL", "contract rehearsal status drift")
    require(testability.get("merged_main_live_regression") == "PASS_AT_CHECKPOINT", "runtime evidence status drift")
    require(testability.get("solo_successor_empirical_execution") == "PROHIBITED_PENDING_REPOSITORY_BOUND_EPOCH_AUTHORITY", "Solo successor execution unexpectedly permitted")
    require(testability.get("legacy_solo_environment_self_authorization") == "INSUFFICIENT", "legacy Solo environment variables unexpectedly authoritative")
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
        expected_solo_block = issue == 369
        require(item.get("blocks_solo_pilot") is expected_solo_block, f"#{issue} Solo-blocking classification drift")
        require(bool(item.get("repo_preparation")), f"#{issue} missing repo preparation classification")
        require(bool(item.get("required_external_fact")), f"#{issue} missing required external fact")
        require(bool(item.get("closure_authority")), f"#{issue} missing closure authority")
        require(isinstance(item.get("blocks"), list) and item["blocks"], f"#{issue} missing downstream block list")

    issue_369 = next(item for item in blockers if item.get("issue") == 369)
    require(issue_369.get("blocks") == ["solo_successor_epoch_authorization"], "#369 downstream block drift")

    high_sequence = data.get("high_assurance_required_sequence")
    require(isinstance(high_sequence, list) and len(high_sequence) >= 8, "high-assurance sequence incomplete")
    require(high_sequence[0] == "close_or_accept_applicable_external_and_admin_blockers", "high-assurance sequence must begin with blockers")
    require("grant_separate_explicit_high_assurance_pilot_authorization" in high_sequence, "high-assurance authorization missing")
    require(high_sequence.index("grant_separate_explicit_high_assurance_pilot_authorization") < high_sequence.index("execute_high_assurance_blinded_pilot"), "high-assurance pilot precedes authorization")

    solo_sequence = data.get("solo_required_sequence")
    require(isinstance(solo_sequence, list) and len(solo_sequence) >= 9, "solo sequence incomplete")
    require(solo_sequence[0] == "resolve_issue_369_empirical_p30_binding", "Solo successor sequence must begin with issue #369")
    require("pass_candidate_bound_n0_p30_validation" in solo_sequence, "Solo N=0 P-30 validation missing")
    require("bind_repository_epoch_authority_to_exact_commit_and_epoch_id" in solo_sequence, "repository-bound Solo authority missing")
    require("grant_repository_bound_epoch_authorization" in solo_sequence, "repository-bound Solo grant missing")
    require(solo_sequence.index("grant_repository_bound_epoch_authorization") < solo_sequence.index("execute_blinded_successor_solo_epoch"), "Solo execution precedes repository-bound authorization")

    effects = data.get("current_non_effects", {})
    require(effects == {
        "high_assurance_final_candidate_designated": False,
        "high_assurance_p4_closed": False,
        "high_assurance_freeze_established": False,
        "high_assurance_pilot_authorized": False,
        "high_assurance_empirical_execution_performed": False,
        "high_assurance_empirical_n": 0,
        "solo_experiment_001_executed": True,
        "solo_experiment_001_retained_observations": 9000,
        "solo_experiment_001_efficacy_eligible": False,
        "future_solo_epoch_authorized": False,
        "future_solo_epoch_scientific_n": 0,
    }, "current non-effects promoted or malformed")


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
    mutated["testability"]["legacy_solo_environment_self_authorization"] = "SUFFICIENT"
    cases.append(("legacy Solo environment authorization promotion", mutated))

    mutated = copy.deepcopy(data)
    mutated["solo_controlling_state"]["future_epoch_authorization"] = "GRANTED"
    cases.append(("future Solo epoch authorization promotion", mutated))

    mutated = copy.deepcopy(data)
    mutated["current_non_effects"]["solo_experiment_001_efficacy_eligible"] = True
    cases.append(("experiment-001 efficacy eligibility promotion", mutated))

    mutated = copy.deepcopy(data)
    issue_369 = next(item for item in mutated["blockers"] if item.get("issue") == 369)
    issue_369["blocks_solo_pilot"] = False
    cases.append(("issue #369 Solo blocker removal", mutated))

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
    print("pilot blocker manifest: PASS (Solo experiment 001 retained / successor epoch fail-closed / high-assurance fail-closed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
