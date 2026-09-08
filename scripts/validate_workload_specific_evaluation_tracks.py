#!/usr/bin/env python3
"""Validate workload-specific DGAF evaluation-track architecture."""
from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs/governance/WORKLOAD_SPECIFIC_DGAF_EVALUATION_TRACKS_V1.json"
HISTORICAL_PROFILE = ROOT / "docs/governance/CANONICAL_PDMAL_TREATMENT_PROFILE_CANDIDATE_V1.json"
KAPPA = ROOT / "components/KAPPA/dynamic_weight_router.py"
EVAL_ROUTER = ROOT / "components/evaluate_router.py"
SENTINEL_ROUTER = ROOT / "components/evaluate_router_v1_1.py"

EXPECTED_HISTORICAL_PROFILE_BLOB = "133d7b71c9e829d5461e7c911527c6b2b10ba9ae"


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
    ).strip()


def load_kappa():
    spec = importlib.util.spec_from_file_location("kappa_v36_architecture_check", KAPPA)
    if spec is None or spec.loader is None:
        raise AssertionError("unable to load KAPPA router")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    data = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    assert data["record_type"] == "DGAF_WORKLOAD_SPECIFIC_EVALUATION_TRACKS"
    assert data["status"] == "NONEMPIRICAL_CANDIDATE_ARCHITECTURE"
    assert data["scientific_n_increment"] == 0
    assert data["empirical_authorization"] is False

    historical = data["historical_profile_policy"]
    assert historical["profile_id"] == "DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1"
    assert historical["future_canonical_use"] is False
    assert historical["rewrite_historical_evidence"] is False
    assert historical["pool_into_future_profiles"] is False
    assert git_blob(HISTORICAL_PROFILE) == EXPECTED_HISTORICAL_PROFILE_BLOB
    assert historical["profile_blob_sha"] == EXPECTED_HISTORICAL_PROFILE_BLOB

    tracks = data["tracks"]
    assert set(tracks) == {
        "A_PDMAL_TOPOLOGY_ROBUSTNESS",
        "B1_SEMANTIC_ROUTING_SAFETY",
        "B2_STATEFUL_CONTEXT_CLOSURE",
        "B3_GRAPH_CONVERGENCE_MONITOR",
        "C_INTEGRATED_DGAF_SYSTEM",
    }

    track_a = tracks["A_PDMAL_TOPOLOGY_ROBUSTNESS"]
    assert track_a["workload_type"] == "NUMERIC_DISTRIBUTED_CONSENSUS"
    assert set(track_a["prohibited_condition_labels"]) == {
        "dgaf", "full_dgaf", "canonical_dgaf"
    }
    assert track_a["empirical_status"] == "NOT_AUTHORIZED"
    dispositions = track_a["dgaf_gate_disposition"]
    for gate in ("P-31", "P-33", "DEMIJOULE", "P-27", "P-29", "P-32", "P-30"):
        assert gate in dispositions

    b1 = tracks["B1_SEMANTIC_ROUTING_SAFETY"]
    required = set(b1["required_workload_fields"])
    assert {
        "content", "entropy_score", "kappa_score", "deontic",
        "scores.accuracy", "scores.false_blocked", "scores.adversarial",
        "scores.ambiguous", "scores.malformed",
    }.issubset(required)
    included_b1 = set(b1["included_components"])
    assert {
        "DEMIJOULE", "P-27_KAPPA_V3_6", "P-28_EVALUATION_PIPELINE",
        "P-29_SENTINEL", "P-30_EXTERNAL_PROFILE_QUALIFICATION",
    }.issubset(included_b1)
    for path in (KAPPA, EVAL_ROUTER, SENTINEL_ROUTER):
        assert path.exists()

    kappa = load_kappa()
    assert kappa.STRONG_THRESH == 0.22
    assert kappa.BLENDED_THRESH == 0.18

    b2 = tracks["B2_STATEFUL_CONTEXT_CLOSURE"]
    persistence_b2 = b2["persistence_contract"]
    assert persistence_b2["lifetime"] == "ONE_COMPLETE_SESSION"
    assert persistence_b2["reset"] == "ONLY_AT_SESSION_BOUNDARY"
    assert {
        "SCPE_TOKEN_STORE", "PHI_STABLE_COUNT", "PHI_TOTAL_COUNT",
        "PHI_CONSECUTIVE_FAILURES",
    }.issubset(set(persistence_b2["required_state"]))

    b3 = tracks["B3_GRAPH_CONVERGENCE_MONITOR"]
    persistence_b3 = b3["persistence_contract"]
    assert persistence_b3["lifetime"] == "ONE_GRAPH_SEQUENCE"
    assert persistence_b3["reset"] == "ONLY_AT_SEQUENCE_BOUNDARY"
    assert {
        "W_T", "W_T_MINUS_1", "DIVERGENCE_COUNTERS", "EVENT_HISTORY"
    }.issubset(set(persistence_b3["required_state"]))
    assert "DIRECT_MAPPING_TO_CONSENSUS_ALPHA" in b3["prohibited_uses"]

    integrated = tracks["C_INTEGRATED_DGAF_SYSTEM"]
    assert integrated["status"] == "DEFERRED"
    assert integrated["empirical_status"] == "PROHIBITED"

    # Future profiles are intentionally distinct identities.
    profile_ids = [
        tracks[name]["profile_id"]
        for name in tracks
    ]
    assert len(profile_ids) == len(set(profile_ids))
    assert historical["profile_id"] not in profile_ids

    # No implemented profile in this architecture may claim empirical readiness.
    for name, track in tracks.items():
        status = track.get("empirical_status")
        assert status in {"NOT_AUTHORIZED", "PROHIBITED"}, (name, status)

    print("WORKLOAD_SPECIFIC_EVALUATION_TRACKS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
