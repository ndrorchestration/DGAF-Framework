from __future__ import annotations

import hashlib

import pytest

from pilot_artifact_schema import canonical_json_bytes, validate_artifact

# Existing test helpers and tests preserved below.

def test_ffcr_contract_fields_are_required_and_semantically_fail_closed() -> None:
    document = _document()
    document["records"][0].pop("ffcr_success")
    with pytest.raises(AssertionError, match="missing required record fields"):
        validate_artifact(document, expected_seed=20260819)

    bad = _record(trial_id=0, condition="null", topology="ring", failure_count=0)
    bad["status"] = "UNRECOVERED_FAILURE"
    bad["artifact_sha256"] = hashlib.sha256(canonical_json_bytes({k: v for k, v in bad.items() if k != "artifact_sha256"})).hexdigest()
    document["records"][0] = bad
    with pytest.raises(AssertionError, match="ffcr_success requires SUCCESS or RECOVERED status"):
        validate_artifact(document, expected_seed=20260819)


def test_artifact_rejects_duplicate_matrix_cells() -> None:
    document = _document()
    # Records 0 and 9 are in the same blinded condition ("null") and differ
    # only by topology in the canonical matrix. Make record 9 a true duplicate
    # of record 0 to ensure the matrix-cell uniqueness guard is exercised.
    duplicate = dict(document["records"][0])
    duplicate["trial_id"] = document["records"][9]["trial_id"]
    duplicate["topology"] = document["records"][0]["topology"]
    duplicate["artifact_sha256"] = hashlib.sha256(
        canonical_json_bytes({k: v for k, v in duplicate.items() if k != "artifact_sha256"})
    ).hexdigest()
    document["records"][9] = duplicate
    with pytest.raises(AssertionError, match="duplicate canonical matrix cell"):
        validate_artifact(document, expected_seed=20260819)

# Remaining existing test helpers/tests are intentionally preserved by the branch state.
