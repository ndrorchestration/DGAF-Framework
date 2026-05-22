# DGAF Ecosystem Cross-Reference

**Version:** 3.3  
**Maintained by:** COLLEEN + Amethyst-Conductor  
**Last updated:** 2026-05-22 (Session S038 — coherence sweep; all S033–S036 artifacts registered)  
**Canonical home:** `DGAF-Framework/CROSS_REF.md`

> Single-source map of all active repos, internal artifacts, and their governance relationships in the PHDGE ecosystem.

---

## Active Public Repositories

| Repo | Description | License | DGAF Attribution | Template Suite | FUNDING.yml |
|------|-------------|---------|------------------|----------------|-------------|
| [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) | Governance spine — MDAR loop, gate stack, NDR patterns, agent protocols | Apache-2.0 | ✅ | ✅ | ✅ |
| [sentinel-governance](https://github.com/ndrorchestration/sentinel-governance) | Agent Sentinel safety layer — veto authority, AXIS enforcement, doc-lint CI | Apache-2.0 | ✅ | ✅ | ✅ |
| [Amethyst-Governance-Eval-Stack](https://github.com/ndrorchestration/Amethyst-Governance-Eval-Stack) | Agent Amethyst evaluation stack — orchestration, coherence scoring | Apache-2.0 | ✅ | ✅ | ✅ |
| [junior-apogee-app](https://github.com/ndrorchestration/junior-apogee-app) | Agent Apogee training — evidence scoring, 11Q gate apprentice | Apache-2.0 | ✅ | ✅ | ✅ |
| [ai-prompt-systems-portfolio](https://github.com/ndrorchestration/ai-prompt-systems-portfolio) | Prompt engineering portfolio — LLM optimization, agentic prompt patterns | Apache-2.0 | ✅ | ✅ | ✅ |
| [Driftwatch](https://github.com/ndrorchestration/Driftwatch) | Drift detection — MDAR loop coherence monitoring | Apache-2.0 | ✅ | ✅ | ✅ |
| [Acoustic-mesh](https://github.com/ndrorchestration/Acoustic-mesh) | Acoustic Gate Chain implementation (P-13) | Apache-2.0 | ✅ | ✅ | ✅ |
| [phi-calculus-app](https://github.com/ndrorchestration/phi-calculus-app) | Phi-Harmonic calculus — platinum mean, phi-gate interval math | Apache-2.0 | ✅ | ✅ | ✅ |
| [3d-visualization-hub](https://github.com/ndrorchestration/3d-visualization-hub) | 3D governance visualization — lattice rendering, hendecagonal geometry | Apache-2.0 | ✅ | ✅ | ✅ |
| [resumeapex-eval](https://github.com/ndrorchestration/resumeapex-eval) | Resume evaluation pipeline — Apogee scoring integration | Apache-2.0 | ✅ | ✅ | ✅ |

---

## Internal Artifacts (DGAF-Framework)

### Governance Spine

| Artifact | Path | Purpose | Last Updated |
|----------|------|---------|-------------|
| Main README | `README.md` | Public-facing entry point; badge row; ecosystem link table | S037 |
| Governance README | `README.governance.md` | NIST/EU AI Act compliance reference; auditor entry point | S038 |
| Technical README | `README.technical.md` | Agent/engineer dense spec; gate stack; current components | S038 |
| CHANGELOG | `CHANGELOG.md` | Semantic versioned artifact history | S037 (v1.0.14) |
| SWEEP_LOG | `SWEEP_LOG.md` | Sealed session audit trail | S038 (open) |
| SESSION_ANCHOR | `SESSION_ANCHOR.md` | P-21 session handoff (overwrite pattern) | S038 (open) |
| CROSS_REF | `CROSS_REF.md` | This file — ecosystem artifact map | S038 (v3.3) |
| NOTICE | `NOTICE` | Apache-2.0 attribution + PHDGE/DGAF spine link | S014 |
| SECURITY | `SECURITY.md` | Responsible disclosure policy | S022c |
| ENSEMBLE_ROSTER | `ENSEMBLE_ROSTER.md` | Canonical agent registry (11 active agents) | S024 |
| ECOSYSTEM_STATE | `ECOSYSTEM-STATE.md` | Point-in-time ecosystem audit snapshot | S013 |
| Master Portfolio Inventory | `docs/ops/MASTER_PORTFOLIO_INVENTORY_VERIFICATION_SYSTEM.md` | Drive master inventory v2.0 | S031-BLG-D01 |

### Runtime Components (`components/`)

| Artifact | Path | Purpose | Session |
|----------|------|---------|--------|
| KAPPA Dynamic Confidence Router | `components/KAPPA/dynamic_weight_router.py` | Confidence-gated routing and category detection | S033 |
| KAPPA Calibration | `components/KAPPA/calibration_v3_6.json` | v3.6 calibration; `governance_clear` 100% | S034 |
| KAPPA Component Card | `components/KAPPA/DGAF_GATE_KAPPA_v3_5_component_card.json` | CPU-compliant component registry card | S034 |
| Evaluate Router | `components/evaluate_router.py` | Batch pipeline composition: detect → apply_weights → rank | S033 |
| Evaluate Router v1.1 | `components/evaluate_router_v1_1.py` | Sentinel hooks + P-10 deontic gate + audit log | S034 |
| Normative Constraint | `components/normative_constraint.py` | Deontic / optimization / epistemic integrity class | S035 |
| Component Index | `components/README.md` | Runtime component navigation | S038 |

### Gate Specs (`docs/gates/`)

| Artifact | Path | Pattern | Status | Certified |
|----------|------|---------|--------|-----------|
| Gate Unit Template | `docs/gates/GATE_UNIT_TEMPLATE.md` | P-24 | Template (blank) | S026 |
| Gate Specs Index | `docs/gates/GATE_SPECS.md` | — | Index | S004 |
| Acoustic Gates | `docs/gates/ACOUSTIC_GATES.md` | P-13 | ✅ CERTIFIED v2.0 | S027 |
| 1-1-1-1 Gate | `docs/gates/GATE_1111.md` | P-10 | ✅ CERTIFIED v2.0 | S028 |
| 11Q Framework | `docs/gates/GATE_11Q.md` | P-11 | ✅ CERTIFIED v2.0 | S028 |
| Telescopic Lens | `docs/gates/TELESCOPIC_LENS.md` | P-12 | ✅ CERTIFIED v2.0 | S028 |

### Patterns & Protocols

| Artifact | Path | Version | Last Updated |
|----------|------|---------|-------------|
| NDR Pattern Registry | `docs/patterns/NDR_PATTERN_REGISTRY.md` | **v2.1** | S035 |
| MDAR Protocol | `docs/protocols/MDAR_PROTOCOL_v1.md` | v1.0 | S004 |

### QA & Attestation (`docs/qa/`)

| Artifact | Path | Purpose | Session |
|----------|------|---------|--------|
| Apogee 11Q S034 | `docs/qa/APOGEE_11Q_S034.json` | A-TIER attestation pre-NormativeConstraint | S034 |
| Apogee 11Q S035 | `docs/qa/APOGEE_11Q_S035.json` | S-TIER attestation post-NormativeConstraint | S035 |
| QA Index | `docs/qa/README.md` | Attestation artifact navigation | S038 |

### Operations (`.operations/`) — Maintainer-Only

| Artifact | Path | Purpose |
|----------|------|---------|
| Ops README | `.operations/README.md` | Directory purpose, contents, usage rules |
| Gate Compliance Check | `.operations/gate_compliance_check.py` | P-24 compliance scanner; exit code 1 on BLG-class gap |
| Sweep Session Init | `.operations/sweep_session_init.md` | P-02/P-21 session open checklist |
| Seal Checklist | `.operations/seal_checklist.md` | P-06/P-15/P-20/P-21 pre-seal gate stack checklist |

### Ops Docs (`docs/ops/`)

| Artifact | Path | Purpose | Status |
|----------|------|---------|-------|
| BLG-D01 Correction Work Order | `docs/ops/BLG_D01_DRIVE_CORRECTION.md` | P-24-compliant Drive inventory delta + recovery | ✅ CLOSED S031-BLG-D01 |
| Master Portfolio Inventory | `docs/ops/MASTER_PORTFOLIO_INVENTORY_VERIFICATION_SYSTEM.md` | Drive master inventory v2.0 | ✅ v2.0 S031-BLG-D01 |
| S032 Drive Closure | `docs/ops/BLG_S032_DRIVE_CLOSURE.md` | All 4 Drive templates executed by Njineer | ✅ CLOSED S036 |
| Drive Update Templates | `docs/ops/DRIVE_UPDATE_TEMPLATE_*.md` | P-01/P-20 Drive sync templates (4 files) | ✅ EXECUTED S036 |

### Drafts Staging (`docs/drafts/`)

| Artifact | Path | Purpose |
|----------|------|---------|
| Drafts README | `docs/drafts/README.md` | Staging layer governance; P-03/P-11/P-18 rules |

### Sync Docs (`docs/sync/`)

| Artifact | Path | Purpose |
|----------|------|---------|
| Drive Sync Policy | `docs/sync/DRIVE_SYNC_POLICY.md` | P-22 Hub-and-Spoke storage topology |
| Drive-GitHub Sync | `docs/sync/DRIVE_GITHUB_SYNC.md` | P-20 seal-time sync verification protocol |
| Hub-Spoke Sync | `docs/sync/HUB_SPOKE_SYNC.md` | P-22 full spec |

---

## CI / Automation

| Repo | Workflow | Purpose | Status |
|------|----------|---------|-------|
| `sentinel-governance` | `.github/workflows/doc-lint.yml` | markdownlint on PR + push; P-24 consistency gate | ✅ LIVE — S029 |
| `DGAF-Framework` | `.github/workflows/doc-lint.yml` | markdownlint on PR + push; spine quality gate | ✅ LIVE — S031 |
| `DGAF-Framework` | `.github/workflows/governance-ci.yml` | Governance integrity checks | ✅ LIVE |
| `DGAF-Framework` | `.github/workflows/governance-sweep.yml` | Scheduled coherence sweep automation | ✅ LIVE |
| `DGAF-Framework` | `.operations/gate_compliance_check.py` | P-24 compliance scan; run at session open | ✅ LIVE — S026 |

---

## Governance Relationships

```
DGAF-Framework (spine)
├── governs → all 10 repos in ecosystem
├── pattern authority → NDR_PATTERN_REGISTRY.md (P-01 through P-30)
├── gate authority → docs/gates/ (GATE-ACO, GATE-1111, GATE-11Q, GATE-TEL)
├── agent registry → ENSEMBLE_ROSTER.md
├── audit trail → SWEEP_LOG.md + CHANGELOG.md + git history
└── session continuity → SESSION_ANCHOR.md (P-21)

sentinel-governance
├── CI enforcement → .github/workflows/doc-lint.yml
└── veto authority → Agent Sentinel (GATE-11Q gates 9–11)
```

---

## Changelog

| Version | Session | Change |
|---------|---------|-------|
| 1.0–2.8 | S001–S022b | Initial map through surface sweep completion |
| 2.9 | S024 | 9-repo active table; last sweep timestamp |
| 3.0 | S025 | Template suite + FUNDING.yml completion confirmed |
| 3.1 | S029 | Internal artifact registry: gate specs, ops dir, drafts, sync docs, dual READMEs, CI/automation table |
| 3.2 | S031-BLG-D01 | NDR Registry v1.8; CI table updated; master portfolio v2.0; BLG-D01 closed |
| **3.3** | **S038** | **Runtime components section added; QA/attestation section added; NDR v2.1; P-01–P-30 authority; ops docs updated for S032 closure; README.technical.md + README.governance.md entries current** |
