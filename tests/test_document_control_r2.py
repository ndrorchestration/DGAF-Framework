import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_document_control_r2.py"
spec = importlib.util.spec_from_file_location("document_control_r2", MODULE_PATH)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def registry():
    return json.loads((ROOT / "docs/governance/document-control-r2.json").read_text(encoding="utf-8"))


def assert_invalid(data, needle):
    try:
        mod.validate(data)
    except ValueError as exc:
        assert needle in str(exc)
    else:
        raise AssertionError("expected fail-closed rejection")


def test_current_registry_passes():
    mod.validate(registry())


def test_registered_historical_sources_are_exact_issue_605_cases():
    refs = {r["owner"]["authority_ref"] for r in registry()["records"]}
    assert refs == {
        "docs/governance/DYNAMIC_FREEZE_ADMISSIBILITY_CONTROL_2026-08-26.md",
        "docs/GOVERNANCE/2026-09-03_CURRENT_EVIDENCE_EXECUTION.md",
        "docs/GOVERNANCE/P9_SECOND_PASS_2026-08-30.md",
    }


def test_historical_record_cannot_route_to_itself_as_current():
    data = registry()
    record = data["records"][0]
    record["current_state_ref"] = record["owner"]["authority_ref"]
    assert_invalid(data, "routes to itself as current")


def test_missing_source_fails_closed():
    data = registry()
    data["records"][0]["owner"]["authority_ref"] = "docs/does-not-exist.md"
    assert_invalid(data, "owner source is missing")


def test_missing_current_authority_target_fails_closed():
    data = registry()
    data["records"][0]["current_state_ref"] = "docs/missing-current.md"
    assert_invalid(data, "current_state_ref is missing")


def test_not_verified_timestamp_is_rejected():
    data = registry()
    data["records"][0]["last_verified_at"] = "2026-09-10T00:00:00Z"
    assert_invalid(data, "non-VERIFIED projection carries last_verified_at")


def test_superseded_without_route_or_terminal_reason_is_rejected():
    data = registry()
    record = data["records"][0]
    record["record_class"] = "SUPERSEDED"
    record["superseded_by"] = []
    record["terminal_reason"] = None
    assert_invalid(data, "SUPERSEDED requires superseded_by or terminal_reason")


def test_conflicting_current_authorities_for_same_scope_are_rejected():
    data = registry()
    a = data["records"][0]
    a["record_class"] = "CURRENT_AUTHORITY"
    a["projection_state"] = "VERIFIED"
    a["last_verified_at"] = "2026-09-10T00:00:00Z"
    b = copy.deepcopy(a)
    b["record_id"] = "conflicting-current-authority"
    data["records"].append(b)
    assert_invalid(data, "conflicting CURRENT_AUTHORITY projections")


def test_path_traversal_is_rejected():
    data = registry()
    data["records"][0]["owner"]["authority_ref"] = "../outside.md"
    assert_invalid(data, "path escapes repository")
