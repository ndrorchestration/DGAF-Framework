"""Deterministic pre-freeze harness tests."""

import hashlib
import importlib
import sys
from pathlib import Path
from types import ModuleType

from artifact_schema import (
    ARTIFACT_SCHEMA_VERSION,
    sha256_sidecar,
    validate_artifact_document,
    validate_seed_record,
)
from harness_contract import (
    EXPERIMENT_CONDITIONS,
    TOPOLOGY_SPECS,
    blind_condition,
    canonical_json_bytes,
    deterministic_contract_run,
    generate_topology,
    make_streams,
    stream_fingerprint,
)
from topology_utils import graph_fingerprint


def test_condition_and_topology_axes_are_distinct() -> None:
    assert set(EXPERIMENT_CONDITIONS) == {"null", "simple", "static", "dgaf", "dgaf_pdmal"}
    assert set(TOPOLOGY_SPECS) == {"ring", "pdmal", "random_regular", "small_world", "complete"}
    assert set(EXPERIMENT_CONDITIONS) != set(TOPOLOGY_SPECS)


def test_seedsequence_streams_are_deterministic() -> None:
    a = make_streams(20260817)
    b = make_streams(20260817)
    for stream_id in a:
        assert a[stream_id].integers(0, 2**32, size=16).tolist() == b[stream_id].integers(0, 2**32, size=16).tolist()


def test_stream_fingerprint_is_reproducible() -> None:
    assert stream_fingerprint(20260817) == stream_fingerprint(20260817)


def test_blinding_is_deterministic_without_exposing_key() -> None:
    key = b"test-only-key-000000000000000000000000"
    blinded_a = blind_condition("dgaf_pdmal", key)
    blinded_b = blind_condition("dgaf_pdmal", key)
    assert blinded_a == blinded_b
    assert "dgaf_pdmal" not in blinded_a
    assert len(blinded_a) == len("blind_" + "0" * 16)


def test_topology_contracts_and_deterministic_output() -> None:
    key = b"test-only-key-000000000000000000000000"
    a = deterministic_contract_run(20260817, key)
    b = deterministic_contract_run(20260817, key)
    assert a == b
    assert len(a) == 5
    assert all(result.topology_valid for result in a)
    assert all(result.status == "CONTRACT_VALIDATED_ONLY" for result in a)


def test_topology_fingerprints_are_reproducible() -> None:
    seed = 20260817
    stream_a = make_streams(seed)["topology_construction"]
    stream_b = make_streams(seed)["topology_construction"]
    for name in TOPOLOGY_SPECS:
        graph_a = generate_topology(name, stream_a)
        graph_b = generate_topology(name, stream_b)
        assert graph_fingerprint(graph_a) == graph_fingerprint(graph_b)


def test_contract_results_include_topology_fingerprints() -> None:
    results = deterministic_contract_run(20260817, b"contract-only-test-key-000000000000000000")
    assert all(len(result.topology_fingerprint) == 64 for result in results)
    assert all(int(result.topology_fingerprint, 16) >= 0 for result in results)


def test_canonical_json_hash_is_stable() -> None:
    payload = {"b": 2, "a": [3, 1]}
    expected = hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
    assert hashlib.sha256(canonical_json_bytes(payload)).hexdigest() == expected


def _valid_seed_record() -> dict:
    return {
        "experiment_id": "PDMAL-PREFREEZE",
        "protocol_version": "1.1",
        "experiment_commit_sha": "a" * 40,
        "seed_id": "seed-0001",
        "blinded_condition_id": "blind_0123456789abcdef",
        "trial_id": "trial-0001",
        "primary_outcome": 1.0,
        "secondary_outcomes": {},
        "failure": {},
        "recovery": {},
        "runtime_ms": 10,
        "status": "SUCCESS",
        "excluded": False,
        "exclusion_reason": None,
        "environment_fingerprint": "env-abc",
        "artifact_sha256": "b" * 64,
    }


def _valid_artifact_document() -> dict:
    return {
        "schema_version": ARTIFACT_SCHEMA_VERSION,
        "artifact_version": "1",
        "protocol_status": "PRE-FREEZE",
        "empirical_data_collection": False,
        "records": [_valid_seed_record()],
    }


def test_seed_artifact_schema_and_sidecar() -> None:
    record = _valid_seed_record()
    validate_seed_record(record)
    document = _valid_artifact_document()
    validate_artifact_document(document)
    raw = canonical_json_bytes(document)
    sidecar = sha256_sidecar(raw, "seed-0001.json")
    assert sidecar.endswith("  seed-0001.json\n")
    assert len(sidecar.split()[0]) == 64


