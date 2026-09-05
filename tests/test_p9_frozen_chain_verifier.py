from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_p9_frozen_chain.py"
SPEC = importlib.util.spec_from_file_location("verify_p9_frozen_chain", SCRIPT)
assert SPEC and SPEC.loader
p9 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p9)

CANDIDATE_SHA = "1" * 40
CANDIDATE_TREE = "2" * 40
DEPLOYMENT = "dpl_test_candidate"
CONTROL_PLANE = "3" * 40
FREEZE_COMMIT = "4" * 40
ANALYSIS_BLOB = "5" * 40
RUNNER_BLOB = "6" * 40
SCHEMA_BLOB = "7" * 40
PROTOCOL_BLOB = "8" * 40
CONFIG_SHA = "9" * 64
PROTOCOL_CONTENT = "a" * 64
EVIDENCE_SHA = "b" * 64
KEY_COMMITMENT = "c" * 64
MAPPING_COMMITMENT = "d" * 64
ATTESTATION_SHA = "e" * 64
NO_ACCESS_SHA = "f" * 64
REVIEW_SHA = "0" * 64
FREEZE_VERIFY_SHA = "1" * 64


def _candidate_manifest() -> str:
    return f"""# candidate\n\n```yaml\ncandidate_sha: {CANDIDATE_SHA}\ncandidate_tree_sha: {CANDIDATE_TREE}\ndeployment_binding:\n  deployment_id: {DEPLOYMENT}\n```\n"""


def _p7(status: str = "CLOSED") -> str:
    return f"""# P7\n\n```yaml\nstatus: "{status}"\ncandidate_sha: "{CANDIDATE_SHA}"\ncandidate_tree_sha: "{CANDIDATE_TREE}"\ndeployment_id: "{DEPLOYMENT}"\nprotocol_version: "0.7.5"\nanalysis_blob_sha: "{ANALYSIS_BLOB}"\nanalysis_config_sha256: "{CONFIG_SHA}"\nrunner_blob_sha: "{RUNNER_BLOB}"\nartifact_schema_blob_sha: "{SCHEMA_BLOB}"\n```\n"""


def _freeze() -> dict:
    return {
        "schema_version": 1,
        "record_type": "PDMAL_IMMUTABLE_FREEZE",
        "freeze_state": "FROZEN",
        "accepted_control_plane_commit": CONTROL_PLANE,
        "candidate": {
            "sha": CANDIDATE_SHA,
            "tree_sha": CANDIDATE_TREE,
            "deployment_id": DEPLOYMENT,
        },
        "apparatus": {
            "source_sha": "a" * 40,
            "p35_boundary_sha": "b" * 40,
        },
        "protocol": {
            "version": "0.7.5",
            "blob_sha": PROTOCOL_BLOB,
            "content_sha256": PROTOCOL_CONTENT,
        },
        "analysis": {
            "implementation_blob_sha": ANALYSIS_BLOB,
            "config_sha256": CONFIG_SHA,
            "runner_blob_sha": RUNNER_BLOB,
            "artifact_schema_blob_sha": SCHEMA_BLOB,
        },
        "predicates": {
            name: {
                "status": "CLOSED / VERIFIED",
                "evidence": [{"id": f"evidence-{name}", "sha256": EVIDENCE_SHA}],
            }
            for name in p9.REQUIRED_PREDICATES
        },
        "p4_custody": {
            "status": "CLOSED / VERIFIED",
            "custodian_id": "human-custodian",
            "execution_principal_id": "human-executor",
            "key_commitment_sha256": KEY_COMMITMENT,
            "mapping_commitment_sha256": MAPPING_COMMITMENT,
            "custodian_attestation_sha256": ATTESTATION_SHA,
            "execution_no_access_attestation_sha256": NO_ACCESS_SHA,
            "independent_custody_review_sha256": REVIEW_SHA,
        },
        "independent_freeze_verification": {
            "status": "PASS",
            "verifier_id": "independent-freeze-verifier",
            "evidence_sha256": FREEZE_VERIFY_SHA,
        },
        "pilot_authorization": {"status": "NOT_GRANTED", "record_id": None},
        "empirical_execution": {"status": "NOT_EXECUTED", "n": 0},
        "unblinding": {"status": "NOT_EXECUTED"},
    }


def _write_controls(tmp_path: Path, *, p7_status: str = "CLOSED") -> tuple[Path, Path]:
    candidate = tmp_path / "candidate.md"
    p7_path = tmp_path / "p7.md"
    candidate.write_text(_candidate_manifest(), encoding="utf-8")
    p7_path.write_text(_p7(p7_status), encoding="utf-8")
    return candidate, p7_path


def _verify(tmp_path: Path, freeze: dict, *, p7_status: str = "CLOSED") -> dict:
    candidate, p7_path = _write_controls(tmp_path, p7_status=p7_status)
    raw = json.dumps(freeze, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(raw).hexdigest()
    return p9.validate_freeze(
        freeze_bytes=raw,
        expected_sha256=digest,
        candidate_manifest=candidate,
        p7_binding=p7_path,
        freeze_commit_sha=FREEZE_COMMIT,
    )


def test_valid_frozen_chain_passes(tmp_path: Path) -> None:
    result = _verify(tmp_path, _freeze())
    assert result["result"] == "PASS"
    assert result["empirical_n"] == 0
    assert result["pilot_authorization"] == "NOT_GRANTED"


def test_open_p7_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(p9.VerificationError, match="P7 must be CLOSED"):
        _verify(tmp_path, _freeze(), p7_status="OPEN")


def test_digest_mismatch_fails_closed(tmp_path: Path) -> None:
    candidate, p7_path = _write_controls(tmp_path)
    raw = json.dumps(_freeze(), sort_keys=True).encode()
    with pytest.raises(p9.VerificationError, match="byte SHA-256"):
        p9.validate_freeze(
            freeze_bytes=raw,
            expected_sha256="0" * 64,
            candidate_manifest=candidate,
            p7_binding=p7_path,
            freeze_commit_sha=FREEZE_COMMIT,
        )


def test_candidate_substitution_fails_closed(tmp_path: Path) -> None:
    freeze = _freeze()
    freeze["candidate"]["sha"] = "f" * 40
    with pytest.raises(p9.VerificationError, match="canonical manifest"):
        _verify(tmp_path, freeze)


def test_same_human_cannot_fill_both_p4_roles(tmp_path: Path) -> None:
    freeze = _freeze()
    freeze["p4_custody"]["execution_principal_id"] = freeze["p4_custody"]["custodian_id"]
    with pytest.raises(p9.VerificationError, match="must be distinct"):
        _verify(tmp_path, freeze)


def test_authorized_or_empirical_state_is_rejected_during_p9(tmp_path: Path) -> None:
    authorized = _freeze()
    authorized["pilot_authorization"] = {"status": "GRANTED", "record_id": "auth-1"}
    with pytest.raises(p9.VerificationError, match="NOT_GRANTED"):
        _verify(tmp_path, authorized)

    empirical = copy.deepcopy(_freeze())
    empirical["empirical_execution"] = {"status": "EXECUTED", "n": 1}
    with pytest.raises(p9.VerificationError, match="NOT_EXECUTED"):
        _verify(tmp_path, empirical)


def test_freeze_cannot_self_embed_its_creating_commit(tmp_path: Path) -> None:
    freeze = _freeze()
    freeze["accepted_control_plane_commit"] = FREEZE_COMMIT
    with pytest.raises(p9.VerificationError, match="self-embedded freeze commit"):
        _verify(tmp_path, freeze)
