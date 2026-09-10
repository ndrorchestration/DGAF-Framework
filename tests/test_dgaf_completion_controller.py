from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.derive_dgaf_completion_state import GraphError, derive_lane, derive_state, validate_graph

ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "registry/dgaf_completion_controller.v0.1.json"


def minimal_graph() -> dict:
    return {
        "record_type": "DGAF_COMPLETION_CONTROLLER_GRAPH",
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
            "forbidden_actions": ["EXECUTE_EMPIRICAL_COLLECTION"],
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
                        "checks": [{"type": "path_exists", "path": "a.json"}],
                    },
                    {
                        "id": "b",
                        "label": "second",
                        "depends_on": ["a"],
                        "action_class": "automatable_non_authorizing",
                        "specialists": ["The Actualizer", "The Auditor"],
                        "checks": [{"type": "path_exists", "path": "b.json"}],
                    },
                    {
                        "id": "c",
                        "label": "human gate",
                        "depends_on": ["b"],
                        "action_class": "human_controlled",
                        "specialists": ["Ender", "The Auditor"],
                        "checks": [{"type": "path_exists", "path": "c.json"}],
                    },
                ],
            }
        ],
    }


def write_graph(root: Path, graph: dict) -> Path:
    path = root / "graph.json"
    path.write_text(json.dumps(graph), encoding="utf-8")
    return path


def test_repository_graph_is_non_authorizing_and_currently_coherent() -> None:
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    validate_graph(graph)

    assert graph["can_authorize"] is False
    assert graph["can_execute_empirical_work"] is False
    assert graph["scientific_state_effect"] == "NONE"
    assert graph["orchestration"]["specialist_outputs_are_authorization"] is False
    assert graph["orchestration"]["pattern_bundle"] == [
        "P-PIER-001",
        "P-SAGA-001",
        "P-DURABLE-001",
        "P-CB-001",
        "P-POL-001",
    ]

    state = derive_state(ROOT, GRAPH_PATH)
    assert state["authorizes_transition"] is False
    assert state["empirical_execution_requested"] is False
    assert state["scientific_state_effect"] == "NONE"
    assert state["fail_closed"]["not_verified_node_count"] == 0

    receipt = ROOT / "docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json"
    if not receipt.exists():
        lane = state["lanes"][0]
        assert lane["next_gate"] == "real_custody_v2"
        assert lane["next_gate_state"] == "HUMAN_ACTION_REQUIRED"
        nodes = {node["id"]: node for node in lane["nodes"]}
        assert nodes["custody_v2_tooling"]["state"] == "SATISFIED"
        assert nodes["precollection_preflight"]["state"] == "BLOCKED"


def test_reducer_marks_reachable_automation_and_blocks_downstream(tmp_path: Path) -> None:
    graph = minimal_graph()
    (tmp_path / "a.json").write_text("{}", encoding="utf-8")

    lane = derive_lane(tmp_path, graph["lanes"][0])
    nodes = {node["id"]: node for node in lane["nodes"]}
    assert nodes["a"]["state"] == "SATISFIED"
    assert nodes["b"]["state"] == "ACTIONABLE"
    assert nodes["c"]["state"] == "BLOCKED"
    assert lane["next_gate"] == "b"
    assert lane["next_gate_specialists"] == ["The Actualizer", "The Auditor"]


def test_reducer_marks_reachable_human_gate(tmp_path: Path) -> None:
    graph = minimal_graph()
    (tmp_path / "a.json").write_text("{}", encoding="utf-8")
    (tmp_path / "b.json").write_text("{}", encoding="utf-8")

    lane = derive_lane(tmp_path, graph["lanes"][0])
    nodes = {node["id"]: node for node in lane["nodes"]}
    assert nodes["a"]["state"] == "SATISFIED"
    assert nodes["b"]["state"] == "SATISFIED"
    assert nodes["c"]["state"] == "HUMAN_ACTION_REQUIRED"
    assert lane["next_gate"] == "c"


