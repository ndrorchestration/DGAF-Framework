import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "scripts/aoss_stage_a/source_driver.py"
GROUND_TRUTH = ROOT / "registry/aoss_v0_6_stage_a_failure_ground_truth_v1.json"
CATALOG = ROOT / "registry/aoss_v0_6_stage_a_source_driver_recipe_catalog_v1.json"

EXPECTED_TRANSFORMS = {
    "normal_completion": ("normal_completion", None),
    "policy_denial": ("policy_denial", None),
    "unknown_capability_rejection": ("unknown_capability_rejection", None),
    "handler_failure": ("handler_failure", None),
    "cancellation": ("cancellation", None),
    "exact_budget_success": ("exact_budget_success", None),
    "budget_exhaustion": ("budget_exhaustion", None),
    "suppressed_budget_exception_fail_closed": (
        "suppressed_budget_exception_fail_closed",
        None,
    ),
    "missing_event": ("normal_completion", "drop_terminal_event"),
    "reordered_exported_events": ("normal_completion", "reverse_events"),
    "duplicate_replayed_event": ("normal_completion", "duplicate_first_event"),
    "stale_timestamp": ("normal_completion", "inject_stale_timestamps"),
    "malformed_manifest": ("normal_completion", "unsupported_schema"),
    "mismatched_run_id": ("normal_completion", "mismatch_event_run_id"),
    "source_order_ambiguity": ("normal_completion", "equalize_event_timestamps"),
    "missing_authority_evidence": ("normal_completion", None),
}


def _tree():
    return ast.parse(DRIVER.read_text(encoding="utf-8"), filename=str(DRIVER))


def _assignment(tree, name):
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == name for target in targets):
                return ast.literal_eval(node.value)
    raise AssertionError(f"missing assignment: {name}")


def test_driver_source_is_exactly_bound_without_importing_it():
    tree = _tree()
    assert _assignment(tree, "SOURCE_REPOSITORY") == "ndrorchestration/agent-control-plane"
    assert _assignment(tree, "SOURCE_COMMIT") == "dbab7c1afafec524ce7c18157de2089cafe79c87"
    assert _assignment(tree, "SOURCE_CORE_BLOB") == "1341df7296a426b336b76ac6b1e4df67611ec931"
    assert _assignment(tree, "DRIVER_STATUS") == "IMPLEMENTED_NOT_ADMITTED"
    assert _assignment(tree, "RECIPE_CATALOG_SHA256") == (
        "b3c0d883cd9463ec558ee8a3fab3376641b2603eb474a745c119a28d1cd15d77"
    )


def test_driver_has_no_direct_acp_or_execution_loader_imports():
    tree = _tree()
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")

    assert all(not name.startswith("agent_control_plane") for name in imported)
    assert imported.isdisjoint({"subprocess", "importlib", "os", "sys", "pathlib"})
    assert imported <= {
        "__future__",
        "copy",
        "hashlib",
        "json",
        "dataclasses",
        "typing",
    }


def test_all_frozen_recipe_classes_are_implemented_with_declared_transforms():
    tree = _tree()
    specs = _assignment(tree, "RECIPE_SPECS")
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    ground = json.loads(GROUND_TRUTH.read_text(encoding="utf-8"))

    catalog_events = {item["class"]: item["synthetic_terminal_event"] for item in catalog["recipes"]}
    assert set(specs) == set(EXPECTED_TRANSFORMS) == set(catalog_events) == set(ground["labels"])

    for name, (native_operation, transform) in EXPECTED_TRANSFORMS.items():
        assert specs[name]["native_operation"] == native_operation
        assert specs[name]["transform"] == transform
        assert specs[name]["expected_terminal_event"] == ground["labels"][name]["terminal_event"]
        assert specs[name]["expected_terminal_event"] == catalog_events[name]


def test_source_driver_implementation_surface_exists_but_has_no_cli_entrypoint():
    tree = _tree()
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert {
        "recipe_spec",
        "_run_native",
        "_apply_transform",
        "generate_source_episode",
    } <= set(functions)
    assert "main" not in functions

    source = DRIVER.read_text(encoding="utf-8")
    assert "if __name__" not in source
    assert "subprocess" not in source
    assert "importlib" not in source


def test_native_and_transform_branches_cover_every_declared_operation():
    tree = _tree()
    strings = {node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, str)}
    native_operations = {value[0] for value in EXPECTED_TRANSFORMS.values()}
    transforms = {value[1] for value in EXPECTED_TRANSFORMS.values() if value[1] is not None}

    assert native_operations <= strings
    assert transforms <= strings
    assert "SOURCE_DRIVER_NATIVE_OPERATION_NOT_FROZEN" in strings
    assert "SOURCE_DRIVER_TRANSFORM_NOT_FROZEN" in strings


def test_candidate_source_does_not_claim_admission_or_outcomes():
    source = DRIVER.read_text(encoding="utf-8")
    normalized = " ".join(source.split())
    assert "IMPLEMENTED_NOT_ADMITTED" in source
    assert "caller must not inject ACP until the separate environment" in normalized
    assert "accepted-study" not in source
    assert "INDEPENDENT_VALIDATION=ESTABLISHED" not in source
    assert "HIGH_ASSURANCE=AUTHORIZED" not in source
