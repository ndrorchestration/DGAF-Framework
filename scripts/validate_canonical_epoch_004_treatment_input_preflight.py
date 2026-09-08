from __future__ import annotations

import ast
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/experiment/CANONICAL_EPOCH_004_TREATMENT_INPUT_PREFLIGHT.json"
PREREG = ROOT / "docs/experiment/CANONICAL_SOLO_EMPIRICAL_EPOCH_004_PREREGISTRATION.json"
PROFILE = ROOT / "docs/governance/CANONICAL_PDMAL_TREATMENT_PROFILE_CANDIDATE_V1.json"
QUAL = ROOT / "docs/qa/APOGEE_11Q_DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1_S077.json"
QUAL_BINDING = ROOT / "docs/qa/APOGEE_11Q_DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1_S077.binding.json"
ANALYSIS = ROOT / "experiments/pdmal_pilot/analysis.py"
TGL = ROOT / "pptl/triadic_governance_loop.py"
OUTPUT = ROOT / "test-artifacts/canonical_epoch_004_treatment_input_preflight.json"

EXPECTED_REQUIRED_STEPS = [1, 2, 3, 4, 5, 6, 8]
EXPECTED_SEEDS = list(range(20261001, 20261051))
HISTORICAL_SEEDS = set(range(20260819, 20260869)) | set(range(20260901, 20260951))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_blob(path: Path) -> str:
    rel = path.relative_to(ROOT)
    return subprocess.check_output(["git", "hash-object", str(rel)], cwd=ROOT, text=True).strip()


