from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "dgaf-cold-start-same-system-execution-artifact.yml"


def test_cold_start_same_system_execution_artifact_workflow_preserves_non_promoting_boundary():
    assert WORKFLOW.exists()
    text = WORKFLOW.read_text(encoding="utf-8")

    required_snippets = [
        "name: DGAF Cold-Start Same-System Execution Artifact",
        "workflow_dispatch:",
        "pull_request:",
        "ref: ${{ github.event.pull_request.head.sha || github.sha }}",
        "persist-credentials: false",
        "python scripts/run_dgaf_self_application_cold_start_same_system_execution.py",
        "cold_start_same_system_execution_summary.json",
        "cold_start_execution_record.json",
        "cold_start_execution_record_validation_result.json",
        "schema_version",
        "dgaf.self_application.cold_start_same_system_execution.v1",
        "executed_cold_start_reproduction",
        "same_system_run_independence",
        "scientific_state_effect",
        "runtime_authorization_effect",
        "canonical_dgaf_efficacy",
        "high_assurance",
        "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4",
        "dgaf-cold-start-same-system-execution-${{ github.sha }}",
        "if-no-files-found: error",
    ]
    for snippet in required_snippets:
        assert snippet in text

    prohibited_snippets = [
        "scientific_n_increment: 1",
        "INDEPENDENT_VALIDATION_ESTABLISHED",
        "EXTERNAL_VALIDATION_ESTABLISHED",
        "HIGH_ASSURANCE_AUTHORIZED",
        "same_system_run_independence: ESTABLISHED",
    ]
    for snippet in prohibited_snippets:
        assert snippet not in text
