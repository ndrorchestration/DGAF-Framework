#!/usr/bin/env python3
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"docs/governance/DGAF_STATEFUL_CONTEXT_CLOSURE_PROFILE_V1.json"
S=ROOT/"components/ensemble_v17.py"
H=ROOT/"experiments/pdmal_pilot/b2_stateful_context_closure_profile.py"
def blob(p): return subprocess.check_output(["git","hash-object",str(p.relative_to(ROOT))],cwd=ROOT,text=True).strip()
d=json.loads(P.read_text())
assert d["profile_id"]=="DGAF_STATEFUL_CONTEXT_CLOSURE_PROFILE_V1"
assert blob(S)=="686eb9ba339742d9de2767fca18b9907a1c3b70a"
assert blob(H)=="765dd5dd50f0590c6ee3c2c805c7e6144c4e86eb"
assert d["registered_phi_checkpoints"]==[13,21,34,55]
assert d["known_source_limitation"]["silent_redesign_allowed"] is False
assert d["scientific_n_increment"]==0 and d["empirical_execution_authorized"] is False
print("B2_STATEFUL_CONTEXT_CLOSURE_PROFILE_PASS_NONEMPIRICAL")
