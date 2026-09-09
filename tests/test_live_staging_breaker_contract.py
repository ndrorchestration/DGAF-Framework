from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = ROOT / "pages" / "api" / "staging-breaker.ts"
WORKFLOW = ROOT / ".github" / "workflows" / "live-staging-breaker.yml"
DEPLOY = ROOT / ".github" / "workflows" / "deploy.yml"
DOC = ROOT / "docs" / "governance" / "LIVE_STAGING_BREAKER_EVIDENCE_CONTRACT.md"


def test_endpoint_is_preview_only_and_fixed_threshold() -> None:
    text = ENDPOINT.read_text(encoding="utf-8")
    assert "process.env.VERCEL_ENV !== 'preview'" in text
    assert "DGAF_STAGING_BREAKER_EXERCISE_ENABLED" in text
    assert "x-dgaf-staging-exercise-id" in text
    assert "const BREAKER_THRESHOLD = 0.8" in text
    assert "const INJECTED_FAULT_SCORE = 0.95" in text
    assert "PASS_STRUCTURAL_LIVE_STAGING_ONLY" in text
    assert "protected_or_empirical_material_used: false" in text
    assert "scientific_state_effect: 'NONE'" in text
    assert "canonical_dgaf_efficacy: 'NOT_ESTABLISHED'" in text


def test_preview_workflow_exact_source_and_attempt_binding() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "pull_request:" in text
    assert "SOURCE_SHA:" in text
    assert "github.event.pull_request.head.sha || github.sha" in text
    assert "Prove checkout is exact source" in text
    assert "--target=preview" in text
    assert "--env DGAF_STAGING_BREAKER_EXERCISE_ENABLED=true" in text
    assert "--env DGAF_STAGING_BREAKER_EXERCISE_ID" in text
    assert 'test "$target" != production' in text
    assert 'test "$source" = "$SOURCE_SHA"' in text
    assert 'exercise_id="${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}-${SOURCE_SHA}"' in text
    assert "STAGING -> ACTIVE -> BREAKER_OPEN -> FROZEN -> ROLLBACK -> VERIFIED" in text
    assert "post_rollback_health" in text
    assert "live_staging_breaker_evidence.json.sha256" in text


def test_production_deploy_has_negative_control() -> None:
    text = DEPLOY.read_text(encoding="utf-8")
    assert "Prove staging breaker is unavailable in production" in text
    assert "production-must-reject" in text
    assert 'test "$status" = 404' in text
    assert "NOT_AVAILABLE" in text


def test_documentation_refuses_persistent_production_claim() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "does not prove" in text
    assert "persistent distributed breaker state across serverless instances" in text
    assert "does not establish a persistent production breaker implementation" in text
    assert "PASS_STRUCTURAL_LIVE_STAGING_ONLY" in text
