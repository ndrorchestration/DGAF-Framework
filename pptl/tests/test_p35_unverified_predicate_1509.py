"""Issue #1509: P-35 predicate-absence and pass-through assurance sentinels.

These behavioral tests describe a proposed, unadmitted runtime remediation.
They do not authorize experimental adapters or establish independently verified
constitutional evaluation. All-True fixtures remain test-only, not proof.
"""

import pytest

from pptl.orchestrator import IntegratedOrchestrator, OrchestratorConfig
from pptl.procluding_premise import (
    DGAF_CONSTITUTIONAL_INVARIANTS,
    PremiseViolationError,
    ProcludingPremiseGate,
)
from pptl.triadic_governance_loop import (
    GateResult,
    TGLHooks,
    TriadicGovernanceLoop,
    TurnStatus,
)


def _pass(_text, _context):
    return GateResult.PASS


def _all_downstream_pass(premise_check_fn=None):
    """Wire every downstream step to expose the gate-0 status on its own."""
    return TGLHooks(
        premise_check_fn=premise_check_fn,
        scpe_fn=_pass,
        pdmal_fn=_pass,
        demijoul_fn=_pass,
        kappa_fn=_pass,
        sentinel_fn=_pass,
        phi_closure_fn=_pass,
        hpg_fn=_pass,
        apogee_fn=_pass,
        herald_fn=_pass,
    )


def _tgl(hooks):
    return TriadicGovernanceLoop(
        session_id="p35-1509-synthetic",
        agent_id="p35-audit",
        hooks=hooks,
    )


@pytest.mark.governance
def test_absent_predicate_cannot_pass_with_all_other_hooks_passing():
    audit = _tgl(_all_downstream_pass()).run_turn("synthetic input")
    premise = next(g for g in audit.gate_records if g.step == 0)
    assert premise.result is GateResult.SKIP
    assert audit.final_status is TurnStatus.ESCALATE
    assert audit.verify_seal()


@pytest.mark.governance
def test_general_domain_does_not_auto_install_unverified_predicate():
    config = OrchestratorConfig(session_id="p35-1509-general", domain="general")
    orchestrator = IntegratedOrchestrator(config)
    assert orchestrator.config.premise_check_fn is None


@pytest.mark.governance
def test_direct_gate_requires_an_explicit_predicate():
    gate = ProcludingPremiseGate(
        invariants=DGAF_CONSTITUTIONAL_INVARIANTS,
        session_id="p35-1509-direct",
        agent_id="p35-audit",
    )
    with pytest.raises(ValueError, match="predicate|check_fn"):
        gate.evaluate("synthetic input")


@pytest.mark.governance
def test_general_domain_no_predicate_never_synthesizes_with_full_hooks():
    orchestrator = IntegratedOrchestrator(OrchestratorConfig(session_id="p35-1509-orch", domain="general"))
    orchestrator.tgl.hooks = _all_downstream_pass(premise_check_fn=orchestrator.config.premise_check_fn)
    result = orchestrator.orchestrate_turn("synthetic input", "p35-1509-turn")
    assert result.tgl_passed is False
    assert result.response is None
    assert result.final_status is TurnStatus.ESCALATE


@pytest.mark.governance
def test_supplied_true_predicate_only_proves_callable_returned_true():
    """Positive control, not evidence of an admitted or substantive verifier."""
    audit = _tgl(_all_downstream_pass(premise_check_fn=lambda _text, _invariant: True)).run_turn("synthetic input")
    assert audit.final_status is TurnStatus.PASS
    assert audit.verify_seal()
    p35 = next(g for g in audit.gate_records if g.step == 0)
    assert "NOT_ESTABLISHED" in p35.notes
    # This is an instrumented test fixture; its PASS must not be called
    # externally verified, independently audited, or authorized.


@pytest.mark.governance
def test_explicit_invariant_denial_stops_before_downstream_hooks():
    calls = []

    def should_not_run(_text, _context):
        calls.append(True)
        return GateResult.PASS

    hooks = _all_downstream_pass(premise_check_fn=lambda _text, _invariant: False)
    hooks.scpe_fn = should_not_run
    with pytest.raises(PremiseViolationError):
        _tgl(hooks).run_turn("synthetic denial")
    assert calls == []


@pytest.mark.governance
def test_missing_p35_does_not_execute_any_downstream_gates():
    executed = []

    def record_call(_text, _context):
        executed.append(True)
        return GateResult.PASS

    hooks = _all_downstream_pass()
    hooks.scpe_fn = record_call
    hooks.pdmal_fn = record_call
    hooks.apogee_fn = record_call
    audit = _tgl(hooks).run_turn("unverified request")
    assert executed == []
    assert audit.final_status is TurnStatus.ESCALATE
    assert audit.verify_seal()
    assert {g.step for g in audit.gate_records} == set(range(10))
    assert all(g.result is GateResult.SKIP for g in audit.gate_records[:9])


@pytest.mark.governance
@pytest.mark.parametrize(
    "bad_predicate",
    [
        lambda _text, _invariant: "True",
        lambda _text, _invariant: None,
        lambda _text, _invariant: 1,
    ],
)
def test_nonboolean_p35_denies_without_downstream_execution(bad_predicate):
    executed = []
    hooks = _all_downstream_pass(premise_check_fn=bad_predicate)
    hooks.scpe_fn = lambda _text, _context: executed.append(True) or GateResult.PASS
    audit = _tgl(hooks).run_turn("nonboolean predicate")
    assert executed == []
    assert audit.final_status is TurnStatus.KILL
    assert audit.gate_records[0].result is GateResult.KILL
    assert audit.verify_seal()


@pytest.mark.governance
def test_raising_p35_predicate_denies_without_downstream_execution():
    executed = []

    def fail(_text, _invariant):
        raise RuntimeError("no valid decision")

    hooks = _all_downstream_pass(premise_check_fn=fail)
    hooks.scpe_fn = lambda _text, _context: executed.append(True) or GateResult.PASS
    audit = _tgl(hooks).run_turn("predicate exception")
    assert executed == []
    assert audit.final_status is TurnStatus.KILL
    assert audit.gate_records[0].result is GateResult.KILL
    assert audit.verify_seal()


@pytest.mark.governance
def test_noncallable_p35_is_killed_without_downstream_execution():
    executed = []
    hooks = _all_downstream_pass(premise_check_fn="NOT_A_PREDICATE")
    hooks.scpe_fn = lambda _text, _context: executed.append(True) or GateResult.PASS
    audit = _tgl(hooks).run_turn("bad predicate configuration")
    assert executed == []
    assert audit.final_status is TurnStatus.KILL
    assert audit.gate_records[0].result is GateResult.KILL
    assert audit.verify_seal()


@pytest.mark.governance
def test_unverified_p35_remains_escalated_after_herald_pass():
    receipts = []

    def herald(_text, context):
        receipts.append(context["audit_record"])
        return GateResult.PASS

    hooks = _all_downstream_pass()
    hooks.herald_fn = herald
    audit = _tgl(hooks).run_turn("missing predicate with herald")
    assert len(receipts) == 1
    assert receipts[0]["final_status"] == "ESCALATE"
    assert len(receipts[0]["gates"]) == 9
    assert audit.gate_records[-1].result is GateResult.PASS
    assert audit.final_status is TurnStatus.ESCALATE
    assert audit.verify_seal()
