import copy
from types import SimpleNamespace

import pytest

import run_track_a_epoch_002 as r

CANDIDATE = "b" * 40
TREE = "c" * 40
PARENT = "a" * 40
PREFLIGHT_BLOB = "d" * 40
FREEZE_BLOB = "e" * 40
CLOSURE_BLOB = "f" * 40
VERIFY_BLOB = "1" * 40
CUSTODY = {
    "custody_receipt_blob_sha": "2" * 40,
    "custody_certificate_blob_sha": "4" * 40,
    "custody_encrypted_private_key_sha256": "5" * 64,
    "custody_certificate_sha256": "6" * 64,
    "custody_certificate_public_key_der_sha256": "7" * 64,
}


def source_blobs():
    return {path: "3" * 40 for path in r.PROTECTED_SOURCE_PATHS}


def auth():
    return r.expected_authorization(
        authorization_parent_sha=PARENT,
        candidate_sha=CANDIDATE,
        candidate_tree_sha=TREE,
        preflight_blob_sha=PREFLIGHT_BLOB,
        freeze_blob_sha=FREEZE_BLOB,
        closure_blob_sha=CLOSURE_BLOB,
        verification_blob_sha=VERIFY_BLOB,
        custody=CUSTODY,
    )


def preflight():
    return r.expected_preflight(
        candidate_sha=CANDIDATE, candidate_tree_sha=TREE, custody=CUSTODY
    )


def freeze():
    return r.expected_freeze(
        candidate_sha=CANDIDATE,
        candidate_tree_sha=TREE,
        preflight_blob_sha=PREFLIGHT_BLOB,
        protected_source_blobs=source_blobs(),
    )


def closure():
    return r.expected_closure(candidate_sha=CANDIDATE, freeze_blob_sha=FREEZE_BLOB)


def verification():
    return r.expected_verification(
        candidate_sha=CANDIDATE, closure_blob_sha=CLOSURE_BLOB
    )


def public_records(seed=r.SEEDS[0]):
    key = b"x" * 32
    rows = []
    for topology, failure in r.ordered_matrix_cells(seed, key):
        rows.append(
            {
                "protocol_id": r.PROTOCOL_ID,
                "algorithm_id": r.ALGORITHM_ID,
                "frozen_candidate_sha": CANDIDATE,
                "seed_id": seed,
                "blinded_topology_id": r.blind_topology(topology, key),
                "failure_count": failure,
                "ffcr_success": True,
                "excluded": False,
            }
        )
    return rows


def test_exact_successor_records_accept():
    r.validate_preflight(
        preflight(),
        candidate_sha=CANDIDATE,
        candidate_tree_sha=TREE,
        custody=CUSTODY,
    )
    r.validate_freeze(
        freeze(),
        candidate_sha=CANDIDATE,
        candidate_tree_sha=TREE,
        preflight_blob_sha=PREFLIGHT_BLOB,
        protected_source_blobs=source_blobs(),
    )
    r.validate_closure(
        closure(), candidate_sha=CANDIDATE, freeze_blob_sha=FREEZE_BLOB
    )
    r.validate_verification(
        verification(), candidate_sha=CANDIDATE, closure_blob_sha=CLOSURE_BLOB
    )
    r.validate_collection_authorization(
        auth(),
        authorization_parent_sha=PARENT,
        candidate_sha=CANDIDATE,
        candidate_tree_sha=TREE,
        preflight_blob_sha=PREFLIGHT_BLOB,
        freeze_blob_sha=FREEZE_BLOB,
        closure_blob_sha=CLOSURE_BLOB,
        verification_blob_sha=VERIFY_BLOB,
        custody=CUSTODY,
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("record_type", "WRONG"),
        ("schema_version", 2),
        ("protocol_id", "WRONG"),
        ("epoch_id", "TRACK_A_EPOCH_001"),
        ("authorization_parent_sha", "9" * 40),
        ("frozen_candidate_sha", "8" * 40),
        ("frozen_candidate_tree_sha", "7" * 40),
        ("preflight_blob_sha", "6" * 40),
        ("freeze_manifest_blob_sha", "5" * 40),
        ("closure_packet_blob_sha", "4" * 40),
        ("verification_classification_blob_sha", "3" * 40),
        ("preregistration_merge_sha", "2" * 40),
        ("analysis_lock_merge_sha", "1" * 40),
        ("analysis_blob_sha", "0" * 40),
        ("analysis_config_sha256", "0" * 64),
        ("requirements_lock_blob_sha", "9" * 40),
        ("algorithm_id", "DGAF"),
        ("seed_start", 20270101),
        ("seed_end", 20270150),
        ("seed_count", 49),
        ("expected_observations", 9000),
        ("custody_receipt_blob_sha", "8" * 40),
        ("custody_certificate_blob_sha", "7" * 40),
        ("custody_certificate_sha256", "6" * 64),
        ("custody_certificate_public_key_der_sha256", "5" * 64),
        ("custody_class", "INDEPENDENT"),
        ("custody_recovery_drill", "FAIL"),
        ("authorize_empirical_collection", False),
        ("authorize_unblinding", True),
        ("authorize_primary_analysis", True),
        ("historical_pooling_allowed", True),
        ("epoch_004_substitution_allowed", True),
        ("high_assurance_authorized", True),
    ],
)
def test_authorization_mutations_fail_closed(field, value):
    data = auth()
    data[field] = value
    with pytest.raises(SystemExit):
        r.validate_collection_authorization(
            data,
            authorization_parent_sha=PARENT,
            candidate_sha=CANDIDATE,
            candidate_tree_sha=TREE,
            preflight_blob_sha=PREFLIGHT_BLOB,
            freeze_blob_sha=FREEZE_BLOB,
            closure_blob_sha=CLOSURE_BLOB,
            verification_blob_sha=VERIFY_BLOB,
            custody=CUSTODY,
        )


