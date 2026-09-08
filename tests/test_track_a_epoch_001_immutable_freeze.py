#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_track_a_epoch_001_immutable_freeze.py"
spec = importlib.util.spec_from_file_location("freeze_validator", SCRIPT)
assert spec and spec.loader
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class ImmutableFreezeValidatorTests(unittest.TestCase):
    def test_exact_record_accepts(self):
        v.require_exact_record(v.expected_freeze())

    def test_missing_field_fails_closed(self):
        data = v.expected_freeze()
        data.pop("preflight_blob_sha")
        with self.assertRaises(SystemExit):
            v.require_exact_record(data)

    def test_extra_field_fails_closed(self):
        data = v.expected_freeze()
        data["authorization"] = True
        with self.assertRaises(SystemExit):
            v.require_exact_record(data)


MUTATIONS = {
    "record_type": "WRONG",
    "schema_version": 2,
    "protocol_id": "WRONG",
    "frozen_candidate_sha": "f" * 40,
    "frozen_candidate_tree_sha": "e" * 40,
    "preflight_blob_sha": "d" * 40,
    "freeze_status": "NOT_ESTABLISHED",
    "scientific_n_increment": 1,
    "collection_authorized": True,
    "unblinding_authorized": True,
    "high_assurance_authorized": True,
}


def make_mutation_test(field: str, value: object):
    def test(self):
        data = copy.deepcopy(v.expected_freeze())
        data[field] = value
        with self.assertRaises(SystemExit):
            v.require_exact_record(data)

    return test


for _field, _value in MUTATIONS.items():
    setattr(
        ImmutableFreezeValidatorTests,
        f"test_mutation_{_field}_fails_closed",
        make_mutation_test(_field, _value),
    )


def protected_source_drift_shape(self):
    data = copy.deepcopy(v.expected_freeze())
    first = next(iter(data["protected_source_blobs"]))
    data["protected_source_blobs"][first] = "0" * 40
    with self.assertRaises(SystemExit):
        v.require_exact_record(data)


setattr(
    ImmutableFreezeValidatorTests,
    "test_protected_source_mutation_fails_closed",
    protected_source_drift_shape,
)


if __name__ == "__main__":
    unittest.main(verbosity=2)
