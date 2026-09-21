import pytest

from scripts.aoss_stage_a.attempt_integrity import (
    AttemptIntegrityError,
    assess_attempt_integrity,
    require_retry_allowed,
)

_DIGEST_A = "a" * 64
_DIGEST_B = "b" * 64
_REQUIRED = ("normal_completion", "policy_denial", "malformed_manifest")


def _kwargs():
    return {
        "expected_source_identity": "source-v1",
        "actual_source_identity": "source-v1",
        "expected_contract_digests": {"policy": _DIGEST_A},
        "actual_contract_digests": {"policy": _DIGEST_A},
        "expected_artifact_digests": {"study": _DIGEST_B},
        "actual_artifact_digests": {"study": _DIGEST_B},
        "required_classes": _REQUIRED,
        "observed_classes": _REQUIRED,
        "outcome_inspected": False,
    }


def test_exact_synthetic_attempt_is_valid_without_promoting_readiness():
    report = assess_attempt_integrity(**_kwargs())

    assert report.status == "VALID_SYNTHETIC_ATTEMPT"
    assert report.retry_allowed is True
    assert report.scientific_n_increment == 0
    assert report.collection_execution_readiness == "NOT_ESTABLISHED"


@pytest.mark.parametrize(
    "mutation",
    ["source", "contract", "artifact", "missing_class", "extra_class"],
)
def test_identity_hash_or_class_drift_invalidates_attempt(mutation):
    kwargs = _kwargs()
    if mutation == "source":
        kwargs["actual_source_identity"] = "source-v2"
    elif mutation == "contract":
        kwargs["actual_contract_digests"] = {"policy": _DIGEST_B}
    elif mutation == "artifact":
        kwargs["actual_artifact_digests"] = {"study": _DIGEST_A}
    elif mutation == "missing_class":
        kwargs["observed_classes"] = _REQUIRED[:-1]
    else:
        kwargs["observed_classes"] = (*_REQUIRED, "unexpected_class")

    report = assess_attempt_integrity(**kwargs)
    assert report.status == "INVALID_SYNTHETIC_ATTEMPT"


def test_retry_is_permanently_blocked_after_outcome_inspection():
    kwargs = _kwargs()
    kwargs["outcome_inspected"] = True
    report = assess_attempt_integrity(**kwargs)

    assert report.retry_allowed is False
    with pytest.raises(AttemptIntegrityError, match="retry after outcome inspection is prohibited"):
        require_retry_allowed(report)


def test_invalid_attempt_after_inspection_still_cannot_retry():
    kwargs = _kwargs()
    kwargs["actual_source_identity"] = "drifted"
    kwargs["outcome_inspected"] = True
    report = assess_attempt_integrity(**kwargs)

    assert report.status == "INVALID_SYNTHETIC_ATTEMPT"
    assert report.retry_allowed is False


def test_invalid_sha256_is_rejected():
    kwargs = _kwargs()
    kwargs["actual_contract_digests"] = {"policy": "not-a-digest"}

    with pytest.raises(AttemptIntegrityError, match="invalid SHA-256"):
        assess_attempt_integrity(**kwargs)


def test_duplicate_required_classes_are_rejected():
    kwargs = _kwargs()
    kwargs["required_classes"] = ("normal_completion", "normal_completion")

    with pytest.raises(AttemptIntegrityError, match="must be unique"):
        assess_attempt_integrity(**kwargs)
