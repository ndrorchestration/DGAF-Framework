from dgaf_discovery.detector_mutation import (
    DetectorMutation,
    PropertyCase,
    run_mutation_campaign,
)


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
        detector=lambda specimen: True,
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
    canonical = lambda specimen: True
    mutant = DetectorMutation(
        mutation_id="DM-PROV-002",
        family="provenance",
        description="undistinguished weakened detector",
        detector=lambda specimen: True,
    )

    result = run_mutation_campaign(canonical, (mutant,), cases)
    assert result.killed == 0
    assert result.survived == 1
    assert result.score == 0.0
    assert result.results[0].distinguishing_cases == ()


def test_detector_mutation_summary_stratifies_by_family():
    cases = (
        PropertyCase("VALID", {"ok": True}, True),
        PropertyCase("INVALID", {"ok": False}, False),
    )
    canonical = lambda specimen: bool(specimen["ok"])
    mutants = (
        DetectorMutation("DM-AUTH-001", "authorization", "always allow", lambda specimen: True),
        DetectorMutation("DM-PROV-003", "provenance", "equivalent detector", canonical),
    )

    result = run_mutation_campaign(canonical, mutants, cases)
    assert result.by_family["authorization"].attempted == 1
    assert result.by_family["authorization"].killed == 1
    assert result.by_family["provenance"].attempted == 1
    assert result.by_family["provenance"].survived == 1


def test_detector_mutation_outputs_are_non_authorizing():
    cases = (PropertyCase("INVALID", {"ok": False}, False),)
    canonical = lambda specimen: bool(specimen["ok"])
    mutant = DetectorMutation("DM-FAIL-001", "fail_open", "always allow", lambda specimen: True)

    result = run_mutation_campaign(canonical, (mutant,), cases)
    assert result.authoritative_effect == "NONE"
    assert result.scientific_state_effect == "NONE"
    assert result.scientific_n_increment == 0
    assert result.mutation_scope == "EPHEMERAL_COPY_ONLY"