def test_artifact_schema_version_is_required() -> None:
    document = _valid_artifact_document()
    del document["schema_version"]
    try:
        validate_artifact_document(document)
    except AssertionError as exc:
        assert "schema_version" in str(exc)
    else:
        raise AssertionError("artifact without schema_version must fail closed")


def test_invalid_artifact_schema_version_fails_closed() -> None:
    document = _valid_artifact_document()
    document["schema_version"] = "0.9"
    try:
        validate_artifact_document(document)
    except AssertionError as exc:
        assert "schema_version" in str(exc)
    else:
        raise AssertionError("unsupported schema_version must fail closed")


def test_excluded_artifact_requires_reason() -> None:
    record = _valid_seed_record()
    record["excluded"] = True
    try:
        validate_seed_record(record)
    except AssertionError as exc:
        assert "exclusion_reason" in str(exc)
    else:
        raise AssertionError("excluded artifact without reason must fail closed")


def test_p35_unverified_three_adapter_paths_are_nonempirical_fail_closed(monkeypatch) -> None:
    """Exercise real TGL source in the lean harness, without optional PPTL package dependencies."""
    root = Path(__file__).resolve().parents[2]
    pilot = Path(__file__).resolve().parent
    for directory in (root, pilot):
        if str(directory) not in sys.path:
            monkeypatch.syspath_prepend(str(directory))

    # The root pptl/__init__.py eagerly imports the optional pandas-backed
    # HeraldAgent. This test exercises real TGL + P-35 modules directly,
    # not that unrelated package convenience import or a simulated gate.
    isolated_package = ModuleType("pptl")
    isolated_package.__path__ = [str(root / "pptl")]
    monkeypatch.setitem(sys.modules, "pptl", isolated_package)

    # Dynamic import after namespace isolation prevents isort from hoisting
    # these imports ahead of the test-only dependency boundary.
    CanonicalEpoch004TGLAdapter = importlib.import_module(
        "canonical_epoch_004_adapter"
    ).CanonicalEpoch004TGLAdapter
    CanonicalQualifiedTGLAdapter = importlib.import_module(
        "canonical_profile_tgl_diagnostic"
    ).CanonicalQualifiedTGLAdapter
    dgaf_module = importlib.import_module("dgaf_tgl_adapter")
    ConsensusState = dgaf_module.ConsensusState
    DGAF_TGLAdapter = dgaf_module.DGAF_TGLAdapter
    gate_module = importlib.import_module("pptl.triadic_governance_loop")
    GateResult, TurnStatus = gate_module.GateResult, gate_module.TurnStatus

    def synthetic_state() -> ConsensusState:
        return ConsensusState(
            seed_id=20260817,
            iteration=3,
            agent_values=(0.1, -0.2, 0.3, 0.4),
            alive=(True, True, True, True),
            original_neighbors=((1, 3), (0, 2), (1, 3), (0, 2)),
            active_neighbors=((1, 3), (0, 2), (1, 2), (0, 2)),
            failure_history=((1,),),
            failure_count_current=1,
            failure_count_total=1,
            current_final_std=0.2,
            current_mean=0.15,
            runtime_budget_remaining_ms=290000,
            protocol_id="PDMAL-PREFREEZE-V1",
        )

    adapters = (
        DGAF_TGLAdapter(session_id="p35-synthetic-unqualified"),
        CanonicalQualifiedTGLAdapter(
            session_id="p35-synthetic-diagnostic",
            qualification_bytes=b"intentionally-invalid-test-only-qualification",
        ),
        CanonicalEpoch004TGLAdapter(
            session_id="p35-synthetic-epoch004",
            qualification_bytes=b"intentionally-invalid-test-only-qualification",
        ),
    )
    for adapter in adapters:
        state = synthetic_state()
        original_values = tuple(state.agent_values)
        result = adapter.run_turn(state)
        assert tuple(state.agent_values) == original_values
        assert result.next_values is None
        assert result.decision == "FAIL_CLOSED"
        assert result.attempt_status.value == "FAILURE"
        assert result.audit.final_status is TurnStatus.ESCALATE
        assert result.audit.verify_seal()
        gates = result.audit.gate_records
        assert [gate.step for gate in gates] == list(range(10))
        assert gates[0].result is GateResult.SKIP
        assert "UNVERIFIED" in gates[0].notes
        assert all(gate.result is GateResult.SKIP for gate in gates[1:9])
        assert result.audit.input_hash == result.input_hash
