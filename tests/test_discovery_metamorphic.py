from dgaf_discovery.metamorphic import (
    PreservationRelation,
    evaluate_preservation,
    provenance_removal_requires_nonpass,
)


def test_presentation_only_change_preserves_authority_fields():
    relation = PreservationRelation(
        relation_id="MR-001",
        protected_paths=("authorization", "scientific_n", "decision"),
    )
    before = {
        "authorization": "NOT_AUTHORIZED",
        "scientific_n": 0,
        "decision": "UNKNOWN",
        "label": "old",
    }
    after = {**before, "label": "new"}
    assert evaluate_preservation(relation, before, after).passed is True

    bad = {**after, "authorization": "AUTHORIZED"}
    result = evaluate_preservation(relation, before, bad)
    assert result.passed is False
    assert result.violations == ("authorization",)


def test_provenance_removal_cannot_retain_pass():
    before = {"decision": "PASS", "evidence": {"predecessor_sha": "abc"}}
    after = {"decision": "PASS", "evidence": {}}
    result = provenance_removal_requires_nonpass(before, after)
    assert result.passed is False
    assert result.violations == ("decision",)

    rejected = {"decision": "NOT_VERIFIED", "evidence": {}}
    assert provenance_removal_requires_nonpass(before, rejected).passed is True
