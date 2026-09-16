from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_002_primary_analysis_authorization.py"
WORKFLOW_PATH = ROOT / ".github/workflows/track-a-epoch-002-primary-analysis-authorization.yml"
PROCEDURE_PATH = ROOT / "docs/experiment/TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_PROCEDURE.md"

FULL_NON_EFFECTS = [
    "DOES_NOT_AUTHORIZE_COLLECTION",
    "DOES_NOT_AUTHORIZE_UNBLINDING",
    "DOES_NOT_AUTHORIZE_ANALYSIS",
    "DOES_NOT_INCREMENT_SCIENTIFIC_N",
    "DOES_NOT_ESTABLISH_CANONICAL_DGAF_EFFICACY",
    "DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION",
    "DOES_NOT_AUTHORIZE_HIGH_ASSURANCE",
]
AUTHORIZATION_NON_EFFECTS = [effect for effect in FULL_NON_EFFECTS if effect != "DOES_NOT_AUTHORIZE_ANALYSIS"]


def load_validator():
    assert MODULE_PATH.exists(), "Epoch 002 primary-analysis authorization validator is missing"
    spec = importlib.util.spec_from_file_location(
        "epoch_002_primary_analysis_authorization",
        MODULE_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def materialization_receipt_fixture() -> dict:
    return {
        "record_type": "MATERIALIZATION_RECEIPT",
        "schema_version": 1,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002",
        "epoch": 2,
        "record_id": "E002-MATERIALIZE-RECEIPT-0001",
        "generated_at_utc": "2026-09-16T12:00:00Z",
        "producer": {
            "system": "DGAF_TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT_VALIDATOR",
            "version_or_commit": "1" * 40,
        },
        "immutable_subject": {
            "commit_sha": "2" * 40,
            "sha256": "3" * 64,
        },
        "evidence_scope": "DETERMINISTIC_EPOCH_002_ANALYSIS_INPUT_MATERIALIZATION_AFTER_BOUNDED_UNBLINDING",
        "non_effects": list(FULL_NON_EFFECTS),
        "status": "PASS",
        "predecessor_record_ids": ["E002-UNBLINDING-00112233"],
        "authorization_effect": "REQUIRES_SEPARATE_EXACT_COMMIT",
        "scientific_state_effect": {
            "empirical_n_increment": 0,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        },
    }


def valid_authorization(validator) -> dict:
    return validator.expected_authorization(
        materialization_receipt_fixture(),
        materialization_receipt_commit_sha="a" * 40,
        materialization_receipt_sha256="b" * 64,
        authorization_parent_sha="c" * 40,
        generated_at_utc="2026-09-16T13:00:00Z",
    )


def validate_fixture(validator, authorization: dict) -> None:
    validator.validate_authorization_object(
        authorization,
        materialization_receipt_fixture(),
        materialization_receipt_commit_sha="a" * 40,
        materialization_receipt_sha256="b" * 64,
        authorization_parent_sha="c" * 40,
    )


def install_valid_event_fixture(monkeypatch: pytest.MonkeyPatch, validator):
    head = "d" * 40
    parent = "c" * 40
    receipt_event = "a" * 40
    receipt_parent = "9" * 40
    receipt = materialization_receipt_fixture()
    receipt_bytes = (json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n").encode()
    receipt_sha256 = hashlib.sha256(receipt_bytes).hexdigest()
    authorization = validator.expected_authorization(
        receipt,
        materialization_receipt_commit_sha=receipt_event,
        materialization_receipt_sha256=receipt_sha256,
        authorization_parent_sha=parent,
        generated_at_utc="2026-09-16T13:00:00Z",
    )

    state: dict[str, Any] = {
        "receipt_exists_parent": True,
        "receipt_exists_head": True,
        "result_exists_parent": False,
        "result_exists_head": False,
        "receipt_history": [receipt_event],
        "receipt_changed_files": [validator.MATERIALIZATION_RECEIPT_REL],
        "receipt_bytes_parent": receipt_bytes,
        "receipt_bytes_head": receipt_bytes,
    }

    def fake_git(*args: str) -> str:
        if args == ("log", "--format=%H", "--", validator.MATERIALIZATION_RECEIPT_REL):
            return "\n".join(state["receipt_history"])
        if args == ("rev-list", "--parents", "-n", "1", receipt_event):
            return f"{receipt_event} {receipt_parent}"
        if args == ("diff-tree", "--no-commit-id", "--name-only", "-r", receipt_event):
            return "\n".join(state["receipt_changed_files"])
        if args == ("merge-base", "--is-ancestor", receipt_event, parent):
            return ""
        raise AssertionError(f"unexpected git call: {args}")

    def fake_exists(spec: str) -> bool:
        values = {
            f"{parent}:{validator.MATERIALIZATION_RECEIPT_REL}": state["receipt_exists_parent"],
            f"{head}:{validator.MATERIALIZATION_RECEIPT_REL}": state["receipt_exists_head"],
            f"{receipt_parent}:{validator.MATERIALIZATION_RECEIPT_REL}": False,
            f"{parent}:{validator.RESULT_REL}": state["result_exists_parent"],
            f"{head}:{validator.RESULT_REL}": state["result_exists_head"],
            f"{head}:{validator.AUTH_REL}": True,
        }
        return bool(values.get(spec, False))

    def fake_load_json_at_ref(ref: str, relpath: str) -> dict:
        if relpath == validator.MATERIALIZATION_RECEIPT_REL and ref in {parent, head}:
            return receipt
        if relpath == validator.AUTH_REL and ref == head:
            return authorization
        raise AssertionError(f"unexpected JSON read: {ref}:{relpath}")

    def fake_read_git_bytes(ref: str, relpath: str) -> bytes:
        if relpath != validator.MATERIALIZATION_RECEIPT_REL:
            raise AssertionError(f"unexpected byte read: {ref}:{relpath}")
        if ref == parent:
            return state["receipt_bytes_parent"]
        if ref == head:
            return state["receipt_bytes_head"]
        raise AssertionError(f"unexpected byte read: {ref}:{relpath}")

    monkeypatch.setattr(validator, "validate_authorization_event_shape", lambda event_head: parent)
    monkeypatch.setattr(validator, "validate_frozen_analysis_identities", lambda ref: None)
    monkeypatch.setattr(validator, "validate_semantic_policy", lambda: None, raising=False)
    monkeypatch.setattr(validator, "git", fake_git)
    monkeypatch.setattr(validator, "git_object_exists", fake_exists)
    monkeypatch.setattr(validator, "load_json_at_ref", fake_load_json_at_ref)
    monkeypatch.setattr(validator, "read_git_bytes", fake_read_git_bytes, raising=False)

    return head, parent, receipt_event, state


def validate_event_fixture(validator, head: str, parent: str) -> str:
    return validator.validate_authorization_event(head, accepted_parent_sha=parent)


def test_authorization_binds_exact_materialization_receipt_and_parent() -> None:
    validator = load_validator()
    receipt = materialization_receipt_fixture()
    authorization = valid_authorization(validator)

    validate_fixture(validator, authorization)

    assert authorization["predecessor_record_ids"] == [receipt["record_id"]]
    assert authorization["immutable_subject"] == {
        "commit_sha": "a" * 40,
        "sha256": "b" * 64,
    }
    assert authorization["producer"]["version_or_commit"] == "c" * 40


def test_authorization_scope_is_locked_primary_analysis_only() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)

    assert authorization["record_type"] == "PRIMARY_ANALYSIS_AUTHORIZATION_RECORD"
    assert authorization["evidence_scope"] == "LOCKED_PRIMARY_ANALYSIS_ONLY"
    assert authorization["authorization_effect"] == "BOUNDED_RECORD_ONLY"
    assert authorization["non_effects"] == AUTHORIZATION_NON_EFFECTS
    assert authorization["scientific_state_effect"] == {
        "empirical_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
    }


def test_authorization_rejects_scope_widening() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)
    authorization["evidence_scope"] = "PRIMARY_AND_EXPLORATORY_ANALYSIS"

    with pytest.raises(SystemExit):
        validate_fixture(validator, authorization)


