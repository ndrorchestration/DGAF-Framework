import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "registry" / "dgaf_v1_runtime_envelope_candidate.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_runtime_envelope_binds_every_current_api_source() -> None:
    data = load_manifest()
    recorded = {entry["path"] for entry in data["interfaces"]}
    discovered = {
        path.relative_to(ROOT).as_posix()
        for root in (ROOT / "api", ROOT / "pages" / "api")
        for pattern in ("*.py", "*.ts")
        for path in root.glob(pattern)
        if path.is_file()
    }
    assert recorded == discovered

    for entry in data["interfaces"]:
        path = ROOT / entry["path"]
        assert sha256(path) == entry["source_sha256"]


def test_runtime_envelope_has_exactly_one_registered_consequential_action() -> None:
    data = load_manifest()
    assert data["registered_consequential_actions"] == [
        {
            "action_class": "AUDIT_COUNTER_UPDATE_V1",
            "target": "/api/audit",
            "aar_required": True,
            "enforcement_state": "ENFORCED_BOUNDED",
            "replay_class": "PROCESS_LOCAL",
            "revocation_class": "RECORD_LOCAL",
            "trust_anchor_class": "SERVER_HMAC_ENV",
            "issuer_class": "NOT_ESTABLISHED",
            "decision_effect": "NON_SCIENTIFIC_EPHEMERAL_AUDIT_COUNTER_UPDATE_ONLY",
            "limitations": [
                "NO_DURABLE_CROSS_INSTANCE_REPLAY_PREVENTION",
                "NO_AUTHORITATIVE_POST_ISSUANCE_REVOCATION",
                "NO_PRODUCTION_AAR_ISSUER",
                "NO_TRUST_ANCHOR_CUSTODY_ROTATION_POLICY",
                "NO_DURABLE_ACTION_LEDGER",
                "NO_OTHER_ACTION_CLASS_COVERAGE",
            ],
        }
    ]

    source = (ROOT / "app/lib/action-admission.ts").read_text(encoding="utf-8")
    assert "export const AUDIT_ACTION_CLASS = 'AUDIT_COUNTER_UPDATE_V1' as const" in source
    assert "registered_action_classes: [AUDIT_ACTION_CLASS]" in source
    assert "complete: false" in source
    assert "'NO_OTHER_ACTION_CLASS_COVERAGE'" in source


def test_external_ingress_stays_non_authoritative() -> None:
    data = load_manifest()
    assert data["non_authoritative_external_ingress"] == [
        {
            "action_class": "NON_CONSEQUENTIAL_RECORD_INGRESS",
            "transition": "RECORD_ONLY",
            "authority_effect": "NONE",
        },
        {
            "action_class": "CONSEQUENTIAL_ACTION_REQUEST",
            "transition": "REQUEST_ACTION_ADMISSION",
            "authority_effect": "NONE",
        },
    ]

    contract = json.loads(
        (ROOT / "registry/external_runtime_adapter_contract_v1.json").read_text(encoding="utf-8")
    )
    assert contract["status"] == "NON_AUTHORITATIVE_INGRESS_CONTRACT"
    assert contract["authority_semantics"] == "PRESENTED_NOT_GRANTED"
    assert contract["non_effects"]["authorization"] == "NONE"
    assert contract["allowed_action_transitions"] == {
        "NON_CONSEQUENTIAL_RECORD_INGRESS": ["RECORD_ONLY"],
        "CONSEQUENTIAL_ACTION_REQUEST": ["REQUEST_ACTION_ADMISSION"],
    }


def test_excluded_and_blocked_surfaces_remain_explicit() -> None:
    data = load_manifest()
    dispositions = {entry["route"]: entry["classification"] for entry in data["interfaces"]}
    assert dispositions["/api/mandate"] == "EXCLUDED_HARD_DISABLED"
    assert dispositions["/api/staging-breaker"] == "TEST_ONLY_PREVIEW_EXCLUDED_FROM_PRODUCTION"
    assert dispositions["/api/tektite-demo"] == "DEMO_ONLY_WRAPPER"
    assert dispositions["/api/ahg_herald"] == "RELEASE_BLOCKED_OPERATIONAL_INGRESS"

    mandate = (ROOT / "pages/api/mandate.ts").read_text(encoding="utf-8")
    assert "res.status(410)" in mandate
    assert "authority: 'NONE'" in mandate
    assert "state_change: 'DISABLED'" in mandate

    assert data["claim_boundary"] == {
        "release_admission": False,
        "independent_validation": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
    assert {item["id"] for item in data["blocked_release_boundaries"]} == {
        "HERALD_OPERATIONAL_INGRESS",
        "RESEARCH_ARTIFACT_PRODUCERS",
    }
