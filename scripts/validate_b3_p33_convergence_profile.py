#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROFILE=ROOT/"docs/governance/DGAF_P33_GRAPH_CONVERGENCE_MONITOR_PROFILE_V1.json"
SOURCE=ROOT/"components/ensemble_v17.py"
HARNESS=ROOT/"experiments/pdmal_pilot/b3_p33_convergence_profile.py"

EXPECTED_SOURCE_BLOB="686eb9ba339742d9de2767fca18b9907a1c3b70a"
EXPECTED_HARNESS_BLOB="3cb8cfd7aa881be241d03a2d3ce08e10e3b2d8f7"

def blob(path:Path)->str:
    return subprocess.check_output(["git","hash-object",str(path.relative_to(ROOT))],cwd=ROOT,text=True).strip()

def main()->None:
    d=json.loads(PROFILE.read_text(encoding="utf-8"))
    assert d["profile_id"]=="DGAF_P33_GRAPH_CONVERGENCE_MONITOR_PROFILE_V1"
    assert d["controller_issue"]==402
    assert d["status"]=="NONEMPIRICAL_PROFILE_CANDIDATE"
    assert d["source"]["blob_sha"]==EXPECTED_SOURCE_BLOB
    assert blob(SOURCE)==EXPECTED_SOURCE_BLOB
    assert blob(HARNESS)==EXPECTED_HARNESS_BLOB
    assert d["persistence"]=={"lifetime":"ONE_GRAPH_SEQUENCE","reset":"ONLY_AT_SEQUENCE_BOUNDARY"}
    assert d["registered_sequence"]["expected_statuses"]==[
        "stable","watch","warn","alert","stable","stable","converged"
    ]
    assert d["prohibited"]["consensus_alpha_mapping"] is True
    assert d["prohibited"]["dgaf_efficacy_inference"] is True
    assert d["prohibited"]["epoch_004_outcome_reuse"] is True
    assert d["scientific_n_increment"]==0
    assert d["empirical_execution_authorized"] is False
    assert d["high_assurance"]=="NOT_AUTHORIZED_N0"
    print("B3_P33_PROFILE_SOURCE_BINDING_PASS_NONEMPIRICAL")

if __name__=="__main__":
    main()