def test_authorization_rejects_wrong_materialization_predecessor() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)
    authorization["predecessor_record_ids"] = ["E002-MATERIALIZE-RECEIPT-WRONG"]

    with pytest.raises(SystemExit):
        validate_fixture(validator, authorization)


def test_authorization_rejects_materialization_content_drift() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)
    authorization["immutable_subject"]["sha256"] = "d" * 64

    with pytest.raises(SystemExit):
        validate_fixture(validator, authorization)


def test_authorization_rejects_parent_binding_drift() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)
    authorization["producer"]["version_or_commit"] = "d" * 40

    with pytest.raises(SystemExit):
        validate_fixture(validator, authorization)


def test_authorization_rejects_secret_bearing_extension() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)
    authorization["private_key"] = "must-never-be-admitted"

    with pytest.raises(SystemExit):
        validate_fixture(validator, authorization)


def test_authorization_rejects_false_independence_or_claim_promotion() -> None:
    validator = load_validator()
    authorization = valid_authorization(validator)
    authorization["non_effects"].remove("DOES_NOT_ESTABLISH_INDEPENDENT_VALIDATION")

    with pytest.raises(SystemExit):
        validate_fixture(validator, authorization)


def test_frozen_epoch_002_analysis_identities_are_exact() -> None:
    validator = load_validator()

    assert validator.PREREG_BLOB_SHA == "9668ec54e50c40b04d40cfa64b817950df4bbffa"
    assert validator.ANALYSIS_LOCK_BLOB_SHA == "26980e27185b3a77980204b2d46a4fdab7e5fc7e"
    assert validator.ANALYSIS_BLOB_SHA == "d4495f7cdf211b974039ec0e66292dc62ea0881f"
    assert validator.ANALYSIS_CONFIG_SHA256 == "a008832cc9e353f323ed18cacf5529e700e73e18fe374aac9e2dcd54bcb10d73"
    assert validator.REQUIREMENTS_BLOB_SHA == "00c1f779e97030f9b25ae494642edb31b5b09de5"


