"""Classify externally effectful/empirical execution workflows without admitting them as audits.

These checks inspect repository source. They never dispatch a workflow, use a
blinding key, create a Rekor entry, or authorize experimental execution.
"""

from pathlib import Path

import pytest

from registry.audit_catalog import (
    collect_unclassified_workflows,
    collect_workflow_classification_violations,
    load_catalog,
    load_workflow_classification,
)

ROOT = Path(__file__).resolve().parents[1]
REKOR = ".github/workflows/p4-mode-t-rekor-timing.yml"
EPOCH = ".github/workflows/canonical-epoch-004-execution.yml"
CLASSES = {
    REKOR: "CONTROLLED_EXTERNAL_SIDE_EFFECT_EXPERIMENT_INSTANCE",
    EPOCH: "EXPERIMENT_EPOCH_WORKFLOW_INSTANCE",
}


def _assert_no_automatic_public_rekor_effect(text: str) -> None:
    trigger = text.split("\npermissions:\n", 1)[0]
    assert "\non:\n  workflow_dispatch:\n" in trigger
    assert all(token not in trigger for token in ("\n  push:", "\n  pull_request:", "\n  schedule:"))
    assert "default: 'NO'" in trigger
    assert "I_UNDERSTAND_PUBLIC_REKOR_ENTRY" in trigger
    assert "needs: validate-apparatus" in text
    validate_job, public_job = text.split("\n  execute-public-rekor:\n", 1)
    assert "if: ${{ inputs.confirm_public_rekor_entry == 'I_UNDERSTAND_PUBLIC_REKOR_ENTRY' }}" in public_job
    assert 'test "$EVIDENCE_SHA" = "$GITHUB_SHA"' in validate_job
    assert 'test "$EVIDENCE_SHA" = "$GITHUB_SHA"' in public_job
    assert "test \"$GITHUB_RUN_ATTEMPT\" = '1'" in public_job
    assert "id-token: write" in public_job
    assert "e['public_transparency_side_effect'] is True" in text
    assert "e['empirical_n'] == 0" in text


def _assert_bounded_epoch_custody(text: str) -> None:
    trigger = text.split("\npermissions:\n", 1)[0]
    assert "\n  pull_request:\n" in trigger
    assert "\n  push:\n" in trigger
    assert "solo-canonical-epoch-004/run-*" in trigger
    assert "branches:\n      - main" not in trigger
    assert "validate-runner-only:" in text
    assert "if: github.event_name == 'pull_request'" in text
    assert "execute-blinded-epoch:" in text
    assert "if: github.event_name == 'push'" in text
    assert "CANONICAL_EPOCH_004_RUNNER_PR_VALIDATION_NONEMPIRICAL_PASS" in text
    assert '"${changed[0]}" != "docs/experiment/solo_runs/CANONICAL_EPOCH_004_RUN_REQUEST.json"' in text
    assert "PDMAL_UNBLINDING_AUTHORIZED: '0'" in text
    assert "'authorize_unblinding': False" in text
    assert "'blinding_key_custody': 'SAME_SYSTEM_GITHUB_ACTIONS_ARTIFACT_NONINDEPENDENT'" in text
    assert "name: canonical-epoch-004-dataset-${{ github.sha }}" in text
    assert "name: canonical-epoch-004-blinding-key-${{ github.sha }}" in text
    assert "retention-days: 90" in text


def test_execution_workflows_classified_as_non_audit_instances() -> None:
    classified = load_workflow_classification(ROOT / "registry/workflow_classification.v1.json")
    catalog = load_catalog(ROOT / "registry/audit_catalog.v1.json")
    assert collect_workflow_classification_violations(classified) == []
    rows = {row["path"]: row for row in classified["classifications"]}
    for path, kind in CLASSES.items():
        row = rows[path]
        assert row["classification"] == "CLASSIFIED_NON_AUDIT"
        assert row["kind"] == kind
        assert row["lifecycle"] == "CURRENT"
        assert row["controller"].strip()
        assert row["decision_effect"].strip()
        assert row["reason"].strip()
    assert CLASSES.keys().isdisjoint({path for row in catalog["audits"] for path in row["implementation"]})
    assert CLASSES.keys().isdisjoint(collect_unclassified_workflows(ROOT, catalog, classified))


def test_source_guards_match_execution_classification() -> None:
    _assert_no_automatic_public_rekor_effect((ROOT / REKOR).read_text(encoding="utf-8"))
    _assert_bounded_epoch_custody((ROOT / EPOCH).read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    ("workflow", "original", "mutated"),
    [
        (REKOR, "default: 'NO'", "default: 'I_UNDERSTAND_PUBLIC_REKOR_ENTRY'"),
        (REKOR, "if: ${{ inputs.confirm_public_rekor_entry == 'I_UNDERSTAND_PUBLIC_REKOR_ENTRY' }}", "if: ${{ true }}"),
        (REKOR, 'test "$EVIDENCE_SHA" = "$GITHUB_SHA"', 'echo "$GITHUB_SHA"'),
        (REKOR, "test \"$GITHUB_RUN_ATTEMPT\" = '1'", 'echo "$GITHUB_RUN_ATTEMPT"'),
        (REKOR, "e['public_transparency_side_effect'] is True", "pass  # no public-effect assertion"),
        (EPOCH, "solo-canonical-epoch-004/run-*", "main"),
        (
            EPOCH,
            '"${changed[0]}" != "docs/experiment/solo_runs/CANONICAL_EPOCH_004_RUN_REQUEST.json"',
            '"${changed[0]}" != "docs/experiment/solo_runs/ANY_RUN_REQUEST.json"',
        ),
        (EPOCH, "if: github.event_name == 'push'", "if: github.event_name == 'pull_request'"),
        (EPOCH, "PDMAL_UNBLINDING_AUTHORIZED: '0'", "PDMAL_UNBLINDING_AUTHORIZED: '1'"),
        (EPOCH, "'authorize_unblinding': False", "'authorize_unblinding': True"),
        (
            EPOCH,
            "name: canonical-epoch-004-blinding-key-${{ github.sha }}",
            "name: canonical-epoch-004-dataset-${{ github.sha }}",
        ),
    ],
)
def test_classification_source_guard_rejects_authority_boundary_mutations(
    workflow: str, original: str, mutated: str
) -> None:
    source = (ROOT / workflow).read_text(encoding="utf-8")
    assert source.count(original) == (2 if original == 'test "$EVIDENCE_SHA" = "$GITHUB_SHA"' else 1)
    corrupt = source.replace(original, mutated, 1)
    with pytest.raises(AssertionError):
        if workflow == REKOR:
            _assert_no_automatic_public_rekor_effect(corrupt)
        else:
            _assert_bounded_epoch_custody(corrupt)


def test_public_rekor_execution_job_requires_its_own_sha_binding() -> None:
    source = (ROOT / REKOR).read_text(encoding="utf-8")
    check = 'test "$EVIDENCE_SHA" = "$GITHUB_SHA"'
    assert source.count(check) == 2
    corrupt = source.rsplit(check, 1)
    assert len(corrupt) == 2
    with pytest.raises(AssertionError):
        _assert_no_automatic_public_rekor_effect('echo "$GITHUB_SHA"'.join(corrupt))
