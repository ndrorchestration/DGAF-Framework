import pytest

from scripts.aoss_stage_a.replay import (
    REQUIRED_ARTIFACT_ROLES,
    ReplayVerificationError,
    verify_five_exact_byte_replays,
)


def _bundles():
    return {
        "study_manifest_sha256": b'{"study":"synthetic"}\n',
        "source_episode_bundle_sha256": b'{"source":"synthetic"}\n',
        "normalized_bundle_sha256": b'{"normalized":"synthetic"}\n',
        "decision_bundle_sha256": b'{"decision":"synthetic"}\n',
        "analysis_bundle_sha256": b'{"analysis":"synthetic"}\n',
    }


def test_five_identical_replays_pass_without_independence_or_n_increment():
    expected = _bundles()
    report = verify_five_exact_byte_replays(
        expected,
        [dict(expected) for _ in range(5)],
        source_identity_match=True,
        contract_digest_match=True,
    )

    assert report["status"] == "PASS"
    assert report["replay_pass_count"] == 5
    assert report["replay_passes_count_as_independent_observations"] is False
    assert report["outcomes_generated"] is False
    assert report["scientific_n_increment"] == 0
    assert report["collection_execution_readiness"] == "NOT_ESTABLISHED"
    assert all(item["status"] == "PASS" for item in report["passes"])


@pytest.mark.parametrize("role", REQUIRED_ARTIFACT_ROLES)
def test_tampering_each_artifact_layer_fails_corresponding_replay(role):
    expected = _bundles()
    passes = [dict(expected) for _ in range(5)]
    passes[2][role] = passes[2][role] + b"tamper"

    report = verify_five_exact_byte_replays(
        expected,
        passes,
        source_identity_match=True,
        contract_digest_match=True,
    )

    assert report["status"] == "FAIL"
    assert report["passes"][2]["status"] == "FAIL"


@pytest.mark.parametrize(
    ("source_identity_match", "contract_digest_match"),
    [(False, True), (True, False), (False, False)],
)
def test_source_or_contract_identity_mismatch_fails(
    source_identity_match, contract_digest_match
):
    expected = _bundles()
    report = verify_five_exact_byte_replays(
        expected,
        [dict(expected) for _ in range(5)],
        source_identity_match=source_identity_match,
        contract_digest_match=contract_digest_match,
    )

    assert report["status"] == "FAIL"


def test_missing_artifact_role_schema_rejects():
    expected = _bundles()
    expected.pop("analysis_bundle_sha256")

    with pytest.raises(ReplayVerificationError, match="role set mismatch"):
        verify_five_exact_byte_replays(
            expected,
            [dict(expected) for _ in range(5)],
            source_identity_match=True,
            contract_digest_match=True,
        )


@pytest.mark.parametrize("count", [0, 1, 4, 6])
def test_replay_count_must_be_exactly_five(count):
    expected = _bundles()
    with pytest.raises(ReplayVerificationError, match="exactly five"):
        verify_five_exact_byte_replays(
            expected,
            [dict(expected) for _ in range(count)],
            source_identity_match=True,
            contract_digest_match=True,
        )


def test_non_bytes_artifact_is_rejected():
    expected = _bundles()
    expected["analysis_bundle_sha256"] = {"not": "bytes"}

    with pytest.raises(ReplayVerificationError, match="exact bytes"):
        verify_five_exact_byte_replays(
            expected,
            [dict(expected) for _ in range(5)],
            source_identity_match=True,
            contract_digest_match=True,
        )
