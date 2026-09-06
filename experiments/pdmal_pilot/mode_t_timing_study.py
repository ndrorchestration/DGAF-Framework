#!/usr/bin/env python3
"""Synthetic-only Mode-T timing characterization for Issue #293.

This module measures operational durations for the exact PDMAL pilot matrix shape,
locked primary-analysis shape, and separately produced synthetic tlock encryption
measurements without invoking pilot mode, creating a real blinding secret,
authorizing empirical work, or retaining synthetic outcomes as scientific
evidence.

The emitted artifact is deliberately ineligible to propose an analysis-lock
window until every required end-to-end stage is measured and independently
reviewed. External transparency and artifact-publication timing remain separate
required stages.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from time import monotonic
from typing import Iterable

import numpy as np

from analysis import (
    BOOTSTRAP_RESAMPLES,
    BOOTSTRAP_SEED,
    CONDITIONS as ANALYSIS_CONDITIONS,
    FAILURE_COUNTS as ANALYSIS_FAILURE_COUNTS,
    TOPOLOGIES as ANALYSIS_TOPOLOGIES,
    paired_bootstrap_ci,
    seed_effect_from_artifact,
)
from harness_contract import TOPOLOGY_SPECS
from run_pilot import FAILURE_COUNTS as PILOT_FAILURE_COUNTS
from task_engine import CONDITION_VALUES, ConsensusTask

EVIDENCE_CLASS = "P4_MODE_T_SYNTHETIC_TIMING_PARTIAL_V1"
TLOCK_ENCRYPTION_EVIDENCE_CLASS = "P4_MODE_T_SYNTHETIC_ENCRYPTION_TIMING_V1"
DEFAULT_REPETITIONS = 3
DEFAULT_MATRIX_SEED_BASE = 2026090500
SYNTHETIC_ANALYSIS_SEED_COUNT = 50
MIN_TLOCK_ENCRYPTION_SAMPLES = 3
MAX_TLOCK_ENCRYPTION_SAMPLES = 20
EXPECTED_TLOCK_SHA256 = "0fda1e0fedffab82217cbd90e0b8b2a9d42df88a361b2dd890d8fac173b5dc57"
EXPECTED_DRAND_ENDPOINT = "https://api.drand.sh/"
EXPECTED_QUICKNET_CHAIN_HASH = "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971"
EXPECTED_QUICKNET_SCHEME = "bls-unchained-g1-rfc9380"
EXPECTED_QUICKNET_PUBLIC_KEY = (
    "83cf0f2896adee7eb8b5f01fcad3912212c437e0073e911fb90022d3e760183c"
    "8c4b450b6a0a6c3ac6a5776a2d1064510d1fec758c921cc22b0e17e63aaf4bc"
    "b5ed66304de9cf809bd274ca73bab4af5a6e9c76a4bc09e76eae8991ef5ece45a"
)

REQUIRED_STAGE_NAMES = (
    "exact_tlock_asset_reverification",
    "full_synthetic_matrix_timing",
    "locked_primary_analysis_timing",
    "synthetic_timelock_encryption_timing",
    "external_transparency_retention_timing",
    "artifact_publication_retention_timing",
)

BLIND_IDS = {
    "null": "blind_timing_fixture_0",
    "simple": "blind_timing_fixture_1",
    "static": "blind_timing_fixture_2",
    "dgaf": "blind_timing_fixture_3",
}
CONDITION_MAP = {blind: condition for condition, blind in BLIND_IDS.items()}


def _validate_canonical_shapes() -> None:
    if set(TOPOLOGY_SPECS) != set(ANALYSIS_TOPOLOGIES):
        raise RuntimeError("pilot topology set differs from locked analysis topology set")
    if set(CONDITION_VALUES) != set(ANALYSIS_CONDITIONS):
        raise RuntimeError("pilot condition set differs from locked analysis condition set")
    if tuple(PILOT_FAILURE_COUNTS) != tuple(ANALYSIS_FAILURE_COUNTS):
        raise RuntimeError("pilot failure-count set differs from locked analysis failure-count set")


def expected_trials_per_seed() -> int:
    _validate_canonical_shapes()
    return len(TOPOLOGY_SPECS) * len(CONDITION_VALUES) * len(PILOT_FAILURE_COUNTS)


def _timing_stats(values_ms: Iterable[float]) -> dict[str, float | int]:
    values = np.asarray(tuple(values_ms), dtype=float)
    if values.size < 1 or not np.all(np.isfinite(values)) or np.any(values < 0):
        raise ValueError("timing samples must be non-empty finite non-negative values")
    return {
        "sample_count": int(values.size),
        "min_ms": round(float(np.min(values)), 3),
        "p50_ms": round(float(np.quantile(values, 0.50)), 3),
        "p95_ms": round(float(np.quantile(values, 0.95)), 3),
        "max_ms": round(float(np.max(values)), 3),
        "mean_ms": round(float(np.mean(values)), 3),
    }


def measure_full_synthetic_matrix(seed: int) -> float:
    """Time one exact 180-cell pilot-shape matrix using deterministic tasks.

    A returned ``ConsensusTrialResult`` counts as an executed matrix cell even
    when its scientific attempt classification is FAILURE. This mirrors
    ``run_pilot``: fail-closed/unrecovered trial classifications are recorded as
    outcomes and do not abort the seed. Exceptions still propagate and fail this
    timing study because they are execution-path failures, not trial outcomes.

    Scientific result values and classifications are deliberately neither
    serialized nor returned from this timing harness.
    """
    _validate_canonical_shapes()
    started = monotonic()
    completed = 0
    for topology in TOPOLOGY_SPECS:
        for condition in CONDITION_VALUES:
            for failure_count in PILOT_FAILURE_COUNTS:
                ConsensusTask(
                    topology=topology,
                    failure_count=failure_count,
                    condition=condition,
                ).run_detailed(seed=seed, attempt=1)
                completed += 1
    if completed != expected_trials_per_seed():
        raise RuntimeError("synthetic matrix timing did not execute the complete pilot shape")
    return (monotonic() - started) * 1000.0


def build_synthetic_analysis_documents(seed_count: int = SYNTHETIC_ANALYSIS_SEED_COUNT) -> list[dict]:
    """Build complete deterministic fixtures for timing locked analysis only."""
    _validate_canonical_shapes()
    if not isinstance(seed_count, int) or isinstance(seed_count, bool) or seed_count < 1:
        raise ValueError("seed_count must be a positive integer")

    documents: list[dict] = []
    topology_index = {name: index for index, name in enumerate(ANALYSIS_TOPOLOGIES)}
    condition_index = {name: index for index, name in enumerate(ANALYSIS_CONDITIONS)}
    for offset in range(seed_count):
        seed = 20270000 + offset
        records: list[dict] = []
        for condition in ANALYSIS_CONDITIONS:
            for topology in ANALYSIS_TOPOLOGIES:
                for failure_count in ANALYSIS_FAILURE_COUNTS:
                    fixture_success = (
                        seed
                        + condition_index[condition]
                        + topology_index[topology]
                        + failure_count
                    ) % 3 != 0
                    records.append(
                        {
                            "blinded_condition_id": BLIND_IDS[condition],
                            "topology": topology,
                            "failure_count": failure_count,
                            "ffcr_success": fixture_success,
                        }
                    )
        documents.append({"seed_id": seed, "records": records})
    return documents


def measure_locked_primary_analysis() -> float:
    """Time the locked 50-seed paired analysis without retaining its result."""
    documents = build_synthetic_analysis_documents()
    started = monotonic()
    effects = [
        seed_effect_from_artifact(document, condition_map=CONDITION_MAP)
        for document in documents
    ]
    low, high = paired_bootstrap_ci(
        effects,
        resamples=BOOTSTRAP_RESAMPLES,
        seed=BOOTSTRAP_SEED,
    )
    if not (math.isfinite(low) and math.isfinite(high) and low <= high):
        raise RuntimeError("locked primary analysis produced an invalid synthetic timing fixture result")
    return (monotonic() - started) * 1000.0


def _tlock_reverification_stage(*, require_tlock_verification: bool) -> dict[str, object]:
    verified = os.environ.get("P4_MODE_T_TLOCK_SHA256_VERIFIED") == "1"
    digest = os.environ.get("P4_MODE_T_TLOCK_SHA256", "").strip().lower()
    valid = verified and digest == EXPECTED_TLOCK_SHA256
    if require_tlock_verification and not valid:
        raise RuntimeError("exact tlock release asset was not reverified at the frozen SHA-256")
    return {
        "status": "PASS" if valid else "NOT_EXECUTED",
        "asset_name": "tlock_1.2.0_linux_amd64.tar.gz",
        "sha256": EXPECTED_TLOCK_SHA256 if valid else None,
        "timing_included_in_end_to_end": False,
    }


def _require_full_sha(value: object, *, field: str) -> str:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise ValueError(f"{field} must be a full lowercase 40-character git SHA")
    return value


def _load_tlock_encryption_stage(path: Path | None) -> dict[str, object]:
    """Validate separately produced synthetic tlock encryption timing evidence."""
    if path is None:
        return {
            "status": "NOT_EXECUTED",
            "reason": "requires separately reviewed synthetic encryption path",
        }
    try:
        evidence = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("invalid synthetic tlock encryption timing evidence") from exc
    if not isinstance(evidence, dict):
        raise ValueError("synthetic tlock encryption timing evidence must be a JSON object")
    if evidence.get("schema_version") != 1:
        raise ValueError("synthetic tlock encryption timing schema_version mismatch")
    if evidence.get("evidence_class") != TLOCK_ENCRYPTION_EVIDENCE_CLASS:
        raise ValueError("synthetic tlock encryption timing evidence_class mismatch")

    evidence_sha = _require_full_sha(evidence.get("control_plane_sha"), field="control_plane_sha")
    expected_sha = os.environ.get("EVIDENCE_SHA", "").strip().lower()
    if expected_sha:
        _require_full_sha(expected_sha, field="EVIDENCE_SHA")
        if not hashlib.sha256(evidence_sha.encode()).digest() == hashlib.sha256(expected_sha.encode()).digest():
            raise ValueError("synthetic tlock encryption evidence head mismatch")

    if evidence.get("tlock_sha256") != EXPECTED_TLOCK_SHA256:
        raise ValueError("synthetic tlock encryption evidence tlock digest mismatch")
    if evidence.get("network_endpoint") != EXPECTED_DRAND_ENDPOINT:
        raise ValueError("synthetic tlock encryption evidence endpoint mismatch")
    if evidence.get("chain_hash") != EXPECTED_QUICKNET_CHAIN_HASH:
        raise ValueError("synthetic tlock encryption evidence chain hash mismatch")
    if evidence.get("scheme") != EXPECTED_QUICKNET_SCHEME:
        raise ValueError("synthetic tlock encryption evidence scheme mismatch")
    if evidence.get("public_key") != EXPECTED_QUICKNET_PUBLIC_KEY:
        raise ValueError("synthetic tlock encryption evidence public key mismatch")
    if evidence.get("network_metadata_verified") is not True:
        raise ValueError("synthetic tlock encryption evidence lacks verified network metadata")

    current_round = evidence.get("metadata_current_round")
    target_round = evidence.get("target_round")
    if (
        not isinstance(current_round, int)
        or isinstance(current_round, bool)
        or current_round < 1
        or not isinstance(target_round, int)
        or isinstance(target_round, bool)
        or target_round <= current_round
    ):
        raise ValueError("synthetic tlock encryption evidence has invalid round binding")

    samples = evidence.get("samples_ms")
    if not isinstance(samples, list) or not MIN_TLOCK_ENCRYPTION_SAMPLES <= len(samples) <= MAX_TLOCK_ENCRYPTION_SAMPLES:
        raise ValueError("synthetic tlock encryption timing sample count is outside the accepted range")
    stats = _timing_stats(samples)
    if evidence.get("sample_count") != stats["sample_count"]:
        raise ValueError("synthetic tlock encryption evidence sample_count mismatch")

    payload_bytes = evidence.get("payload_bytes")
    if not isinstance(payload_bytes, int) or isinstance(payload_bytes, bool) or payload_bytes < 1:
        raise ValueError("synthetic tlock encryption evidence payload_bytes must be positive")
    if evidence.get("payload_class") != "P4_MODE_T_SYNTHETIC_TIMING_NOT_AUTHORIZATION":
        raise ValueError("synthetic tlock encryption evidence payload class mismatch")
    if evidence.get("all_encryptions_succeeded") is not True:
        raise ValueError("synthetic tlock encryption evidence does not prove all samples succeeded")
    if evidence.get("ciphertexts_retained") is not False:
        raise ValueError("synthetic tlock encryption evidence must not retain ciphertext fixtures")
    if evidence.get("empirical_data_collection") is not False:
        raise ValueError("synthetic tlock encryption evidence must be non-empirical")
    if evidence.get("secret_instantiation") is not False:
        raise ValueError("synthetic tlock encryption evidence must not instantiate a protected secret")
    if evidence.get("pilot_authorized") is not False:
        raise ValueError("synthetic tlock encryption evidence must not assert pilot authorization")

    return {
        "status": "PASS",
        "evidence_class": TLOCK_ENCRYPTION_EVIDENCE_CLASS,
        "network_endpoint": EXPECTED_DRAND_ENDPOINT,
        "chain_hash": EXPECTED_QUICKNET_CHAIN_HASH,
        "scheme": EXPECTED_QUICKNET_SCHEME,
        "target_round": target_round,
        "payload_bytes": payload_bytes,
        "statistics": stats,
        "ciphertexts_retained": False,
    }


def run_study(
    *,
    output_path: Path,
    repetitions: int = DEFAULT_REPETITIONS,
    require_tlock_verification: bool = False,
    tlock_encryption_evidence: Path | None = None,
) -> dict:
    if not isinstance(repetitions, int) or isinstance(repetitions, bool) or not 1 <= repetitions <= 20:
        raise ValueError("repetitions must be an integer between 1 and 20")
    _validate_canonical_shapes()

    matrix_samples: list[float] = []
    analysis_samples: list[float] = []
    for index in range(repetitions):
        matrix_samples.append(measure_full_synthetic_matrix(DEFAULT_MATRIX_SEED_BASE + index))
        analysis_samples.append(measure_locked_primary_analysis())

    stages: dict[str, dict[str, object]] = {
        "exact_tlock_asset_reverification": _tlock_reverification_stage(
            require_tlock_verification=require_tlock_verification
        ),
        "full_synthetic_matrix_timing": {
            "status": "PASS",
            "trials_per_repetition": expected_trials_per_seed(),
            "statistics": _timing_stats(matrix_samples),
        },
        "locked_primary_analysis_timing": {
            "status": "PASS",
            "synthetic_seed_count": SYNTHETIC_ANALYSIS_SEED_COUNT,
            "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
            "statistics": _timing_stats(analysis_samples),
        },
        "synthetic_timelock_encryption_timing": _load_tlock_encryption_stage(
            tlock_encryption_evidence
        ),
        "external_transparency_retention_timing": {
            "status": "NOT_EXECUTED",
            "reason": "final P6/transparency mechanism is not selected and validated",
        },
        "artifact_publication_retention_timing": {
            "status": "NOT_EXECUTED",
            "reason": "Actions artifact upload occurs after this evidence file is sealed",
        },
    }
    if tuple(stages) != REQUIRED_STAGE_NAMES:
        raise RuntimeError("timing evidence stage set drifted from the required contract")

    coverage_complete = all(stage["status"] == "PASS" for stage in stages.values())
    artifact = {
        "schema_version": 1,
        "evidence_class": EVIDENCE_CLASS,
        "epistemic_status": "PARTIAL_SYNTHETIC_TIMING_NOT_W_EVIDENCE",
        "issue": 293,
        "parent_issue": 287,
        "control_plane_sha": os.environ.get("EVIDENCE_SHA", "unknown"),
        "workflow_content_sha256": os.environ.get("TIMING_WORKFLOW_SHA256", "unknown"),
        "helper_content_sha256": os.environ.get("TIMING_HELPER_SHA256", "unknown"),
        "dependency_lock_sha256": os.environ.get("DEPENDENCY_LOCK_SHA256", "unknown"),
        "analysis_content_sha256": os.environ.get("ANALYSIS_SHA256", "unknown"),
        "run_pilot_content_sha256": os.environ.get("RUN_PILOT_SHA256", "unknown"),
        "task_engine_content_sha256": os.environ.get("TASK_ENGINE_SHA256", "unknown"),
        "runner_class": os.environ.get("RUNNER_CLASS", "unknown"),
        "repetitions": repetitions,
        "stages": stages,
        "coverage_complete": coverage_complete,
        "w_proposal_eligible": False,
        "numeric_w_selected": False,
        "proposed_w_seconds": None,
        "protocol_frozen": False,
        "pilot_authorized": False,
        "empirical_data_collection": False,
        "secret_instantiation": False,
        "unblinding_requested": False,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    if artifact["coverage_complete"]:
        artifact["epistemic_status"] = "COMPLETE_SYNTHETIC_TIMING_REQUIRES_INDEPENDENT_W_REVIEW"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(artifact, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    output_path.with_suffix(output_path.suffix + ".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="utf-8"
    )
    return artifact


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repetitions", type=int, default=DEFAULT_REPETITIONS)
    parser.add_argument("--require-tlock-verification", action="store_true")
    parser.add_argument("--tlock-encryption-evidence", type=Path)
    args = parser.parse_args(argv)
    artifact = run_study(
        output_path=args.output,
        repetitions=args.repetitions,
        require_tlock_verification=args.require_tlock_verification,
        tlock_encryption_evidence=args.tlock_encryption_evidence,
    )
    print(
        json.dumps(
            {
                "evidence_class": artifact["evidence_class"],
                "coverage_complete": artifact["coverage_complete"],
                "w_proposal_eligible": artifact["w_proposal_eligible"],
                "numeric_w_selected": artifact["numeric_w_selected"],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
