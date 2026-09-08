#!/usr/bin/env python3
"""Validate B3 source-bound P-30/11Q profile qualification."""
from __future__ import annotations
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
QUAL=ROOT/"docs/qa/APOGEE_11Q_DGAF_P33_GRAPH_CONVERGENCE_MONITOR_PROFILE_V1_S080.json"
PROFILE=ROOT/"docs/governance/DGAF_P33_GRAPH_CONVERGENCE_MONITOR_PROFILE_V1.json"
SOURCE=ROOT/"components/ensemble_v17.py"
HARNESS=ROOT/"experiments/pdmal_pilot/b3_p33_convergence_profile.py"
TESTS=ROOT/"experiments/pdmal_pilot/test_b3_p33_convergence_profile.py"
PROFILE_VALIDATOR=ROOT/"scripts/validate_b3_p33_convergence_profile.py"
WORKFLOW=ROOT/".github/workflows/b3-p33-convergence-profile.yml"
EXPECTED={
 PROFILE:"258a490a7e431be9d58e08b88e037ef1d9589ded",
 SOURCE:"686eb9ba339742d9de2767fca18b9907a1c3b70a",
 HARNESS:"3cb8cfd7aa881be241d03a2d3ce08e10e3b2d8f7",
 TESTS:"4c7053dccba13ae0ff420d631701aae875d89694",
 PROFILE_VALIDATOR:"11680dcf0ace99f7abaf94ac83952f25990125fd",
 WORKFLOW:"445fb8765b2c07fb44b960b82f55a95f151f4c31",
}
def blob(p):
 return subprocess.check_output(["git","hash-object",str(p.relative_to(ROOT))],cwd=ROOT,text=True).strip()
q=json.loads(QUAL.read_text())
p=json.loads(PROFILE.read_text())
assert q["record_type"]=="DGAF_P30_11Q_PROFILE_QUALIFICATION"
assert q["profile_id"]==p["profile_id"]=="DGAF_P33_GRAPH_CONVERGENCE_MONITOR_PROFILE_V1"
assert q["verification_class"]=="DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
assert q["independent_verification"] is False and q["empirical_evidence"] is False
assert q["scientific_n_increment"]==0
for path,expected in EXPECTED.items():
 assert blob(path)==expected, f"source blob drift: {path}"
b=q["source_bindings"]
assert b["profile_merge_sha"]=="114312db125439ae861065e36d3b0d37ffe32d14"
assert b["profile_blob_sha"]==EXPECTED[PROFILE]
assert b["source_blob_sha"]==EXPECTED[SOURCE]
assert b["harness_blob_sha"]==EXPECTED[HARNESS]
assert b["test_blob_sha"]==EXPECTED[TESTS]
assert b["validator_blob_sha"]==EXPECTED[PROFILE_VALIDATOR]
assert b["workflow_blob_sha"]==EXPECTED[WORKFLOW]
scores=q["scoring"]
assert set(scores)=={f"Q{i:02d}" for i in range(1,12)}
assert sum(v["score"] for v in scores.values())==q["scoring_summary"]["total_score"]==108
assert q["scoring_summary"]["max_score"]==110
assert q["scoring_summary"]["tier"]=="S-TIER"
assert q["scoring_summary"]["q11_score"]==scores["Q11"]["score"]==9
assert q["scoring_summary"]["attestation_result"]=="GRANTED"
assert p["scientific_n_increment"]==0 and p["empirical_execution_authorized"] is False
assert q["next_gate"]["required"]=="B3_NONEMPIRICAL_INTEGRATION_ADJUDICATION"
assert q["next_gate"]["empirical_execution"]=="NOT_AUTHORIZED"
assert q["next_gate"]["canonical_dgaf_efficacy"]=="NOT_ESTABLISHED"
assert q["next_gate"]["high_assurance_changed"] is False
print("B3_P30_11Q_QUALIFICATION_PASS")
