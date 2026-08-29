"""TGL governance contract and adversarial regression tests."""

import hashlib

import pytest

from pptl.procluding_premise import PremiseViolationError
from pptl.triadic_governance_loop import GateResult, TriadicGovernanceLoop, TGLHooks, TurnStatus


def make_tgl(hooks: TGLHooks | None = None) -> TriadicGovernanceLoop:
    return TriadicGovernanceLoop(
        session_id="S068-TEST",
        agent_id="test-amethyst",
        hooks=hooks or TGLHooks(),
    )


def pass_hooks(**overrides) -> TGLHooks:
    values = {
        "scpe_fn": lambda t, c: GateResult.PASS,
        "pdmal_fn": lambda t, c: GateResult.PASS,
        "demijoul_fn": lambda t, c: GateResult.PASS,
        "kappa_fn": lambda t, c: GateResult.PASS,
        "sentinel_fn": lambda t, c: GateResult.PASS,
        "phi_closure_fn": lambda t, c: GateResult.PASS,
        "hpg_fn": lambda t, c: GateResult.PASS,
        "apogee_fn": lambda t, c: GateResult.PASS,
        "herald_fn": lambda t, c: GateResult.PASS,
    }
    values.update(overrides)
    return TGLHooks(**values)


@pytest.mark.governance
def test_full_skip_turn_escalates():
    audit = make_tgl().run_turn("safe input")
    assert audit.final_status == TurnStatus.ESCALATE
    assert {g.step for g in audit.gate_records} == set(range(10))


@pytest.mark.governance
def test_partial_skip_turn_escalates():
    hooks = pass_hooks(herald_fn=None)
    hooks.apogee_fn = None
    audit = make_tgl(hooks).run_turn("partial wiring")
    assert audit.final_status == TurnStatus.ESCALATE
    assert any(g.step == 8 and g.result == GateResult.SKIP for g in audit.gate_records)


@pytest.mark.governance
def test_full_wiring_returns_pass():
    audit = make_tgl(pass_hooks()).run_turn("full pass")
    assert audit.final_status == TurnStatus.PASS
    assert {g.step for g in audit.gate_records} == set(range(10))
    assert all(g.result == GateResult.PASS for g in audit.gate_records)


@pytest.mark.governance
def test_premise_violation_raises_and_records_kill():
    hooks = TGLHooks(premise_check_fn=lambda text, inv: False)
    with pytest.raises(PremiseViolationError):
        make_tgl(hooks).run_turn("constitutional violation")


@pytest.mark.governance
def test_premise_failure_does_not_get_masked_by_herald_exception():
    def exploding_herald(payload, ctx):
        raise RuntimeError("herald unavailable")

    hooks = TGLHooks(
        premise_check_fn=lambda text, inv: False,
        herald_fn=exploding_herald,
    )
    with pytest.raises(PremiseViolationError):
        make_tgl(hooks).run_turn("constitutional violation")


@pytest.mark.governance
def test_downstream_gate_kill_sets_status_and_stops_execution():
    executed_steps = []

    def kill_gate(text, ctx):
        executed_steps.append(3)
        return GateResult.KILL

    def should_not_run(text, ctx):
        executed_steps.append(99)
        return GateResult.PASS

    hooks = TGLHooks(demijoul_fn=kill_gate, kappa_fn=should_not_run)
    audit = make_tgl(hooks).run_turn("trigger kill")
    assert audit.final_status == TurnStatus.KILL
    assert executed_steps == [3]


@pytest.mark.governance
def test_phi_closure_kill_sets_kill_rec():
    audit = make_tgl(TGLHooks(phi_closure_fn=lambda t, c: GateResult.KILL)).run_turn("phi closure fail")
    assert audit.final_status == TurnStatus.KILL_REC


@pytest.mark.governance
def test_warn_reduces_to_warn_when_no_stronger_state_exists():
    hooks = pass_hooks(scpe_fn=lambda t, c: GateResult.WARN)
    audit = make_tgl(hooks).run_turn("warning")
    assert audit.final_status == TurnStatus.WARN


@pytest.mark.governance
def test_warn_then_required_skip_reduces_to_escalate():
    hooks = pass_hooks(scpe_fn=lambda t, c: GateResult.WARN, apogee_fn=None)
    audit = make_tgl(hooks).run_turn("warn and missing attestation")
    assert audit.final_status == TurnStatus.ESCALATE


@pytest.mark.governance
def test_phi_closure_warn_skips_hpg_and_preserves_warn():
    executed = []
    hooks = pass_hooks(
        phi_closure_fn=lambda t, c: GateResult.WARN,
        hpg_fn=lambda t, c: executed.append(True) or GateResult.PASS,
    )
    audit = make_tgl(hooks).run_turn("phi warning")
    hpg = next(g for g in audit.gate_records if g.step == 7)
    assert hpg.result == GateResult.SKIP
    assert hpg.notes == "Phi-Closure did not PASS"
    assert executed == []
    assert audit.final_status == TurnStatus.WARN


@pytest.mark.governance
def test_phi_closure_skip_is_dependency_skip_not_unwired_required_gate():
    executed = []
    hooks = pass_hooks(
        phi_closure_fn=None,
        hpg_fn=lambda t, c: executed.append(True) or GateResult.PASS,
    )
    audit = make_tgl(hooks).run_turn("phi skipped")
    hpg = next(g for g in audit.gate_records if g.step == 7)
    assert hpg.result == GateResult.SKIP
    assert hpg.notes == "Phi-Closure did not PASS"
    assert executed == []
    assert audit.final_status == TurnStatus.ESCALATE