def test_tooling_mode_preserves_authorization_and_result_absence() -> None:
    validator = load_validator()
    validator.validate_tooling_only()


def test_event_shape_rejects_extra_changed_file(monkeypatch: pytest.MonkeyPatch) -> None:
    validator = load_validator()
    head = "d" * 40
    parent = "c" * 40

    def fake_git(*args: str) -> str:
        if args[:4] == ("rev-list", "--parents", "-n", "1"):
            return f"{head} {parent}"
        if args[:4] == ("diff-tree", "--no-commit-id", "--name-only", "-r"):
            return f"{validator.AUTH_REL}\nREADME.md"
        if args[:3] == ("log", "--format=%H", "--"):
            return head
        raise AssertionError(f"unexpected git call: {args}")

    monkeypatch.setattr(validator, "git", fake_git)
    monkeypatch.setattr(validator, "git_object_exists", lambda spec: False)

    with pytest.raises(SystemExit):
        validator.validate_authorization_event_shape(head)


def test_event_shape_rejects_preexisting_authorization(monkeypatch: pytest.MonkeyPatch) -> None:
    validator = load_validator()
    head = "d" * 40
    parent = "c" * 40

    def fake_git(*args: str) -> str:
        if args[:4] == ("rev-list", "--parents", "-n", "1"):
            return f"{head} {parent}"
        if args[:4] == ("diff-tree", "--no-commit-id", "--name-only", "-r"):
            return validator.AUTH_REL
        if args[:3] == ("log", "--format=%H", "--"):
            return head
        raise AssertionError(f"unexpected git call: {args}")

    monkeypatch.setattr(validator, "git", fake_git)
    monkeypatch.setattr(validator, "git_object_exists", lambda spec: spec == f"{parent}:{validator.AUTH_REL}")

    with pytest.raises(SystemExit):
        validator.validate_authorization_event_shape(head)


def test_authorization_event_validates_immutable_materialization_predecessor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    head, parent, _, _ = install_valid_event_fixture(monkeypatch, validator)

    assert validate_event_fixture(validator, head, parent) == parent


