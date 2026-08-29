"""TGL governance contract tests."""

import hashlib
import pytest

from pptl.procluding_premise import PremiseViolationError
from pptl.triadic_governance_loop import GateResult, TriadicGovernanceLoop, TGLHooks, TurnStatus


def make_tgl(hooks: TGLHooks = None) -> TriadicGovernanceLoop:
    return TriadicGovernanceLoop(session_id="S068-TEST", agent_id="test-amethyst", hooks=hooks or TGLHooks())


@pytest.mark.governance
def test_full_skip_turn_escalates():
    audit = make_tgl().run_turn("safe input")
    assert audit.final_status == TurnStatus.ESCALATE


@pytest.mark.governance
def test_partial_skip_turn_escalates():
    hooks = TGLHooks(
        scpe_fn=lambda text, ctx: GateResult.PASS,
        pdmal_fn=lambda text, ctx: GateResult.PASS,
        demijoul_fn=lambda text, ctx: GateResult.PASS,
        kappa_fn=lambda text, ctx: GateResult.PASS,
        sentinel_fn=lambda text, ctx: GateResult.PASS,
        phi_closure_fn=lambda text, ctx: GateResult.PASS,
    )
    audit = make_tgl(hooks).run_turn("partial wiring")
    assert audit.final_status == TurnStatus.ESCALATE
    assert any(g.step == 8 and g.result == GateResult.SKIP for g in audit.gate_records)


@pytest.mark.governance
def test_premise_violation_raises_and_kills():
    hooks = TGLHooks(premise_check_fn=lambda text, inv: False)
    with pytest.raises(PremiseViolationError):
        make_tgl(hooks).run_turn("constitutional violation")


@pytest.mark.governance
def test_downstream_gate_kill_sets_status():
    executed_steps = []
    def kill_gate(text, ctx):
        executed_steps.append(3)
        return GateResult.KILL
    def should_not_run(text, ctx):
        executed_steps.append(99)
        return GateResult.PASS
    audit = make_tgl(TGLHooks(demijoul_fn=kill_gate, kappa_fn=should_not_run)).run_turn("trigger kill")
    assert audit.final_status == TurnStatus.KILL
    assert 99 not in executed_steps


@pytest.mark.governance
def test_phi_closure_kill_sets_kill_rec():
    audit = make_tgl(TGLHooks(phi_closure_fn=lambda t, c: GateResult.KILL)).run_turn("phi closure fail")
    assert audit.final_status == TurnStatus.KILL_REC


@pytest.mark.governance
def test_warn_reduces_to_warn():
    hooks = TGLHooks(
        scpe_fn=lambda t, c: GateResult.WARN,
        pdmal_fn=lambda t, c: GateResult.PASS,
        demijoul_fn=lambda t, c: GateResult.PASS,
        kappa_fn=lambda t, c: GateResult.PASS,
        sentinel_fn=lambda t, c: GateResult.PASS,
        phi_closure_fn=lambda t, c: GateResult.PASS,
        hpg_fn=lambda t, c: GateResult.PASS,
        apogee_fn=lambda t, c: GateResult.PASS,
    )
    audit = make_tgl(hooks).run_turn("warning")
    assert audit.final_status == TurnStatus.WARN


@pytest.mark.governance
def test_phi_closure_warn_skips_hpg():
    executed = []
    hooks = TGLHooks(phi_closure_fn=lambda t, c: GateResult.WARN, hpg_fn=lambda t, c: executed.append(True) or GateResult.PASS)
    audit = make_tgl(hooks).run_turn("phi warning")
    hpg = next(g for g in audit.gate_records if g.step == 7)
    assert hpg.result == GateResult.SKIP
    assert executed == []
    assert audit.final_status == TurnStatus.WARN


@pytest.mark.governance
def test_phi_closure_skip_is_dependency_skip_not_unwired():
    executed = []
    hooks = TGLHooks(hpg_fn=lambda t, c: executed.append(True) or GateResult.PASS)
    audit = make_tgl(hooks).run_turn("phi skipped")
    hpg = next(g for g in audit.gate_records if g.step == 7)
    assert hpg.result == GateResult.SKIP
    assert hpg.notes == "Phi-Closure did not PASS"
    assert executed == []
    assert audit.final_status == TurnStatus.ESCALATE


@pytest.mark.governance
def test_herald_receives_tgl_turn_audit_event():
    received = []
    def capture_herald(audit_dict, ctx):
        received.append(audit_dict)
        return GateResult.PASS
    make_tgl(TGLHooks(herald_fn=capture_herald)).run_turn("test input")
    assert len(received) == 1
    assert received[0]["event_type"] == "TGL_TURN_AUDIT"


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
    assert len(audit.seal_hash) == 64


@pytest.mark.governance
def test_input_hash_is_full_sha256():
    text = "hash-bound input"
    audit = make_tgl().run_turn(text)
    assert audit.input_hash == hashlib.sha256(text.encode("utf-8")).hexdigest()


@pytest.mark.governance
def test_gate_records_include_all_10_steps():
    hooks = TGLHooks(
        scpe_fn=lambda t, c: GateResult.PASS,
        pdmal_fn=lambda t, c: GateResult.PASS,
        demijoul_fn=lambda t, c: GateResult.PASS,
        kappa_fn=lambda t, c: GateResult.PASS,
        sentinel_fn=lambda t, c: GateResult.PASS,
        phi_closure_fn=lambda t, c: GateResult.PASS,
        hpg_fn=lambda t, c: GateResult.PASS,
        apogee_fn=lambda t, c: GateResult.PASS,
        herald_fn=lambda t, c: GateResult.PASS,
    )
    audit = make_tgl(hooks).run_turn("full pass")
    assert {g.step for g in audit.gate_records} == set(range(10))
    assert audit.final_status == TurnStatus.PASS


@pytest.mark.governance
def test_all_unwired_gates_marked_skip():
    audit = make_tgl().run_turn("skip test")
    skip_steps = [g for g in audit.gate_records if g.step in range(1, 9)]
    assert all(g.result == GateResult.SKIP for g in skip_steps)


@pytest.mark.governance
def test_p35_always_fires_regardless_of_hooks():
    audit = make_tgl().run_turn("p35 check")
    step0 = next(g for g in audit.gate_records if g.step == 0)
    assert step0.pattern == "P-35"
    assert step0.result == GateResult.PASS


@pytest.mark.governance
def test_seal_changes_when_gate_records_change():
    audit = make_tgl().run_turn("seal coverage")
    original = audit.seal_hash
    audit.gate_records.append(audit.gate_records[-1])
    assert audit.seal() != original


@pytest.mark.governance
def test_final_returned_gate_set_is_sealed():
    audit = make_tgl().run_turn("final seal")
    sealed = audit.seal_hash
    assert audit.seal() == sealed


@pytest.mark.governance
def test_hook_exception_is_contained_as_kill():
    def exploding_hook(text, ctx):
        raise RuntimeError("boom")
    audit = make_tgl(TGLHooks(scpe_fn=exploding_hook)).run_turn("exception")
    step1 = next(g for g in audit.gate_records if g.step == 1)
    assert step1.result == GateResult.KILL
    assert audit.final_status == TurnStatus.KILL
