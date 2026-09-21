"""Read-only, fail-closed AOSS Stage-A static identity preflight."""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


class PreflightError(RuntimeError):
    """Raised when a required static preflight predicate fails."""

    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        message = code if not detail else f"{code}: {detail}"
        super().__init__(message)


@dataclass(frozen=True)
class ExpectedBindings:
    dgaf_receipt_commit: str
    dgaf_authorization_commit: str
    protected_source_basis: str
    acp_commit: str
    contract_blobs: Mapping[str, str]
    executable_blobs: Mapping[str, str]


DEFAULT_BINDINGS = ExpectedBindings(
    dgaf_receipt_commit="6baea5a6b6a316add6292cc647f5b455eb235ce3",
    dgaf_authorization_commit="854b9d5adb33c6ee6158a63017f133f20b90742e",
    protected_source_basis="807216df1bd5b28c677b8c42822975b2941c1211",
    acp_commit="dbab7c1afafec524ce7c18157de2089cafe79c87",
    contract_blobs={
        "registry/aoss_v0_6_acp_measurement_manifest_v1.json": "1c690abbe2ab451f5081f56c25970eb85b031ce4",
        "registry/aoss_v0_6_stage_a_analysis_multiplicity_contract_v1.json": "8e95d00e6cc12f95336b004c75c3771ac7530bf6",
        "registry/aoss_v0_6_stage_a_decision_policy_v1.json": "b93f01af1825e93279e945f7dc07f299daab89bb",
        "registry/aoss_v0_6_stage_a_episode_eligibility_repetition_v1.json": "f91735ae51b44921e78a50e9f6bb4486750ba96f",
        "registry/aoss_v0_6_stage_a_failure_ground_truth_v1.json": "02a393bf025df6dbd8bd0126a0626a31d832ee00",
        "registry/aoss_v0_6_stage_a_freshness_calibration_v1.json": "694ecec6c7214e5c4047f6d7de612513d176b740",
        "registry/aoss_v0_6_stage_a_observer_measurement_boundary_v1.json": "108dc570dd5dc1903e49a2b4afbf9a4eb3d604ce",
        "registry/aoss_v0_6_stage_a_practical_effect_adoption_rule_v1.json": "4576366f839f80af1fcb1318a3a9ac69f90e7244",
        "registry/aoss_v0_6_stage_a_primary_comparator_amendment_v1.json": "aaf2a62399158dda0ffdc3006d6b7fbe64a1d0e8",
    },
    executable_blobs={
        "scripts/aoss_v0_6_acp_adapter.py": "a2505deb457157e535bab713150d49d3950f789f",
        "scripts/aoss_v0_6_stage_a_decision_policy.py": "dd03a34fe17579c57dcf386abac9f1f5e7eb23de",
        "scripts/aoss_v0_6_stage_a_acp_direct_baseline.py": "f1846d00084b9e0a1b1ddbd21999f1ce9627c4f5",
    },
)

AUTH_REL = "registry/aoss_v0_6_stage_a_collection_authorization_v1.json"
RECEIPT_REL = "registry/aoss_v0_6_stage_a_precollection_receipt_v1.json"


def _git(root: Path, *args: str) -> str:
    env = os.environ.copy()
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "stderr", "") or str(exc)
        raise PreflightError("GIT_COMMAND_FAILED", detail.strip()) from exc
    return completed.stdout.strip()


def _require_repository(root: Path, code: str) -> None:
    if not root.exists() or not root.is_dir():
        raise PreflightError(code)
    try:
        _git(root, "rev-parse", "--git-dir")
    except PreflightError as exc:
        raise PreflightError(code) from exc


def _require_clean_full_repo(root: Path, label: str) -> None:
    if _git(root, "rev-parse", "--is-shallow-repository") != "false":
        raise PreflightError(f"{label}_SHALLOW_REPOSITORY")
    if _git(root, "for-each-ref", "--format=%(refname)", "refs/replace"):
        raise PreflightError(f"{label}_REPLACE_OBJECTS_PRESENT")
    if _git(root, "status", "--porcelain=v1", "--untracked-files=all"):
        raise PreflightError(f"{label}_WORKTREE_DIRTY")


def _blob_at(root: Path, ref: str, path: str) -> str:
    return _git(root, "rev-parse", f"{ref}:{path}")


def _working_blob(root: Path, path: str) -> str:
    target = root / path
    if not target.is_file():
        raise PreflightError("REQUIRED_FILE_MISSING", path)
    return _git(root, "hash-object", "--", path)


def _require_blob(root: Path, ref: str, path: str, expected: str) -> None:
    actual_ref = _blob_at(root, ref, path)
    if actual_ref != expected:
        raise PreflightError("ACCEPTED_BLOB_MISMATCH", f"{path} {actual_ref} != {expected}")
    actual_working = _working_blob(root, path)
    if actual_working != expected:
        raise PreflightError("WORKTREE_BLOB_MISMATCH", f"{path} {actual_working} != {expected}")


