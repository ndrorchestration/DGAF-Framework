from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATE = ROOT / "pages" / "api" / "orchestrate.ts"
SWEEP = ROOT / "pages" / "api" / "sweep.ts"


def test_orchestrate_does_not_encode_placeholder_checkpoint_as_pass():
    text = ORCHESTRATE.read_text(encoding="utf-8")
    forbidden = (
        "phi_delta = Math.abs(PHI_STAR - PHI_STAR)",
        "phi_delta = 0",
        "audit_state: 'NOT_WIRED', phi_delta",
    )
    assert not any(marker in text for marker in forbidden), (
        "orchestrate.ts still contains a hardcoded Phi checkpoint success path; "
        "replace it with a real audit-state evaluation or fail closed"
    )


def test_sweep_does_not_claim_mutation_or_fabricate_harmonic_score():
    text = SWEEP.read_text(encoding="utf-8")
    assert "mutation_performed: false" in text
    assert "harmonic_score: null" in text
    assert "harmonic_score_status: 'NOT_COMPUTED'" in text
    assert "[PLAN ONLY]" in text
