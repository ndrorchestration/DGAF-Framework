"""Deterministic pre-freeze harness tests."""

import hashlib

from harness_contract import (
    EXPERIMENT_CONDITIONS,
    TOPOLOGY_SPECS,
    blind_condition,
    canonical_json_bytes,
    deterministic_contract_run,
    make_streams,
    stream_fingerprint,
)


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


def test_canonical_json_hash_is_stable() -> None:
    payload = {"b": 2, "a": [3, 1]}
    expected = hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
    assert hashlib.sha256(canonical_json_bytes(payload)).hexdigest() == expected