@pytest.mark.parametrize("which", ["missing", "extra"])
def test_authorization_shape_mutations_fail_closed(which):
    data = auth()
    if which == "missing":
        data.pop("algorithm_id")
    else:
        data["legacy_epoch_001_observations"] = True
    with pytest.raises(SystemExit):
        r.validate_collection_authorization(
            data,
            authorization_parent_sha=PARENT,
            candidate_sha=CANDIDATE,
            candidate_tree_sha=TREE,
            preflight_blob_sha=PREFLIGHT_BLOB,
            freeze_blob_sha=FREEZE_BLOB,
            closure_blob_sha=CLOSURE_BLOB,
            verification_blob_sha=VERIFY_BLOB,
            custody=CUSTODY,
        )


@pytest.mark.parametrize("value", [1, 0, "true", "false", None, [], {}, 1.0])
def test_strict_endpoint_rejects_non_boolean(value):
    with pytest.raises(SystemExit):
        r.strict_consensus_success(SimpleNamespace(consensus_success=value))


@pytest.mark.parametrize("value", [True, False])
def test_strict_endpoint_accepts_only_real_boolean(value):
    assert r.strict_consensus_success(SimpleNamespace(consensus_success=value)) is value


@pytest.mark.parametrize(
    "seed", [20270101, 20270150, 20270200, 20270251, 20261001, 0, -1]
)
def test_historical_or_outside_seed_rejected(seed):
    with pytest.raises(ValueError):
        tuple(r.ordered_matrix_cells(seed, b"x" * 32))


def test_keyed_order_is_complete_unique_and_not_public_canonical_order():
    key = b"x" * 32
    actual = r.ordered_matrix_cells(r.SEEDS[0], key)
    canonical = tuple((t, f) for t in r.TOPOLOGIES for f in r.FAILURE_COUNTS)
    assert len(actual) == 45 and len(set(actual)) == 45 and set(actual) == set(canonical)
    assert actual != canonical


def test_keyed_order_changes_with_key():
    assert r.ordered_matrix_cells(
        r.SEEDS[0], b"x" * 32
    ) != r.ordered_matrix_cells(r.SEEDS[0], b"y" * 32)


def test_topology_labels_are_keyed_unique_nonplaintext():
    labels = [r.blind_topology(topology, b"x" * 32) for topology in r.TOPOLOGIES]
    assert len(set(labels)) == 5
    assert all(label.startswith("topology_") for label in labels)
    assert not set(labels) & set(r.TOPOLOGIES)


def test_exact_public_matrix_accepts():
    r.validate_matrix_records(public_records(), seed=r.SEEDS[0])


@pytest.mark.parametrize(
    "mutation",
    [
        "duplicate",
        "missing",
        "extra",
        "wrong_seed",
        "wrong_protocol",
        "wrong_algorithm",
        "malformed_blind",
        "wrong_failure",
        "nonbool_endpoint",
        "excluded",
        "extra_key",
        "missing_key",
    ],
)
def test_public_matrix_negative_controls(mutation):
    rows = public_records()
    if mutation == "duplicate":
        rows[-1] = copy.deepcopy(rows[0])
    elif mutation == "missing":
        rows.pop()
    elif mutation == "extra":
        rows.append(copy.deepcopy(rows[0]))
    elif mutation == "wrong_seed":
        rows[0]["seed_id"] = r.SEEDS[1]
    elif mutation == "wrong_protocol":
        rows[0]["protocol_id"] = "WRONG"
    elif mutation == "wrong_algorithm":
        rows[0]["algorithm_id"] = "DGAF"
    elif mutation == "malformed_blind":
        rows[0]["blinded_topology_id"] = "ring"
    elif mutation == "wrong_failure":
        rows[0]["failure_count"] = 7
    elif mutation == "nonbool_endpoint":
        rows[0]["ffcr_success"] = 1
    elif mutation == "excluded":
        rows[0]["excluded"] = True
    elif mutation == "extra_key":
        rows[0]["topology"] = "ring"
    elif mutation == "missing_key":
        rows[0].pop("algorithm_id")
    with pytest.raises(SystemExit):
        r.validate_matrix_records(rows, seed=r.SEEDS[0])


