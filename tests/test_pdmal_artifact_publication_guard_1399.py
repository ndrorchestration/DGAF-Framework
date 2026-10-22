"""Fail-closed structural-artifact publication contract, issue #1399.

Static/non-executing guard tests: do NOT dispatch PDMAL, fetch artifacts, or
load the real PDMAL_BLINDING_KEY. They are regression guards, not authorization
or proof of an independently accepted analyst/custody threat model.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "pdmal-instrumentation-dry-run.yml"
GUARD = "      - name: Block unapproved structural artifact publication (#1399)"
NEXT = "      - name: Checkout control plane for candidate resolution"
UPLOAD = "      - name: Upload dry-run artifacts"


def _assert_fail_closed_publication_contract(source: str) -> None:
    """A future run must stop before any checkout, secret use or artifact upload."""
    assert source.count(GUARD) == 1
    assert source.count(NEXT) == 1
    assert source.count(UPLOAD) == 1
    assert source.index(GUARD) < source.index(NEXT) < source.index(UPLOAD)
    guard = source.split(GUARD, 1)[1].split(NEXT, 1)[0]
    assert "PDMAL_REPO_PRIVATE: ${{ github.event.repository.private }}" in guard
    assert 'if [ "$PDMAL_REPO_PRIVATE" != "true" ]; then' in guard
    assert "::error::PDMAL masked structural artifact publication is blocked in a public repository" in guard
    assert "::error::PDMAL masked structural artifact custody/audience decision is not independently approved" in guard
    assert guard.count("exit 1") == 2
    assert guard.count('echo "::error::') == 2
    assert "set -euo pipefail" in guard
    assert "\n        if:" not in guard
    assert "\n      - uses:" not in guard
    assert "upload-artifact" not in guard
    assert "PDMAL_BLINDING_KEY" not in guard
    assert "workflow_dispatch:" in source
    assert "pull_request:" in source
    assert "push:" in source
    assert "retention-days: 14" in source
    secret_binding = "PDMAL_BLINDING_KEY: ${{ secrets.PDMAL_BLINDING_KEY }}"
    assert source.count(secret_binding) == 2
    job_header = source.split("    steps:", 1)[0]
    assert "PDMAL_BLINDING_KEY" not in job_header
    fail_fast = source.split("      - name: Fail fast if blinding secret is unavailable", 1)[1].split(
        "      - name: Run deterministic smoke case twice", 1
    )[0]
    generate = source.split("      - name: Generate one-seed masked dry-run CSV", 1)[1].split(
        "      - name: Validate dry-run CSV schema", 1
    )[0]
    assert secret_binding in fail_fast
    assert secret_binding in generate


def test_pdmal_dry_run_blocks_all_unapproved_artifact_production_before_processing() -> None:
    _assert_fail_closed_publication_contract(WORKFLOW.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    ("before", "after"),
    [
        (
            "PDMAL_REPO_PRIVATE: ${{ github.event.repository.private }}",
            "PDMAL_REPO_PRIVATE: 'true'",
        ),
        (
            'if [ "$PDMAL_REPO_PRIVATE" != "true" ]; then',
            'if [ "$PDMAL_REPO_PRIVATE" = "true" ]; then',
        ),
        (
            'echo "::error::PDMAL masked structural artifact publication is blocked in a public repository',
            'echo "unrestricted repository publication"',
        ),
        (
            'echo "::error::PDMAL masked structural artifact custody/audience decision is not independently approved',
            'echo "custody independently approved"',
        ),
        ("          exit 1", "          exit 0"),
        ("          exit 1", "          :"),
        ("          set -euo pipefail", "          set +e"),
    ],
)
def test_guard_rejects_dangerous_policy_mutations(before: str, after: str) -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert before in source
    with pytest.raises(AssertionError):
        _assert_fail_closed_publication_contract(source.replace(before, after, 1))


def test_guard_cannot_be_moved_after_sensitive_upload() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    prefix = source.split(GUARD, 1)[0]
    body_and_remainder = source.split(GUARD, 1)[1]
    block, after = body_and_remainder.split(NEXT, 1)
    malformed = prefix + NEXT + after
    malformed = malformed.replace(UPLOAD, GUARD + block + UPLOAD, 1)
    with pytest.raises(AssertionError):
        _assert_fail_closed_publication_contract(malformed)


def test_guard_cannot_be_silently_skipped() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert GUARD in source
    malformed = source.replace(GUARD, GUARD + "\n        if: false", 1)
    with pytest.raises(AssertionError):
        _assert_fail_closed_publication_contract(malformed)