def test_authorization_event_rejects_unaccepted_parent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    head, _, _, _ = install_valid_event_fixture(monkeypatch, validator)

    with pytest.raises(SystemExit):
        validator.validate_authorization_event(head, accepted_parent_sha="e" * 40)


def test_authorization_event_rejects_missing_materialization_receipt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    head, parent, _, state = install_valid_event_fixture(monkeypatch, validator)
    state["receipt_exists_parent"] = False

    with pytest.raises(SystemExit):
        validate_event_fixture(validator, head, parent)


def test_authorization_event_rejects_preexisting_locked_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    head, parent, _, state = install_valid_event_fixture(monkeypatch, validator)
    state["result_exists_parent"] = True

    with pytest.raises(SystemExit):
        validate_event_fixture(validator, head, parent)


def test_authorization_event_rejects_receipt_content_drift(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    head, parent, _, state = install_valid_event_fixture(monkeypatch, validator)
    state["receipt_bytes_head"] = b"drifted-materialization-receipt\n"

    with pytest.raises(SystemExit):
        validate_event_fixture(validator, head, parent)


def test_authorization_event_rejects_nonunique_receipt_history(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    head, parent, receipt_event, state = install_valid_event_fixture(monkeypatch, validator)
    state["receipt_history"] = [receipt_event, "8" * 40]

    with pytest.raises(SystemExit):
        validate_event_fixture(validator, head, parent)


def test_authorization_event_rejects_invalid_receipt_event_shape(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = load_validator()
    head, parent, _, state = install_valid_event_fixture(monkeypatch, validator)
    state["receipt_changed_files"] = [validator.MATERIALIZATION_RECEIPT_REL, "README.md"]

    with pytest.raises(SystemExit):
        validate_event_fixture(validator, head, parent)


def test_primary_analysis_authorization_semantic_policy_is_exact() -> None:
    validator = load_validator()
    validator.validate_semantic_policy()


def test_ci_workflow_is_read_only_exact_head_and_never_runs_analysis() -> None:
    assert WORKFLOW_PATH.exists(), "Epoch 002 primary-analysis authorization workflow is missing"
    source = WORKFLOW_PATH.read_text(encoding="utf-8")

    required = (
        "permissions:\n  contents: read",
        "ref: ${{ github.event.pull_request.head.sha || github.sha }}",
        "fetch-depth: 0",
        "persist-credentials: false",
        "python scripts/validate_track_a_epoch_002_primary_analysis_authorization.py --tooling",
        "--event-commit HEAD",
        '--accepted-parent "${{ steps.mode.outputs.accepted_parent }}"',
        'accepted_parent="${{ github.event.pull_request.base.sha }}"',
        'accepted_parent="${{ github.event.before }}"',
        "TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json",
        "TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_RECORD.json",
        "TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json",
        "PRIMARY_ANALYSIS_RUN=FALSE",
        "SCIENTIFIC_N_INCREMENT=0",
        "CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED",
        "INDEPENDENT_VALIDATION=NOT_ESTABLISHED",
        "HIGH_ASSURANCE=NOT_AUTHORIZED",
    )
    for marker in required:
        assert marker in source, marker

    assert "python experiments/pdmal_pilot/track_a_epoch_002_analysis.py" not in source
    assert "run_primary_analysis" not in source


def test_procedure_preserves_prospective_fail_closed_boundary() -> None:
    assert PROCEDURE_PATH.exists(), "Epoch 002 primary-analysis authorization procedure is missing"
    source = PROCEDURE_PATH.read_text(encoding="utf-8")

    required = (
        "LOCKED_PRIMARY_ANALYSIS_ONLY",
        "TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json",
        "TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_RECORD.json",
        "TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json",
        "accepted protected-main parent",
        "exactly one parent",
        "exactly one changed file",
        "creation-only",
        "first-and-only history",
        "PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN",
        "SCIENTIFIC_N_INCREMENT=0",
        "CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED",
        "INDEPENDENT_VALIDATION=NOT_ESTABLISHED",
        "HIGH_ASSURANCE=NOT_AUTHORIZED",
        "2,250 blinded observations",
        "50 paired seed units",
    )
    for marker in required:
        assert marker in source, marker
