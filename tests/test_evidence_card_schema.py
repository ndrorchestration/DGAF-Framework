import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "docs/evidence/EVIDENCE_CARD_SCHEMA.json").read_text())


def test_worked_evidence_card_matches_schema():
    import yaml

    card = yaml.safe_load((ROOT / "docs/evidence/example-dgaf-claim-v2.yaml").read_text())
    jsonschema.validate(card, SCHEMA)


def test_invalid_claim_class_is_rejected():
    card = {
        "id": "DGAF-CLAIM-INVALID",
        "claim": "x",
        "claim_class": "CERTIFIED",
        "context": {"intended_use": "test"},
        "measurement": {"metric": "x", "method": "test"},
        "provenance": {"source": "test", "recorded_at": "2026-08-17"},
        "evidence_maturity": "SPECIFIED",
        "validation_status": "NOT_VALIDATED",
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(card, SCHEMA)


def test_missing_provenance_is_rejected():
    card = {
        "id": "DGAF-CLAIM-MISSING-PROVENANCE",
        "claim": "x",
        "claim_class": "HYPOTHESIS",
        "context": {"intended_use": "test"},
        "measurement": {"metric": "x", "method": "test"},
        "evidence_maturity": "SPECIFIED",
        "validation_status": "NOT_VALIDATED",
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(card, SCHEMA)


def test_external_reference_role_is_constrained():
    card = {
        "id": "DGAF-CLAIM-BAD-REFERENCE",
        "claim": "x",
        "claim_class": "HYPOTHESIS",
        "context": {"intended_use": "test"},
        "measurement": {"metric": "x", "method": "test"},
        "provenance": {"source": "test", "recorded_at": "2026-08-17"},
        "external_references": [{"source": "example", "role": "proof"}],
        "evidence_maturity": "SPECIFIED",
        "validation_status": "NOT_VALIDATED",
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(card, SCHEMA)
