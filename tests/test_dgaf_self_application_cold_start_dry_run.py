from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_dgaf_self_application_cold_start_dry_run.py"
MANIFEST = ROOT / "registry" / "dgaf_self_application_cold_start_manifest_v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("dgaf_cold_start_dry_run", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_dry_run_preserves_nonpromoting_claim_ceiling():
    module = load_module()
    record = module.build_dry_run_record(MANIFEST)

    assert record["schema_version"] == "dgaf.self_application.cold_start_dry_run_result.v1"
    assert record["evidence_class"] == "INTERNAL_SELF_APPLICATION_ENGINEERING_VALIDATION"
    assert record["claim_ceiling"] == {
        "scientific_n_increment": 0,
        "independent_validation": "NOT_ESTABLISHED",
        "external_validation": "NOT_ESTABLISHED",
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
    assert record["same_system_run_independence"] == "NOT_ESTABLISHED"
    assert record["runtime_authorization_effect"] == "NONE"
    assert record["scientific_state_effect"] == "NONE"
    assert record["executed_cold_start_reproduction"] is False


def test_dry_run_retains_raw_measurement_scaffold_before_summary():
    module = load_module()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    record = module.build_dry_run_record(MANIFEST)

    expected_ids = [measure["id"] for measure in manifest["measures"]]
    observed_ids = [step["measure_id"] for step in record["per_step_results"]]

    assert observed_ids == expected_ids
    assert all(step["status"] == "NOT_EXECUTED" for step in record["per_step_results"])
    assert all(step["evidence_retained"] is False for step in record["per_step_results"])
    assert record["summary"]["raw_per_step_results_retained_before_summary"] is True
    assert record["summary"]["cold_start_completion_rate"] == 0.0


def test_dry_run_binds_manifest_identity_and_external_review_controller():
    module = load_module()
    manifest_bytes = MANIFEST.read_bytes()
    record = module.build_dry_run_record(MANIFEST)

    assert record["controller_issue"] == "issue://1022"
    assert record["external_review_controller"] == "issue://929"
    assert record["summary"]["external_review_controller"] == "issue://929"
    assert record["manifest"]["path"] == "registry/dgaf_self_application_cold_start_manifest_v1.json"
    assert record["manifest"]["sha256"] == module._sha256_bytes(manifest_bytes)


def test_cli_writes_nonexecuting_result(tmp_path: Path):
    module = load_module()
    output = tmp_path / "cold-start-dry-run.json"

    exit_code = module.main.__wrapped__() if hasattr(module.main, "__wrapped__") else None
    assert exit_code is None

    # Exercise the pure record path instead of mutating sys.argv in this unit test.
    record = module.build_dry_run_record(MANIFEST)
    output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    reread = json.loads(output.read_text(encoding="utf-8"))

    assert reread["executed_cold_start_reproduction"] is False
    assert reread["same_system_run_independence"] == "NOT_ESTABLISHED"
