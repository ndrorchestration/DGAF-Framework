from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from tools.validate_evidence_truth_layer import load_card_index, validate_claim_surfaces


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


def card_index(
    *,
    relationship: str = "SPECIFICATION_ONLY",
    canonical_claim_id=None,
    card: str = "pending",
) -> dict:
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


def valid_card() -> dict:
    return {
        "id": "DGAF-CLAIM-A",
        "claim_class": "HYPOTHESIS",
        "evidence_maturity": "SPECIFIED",
        "validation_status": "NOT_VALIDATED",
    }


def test_specification_only_card_does_not_create_operational_claim_state() -> None:
    assert validate_claim_surfaces(canonical_registry(), card_index()) == []


def test_specification_only_card_rejects_canonical_mapping() -> None:
    index = card_index(canonical_claim_id="claim-a")
    failures = validate_claim_surfaces(canonical_registry(), index)
    assert any("SPECIFICATION_ONLY must have canonical_claim_id=null" in failure for failure in failures)


def test_mapped_card_rejects_unknown_canonical_claim() -> None:
    index = card_index(
        relationship="CANONICAL_CLAIM_DETAIL",
        canonical_claim_id="missing",
        card="card.yaml",
    )
    failures = validate_claim_surfaces(canonical_registry(), index, card_loader=lambda _: valid_card())
    assert any("unknown canonical_claim_id=missing" in failure for failure in failures)


def test_mapped_card_requires_materialized_card_target() -> None:
    index = card_index(relationship="CANONICAL_CLAIM_DETAIL", canonical_claim_id="claim-a")
    failures = validate_claim_surfaces(canonical_registry(), index)
    assert any("mapped canonical claim cannot use pending card target" in failure for failure in failures)


def test_hypothesis_cannot_be_silently_promoted_by_mapped_card() -> None:
    index = card_index(
        relationship="CANONICAL_CLAIM_DETAIL",
        canonical_claim_id="claim-a",
        card="card.yaml",
    )
    promoted = valid_card()
    promoted["claim_class"] = "VERIFIED"
    index["cards"][0]["claim_class"] = "VERIFIED"

    failures = validate_claim_surfaces(
        canonical_registry("HYPOTHESIS"),
        index,
        card_loader=lambda _: promoted,
    )
    assert any("canonical HYPOTHESIS claim cannot map to VERIFIED card class" in failure for failure in failures)


def test_index_and_materialized_card_state_must_match() -> None:
    index = card_index(card="card.yaml")
    card = valid_card()
    card["evidence_maturity"] = "TESTED"

    failures = validate_claim_surfaces(canonical_registry(), index, card_loader=lambda _: card)
    assert any("index/card evidence_maturity mismatch" in failure for failure in failures)


def test_duplicate_canonical_mapping_is_rejected() -> None:
    index = card_index(
        relationship="CANONICAL_CLAIM_DETAIL",
        canonical_claim_id="claim-a",
        card="card-a.yaml",
    )
    second = deepcopy(index["cards"][0])
    second["id"] = "DGAF-CLAIM-B"
    second["card"] = "card-b.yaml"
    index["cards"].append(second)

    def loader(path: str) -> dict:
        card = valid_card()
        card["id"] = "DGAF-CLAIM-A" if path == "card-a.yaml" else "DGAF-CLAIM-B"
        return card

    failures = validate_claim_surfaces(canonical_registry(), index, card_loader=loader)
    assert "duplicate canonical claim mapping: claim-a" in failures


def test_current_repository_index_parses_without_external_yaml_dependency() -> None:
    parsed = load_card_index()
    assert parsed["version"] == 2
    assert len(parsed["cards"]) == 5
    assert all(card["relationship"] == "SPECIFICATION_ONLY" for card in parsed["cards"])


def test_index_parser_rejects_nested_structures(tmp_path: Path) -> None:
    path = tmp_path / "index.yaml"
    path.write_text(
        "version: 2\nauthority:\n  role: evidence_card_specification_index\n"
        "cards:\n  - id: DGAF-CLAIM-A\n      nested: forbidden\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="nested card structures are unsupported"):
        load_card_index(path)


def test_index_parser_rejects_tabs(tmp_path: Path) -> None:
    path = tmp_path / "index.yaml"
    path.write_text("version: 2\nauthority:\n\trole: invalid\ncards:\n", encoding="utf-8")
    with pytest.raises(ValueError, match="tabs are not allowed"):
        load_card_index(path)
