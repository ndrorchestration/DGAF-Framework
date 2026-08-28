"""Regression tests for strict TGL downstream gate ordering."""
from __future__ import annotations

from pptl.triadic_governance_loop import GateResult, TriadicGovernanceLoop, TGLHooks


def test_hpg_is_not_executed_when_phi_closure_warns() -> None:
    executed: list[str] = []

    def phi(_text, _ctx):
        executed.append("phi")
        return GateResult.WARN

    def hpg(_text, _ctx):
        executed.append("hpg")
        return GateResult.PASS

    audit = TriadicGovernanceLoop(
        session_id="TGL-ORDER-TEST",
        agent_id="test",
        hooks=TGLHooks(phi_closure_fn=phi, hpg_fn=hpg),
    ).run_turn("safe")

    assert executed == ["phi"]
    step6 = next(g for g in audit.gate_records if g.step == 6)
    step7 = next(g for g in audit.gate_records if g.step == 7)
    assert step6.result is GateResult.WARN
    assert step7.result is GateResult.SKIP
    assert step7.notes == "Phi-Closure did not PASS"


def test_hpg_is_not_executed_when_phi_closure_is_unwired() -> None:
    executed: list[str] = []

    def hpg(_text, _ctx):
        executed.append("hpg")
        return GateResult.PASS

    audit = TriadicGovernanceLoop(
        session_id="TGL-ORDER-TEST-SKIP",
        agent_id="test",
        hooks=TGLHooks(hpg_fn=hpg),
    ).run_turn("safe")

    assert executed == []
    step6 = next(g for g in audit.gate_records if g.step == 6)
    step7 = next(g for g in audit.gate_records if g.step == 7)
    assert step6.result is GateResult.SKIP
    assert step7.result is GateResult.SKIP
    assert step7.notes == "Phi-Closure did not PASS"


def test_hpg_executes_after_phi_closure_passes() -> None:
    executed: list[str] = []

    def phi(_text, _ctx):
        executed.append("phi")
        return GateResult.PASS

    def hpg(_text, _ctx):
        executed.append("hpg")
        return GateResult.PASS

    audit = TriadicGovernanceLoop(
        session_id="TGL-ORDER-TEST-PASS",
        agent_id="test",
        hooks=TGLHooks(phi_closure_fn=phi, hpg_fn=hpg),
    ).run_turn("safe")

    assert executed == ["phi", "hpg"]
    step7 = next(g for g in audit.gate_records if g.step == 7)
    assert step7.result is GateResult.PASS
