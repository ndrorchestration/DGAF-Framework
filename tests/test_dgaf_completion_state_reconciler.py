from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.derive_dgaf_completion_state import (
    GraphError,
    derive_lane,
    derive_state,
    validate_graph,
)

ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "registry/dgaf_completion_state_reconciler.v0.1.json"


def minimal_graph() -> dict:
    return {
        "record_type": "DGAF_COMPLETION_STATE_RECONCILER_GRAPH",
        "schema_version": 1,
        "controller_issue": 600,
        "status": "NON_AUTHORIZING_IMPLEMENTATION",
        "scope": "TEST_ONLY",
        "scientific_state_effect": "NONE",
        "can_authorize": False,
        "can_execute_empirical_work": False,
        "authority": {
            "human_final_arbiter": "Ender",
            "canonical_authority_sources": ["test-authority"],
            "forbidden_actions": [
                "GRANT_FREEZE",
                "GRANT_COLLECTION_AUTHORIZATION",
                "GENERATE_REAL_CUSTODY_SECRET",
                "CLAIM_INDEPENDENT_VERIFICATION",
                "EXECUTE_EMPIRICAL_COLLECTION",
                "AUTHORIZE_UNBLINDING",
                "AUTHORIZE_PRIMARY_ANALYSIS",
                "PROMOTE_CANONICAL_DGAF_EFFICACY",
                "INCREMENT_SCIENTIFIC_N",
            ],
        },
        "orchestration": {
            "pattern_bundle": ["P-PIER-001", "P-POL-001"],
            "specialist_roles": {
                "The Auditor": "verification",
                "The Actualizer": "execution",
                "Ender": "human_final_transition_authority",
            },
            "specialist_outputs_are_authorization": False,
        },
        "lanes": [
            {
                "id": "test-lane",
                "label": "test lane",
                "nodes": [
                    {
                        "id": "a",
                        "label": "first",
                        "depends_on": [],
                        "action_class": "automatable_non_authorizing",
                        "specialists": ["The Auditor"],
                        "checks": [
                            {
                                "type": "path_exists",
                                "path": "docs/experiment/a.json",
                            }
                        ],
                    },
                    {
                        "id": "b",
                        "label": "second",
                        "depends_on": ["a"],
                        "action_class": "automatable_non_authorizing",
                        "specialists": ["The Actualizer", "The Auditor"],
                        "checks": [
                            {
                                "type": "path_exists",
                                "path": "docs/experiment/b.json",
                            }
                        ],
                    },
                    {
                        "id": "c",
                        "label": "human gate",
                        "depends_on": ["b"],
                        "action_class": "human_controlled",
                        "specialists": ["Ender", "The Auditor"],
                        "checks": [
                            {
                                "type": "path_exists",
                                "path": "docs/experiment/c.json",
                            }
                        ],
                    },
                ],
            }
        ],
    }


def write_path(root: Path, relative: str, content: str = "{}") -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def write_graph(root: Path, graph: dict) -> Path:
    path = root / "graph.json"
    path.write_text(json.dumps(graph), encoding="utf-8")
    return path


