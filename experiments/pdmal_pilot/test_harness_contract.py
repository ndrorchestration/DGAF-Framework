"""Deterministic pre-freeze harness tests."""

import hashlib

from artifact_schema import (
    ARTIFACT_PROFILE,
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
    results = deterministic_contract_run(
        20260817, b"contract-only-test-key-000000000000000000"
    )
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
        "artifact_profile": ARTIFACT_PROFILE,
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


def test_invalid_artifact_profile_fails_closed() -> None:
    document = _valid_artifact_document()
    document["artifact_profile"] = "PDMAL_AUTHORIZED_PILOT_V1"
    try:
        validate_artifact_document(document)
    except AssertionError as exc:
        assert "artifact_profile" in str(exc)
    else:
        raise AssertionError("wrong lifecycle profile must fail closed")


def test_excluded_artifact_requires_reason() -> None:
    record = _valid_seed_record()
    record["excluded"] = True
    try:
        validate_seed_record(record)
    except AssertionError as exc:
        assert "exclusion_reason" in str(exc)
    else:
        raise AssertionError("excluded artifact without reason must fail closed")
