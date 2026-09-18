# .operations — DGAF Internal Ops Directory

> **Visibility:** Maintainer-only. Not published governance doctrine.  
> **Owner roles:** `role.continuity-archive-coordinator` + `role.security-containment-gate`  
> **Governance authority:** `role.governance-orchestrator`  
> **Identity provenance:** historical persona labels resolve through `governance/persona_role_lineage.v1.json`; persona names do not independently grant authority.  
> **Pattern:** P-14 (Trio Formation Sweep), P-02 (COLLEEN-Trigger-Chain)

This directory contains operational tooling that **runs** the DGAF-Framework repository — automation scripts, audit runners, CI helpers, and session scaffolding. It is distinct from `docs/` which contains published governance doctrine.

---

## Contents

| File | Owner | Purpose |
|------|-------|----------|
| `gate_compliance_check.py` | COLLEEN | Scans `docs/gates/` + `docs/protocols/` for P-24 (CPU) 6-field completeness; outputs compliance table; non-compliant files surface as BLG-class gaps |
| `sweep_session_init.md` | `role.continuity-archive-coordinator` → `role.governance-orchestrator` | Session open checklist: read SESSION_ANCHOR → build governed priority queue |
| `seal_checklist.md` | `role.governance-orchestrator` + scoped review/gate roles | Pre-seal checklist: atomic commit → scoped checks → synchronization evidence → state anchor |

---

## Usage

### Gate Compliance Check (run at session open)

```bash
python .operations/gate_compliance_check.py
```

Outputs a compliance table to stdout. Any FAIL rows are BLG-class gaps → surface immediately per P-03.

### Seal Checklist (run before every SWEEP_LOG seal)

Open `.operations/seal_checklist.md` and verify all items before executing the seal commit.

---

## Rules

- Nothing in `.operations/` is user-facing. No links to these files in public READMEs.
- Scripts here must be idempotent — safe to run multiple times per session.
- All scripts output to stdout only; writes to governed documentation require the authority defined by the applicable current contract.
- CI wiring or containment changes require the applicable `role.governance-orchestrator` and/or `role.security-containment-gate` authority; a persona label or historical repository does not grant it.

---

*Current authority: `role.continuity-archive-coordinator` + scoped `role.security-containment-gate`; governance orchestration: `role.governance-orchestrator`; explicit human authority remains with Ndr / [@ndrorchestration](https://github.com/ndrorchestration).*