def _required_steps_from_source() -> list[int]:
    tree = ast.parse(TGL.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if not any(isinstance(t, ast.Name) and t.id == "REQUIRED_STEPS" for t in node.targets):
                continue
            value = node.value
            if not (
                isinstance(value, ast.Call)
                and isinstance(value.func, ast.Name)
                and value.func.id == "frozenset"
                and len(value.args) == 1
                and isinstance(value.args[0], ast.Set)
            ):
                raise AssertionError("REQUIRED_STEPS source shape changed")
            return sorted(ast.literal_eval(value.args[0]))
    raise AssertionError("REQUIRED_STEPS not found")


def validate() -> dict[str, object]:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    qual = json.loads(QUAL.read_text(encoding="utf-8"))
    binding = json.loads(QUAL_BINDING.read_text(encoding="utf-8"))

    assert contract["record_type"] == "DGAF_CANONICAL_EPOCH_TREATMENT_INPUT_PREFLIGHT_CONTRACT"
    assert contract["epoch_id"] == prereg["epoch_id"] == "PDMAL-SOLO-CANONICAL-EPOCH-004"
    assert prereg["empirical_execution_authorized"] is False
    assert prereg["scientific_n_increment_at_preregistration"] == 0
    assert contract["empirical_execution_authorized"] is False
    assert contract["scientific_n_increment"] == 0

    treatment = prereg["canonical_treatment"]
    assert treatment["profile_id"] == contract["profile_id"]
    assert treatment["profile_merge_sha"] == contract["profile_source_merge_sha"]
    assert treatment["qualification_sha256"] == contract["qualification_sha256"]
    assert treatment["qualification_class"] == contract["qualification_class"]
    assert treatment["reachability_merge_sha"] == contract["reachability_merge_sha"]
    assert treatment["reachability_run_id"] == contract["reachability_run_id"]
    assert treatment["reachability_artifact_id"] == contract["reachability_artifact_id"]
    assert treatment["reachability_artifact_digest"] == contract["reachability_artifact_digest"]
    assert treatment["required_tgl_steps"] == EXPECTED_REQUIRED_STEPS

    assert profile["profile_id"] == contract["profile_id"]
    assert profile["empirical_authorization"] is False
    assert profile["canonical_p30"]["authority"] == "S035_P11_11Q_ATTESTATION"
    assert profile["canonical_p30"]["location"] == "EXTERNAL_GOVERNANCE_PROMOTION_ATTESTATION"
    assert profile["canonical_p30"]["per_turn_scoring"] is False
    assert profile["canonical_p30"]["tgl_step"] == 8
    assert profile["canonical_p30"]["step8_semantics"] == "VERIFY_EXTERNAL_QUALIFICATION_ARTIFACT"
    assert profile["legacy_runtime_gate"]["id"] == "LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1"
    assert profile["legacy_runtime_gate"]["allowed_in_profile"] is False
    assert profile["legacy_runtime_gate"]["status"] == "RETIRED_FROM_CANONICAL_DGAF_TREATMENT"
    assert profile["historical_evidence_policy"]["pool_with_future_canonical_epoch"] is False
    assert _git_blob(PROFILE) == contract["profile_blob_sha"]

    assert _sha256(QUAL) == contract["qualification_sha256"]
    assert binding["qualification_sha256"] == contract["qualification_sha256"]
    assert binding["profile_id"] == contract["profile_id"]
    assert qual["verification_class"] == contract["qualification_class"]
    assert qual["independent_verification"] is False
    assert qual["empirical_evidence"] is False

    assert _required_steps_from_source() == EXPECTED_REQUIRED_STEPS
    assert contract["required_tgl_steps"] == EXPECTED_REQUIRED_STEPS

    assert _git_blob(ANALYSIS) == contract["analysis_blob_sha"]
    assert prereg["primary_analysis"]["statistical_source_blob_sha"] == contract["analysis_blob_sha"]
    assert prereg["primary_analysis"]["analysis_config_sha256"] == contract["analysis_config_sha256"]

    seeds = prereg["matrix"]["seeds"]
    assert seeds == EXPECTED_SEEDS
    assert len(seeds) == len(set(seeds)) == 50
    assert not (set(seeds) & HISTORICAL_SEEDS)
    assert prereg["matrix"]["expected_total_observations"] == contract["expected_observations"] == 9000
    assert prereg["matrix"]["conditions"] == ["null", "simple", "static", "dgaf"]
    assert len(prereg["matrix"]["topologies"]) == 5
    assert prereg["matrix"]["failure_counts"] == [0, 1, 2, 3, 4, 5, 6, 8, 10]

    controls = prereg["collection_controls"]
    assert controls["runner_status"] == "NOT_YET_IMPLEMENTED_OR_AUTHORIZED"
    assert controls["fresh_blinding_key_required"] is True
    assert controls["same_system_key_custody_is_independent"] is False
    assert controls["outcome_inspection_during_collection"] is False
    assert controls["dataset_lock_before_unblinding"] is True
    assert controls["separate_unblinding_authorization_required"] is True
    assert controls["historical_pooling_allowed"] is False
    assert controls["precollection_treatment_input_preflight_required"] is True
    assert controls["exact_frozen_commit_required"] is True
    assert controls["one_file_execution_authorization_required"] is True

    # Reuse the already-governed validators rather than duplicating their semantics.
    subprocess.run(["python", "scripts/validate_canonical_treatment_profile.py"], cwd=ROOT, check=True)
    subprocess.run(["python", "scripts/validate_canonical_profile_11q_qualification.py"], cwd=ROOT, check=True)
    subprocess.run(["python", "scripts/validate_canonical_epoch_004_preregistration.py"], cwd=ROOT, check=True)

    result = {
        "record_type": "DGAF_CANONICAL_EPOCH_TREATMENT_INPUT_PREFLIGHT_RESULT",
        "schema_version": 1,
        "epoch_id": contract["epoch_id"],
        "preflight_id": contract["preflight_id"],
        "status": contract["output_status_on_success"],
        "required_checks": contract["required_checks"],
        "required_tgl_steps": EXPECTED_REQUIRED_STEPS,
        "seed_count": 50,
        "expected_observations_if_later_authorized": 9000,
        "profile_blob_sha": _git_blob(PROFILE),
        "qualification_sha256": _sha256(QUAL),
        "analysis_blob_sha": _git_blob(ANALYSIS),
        "analysis_config_sha256": contract["analysis_config_sha256"],
        "empirical_execution_authorized": False,
        "scientific_n_increment": 0,
        "claim_ceiling": contract["claim_ceiling"],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = validate()
    print(result["status"])
    print("EMPIRICAL_EXECUTION=NOT_AUTHORIZED")
    print("SCIENTIFIC_N_INCREMENT=0")
