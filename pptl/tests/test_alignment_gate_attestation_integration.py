import json
import tempfile
from pathlib import Path

import pytest

from pptl.attestation_gate import AttestationGate, AttestationStatus
from pptl.co_orchestration_schema import AlignmentGate, CoOrchQueue, Opportunity, save_queue, load_queue


@pytest.mark.co_orch
def test_alignment_gate_evaluate_claim_passes_without_attestation_gate():
    gate = AlignmentGate(fit=True, risk=True, effort=True, priority=True)
    assert gate.evaluate_claim("sentinel", "all good", "sufficient evidence") is True


@pytest.mark.co_orch
def test_alignment_gate_evaluate_claim_fails_when_alignment_fails_even_with_attestation():
    gate = AlignmentGate(
        fit=False, risk=True, effort=True, priority=True,
        attestation_gate=AttestationGate(),
    )
    assert gate.evaluate_claim("sentinel", "all good", "sufficient evidence") is False


@pytest.mark.co_orch
def test_alignment_gate_evaluate_claim_blocks_rejected_attestation():
    gate = AlignmentGate(
        fit=True, risk=True, effort=True, priority=True,
        attestation_gate=AttestationGate(),
    )
    assert gate.evaluate_claim("sentinel", "claim", "bad") is False


@pytest.mark.co_orch
def test_alignment_gate_evaluate_claim_passes_attested_claim():
    gate = AlignmentGate(
        fit=True, risk=True, effort=True, priority=True,
        attestation_gate=AttestationGate(),
    )
    assert gate.evaluate_claim("sentinel", "claim", "evidence is long enough") is True


@pytest.mark.co_orch
def test_alignment_gate_runtime_dependency_not_serialized(tmp_path: Path):
    gate = AlignmentGate(
        fit=True, risk=True, effort=True, priority=True,
        attestation_gate=AttestationGate(),
    )
    opp = Opportunity(
        id="OPP-X",
        title="integration test",
        layer="pptl",
        detected_by="Amethyst",
        mode="ADOPT",
        pattern_ref="P-04",
        gate=gate,
    )
    queue = CoOrchQueue(opportunities=[opp])
    path = tmp_path / "queue.json"
    save_queue(queue, path)
    raw = path.read_text(encoding="utf-8")
    assert "attestation_gate" not in raw
    loaded = load_queue(path)
    assert loaded.opportunities[0].gate.attestation_gate is None


@pytest.mark.co_orch
def test_alignment_gate_custom_attestor_contract():
    class FakeResult:
        def __init__(self, passed):
            self.passed = passed

    class FakeAttestor:
        def __init__(self, passed):
            self.passed = passed
            self.calls = 0
        def attest(self, record):
            self.calls += 1
            return FakeResult(self.passed)

    fake = FakeAttestor(True)
    gate = AlignmentGate(
        fit=True, risk=True, effort=True, priority=True,
        attestation_gate=fake,
    )
    assert gate.evaluate_claim("sentinel", "claim", "evidence is long enough") is True
    assert fake.calls == 1


@pytest.mark.co_orch
def test_alignment_gate_custom_attestor_false_blocks():
    class FakeResult:
        def __init__(self, passed):
            self.passed = passed

    class FakeAttestor:
        def attest(self, record):
            return FakeResult(False)

    gate = AlignmentGate(
        fit=True, risk=True, effort=True, priority=True,
        attestation_gate=FakeAttestor(),
    )
    assert gate.evaluate_claim("sentinel", "claim", "evidence is long enough") is False
