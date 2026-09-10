from __future__ import annotations

import json
from pathlib import Path

from scripts import propagation_check as pc

ROOT = Path(__file__).resolve().parents[1]


def _write_minimal_surface(tmp_path: Path, *, status: str = "HYPOTHESIS") -> tuple[Path, Path]:
    claims = {
        "schema_version": "1.1",
        "claims": [
            {
                "claim_id": "example-claim",
                "statement": "Example proposition.",
                "status": status,
                "evidence_mode": "empirical",
                "run_id": None,
                "dataset": "to-be-established",
            }
        ],
    }
    claims_path = tmp_path / "evidence" / "claims.json"
    claims_path.parent.mkdir(parents=True)
    claims_path.write_text(json.dumps(claims), encoding="utf-8")

    card = {
        "id": "DGAF-CLAIM-EXAMPLE",
        "canonical_claim_id": "example-claim",
        "claim": "Example proposition.",
        "claim_class": "HYPOTHESIS" if status != "VERIFIED" else "VERIFIED",
        "context": {"intended_use": "test", "scope": "fixture"},
        "measurement": {"metric": "x", "method": "test"},
        "provenance": {
            "source": "evidence/claims.json#example-claim",
            "recorded_at": "2026-09-10",
        },
        "evidence_maturity": "SPECIFIED" if status != "VERIFIED" else "VERIFIED",
        "validation_status": "NOT_VALIDATED" if status != "VERIFIED" else "VALIDATED_FOR_CONTEXT",
    }
    card_path = tmp_path / "docs" / "evidence" / "claims" / "example-claim.json"
    card_path.parent.mkdir(parents=True)
    card_path.write_text(json.dumps(card), encoding="utf-8")

    index_path = tmp_path / "docs" / "evidence" / "CLAIM_CARD_INDEX.yaml"
    index_path.write_text(
        "\n".join(
            [
                "version: 2",
                "canonical_claim_source: evidence/claims.json",
                "state_authority: evidence/claims.json",
                "cards:",
                "  - id: DGAF-CLAIM-EXAMPLE",
                "    canonical_claim_id: example-claim",
                "    card: docs/evidence/claims/example-claim.json",
                "supplemental_cards:",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return claims_path, index_path


def test_repository_claim_surface_is_structurally_consistent():
    claims_path = ROOT / "evidence" / "claims.json"
    index_path = ROOT / "docs" / "evidence" / "CLAIM_CARD_INDEX.yaml"
    errors, canonical_cards, stats = pc.reconcile_claim_surfaces(ROOT, claims_path, index_path)
    assert errors == []
    assert stats["canonical_claims"] == stats["canonical_cards"] == 5
    assert len(canonical_cards) == 5

    registry = pc.load_registry(ROOT / "registry" / "propagation_registry.json")
    claims = pc.load_claim_registry(claims_path)
    assert pc.validate_registry_claim_bindings(registry, claims) == []


def test_silent_hypothesis_promotion_is_rejected(tmp_path: Path):
    claims_path, index_path = _write_minimal_surface(tmp_path)
    card_path = tmp_path / "docs" / "evidence" / "claims" / "example-claim.json"
    card = json.loads(card_path.read_text(encoding="utf-8"))
    card["claim_class"] = "VERIFIED"
    card["validation_status"] = "VALIDATED_FOR_CONTEXT"
    card["evidence_maturity"] = "VERIFIED"
    card["last_verified"] = "2026-09-10"
    card_path.write_text(json.dumps(card), encoding="utf-8")

    errors, _, _ = pc.reconcile_claim_surfaces(tmp_path, claims_path, index_path)
    assert any("incompatible with canonical status" in error for error in errors)
    assert any("non-verified claim card must be NOT_VALIDATED" in error for error in errors)
    assert any("may not carry last_verified" in error for error in errors)


def test_missing_canonical_mapping_fails_closed(tmp_path: Path):
    claims_path, index_path = _write_minimal_surface(tmp_path)
    index_path.write_text(
        "\n".join(
            [
                "version: 2",
                "canonical_claim_source: evidence/claims.json",
                "state_authority: evidence/claims.json",
                "cards:",
                "supplemental_cards:",
                "",
            ]
        ),
        encoding="utf-8",
    )
    errors, _, _ = pc.reconcile_claim_surfaces(tmp_path, claims_path, index_path)
    assert "example-claim: canonical claim has no Evidence Card mapping" in errors


def test_proposition_drift_is_rejected(tmp_path: Path):
    claims_path, index_path = _write_minimal_surface(tmp_path)
    card_path = tmp_path / "docs" / "evidence" / "claims" / "example-claim.json"
    card = json.loads(card_path.read_text(encoding="utf-8"))
    card["claim"] = "Materially different proposition."
    card_path.write_text(json.dumps(card), encoding="utf-8")

    errors, _, _ = pc.reconcile_claim_surfaces(tmp_path, claims_path, index_path)
    assert "example-claim: Evidence Card proposition differs from canonical statement" in errors


def test_current_propagation_entry_requires_real_canonical_binding():
    claims = {
        "claims": [{"claim_id": "real-claim"}],
    }
    missing = {"entries": [{"id": "a", "classification": "current_claim"}]}
    invented = {
        "entries": [
            {
                "id": "a",
                "classification": "current_claim",
                "canonical_claim_id": "invented-claim",
            }
        ]
    }
    assert any("must bind canonical_claim_id" in e for e in pc.validate_registry_claim_bindings(missing, claims))
    assert any("unknown canonical_claim_id" in e for e in pc.validate_registry_claim_bindings(invented, claims))


def test_bare_derivative_fails_classification_but_qualified_derivative_passes():
    entry = {
        "id": "coordination",
        "canonical_claim_id": "coordination-gain-340",
        "claim_pattern": "340%",
        "qualifiers_any": ["UNVERIFIED", "BLOCKED", "NOT ESTABLISHED"],
        "classification": "current_claim",
        "historical_allowed": True,
        "historical_markers": ["historical"],
        "context_radius": 180,
    }
    bare = pc.scan_entry(entry, Path("public.md"), "DGAF has a 340% coordination gain.")
    qualified = pc.scan_entry(
        entry,
        Path("public.md"),
        "The 340% coordination gain remains UNVERIFIED and is not a current result.",
    )
    assert bare[0]["status"] == "ERROR_BARE_CURRENT"
    assert qualified[0]["status"] == "PASS_QUALIFIED"


def test_canonical_sources_can_be_excluded_from_derivative_scan(tmp_path: Path):
    canonical = tmp_path / "evidence" / "claims.json"
    card = tmp_path / "docs" / "evidence" / "claims" / "example.json"
    derivative = tmp_path / "docs" / "public.md"
    canonical.parent.mkdir(parents=True)
    card.parent.mkdir(parents=True)
    derivative.parent.mkdir(parents=True, exist_ok=True)
    canonical.write_text('{"statement":"340%"}', encoding="utf-8")
    card.write_text('{"claim":"340%"}', encoding="utf-8")
    derivative.write_text("340%", encoding="utf-8")

    files = {
        p.relative_to(tmp_path).as_posix()
        for p in pc.files_under(
            tmp_path,
            {"evidence/claims.json", "docs/evidence/claims/example.json"},
        )
    }
    assert "evidence/claims.json" not in files
    assert "docs/evidence/claims/example.json" not in files
    assert "docs/public.md" in files
