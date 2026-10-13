"""Exact-source AOSS Stage-A source-driver candidate.

This executable is an implementation candidate only. It verifies the frozen ACP
checkout before import, runs exactly one requested recipe, preserves the raw ACP
provenance manifest bytes, and records any declared post-export transformation
separately. It does not perform observer evaluation, admission, replay, analysis,
or collection authorization.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

SOURCE_REPOSITORY = "ndrorchestration/agent-control-plane"
SOURCE_COMMIT = "dbab7c1afafec524ce7c18157de2089cafe79c87"
SOURCE_MODULE = "src/agent_control_plane/core.py"
SOURCE_MODULE_BLOB = "1341df7296a426b336b76ac6b1e4df67611ec931"
RECIPE_VERSION = "AOSS_V0_6_STAGE_A_SYNTHETIC_RECIPE_CATALOG_V1"

RECIPE_CLASSES = (
    "normal_completion",
    "policy_denial",
    "unknown_capability_rejection",
    "handler_failure",
    "cancellation",
    "exact_budget_success",
    "budget_exhaustion",
    "suppressed_budget_exception_fail_closed",
    "missing_event",
    "reordered_exported_events",
    "duplicate_replayed_event",
    "stale_timestamp",
    "malformed_manifest",
    "mismatched_run_id",
    "source_order_ambiguity",
    "missing_authority_evidence",
)

_BASE_RECIPE = {
    "missing_event": "normal_completion",
    "reordered_exported_events": "normal_completion",
    "duplicate_replayed_event": "normal_completion",
    "stale_timestamp": "normal_completion",
    "malformed_manifest": "normal_completion",
    "mismatched_run_id": "normal_completion",
    "source_order_ambiguity": "normal_completion",
    "missing_authority_evidence": "normal_completion",
}


class SourceDriverError(RuntimeError):
    """Fail-closed source-driver boundary error."""


def _fail(code: str) -> None:
    raise SourceDriverError(code)


def _git(root: Path, *args: str) -> str:
    env = os.environ.copy()
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        _fail("SOURCE_DRIVER_GIT_VERIFICATION_FAILED")
    return result.stdout.strip()


def verify_frozen_acp_checkout(acp_root: Path) -> None:
    root = Path(acp_root)
    if not root.is_dir():
        _fail("SOURCE_DRIVER_ACP_ROOT_MISSING")
    if _git(root, "rev-parse", "--is-shallow-repository") != "false":
        _fail("SOURCE_DRIVER_ACP_SHALLOW_REPOSITORY")
    if _git(root, "status", "--porcelain=v1", "--untracked-files=all"):
        _fail("SOURCE_DRIVER_ACP_WORKTREE_DIRTY")
    if _git(root, "rev-parse", "HEAD") != SOURCE_COMMIT:
        _fail("SOURCE_DRIVER_ACP_COMMIT_MISMATCH")
    if _git(root, "rev-parse", f"HEAD:{SOURCE_MODULE}") != SOURCE_MODULE_BLOB:
        _fail("SOURCE_DRIVER_ACP_MODULE_BLOB_MISMATCH")


def _canonical_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_frozen_acp(acp_root: Path) -> Any:
    verify_frozen_acp_checkout(acp_root)
    if any(name == "agent_control_plane" or name.startswith("agent_control_plane.") for name in sys.modules):
        _fail("SOURCE_DRIVER_ACP_ALREADY_IMPORTED")
    src = str(Path(acp_root) / "src")
    sys.path.insert(0, src)
    try:
        import agent_control_plane as acp  # type: ignore

        return acp
    except Exception as exc:
        raise SourceDriverError("SOURCE_DRIVER_ACP_IMPORT_FAILED") from exc
    finally:
        if sys.path and sys.path[0] == src:
            sys.path.pop(0)


def _base_manifest(acp: Any, recipe_class: str, run_id: str) -> dict[str, Any]:
    if recipe_class == "normal_completion":
        plane = acp.ControlPlane(run_id=run_id)
        plane.register("work", lambda _task: "ok")
        plane.dispatch("work", acp.Task(payload="work", id="task-1"))
        return plane.provenance_manifest()

    if recipe_class == "policy_denial":
        plane = acp.ControlPlane(policy=lambda _capability, _task: "policy denied", run_id=run_id)
        plane.register("work", lambda _task: "unused")
        plane.dispatch("work", acp.Task(payload="work", id="task-1"))
        return plane.provenance_manifest()

    if recipe_class == "unknown_capability_rejection":
        plane = acp.ControlPlane(run_id=run_id)
        try:
            plane.dispatch("missing", acp.Task(payload="work", id="task-1"))
        except KeyError:
            pass
        return plane.provenance_manifest()

    if recipe_class == "handler_failure":
        plane = acp.ControlPlane(run_id=run_id)

        def fail_handler(_task: Any) -> None:
            raise RuntimeError("boom")

        plane.register("work", fail_handler)
        plane.dispatch("work", acp.Task(payload="work", id="task-1"))
        return plane.provenance_manifest()

    if recipe_class == "cancellation":
        plane = acp.ControlPlane(run_id=run_id)
        plane.cancel(acp.Task(payload="work", id="task-1"))
        return plane.provenance_manifest()

    if recipe_class == "exact_budget_success":
        plane = acp.ControlPlane(run_id=run_id)

        def exact_handler(task: Any) -> str:
            task.consume(steps=2, tool_calls=1, tokens=100, cost=0.25)
            return "ok"

        plane.register("work", exact_handler)
        budget = acp.ExecutionBudget(max_steps=2, max_tool_calls=1, max_tokens=100, max_cost=0.25)
        plane.dispatch("work", acp.Task(payload="work", id="task-1", budget=budget))
        return plane.provenance_manifest()

    if recipe_class == "budget_exhaustion":
        plane = acp.ControlPlane(run_id=run_id)

        def budget_handler(task: Any) -> None:
            task.consume(steps=2)

        plane.register("work", budget_handler)
        plane.dispatch(
            "work",
            acp.Task(payload="work", id="task-1", budget=acp.ExecutionBudget(max_steps=1)),
        )
        return plane.provenance_manifest()

    if recipe_class == "suppressed_budget_exception_fail_closed":
        plane = acp.ControlPlane(run_id=run_id)

        def suppressing_handler(task: Any) -> str:
            try:
                task.consume(tool_calls=1)
            except acp.BudgetExceeded:
                return "suppressed"
            return "unexpected"

        plane.register("work", suppressing_handler)
        plane.dispatch(
            "work",
            acp.Task(payload="work", id="task-1", budget=acp.ExecutionBudget(max_tool_calls=0)),
        )
        return plane.provenance_manifest()

    _fail("SOURCE_DRIVER_BASE_RECIPE_UNSUPPORTED")


def _transform(recipe_class: str, manifest: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
    transformed = copy.deepcopy(manifest)
    if recipe_class not in _BASE_RECIPE:
        return transformed, None

    events = transformed["events"]
    if recipe_class == "missing_event":
        transformed["events"] = events[:1]
    elif recipe_class == "reordered_exported_events":
        transformed["events"] = list(reversed(events))
    elif recipe_class == "duplicate_replayed_event":
        transformed["events"] = [events[0], copy.deepcopy(events[0]), *events[1:]]
    elif recipe_class == "stale_timestamp":
        for index, event in enumerate(events):
            event["timestamp"] = f"2025-01-01T00:00:0{index}+00:00"
    elif recipe_class == "malformed_manifest":
        transformed["schema"] = "agent-control-plane.provenance.v999"
        transformed["events"] = events[:1]
    elif recipe_class == "mismatched_run_id":
        transformed["events"] = events[:1]
        transformed["events"][0]["run_id"] = "other-run"
    elif recipe_class == "source_order_ambiguity":
        if len(events) >= 2:
            events[1]["timestamp"] = events[0]["timestamp"]
    elif recipe_class == "missing_authority_evidence":
        pass
    transformed["event_count"] = len(transformed["events"])
    return transformed, f"POST_EXPORT_{recipe_class.upper()}"


def execute_recipe(acp_root: Path, recipe_class: str, *, run_id: str) -> dict[str, Any]:
    if recipe_class not in RECIPE_CLASSES:
        _fail("SOURCE_DRIVER_RECIPE_NOT_FROZEN")
    if not run_id.strip():
        _fail("SOURCE_DRIVER_RUN_ID_MISSING")

    acp = _load_frozen_acp(Path(acp_root))
    base = _BASE_RECIPE.get(recipe_class, recipe_class)
    raw_manifest = _base_manifest(acp, base, run_id)
    raw_bytes = _canonical_bytes(raw_manifest)
    exported, transform = _transform(recipe_class, raw_manifest)
    export_bytes = _canonical_bytes(exported)

    return {
        "record_type": "AOSS_V0_6_STAGE_A_SOURCE_DRIVER_RESULT",
        "status": "IMPLEMENTATION_CANDIDATE_NOT_ACCEPTED",
        "recipe_version": RECIPE_VERSION,
        "recipe_class": recipe_class,
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": SOURCE_COMMIT,
        "source_module": SOURCE_MODULE,
        "source_module_blob": SOURCE_MODULE_BLOB,
        "raw_manifest": raw_manifest,
        "raw_manifest_sha256": _sha256(raw_bytes),
        "post_export_transformation": transform,
        "export_manifest": exported,
        "export_manifest_sha256": _sha256(export_bytes),
        "observer_executed": False,
        "collection_authorized": False,
        "scientific_n_increment": 0,
    }


def write_result_exclusive(result: dict[str, Any], destination: Path) -> str:
    data = _canonical_bytes(result)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise SourceDriverError("SOURCE_DRIVER_DESTINATION_EXISTS") from exc
    return _sha256(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--acp-root", required=True, type=Path)
    parser.add_argument("--recipe-class", required=True, choices=RECIPE_CLASSES)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)

    result = execute_recipe(args.acp_root, args.recipe_class, run_id=args.run_id)
    digest = write_result_exclusive(result, args.output)
    print(json.dumps({"status": "WRITTEN_CANDIDATE_NOT_ADMITTED", "sha256": digest}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
