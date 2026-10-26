"""Issue #1509: P-35 predicate-absence and pass-through assurance sentinels.

This is a non-experimental, test-only audit candidate. Strict XFAIL tests
describe currently confirmed gaps; they are NOT remediation or passing proof.
In particular, supplied all-True predicates are not independent verification.
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
@pytest.mark.xfail(
    strict=True,
    reason="#1509: absent P-35 predicate currently produces a sealed PASS",
)
def test_absent_predicate_cannot_pass_with_all_other_hooks_passing():
    audit = _tgl(_all_downstream_pass()).run_turn("synthetic input")
    premise = next(g for g in audit.gate_records if g.step == 0)
    assert premise.result is GateResult.SKIP
    assert audit.final_status is TurnStatus.ESCALATE
    assert audit.verify_seal()


@pytest.mark.governance
@pytest.mark.xfail(
    strict=True,
    reason="#1509: default general domain currently installs an all-True lambda",
)
def test_general_domain_does_not_auto_install_unverified_predicate():
    config = OrchestratorConfig(session_id="p35-1509-general", domain="general")
    orchestrator = IntegratedOrchestrator(config)
    assert orchestrator.config.premise_check_fn is None


@pytest.mark.governance
@pytest.mark.xfail(
    strict=True,
    reason="#1509: direct P-35 evaluate() currently defaults missing predicate to True",
)
def test_direct_gate_requires_an_explicit_predicate():
    gate = ProcludingPremiseGate(
        invariants=DGAF_CONSTITUTIONAL_INVARIANTS,
        session_id="p35-1509-direct",
        agent_id="p35-audit",
    )
    with pytest.raises(ValueError, match="predicate|check_fn"):
        gate.evaluate("synthetic input")


@pytest.mark.governance
@pytest.mark.xfail(
    strict=True,
    reason="#1509: general-domain pass-through can synthesize after other hooks PASS",
)
def test_general_domain_no_predicate_never_synthesizes_with_full_hooks():
    orchestrator = IntegratedOrchestrator(
        OrchestratorConfig(session_id="p35-1509-orch", domain="general")
    )
    orchestrator.tgl.hooks = _all_downstream_pass(
        premise_check_fn=orchestrator.config.premise_check_fn
    )
    result = orchestrator.orchestrate_turn("synthetic input", "p35-1509-turn")
    assert result.tgl_passed is False
    assert result.response is None
    assert result.final_status is TurnStatus.ESCALATE


@pytest.mark.governance
def test_supplied_true_predicate_only_proves_callable_returned_true():
    """Positive control, not evidence of an admitted or substantive verifier."""
    audit = _tgl(
        _all_downstream_pass(premise_check_fn=lambda _text, _invariant: True)
    ).run_turn("synthetic input")
    assert audit.final_status is TurnStatus.PASS
    assert audit.verify_seal()
    # This is an instrumented test fixture; its PASS must not be called
    # externally verified, independently audited, or authorized.


@pytest.mark.governance
def test_explicit_invariant_denial_stops_before_downstream_hooks():
    calls = []

    def should_not_run(_text, _context):
        calls.append(True)
        return GateResult.PASS

    hooks = _all_downstream_pass(
        premise_check_fn=lambda _text, _invariant: False
    )
    hooks.scpe_fn = should_not_run
    with pytest.raises(PremiseViolationError):
        _tgl(hooks).run_turn("synthetic denial")
    assert calls == []
