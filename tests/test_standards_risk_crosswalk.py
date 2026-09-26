"""Contract tests for the initial standards/risk crosswalk."""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = REPO_ROOT / "registry/standards_risk_crosswalk.v0.json"

ALLOWED_STATUSES = {
    "DIRECT_SUPPORT",
    "PARTIAL_SUPPORT",
    "RELATED",
    "NOT_COVERED",
    "NOT_APPLICABLE",
}


def load_crosswalk() -> dict:
    return json.loads(CROSSWALK.read_text(encoding="utf-8"))


def test_crosswalk_is_explicitly_non_certifying() -> None:
    crosswalk = load_crosswalk()
    assert crosswalk["status"] == "INITIAL_PARTIAL_NON_CERTIFYING"
    assert "NO_COMPLIANCE_DETERMINATION" in crosswalk["claim_ceiling"]
    assert "NO_CERTIFICATION" in crosswalk["claim_ceiling"]
    assert "NO_LEGAL_APPLICABILITY_DETERMINATION" in crosswalk["claim_ceiling"]


def test_sources_are_official_and_versioned() -> None:
    crosswalk = load_crosswalk()
    sources = {source["id"]: source for source in crosswalk["sources"]}
    assert sources["NIST_AI_RMF_1_0_CORE"]["official_url"].startswith("https://airc.nist.gov/")
    assert sources["ISO_IEC_42001_2023"]["authority"] == "ISO/IEC"
    assert sources["OWASP_AGENTIC_TOP10_2026"]["official_url"].startswith("https://genai.owasp.org/")
    assert sources["EU_AI_ACT_ARTICLE_14"]["official_url"].startswith("https://eur-lex.europa.eu/")


def test_every_mapping_is_bounded_and_source_bound() -> None:
    crosswalk = load_crosswalk()
    source_ids = {source["id"] for source in crosswalk["sources"]}
    for mapping in crosswalk["mappings"]:
        assert mapping["mapping_status"] in ALLOWED_STATUSES
        assert mapping["source_id"] in source_ids
        assert mapping["dgaf_artifacts"]
        assert mapping["limitations"]


def test_no_initial_mapping_claims_direct_support() -> None:
    crosswalk = load_crosswalk()
    assert all(mapping["mapping_status"] != "DIRECT_SUPPORT" for mapping in crosswalk["mappings"])
