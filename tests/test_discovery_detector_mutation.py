import pytest

from dgaf_discovery.detector_mutation import (
    DetectorMutation,
    PropertyCase,
    blindspots_from_survivors,
    run_mutation_campaign,
)
from dgaf_discovery.ledger import validate_blindspot_record


def always_true(_specimen):
    return True


def always_false(_specimen):
    return False


def specimen_ok(specimen):
    return bool(specimen["ok"])


def test_detector_mutation_campaign_kills_weakened_provenance_property():
    cases = (
        PropertyCase(
            case_id="PASS_WITH_PROVENANCE",
            specimen={"decision": "PASS", "evidence": {"predecessor_sha": "abc"}},
            expected_valid=True,
        ),
        PropertyCase(
            case_id="PASS_WITHOUT_PROVENANCE",
            specimen={"decision": "PASS", "evidence": {}},
            expected_valid=False,
        ),
    )

    def canonical(specimen):
        return not (
            specimen.get("decision") == "PASS"
            and not specimen.get("evidence", {}).get("predecessor_sha")
        )

    mutant = DetectorMutation(
        mutation_id="DM-PROV-001",
        family="provenance",
        description="weaken detector so PASS no longer requires predecessor provenance",
        detector=always_true,
    )

    result = run_mutation_campaign(canonical, (mutant,), cases)
    assert result.attempted == 1
    assert result.killed == 1
    assert result.survived == 0
    assert result.score == 1.0
    assert result.results[0].distinguishing_cases == ("PASS_WITHOUT_PROVENANCE",)


def test_detector_mutation_campaign_reports_survivor_when_cases_do_not_distinguish():
    cases = (
        PropertyCase(
            case_id="ONLY_VALID_CASE",
            specimen={"decision": "PASS", "evidence": {"predecessor_sha": "abc"}},
            expected_valid=True,
        ),
    )
    mutant = DetectorMutation(
        mutation_id="DM-PROV-002",
        family="provenance",
        description="undistinguished weakened detector",
        detector=always_true,
    )

    result = run_mutation_campaign(always_true, (mutant,), cases)
    assert result.killed == 0
    assert result.survived == 1
    assert result.score == 0.0
    assert result.results[0].distinguishing_cases == ()


def test_detector_mutation_summary_stratifies_by_family():
    cases = (
        PropertyCase("VALID", {"ok": True}, True),
        PropertyCase("INVALID", {"ok": False}, False),
    )
    mutants = (
        DetectorMutation(
            "DM-AUTH-001",
            "authorization",
            "always allow",
            always_true,
        ),
        DetectorMutation(
            "DM-PROV-003",
            "provenance",
            "equivalent detector",
            specimen_ok,
        ),
    )

    result = run_mutation_campaign(specimen_ok, mutants, cases)
    assert result.by_family["authorization"].attempted == 1
    assert result.by_family["authorization"].killed == 1
    assert result.by_family["provenance"].attempted == 1
    assert result.by_family["provenance"].survived == 1


def test_detector_mutation_outputs_are_non_authorizing():
    cases = (PropertyCase("INVALID", {"ok": False}, False),)
    mutant = DetectorMutation(
        "DM-FAIL-001",
        "fail_open",
        "always allow",
        always_true,
    )

    result = run_mutation_campaign(specimen_ok, (mutant,), cases)
    assert result.authoritative_effect == "NONE"
    assert result.scientific_state_effect == "NONE"
    assert result.scientific_n_increment == 0
    assert result.mutation_scope == "EPHEMERAL_COPY_ONLY"


def test_detector_mutation_rejects_vacuous_campaigns():
    cases = (PropertyCase("VALID", {"ok": True}, True),)
    with pytest.raises(ValueError, match="requires detector mutations"):
        run_mutation_campaign(always_true, (), cases)


def test_detector_mutation_rejects_canonical_oracle_disagreement():
    cases = (PropertyCase("EXPECTED_INVALID", {"ok": False}, False),)
    mutant = DetectorMutation(
        "DM-ORACLE-001",
        "oracle",
        "irrelevant mutant",
        always_false,
    )
    with pytest.raises(ValueError, match="canonical detector disagrees"):
        run_mutation_campaign(always_true, (mutant,), cases)


def test_surviving_mutants_become_candidate_blindspot_records_only():
    cases = (PropertyCase("ONLY_VALID_CASE", {"ok": True}, True),)
    mutants = (
        DetectorMutation("DM-PROV-010", "provenance", "surviving provenance mutant", always_true),
        DetectorMutation("DM-AUTH-010", "authorization", "killed authorization mutant", always_false),
    )
    campaign = run_mutation_campaign(always_true, mutants, cases)

    records = blindspots_from_survivors(campaign, detector_id="property-suite-v1")

    assert len(records) == 1
    record = records[0]
    validate_blindspot_record(record)
    assert record.finding_id == "BLINDSPOT-DM-PROV-010"
    assert record.discovered_by == frozenset({"detector-mutation"})
    assert record.missed_by == frozenset({"property-suite-v1"})
    assert record.reproduction_evidence == ("surviving-mutant:DM-PROV-010",)
    assert record.generated_detector == "provenance"
    assert record.review_status == "CANDIDATE"
    assert record.authoritative_effect == "NONE"


def test_blindspot_conversion_rejects_empty_detector_identity():
    cases = (PropertyCase("ONLY_VALID_CASE", {"ok": True}, True),)
    mutant = DetectorMutation("DM-PROV-011", "provenance", "survivor", always_true)
    campaign = run_mutation_campaign(always_true, (mutant,), cases)

    with pytest.raises(ValueError, match="detector_id is required"):
        blindspots_from_survivors(campaign, detector_id="   ")