@pytest.mark.parametrize(
    "record_kind,field,value",
    [
        ("preflight", "preflight_status", "FAIL"),
        ("preflight", "custody_recovery_drill", "FAIL"),
        ("preflight", "custody_receipt_blob_sha", "9" * 40),
        ("preflight", "collection_authorized", True),
        ("preflight", "primary_analysis_authorized", True),
        ("preflight", "scientific_n_increment", 1),
        ("freeze", "freeze_status", "NOT_ESTABLISHED"),
        ("freeze", "collection_authorized", True),
        ("freeze", "frozen_candidate_sha", "9" * 40),
        ("closure", "closure_status", "OPEN"),
        ("closure", "open_blockers", ["x"]),
        ("closure", "collection_authorized", True),
        ("verification", "verification_status", "FAIL"),
        ("verification", "verification_class", "INDEPENDENT"),
        ("verification", "independent_verification", True),
        ("verification", "same_system_custody", False),
        ("verification", "collection_authorized", True),
    ],
)
def test_successor_gate_mutations_fail_closed(record_kind, field, value):
    if record_kind == "preflight":
        data = preflight()
        data[field] = value

        def validate():
            r.validate_preflight(
                data,
                candidate_sha=CANDIDATE,
                candidate_tree_sha=TREE,
                custody=CUSTODY,
            )

    elif record_kind == "freeze":
        data = freeze()
        data[field] = value

        def validate():
            r.validate_freeze(
                data,
                candidate_sha=CANDIDATE,
                candidate_tree_sha=TREE,
                preflight_blob_sha=PREFLIGHT_BLOB,
                protected_source_blobs=source_blobs(),
            )

    elif record_kind == "closure":
        data = closure()
        data[field] = value

        def validate():
            r.validate_closure(
                data, candidate_sha=CANDIDATE, freeze_blob_sha=FREEZE_BLOB
            )

    else:
        data = verification()
        data[field] = value

        def validate():
            r.validate_verification(
                data, candidate_sha=CANDIDATE, closure_blob_sha=CLOSURE_BLOB
            )

    with pytest.raises(SystemExit):
        validate()


@pytest.mark.parametrize(
    "parents,changed",
    [
        ((), (str(r.AUTH_PATH),)),
        ((PARENT, "b" * 40), (str(r.AUTH_PATH),)),
        ((PARENT,), (str(r.AUTH_PATH), "README.md")),
        ((PARENT,), ("README.md",)),
    ],
)
def test_authorization_commit_shape_fail_closed(monkeypatch, parents, changed):
    monkeypatch.setattr(r, "git_head", lambda: "9" * 40)
    monkeypatch.setattr(r, "git_parents", lambda revision="HEAD": parents)
    monkeypatch.setattr(r, "git_changed_paths", lambda revision="HEAD": changed)
    monkeypatch.setattr(r, "git_path_exists_at", lambda path, revision: False)
    monkeypatch.setattr(
        r, "git_path_history", lambda path, revision="HEAD": ("9" * 40,)
    )
    with pytest.raises(SystemExit):
        r.validate_authorization_commit_shape()


def test_authorization_commit_shape_accepts(monkeypatch):
    monkeypatch.setattr(r, "git_head", lambda: "9" * 40)
    monkeypatch.setattr(r, "git_parents", lambda revision="HEAD": (PARENT,))
    monkeypatch.setattr(
        r, "git_changed_paths", lambda revision="HEAD": (str(r.AUTH_PATH),)
    )
    monkeypatch.setattr(r, "git_path_exists_at", lambda path, revision: False)
    monkeypatch.setattr(
        r, "git_path_history", lambda path, revision="HEAD": ("9" * 40,)
    )
    assert r.validate_authorization_commit_shape() == ("9" * 40, PARENT)


def test_custody_artifacts_must_have_single_shared_history_commit(monkeypatch):
    def history(path, revision="HEAD"):
        if path in {str(r.CUSTODY_RECEIPT_PATH), str(r.CUSTODY_CERT_PATH)}:
            return ("8" * 40,)
        return ()

    monkeypatch.setattr(r, "git_path_history", history)
    monkeypatch.setattr(r, "git_is_ancestor", lambda ancestor, descendant: True)
    r.require_custody_history(CANDIDATE, PARENT)


@pytest.mark.parametrize("mode", ["missing", "different", "after_candidate"])
def test_custody_history_mutations_fail_closed(monkeypatch, mode):
    def history(path, revision="HEAD"):
        if mode == "missing" and path == str(r.CUSTODY_RECEIPT_PATH):
            return ()
        if path == str(r.CUSTODY_RECEIPT_PATH):
            return ("8" * 40,)
        if path == str(r.CUSTODY_CERT_PATH):
            return (("7" if mode == "different" else "8") * 40,)
        return ()

    monkeypatch.setattr(r, "git_path_history", history)
    monkeypatch.setattr(
        r,
        "git_is_ancestor",
        lambda ancestor, descendant: False if mode == "after_candidate" else True,
    )
    with pytest.raises(SystemExit):
        r.require_custody_history(CANDIDATE, PARENT)