def test_out_of_order_evidence_is_not_verified(tmp_path: Path) -> None:
    graph = minimal_graph()
    (tmp_path / "b.json").write_text("{}", encoding="utf-8")

    lane = derive_lane(tmp_path, graph["lanes"][0])
    nodes = {node["id"]: node for node in lane["nodes"]}
    assert nodes["a"]["state"] == "ACTIONABLE"
    assert nodes["b"]["state"] == "NOT_VERIFIED"
    assert nodes["b"]["reason"] == "evidence_present_before_prerequisites"
    assert nodes["c"]["state"] == "BLOCKED"


def test_graph_rejects_authority_leakage() -> None:
    graph = minimal_graph()
    graph["can_authorize"] = True
    with pytest.raises(GraphError, match="must not be able to authorize"):
        validate_graph(graph)

    graph = minimal_graph()
    graph["can_execute_empirical_work"] = True
    with pytest.raises(GraphError, match="must not execute empirical work"):
        validate_graph(graph)

    graph = minimal_graph()
    graph["orchestration"]["specialist_outputs_are_authorization"] = True
    with pytest.raises(GraphError, match="must never become authorization"):
        validate_graph(graph)


def test_graph_rejects_cycles_and_unknown_specialists() -> None:
    graph = minimal_graph()
    graph["lanes"][0]["nodes"][0]["depends_on"] = ["c"]
    with pytest.raises(GraphError, match="cycle detected"):
        validate_graph(graph)

    graph = minimal_graph()
    graph["lanes"][0]["nodes"][0]["specialists"] = ["Unregistered Agent"]
    with pytest.raises(GraphError, match="unknown specialists"):
        validate_graph(graph)


def test_json_check_is_strict_about_boolean_vs_integer(tmp_path: Path) -> None:
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
                    "path": "value.json",
                    "field": "authorized",
                    "value": False,
                }
            ],
        }
    ]
    (tmp_path / "value.json").write_text('{"authorized": 0}', encoding="utf-8")
    lane = derive_lane(tmp_path, graph["lanes"][0])
    assert lane["nodes"][0]["state"] == "ACTIONABLE"
    assert lane["nodes"][0]["checks"][0]["reason"] == "value_mismatch"


def test_python_json_validator_is_fail_closed(tmp_path: Path) -> None:
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
                    "validator_path": "validator.py",
                    "function": "validate",
                    "input_path": "receipt.json",
                }
            ],
        }
    ]
    (tmp_path / "validator.py").write_text(
        "def validate(payload):\n    raise ValueError('synthetic rejection')\n",
        encoding="utf-8",
    )
    (tmp_path / "receipt.json").write_text("{}", encoding="utf-8")

    lane = derive_lane(tmp_path, graph["lanes"][0])
    result = lane["nodes"][0]
    assert result["state"] == "HUMAN_ACTION_REQUIRED"
    assert result["checks"][0]["passed"] is False
    assert "validator_rejected" in result["checks"][0]["reason"]


def test_derive_state_is_deterministic_for_same_tree(tmp_path: Path) -> None:
    graph = minimal_graph()
    (tmp_path / "a.json").write_text("{}", encoding="utf-8")
    graph_path = write_graph(tmp_path, graph)

    first = derive_state(tmp_path, graph_path)
    second = derive_state(tmp_path, graph_path)
    assert first == second
    assert first["source_head_sha"] == "UNAVAILABLE"
    assert first["source_tree_sha"] == "UNAVAILABLE"


def test_unknown_check_type_is_rejected_before_execution() -> None:
    graph = minimal_graph()
    mutated = copy.deepcopy(graph)
    mutated["lanes"][0]["nodes"][0]["checks"] = [{"type": "shell", "command": "rm -rf /"}]
    with pytest.raises(GraphError, match="unsupported check"):
        validate_graph(mutated)
