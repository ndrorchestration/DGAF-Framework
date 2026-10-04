import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/query_public_claim_evidence_linkage.py"


def load_module():
    spec = importlib.util.spec_from_file_location("query_public_claim_evidence_linkage", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def observation(*claims):
    return {
        "schema_version": "PUBLIC_CLAIM_LINKAGE_OBSERVATION_V0",
        "surface_binding": {
            "manifest_schema_version": "NDR_PUBLIC_SURFACE_MANIFEST_V1",
            "surface_id": "github.profile",
            "source_repository": "ndrorchestration/ndrorchestration",
            "source_commit": "aa42ab2ddd9825938362e76e31b45e306e948c02",
            "source_blob_sha": "373189e9452fe5de555db99dd26648d2be4aa004",
            "copy_state": "RECONCILED",
            "release_gate": "PASS",
            "observed_at": "2026-10-04T15:49:00Z",
        },
        "canonical_authorities": {
            "DGAF": {
                "repository": "ndrorchestration/DGAF-Framework",
                "repository_commit": "3f76c9a93168eed7b366f51ac16481ae53954e27",
            },
            "ACP": {
                "repository": "ndrorchestration/agent-control-plane",
                "repository_commit": "cb264a123cb67ada7616ece4b30172f7d5d59a2f",
            },
            "TEKTITE": {
                "repository": "ndrorchestration/DGAF-Framework",
                "repository_commit": "3f76c9a93168eed7b366f51ac16481ae53954e27",
            },
        },
        "claims": list(claims),
    }


def evidence(repository, commit, path):
    return {
        "repository": repository,
        "repository_commit": commit,
        "path": path,
    }


def claim(
    claim_id="dgaf-epoch-002",
    dependency="DGAF",
    support_state="DIRECT_EVIDENCE_LINKED",
    evidence_refs=None,
    claim_not_supported="Does not establish canonical efficacy or independent validation.",
):
    if evidence_refs is None:
        evidence_refs = [
            evidence(
                "ndrorchestration/DGAF-Framework",
                "3f76c9a93168eed7b366f51ac16481ae53954e27",
                "docs/CURRENT_STATE.md",
            )
        ]
    return {
        "claim_id": claim_id,
        "claim_text": "Track A Epoch 002 completed 50 paired seed units / 2,250 blinded observations.",
        "canonical_dependency": dependency,
        "support_state": support_state,
        "evidence_refs": evidence_refs,
        "claim_not_supported": claim_not_supported,
        "basis": "Current project-local state record directly encodes the bounded result and ceiling.",
    }


def test_direct_linkage_is_bound_to_project_local_authority():
    module = load_module()
    receipt = module.link_claims(observation(claim()))

    row = receipt["claims"][0]
    assert row["support_state"] == "DIRECT_EVIDENCE_LINKED"
    assert row["authority_binding_state"] == "MATCH"
    assert receipt["surface_release_gate"] == "PASS"
    assert receipt["surface_release_gate_effect"] == "NONE"


def test_surface_pass_does_not_upgrade_summary_claim():
    module = load_module()
    summary = claim(
        claim_id="dgaf-broad-summary",
        support_state="INDIRECT_OR_SUMMARY_ONLY",
        evidence_refs=[],
    )
    receipt = module.link_claims(observation(summary))

    assert receipt["claims"][0]["support_state"] == "INDIRECT_OR_SUMMARY_ONLY"
    assert receipt["direct_linkage_complete"] is False
    assert receipt["linkage_state"] == "OBSERVED_WITH_LINKAGE_GAPS"


def test_direct_linkage_requires_evidence_reference():
    module = load_module()
    bad = claim(evidence_refs=[])

    with pytest.raises(ValueError, match="DIRECT_EVIDENCE_LINKED"):
        module.link_claims(observation(bad))


def test_evidence_repository_must_match_declared_authority():
    module = load_module()
    bad = claim(
        evidence_refs=[
            evidence(
                "ndrorchestration/agent-control-plane",
                "cb264a123cb67ada7616ece4b30172f7d5d59a2f",
                "docs/CURRENT_FRONTIER.md",
            )
        ]
    )

    with pytest.raises(ValueError, match="canonical authority"):
        module.link_claims(observation(bad))


def test_evidence_commit_must_match_declared_authority_commit():
    module = load_module()
    bad = claim(
        evidence_refs=[
            evidence(
                "ndrorchestration/DGAF-Framework",
                "0000000000000000000000000000000000000000",
                "docs/CURRENT_STATE.md",
            )
        ]
    )

    with pytest.raises(ValueError, match="authority commit"):
        module.link_claims(observation(bad))


def test_unknown_dependency_is_rejected():
    module = load_module()
    bad = claim(dependency="UNKNOWN_PROJECT")

    with pytest.raises(ValueError, match="canonical_dependency"):
        module.link_claims(observation(bad))


def test_no_direct_evidence_link_remains_visible():
    module = load_module()
    missing = claim(
        claim_id="unmapped-claim",
        support_state="NO_DIRECT_EVIDENCE_LINK",
        evidence_refs=[],
    )
    receipt = module.link_claims(observation(missing))

    assert receipt["claims_without_direct_evidence"] == ["unmapped-claim"]
    assert receipt["direct_linkage_complete"] is False


def test_receipt_preserves_surface_and_non_authority_effects():
    module = load_module()
    receipt = module.link_claims(observation(claim()))

    assert receipt["surface_binding"]["surface_id"] == "github.profile"
    assert receipt["truth_effect"] == "NONE"
    assert receipt["authorization_effect"] == "NONE"
    assert receipt["scientific_state_effect"] == "NONE"
    assert receipt["evidence_authority_effect"] == "NONE"


def test_cli_with_linkage_gap_exits_two(tmp_path):
    import subprocess
    import sys

    observation_path = tmp_path / "observation.json"
    observation_path.write_text(
        json.dumps(
            observation(
                claim(
                    claim_id="summary",
                    support_state="INDIRECT_OR_SUMMARY_ONLY",
                    evidence_refs=[],
                )
            )
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(observation_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2, result.stderr
    receipt = json.loads(result.stdout)
    assert receipt["linkage_state"] == "OBSERVED_WITH_LINKAGE_GAPS"
