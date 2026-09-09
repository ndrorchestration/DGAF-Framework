#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDMAL = ROOT / "experiments/pdmal_pilot"
CONTRACT = ROOT / "docs/experiment/TRACK_A_EPOCH_001_RUNNER_CONTRACT.json"
RUNNER = PDMAL / "run_track_a_epoch_001.py"
TESTS = PDMAL / "test_track_a_epoch_001_runner.py"
WORKFLOW = ROOT / ".github/workflows/track-a-epoch-001-runner.yml"
FUTURE_GATES = (
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_PRECOLLECTION_PREFLIGHT.json",
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_IMMUTABLE_FREEZE_MANIFEST.json",
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_FINAL_CLOSURE_PACKET.json",
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_VERIFICATION_CLASSIFICATION.json",
    ROOT / "docs/experiment/track_a_runs/TRACK_A_EPOCH_001_COLLECTION_AUTHORIZATION.json",
)
EXPECTED = {
    ROOT / "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_001_PREREGISTRATION.json": "52148950ff054a407c2e6b5cf36103695cf96474",
    ROOT / "docs/experiment/TRACK_A_EPOCH_001_ANALYSIS_LOCK.json": "ff9a37a0be7a75912dbe0ae34dd95893d41efafb",
    PDMAL / "track_a_epoch_001_analysis.py": "76bc8e9604c5d7e039e324e73036f353dc8ea31f",
    PDMAL / "requirements-full-lock.txt": "00c1f779e97030f9b25ae494642edb31b5b09de5",
    PDMAL / "task_engine.py": "90135e1c6dfccc3b56ffdc0dcb9eb50a0b2a5b05",
    PDMAL / "harness_contract.py": "bb97c54ddf087fef568b1b3c8f8df72c30dad11e",
    PDMAL / "topology_utils.py": "7ae92ba8a9ab964537e5dafa5e12de36b841391e",
    RUNNER: "d8ef6f31f49da82e4eaf5295bad024c3194f6d15",
    TESTS: "f66d1b2dee94d2f2615575797484900cec0c4d94",
    CONTRACT: "b7b38696403c9626eb86a193acf5abffb8424c33",
    WORKFLOW: "36a21ac0bb66a6655367bafa7969ca183c50b501",
}


def blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True
    ).strip()


def load_runner():
    sys.path.insert(0, str(PDMAL))
    spec = importlib.util.spec_from_file_location("track_a_runner", RUNNER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["record_type"] == "TRACK_A_EPOCH_001_RUNNER_CONTRACT"
    assert contract["schema_version"] == 2
    assert contract["controller_issue"] == 421
    assert contract["status"] == "RUNNER_HARDENED_NOT_AUTHORIZED"

    for path, expected in EXPECTED.items():
        assert blob(path) == expected, f"source drift: {path}"

    runner = load_runner()
    assert runner.PROTOCOL_ID == "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
    assert runner.EPOCH_ID == "TRACK_A_EPOCH_001"
    assert runner.ALGORITHM_ID == "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1"
    assert runner.SEEDS == tuple(range(20270101, 20270151))
    assert runner.TOPOLOGIES == ("ring", "pdmal", "random_regular", "small_world", "complete")
    assert runner.FAILURE_COUNTS == (0, 1, 2, 3, 4, 5, 6, 8, 10)
    assert runner.EXPECTED_CELLS_PER_SEED == 45
    assert runner.EXPECTED_TOTAL == 2250
    assert runner.CONDITION == "null"

    canonical = tuple((t, f) for t in runner.TOPOLOGIES for f in runner.FAILURE_COUNTS)
    keyed = runner.ordered_matrix_cells(runner.SEEDS[0], b"validation-only-secret-material!!")
    assert set(keyed) == set(canonical)
    assert keyed != canonical
    assert len(keyed) == len(set(keyed)) == 45

    assert contract["endpoint"]["type"] == "strict_boolean"
    assert contract["endpoint"]["boolean_coercion_allowed"] is False
    assert contract["blinding"]["trial_order_blinding_required"] is True
    assert contract["blinding"]["public_record_exact_allowlist_required"] is True
    assert contract["integrity"]["protected_source_drift_after_freeze_prohibited"] is True
    assert contract["integrity"]["frozen_candidate_must_be_authorization_ancestor"] is True
    assert contract["matrix"]["historical_epoch_004_substitution_allowed"] is False
    assert contract["authorization"]["authorization_head_exactly_one_parent"] is True
    assert contract["authorization"]["authorization_file_must_be_only_change"] is True
    assert contract["successor_gate_chain"]["same_system_verification_must_be_nonindependent"] is True

    expected_order = [
        "TRACK_A_EPOCH_001_PRECOLLECTION_PREFLIGHT",
        "TRACK_A_EPOCH_001_IMMUTABLE_FREEZE_MANIFEST",
        "TRACK_A_EPOCH_001_FINAL_CLOSURE_PACKET",
        "TRACK_A_EPOCH_001_VERIFICATION_CLASSIFICATION",
        "TRACK_A_EPOCH_001_COLLECTION_AUTHORIZATION",
    ]
    assert contract["successor_gate_chain"]["order"] == expected_order

    for path in FUTURE_GATES:
        assert not path.exists(), f"runner PR must not contain future gate: {path}"

    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "github.event.pull_request.head.sha" in workflow
    assert "Prove checkout is exact PR head" in workflow
    assert "Prove successor gates are absent from runner PR" in workflow
    assert "SCIENTIFIC_N_INCREMENT = 0" in workflow

    assert contract["authorization"]["pr_validation_can_authorize"] is False
    assert contract["authorization"]["collection_authorized"] is False
    assert contract["authorization"]["unblinding_authorized"] is False
    assert contract["authorization"]["high_assurance_authorized"] is False
    assert contract["scientific_n_increment"] == 0
    assert contract["track_a_freeze"] == "NOT_ESTABLISHED"
    assert contract["track_a_empirical_execution"] == "NOT_AUTHORIZED"
    assert contract["canonical_dgaf_efficacy"] == "NOT_ESTABLISHED"
    assert contract["high_assurance"] == "NOT_AUTHORIZED_N0"

    print("TRACK_A_EPOCH_001_RUNNER_HARDENING_PASS_NONAUTHORIZING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
