#!/usr/bin/env python3
"""Fail-closed validation for inert external-acceptance readiness templates."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]

STAGE_A_INPUT = ROOT / "docs/GOVERNANCE/stage_a/EXECUTION_INPUT_TEMPLATE.json"
STAGE_A_EVIDENCE = ROOT / "docs/GOVERNANCE/stage_a/EVIDENCE_MANIFEST_TEMPLATE.json"
PROD_AUTHORITY = ROOT / "docs/GOVERNANCE/production_authority/ACCEPTANCE_TEMPLATE.json"
CONTINUITY = ROOT / "docs/GOVERNANCE/continuity/P4_B_FINAL_ACCEPTANCE_TEMPLATE.json"
CANDIDATE = ROOT / "docs/experiment/FINAL_CANDIDATE_DESIGNATION_TEMPLATE_V0.7.6.json"
AUTHORIZATION = ROOT / "docs/experiment/PILOT_AUTHORIZATION_TEMPLATE_V0.7.6.json"
STAGE_A_PROCEDURE = ROOT / "docs/GOVERNANCE/STAGE_A_CONFIDENTIAL_SPACE_QUALIFICATION_PREPARATION_2026-09-07.md"
REVIEW_MANIFEST = ROOT / "docs/GOVERNANCE/review_packages/320_mode_t_oidc_security/SOURCE_IDENTITIES.json"

EXPECTED_STAGE_A_PROCEDURE_BLOB = "969ef63fb2bd4188f2f60eb7f94d11bf7125b2a1"
EXPECTED_REVIEW_MANIFEST_BLOB = "412b2050900defd81175b6f787bad430eb24eff1"


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
    ).strip()


def validate_stage_a_input(data: dict[str, Any]) -> None:
    require(data["record_type"] == "DGAF_STAGE_A_EXECUTION_INPUT_TEMPLATE", "wrong Stage-A input record type")
    require(data["status"] == "TEMPLATE_NOT_EXECUTED", "Stage-A input must remain inert")
    require(data["procedure"]["blob_sha"] == EXPECTED_STAGE_A_PROCEDURE_BLOB, "Stage-A procedure identity drift")
    state = data["controlling_state"]
    require(
        state
        == {
            "final_candidate": "NOT_DESIGNATED",
            "candidate_tracker": 309,
            "p4": "OPEN_FAIL_CLOSED",
            "freeze": "NOT_ESTABLISHED",
            "authorization": "NOT_GRANTED",
            "empirical_n": 0,
        },
        "Stage-A controlling state promoted",
    )
    require(data["gcp"]["project_id"] is None, "template must not contain a project id")
    require(data["gcp"]["workload_service_account"] is None, "template must not contain a service account")
    require(data["workload"]["container_digest_sha256"] is None, "template must not pretend a workload digest is frozen")
    require(data["authorization_binding"]["production_authority_accepted"] is False, "production authority must remain unaccepted")
    require(
        data["execution_permission"]
        == {
            "authenticated_gcp_session_available": False,
            "operator_approved_real_cloud_qualification": False,
            "empirical_execution_permitted": False,
        },
        "Stage-A execution permission promoted",
    )


def validate_stage_a_evidence(data: dict[str, Any]) -> None:
    require(data["record_type"] == "DGAF_STAGE_A_EVIDENCE_MANIFEST_TEMPLATE", "wrong Stage-A evidence record type")
    require(data["status"] == "TEMPLATE_NOT_EXECUTED", "Stage-A evidence must remain inert")
    require(data["pre_attestation"]["verified"] is False, "PRE cannot be pre-verified")
    require(data["post_attestation"]["verified"] is False, "POST cannot be pre-verified")
    require(data["two_phase_binding"]["verified"] is False, "two-phase binding cannot be pre-verified")
    action = data["synthetic_action"]
    require(action["executed"] is False, "Stage-A action cannot be pre-executed")
    require(action["empirical_observations_collected"] is False, "template cannot collect empirical observations")
    require(data["adjudication"]["stage_a_outcome"] == "NOT_EXECUTED", "Stage-A outcome must remain NOT_EXECUTED")
    require(data["adjudication"]["accepted_for_p4"] is False, "template cannot accept P4")
    require(data["adjudication"]["candidate_designation_authorized"] is False, "template cannot authorize candidate designation")
    require(data["controlling_state_after_record"]["empirical_n"] == 0, "template cannot increase empirical N")


def validate_production_authority(data: dict[str, Any]) -> None:
    require(data["record_type"] == "DGAF_MODE_T_PRODUCTION_AUTHORITY_ACCEPTANCE_TEMPLATE", "wrong production-authority record type")
    require(data["status"] == "TEMPLATE_NOT_EXECUTED", "production authority template must remain inert")
    require(data["authorization_chain"]["reservation_record_sha256"] is None, "production R must remain unset")
    require(data["authorization_chain"]["authorization_record_sha256"] is None, "production A must remain unset")
    require(data["authorization_chain"]["consumption_record_sha256"] is None, "production C must remain unset")
    require(data["admission_policy"]["canonical_policy_sha256"] is None, "production policy must not be preaccepted")
    require(data["signer_and_transparency"]["approved"] is False, "production signer must remain unapproved")
    require(data["trusted_root_and_tuf"]["approved"] is False, "TrustedRoot/TUF must remain unapproved")
    require(data["retention_and_reverification"]["fresh_cryptographic_verification"] is False, "external retention cannot be preverified")
    require(data["external_dependencies"]["issue_320_accepted"] is False, "#320 cannot be preaccepted")
    require(data["external_dependencies"]["issue_310_accepted"] is False, "#310 cannot be preaccepted")
    require(data["adjudication"]["classification"] == "NOT_EXECUTED", "production authority cannot be preadjudicated")
    require(data["adjudication"]["production_authority_established"] is False, "production authority cannot be preestablished")
    require(data["non_effects"]["empirical_n"] == 0, "production authority template cannot increase N")


def validate_continuity(data: dict[str, Any]) -> None:
    require(data["record_type"] == "P4_B_MODE_T_FINAL_CONTINUITY_ACCEPTANCE_TEMPLATE", "wrong continuity record type")
    require(data["status"] == "TEMPLATE_NOT_EXECUTED", "continuity template must remain inert")
    binding = data["candidate_binding"]
    require(binding["candidate_commit_sha"] is None and binding["candidate_tree_sha"] is None, "continuity template cannot preselect candidate")
    run = data["protected_run"]
    require(run["run_id"] is None and run["ciphertext_sha256"] is None, "continuity protected-run identity must remain unset")
    require(run["protected_plaintext_emitted"] is False and run["protected_key_or_mapping_emitted"] is False, "continuity template cannot emit protected material")
    strict = data["strict_chain_verification"]
    require(strict["network_metadata_preflight_verified"] is False, "strict-chain verification cannot be preverified")
    require(strict["strict_mode_used"] is False, "strict mode cannot be claimed before execution")
    require(data["retention"]["independent_rehash_match"] is False, "continuity retention cannot be preverified")
    adjudication = data["independent_adjudication"]
    require(adjudication["classification"] == "NOT_EXECUTED", "continuity adjudication cannot be preexecuted")
    require(adjudication["accepted"] is False, "continuity cannot be preaccepted")
    require(data["non_effects"]["empirical_n"] == 0, "continuity template cannot increase N")


def validate_candidate(data: dict[str, Any]) -> None:
    require(data["record_type"] == "PDMAL_V0_7_6_FINAL_CANDIDATE_DESIGNATION_TEMPLATE", "wrong candidate record type")
    require(data["status"] == "TEMPLATE_NOT_DESIGNATED", "candidate template must remain NOT_DESIGNATED")
    designation = data["designation"]
    require(all(value is None for value in designation.values()), "candidate identity/actor/timestamp must remain null")
    prereq = data["designation_prerequisites"]
    for key, value in prereq.items():
        if key == "empirical_n_still_zero":
            require(value is True, "empirical N zero invariant must be true")
        else:
            require(value is False, f"candidate prerequisite unexpectedly satisfied: {key}")
    require(data["post_designation_required_sequence"]["separate_pilot_authorization"] == "NOT_GRANTED", "pilot authorization promoted")
    effects = data["non_effects"]
    require(
        effects
        == {
            "freeze_established": False,
            "pilot_authorized": False,
            "empirical_execution_performed": False,
            "empirical_n": 0,
        },
        "candidate template changed scientific state",
    )


def validate_authorization(data: dict[str, Any]) -> None:
    require(data["record_type"] == "PDMAL_V0_7_6_PILOT_AUTHORIZATION_TEMPLATE", "wrong authorization record type")
    require(data["status"] == "NOT_AUTHORIZED", "authorization template must remain NOT_AUTHORIZED")
    require(data["candidate"]["commit_sha"] is None and data["candidate"]["tree_sha"] is None, "authorization template cannot preselect candidate")
    require(data["freeze"]["verified"] is False, "authorization template cannot pre-verify freeze")
    require(
        all(value is False for key, value in data["gate_prerequisites"].items() if key != "unresolved_blocking_findings"),
        "authorization prerequisite promoted",
    )
    require(data["gate_prerequisites"]["unresolved_blocking_findings"] is True, "template must retain blocking findings")
    require(all(value is False for value in data["permitted_actions"].values()), "authorization template cannot permit execution")
    require(
        data["current_state"]
        == {
            "freeze": "NOT_ESTABLISHED",
            "authorization": "NOT_GRANTED",
            "empirical_n": 0,
        },
        "authorization template changed current state",
    )


def validate_all() -> None:
    require(git_blob(STAGE_A_PROCEDURE) == EXPECTED_STAGE_A_PROCEDURE_BLOB, "bound Stage-A procedure blob mismatch")
    require(git_blob(REVIEW_MANIFEST) == EXPECTED_REVIEW_MANIFEST_BLOB, "bound #320 review manifest blob mismatch")
    validate_stage_a_input(load_json(STAGE_A_INPUT))
    validate_stage_a_evidence(load_json(STAGE_A_EVIDENCE))
    validate_production_authority(load_json(PROD_AUTHORITY))
    validate_continuity(load_json(CONTINUITY))
    validate_candidate(load_json(CANDIDATE))
    validate_authorization(load_json(AUTHORIZATION))


def expect_failure(fn: Callable[[dict[str, Any]], None], data: dict[str, Any], label: str) -> None:
    try:
        fn(data)
    except ValidationError:
        return
    raise ValidationError(f"negative control did not fail closed: {label}")


def self_test() -> None:
    stage_a = load_json(STAGE_A_INPUT)
    mutated = copy.deepcopy(stage_a)
    mutated["execution_permission"]["operator_approved_real_cloud_qualification"] = True
    expect_failure(validate_stage_a_input, mutated, "Stage-A execution promotion")

    evidence = load_json(STAGE_A_EVIDENCE)
    mutated = copy.deepcopy(evidence)
    mutated["adjudication"]["stage_a_outcome"] = "PASS"
    expect_failure(validate_stage_a_evidence, mutated, "synthetic PASS promotion")

    authority = load_json(PROD_AUTHORITY)
    mutated = copy.deepcopy(authority)
    mutated["adjudication"]["production_authority_established"] = True
    expect_failure(validate_production_authority, mutated, "production authority promotion")

    continuity = load_json(CONTINUITY)
    mutated = copy.deepcopy(continuity)
    mutated["independent_adjudication"]["accepted"] = True
    expect_failure(validate_continuity, mutated, "continuity preacceptance")

    candidate = load_json(CANDIDATE)
    mutated = copy.deepcopy(candidate)
    mutated["designation"]["candidate_commit_sha"] = "0" * 40
    expect_failure(validate_candidate, mutated, "candidate predesignation")

    authorization = load_json(AUTHORIZATION)
    mutated = copy.deepcopy(authorization)
    mutated["permitted_actions"]["blinded_pilot_execution"] = True
    expect_failure(validate_authorization, mutated, "pilot preauthorization")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    validate_all()
    if args.self_test:
        self_test()
    print("external-acceptance readiness templates: PASS (inert/fail-closed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
