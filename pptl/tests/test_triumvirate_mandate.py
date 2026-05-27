"""
test_triumvirate_mandate.py — NDR P-09 contract tests.

Covers TriumvirateMandate + PrefectDomain lifecycle.
Markers: triumvirate, governance
"""
import pytest
from unittest.mock import MagicMock, call
from pptl.triumvirate_mandate import PrefectDomain, TriumvirateMandate


# ── Fixtures ────────────────────────────────────────────────────────────

@pytest.fixture
def herald():
    return MagicMock()


@pytest.fixture
def prefect_a():
    return PrefectDomain(
        agent="COLLEEN",
        domain="coherence",
        agents_governed=["Herald", "Echolette"],
    )


@pytest.fixture
def prefect_b():
    return PrefectDomain(
        agent="Apogee",
        domain="quality",
        agents_governed=["DemiJoule", "Sentinel"],
    )


@pytest.fixture
def mandate(herald, prefect_a, prefect_b):
    return TriumvirateMandate(
        prime="Amethyst",
        task="S042 Cycle 2 test",
        scope="DGAF-Framework pptl/",
        constraints=["CI must remain green", "append-only CO_ORCH_QUEUE"],
        prefect_a=prefect_a,
        prefect_b=prefect_b,
        herald=herald,
    )


# ── MECE Guard ──────────────────────────────────────────────────────────

@pytest.mark.triumvirate
@pytest.mark.governance
def test_mece_domain_collision_raises(herald):
    """Contract 2: identical domains must raise ValueError."""
    pa = PrefectDomain(agent="COLLEEN", domain="coherence", agents_governed=["Herald"])
    pb = PrefectDomain(agent="Apogee",  domain="coherence", agents_governed=["DemiJoule"])
    with pytest.raises(ValueError, match="MECE split"):
        TriumvirateMandate(
            prime="Amethyst", task="t", scope="s", constraints=[],
            prefect_a=pa, prefect_b=pb, herald=herald,
        )


@pytest.mark.triumvirate
@pytest.mark.governance
def test_mece_agent_overlap_raises(herald):
    """Contract 2: shared governed agents must raise ValueError."""
    pa = PrefectDomain(agent="COLLEEN", domain="coherence", agents_governed=["Herald", "Reson"])
    pb = PrefectDomain(agent="Apogee",  domain="quality",   agents_governed=["Reson", "DemiJoule"])
    with pytest.raises(ValueError, match="MECE violation"):
        TriumvirateMandate(
            prime="Amethyst", task="t", scope="s", constraints=[],
            prefect_a=pa, prefect_b=pb, herald=herald,
        )


@pytest.mark.triumvirate
@pytest.mark.governance
def test_mandate_id_generated_at_init(mandate):
    """mandate_id must be non-empty string with MANDATE- prefix."""
    assert mandate.mandate_id.startswith("MANDATE-AME-")


# ── Issue ────────────────────────────────────────────────────────────────

@pytest.mark.triumvirate
@pytest.mark.governance
def test_issue_emits_mandate_issued_event(mandate, herald):
    """Contract 1: issue() must emit mandate_issued via HeraldAgent."""
    result = mandate.issue()
    herald.emit.assert_called_once()
    call_kwargs = herald.emit.call_args
    assert call_kwargs.kwargs["event_type"] == "mandate_issued" or \
           call_kwargs.args[0] == "mandate_issued" or \
           call_kwargs[1].get("event_type") == "mandate_issued" or \
           call_kwargs[0][0] == "mandate_issued"
    assert result["prime"] == "Amethyst"
    assert result["mandate_id"] == mandate.mandate_id


@pytest.mark.triumvirate
@pytest.mark.governance
def test_issue_sets_issued_at(mandate):
    """Contract 1: issued_at must be non-empty ISO string after issue()."""
    assert mandate.issued_at == ""
    mandate.issue()
    assert mandate.issued_at != ""


# ── Submit Aggregate ────────────────────────────────────────────────────

@pytest.mark.triumvirate
@pytest.mark.governance
def test_submit_aggregate_before_issue_raises(mandate):
    """Contract 3: aggregate before issue() must raise RuntimeError."""
    with pytest.raises(RuntimeError, match="issued before"):
        mandate.submit_prefect_aggregate("COLLEEN", "report")


@pytest.mark.triumvirate
@pytest.mark.governance
def test_submit_aggregate_both_prefects(mandate, herald):
    """Contract 3: both prefects can submit aggregates after issue."""
    mandate.issue()
    mandate.submit_prefect_aggregate("COLLEEN", "coherence report")
    mandate.submit_prefect_aggregate("Apogee",  "quality report")
    assert mandate.prefect_a.aggregate == "coherence report"
    assert mandate.prefect_b.aggregate == "quality report"


@pytest.mark.triumvirate
@pytest.mark.governance
def test_submit_aggregate_unknown_agent_raises(mandate):
    """Contract 3: unknown agent must raise ValueError."""
    mandate.issue()
    with pytest.raises(ValueError, match="not a Prefect"):
        mandate.submit_prefect_aggregate("Lyra", "interloper report")


# ── Sign Off ────────────────────────────────────────────────────────────

@pytest.mark.triumvirate
@pytest.mark.governance
def test_sign_off_requires_both_aggregates(mandate):
    """Contract 4: sign_off without both aggregates must raise RuntimeError."""
    mandate.issue()
    mandate.submit_prefect_aggregate("COLLEEN", "coherence report")
    with pytest.raises(RuntimeError, match="not submitted"):
        mandate.sign_off()


@pytest.mark.triumvirate
@pytest.mark.governance
def test_full_lifecycle(mandate, herald):
    """Contract 5 (P-01 integration): full lifecycle emits 4 Herald events."""
    mandate.issue()
    mandate.submit_prefect_aggregate("COLLEEN", "coherence report")
    mandate.submit_prefect_aggregate("Apogee",  "quality report")
    result = mandate.sign_off(note="all clear")

    assert mandate.signed_off is True
    assert mandate.signoff_note == "all clear"
    assert result["prime"] == "Amethyst"
    # Herald called: mandate_issued + 2x prefect_aggregate + mandate_signed_off
    assert herald.emit.call_count == 4
    event_types = [c.kwargs.get("event_type") or c.args[0]
                   for c in herald.emit.call_args_list]
    assert "mandate_issued"    in event_types
    assert "prefect_aggregate" in event_types
    assert "mandate_signed_off" in event_types


@pytest.mark.triumvirate
def test_status_report_contains_key_fields(mandate):
    """status_report() must surface mandate_id, prime, task, signed_off."""
    report = mandate.status_report()
    assert mandate.mandate_id in report
    assert "Amethyst" in report
    assert "Signed off: False" in report