def _require_event_history(root: Path, path: str, expected_commit: str, code: str) -> None:
    history = [line for line in _git(root, "log", "--format=%H", "HEAD", "--", path).splitlines() if line]
    if history != [expected_commit]:
        raise PreflightError(code, f"{path} history={history}")


def _require_json_contracts(dgaf: Path) -> None:
    try:
        authorization = json.loads((dgaf / AUTH_REL).read_text(encoding="utf-8"))
        receipt = json.loads((dgaf / RECEIPT_REL).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PreflightError("AUTHORIZATION_RECEIPT_INVALID", str(exc)) from exc
    if authorization.get("status") != "AUTHORIZED_BOUNDED_STAGE_A_COLLECTION":
        raise PreflightError("AUTHORIZATION_STATUS_INVALID")
    if authorization.get("outcome_collection_authorized") is not True:
        raise PreflightError("AUTHORIZATION_SCOPE_INVALID")
    if receipt.get("status") != "PASS" or receipt.get("outcomes_generated_before_receipt") is not False:
        raise PreflightError("PRECOLLECTION_RECEIPT_INVALID")
    if receipt.get("scientific_n_increment") != 0:
        raise PreflightError("SCIENTIFIC_N_INCREMENT_INVALID")


def _inspect_preflight(dgaf: Path, acp: Path, bindings: ExpectedBindings) -> dict[str, object]:
    dgaf = Path(dgaf)
    acp = Path(acp)
    _require_repository(dgaf, "DGAF_REPOSITORY_MISSING")
    _require_repository(acp, "ACP_REPOSITORY_MISSING")
    _require_clean_full_repo(dgaf, "DGAF")
    _require_clean_full_repo(acp, "ACP")

    acp_head = _git(acp, "rev-parse", "HEAD")
    if acp_head != bindings.acp_commit:
        raise PreflightError("ACP_COMMIT_MISMATCH", acp_head)

    dgaf_head = _git(dgaf, "rev-parse", "HEAD")
    for ancestor, code in (
        (bindings.dgaf_authorization_commit, "AUTHORIZATION_COMMIT_NOT_ANCESTOR"),
        (bindings.dgaf_receipt_commit, "RECEIPT_COMMIT_NOT_ANCESTOR"),
    ):
        try:
            _git(dgaf, "merge-base", "--is-ancestor", ancestor, dgaf_head)
        except PreflightError as exc:
            raise PreflightError(code) from exc

    receipt_lineage = _git(dgaf, "rev-list", "--parents", "-n", "1", bindings.dgaf_receipt_commit).split()
    if receipt_lineage != [bindings.dgaf_receipt_commit, bindings.dgaf_authorization_commit]:
        raise PreflightError("RECEIPT_AUTHORIZATION_LINEAGE_INVALID")

    for path, expected in bindings.contract_blobs.items():
        _require_blob(dgaf, bindings.protected_source_basis, path, expected)
    for path, expected in bindings.executable_blobs.items():
        _require_blob(dgaf, "HEAD", path, expected)

    _require_event_history(
        dgaf,
        AUTH_REL,
        bindings.dgaf_authorization_commit,
        "AUTHORIZATION_EVENT_HISTORY_MUTATED",
    )
    _require_event_history(
        dgaf,
        RECEIPT_REL,
        bindings.dgaf_receipt_commit,
        "RECEIPT_EVENT_HISTORY_MUTATED",
    )

    current_auth = _working_blob(dgaf, AUTH_REL)
    accepted_auth = _blob_at(dgaf, bindings.dgaf_authorization_commit, AUTH_REL)
    if current_auth != accepted_auth:
        raise PreflightError("AUTHORIZATION_BYTES_DRIFTED")
    current_receipt = _working_blob(dgaf, RECEIPT_REL)
    accepted_receipt = _blob_at(dgaf, bindings.dgaf_receipt_commit, RECEIPT_REL)
    if current_receipt != accepted_receipt:
        raise PreflightError("RECEIPT_BYTES_DRIFTED")

    _require_json_contracts(dgaf)

    return {
        "record_type": "AOSS_STAGE_A_STATIC_PREFLIGHT",
        "static_identity_checks": "PASS",
        "dgaf_head": dgaf_head,
        "acp_head": acp_head,
        "collection_readiness": "NOT_ESTABLISHED",
        "mapping_binding": "NOT_ESTABLISHED",
        "runtime_binding": "NOT_ESTABLISHED",
        "scientific_n_increment": 0,
        "outcomes_generated": False,
        "external_validation_established": False,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }


def inspect_preflight(dgaf: Path, acp: Path) -> dict[str, object]:
    """Inspect exact static identities without executing or importing ACP."""

    return _inspect_preflight(dgaf, acp, DEFAULT_BINDINGS)
