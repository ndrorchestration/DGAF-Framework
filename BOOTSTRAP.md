# BOOTSTRAP.md — DGAF Workspace Quickstart

> **Version:** 2.1.0 | **Last updated:** 2026-08-15 | **Status:** Project-local operating document

This is the workspace bootstrap for a new session, agent instantiation, or onboarding run. It identifies the current project-local operating order and points to the evidence and audit surfaces that must be checked before synthesis.

---

## 1. Workspace Identity

| Field | Value |
|---|---|
| Framework | DGAF — Dynamic Governance Agentic Formation |
| Primary repo | `ndrorchestration/DGAF-Framework` |
| Governance model | Project-local multi-agent governance/orchestration model |
| Co-orchestration pair | Amethyst (QA lens) × COLLEEN (Evaluation/Archive lens) |
| Safety supervisor | Sentinel-Phi (project role) |
| Trace/audit sink | Herald → JSONL + n8n webhook |
| Pattern authority | COLLEEN (project-local Librarian/Auditor/Actualizer role) |

**Epistemic boundary:** Project personas, governance roles, tiers, and approval labels are internal mechanisms. They are not independent certification authorities and do not establish legal compliance, external accreditation, or production readiness by themselves.

---

## 2. First-Run Checklist (Every Session)

- [ ] Read `SESSION_ANCHOR.md` — confirms last known state, open items, active cycle
- [ ] Read `CO_ORCH_QUEUE.md` — confirms active OPP batch and cycle number
- [ ] Read `registry/PATTERN_REGISTRY_v2.md` — confirms active patterns
- [ ] Read `CROSS_REF.md` — confirms cross-repo alignment
- [ ] Read `CHANGELOG.md` — confirms last committed changes
- [ ] Check `SWEEP_LOG/` — read most recent sweep file
- [ ] Confirm `docs/RD_GAPS.md` — check open R&D items before proceeding
- [ ] Classify new material using the project evidence ladder before treating it as established fact

---

## 3. Canonical File Map

```
DGAF-Framework/
├── BOOTSTRAP.md                    ← YOU ARE HERE
├── SESSION_ANCHOR.md               ← Session state, open items, last stamp
├── CHANGELOG.md                    ← All commits, versioned
├── CO_ORCH_PROTOCOL.md             ← Execution flow, triad roles
├── CO_ORCH_QUEUE.md                ← Active OPP improvement queue
├── CROSS_REF.md                    ← Cross-repo alignment map
├── ENSEMBLE_ROSTER.md              ← Agents, roles, L-levels
├── AGENT_MANIFEST.md               ← Agent instantiation contracts
├── AGENT_INSTANTIATION.md          ← Instantiation procedures
├── GRADUATION_REPORT.md             ← Historical graduation record
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
│   └── SWEEP_*.md                  ← Per-session sweep logs
├── pptl/                           ← Phi-pentagon test layer
├── tests/                          ← pytest governance harness
└── scripts/                        ← Automation scripts
```

---

## 4. Authority and Evidence Order

**Instruction order** is separate from **epistemic evidence strength**.

### Operating instruction order

1. User instruction
2. Project-local host/space instructions
3. Current project operating constraints
4. Repository-local documentation
5. Default assistant behavior

### Evidence ladder

**DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED**

A project-local approval, Gold Star/S-Tier designation, persona sign-off, or rubric score does not automatically upgrade a claim on this ladder.

---

## 5. Non-Negotiables

- Refresh relevant context before synthesis.
- Update the pattern registry before implementation when a new pattern is actually introduced.
- Pair substantive outputs with a coherence and quality sweep.
- Do not represent S-Tier or Gold Star as external certification.
- Update logging and documentation when the change materially affects project state.
- Irreversible actions require the applicable HITL gate.
- Preserve failed experiments and superseded claims as historical evidence rather than silently converting them into current facts.
- Numeric thresholds must identify their provenance: computed, externally sourced, empirically fitted, arbitrary engineering parameter, or other appropriate category.
- Named mathematical constructs must correspond to the mathematics actually implemented; metaphorical labels must be marked as such.

---

## 6. Quick-Start for Agents

```python
# Minimal session bootstrap
from dgaf.bootstrap import load_session_anchor, load_co_orch_queue, load_pattern_registry

anchor = load_session_anchor()
queue  = load_co_orch_queue()
reg    = load_pattern_registry()

print(f"Active cycle: {queue['active_cycle']}")
print(f"Open OPPs: {[o for o in queue['opps'] if o['status'] == 'OPEN']}")
print(f"Active patterns: {len(reg['patterns'])}")
```

---

## 7. Escalation Contacts

| Trigger | Route To |
|---|---|
| Governance breach | Sentinel-Phi → Amethyst (project roles) |
| Coherence failure | COLLEEN → Amethyst (project roles) |
| Safety / ethics | DemiJoule (project role) |
| Architectural decision | Reson → Amethyst (project roles) |
| Human approval required | HITL queue → User |

*Historical project roles and terminology are retained for provenance. They should not be represented as independent authorities.*
