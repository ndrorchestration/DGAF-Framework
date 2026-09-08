from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_track_a_epoch_001_final_closure.py"

spec = importlib.util.spec_from_file_location("track_a_final_closure", MODULE_PATH)
assert spec and spec.loader
closure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(closure)


def mutated(**updates):
    data = copy.deepcopy(closure.EXPECTED_CLOSURE)
    data.update(updates)
    return data


class FinalClosureValidatorTests(unittest.TestCase):
    def test_exact_closure_record_accepts(self):
        closure.validate_closure_record(copy.deepcopy(closure.EXPECTED_CLOSURE))

    def test_mutations_fail_closed(self):
        mutations = [
            ("record_type", "WRONG"),
            ("schema_version", 2),
            ("protocol_id", "WRONG"),
            ("frozen_candidate_sha", "0" * 40),
            ("freeze_manifest_blob_sha", "0" * 40),
            ("open_blockers", ["BLOCKER"]),
            ("closure_status", "OPEN"),
            ("scientific_n_increment", 1),
            ("collection_authorized", True),
            ("unblinding_authorized", True),
            ("high_assurance_authorized", True),
        ]
        for key, value in mutations:
            with self.subTest(key=key, value=value):
                with self.assertRaises(SystemExit):
                    closure.validate_closure_record(mutated(**{key: value}))

    def test_missing_field_fails_closed(self):
        data = copy.deepcopy(closure.EXPECTED_CLOSURE)
        data.pop("closure_status")
        with self.assertRaises(SystemExit):
            closure.validate_closure_record(data)

    def test_extra_field_fails_closed(self):
        data = copy.deepcopy(closure.EXPECTED_CLOSURE)
        data["unexpected"] = True
        with self.assertRaises(SystemExit):
            closure.validate_closure_record(data)

    def test_protected_source_set_is_exact(self):
        self.assertEqual(
            closure.EXPECTED_PROTECTED_SOURCE_BLOBS,
            {
                "docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_001_PREREGISTRATION.json": "52148950ff054a407c2e6b5cf36103695cf96474",
                "docs/experiment/TRACK_A_EPOCH_001_ANALYSIS_LOCK.json": "ff9a37a0be7a75912dbe0ae34dd95893d41efafb",
                "experiments/pdmal_pilot/track_a_epoch_001_analysis.py": "76bc8e9604c5d7e039e324e73036f353dc8ea31f",
                "experiments/pdmal_pilot/requirements-full-lock.txt": "00c1f779e97030f9b25ae494642edb31b5b09de5",
                "experiments/pdmal_pilot/task_engine.py": "90135e1c6dfccc3b56ffdc0dcb9eb50a0b2a5b05",
                "experiments/pdmal_pilot/harness_contract.py": "bb97c54ddf087fef568b1b3c8f8df72c30dad11e",
                "experiments/pdmal_pilot/topology_utils.py": "7ae92ba8a9ab964537e5dafa5e12de36b841391e",
                "experiments/pdmal_pilot/run_track_a_epoch_001.py": "d8ef6f31f49da82e4eaf5295bad024c3194f6d15",
            },
        )

    def test_freeze_identity_is_exact(self):
        self.assertEqual(
            closure.FREEZE_MANIFEST_BLOB_SHA,
            "ae15c6282351c01bd13ace2423d273ba0dde8348",
        )
        self.assertEqual(
            closure.FROZEN_CANDIDATE_SHA,
            "961b9918002c4c68afac9c0fd5dd3e352e49b926",
        )
        self.assertEqual(
            closure.FROZEN_CANDIDATE_TREE_SHA,
            "f20fa0ffee4b47872d84ce10cc9fd05e75c7306d",
        )

    def test_closure_remains_non_authorizing(self):
        expected = closure.EXPECTED_CLOSURE
        self.assertEqual(expected["scientific_n_increment"], 0)
        self.assertIs(expected["collection_authorized"], False)
        self.assertIs(expected["unblinding_authorized"], False)
        self.assertIs(expected["high_assurance_authorized"], False)
        self.assertEqual(expected["open_blockers"], [])


if __name__ == "__main__":
    unittest.main()
