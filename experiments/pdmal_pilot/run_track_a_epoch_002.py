#!/usr/bin/env python3
"""Fail-closed Track A Epoch 002 collection runner.

Code presence is not authorization. Empirical execution requires a validated
successor custody receipt/certificate pair, completed precollection preflight,
immutable freeze, closure/verification chain, and a separate one-file
collection-authorization commit. PR validation cannot satisfy that predicate
and must never execute the preregistered scientific panel.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from time import monotonic
from typing import Iterable, Sequence

from harness_contract import canonical_json_bytes
from task_engine import SEED_RUNTIME_CEILING_SECONDS, AttemptStatus, ConsensusTask

PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
EPOCH_ID = "TRACK_A_EPOCH_002"
ALGORITHM_ID = "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1"
MODE = "track_a_epoch_002"
SEEDS = tuple(range(20270201, 20270251))
TOPOLOGIES = ("ring", "pdmal", "random_regular", "small_world", "complete")
FAILURE_COUNTS = (0, 1, 2, 3, 4, 5, 6, 8, 10)
EXPECTED_CELLS_PER_SEED = len(TOPOLOGIES) * len(FAILURE_COUNTS)
EXPECTED_TOTAL = len(SEEDS) * EXPECTED_CELLS_PER_SEED
CONDITION = "null"

RUNS_ROOT = Path("docs/experiment/track_a_runs")
CUSTODY_RECEIPT_PATH = RUNS_ROOT / "TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json"
CUSTODY_CERT_PATH = RUNS_ROOT / "TRACK_A_SUCCESSOR_CUSTODY_CERT.pem"
PREFLIGHT_PATH = RUNS_ROOT / "TRACK_A_EPOCH_002_PRECOLLECTION_PREFLIGHT.json"
FREEZE_PATH = RUNS_ROOT / "TRACK_A_EPOCH_002_IMMUTABLE_FREEZE_MANIFEST.json"
CLOSURE_PATH = RUNS_ROOT / "TRACK_A_EPOCH_002_FINAL_CLOSURE_PACKET.json"
VERIFICATION_PATH = RUNS_ROOT / "TRACK_A_EPOCH_002_VERIFICATION_CLASSIFICATION.json"
AUTH_PATH = RUNS_ROOT / "TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION.json"

PREREG_PATH = "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json"
ANALYSIS_LOCK_PATH = "docs/experiment/TRACK_A_EPOCH_002_ANALYSIS_LOCK.json"
RUNNER_CONTRACT_PATH = "docs/experiment/TRACK_A_EPOCH_002_RUNNER_CONTRACT.json"
ANALYSIS_PATH = "experiments/pdmal_pilot/track_a_epoch_002_analysis.py"
REQUIREMENTS_LOCK_PATH = "experiments/pdmal_pilot/requirements-full-lock.txt"
TASK_ENGINE_PATH = "experiments/pdmal_pilot/task_engine.py"
HARNESS_PATH = "experiments/pdmal_pilot/harness_contract.py"
TOPOLOGY_UTILS_PATH = "experiments/pdmal_pilot/topology_utils.py"
RUNNER_PATH = "experiments/pdmal_pilot/run_track_a_epoch_002.py"
CUSTODY_CONTRACT_PATH = "docs/experiment/TRACK_A_SUCCESSOR_SOLO_CUSTODY_CONTRACT.md"
CUSTODY_VALIDATOR_PATH = "scripts/validate_track_a_successor_solo_custody_receipt.py"

PROTECTED_SOURCE_PATHS = (
    PREREG_PATH,
    ANALYSIS_LOCK_PATH,
    RUNNER_CONTRACT_PATH,
    ANALYSIS_PATH,
    REQUIREMENTS_LOCK_PATH,
    TASK_ENGINE_PATH,
    HARNESS_PATH,
    TOPOLOGY_UTILS_PATH,
    RUNNER_PATH,
    CUSTODY_CONTRACT_PATH,
    CUSTODY_VALIDATOR_PATH,
    str(CUSTODY_RECEIPT_PATH),
    str(CUSTODY_CERT_PATH),
)

PREREG_MERGE_SHA = "eed3da6b0c4bae45f13871c45f42027da12ad36e"
PREREG_BLOB_SHA = "9668ec54e50c40b04d40cfa64b817950df4bbffa"
ANALYSIS_LOCK_MERGE_SHA = "45655263072767dd4279e48650e70935432982e5"
ANALYSIS_LOCK_BLOB_SHA = "26980e27185b3a77980204b2d46a4fdab7e5fc7e"
ANALYSIS_BLOB_SHA = "d4495f7cdf211b974039ec0e66292dc62ea0881f"
ANALYSIS_CONFIG_SHA256 = "a008832cc9e353f323ed18cacf5529e700e73e18fe374aac9e2dcd54bcb10d73"
REQUIREMENTS_LOCK_BLOB_SHA = "00c1f779e97030f9b25ae494642edb31b5b09de5"
TASK_ENGINE_BLOB_SHA = "90135e1c6dfccc3b56ffdc0dcb9eb50a0b2a5b05"
HARNESS_BLOB_SHA = "bb97c54ddf087fef568b1b3c8f8df72c30dad11e"
TOPOLOGY_UTILS_BLOB_SHA = "7ae92ba8a9ab964537e5dafa5e12de36b841391e"
CUSTODY_CONTRACT_BLOB_SHA = "96ba5e297e7645d3a91a52a4c1eda56af9c337a5"
CUSTODY_VALIDATOR_BLOB_SHA = "b2283a524f4eb8fd9191c953310ae264e0d8d369"

PUBLIC_RECORD_KEYS = frozenset(
    {
        "protocol_id",
        "algorithm_id",
        "frozen_candidate_sha",
        "seed_id",
        "blinded_topology_id",
        "failure_count",
        "ffcr_success",
        "excluded",
    }
)
PROHIBITED_PUBLIC_KEYS = frozenset(
    {
        "topology",
        "topology_name",
        "topology_fingerprint",
        "mapping",
        "blind_key",
        "blinding_key",
        "dgaf",
        "full_dgaf",
        "canonical_dgaf",
        "condition",
    }
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo_root(), text=True).strip()


def git_blob(path: str, *, revision: str | None = None) -> str:
    if revision is None:
        return _git("hash-object", path)
    return _git("rev-parse", f"{revision}:{path}")


def git_head() -> str:
    return _git("rev-parse", "HEAD").lower()


def git_tree(revision: str = "HEAD") -> str:
    return _git("rev-parse", f"{revision}^{{tree}}").lower()


def git_parents(revision: str = "HEAD") -> tuple[str, ...]:
    fields = _git("rev-list", "--parents", "-n", "1", revision).lower().split()
    return tuple(fields[1:])


def git_changed_paths(revision: str = "HEAD") -> tuple[str, ...]:
    output = _git("diff-tree", "--no-commit-id", "--name-only", "-r", revision)
    return tuple(line for line in output.splitlines() if line)


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=repo_root(),
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def git_path_history(path: str, revision: str = "HEAD") -> tuple[str, ...]:
    output = _git("log", "--format=%H", revision, "--", path).lower()
    return tuple(line for line in output.splitlines() if line)


def git_path_exists_at(path: str, revision: str) -> bool:
    completed = subprocess.run(
        ["git", "cat-file", "-e", f"{revision}:{path}"],
        cwd=repo_root(),
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def require_immutable_gate_history(candidate_sha: str, authorization_parent: str) -> None:
    gate_paths = (PREFLIGHT_PATH, FREEZE_PATH, CLOSURE_PATH, VERIFICATION_PATH)
    gate_commits: list[str] = []
    for path in gate_paths:
        history = git_path_history(str(path), authorization_parent)
        if len(history) != 1:
            raise SystemExit(
                f"Track A collection prohibited: {path} must have exactly one immutable "
                f"history commit; history={list(history)}"
            )
        gate_commits.append(history[0])
    preflight_commit, freeze_commit, closure_commit, verification_commit = gate_commits
    chain = (
        (candidate_sha, preflight_commit, "candidate->preflight"),
        (preflight_commit, freeze_commit, "preflight->freeze"),
        (freeze_commit, closure_commit, "freeze->closure"),
        (closure_commit, verification_commit, "closure->verification"),
        (
            verification_commit,
            authorization_parent,
            "verification->authorization-parent",
        ),
    )
    for ancestor, descendant, label in chain:
        if ancestor == descendant or not git_is_ancestor(ancestor, descendant):
            raise SystemExit(f"Track A collection prohibited: successor gate ordering violated ({label})")


def require_custody_history(candidate_sha: str, authorization_parent: str) -> None:
    receipt_history = git_path_history(str(CUSTODY_RECEIPT_PATH), authorization_parent)
    cert_history = git_path_history(str(CUSTODY_CERT_PATH), authorization_parent)
    if len(receipt_history) != 1 or len(cert_history) != 1:
        raise SystemExit(
            "Track A collection prohibited: custody receipt and certificate must each "
            "have exactly one immutable history commit"
        )
    if receipt_history[0] != cert_history[0]:
        raise SystemExit(
            "Track A collection prohibited: custody receipt and certificate must be " "introduced together"
        )
    custody_commit = receipt_history[0]
    if not git_is_ancestor(custody_commit, candidate_sha):
        raise SystemExit(
            "Track A collection prohibited: custody artifacts must predate or equal " "the frozen candidate"
        )


def load_json_object(path: Path, label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Track A collection prohibited: valid {label} file absent ({exc})") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"Track A collection prohibited: {label} must be a JSON object")
    return value


def require_exact_object(data: dict, expected: dict, label: str) -> None:
    if data != expected:
        missing = sorted(set(expected) - set(data))
        extra = sorted(set(data) - set(expected))
        mismatched = sorted(key for key in set(expected) & set(data) if data[key] != expected[key])
        raise SystemExit(
            f"Track A collection prohibited: {label} mismatch "
            f"missing={missing} extra={extra} mismatched={mismatched}"
        )


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certificate_public_key_der_sha256(path: Path) -> str:
    if shutil.which("openssl") is None:
        raise SystemExit("Track A collection prohibited: OpenSSL is required")
    public_pem = subprocess.check_output(["openssl", "x509", "-in", str(path), "-pubkey", "-noout"])
    public_der = subprocess.check_output(["openssl", "pkey", "-pubin", "-outform", "DER"], input=public_pem)
    return hashlib.sha256(public_der).hexdigest()


def load_custody_validator():
    path = repo_root() / CUSTODY_VALIDATOR_PATH
    spec = importlib.util.spec_from_file_location("track_a_successor_custody_validator", path)
    if spec is None or spec.loader is None:
        raise SystemExit("Track A collection prohibited: custody validator cannot load")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_custody_artifacts(receipt: dict) -> dict[str, str]:
    try:
        load_custody_validator().validate_receipt(receipt)
    except (AttributeError, ValueError) as exc:
        raise SystemExit(f"Track A collection prohibited: custody receipt validation failed ({exc})") from exc

    if not CUSTODY_CERT_PATH.is_file():
        raise SystemExit("Track A collection prohibited: custody certificate absent")
    certificate_sha = sha256_file(CUSTODY_CERT_PATH)
    certificate_public_sha = certificate_public_key_der_sha256(CUSTODY_CERT_PATH)
    if receipt["certificate_sha256"] != certificate_sha:
        raise SystemExit("Track A collection prohibited: custody certificate SHA-256 mismatch")
    if receipt["certificate_public_key_der_sha256"] != certificate_public_sha:
        raise SystemExit("Track A collection prohibited: custody certificate public-key fingerprint mismatch")
    if receipt["recovered_public_key_der_sha256"] != certificate_public_sha:
        raise SystemExit("Track A collection prohibited: recovered custody key does not match certificate")

    return {
        "custody_receipt_blob_sha": git_blob(str(CUSTODY_RECEIPT_PATH)),
        "custody_certificate_blob_sha": git_blob(str(CUSTODY_CERT_PATH)),
        "custody_encrypted_private_key_sha256": receipt["encrypted_private_key_sha256"],
        "custody_certificate_sha256": certificate_sha,
        "custody_certificate_public_key_der_sha256": certificate_public_sha,
    }


def require_source_bindings() -> None:
    expected = {
        PREREG_PATH: PREREG_BLOB_SHA,
        ANALYSIS_LOCK_PATH: ANALYSIS_LOCK_BLOB_SHA,
        ANALYSIS_PATH: ANALYSIS_BLOB_SHA,
        REQUIREMENTS_LOCK_PATH: REQUIREMENTS_LOCK_BLOB_SHA,
        TASK_ENGINE_PATH: TASK_ENGINE_BLOB_SHA,
        HARNESS_PATH: HARNESS_BLOB_SHA,
        TOPOLOGY_UTILS_PATH: TOPOLOGY_UTILS_BLOB_SHA,
        CUSTODY_CONTRACT_PATH: CUSTODY_CONTRACT_BLOB_SHA,
        CUSTODY_VALIDATOR_PATH: CUSTODY_VALIDATOR_BLOB_SHA,
    }
    for path, wanted in expected.items():
        actual = git_blob(path)
        if actual != wanted:
            raise SystemExit(f"Track A collection prohibited: source drift {path}: {actual} != {wanted}")


def expected_preflight(*, candidate_sha: str, candidate_tree_sha: str, custody: dict[str, str]) -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_002_PRECOLLECTION_PREFLIGHT",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "candidate_sha": candidate_sha,
        "candidate_tree_sha": candidate_tree_sha,
        "preregistration_merge_sha": PREREG_MERGE_SHA,
        "analysis_lock_merge_sha": ANALYSIS_LOCK_MERGE_SHA,
        "analysis_blob_sha": ANALYSIS_BLOB_SHA,
        "analysis_config_sha256": ANALYSIS_CONFIG_SHA256,
        "requirements_lock_blob_sha": REQUIREMENTS_LOCK_BLOB_SHA,
        "algorithm_id": ALGORITHM_ID,
        "matrix_cells_per_seed": EXPECTED_CELLS_PER_SEED,
        "expected_observations": EXPECTED_TOTAL,
        **custody,
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "custody_recovery_drill": "PASS",
        "preflight_status": "PASS",
        "scientific_n_increment": 0,
        "collection_authorized": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "high_assurance_authorized": False,
    }


def validate_preflight(
    data: dict,
    *,
    candidate_sha: str,
    candidate_tree_sha: str,
    custody: dict[str, str],
) -> None:
    require_exact_object(
        data,
        expected_preflight(
            candidate_sha=candidate_sha,
            candidate_tree_sha=candidate_tree_sha,
            custody=custody,
        ),
        "preflight",
    )


def expected_freeze(
    *,
    candidate_sha: str,
    candidate_tree_sha: str,
    preflight_blob_sha: str,
    protected_source_blobs: dict[str, str],
) -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_002_IMMUTABLE_FREEZE_MANIFEST",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "frozen_candidate_sha": candidate_sha,
        "frozen_candidate_tree_sha": candidate_tree_sha,
        "preflight_blob_sha": preflight_blob_sha,
        "protected_source_blobs": protected_source_blobs,
        "freeze_status": "ESTABLISHED",
        "scientific_n_increment": 0,
        "collection_authorized": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "high_assurance_authorized": False,
    }


def validate_freeze(
    data: dict,
    *,
    candidate_sha: str,
    candidate_tree_sha: str,
    preflight_blob_sha: str,
    protected_source_blobs: dict[str, str],
) -> None:
    require_exact_object(
        data,
        expected_freeze(
            candidate_sha=candidate_sha,
            candidate_tree_sha=candidate_tree_sha,
            preflight_blob_sha=preflight_blob_sha,
            protected_source_blobs=protected_source_blobs,
        ),
        "freeze manifest",
    )


def expected_closure(*, candidate_sha: str, freeze_blob_sha: str) -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_002_FINAL_CLOSURE_PACKET",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "frozen_candidate_sha": candidate_sha,
        "freeze_manifest_blob_sha": freeze_blob_sha,
        "open_blockers": [],
        "closure_status": "CLOSED_VERIFIED_FOR_AUTHORIZATION_REVIEW",
        "scientific_n_increment": 0,
        "collection_authorized": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "high_assurance_authorized": False,
    }


def validate_closure(data: dict, *, candidate_sha: str, freeze_blob_sha: str) -> None:
    require_exact_object(
        data,
        expected_closure(candidate_sha=candidate_sha, freeze_blob_sha=freeze_blob_sha),
        "closure packet",
    )


def expected_verification(*, candidate_sha: str, closure_blob_sha: str) -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_002_VERIFICATION_CLASSIFICATION",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "frozen_candidate_sha": candidate_sha,
        "closure_packet_blob_sha": closure_blob_sha,
        "verification_status": "PASS",
        "verification_class": "DEVELOPER_SELF_ATTESTED_NONINDEPENDENT",
        "independent_verification": False,
        "same_system_custody": True,
        "scientific_n_increment": 0,
        "collection_authorized": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "high_assurance_authorized": False,
    }


def validate_verification(data: dict, *, candidate_sha: str, closure_blob_sha: str) -> None:
    require_exact_object(
        data,
        expected_verification(candidate_sha=candidate_sha, closure_blob_sha=closure_blob_sha),
        "verification classification",
    )


def expected_authorization(
    *,
    authorization_parent_sha: str,
    candidate_sha: str,
    candidate_tree_sha: str,
    preflight_blob_sha: str,
    freeze_blob_sha: str,
    closure_blob_sha: str,
    verification_blob_sha: str,
    custody: dict[str, str],
) -> dict:
    return {
        "record_type": "TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "epoch_id": EPOCH_ID,
        "authorization_parent_sha": authorization_parent_sha,
        "frozen_candidate_sha": candidate_sha,
        "frozen_candidate_tree_sha": candidate_tree_sha,
        "preflight_blob_sha": preflight_blob_sha,
        "freeze_manifest_blob_sha": freeze_blob_sha,
        "closure_packet_blob_sha": closure_blob_sha,
        "verification_classification_blob_sha": verification_blob_sha,
        "preregistration_merge_sha": PREREG_MERGE_SHA,
        "analysis_lock_merge_sha": ANALYSIS_LOCK_MERGE_SHA,
        "analysis_blob_sha": ANALYSIS_BLOB_SHA,
        "analysis_config_sha256": ANALYSIS_CONFIG_SHA256,
        "requirements_lock_blob_sha": REQUIREMENTS_LOCK_BLOB_SHA,
        "algorithm_id": ALGORITHM_ID,
        "seed_start": SEEDS[0],
        "seed_end": SEEDS[-1],
        "seed_count": len(SEEDS),
        "expected_observations": EXPECTED_TOTAL,
        **custody,
        "custody_class": "SAME_SYSTEM_NONINDEPENDENT",
        "custody_recovery_drill": "PASS",
        "authorize_empirical_collection": True,
        "authorize_unblinding": False,
        "authorize_primary_analysis": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
        "high_assurance_authorized": False,
    }


def validate_collection_authorization(
    data: dict,
    *,
    authorization_parent_sha: str,
    candidate_sha: str,
    candidate_tree_sha: str,
    preflight_blob_sha: str,
    freeze_blob_sha: str,
    closure_blob_sha: str,
    verification_blob_sha: str,
    custody: dict[str, str],
) -> None:
    require_exact_object(
        data,
        expected_authorization(
            authorization_parent_sha=authorization_parent_sha,
            candidate_sha=candidate_sha,
            candidate_tree_sha=candidate_tree_sha,
            preflight_blob_sha=preflight_blob_sha,
            freeze_blob_sha=freeze_blob_sha,
            closure_blob_sha=closure_blob_sha,
            verification_blob_sha=verification_blob_sha,
            custody=custody,
        ),
        "authorization",
    )


def protected_source_blobs_at(revision: str) -> dict[str, str]:
    return {path: git_blob(path, revision=revision) for path in PROTECTED_SOURCE_PATHS}


def validate_authorization_commit_shape() -> tuple[str, str]:
    head = git_head()
    parents = git_parents(head)
    if len(parents) != 1:
        raise SystemExit("Track A collection prohibited: authorization HEAD must have exactly one parent")
    changed = git_changed_paths(head)
    if changed != (str(AUTH_PATH),):
        raise SystemExit(
            "Track A collection prohibited: authorization commit must introduce exactly "
            f"one file {AUTH_PATH}; changed={list(changed)}"
        )
    if git_path_exists_at(str(AUTH_PATH), parents[0]):
        raise SystemExit(
            "Track A collection prohibited: authorization file already existed before " "authorization HEAD"
        )
    auth_history = git_path_history(str(AUTH_PATH), head)
    if auth_history != (head,):
        raise SystemExit("Track A collection prohibited: authorization file must be introduced exactly " "at HEAD")
    return head, parents[0]


def validate_matrix_records(records: Sequence[dict], *, seed: int) -> None:
    if seed not in SEEDS:
        raise SystemExit("Track A collection prohibited: seed outside preregistered panel")
    if len(records) != EXPECTED_CELLS_PER_SEED:
        raise SystemExit("Track A collection prohibited: seed matrix size mismatch")
    cells: set[tuple[str, int]] = set()
    for record in records:
        if not isinstance(record, dict):
            raise SystemExit("Track A collection prohibited: public record must be object")
        if set(record) != PUBLIC_RECORD_KEYS:
            raise SystemExit("Track A collection prohibited: public record schema mismatch")
        if PROHIBITED_PUBLIC_KEYS & set(record):
            raise SystemExit("Track A collection prohibited: prohibited public topology/treatment field")
        blinded = record["blinded_topology_id"]
        failure = record["failure_count"]
        endpoint = record["ffcr_success"]
        if not isinstance(blinded, str) or not blinded.startswith("topology_"):
            raise SystemExit("Track A collection prohibited: malformed blinded topology id")
        if type(failure) is not int or failure not in FAILURE_COUNTS:
            raise SystemExit("Track A collection prohibited: failure-count panel drift")
        if type(endpoint) is not bool:
            raise SystemExit("Track A collection prohibited: ffcr_success must be strict boolean")
        if record["seed_id"] != seed:
            raise SystemExit("Track A collection prohibited: seed id mismatch")
        if record["protocol_id"] != PROTOCOL_ID or record["algorithm_id"] != ALGORITHM_ID:
            raise SystemExit("Track A collection prohibited: public identity mismatch")
        if record["excluded"] is not False:
            raise SystemExit("Track A collection prohibited: unregistered exclusion")
        cell = (blinded, failure)
        if cell in cells:
            raise SystemExit("Track A collection prohibited: duplicate matrix cell")
        cells.add(cell)
    blinded_ids = {cell[0] for cell in cells}
    if len(blinded_ids) != len(TOPOLOGIES):
        raise SystemExit("Track A collection prohibited: missing/extra blinded topology")
    expected_failures = set(FAILURE_COUNTS)
    for blinded in blinded_ids:
        if {failure for topology, failure in cells if topology == blinded} != expected_failures:
            raise SystemExit("Track A collection prohibited: missing/extra failure cell")


def strict_consensus_success(result: object) -> bool:
    value = getattr(result, "consensus_success", None)
    if type(value) is not bool:
        raise SystemExit("Track A collection prohibited: ConsensusTrialResult.consensus_success must be bool")
    return value


def blind_topology(topology: str, key: bytes) -> str:
    digest = hmac.new(key, b"label:" + topology.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"topology_{digest[:20]}"


def ordered_matrix_cells(seed: int, key: bytes) -> tuple[tuple[str, int], ...]:
    if seed not in SEEDS:
        raise ValueError("seed is outside the preregistered panel")
    cells = [(topology, failure_count) for topology in TOPOLOGIES for failure_count in FAILURE_COUNTS]

    def rank(cell: tuple[str, int]) -> bytes:
        topology, failure = cell
        message = f"order:{seed}:{topology}:{failure}".encode("utf-8")
        return hmac.new(key, message, hashlib.sha256).digest()

    return tuple(sorted(cells, key=rank))


def matrix_cells(seed: int) -> Iterable[tuple[str, int]]:
    """Canonical matrix membership only; collection uses secret-keyed ordering."""
    if seed not in SEEDS:
        raise ValueError("seed is outside the preregistered panel")
    return ((topology, failure) for topology in TOPOLOGIES for failure in FAILURE_COUNTS)


def environment_fingerprint() -> dict[str, object]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "requirements_lock_blob_sha": REQUIREMENTS_LOCK_BLOB_SHA,
        "task_engine_blob_sha": TASK_ENGINE_BLOB_SHA,
        "harness_contract_blob_sha": HARNESS_BLOB_SHA,
        "topology_utils_blob_sha": TOPOLOGY_UTILS_BLOB_SHA,
        "analysis_lock_blob_sha": ANALYSIS_LOCK_BLOB_SHA,
        "analysis_blob_sha": ANALYSIS_BLOB_SHA,
        "analysis_config_sha256": ANALYSIS_CONFIG_SHA256,
        "custody_receipt_validator_blob_sha": CUSTODY_VALIDATOR_BLOB_SHA,
    }


def write_json_with_sidecar(path: Path, value: object) -> str:
    payload = canonical_json_bytes(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    path.with_suffix(path.suffix + ".sha256").write_text(f"{digest}  {path.name}\n", encoding="utf-8")
    return digest


def require_collection_authorization() -> tuple[str, bytes, Path, Path, dict[str, str]]:
    if os.getenv("PDMAL_MODE") != MODE:
        raise SystemExit(f"Track A collection prohibited: PDMAL_MODE={MODE} required")
    if os.getenv("PDMAL_PROTOCOL_FROZEN") != "1":
        raise SystemExit("Track A collection prohibited: PDMAL_PROTOCOL_FROZEN=1 required")
    if os.getenv("PDMAL_TRACK_A_EPOCH_002_AUTHORIZED") != "1":
        raise SystemExit("Track A collection prohibited: explicit Epoch 002 authorization env required")
    if os.getenv("PDMAL_UNBLINDING_AUTHORIZED") == "1":
        raise SystemExit("Track A collection prohibited: unblinding must remain unauthorized")
    if os.getenv("PDMAL_PRIMARY_ANALYSIS_AUTHORIZED") == "1":
        raise SystemExit("Track A collection prohibited: primary analysis must remain separately unauthorized")
    if os.getenv("PDMAL_PILOT_AUTHORIZED") == "1":
        raise SystemExit("Track A collection prohibited: High-Assurance authorization must not be asserted")
    if os.getenv("PDMAL_HISTORICAL_POOLING") == "1" or os.getenv("PDMAL_EPOCH_004_SUBSTITUTION") == "1":
        raise SystemExit("Track A collection prohibited: historical pooling/Epoch-004 substitution forbidden")

    secret = os.getenv("PDMAL_TOPOLOGY_BLINDING_KEY")
    public_dir = os.getenv("PDMAL_TRACK_A_PUBLIC_OUTPUT_DIR")
    protected_dir = os.getenv("PDMAL_TRACK_A_PROTECTED_OUTPUT_DIR")
    if not secret or len(secret.encode()) < 32:
        raise SystemExit("Track A collection prohibited: fresh topology blinding secret required")
    if not public_dir or not protected_dir or Path(public_dir).resolve() == Path(protected_dir).resolve():
        raise SystemExit("Track A collection prohibited: distinct public/protected retention roots required")

    require_source_bindings()
    _, authorization_parent = validate_authorization_commit_shape()

    custody_receipt = load_json_object(CUSTODY_RECEIPT_PATH, "custody recovery receipt")
    custody = validate_custody_artifacts(custody_receipt)
    preflight = load_json_object(PREFLIGHT_PATH, "preflight")
    freeze = load_json_object(FREEZE_PATH, "freeze manifest")
    closure = load_json_object(CLOSURE_PATH, "closure packet")
    verification = load_json_object(VERIFICATION_PATH, "verification classification")
    authorization = load_json_object(AUTH_PATH, "authorization")

    candidate_sha = freeze.get("frozen_candidate_sha")
    candidate_tree = freeze.get("frozen_candidate_tree_sha")
    if not isinstance(candidate_sha, str) or len(candidate_sha) != 40:
        raise SystemExit("Track A collection prohibited: malformed frozen candidate sha")
    if not isinstance(candidate_tree, str) or len(candidate_tree) != 40:
        raise SystemExit("Track A collection prohibited: malformed frozen candidate tree sha")
    if not git_is_ancestor(candidate_sha, authorization_parent):
        raise SystemExit("Track A collection prohibited: frozen candidate is not ancestor of authorization parent")
    if git_tree(candidate_sha) != candidate_tree:
        raise SystemExit("Track A collection prohibited: frozen candidate tree mismatch")

    require_custody_history(candidate_sha, authorization_parent)
    require_immutable_gate_history(candidate_sha, authorization_parent)

    preflight_blob = git_blob(str(PREFLIGHT_PATH))
    freeze_blob = git_blob(str(FREEZE_PATH))
    closure_blob = git_blob(str(CLOSURE_PATH))
    verification_blob = git_blob(str(VERIFICATION_PATH))
    frozen_sources = protected_source_blobs_at(candidate_sha)

    validate_preflight(
        preflight,
        candidate_sha=candidate_sha,
        candidate_tree_sha=candidate_tree,
        custody=custody,
    )
    validate_freeze(
        freeze,
        candidate_sha=candidate_sha,
        candidate_tree_sha=candidate_tree,
        preflight_blob_sha=preflight_blob,
        protected_source_blobs=frozen_sources,
    )
    validate_closure(closure, candidate_sha=candidate_sha, freeze_blob_sha=freeze_blob)
    validate_verification(verification, candidate_sha=candidate_sha, closure_blob_sha=closure_blob)
    validate_collection_authorization(
        authorization,
        authorization_parent_sha=authorization_parent,
        candidate_sha=candidate_sha,
        candidate_tree_sha=candidate_tree,
        preflight_blob_sha=preflight_blob,
        freeze_blob_sha=freeze_blob,
        closure_blob_sha=closure_blob,
        verification_blob_sha=verification_blob,
        custody=custody,
    )

    current_sources = protected_source_blobs_at("HEAD")
    if current_sources != frozen_sources:
        raise SystemExit("Track A collection prohibited: protected source drift after freeze")

    public_root, protected_root = Path(public_dir), Path(protected_dir)
    return candidate_sha, secret.encode(), public_root, protected_root, custody


def collect_seed(seed: int, *, frozen_sha: str, key: bytes, custody: dict[str, str]) -> tuple[dict, dict, dict]:
    started = monotonic()
    public_records: list[dict[str, object]] = []
    mapping = {blind_topology(topology, key): topology for topology in TOPOLOGIES}
    for topology, failure_count in ordered_matrix_cells(seed, key):
        task = ConsensusTask(topology=topology, failure_count=failure_count, condition=CONDITION)
        result = task.run_detailed(seed=seed, attempt=1)
        if result.attempt_status is not AttemptStatus.SUCCESS:
            raise SystemExit(
                "Track A collection prohibited: trial failed "
                f"seed={seed} topology={topology} failure_count={failure_count}"
            )
        public_records.append(
            {
                "protocol_id": PROTOCOL_ID,
                "algorithm_id": ALGORITHM_ID,
                "frozen_candidate_sha": frozen_sha,
                "seed_id": seed,
                "blinded_topology_id": blind_topology(topology, key),
                "failure_count": failure_count,
                "ffcr_success": strict_consensus_success(result),
                "excluded": False,
            }
        )

    validate_matrix_records(public_records, seed=seed)
    elapsed = monotonic() - started
    if elapsed > SEED_RUNTIME_CEILING_SECONDS:
        raise SystemExit(f"Track A collection prohibited: seed {seed} exceeded runtime ceiling")

    public_doc = {
        "record_type": "TRACK_A_EPOCH_002_BLINDED_SEED_DATASET",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "seed_id": seed,
        "records": public_records,
        "environment_fingerprint": environment_fingerprint(),
        "runtime_seconds": elapsed,
        "outcomes_inspected_by_collection_workflow": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
    }
    protected_mapping_doc = {
        "record_type": "TRACK_A_EPOCH_002_PROTECTED_TOPOLOGY_MAPPING",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "seed_id": seed,
        "mapping": mapping,
        "custody": "PROTECTED_SAME_SYSTEM_NONINDEPENDENT",
        "custody_certificate_public_key_der_sha256": custody["custody_certificate_public_key_der_sha256"],
        "public_dataset_contains_plaintext_topology": False,
        "public_dataset_contains_topology_fingerprint": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
    }
    protected_key_custody_doc = {
        "record_type": "TRACK_A_EPOCH_002_PROTECTED_BLINDING_KEY_CUSTODY",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "key_material_persisted": False,
        "key_fingerprint_sha256": hashlib.sha256(key).hexdigest(),
        "custody": "SAME_SYSTEM_NONINDEPENDENT",
        "independent_custody": False,
        "custody_certificate_public_key_der_sha256": custody["custody_certificate_public_key_der_sha256"],
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
    }
    return public_doc, protected_mapping_doc, protected_key_custody_doc


def run_epoch() -> int:
    frozen_sha, key, public_root, protected_root, custody = require_collection_authorization()
    key_custody_written = False
    manifest_rows: list[dict[str, object]] = []
    total_records = 0
    for seed in SEEDS:
        public_doc, mapping_doc, key_doc = collect_seed(seed, frozen_sha=frozen_sha, key=key, custody=custody)
        public_path = public_root / f"track_a_epoch_002_seed_{seed}.json"
        mapping_path = protected_root / f"track_a_epoch_002_mapping_{seed}.json"
        public_digest = write_json_with_sidecar(public_path, public_doc)
        mapping_digest = write_json_with_sidecar(mapping_path, mapping_doc)
        if not key_custody_written:
            write_json_with_sidecar(protected_root / "track_a_epoch_002_blinding_key_custody.json", key_doc)
            key_custody_written = True
        record_count = len(public_doc["records"])
        manifest_rows.append(
            {
                "seed_id": seed,
                "public_dataset_sha256": public_digest,
                "protected_mapping_sha256": mapping_digest,
                "record_count": record_count,
            }
        )
        total_records += record_count
    if total_records != EXPECTED_TOTAL:
        raise SystemExit("Track A collection prohibited: whole-epoch matrix incomplete")
    manifest = {
        "record_type": "TRACK_A_EPOCH_002_BLINDED_COLLECTION_MANIFEST",
        "schema_version": 1,
        "protocol_id": PROTOCOL_ID,
        "frozen_candidate_sha": frozen_sha,
        "seed_count": len(SEEDS),
        "expected_observations": EXPECTED_TOTAL,
        "custody_receipt_blob_sha": custody["custody_receipt_blob_sha"],
        "custody_certificate_sha256": custody["custody_certificate_sha256"],
        "custody_certificate_public_key_der_sha256": custody["custody_certificate_public_key_der_sha256"],
        "rows": manifest_rows,
        "outcomes_inspected_by_collection_workflow": False,
        "outcome_aggregation_performed": False,
        "unblinding_authorized": False,
        "primary_analysis_authorized": False,
        "historical_pooling_allowed": False,
        "epoch_004_substitution_allowed": False,
    }
    write_json_with_sidecar(public_root / "track_a_epoch_002_manifest.json", manifest)
    print("TRACK_A_EPOCH_002_COLLECTION_COMPLETE: " f"{len(SEEDS)} seeds; {EXPECTED_TOTAL} observations")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="execute only after every authorization predicate passes",
    )
    args = parser.parse_args(argv)
    if not args.execute:
        raise SystemExit("Track A collection prohibited: --execute is required after authorization")
    return run_epoch()


if __name__ == "__main__":
    raise SystemExit(main())
