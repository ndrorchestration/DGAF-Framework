from src.evidence_mode import can_satisfy, evidence_mode, evidence_rank


def test_evidence_rank_is_ordered():
    assert evidence_rank("synthetic") < evidence_rank("integration")
    assert evidence_rank("integration") < evidence_rank("empirical")
    assert evidence_rank("empirical") < evidence_rank("production")


def test_weaker_evidence_cannot_satisfy_stronger_claim():
    assert can_satisfy("synthetic", "synthetic")
    assert can_satisfy("integration", "synthetic")
    assert not can_satisfy("synthetic", "empirical")
    assert not can_satisfy("integration", "production")
    assert can_satisfy("production", "empirical")


def test_decorator_attaches_machine_readable_metadata():
    @evidence_mode("empirical", claim_id="DGAF-TEST-001")
    def run():
        return True

    metadata = getattr(run, "__evidence_metadata__")
    assert metadata.mode == "empirical"
    assert metadata.claim_id == "DGAF-TEST-001"
    assert metadata.run_id_required is True
    assert metadata.dataset_required is True
