#!/usr/bin/env python3
"""Derive a fail-closed DGAF completion state from repository evidence.

This controller is observational and advisory. It cannot grant governance or
scientific transitions and it never executes empirical work.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ACTION_CLASSES = {
    "automatable_non_authorizing",
    "human_controlled",
    "operator_external",
}
CHECK_TYPES = {"path_exists", "json_equals", "python_json_validator"}
NODE_STATES = {
    "SATISFIED",
    "ACTIONABLE",
    "HUMAN_ACTION_REQUIRED",
    "BLOCKED",
    "NOT_VERIFIED",
}


class GraphError(ValueError):
    """Raised when the completion graph violates controller invariants."""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def lookup_field(value: Any, dotted_field: str) -> Any:
    current = value
    for part in dotted_field.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(dotted_field)
        current = current[part]
    return current


def validate_graph(graph: dict[str, Any]) -> None:
    if graph.get("record_type") != "DGAF_COMPLETION_CONTROLLER_GRAPH":
        raise GraphError("wrong record_type")
    if graph.get("schema_version") != 1:
        raise GraphError("unsupported schema_version")
    if graph.get("scientific_state_effect") != "NONE":
        raise GraphError("controller must have scientific_state_effect=NONE")
    if graph.get("can_authorize") is not False:
        raise GraphError("controller must not be able to authorize")
    if graph.get("can_execute_empirical_work") is not False:
        raise GraphError("controller must not execute empirical work")

    authority = graph.get("authority")
    orchestration = graph.get("orchestration")
    lanes = graph.get("lanes")
    if not isinstance(authority, dict) or not isinstance(orchestration, dict) or not isinstance(lanes, list):
        raise GraphError("authority, orchestration, and lanes are required")
    if orchestration.get("specialist_outputs_are_authorization") is not False:
        raise GraphError("specialist output must never become authorization")

    specialist_roles = orchestration.get("specialist_roles")
    pattern_bundle = orchestration.get("pattern_bundle")
    if not isinstance(specialist_roles, dict) or not specialist_roles:
        raise GraphError("specialist_roles must be a non-empty object")
    if authority.get("human_final_arbiter") not in specialist_roles:
        raise GraphError("human final arbiter must be an explicit specialist role")
    if not isinstance(pattern_bundle, list) or len(pattern_bundle) < 2:
        raise GraphError("pattern_bundle must select explicit registered patterns")

    all_ids: set[str] = set()
    for lane in lanes:
        if not isinstance(lane, dict) or not isinstance(lane.get("nodes"), list):
            raise GraphError("each lane must contain nodes")
        nodes = lane["nodes"]
        lane_ids: set[str] = set()
        for node in nodes:
            if not isinstance(node, dict):
                raise GraphError("node must be an object")
            node_id = node.get("id")
            if not isinstance(node_id, str) or not node_id:
                raise GraphError("node id must be a non-empty string")
            if node_id in all_ids:
                raise GraphError(f"duplicate node id: {node_id}")
            all_ids.add(node_id)
            lane_ids.add(node_id)
            if node.get("action_class") not in ACTION_CLASSES:
                raise GraphError(f"invalid action_class for {node_id}")
            specialists = node.get("specialists")
            if not isinstance(specialists, list) or not specialists:
                raise GraphError(f"specialists missing for {node_id}")
            unknown_specialists = sorted(set(specialists) - set(specialist_roles))
            if unknown_specialists:
                raise GraphError(f"unknown specialists for {node_id}: {unknown_specialists}")
            checks = node.get("checks")
            if not isinstance(checks, list) or not checks:
                raise GraphError(f"checks missing for {node_id}")
            for check in checks:
                if not isinstance(check, dict) or check.get("type") not in CHECK_TYPES:
                    raise GraphError(f"unsupported check in {node_id}")

        for node in nodes:
            dependencies = node.get("depends_on")
            if not isinstance(dependencies, list):
                raise GraphError(f"depends_on must be a list for {node['id']}")
            missing = sorted(set(dependencies) - lane_ids)
            if missing:
                raise GraphError(f"unknown dependencies for {node['id']}: {missing}")
        topological_order(nodes)


def topological_order(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    indexed = {str(node["id"]): node for node in nodes}
    pending = set(indexed)
    ordered: list[dict[str, Any]] = []
    resolved: set[str] = set()

    while pending:
        progressed = False
        for node in nodes:
            node_id = str(node["id"])
            if node_id not in pending:
                continue
            dependencies = set(node.get("depends_on", []))
            if dependencies <= resolved:
                ordered.append(node)
                resolved.add(node_id)
                pending.remove(node_id)
                progressed = True
        if not progressed:
            raise GraphError(f"cycle detected among nodes: {sorted(pending)}")
    return ordered


def evaluate_check(repo_root: Path, check: dict[str, Any]) -> dict[str, Any]:
    check_type = str(check["type"])
    if check_type == "path_exists":
        path = repo_root / str(check["path"])
        passed = path.exists()
        return {"type": check_type, "passed": passed, "ref": str(check["path"])}

    if check_type == "json_equals":
        relative = str(check["path"])
        path = repo_root / relative
        if not path.is_file():
            return {"type": check_type, "passed": False, "ref": relative, "reason": "file_absent"}
        try:
            payload = load_json(path)
            actual = lookup_field(payload, str(check["field"]))
        except (OSError, json.JSONDecodeError, KeyError) as exc:
            return {
                "type": check_type,
                "passed": False,
                "ref": relative,
                "reason": f"unreadable_or_missing_field:{type(exc).__name__}",
            }
        passed = actual == check.get("value") and type(actual) is type(check.get("value"))
        result: dict[str, Any] = {
            "type": check_type,
            "passed": passed,
            "ref": relative,
            "field": str(check["field"]),
        }
        if not passed:
            result["reason"] = "value_mismatch"
        return result

    if check_type == "python_json_validator":
        validator_path = repo_root / str(check["validator_path"])
        input_path = repo_root / str(check["input_path"])
        if not input_path.is_file():
            return {
                "type": check_type,
                "passed": False,
                "ref": str(check["input_path"]),
                "reason": "input_absent",
            }
        if not validator_path.is_file():
            return {
                "type": check_type,
                "passed": False,
                "error": True,
                "ref": str(check["validator_path"]),
                "reason": "validator_absent",
            }
        try:
            spec = importlib.util.spec_from_file_location("_dgaf_completion_validator", validator_path)
            if spec is None or spec.loader is None:
                raise ImportError("validator module could not be loaded")
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            function = getattr(module, str(check["function"]))
            payload = load_json(input_path)
            if not isinstance(payload, dict):
                raise ValueError("validator input must be a JSON object")
            function(payload)
        except ValueError as exc:
            return {
                "type": check_type,
                "passed": False,
                "ref": str(check["input_path"]),
                "reason": f"validator_rejected:{exc}",
            }
        except (AttributeError, ImportError, OSError, json.JSONDecodeError) as exc:
            return {
                "type": check_type,
                "passed": False,
                "error": True,
                "ref": str(check["input_path"]),
                "reason": f"validator_error:{type(exc).__name__}",
            }
        return {"type": check_type, "passed": True, "ref": str(check["input_path"])}

    raise GraphError(f"unsupported check type: {check_type}")


def git_identity(repo_root: Path) -> tuple[str, str]:
    try:
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_root, text=True, stderr=subprocess.DEVNULL
        ).strip()
        tree = subprocess.check_output(
            ["git", "rev-parse", "HEAD^{tree}"], cwd=repo_root, text=True, stderr=subprocess.DEVNULL
        ).strip()
        return head, tree
    except (OSError, subprocess.CalledProcessError):
        return "UNAVAILABLE", "UNAVAILABLE"


def derive_lane(repo_root: Path, lane: dict[str, Any]) -> dict[str, Any]:
    states: dict[str, str] = {}
    node_results: list[dict[str, Any]] = []

    for node in topological_order(lane["nodes"]):
        node_id = str(node["id"])
        dependencies = [str(value) for value in node["depends_on"]]
        dependency_states = {dependency: states[dependency] for dependency in dependencies}
        dependencies_satisfied = all(state == "SATISFIED" for state in dependency_states.values())
        checks = [evaluate_check(repo_root, check) for check in node["checks"]]
        check_error = any(result.get("error") is True for result in checks)
        own_satisfied = all(result["passed"] is True for result in checks)

        if check_error:
            state = "NOT_VERIFIED"
            reason = "check_execution_error"
        elif own_satisfied and dependencies_satisfied:
            state = "SATISFIED"
            reason = "all_predicates_satisfied"
        elif own_satisfied and not dependencies_satisfied:
            state = "NOT_VERIFIED"
            reason = "evidence_present_before_prerequisites"
        elif not dependencies_satisfied:
            state = "BLOCKED"
            reason = "prerequisite_not_satisfied"
        elif node["action_class"] == "automatable_non_authorizing":
            state = "ACTIONABLE"
            reason = "non_authorizing_work_reachable"
        else:
            state = "HUMAN_ACTION_REQUIRED"
            reason = "human_or_operator_controlled_gate_reachable"

        if state not in NODE_STATES:
            raise GraphError(f"invalid derived state for {node_id}")
        states[node_id] = state
        node_results.append(
            {
                "id": node_id,
                "label": node["label"],
                "state": state,
                "reason": reason,
                "action_class": node["action_class"],
                "depends_on": dependencies,
                "dependency_states": dependency_states,
                "specialists": node["specialists"],
                "checks": checks,
            }
        )

    reachable = [
        result for result in node_results if result["state"] in {"ACTIONABLE", "HUMAN_ACTION_REQUIRED"}
    ]
    first_reachable = reachable[0] if reachable else None
    counts = {state: sum(result["state"] == state for result in node_results) for state in sorted(NODE_STATES)}

    return {
        "id": lane["id"],
        "label": lane["label"],
        "nodes": node_results,
        "next_gate": first_reachable["id"] if first_reachable else None,
        "next_gate_state": first_reachable["state"] if first_reachable else None,
        "next_gate_specialists": first_reachable["specialists"] if first_reachable else [],
        "completion_distance": {
            "total_nodes": len(node_results),
            "satisfied_nodes": counts["SATISFIED"],
            "remaining_nodes": len(node_results) - counts["SATISFIED"],
            "actionable_non_authorizing_nodes": counts["ACTIONABLE"],
            "human_action_required_nodes": counts["HUMAN_ACTION_REQUIRED"],
            "blocked_nodes": counts["BLOCKED"],
            "not_verified_nodes": counts["NOT_VERIFIED"],
        },
    }


def derive_state(repo_root: Path, graph_path: Path) -> dict[str, Any]:
    graph_bytes = graph_path.read_bytes()
    graph_value = json.loads(graph_bytes)
    if not isinstance(graph_value, dict):
        raise GraphError("graph must be a JSON object")
    validate_graph(graph_value)

    head, tree = git_identity(repo_root)
    lanes = [derive_lane(repo_root, lane) for lane in graph_value["lanes"]]
    not_verified = sum(lane["completion_distance"]["not_verified_nodes"] for lane in lanes)

    return {
        "record_type": "DGAF_COMPLETION_CONTROLLER_STATE",
        "schema_version": 1,
        "controller_issue": graph_value["controller_issue"],
        "scope": graph_value["scope"],
        "source_head_sha": head,
        "source_tree_sha": tree,
        "graph_sha256": hashlib.sha256(graph_bytes).hexdigest(),
        "orchestration_pattern_bundle": graph_value["orchestration"]["pattern_bundle"],
        "scientific_state_effect": "NONE",
        "authorizes_transition": False,
        "empirical_execution_requested": False,
        "specialist_outputs_are_authorization": False,
        "lanes": lanes,
        "fail_closed": {
            "not_verified_node_count": not_verified,
            "controller_valid": not_verified == 0,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--graph",
        type=Path,
        default=Path("registry/dgaf_completion_controller.v0.1.json"),
    )
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    repo_root = args.repo_root.resolve()
    graph_path = args.graph if args.graph.is_absolute() else repo_root / args.graph
    try:
        state = derive_state(repo_root, graph_path)
    except (GraphError, OSError, json.JSONDecodeError) as exc:
        print(f"DGAF_COMPLETION_CONTROLLER=FAIL_CLOSED:{exc}", file=sys.stderr)
        return 2

    payload = json.dumps(state, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else repo_root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")

    if state["fail_closed"]["not_verified_node_count"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