class CompletionStateReconcilerTests(unittest.TestCase):
    def test_repository_graph_is_non_authorizing_and_currently_coherent(self) -> None:
        graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
        validate_graph(graph)

        self.assertIs(graph["can_authorize"], False)
        self.assertIs(graph["can_execute_empirical_work"], False)
        self.assertEqual(graph["scientific_state_effect"], "NONE")
        self.assertIs(graph["orchestration"]["specialist_outputs_are_authorization"], False)
        self.assertEqual(
            graph["orchestration"]["pattern_bundle"],
            ["P-PIER-001", "P-SAGA-001", "P-DURABLE-001", "P-CB-001", "P-POL-001"],
        )
        custody_node = next(
            node
            for node in graph["lanes"][0]["nodes"]
            if node["id"] == "real_custody_v2"
        )
        self.assertTrue(
            any(check["type"] == "file_sha256_equals_json_field" for check in custody_node["checks"])
        )

        state = derive_state(ROOT, GRAPH_PATH)
        self.assertIs(state["authorizes_transition"], False)
        self.assertIs(state["empirical_execution_requested"], False)
        self.assertEqual(state["scientific_state_effect"], "NONE")
        self.assertEqual(state["fail_closed"]["not_verified_node_count"], 0)

        receipt = ROOT / "docs/experiment/track_a_runs/" "TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json"
        if not receipt.exists():
            lane = state["lanes"][0]
            self.assertEqual(lane["next_gate"], "real_custody_v2")
            self.assertEqual(lane["next_gate_state"], "HUMAN_ACTION_REQUIRED")
            nodes = {node["id"]: node for node in lane["nodes"]}
            self.assertEqual(nodes["custody_v2_tooling"]["state"], "SATISFIED")
            self.assertEqual(nodes["precollection_preflight"]["state"], "BLOCKED")

    def test_reducer_marks_reachable_automation_and_blocks_downstream(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            graph = minimal_graph()
            write_path(root, "docs/experiment/a.json")

            lane = derive_lane(root, graph["lanes"][0])
            nodes = {node["id"]: node for node in lane["nodes"]}
            self.assertEqual(nodes["a"]["state"], "SATISFIED")
            self.assertEqual(nodes["b"]["state"], "ACTIONABLE")
            self.assertEqual(nodes["c"]["state"], "BLOCKED")
            self.assertEqual(lane["next_gate"], "b")
            self.assertEqual(lane["next_gate_specialists"], ["The Actualizer", "The Auditor"])

    def test_reducer_marks_reachable_human_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            graph = minimal_graph()
            write_path(root, "docs/experiment/a.json")
            write_path(root, "docs/experiment/b.json")

            lane = derive_lane(root, graph["lanes"][0])
            nodes = {node["id"]: node for node in lane["nodes"]}
            self.assertEqual(nodes["a"]["state"], "SATISFIED")
            self.assertEqual(nodes["b"]["state"], "SATISFIED")
            self.assertEqual(nodes["c"]["state"], "HUMAN_ACTION_REQUIRED")
            self.assertEqual(lane["next_gate"], "c")

    def test_out_of_order_evidence_is_not_verified(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            graph = minimal_graph()
            write_path(root, "docs/experiment/b.json")

            lane = derive_lane(root, graph["lanes"][0])
            nodes = {node["id"]: node for node in lane["nodes"]}
            self.assertEqual(nodes["a"]["state"], "ACTIONABLE")
            self.assertEqual(nodes["b"]["state"], "NOT_VERIFIED")
            self.assertEqual(nodes["b"]["reason"], "evidence_present_before_prerequisites")
            self.assertEqual(nodes["c"]["state"], "BLOCKED")

    def test_graph_rejects_authority_leakage(self) -> None:
        graph = minimal_graph()
        graph["can_authorize"] = True
        with self.assertRaisesRegex(GraphError, "must not be able to authorize"):
            validate_graph(graph)

        graph = minimal_graph()
        graph["can_execute_empirical_work"] = True
        with self.assertRaisesRegex(GraphError, "must not execute empirical work"):
            validate_graph(graph)

        graph = minimal_graph()
        graph["orchestration"]["specialist_outputs_are_authorization"] = True
        with self.assertRaisesRegex(GraphError, "must never become authorization"):
            validate_graph(graph)

        graph = minimal_graph()
        graph["authority"]["forbidden_actions"].remove("INCREMENT_SCIENTIFIC_N")
        with self.assertRaisesRegex(GraphError, "authority prohibitions are missing"):
            validate_graph(graph)

    def test_graph_rejects_cycles_and_unknown_specialists(self) -> None:
        graph = minimal_graph()
        graph["lanes"][0]["nodes"][0]["depends_on"] = ["c"]
        with self.assertRaisesRegex(GraphError, "cycle detected"):
            validate_graph(graph)

        graph = minimal_graph()
        graph["lanes"][0]["nodes"][0]["specialists"] = ["Unregistered Agent"]
        with self.assertRaisesRegex(GraphError, "unknown specialists"):
            validate_graph(graph)

    def test_json_check_is_strict_about_boolean_vs_integer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            graph = minimal_graph()
            graph["lanes"][0]["nodes"] = [
                {
                    "id": "strict",
                    "label": "strict json",
                    "depends_on": [],
                    "action_class": "automatable_non_authorizing",
                    "specialists": ["The Auditor"],
                    "checks": [
                        {
                            "type": "json_equals",
                            "path": "docs/experiment/value.json",
                            "field": "authorized",
                            "value": False,
                        }
                    ],
                }
            ]
            write_path(root, "docs/experiment/value.json", '{"authorized": 0}')

            lane = derive_lane(root, graph["lanes"][0])
            self.assertEqual(lane["nodes"][0]["state"], "ACTIONABLE")
            self.assertEqual(lane["nodes"][0]["checks"][0]["reason"], "value_mismatch")

    def test_file_sha256_json_binding_accepts_match_and_rejects_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            graph = minimal_graph()
            graph["lanes"][0]["nodes"] = [
                {
                    "id": "binding",
                    "label": "certificate binding",
                    "depends_on": [],
                    "action_class": "operator_external",
                    "specialists": ["Ender", "The Auditor"],
                    "checks": [
                        {
                            "type": "file_sha256_equals_json_field",
                            "file_path": "docs/experiment/cert.pem",
                            "json_path": "docs/experiment/receipt.json",
                            "field": "certificate_sha256",
                        }
                    ],
                }
            ]
            certificate = b"synthetic public certificate bytes\n"
            cert_path = root / "docs/experiment/cert.pem"
            cert_path.parent.mkdir(parents=True, exist_ok=True)
            cert_path.write_bytes(certificate)
            write_path(
                root,
                "docs/experiment/receipt.json",
                json.dumps({"certificate_sha256": hashlib.sha256(certificate).hexdigest()}),
            )

            lane = derive_lane(root, graph["lanes"][0])
            self.assertEqual(lane["nodes"][0]["state"], "SATISFIED")
            self.assertIs(lane["nodes"][0]["checks"][0]["passed"], True)

            cert_path.write_bytes(b"wrong certificate bytes\n")
            lane = derive_lane(root, graph["lanes"][0])
            self.assertEqual(lane["nodes"][0]["state"], "HUMAN_ACTION_REQUIRED")
            self.assertIs(lane["nodes"][0]["checks"][0]["passed"], False)
            self.assertEqual(lane["nodes"][0]["checks"][0]["reason"], "sha256_mismatch")

    def test_file_sha256_json_binding_rejects_unsafe_paths(self) -> None:
        graph = minimal_graph()
        graph["lanes"][0]["nodes"][0]["checks"] = [
            {
                "type": "file_sha256_equals_json_field",
                "file_path": "docs/experiment/../../secret.pem",
                "json_path": "docs/experiment/receipt.json",
                "field": "certificate_sha256",
            }
        ]
        with self.assertRaisesRegex(GraphError, "prohibited path traversal"):
            validate_graph(graph)

        graph = minimal_graph()
        graph["lanes"][0]["nodes"][0]["checks"] = [
            {
                "type": "file_sha256_equals_json_field",
                "file_path": ".github/workflows/cert.pem",
                "json_path": "docs/experiment/receipt.json",
                "field": "certificate_sha256",
            }
        ]
        with self.assertRaisesRegex(GraphError, "outside approved evidence roots"):
            validate_graph(graph)

    def test_allowlisted_python_validator_is_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            graph = minimal_graph()
            graph["lanes"][0]["nodes"] = [
                {
                    "id": "validator",
                    "label": "validator",
                    "depends_on": [],
                    "action_class": "operator_external",
                    "specialists": ["Ender", "The Auditor"],
                    "checks": [
                        {
                            "type": "python_json_validator",
                            "validator_path": ("scripts/validate_track_a_successor_solo_custody_receipt.py"),
                            "function": "validate_receipt",
                            "input_path": "docs/experiment/receipt.json",
                        }
                    ],
                }
            ]
            write_path(
                root,
                "scripts/validate_track_a_successor_solo_custody_receipt.py",
                "def validate_receipt(payload):\n" "    raise ValueError('synthetic rejection')\n",
            )
            write_path(root, "docs/experiment/receipt.json")

            lane = derive_lane(root, graph["lanes"][0])
            result = lane["nodes"][0]
            self.assertEqual(result["state"], "HUMAN_ACTION_REQUIRED")
            self.assertIs(result["checks"][0]["passed"], False)
            self.assertIn("validator_rejected", result["checks"][0]["reason"])

    def test_arbitrary_validator_is_rejected_before_execution(self) -> None:
        graph = minimal_graph()
        graph["lanes"][0]["nodes"][0]["checks"] = [
            {
                "type": "python_json_validator",
                "validator_path": "scripts/evil.py",
                "function": "run",
                "input_path": "docs/experiment/input.json",
            }
        ]
        with self.assertRaisesRegex(GraphError, "validator is not allowlisted"):
            validate_graph(graph)

    def test_traversal_and_unapproved_roots_are_rejected(self) -> None:
        graph = minimal_graph()
        graph["lanes"][0]["nodes"][0]["checks"] = [{"type": "path_exists", "path": "docs/experiment/../../etc/passwd"}]
        with self.assertRaisesRegex(GraphError, "prohibited path traversal"):
            validate_graph(graph)

        graph = minimal_graph()
        graph["lanes"][0]["nodes"][0]["checks"] = [
            {"type": "path_exists", "path": ".github/workflows/completion-controller.yml"}
        ]
        with self.assertRaisesRegex(GraphError, "outside approved evidence roots"):
            validate_graph(graph)

    def test_symlink_escape_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as repo_tmp, tempfile.TemporaryDirectory() as outside_tmp:
            root = Path(repo_tmp)
            outside = Path(outside_tmp)
            write_path(outside, "payload.json")
            link = root / "docs/experiment/link"
            link.parent.mkdir(parents=True, exist_ok=True)
            try:
                link.symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")

            graph = minimal_graph()
            graph["lanes"][0]["nodes"] = [
                {
                    "id": "escape",
                    "label": "escape",
                    "depends_on": [],
                    "action_class": "automatable_non_authorizing",
                    "specialists": ["The Auditor"],
                    "checks": [
                        {
                            "type": "path_exists",
                            "path": "docs/experiment/link/payload.json",
                        }
                    ],
                }
            ]
            with self.assertRaisesRegex(GraphError, "escapes repository root"):
                derive_lane(root, graph["lanes"][0])

    def test_derive_state_is_deterministic_for_same_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            graph = minimal_graph()
            write_path(root, "docs/experiment/a.json")
            graph_path = write_graph(root, graph)

            first = derive_state(root, graph_path)
            second = derive_state(root, graph_path)
            self.assertEqual(first, second)
            self.assertEqual(first["source_head_sha"], "UNAVAILABLE")
            self.assertEqual(first["source_tree_sha"], "UNAVAILABLE")

    def test_unknown_check_type_and_extra_keys_are_rejected(self) -> None:
        graph = minimal_graph()
        mutated = copy.deepcopy(graph)
        mutated["lanes"][0]["nodes"][0]["checks"] = [{"type": "shell", "command": "rm -rf /"}]
        with self.assertRaisesRegex(GraphError, "unsupported check"):
            validate_graph(mutated)

        graph = minimal_graph()
        graph["lanes"][0]["nodes"][0]["checks"][0]["command"] = "unexpected"
        with self.assertRaisesRegex(GraphError, "path_exists keys invalid"):
            validate_graph(graph)


if __name__ == "__main__":
    unittest.main()
