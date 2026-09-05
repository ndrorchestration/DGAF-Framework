from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THREAT_MODEL = ROOT / "docs/governance/P4_MODE_T_SOLO_CUSTODY_THREAT_MODEL_2026-09-05.md"
EVIDENCE = ROOT / "docs/governance/P4_MODE_T_EXTERNAL_ASSUMPTIONS_EVIDENCE_2026-09-05.md"
P4 = ROOT / "docs/governance/P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_mode_t_design_keeps_secret_instantiation_post_authorization():
    text = _read(THREAT_MODEL)
    assert "P4-T-A — mechanism closure, pre-freeze" in text
    assert "No real key, mapping, commitment nonce, or empirical workload exists." in text
    assert "P4-T-X — custody instantiation, authorized execution" in text
    assert "unreachable until the separately frozen chain passes and explicit pilot authorization exists" in text


def test_mode_t_requires_analysis_lock_before_release():
    text = _read(THREAT_MODEL)
    assert "P4-T-L — analysis lock, pre-release" in text
    assert "If this ordering cannot be established, the pilot is **INVALID / NO SCIENTIFIC INTERPRETATION**" in text


def test_mode_t_rejects_rerun_and_multi_run_selection():
    threat = _read(THREAT_MODEL)
    evidence = _read(EVIDENCE)
    assert "Reruns enable cherry-picking" in threat
    assert "One authorization maps to one accepted execution identity" in threat
    assert "reject `GITHUB_RUN_ATTEMPT != 1`" in evidence
    assert "run-reservation → exact-run authorization → execution" in evidence


def test_mode_t_does_not_treat_github_history_as_immutable_evidence():
    text = _read(EVIDENCE)
    assert "Logs and workflow runs are not immutable evidence" in text
    assert "users with write access can delete workflow runs" in text
    assert "independently preserved P6 evidence channel" in text


def test_mode_t_requires_strict_timelock_chain_binding():
    text = _read(EVIDENCE)
    assert "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971" in text
    assert "Ciphertext chain-hash trust must be disabled" in text
    assert "Strict()" in text


def test_mode_t_keeps_live_runner_memory_access_unknown():
    text = _read(EVIDENCE)
    assert "repository owner cannot inspect live runner memory" in text
    assert "remains **UNKNOWN**, not PASS" in text


def test_mode_h_and_i_are_not_weakened_by_mode_t_design():
    p4 = _read(P4)
    threat = _read(THREAT_MODEL)
    assert "Mode H — distinct-human custody" in p4
    assert "Mode I — institutional / third-party custody" in p4
    assert "Mode H and Mode I semantics exactly" in threat


def test_design_record_is_explicitly_non_authorizing():
    text = _read(THREAT_MODEL)
    assert "AUTHORIZATION NOT GRANTED" in text
    assert "empirical N=0" in text
    assert "IMPLEMENTATION NOT YET PROMOTABLE" in text
