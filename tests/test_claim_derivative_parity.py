from __future__ import annotations

from pathlib import Path

from scripts.propagation_check import CANONICAL_DERIVATIVE, scan_entry


def entry(**overrides):
    base = {
        "id": "claim-a-derivative",
        "claim_pattern": r"Claim A improves outcomes",
        "classification": CANONICAL_DERIVATIVE,
        "canonical_claim_id": "claim-a",
        "historical_allowed": True,
        "historical_markers": ["historical", "archived", "at the time"],
        "context_radius": 220,
    }
    base.update(overrides)
    return base


def claims(status: str = "HYPOTHESIS", run_id=None, provenance=None):
    claim = {
        "claim_id": "claim-a",
        "statement": "Claim A improves outcomes.",
        "status": status,
        "evidence_mode": "empirical",
        "run_id": run_id,
        "dataset": "future",
    }
    if provenance is not None:
        claim["provenance"] = provenance
    return {"claim-a": claim}


def one_status(text: str, *, claim_set=None, configured_entry=None) -> str:
    findings = scan_entry(
        configured_entry or entry(),
        Path("docs/derivative.md"),
        text,
        claim_set or claims(),
    )
    assert len(findings) == 1
    return findings[0]["status"]


def test_hypothesis_derivative_requires_local_status_qualifier() -> None:
    assert one_status("Claim A improves outcomes for deployed systems.") == "ERROR_BARE_CURRENT"
    assert one_status("Claim A improves outcomes; this remains a HYPOTHESIS.") == "PASS_CANONICAL_PARITY"


def test_public_brevity_cannot_remove_nonverified_qualifier() -> None:
    verbose = "Claim A improves outcomes. The claim is NOT ESTABLISHED."
    brief = "Claim A improves outcomes."
    assert one_status(verbose) == "PASS_CANONICAL_PARITY"
    assert one_status(brief) == "ERROR_BARE_CURRENT"


def test_historical_statement_is_not_rewritten_as_current() -> None:
    assert one_status("Historical record: Claim A improves outcomes.") == "ALLOWED_HISTORICAL"
    assert one_status("Current result: Claim A improves outcomes.") == "ERROR_BARE_CURRENT"


def test_stale_run_binding_is_rejected() -> None:
    current = claims(status="VERIFIED", run_id="dpl_CURRENT123")
    assert one_status("Claim A improves outcomes; VERIFIED by dpl_CURRENT123.", claim_set=current) == "PASS_CANONICAL_PARITY"
    assert one_status("Claim A improves outcomes; VERIFIED by dpl_OLD999.", claim_set=current) == "ERROR_STALE_BINDING"


def test_run_token_is_rejected_when_canonical_claim_has_no_run() -> None:
    assert one_status("Claim A improves outcomes; HYPOTHESIS based on dpl_FAKE123.") == "ERROR_STALE_BINDING"


def test_external_attribution_cannot_be_transferred_to_dgaf() -> None:
    external = claims(
        provenance={"source_owner": "External Lab"},
    )
    text = "DGAF demonstrated Claim A improves outcomes."
    assert one_status(text, claim_set=external) == "ERROR_ATTRIBUTION_TRANSFER"


def test_external_attribution_preserved_is_not_flagged_as_transfer() -> None:
    external = claims(
        provenance={"source_owner": "External Lab"},
    )
    text = "External Lab reported Claim A improves outcomes; this remains a HYPOTHESIS."
    assert one_status(text, claim_set=external) == "PASS_CANONICAL_PARITY"


def test_unknown_canonical_claim_fails_closed() -> None:
    configured = entry(canonical_claim_id="missing")
    findings = scan_entry(configured, Path("docs/derivative.md"), "Claim A improves outcomes.", claims())
    assert findings[0]["status"] == "ERROR_UNKNOWN_CANONICAL_CLAIM"


def test_harmless_wording_change_preserves_status_when_pattern_matches() -> None:
    configured = entry(claim_pattern=r"Claim A\s+improves\s+outcomes")
    text = "Claim A   improves outcomes; it is explicitly NOT ESTABLISHED."
    assert one_status(text, configured_entry=configured) == "PASS_CANONICAL_PARITY"


def test_canonical_source_exclusion_contract_is_explicit() -> None:
    # The repository scan excludes evidence/claims.json before scan_entry is called.
    # This fixture guards the intended authority boundary without treating the
    # canonical statement itself as a derivative publication.
    from scripts.propagation_check import CANONICAL_SOURCE

    assert CANONICAL_SOURCE == Path("evidence/claims.json")
