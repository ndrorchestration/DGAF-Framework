from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "dgaf-cold-start-scaffold-artifact.yml"


def test_cold_start_scaffold_artifact_workflow_preserves_non_promoting_boundary():
    text = WORKFLOW.read_text(encoding="utf-8")

    required_snippets = [
        "name: DGAF Cold-Start Scaffold Artifact",
        "workflow_dispatch:",
        "pull_request:",
        "ref: ${{ github.event.pull_request.head.sha || github.sha }}",
        "persist-credentials: false",
        "python scripts/materialize_dgaf_self_application_cold_start_scaffold.py",
        "cold_start_scaffold_materialization_summary.json",
        "cold_start_execution_record.json",
        "cold_start_execution_record_validation_result.json",
        "executed_cold_start_reproduction",
        "scientific_state_effect",
        "runtime_authorization_effect",
        "canonical_dgaf_efficacy",
        "high_assurance",
        "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4",
        "dgaf-cold-start-scaffold-${{ github.sha }}",
        "if-no-files-found: error",
    ]
    for snippet in required_snippets:
        assert snippet in text

    prohibited_snippets = [
        "scientific_n_increment: 1",
        "INDEPENDENT_VALIDATION_ESTABLISHED",
        "EXTERNAL_VALIDATION_ESTABLISHED",
        "HIGH_ASSURANCE_AUTHORIZED",
    ]
    for snippet in prohibited_snippets:
        assert snippet not in text
