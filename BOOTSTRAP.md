# BOOTSTRAP.md — DGAF Workspace Quickstart

> **Version:** 2.0.0 | **Last updated:** 2026-06-26 | **Authority:** Amethyst (QA) × COLLEEN (Evaluation)

This is the single-file workspace bootstrap for any new session, agent instantiation, or onboarding run. Read this first. Everything else is reachable from here.

---

## 1. Workspace Identity

| Field | Value |
|---|---|
| Framework | DGAF — Dynamic Governance Agentic Formation Architecture |
| Primary repo | `ndrorchestration/DGAF-Framework` |
| Governance model | Triadic / Constitutional Cognition |
| Co-orchestration pair | Amethyst (QA lens) × COLLEEN (Evaluation/Archive lens) |
| Safety supervisor | Sentinel-Phi |
| Trace/audit sink | Herald → JSONL + n8n webhook |
| Pattern authority | COLLEEN (Librarian/Auditor/Actualizer) |

---

## 2. First-Run Checklist (Every Session)

- [ ] Read `SESSION_ANCHOR.md` — confirms last known state, open items, active cycle
- [ ] Read `CO_ORCH_QUEUE.md` — confirms active OPP batch and cycle number
- [ ] Read `registry/PATTERN_REGISTRY_v2.md` — confirms active patterns
- [ ] Read `CROSS_REF.md` — confirms cross-repo alignment
- [ ] Read `CHANGELOG.md` — confirms last committed changes
- [ ] Check `SWEEP_LOG/` — read most recent sweep file
- [ ] Confirm `docs/RD_GAPS.md` — check open R&D items before proceeding

---

## 3. Canonical File Map

```
DGAF-Framework/
├── BOOTSTRAP.md                    ← YOU ARE HERE
├── SESSION_ANCHOR.md               ← Session state, open items, last stamp
├── CHANGELOG.md                    ← All commits, versioned
├── CO_ORCH_PROTOCOL.md             ← 7-step execution flow, triad roles
├── CO_ORCH_QUEUE.md                ← Active OPP improvement queue
├── CROSS_REF.md                    ← Cross-repo alignment map
├── ENSEMBLE_ROSTER.md              ← All agents, roles, L-levels
├── AGENT_MANIFEST.md               ← Agent instantiation contracts
├── AGENT_INSTANTIATION.md          ← Instantiation procedures
├── GRADUATION_REPORT.md            ← S042 graduation record
├── README.md                       ← Public-facing overview
├── README.governance.md            ← Governance protocol reference
├── README.technical.md             ← Technical architecture reference
├── patterns/                       ← NDR pattern files (P-*.md)
├── registry/
│   ├── PATTERN_REGISTRY_v2.md      ← Master pattern registry
│   └── AMETHYST_COLLEEN_CO_ORCH_CONTRACT_v1.json
├── docs/
│   ├── TEAM_WIKI.md                ← Team onboarding, roles, governance map
│   └── RD_GAPS.md                  ← Open R&D gap log
├── SWEEP_LOG/
│   └── SWEEP_2026-06-26_*.md       ← Per-session sweep logs
├── pptl/                           ← Phi-pentagon test layer
├── tests/                          ← pytest governance harness
└── scripts/                        ← Automation scripts
```

---

## 4. Authority Order

1. User instruction
2. Space instruction (Agent Amethyst as host)
3. Portfolio governance rules + Apogee Lens review
4. DGAF / PDMAL operating constraints
5. Default assistant behavior

---

## 5. Non-Negotiables

- Refresh memory before synthesis
- Pattern registry updated before implementation
- All outputs paired with coherence + quality sweep
- No S-Tier or Gold Star until Apogee Lens approval
- All logging, documentation, storage, and GitHub repos updated per session
- Irreversible actions require HITL gate before commit
- COLLEEN archives every session episode; Amethyst QA-stamps every push

---

## 6. Quick-Start for Agents

```python
# Minimal session bootstrap
from dgaf.bootstrap import load_session_anchor, load_co_orch_queue, load_pattern_registry

anchor = load_session_anchor()          # SESSION_ANCHOR.md
queue  = load_co_orch_queue()           # CO_ORCH_QUEUE.md
reg    = load_pattern_registry()        # registry/PATTERN_REGISTRY_v2.md

print(f"Active cycle: {queue['active_cycle']}")
print(f"Open OPPs: {[o for o in queue['opps'] if o['status'] == 'OPEN']}")
print(f"Active patterns: {len(reg['patterns'])}")
```

---

## 7. Escalation Contacts

| Trigger | Route To |
|---|---|
| Governance breach | Sentinel-Phi → Amethyst |
| Coherence failure | COLLEEN → Amethyst |
| Safety / ethics | DemiJoule |
| Architectural decision | Reson → Amethyst |
| Human approval required | HITL queue → User |
