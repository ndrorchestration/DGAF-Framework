"""Synthetic integrated lifecycle primitives for the DGAF Mode-T admission proof.

This module connects the reviewed Mode-T record ordering without executing the real
pilot: reservation R -> authorization A -> single-use consumption C -> PRE_EXECUTION
admission -> in-process key capability -> blinded synthetic artifact/output manifest
-> POST_EXECUTION admission -> two-phase lineage evidence.

The in-memory ledger supports snapshot/rehydration so tests can model crashes after C
and prove that retries remain consumed. It is *not* an independently retained P6 or
transparency implementation and therefore cannot establish real authorization or P4.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Iterable, Mapping

from mode_t_confidential_space_attestation import verify_two_phase_attestation_binding
from mode_t_inprocess_key import ModeTKeyLease

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
_IMAGE_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class ModeTLifecycleError(RuntimeError):
    """Raised when lifecycle ordering, binding, or single-use rules fail closed."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ModeTLifecycleError(message)


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _sha(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None,
        f"{label} must be lowercase SHA-256 hex",
    )
    return value


def _commit(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and _COMMIT_RE.fullmatch(value) is not None,
        f"{label} must be a full lowercase 40-character commit SHA",
    )
    return value


def _integer(value: Any, label: str) -> int:
    _require(
        isinstance(value, int) and not isinstance(value, bool),
        f"{label} must be an integer",
    )
    return value


def canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    """Canonical bytes used only for this synthetic lifecycle evidence contract."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def canonical_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _seal(record: Mapping[str, Any], digest_field: str) -> dict[str, Any]:
    _require(digest_field not in record, f"{digest_field} must not be pre-populated")
    sealed = dict(record)
    sealed[digest_field] = canonical_sha256(dict(record))
    return sealed


def _verify_seal(record: Mapping[str, Any], digest_field: str) -> str:
    data = dict(_mapping(record, "record"))
    claimed = _sha(data.pop(digest_field, None), digest_field)
    _require(canonical_sha256(data) == claimed, f"{digest_field} does not match record")
    return claimed


def make_synthetic_reservation(
    *,
    freeze_commit_sha: str,
    freeze_sha256: str,
    workflow_sha256: str,
    github_run_id: int,
    github_sha: str,
) -> dict[str, Any]:
    """Create a sealed synthetic R record; no real reservation is granted."""
    _commit(freeze_commit_sha, "freeze_commit_sha")
    _sha(freeze_sha256, "freeze_sha256")
    _sha(workflow_sha256, "workflow_sha256")
    _commit(github_sha, "github_sha")
    _require(github_run_id > 0, "github_run_id must be positive")
    return _seal(
        {
            "record_type": "PDMAL_MODE_T_RUN_RESERVATION",
            "freeze_commit_sha": freeze_commit_sha,
            "freeze_sha256": freeze_sha256,
            "workflow_sha256": workflow_sha256,
            "github_run_id": github_run_id,
            "github_run_attempt": 1,
            "github_sha": github_sha,
            "synthetic_only": True,
            "empirical_n": 0,
        },
        "reservation_evidence_sha256",
    )


def make_synthetic_authorization(
    reservation: Mapping[str, Any],
    *,
    authorization_id: str,
) -> dict[str, Any]:
    """Create a sealed synthetic A fixture bound to one R; never real authorization."""
    reservation_sha = _verify_seal(reservation, "reservation_evidence_sha256")
    r = _mapping(reservation, "reservation")
    _require(
        isinstance(authorization_id, str) and bool(authorization_id),
        "authorization_id must be non-empty",
    )
    return _seal(
        {
            "record_type": "PDMAL_PILOT_AUTHORIZATION_SYNTHETIC_FIXTURE",
            "status": "SYNTHETIC_GRANTED_FOR_TEST_ONLY",
            "freeze_commit_sha": _commit(r.get("freeze_commit_sha"), "freeze_commit_sha"),
            "freeze_sha256": _sha(r.get("freeze_sha256"), "freeze_sha256"),
            "reservation_evidence_sha256": reservation_sha,
            "github_run_id": _integer(r.get("github_run_id"), "github_run_id"),
            "allowed_run_attempt": 1,
            "authorization_id": authorization_id,
            "synthetic_only": True,
            "empirical_n": 0,
        },
        "authorization_record_sha256",
    )


class SyntheticAuthorizationConsumptionLedger:
    """Crash-rehydratable single-use C model; not a durable external evidence store."""

    def __init__(self, snapshot: Mapping[str, str] | None = None) -> None:
        self._consumed: dict[str, str] = {}
        if snapshot is not None:
            for authorization_id, consumption_sha in snapshot.items():
                _require(
                    isinstance(authorization_id, str) and bool(authorization_id),
                    "snapshot authorization id must be non-empty",
                )
                self._consumed[authorization_id] = _sha(
                    consumption_sha,
                    "snapshot consumption SHA",
                )

    def snapshot(self) -> dict[str, str]:
        """Return the accepted-consumption index for simulated process rehydration."""
        return dict(self._consumed)

    def consume(
        self,
        reservation: Mapping[str, Any],
        authorization: Mapping[str, Any],
    ) -> dict[str, Any]:
        reservation_sha = _verify_seal(reservation, "reservation_evidence_sha256")
        authorization_sha = _verify_seal(
            authorization,
            "authorization_record_sha256",
        )
        r = _mapping(reservation, "reservation")
        a = _mapping(authorization, "authorization")

        _require(r.get("record_type") == "PDMAL_MODE_T_RUN_RESERVATION", "wrong R type")
        _require(r.get("github_run_attempt") == 1, "R run attempt must be exactly 1")
        _require(r.get("synthetic_only") is True, "R must be an explicit synthetic fixture")
        _require(
            a.get("record_type") == "PDMAL_PILOT_AUTHORIZATION_SYNTHETIC_FIXTURE",
            "wrong A type",
        )
        _require(
            a.get("status") == "SYNTHETIC_GRANTED_FOR_TEST_ONLY",
            "A is not the explicit synthetic-grant fixture state",
        )
        _require(a.get("synthetic_only") is True, "A must be an explicit synthetic fixture")

        _require(a.get("freeze_commit_sha") == r.get("freeze_commit_sha"), "A/R freeze commit mismatch")
        _require(a.get("freeze_sha256") == r.get("freeze_sha256"), "A/R freeze digest mismatch")
        _require(
            a.get("reservation_evidence_sha256") == reservation_sha,
            "A does not bind exact R evidence",
        )
        _require(a.get("github_run_id") == r.get("github_run_id"), "A/R run-id mismatch")
        _require(a.get("allowed_run_attempt") == 1, "A allowed attempt must be exactly 1")

        authorization_id = a.get("authorization_id")
        _require(
            isinstance(authorization_id, str) and bool(authorization_id),
            "authorization_id must be non-empty",
        )
        _require(
            authorization_id not in self._consumed,
            "authorization already consumed; retry requires a new R/A/C lineage",
        )

        c = _seal(
            {
                "record_type": "PDMAL_MODE_T_AUTHORIZATION_CONSUMPTION",
                "status": "CONSUMED_PRE_SECRET_SYNTHETIC",
                "freeze_sha256": _sha(r.get("freeze_sha256"), "freeze_sha256"),
                "reservation_evidence_sha256": reservation_sha,
                "authorization_record_sha256": authorization_sha,
                "authorization_id": authorization_id,
                "github_run_id": _integer(r.get("github_run_id"), "github_run_id"),
                "github_run_attempt": 1,
                "secret_instantiation_status": "NOT_EXECUTED_AT_CONSUMPTION",
                "retention_status": "SYNTHETIC_MODEL_ONLY_NOT_INDEPENDENTLY_RETAINED",
                "synthetic_only": True,
                "empirical_n": 0,
            },
            "consumption_evidence_sha256",
        )
        c_sha = _sha(c["consumption_evidence_sha256"], "consumption_evidence_sha256")
        # Mark consumed before the caller is allowed to cross into any secret/key step.
        self._consumed[authorization_id] = c_sha
        return c


def build_synthetic_blinded_artifact(
    lease: ModeTKeyLease,
    clear_identifiers: Iterable[str],
) -> dict[str, Any]:
    """Build a synthetic blinded artifact containing no supplied clear identifiers."""
    identifiers = list(clear_identifiers)
    _require(bool(identifiers), "at least one synthetic identifier is required")
    _require(
        all(isinstance(item, str) and bool(item) for item in identifiers),
        "synthetic identifiers must be non-empty strings",
    )
    _require(len(set(identifiers)) == len(identifiers), "synthetic identifiers must be unique")

    records = []
    for index, clear_identifier in enumerate(identifiers):
        records.append(
            {
                "blinded_id": lease.blind_identifier(clear_identifier),
                "order_token": lease.order_token(index.to_bytes(8, "big")),
            }
        )
    artifact_core = {
        "artifact_type": "PDMAL_MODE_T_SYNTHETIC_BLINDED_OUTPUT",
        "records": records,
        "synthetic_only": True,
        "empirical_n": 0,
    }
    artifact = dict(artifact_core)
    artifact["artifact_sha256"] = canonical_sha256(artifact_core)
    encoded = canonical_json_bytes(artifact)
    for clear_identifier in identifiers:
        _require(
            clear_identifier.encode("utf-8") not in encoded,
            "clear identifier leaked into blinded artifact",
        )
    return artifact


def build_output_manifest(
    *,
    candidate_sha: str,
    freeze_sha256: str,
    consumption_sha256: str,
    runtime_identity_sha256: str,
    workload_image_digest: str,
    tlock_client_sha256: str,
    tlock_chain_hash: str,
    blinded_artifact_sha256: str,
    timelock_ciphertext_sha256: str,
    key_commitment_sha256: str,
    pre_execution_token_sha256: str,
    execution_started_unix: int,
    execution_completed_unix: int,
) -> dict[str, Any]:
    """Build the exact pre-POST manifest whose digest becomes POST nonce B."""
    _commit(candidate_sha, "candidate_sha")
    _sha(freeze_sha256, "freeze_sha256")
    _sha(consumption_sha256, "consumption_sha256")
    _sha(runtime_identity_sha256, "runtime_identity_sha256")
    _require(
        isinstance(workload_image_digest, str)
        and _IMAGE_RE.fullmatch(workload_image_digest) is not None,
        "workload_image_digest must be sha256:<hex>",
    )
    for label, value in (
        ("tlock_client_sha256", tlock_client_sha256),
        ("tlock_chain_hash", tlock_chain_hash),
        ("blinded_artifact_sha256", blinded_artifact_sha256),
        ("timelock_ciphertext_sha256", timelock_ciphertext_sha256),
        ("key_commitment_sha256", key_commitment_sha256),
        ("pre_execution_token_sha256", pre_execution_token_sha256),
    ):
        _sha(value, label)
    start = _integer(execution_started_unix, "execution_started_unix")
    end = _integer(execution_completed_unix, "execution_completed_unix")
    _require(end >= start, "execution completion predates start")

    manifest = {
        "record_type": "PDMAL_MODE_T_OUTPUT_MANIFEST_SYNTHETIC",
        "candidate_sha": candidate_sha,
        "freeze_sha256": freeze_sha256,
        "authorization_consumption_sha256": consumption_sha256,
        "runtime_identity_sha256": runtime_identity_sha256,
        "workload_image_digest": workload_image_digest,
        "tlock_client_sha256": tlock_client_sha256,
        "tlock_chain_hash": tlock_chain_hash,
        "blinded_artifact_sha256": blinded_artifact_sha256,
        "timelock_ciphertext_sha256": timelock_ciphertext_sha256,
        "key_commitment_sha256": key_commitment_sha256,
        "pre_execution_token_sha256": pre_execution_token_sha256,
        "execution_started_unix": start,
        "execution_completed_unix": end,
        "synthetic_only": True,
        "empirical_n": 0,
    }
    return {
        "manifest": manifest,
        "manifest_sha256": canonical_sha256(manifest),
    }


def finalize_two_phase_lifecycle(
    pre_execution: Mapping[str, Any],
    post_execution: Mapping[str, Any],
    output_manifest: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind PRE, output manifest, and POST into one retention-safe synthetic record."""
    bundle = _mapping(output_manifest, "output_manifest")
    manifest = _mapping(bundle.get("manifest"), "output_manifest.manifest")
    manifest_sha = _sha(bundle.get("manifest_sha256"), "manifest_sha256")
    _require(
        canonical_sha256(dict(manifest)) == manifest_sha,
        "output manifest digest mismatch",
    )
    consumption_sha = _sha(
        manifest.get("authorization_consumption_sha256"),
        "authorization_consumption_sha256",
    )
    pair = verify_two_phase_attestation_binding(
        pre_execution,
        post_execution,
        authorization_consumption_sha256=consumption_sha,
        output_manifest_sha256=manifest_sha,
    )
    _require(
        pair.get("runtime_identity_sha256") == manifest.get("runtime_identity_sha256"),
        "two-phase runtime identity does not match output manifest",
    )
    _require(
        pair.get("pre_execution_token_sha256") == manifest.get("pre_execution_token_sha256"),
        "PRE token digest does not match output manifest",
    )
    return {
        "integrated_lifecycle": "PASS_SYNTHETIC_ONLY",
        "authorization_consumption_sha256": consumption_sha,
        "output_manifest_sha256": manifest_sha,
        "runtime_identity_sha256": pair["runtime_identity_sha256"],
        "pre_execution_token_sha256": pair["pre_execution_token_sha256"],
        "post_execution_token_sha256": pair["post_execution_token_sha256"],
        "real_confidential_space_admission": False,
        "independent_retention_verified": False,
        "freeze_established": False,
        "pilot_authorized": False,
        "empirical_data_collection": False,
        "empirical_n": 0,
    }
