from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "p9-final-frozen-chain.yml"


def _workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_p9_dispatch_binds_separate_freeze_and_p8_verification_commits() -> None:
    text = _workflow_text()
    assert "freeze_commit_sha:" in text
    assert "p8_verification_commit_sha:" in text
    assert "p8_verification_sha256:" in text
    assert 'test "$FREEZE_COMMIT_SHA" != "$REQUESTED_VERIFICATION_SHA"' in text


def test_p9_requires_freeze_ancestry_and_frozen_verifier_identity() -> None:
    text = _workflow_text()
    assert 'git merge-base --is-ancestor "$FREEZE_COMMIT_SHA" "$P8_VERIFICATION_COMMIT_SHA"' in text
    assert 'git show "$FREEZE_COMMIT_SHA:scripts/verify_p9_frozen_chain.py"' in text
    assert 'git show "$FREEZE_COMMIT_SHA:.github/workflows/p9-final-frozen-chain.yml"' in text
    assert 'test "$frozen_script_sha" = "$current_script_sha"' in text
    assert 'test "$frozen_workflow_sha" = "$current_workflow_sha"' in text


def test_p9_resolves_candidate_and_p7_from_freeze_commit() -> None:
    text = _workflow_text()
    assert 'git show "$FREEZE_COMMIT_SHA:$CANDIDATE_MANIFEST"' in text
    assert 'git show "$FREEZE_COMMIT_SHA:$P7_BINDING"' in text
    assert "--candidate-manifest /tmp/p9-frozen/NEW_CANDIDATE_MANIFEST.md" in text
    assert "--p7-binding /tmp/p9-frozen/P7_FINAL_BINDING.md" in text


def test_p9_binds_frozen_verifier_hashes_to_final_p7() -> None:
    text = _workflow_text()
    assert "--p9-verifier-script-sha256" in text
    assert '"$FROZEN_SCRIPT_SHA256"' in text
    assert "--p9-workflow-sha256" in text
    assert '"$FROZEN_WORKFLOW_SHA256"' in text


def test_p9_registry_keeps_authorization_and_empirical_state_closed() -> None:
    text = _workflow_text()
    assert "'pilot_authorization': 'NOT_GRANTED'" in text
    assert "'empirical_n': 0" in text
    assert "GITHUB_ACTIONS_30_DAY_NOT_DURABLE_CUSTODY" in text
