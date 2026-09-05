from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCEDURE = ROOT / "docs/governance/P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md"
P7 = ROOT / "docs/governance/P7_FINAL_BINDING_DRAFT_2026-09-05.md"
P8 = ROOT / "docs/governance/P8_VERIFICATION_CHECKLIST.md"
LEGACY = ROOT / "docs/governance/P4_HUMAN_KEY_CUSTODY_PROCEDURE.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_canonical_p4_procedure_declares_effective_control_invariant():
    text = _read(PROCEDURE)
    assert "effective control separation" in text
    assert "unable to obtain the raw blinding key" in text
    assert "unilateral action" in text
    assert "Mode H" in text
    assert "Mode I" in text
    assert "Mode T" in text


def test_p4_rejects_same_operator_and_ai_pseudo_separation():
    text = _read(PROCEDURE)
    required = [
        "AI agent",
        "repository secret",
        "password-manager vault",
        "break-glass",
        "preregistration alone",
    ]
    for phrase in required:
        assert phrase in text


def test_p7_consumes_custody_mode_not_mandatory_second_human():
    text = _read(P7)
    assert "P4 custody mode" in text
    assert "exactly one of `H`, `I`, `T`" in text
    assert "A second human is therefore not mandatory" in text
    assert "p4_custody_mode: null" in text
    assert "empirical_n: 0" in text


def test_p8_remains_fail_closed_until_real_custody_is_instantiated():
    text = _read(P8)
    assert "P4 remains **OPEN / PROCEDURE REVISED / OPERATION NOT EXECUTED**" in text
    assert "Freeze NOT ESTABLISHED" in text
    assert "Pilot authorization NOT GRANTED" in text
    assert "Empirical N = 0" in text


def test_legacy_human_path_is_compatibility_mode_not_canonical_gate():
    text = _read(LEGACY)
    assert "SUPERSEDED AS CANONICAL PROCEDURE" in text
    assert "Mode H" in text
    assert "it is no longer the only permitted topology" in text
