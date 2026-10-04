import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "docs/research/fixtures/STRUCTURAL_EPISTEMICS_CLAIM_GRAPH_REFERENCE.json"
SCRIPT = ROOT / "scripts/claimgraph_attribution_query.py"


def load_module():
    spec = importlib.util.spec_from_file_location("claimgraph_attribution_query", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def graph():
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def observation(*records):
    return {
        "record_class": "CLAIMGRAPH_ATTRIBUTION_OBSERVATION_V0",
        "graph_id": "EGRAPH-REFERENCE-001",
        "records": list(records),
    }


def record(
    evidence_id="EVID-REFERENCE-SUPPORT",
    producer_class="INTERNAL_SAME_SYSTEM",
    producer_identity_ref="fixture://producer",
    attribution_state="CLAIMED_UNVERIFIED",
    independence_claimed=False,
    independence_basis_refs=None,
    independence_adjudication_state="NOT_EXECUTED",
    adjudication_ref=None,
):
    if independence_basis_refs is None:
        independence_basis_refs = ["fixture://independence-basis"] if independence_claimed else []
    return {
        "evidence_id": evidence_id,
        "attribution_source_ref": "fixture://attribution",
        "producer_class": producer_class,
        "producer_identity_ref": producer_identity_ref,
        "attribution_state": attribution_state,
        "independence_claimed": independence_claimed,
        "independence_basis_refs": independence_basis_refs,
        "independence_adjudication_state": independence_adjudication_state,
        "adjudication_ref": adjudication_ref,
    }


def test_internal_only_classification_is_declared_not_verified():
    module = load_module()
    receipt = module.query_attribution(graph(), observation(record()))

    assert receipt["receipt_schema_version"] == "claimgraph.attribution-query.v0-candidate"
    assert receipt["truth_effect"] == "NONE"
    assert receipt["authorization_effect"] == "NONE"
    assert receipt["independence_effect"] == "NONE"
    assert receipt["completeness"] == "COMPLETE_FOR_SUPPORTING_EVIDENCE"
    assert receipt["claims_declared_supported_only_by_internal_evidence"] == ["CLAIM-REFERENCE-001"]
    assert receipt["claims_with_unmapped_support"] == []


def test_unmapped_support_fails_closed():
    module = load_module()
    receipt = module.query_attribution(graph(), observation())

    assert receipt["completeness"] == "PARTIAL"
    assert receipt["claims_declared_supported_only_by_internal_evidence"] == []
    assert receipt["claims_with_unmapped_support"] == ["CLAIM-REFERENCE-001"]


def test_external_claimed_unverified_is_not_internal_or_independent():
    module = load_module()
    external = record(
        producer_class="EXTERNAL_HUMAN",
        attribution_state="CLAIMED_UNVERIFIED",
        independence_claimed=True,
    )
    receipt = module.query_attribution(graph(), observation(external))

    assert receipt["claims_declared_supported_only_by_internal_evidence"] == []
    assert receipt["claims_with_external_attribution_claimed_unverified"] == ["CLAIM-REFERENCE-001"]
    assert receipt["claims_with_reported_independently_adjudicated_support"] == []


def test_reported_verified_independence_requires_adjudication_ref():
    module = load_module()
    bad = record(
        producer_class="EXTERNAL_HUMAN",
        attribution_state="REPORTED_VERIFIED",
        independence_claimed=True,
        independence_adjudication_state="REPORTED_VERIFIED_INDEPENDENT",
        adjudication_ref=None,
    )

    with pytest.raises(ValueError, match="adjudication_ref"):
        module.query_attribution(graph(), observation(bad))


def test_same_system_cannot_be_reported_verified_independent():
    module = load_module()
    bad = record(
        producer_class="INTERNAL_SAME_SYSTEM",
        attribution_state="REPORTED_VERIFIED",
        independence_claimed=True,
        independence_adjudication_state="REPORTED_VERIFIED_INDEPENDENT",
        adjudication_ref="fixture://adjudication",
    )

    with pytest.raises(ValueError, match="external producer class"):
        module.query_attribution(graph(), observation(bad))


def test_unknown_evidence_id_is_rejected():
    module = load_module()
    bad = record(evidence_id="EVID-NOT-IN-GRAPH")

    with pytest.raises(ValueError, match="unknown evidence_id"):
        module.query_attribution(graph(), observation(bad))


def test_reported_external_independence_remains_observation_classification_only():
    module = load_module()
    external = record(
        producer_class="EXTERNAL_HUMAN",
        attribution_state="REPORTED_VERIFIED",
        independence_claimed=True,
        independence_adjudication_state="REPORTED_VERIFIED_INDEPENDENT",
        adjudication_ref="fixture://adjudication",
    )
    receipt = module.query_attribution(graph(), observation(external))

    assert receipt["claims_with_reported_independently_adjudicated_support"] == ["CLAIM-REFERENCE-001"]
    assert receipt["independence_effect"] == "NONE"
    assert receipt["observation_authority"] == "CALLER_SUPPLIED_NOT_REVERIFIED"


def test_reported_verified_external_producer_is_visible_without_independence_promotion():
    module = load_module()
    external = record(
        producer_class="EXTERNAL_HUMAN",
        attribution_state="REPORTED_VERIFIED",
        independence_claimed=False,
    )
    receipt = module.query_attribution(graph(), observation(external))

    assert receipt["claims_with_external_support_observed"] == ["CLAIM-REFERENCE-001"]
    assert receipt["claims_with_external_attribution_claimed_unverified"] == []
    assert receipt["claims_with_reported_independently_adjudicated_support"] == []
    assert receipt["independence_effect"] == "NONE"


def test_external_producer_requires_identity_reference():
    module = load_module()
    external = record(producer_class="EXTERNAL_HUMAN")
    external["producer_identity_ref"] = None

    with pytest.raises(ValueError, match="producer_identity_ref"):
        module.query_attribution(graph(), observation(external))


def test_claimed_independence_requires_basis_reference():
    module = load_module()
    external = record(
        producer_class="EXTERNAL_HUMAN",
        independence_claimed=True,
    )
    external["independence_basis_refs"] = []

    with pytest.raises(ValueError, match="independence_basis_refs"):
        module.query_attribution(graph(), observation(external))


def test_duplicate_attribution_mapping_is_rejected():
    module = load_module()
    first = record()
    second = record()

    with pytest.raises(ValueError, match="duplicate evidence attribution"):
        module.query_attribution(graph(), observation(first, second))


def test_graph_binding_mismatch_is_rejected():
    module = load_module()
    wrong = observation(record())
    wrong["graph_id"] = "EGRAPH-OTHER"

    with pytest.raises(ValueError, match="graph_id"):
        module.query_attribution(graph(), wrong)


def test_mixed_internal_external_support_is_not_internal_only():
    module = load_module()
    candidate = graph()
    claim = candidate["claims"][0]
    claim["supporting_evidence_ids"] = [
        "EVID-REFERENCE-SUPPORT",
        "EVID-REFERENCE-COUNTER",
    ]
    claim["contradicting_evidence_ids"] = []
    candidate["relations"][1]["relation_type"] = "SUPPORTS"

    internal = record()
    external = record(
        evidence_id="EVID-REFERENCE-COUNTER",
        producer_class="EXTERNAL_HUMAN",
        attribution_state="REPORTED_VERIFIED",
    )
    receipt = module.query_attribution(candidate, observation(internal, external))

    assert receipt["claims_declared_supported_only_by_internal_evidence"] == []
    assert receipt["claims_with_external_support_observed"] == ["CLAIM-REFERENCE-001"]
    assert receipt["completeness"] == "COMPLETE_FOR_SUPPORTING_EVIDENCE"


def test_internal_producer_requires_identity_reference():
    module = load_module()
    internal = record(producer_identity_ref=None)

    with pytest.raises(ValueError, match="producer_identity_ref"):
        module.query_attribution(graph(), observation(internal))


@pytest.mark.parametrize("producer_class", ["INTERNAL_SAME_SYSTEM", "MIXED", "UNKNOWN"])
def test_only_external_producer_classes_may_claim_independence(producer_class):
    module = load_module()
    candidate = record(
        producer_class=producer_class,
        independence_claimed=True,
    )

    with pytest.raises(ValueError, match="external producer class"):
        module.query_attribution(graph(), observation(candidate))


def test_cli_complete_observation_exits_zero(tmp_path):
    import subprocess
    import sys

    observation_path = tmp_path / "complete.json"
    observation_path.write_text(json.dumps(observation(record())), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(GRAPH_PATH), str(observation_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    receipt = json.loads(result.stdout)
    assert receipt["completeness"] == "COMPLETE_FOR_SUPPORTING_EVIDENCE"


def test_cli_partial_observation_exits_two(tmp_path):
    import subprocess
    import sys

    observation_path = tmp_path / "partial.json"
    observation_path.write_text(json.dumps(observation()), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(GRAPH_PATH), str(observation_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2, result.stderr
    receipt = json.loads(result.stdout)
    assert receipt["completeness"] == "PARTIAL"
