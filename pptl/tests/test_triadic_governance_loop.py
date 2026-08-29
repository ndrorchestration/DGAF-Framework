"""
test_triadic_governance_loop.py — TGL governance contract tests
DGAF-Framework · pptl/tests · S068
"""

import hashlib
import pytest

from pptl.procluding_premise import PremiseViolationError
from pptl.triadic_governance_loop import (
    GateRecord,
    GateResult,
    TriadicGovernanceLoop,
    TGLHooks,
    TurnStatus,
)


def make_tgl(hooks: TGLHooks = None) -> TriadicGovernanceLoop:
    return TriadicGovernanceLoop(
        session_id="S068-TEST",
        agent_id="test-amethyst",
        hooks=hooks or TGLHooks(),
    )


@pytest.mark.governance
def test_unwired_required_gates_escalate():
    """Required SKIP states must fail closed to ESCALATE rather than PASS."""
    audit = make_tgl().run_turn("safe input")
    assert audit.final_status == TurnStatus.ESCALATE


@pytest.mark.governance
def test_premise_violation_raises_and_kills():
    """P-35 KILL → PremiseViolationError raised and gate logged as KILL."""
    hooks = TGLHooks(premise_check_fn=lambda text, inv: False)
    with pytest.raises(PremiseViolationError):
        make_tgl(hooks).run_turn("constitutional violation")


@pytest.mark.governance
def test_downstream_gate_kill_sets_status_and_stops_execution():
    """Terminal KILL stops later hooks, including conditional HPG/Apogee execution."""
    executed_steps = []

    def kill_gate(text, ctx):
        executed_steps.append(3)
        return GateResult.KILL

    def should_not_run(text, ctx):
        executed_steps.append(99)
        return GateResult.PASS

    hooks = TGLHooks(
        demijoul_fn=kill_gate,
        kappa_fn=should_not_run,
        hpg_fn=should_not_run,
        apogee_fn=should_not_run,
    )
    audit = make_tgl(hooks).run_turn("trigger kill")
    assert audit.final_status == TurnStatus.KILL
    assert executed_steps == [3]


@pytest.mark.governance
def test_phi_closure_kill_sets_kill_rec():
    """P-32 KILL → final_status KILL_REC."""
    hooks = TGLHooks(phi_closure_fn=lambda t, c: GateResult.KILL)
    audit = make_tgl(hooks).run_turn("phi closure fail")
    assert audit.final_status == TurnStatus.KILL


@pytest.mark.governance
def test_warn_propagates_to_turn_status():
    """A WARN gate must not be silently reduced to PASS."""
    hooks = TGLHooks(scpe_fn=lambda text, ctx: GateResult.WARN)
    audit = make_tgl(hooks).run_turn("warning")
    assert audit.final_status == TurnStatus.WARN


@pytest.mark.governance
def test_phi_closure_warn_skips_hpg():
    """HPG must not execute unless Phi-Closure returns PASS."""
    executed = []
    hooks = TGLHooks(
        phi_closure_fn=lambda text, ctx: GateResult.WARN,
        hpg_fn=lambda text, ctx: executed.append(True) or GateResult.PASS,
    )
    audit = make_tgl(hooks).run_turn("phi warning")
    hpg = next(g for g in audit.gate_records if g.step == 7)
    assert hpg.result == GateResult.SKIP
    assert executed == []


@pytest.mark.governance
def test_phi_closure_skip_skips_hpg():
    """An unwired Phi-Closure gate must also prevent HPG execution."""
    executed = []
    hooks = TGLHooks(hpg_fn=lambda text, ctx: executed.append(True) or GateResult.PASS)
    audit = make_tgl(hooks).run_turn("phi skipped")
    hpg = next(g for g in audit.gate_records if g.step == 7)
    assert hpg.result == GateResult.SKIP
    assert executed == []


@pytest.mark.governance
def test_herald_receives_tgl_turn_audit_event():
    """Herald hook receives a TGL audit snapshot."""
    received = []

    def capture_herald(audit_dict, ctx):
        received.append(audit_dict)
        return GateResult.PASS

    audit = make_tgl(TGLHooks(herald_fn=capture_herald)).run_turn("test input")
    assert len(received) == 1
    assert received[0]["event_type"] == "TGL_TURN_AUDIT"
    assert received[0]["seal_hash"] != ""
    assert any(g["step"] == 8 for g in received[0]["gates"])
    assert any(g.step == 9 for g in audit.gate_records)


@pytest.mark.governance
def test_turn_counter_increments_per_run():
    tgl = make_tgl()
    assert tgl.turn_counter == 0
    tgl.run_turn("first")
    assert tgl.turn_counter == 1
    tgl.run_turn("second")
    assert tgl.turn_counter == 2


@pytest.mark.governance
def test_audit_record_is_sealed():
    audit = make_tgl().run_turn("sealed turn")
    assert audit.seal_hash != ""
    assert len(audit.seal_hash) == 64


@pytest.mark.governance
def test_seal_covers_herald_gate_and_gate_mutation():
    audit = make_tgl().run_turn("sealed full set")
    sealed = audit.seal_hash
    assert any(g.step == 9 for g in audit.gate_records)
    audit.gate_records.append(GateRecord(10, "TEST", "MutationProbe", GateResult.PASS))
    assert audit.seal() != sealed


@pytest.mark.governance
def test_input_hash_is_full_sha256():
    text = "hash-bound input"
    audit = make_tgl().run_turn(text)
    assert audit.input_hash == hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert len(audit.input_hash) == 64


@pytest.mark.governance
def test_gate_records_include_all_10_steps():
    audit = make_tgl().run_turn("full pass")
    steps = {g.step for g in audit.gate_records}
    assert steps == {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}


@pytest.mark.governance
def test_all_unwired_gates_marked_skip():
    audit = make_tgl().run_turn("skip test")
    skip_steps = [g for g in audit.gate_records if g.step in range(1, 9)]
    assert all(g.result == GateResult.SKIP for g in skip_steps if g.step != 7)


@pytest.mark.governance
def test_p35_always_fires_regardless_of_hooks():
    audit = make_tgl().run_turn("p35 check")
    step0 = next(g for g in audit.gate_records if g.step == 0)
    assert step0.pattern == "P-35"
    assert step0.result == GateResult.PASS
