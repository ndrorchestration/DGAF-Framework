from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/experiment/CANONICAL_EPOCH_004_COLLECTION_CONTRACT.json"
PREREG = ROOT / "docs/experiment/CANONICAL_SOLO_EMPIRICAL_EPOCH_004_PREREGISTRATION.json"
PREFLIGHT = ROOT / "docs/experiment/CANONICAL_EPOCH_004_TREATMENT_INPUT_PREFLIGHT.json"
ANALYSIS = ROOT / "experiments/pdmal_pilot/analysis.py"
PROFILE = ROOT / "docs/governance/CANONICAL_PDMAL_TREATMENT_PROFILE_CANDIDATE_V1.json"
QUAL = ROOT / "docs/qa/APOGEE_11Q_DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1_S077.json"


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    c = json.loads(CONTRACT.read_text())
    p = json.loads(PREREG.read_text())
    f = json.loads(PREFLIGHT.read_text())
    assert c["record_type"] == "DGAF_CANONICAL_SOLO_EMPIRICAL_COLLECTION_CONTRACT"
    assert c["epoch_id"] == p["epoch_id"] == f["epoch_id"] == "PDMAL-SOLO-CANONICAL-EPOCH-004"
    assert c["status"] == "CONTRACT_ONLY_NOT_AUTHORIZED"
    assert c["preregistration_merge_sha"] == "ae854edf565c903bf799f243841799819333d920"
    assert c["treatment_input_preflight_merge_sha"] == "15c6621ccab0c28e2938c302d23975ba037bd3ee"
    assert c["treatment_input_preflight_artifact_digest"] == "sha256:810adc623193e7b08c24211585046c1db800717e8d1db2eccb5c56e86f63327c"
    assert c["runner"]["implementation_status"] == "NOT_IMPLEMENTED_IN_THIS_CONTRACT"
    assert c["runner"]["execution_authorization_status"] == "NOT_AUTHORIZED"
    assert c["runner"]["execution_request_status"] == "ABSENT"
    assert c["runner"]["authorization_file_must_be_only_change"] is True
    assert c["runner"]["exact_frozen_commit_required"] is True
    assert c["matrix"]["conditions"] == p["matrix"]["conditions"]
    assert c["matrix"]["topologies"] == p["matrix"]["topologies"]
    assert c["matrix"]["failure_counts"] == p["matrix"]["failure_counts"]
    assert c["matrix"]["seeds"] == p["matrix"]["seeds"] == list(range(20261001, 20261051))
    assert c["matrix"]["expected_total_observations"] == 9000
    assert c["matrix"]["duplicate_cells_allowed"] is False
    assert c["matrix"]["missing_cells_allowed"] is False
    assert c["treatment_binding"]["profile_blob_sha"] == git_blob(PROFILE) == "133d7b71c9e829d5461e7c911527c6b2b10ba9ae"
    assert c["treatment_binding"]["qualification_sha256"] == sha256(QUAL)
    assert c["treatment_binding"]["required_tgl_steps"] == [1, 2, 3, 4, 5, 6, 8]
    assert c["blinding"]["fresh_key_required"] is True
    assert c["blinding"]["plaintext_condition_mapping_in_dataset_prohibited"] is True
    assert c["blinding"]["independent_custody_claim_permitted"] is False
    assert c["collection_behavior"]["outcome_inspection_by_collection_workflow"] is False
    assert c["collection_behavior"]["outcome_aggregation_by_collection_workflow"] is False
    assert c["collection_behavior"]["historical_dataset_pooling"] is False
    assert c["collection_behavior"]["missing_required_treatment_input"] == "ABORT_BEFORE_COLLECTION"
    assert c["retention"]["dataset_status_before_unblinding"] == "LOCKED_BLINDED"
    assert c["retention"]["unblinding_authorized_at_collection_time"] is False
    assert c["retention"]["separate_post_lock_unblinding_authorization_required"] is True
    assert c["analysis_lock"]["statistical_source_blob_sha"] == git_blob(ANALYSIS) == "a269ed226b1d261663994fc3ef0e8a1a96da6cd3"
    assert c["analysis_lock"]["analysis_config_sha256"] == p["primary_analysis"]["analysis_config_sha256"]
    assert c["empirical_execution_authorized"] is False
    assert c["scientific_n_increment"] == 0
    subprocess.run(["python", "scripts/validate_canonical_epoch_004_preregistration.py"], cwd=ROOT, check=True)
    subprocess.run(["python", "scripts/validate_canonical_epoch_004_treatment_input_preflight.py"], cwd=ROOT, check=True)
    print("CANONICAL_EPOCH_004_COLLECTION_CONTRACT_PASS_NOT_AUTHORIZED")
    print("EMPIRICAL_EXECUTION=NOT_AUTHORIZED")
    print("SCIENTIFIC_N_INCREMENT=0")


if __name__ == "__main__":
    main()
