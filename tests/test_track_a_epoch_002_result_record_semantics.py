from __future__ import annotations

import importlib.util
import json
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_result_record_semantics.py"
SPEC = importlib.util.spec_from_file_location("epoch_002_result_semantics", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

ALL_NON_EFFECTS = {
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
}


def record(
    record_type: str,
    record_id: str,
    *,
    status: str = "PASS",
    predecessors: list[str] | None = None,
    effect: str = "NONE",
    non_effects: set[str] | None = None,
) -> dict:
    return {
        "record_type": record_type,
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "record_id": record_id,
        "generated_at_utc": "2026-09-10T00:00:00Z",
        "producer": {"system": "semantic-test", "version_or_commit": "944e746"},
        "immutable_subject": {"commit_sha": "a" * 40},
        "evidence_scope": "prospective semantic test only",
        "non_effects": sorted(non_effects if non_effects is not None else ALL_NON_EFFECTS),
        "status": status,
        "predecessor_record_ids": predecessors or [],
        "authorization_effect": effect,
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def write_ledger(tmp_path: Path, records: list[dict]) -> Path:
    path = tmp_path / "ledger.json"
    path.write_text(json.dumps(records), encoding="utf-8")
    return path


def test_policy_is_complete_and_non_authorizing() -> None:
    policy = MODULE.validate_policy()
    assert policy["policy_effect"] == MODULE.EXPECTED_POLICY_EFFECT
    assert set(policy["records"]) == set(MODULE.EXPECTED_RECORD_CLASS)


def test_observational_pass_requires_full_non_authorization_ceiling() -> None:
    policy = MODULE.validate_policy()
    MODULE.validate_record_semantics(record("QC_LEDGER", "E002-QC-0001"), policy)

    weakened = record("QC_LEDGER", "E002-QC-0001")
    weakened["non_effects"].remove("DOES_NOT_AUTHORIZE_HIGH_ASSURANCE")
    with pytest.raises(SystemExit, match="non_effects mismatch"):
        MODULE.validate_record_semantics(weakened, policy)


def test_dataset_lock_requires_separate_exact_unblinding_commit() -> None:
    policy = MODULE.validate_policy()
    locked = record(
        "DATASET_LOCK_RECEIPT",
        "E002-LOCK-0001",
        effect="REQUIRES_SEPARATE_EXACT_COMMIT",
    )
    MODULE.validate_record_semantics(locked, policy)

    promoted = deepcopy(locked)
    promoted["authorization_effect"] = "BOUNDED_RECORD_ONLY"
    with pytest.raises(SystemExit, match="authorization_effect mismatch"):
        MODULE.validate_record_semantics(promoted, policy)


def test_unblinding_pass_is_bounded_human_authority_only() -> None:
    policy = MODULE.validate_policy()
    non_effects = ALL_NON_EFFECTS - {"DOES_NOT_AUTHORIZE_UNBLINDING"}
    unblinding = record(
        "UNBLINDING_DECISION_RECORD",
        "E002-UNBLIND-0001",
        effect="BOUNDED_RECORD_ONLY",
        non_effects=non_effects,
    )
    MODULE.validate_record_semantics(unblinding, policy)

    contradiction = deepcopy(unblinding)
    contradiction["non_effects"].append("DOES_NOT_AUTHORIZE_UNBLINDING")
    with pytest.raises(SystemExit, match="non_effects mismatch"):
        MODULE.validate_record_semantics(contradiction, policy)


def test_blocked_unblinding_fails_closed_to_zero_authority() -> None:
    policy = MODULE.validate_policy()
    blocked = record(
        "UNBLINDING_DECISION_RECORD",
        "E002-UNBLIND-0001",
        status="BLOCKED",
        effect="NONE",
    )
    MODULE.validate_record_semantics(blocked, policy)

    leaked_authority = deepcopy(blocked)
    leaked_authority["authorization_effect"] = "BOUNDED_RECORD_ONLY"
    leaked_authority["non_effects"].remove("DOES_NOT_AUTHORIZE_UNBLINDING")
    with pytest.raises(SystemExit, match="authorization_effect mismatch"):
        MODULE.validate_record_semantics(leaked_authority, policy)


def test_materialization_cannot_self_authorize_primary_analysis() -> None:
    policy = MODULE.validate_policy()
    materialization = record(
        "MATERIALIZATION_RECEIPT",
        "E002-MATERIALIZE-0001",
        effect="REQUIRES_SEPARATE_EXACT_COMMIT",
    )
    MODULE.validate_record_semantics(materialization, policy)


def test_primary_analysis_pass_is_bounded_and_not_efficacy() -> None:
    policy = MODULE.validate_policy()
    non_effects = ALL_NON_EFFECTS - {"DOES_NOT_AUTHORIZE_ANALYSIS"}
    authorization = record(
        "PRIMARY_ANALYSIS_AUTHORIZATION_RECORD",
        "E002-ANALYSIS-AUTH-0001",
        effect="BOUNDED_RECORD_ONLY",
        non_effects=non_effects,
    )
    MODULE.validate_record_semantics(authorization, policy)

    promoted = deepcopy(authorization)
    promoted["scientific_state_effect"]["canonical_dgaf_efficacy"] = "ESTABLISHED"
    with pytest.raises(SystemExit, match="scientific-state promotion"):
        MODULE.validate_record_semantics(promoted, policy)


def test_partial_blocked_ledger_passes_structural_and_semantic_validation(tmp_path: Path) -> None:
    MODULE.validate_ledger(
        write_ledger(
            tmp_path,
            [record("PRECOLLECTION_GATE_CHECKLIST", "E002-GATE-0001", status="BLOCKED")],
        )
    )


def test_structurally_valid_record_with_wrong_semantics_fails(tmp_path: Path) -> None:
    first = record("PRECOLLECTION_GATE_CHECKLIST", "E002-GATE-0001")
    second = record(
        "COLLECTION_START_RECEIPT",
        "E002-START-0001",
        predecessors=["E002-GATE-0001"],
        effect="BOUNDED_RECORD_ONLY",
    )
    with pytest.raises(SystemExit, match="authorization_effect mismatch"):
        MODULE.validate_ledger(write_ledger(tmp_path, [first, second]))


def test_policy_mutation_cannot_reclassify_human_authorization() -> None:
    policy = MODULE.validate_policy()
    mutated = deepcopy(policy)
    mutated["records"]["UNBLINDING_DECISION_RECORD"]["authority_class"] = "NONAUTHORIZING_OBSERVATION"
    original = MODULE.load_object
    try:
        MODULE.load_object = lambda path, label: mutated if path == MODULE.POLICY_PATH else original(path, label)
        with pytest.raises(SystemExit, match="authority_class drift"):
            MODULE.validate_policy()
    finally:
        MODULE.load_object = original
