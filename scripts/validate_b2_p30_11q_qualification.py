#!/usr/bin/env python3
"""Validate B2 source-bound P-30/11Q profile qualification."""
from __future__ import annotations
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
QUAL=ROOT/"docs/qa/APOGEE_11Q_DGAF_STATEFUL_CONTEXT_CLOSURE_PROFILE_V1_S079.json"
PROFILE=ROOT/"docs/governance/DGAF_STATEFUL_CONTEXT_CLOSURE_PROFILE_V1.json"
SOURCE=ROOT/"components/ensemble_v17.py"
HARNESS=ROOT/"experiments/pdmal_pilot/b2_stateful_context_closure_profile.py"
TESTS=ROOT/"experiments/pdmal_pilot/test_b2_stateful_context_closure_profile.py"
PROFILE_VALIDATOR=ROOT/"scripts/validate_b2_stateful_context_closure_profile.py"
WORKFLOW=ROOT/".github/workflows/b2-stateful-context-closure-profile.yml"
EXPECTED={
 PROFILE:"306cd38952b979276908789bd042a3e3323c5ac3",
 SOURCE:"686eb9ba339742d9de2767fca18b9907a1c3b70a",
 HARNESS:"765dd5dd50f0590c6ee3c2c805c7e6144c4e86eb",
 TESTS:"a205b878bf17f2160d323aa6e79b31ffa242d6b0",
 PROFILE_VALIDATOR:"294af500f20aec2a40d443fbfb299792a0f61172",
 WORKFLOW:"a239ff486816d1e7b5414334b7342b7a2873c4ee",
}
def blob(p):
 return subprocess.check_output(["git","hash-object",str(p.relative_to(ROOT))],cwd=ROOT,text=True).strip()
q=json.loads(QUAL.read_text())
p=json.loads(PROFILE.read_text())
assert q["record_type"]=="DGAF_P30_11Q_PROFILE_QUALIFICATION"
assert q["profile_id"]==p["profile_id"]=="DGAF_STATEFUL_CONTEXT_CLOSURE_PROFILE_V1"
assert q["verification_class"]=="DEVELOPER_SELF_ATTESTED_NONINDEPENDENT"
assert q["independent_verification"] is False and q["empirical_evidence"] is False
assert q["scientific_n_increment"]==0
for path,expected in EXPECTED.items():
 assert blob(path)==expected, f"source blob drift: {path}"
b=q["source_bindings"]
assert b["profile_merge_sha"]=="9e6971d5c8fc39e46acfe743e6588bbdc127abe8"
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
assert q["next_gate"]["required"]=="B2_NONEMPIRICAL_INTEGRATION_ADJUDICATION"
assert q["next_gate"]["empirical_execution"]=="NOT_AUTHORIZED"
assert q["next_gate"]["canonical_dgaf_efficacy"]=="NOT_ESTABLISHED"
assert q["next_gate"]["high_assurance_changed"] is False
print("B2_P30_11Q_QUALIFICATION_PASS")