@pytest.mark.governance
def test_unwired_hpg_after_passing_phi_escalates():
    hooks = pass_hooks(hpg_fn=None)
    audit = make_tgl(hooks).run_turn("missing hpg")
    hpg = next(g for g in audit.gate_records if g.step == 7)
    assert hpg.result == GateResult.SKIP
    assert hpg.notes == "Hook not wired"
    assert audit.final_status == TurnStatus.ESCALATE


@pytest.mark.governance
def test_herald_receives_complete_pre_herald_audit_event():
    received = []

    def capture_herald(audit_dict, ctx):
        received.append(audit_dict)
        return GateResult.PASS

    audit = make_tgl(pass_hooks(herald_fn=capture_herald)).run_turn("test input")
    assert len(received) == 1
    assert received[0]["event_type"] == "TGL_TURN_AUDIT"
    assert received[0]["final_status"] == "PASS"
    assert all(g["step"] != 9 for g in received[0]["gates"])
    assert audit.gate_records[-1].step == 9


@pytest.mark.governance
def test_herald_kill_cannot_leave_final_status_pass():
    audit = make_tgl(pass_hooks(herald_fn=lambda t, c: GateResult.KILL)).run_turn("herald kill")
    assert audit.final_status == TurnStatus.KILL
    assert audit.gate_records[-1].result == GateResult.KILL


@pytest.mark.governance
def test_invalid_hook_result_is_fail_closed_kill():
    audit = make_tgl(pass_hooks(scpe_fn=lambda t, c: object())).run_turn("invalid result")
    step1 = next(g for g in audit.gate_records if g.step == 1)
    assert step1.result == GateResult.KILL
    assert audit.final_status == TurnStatus.KILL


@pytest.mark.governance
def test_hook_exception_is_contained_as_kill():
    def exploding_hook(text, ctx):
        raise RuntimeError("boom")

    audit = make_tgl(pass_hooks(scpe_fn=exploding_hook)).run_turn("exception")
    step1 = next(g for g in audit.gate_records if g.step == 1)
    assert step1.result == GateResult.KILL
    assert "boom" in step1.notes
    assert audit.final_status == TurnStatus.KILL


@pytest.mark.governance
def test_turn_counter_increments_per_run():
    tgl = make_tgl()
    assert tgl.turn_counter == 0
    tgl.run_turn("first")
    assert tgl.turn_counter == 1
    tgl.run_turn("second")
    assert tgl.turn_counter == 2


@pytest.mark.governance
def test_input_hash_is_full_sha256():
    text = "hash-bound input"
    audit = make_tgl().run_turn(text)
    assert audit.input_hash == hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert len(audit.input_hash) == 64


@pytest.mark.governance
def test_audit_record_is_sealed_after_final_gate_set():
    audit = make_tgl(pass_hooks()).run_turn("sealed turn")
    assert len(audit.seal_hash) == 64
    assert audit.seal() == audit.seal_hash


@pytest.mark.governance
def test_seal_changes_when_gate_records_change():
    audit = make_tgl(pass_hooks()).run_turn("seal coverage")
    original = audit.seal_hash
    audit.gate_records.append(audit.gate_records[-1])
    assert audit.seal() != original


@pytest.mark.governance
def test_seal_changes_when_gate_notes_change():
    audit = make_tgl(pass_hooks()).run_turn("seal notes")
    original = audit.seal_hash
    audit.gate_records[1] = type(audit.gate_records[1])(
        audit.gate_records[1].step,
        audit.gate_records[1].pattern,
        audit.gate_records[1].gate_name,
        audit.gate_records[1].result,
        "tampered",
    )
    assert audit.seal() != original


@pytest.mark.governance
def test_final_returned_gate_set_includes_herald_before_seal():
    audit = make_tgl(pass_hooks()).run_turn("final seal")
    assert audit.gate_records[-1].step == 9
    assert audit.seal_hash == audit.seal()


@pytest.mark.governance
def test_required_gate_set_is_explicit_and_excludes_p35_and_herald():
    assert TriadicGovernanceLoop.REQUIRED_GATE_STEPS == frozenset({1, 2, 3, 4, 5, 6, 7, 8})


@pytest.mark.governance
def test_status_reduction_is_monotonic_for_stronger_failures():
    pass_audit = make_tgl(pass_hooks()).run_turn("baseline")
    warn_audit = make_tgl(pass_hooks(scpe_fn=lambda t, c: GateResult.WARN)).run_turn("warn")
    kill_audit = make_tgl(pass_hooks(scpe_fn=lambda t, c: GateResult.KILL)).run_turn("kill")
    assert pass_audit.final_status == TurnStatus.PASS
    assert warn_audit.final_status == TurnStatus.WARN
    assert kill_audit.final_status == TurnStatus.KILL


@pytest.mark.governance
def test_all_required_gates_must_be_represented_for_pass():
    hooks = pass_hooks(apogee_fn=None)
    audit = make_tgl(hooks).run_turn("missing required gate")
    assert audit.final_status == TurnStatus.ESCALATE
    assert any(g.step == 8 and g.result == GateResult.SKIP for g in audit.gate_records)
