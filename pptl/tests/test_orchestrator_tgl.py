"""
Test suite: IntegratedOrchestrator × TGL wire-in
Anchor: S068 | OI-05
Metrics: TGL gate records present per turn; blocked turns return no response;
         domain auto-wire fires correct premise_check_fn.
"""

import pytest

from pptl.orchestrator import IntegratedOrchestrator, OrchestratorConfig
from pptl.triadic_governance_loop import GateResult, TGLHooks, TurnStatus

SESSION = "test-s068"


def _make_orchestrator(domain="general", premise_check_fn=None, dry_run=True):
    cfg = OrchestratorConfig(
        session_id=SESSION,
        domain=domain,
        premise_check_fn=premise_check_fn,
        dry_run=dry_run,
    )
    return IntegratedOrchestrator(cfg)


# --- Basic turn execution ---


def test_default_turn_preserves_escalation_without_synthesis():
    orch = _make_orchestrator()
    synthesized = []
    orch._synthesize_response = lambda text, audit: synthesized.append(text)
    result = orch.orchestrate_turn("What is the weather today?", turn_id="t001")
    assert result.tgl_passed is False
    assert result.final_status == TurnStatus.ESCALATE
    assert result.response is None
    assert result.blocked_reason
    assert any(g.result == GateResult.SKIP for g in result.gate_records)
    assert synthesized == []


def _wire_required_hooks(orch):
    orch.tgl.hooks = TGLHooks(
        premise_check_fn=lambda _text, _invariant: True,
        scpe_fn=lambda _text, _ctx: GateResult.PASS,
        pdmal_fn=lambda _text, _ctx: GateResult.PASS,
        demijoul_fn=lambda _text, _ctx: GateResult.PASS,
        kappa_fn=lambda _text, _ctx: GateResult.PASS,
        sentinel_fn=lambda _text, _ctx: GateResult.PASS,
        phi_closure_fn=lambda _text, _ctx: GateResult.PASS,
        hpg_fn=lambda _text, _ctx: GateResult.PASS,
        apogee_fn=lambda _text, _ctx: GateResult.PASS,
        herald_fn=lambda _text, _ctx: GateResult.PASS,
    )


@pytest.mark.parametrize(
    "gate_result, status, passed",
    [
        (GateResult.PASS, TurnStatus.PASS, True),
        (GateResult.WARN, TurnStatus.WARN, True),
        (GateResult.KILL, TurnStatus.KILL, False),
        (GateResult.SKIP, TurnStatus.ESCALATE, False),
    ],
)
def test_wrapper_preserves_real_tgl_status(gate_result, status, passed):
    orch = _make_orchestrator()
    _wire_required_hooks(orch)
    orch.tgl.hooks.scpe_fn = lambda _text, _ctx: gate_result
    result = orch.orchestrate_turn("synthetic input", "status-turn")
    assert result.final_status == status
    assert result.tgl_passed is passed
    if passed:
        assert result.response == "[Governed response] synthetic input"
        assert result.blocked_reason is None
    else:
        assert result.response is None
        assert result.blocked_reason


@pytest.mark.parametrize("bad_hook", [lambda _text, _ctx: "invalid", lambda _text, _ctx: 1 / 0])
def test_failed_hook_remains_blocked(bad_hook):
    orch = _make_orchestrator()
    _wire_required_hooks(orch)
    orch.tgl.hooks.scpe_fn = bad_hook
    result = orch.orchestrate_turn("synthetic input", "bad-hook")
    assert result.final_status == TurnStatus.KILL
    assert result.tgl_passed is False
    assert result.response is None
    assert result.blocked_reason


def test_turn_result_has_gate_records():
    orch = _make_orchestrator()
    result = orch.orchestrate_turn("Hello", turn_id="t002")
    assert isinstance(result.gate_records, list)
    assert len(result.gate_records) > 0


def test_turn_result_does_not_fabricate_phi_score():
    """The current TGL TurnAuditRecord exposes no numeric phi score."""
    orch = _make_orchestrator()
    result = orch.orchestrate_turn("Hello", turn_id="t003")
    assert result.phi_score is None


# --- Blocking behaviour ---


def test_blocked_turn_returns_no_response():
    # Canonical P-35 check returns False when an invariant is violated.
    orch = _make_orchestrator(premise_check_fn=lambda _text, _invariant: False)
    result = orch.orchestrate_turn("zip code feature used", turn_id="t004")
    assert result.tgl_passed is False
    assert result.final_status == TurnStatus.KILL
    assert result.response is None
    assert result.blocked_reason is not None


def test_blocked_turn_has_gate_records():
    orch = _make_orchestrator(premise_check_fn=lambda _text, _invariant: False)
    result = orch.orchestrate_turn("zip code feature used", turn_id="t005")
    assert len(result.gate_records) > 0


# --- Domain auto-wire ---


def test_credit_domain_auto_wires_premise_fn():
    orch = _make_orchestrator(domain="credit")
    assert orch.config.premise_check_fn is not None
    # Credit fn should fire on known proxy
    assert not orch.config.premise_check_fn("zip code used in model", None)
    assert orch.config.premise_check_fn("standard credit feature", None)


def test_justice_domain_auto_wires_premise_fn():
    orch = _make_orchestrator(domain="justice")
    assert orch.config.premise_check_fn is not None
    assert not orch.config.premise_check_fn("compas score for defendant", None)
    assert orch.config.premise_check_fn("standard justice feature", None)


def test_general_domain_premise_fn_is_passthrough():
    orch = _make_orchestrator(domain="general")
    assert orch.config.premise_check_fn is not None
    assert orch.config.premise_check_fn("anything at all", None)


# --- Session metadata ---


def test_turn_result_carries_session_id():
    orch = _make_orchestrator()
    result = orch.orchestrate_turn("test", turn_id="t009")
    assert result.session_id == SESSION


def test_turn_result_carries_domain():
    orch = _make_orchestrator(domain="credit")
    result = orch.orchestrate_turn("standard input", turn_id="t010")
    assert result.domain == "credit"
