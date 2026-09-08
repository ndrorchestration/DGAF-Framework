#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_track_a_epoch_001_precollection_preflight.py"
spec = importlib.util.spec_from_file_location("preflight_validator", SCRIPT)
assert spec and spec.loader
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

CANDIDATE = "1" * 40
TREE = "2" * 40


def contract() -> dict:
    return {
        "schema_version": 2,
        "protocol_id": "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001",
        "algorithm_id": "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1",
        "next_gate": "CANDIDATE_STABILIZATION_AND_PRECOLLECTION_PREFLIGHT",
        "scientific_n_increment": 0,
        "track_a_freeze": "NOT_ESTABLISHED",
        "track_a_empirical_execution": "NOT_AUTHORIZED",
        "authorization": {"collection_authorized": False},
        "source_bindings": {
            "preregistration_merge_sha": "3" * 40,
            "preregistration_blob_sha": "4" * 40,
            "analysis_lock_merge_sha": "5" * 40,
            "analysis_lock_blob_sha": "6" * 40,
            "analysis_blob_sha": "7" * 40,
            "analysis_config_sha256": "8" * 64,
            "requirements_lock_blob_sha": "9" * 40,
            "task_engine_blob_sha": "a" * 40,
            "harness_contract_blob_sha": "b" * 40,
            "topology_utils_blob_sha": "c" * 40,
        },
        "matrix": {"cells_per_seed": 45, "expected_total_observations": 2250},
    }


def record() -> dict:
    return v.expected_record(contract(), CANDIDATE, TREE)


class PreflightValidatorTests(unittest.TestCase):
    def test_exact_record_accepts(self):
        v.validate_record(record(), contract(), CANDIDATE, TREE)

    def test_missing_field_fails_closed(self):
        data = record()
        data.pop("algorithm_id")
        with self.assertRaises(SystemExit):
            v.validate_record(data, contract(), CANDIDATE, TREE)

    def test_extra_field_fails_closed(self):
        data = record()
        data["empirical_result"] = "PASS"
        with self.assertRaises(SystemExit):
            v.validate_record(data, contract(), CANDIDATE, TREE)

    def test_contract_boundary_accepts(self):
        v.validate_contract_boundary(contract())

    def test_contract_boundary_rejects_authorization(self):
        data = contract()
        data["authorization"]["collection_authorized"] = True
        with self.assertRaises(SystemExit):
            v.validate_contract_boundary(data)


MUTATIONS = {
    "record_type": "WRONG",
    "schema_version": 2,
    "protocol_id": "WRONG",
    "candidate_sha": "f" * 40,
    "candidate_tree_sha": "e" * 40,
    "preregistration_merge_sha": "d" * 40,
    "analysis_lock_merge_sha": "c" * 40,
    "analysis_blob_sha": "b" * 40,
    "analysis_config_sha256": "a" * 64,
    "requirements_lock_blob_sha": "0" * 40,
    "algorithm_id": "DGAF",
    "matrix_cells_per_seed": 44,
    "expected_observations": 9000,
    "preflight_status": "FAIL",
    "scientific_n_increment": 1,
    "collection_authorized": True,
    "unblinding_authorized": True,
    "high_assurance_authorized": True,
}


def make_mutation_test(field: str, value: object):
    def test(self):
        data = copy.deepcopy(record())
        data[field] = value
        with self.assertRaises(SystemExit):
            v.validate_record(data, contract(), CANDIDATE, TREE)
    return test


for _field, _value in MUTATIONS.items():
    setattr(PreflightValidatorTests, f"test_mutation_{_field}_fails_closed", make_mutation_test(_field, _value))


if __name__ == "__main__":
    unittest.main(verbosity=2)
