"""
Test suite: IntegratedOrchestrator × TGL wire-in
Anchor: S068 | OI-05
Metrics: TGL gate records present per turn; blocked turns return no response;
         domain auto-wire fires correct premise_check_fn.
"""
import pytest
from unittest.mock import MagicMock, patch
from pptl.orchestrator import IntegratedOrchestrator, OrchestratorConfig


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

def test_clean_turn_passes_tgl():
    orch = _make_orchestrator()
    result = orch.orchestrate_turn("What is the weather today?", turn_id="t001")
    assert result.tgl_passed is True
    assert result.response is not None
    assert result.blocked_reason is None


def test_turn_result_has_gate_records():
    orch = _make_orchestrator()
    result = orch.orchestrate_turn("Hello", turn_id="t002")
    assert isinstance(result.gate_records, list)
    assert len(result.gate_records) > 0


def test_turn_result_has_phi_score():
    orch = _make_orchestrator()
    result = orch.orchestrate_turn("Hello", turn_id="t003")
    assert result.phi_score is not None
    assert 0.0 <= result.phi_score <= 1.0


# --- Blocking behaviour ---

def test_blocked_turn_returns_no_response():
    # Premise check always fires — should block at step 2
    orch = _make_orchestrator(premise_check_fn=lambda _: True)
    result = orch.orchestrate_turn("zip code feature used", turn_id="t004")
    assert result.tgl_passed is False
    assert result.response is None
    assert result.blocked_reason is not None


def test_blocked_turn_has_gate_records():
    orch = _make_orchestrator(premise_check_fn=lambda _: True)
    result = orch.orchestrate_turn("zip code feature used", turn_id="t005")
    assert len(result.gate_records) > 0


# --- Domain auto-wire ---

def test_credit_domain_auto_wires_premise_fn():
    orch = _make_orchestrator(domain="credit")
    assert orch.config.premise_check_fn is not None
    # Credit fn should fire on known proxy
    assert orch.config.premise_check_fn("zip code used in model")


def test_justice_domain_auto_wires_premise_fn():
    orch = _make_orchestrator(domain="justice")
    assert orch.config.premise_check_fn is not None
    assert orch.config.premise_check_fn("compas score for defendant")


def test_general_domain_premise_fn_is_passthrough():
    orch = _make_orchestrator(domain="general")
    assert orch.config.premise_check_fn is not None
    assert not orch.config.premise_check_fn("anything at all")


# --- Session metadata ---

def test_turn_result_carries_session_id():
    orch = _make_orchestrator()
    result = orch.orchestrate_turn("test", turn_id="t009")
    assert result.session_id == SESSION


def test_turn_result_carries_domain():
    orch = _make_orchestrator(domain="credit")
    result = orch.orchestrate_turn("standard input", turn_id="t010")
    assert result.domain == "credit"
