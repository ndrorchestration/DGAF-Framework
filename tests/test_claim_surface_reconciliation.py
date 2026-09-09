from __future__ import annotations

from copy import deepcopy

from tools.validate_evidence_truth_layer import validate_claim_surfaces


def canonical_registry(status: str = "HYPOTHESIS") -> dict:
    return {
        "schema_version": "1.1",
        "authority": {
            "claim_identity_and_state": "CANONICAL",
            "evidence_card_relationship": "EXPLICIT_REFERENCE_ONLY",
            "card_index": "docs/evidence/CLAIM_CARD_INDEX.yaml",
        },
        "claims": [
            {
                "claim_id": "claim-a",
                "statement": "Claim A",
                "status": status,
                "evidence_mode": "empirical",
                "run_id": None,
                "dataset": "future",
            }
        ],
    }


def card_index(*, relationship: str = "SPECIFICATION_ONLY", canonical_claim_id=None, card: str = "pending") -> dict:
    return {
        "version": 2,
        "authority": {
            "role": "evidence_card_specification_index",
            "canonical_claim_identity_and_state": "evidence/claims.json",
            "mapping_field": "canonical_claim_id",
        },
        "cards": [
            {
                "id": "DGAF-CLAIM-A",
                "card": card,
                "relationship": relationship,
                "canonical_claim_id": canonical_claim_id,
                "claim_class": "HYPOTHESIS",
                "evidence_maturity": "SPECIFIED",
                "validation_status": "NOT_VALIDATED",
            }
        ],
    }


def load_valid_card(_: str) -> dict:
    return {
        "id": "DGAF-CLAIM-A",
        "claim": "Claim A detail",
        "claim_class": "HYPOTHESIS",
        "context": {"intended_use": "test"},
        "measurement": {"metric": "x", "method": "test"},
        "provenance": {"source": "test", "recorded_at": "2026-09-09"},
        "evidence_maturity": "SPECIFIED",
        "validation_status": "NOT_VALIDATED",
    }


def test_specification_only_card_does_not_create_operational_claim_state() -> None:
    failures = validate_claim_surfaces(canonical_registry(), card_index())
    assert failures == []


def test_specification_only_card_rejects_canonical_claim_mapping() -> None:
    index = card_index(canonical_claim_id="claim-a")
    failures = validate_claim_surfaces(canonical_registry(), index)
    assert any("SPECIFICATION_ONLY must have canonical_claim_id=null" in failure for failure in failures)


def test_mapped_card_rejects_unknown_canonical_claim() -> None:
    index = card_index(relationship="CANONICAL_CLAIM_DETAIL", canonical_claim_id="missing", card="card.yaml")
    failures = validate_claim_surfaces(canonical_registry(), index, card_loader=load_valid_card)
    assert any("unmapped canonical_claim_id=missing" in failure for failure in failures)


def test_mapped_card_requires_materialized_card_target() -> None:
    index = card_index(relationship="CANONICAL_CLAIM_DETAIL", canonical_claim_id="claim-a")
    failures = validate_claim_surfaces(canonical_registry(), index)
    assert any("mapped canonical claim cannot use pending card target" in failure for failure in failures)


def test_hypothesis_cannot_be_silently_promoted_by_mapped_card() -> None:
    index = card_index(relationship="CANONICAL_CLAIM_DETAIL", canonical_claim_id="claim-a", card="card.yaml")
    promoted = load_valid_card("card.yaml")
    promoted["claim_class"] = "VERIFIED"
    index["cards"][0]["claim_class"] = "VERIFIED"

    failures = validate_claim_surfaces(canonical_registry("HYPOTHESIS"), index, card_loader=lambda _: promoted)
    assert any("canonical HYPOTHESIS claim cannot be mapped to VERIFIED card class" in failure for failure in failures)


def test_index_and_materialized_card_state_must_match() -> None:
    index = card_index(card="card.yaml")
    card = load_valid_card("card.yaml")
    card["evidence_maturity"] = "TESTED"

    failures = validate_claim_surfaces(canonical_registry(), index, card_loader=lambda _: card)
    assert any("index/card evidence_maturity mismatch" in failure for failure in failures)


def test_duplicate_canonical_mapping_is_rejected() -> None:
    index = card_index(relationship="CANONICAL_CLAIM_DETAIL", canonical_claim_id="claim-a", card="card.yaml")
    second = deepcopy(index["cards"][0])
    second["id"] = "DGAF-CLAIM-B"
    index["cards"].append(second)

    def loader(path: str) -> dict:
        card = load_valid_card(path)
        card["id"] = "DGAF-CLAIM-A" if len(path) else "DGAF-CLAIM-B"
        return card

    # Use matching card IDs so the duplicate mapping is isolated from target-ID validation.
    def matching_loader(_: str) -> dict:
        return load_valid_card("card.yaml")

    failures = validate_claim_surfaces(canonical_registry(), index, card_loader=matching_loader)
    assert any("duplicate canonical claim mapping: claim-a" in failure for failure in failures)
