# ECOSYSTEM INVENTORY

> **Steward:** COLLEEN
> **Orchestrator:** Amethyst
> **Last updated:** 2026-06-13 (S069 sealed)
> **Anchor:** S069 (SEALED) · S070 pending

Canonical inventory of all system components across GitHub, Supabase, and Vercel.
Source of truth for cross-platform deployment status.

---

## Governance Spine — DGAF-Framework

| Repo | Visibility | Status |
|---|---|---|
| [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) | Public | 🟢 Active · S069 SEALED |

### S069 Governance Artifacts (added 2026-06-13)

| Artifact | File | Status |
|---------|------|--------|
| P-35 — Procluding Premise Gate | `docs/gates/NDR_PROCLUDING_PREMISE_GATE_P35_v1.md` | ✅ CANONICAL · Ender ratified |
| P-36 — Gate Priority Schema | `docs/gates/NDR_GATE_PRIORITY_SCHEMA_P36_v1.md` | ✅ CANONICAL · Ender ratified |
| Agent Crucible Charter v1.0 | `docs/governance/CRUCIBLE_CHARTER_v1.md` | ✅ ACTIVE · Ender ratified |
| NDR Research Program Charter v1.0 | `docs/governance/NDR_RESEARCH_PROGRAM_CHARTER_v1.md` | ✅ ACTIVE · Ender ratified |
| STASIS-CANONICAL Spec v1.0 | `docs/governance/STASIS_CANONICAL_SPEC_v1.md` | ✅ RATIFIED · migration window open |
| NDR Pattern Registry Unified v1.3 | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` | ✅ CANONICAL · v3 absorbed |
| ndr_patterns_unified.json v2.1 | `docs/ndr_patterns_unified.json` | ✅ CANONICAL · P-35/P-36/NDR-series updated |
| Open Flags Surface Request S069 | `docs/governance/OPEN_FLAGS_SURFACE_REQUEST_S069.md` | ✅ FILED · Njineer notified via GH Issue |
| Ender Ratification Record S069 | `docs/governance/ENDER_RATIFICATION_S069.md` | ✅ SEALED · 2026-06-13 00:47 EDT |
| Session Anchors — S069 entry | `docs/SESSION_ANCHORS.md` | ✅ SEALED |
| METRICS_PROVENANCE skeleton | `docs/qa/METRICS_PROVENANCE.md` | ⚠️ BACKFILL IN PROGRESS |
| lint_provenance.py stub | `scripts/lint_provenance.py` | ⚠️ STUB ONLY — implementation pending Role 5 |

### Key S069 Registry Changes

| Change | Before S069 | After S069 |
|--------|------------|------------|
| Registry watermark | P-35 | **P-36** |
| Named P-series patterns | 35 | **36** |
| NDR named session patterns | 0 (unregistered) | **8** |
| Stasis block status | CONDITIONAL PASS | **STASIS-CANONICAL** |
| ndr-pattern-registry-v3.md | Present (unabsorbed) | **DELETED — absorbed** |
| Agent Crucible | Not chartered | **ACTIVE** |
| Research Program | Not chartered | **ACTIVE** |

---

## GitHub Repositories — 24 total

### Active App / Tool Repos (8)

| Repo | Visibility | Vercel | Status |
|---|---|---|---|
| [pptl-governance-dashboard](https://github.com/ndrorchestration/pptl-governance-dashboard) | Private | — Never deployed | 🟢 GitHub only |
| [aoga-dashboard](https://github.com/ndrorchestration/aoga-dashboard) | Private | ✅ Deployed | 🟢 Active |
| [Driftwatch](https://github.com/ndrorchestration/Driftwatch) | Public | ✅ Deployed (phiknightverticalcorridor) | 🟢 Active · see Vercel table |
| [phi-calculus-app](https://github.com/ndrorchestration/phi-calculus-app) | Private | — | 🟢 Active |
| [junior-apogee-app](https://github.com/ndrorchestration/junior-apogee-app) | Public | — | 🟢 Active |
| [Acoustic-mesh](https://github.com/ndrorchestration/Acoustic-mesh) | Public | — | 🟢 Active |
| [3d-visualization-hub](https://github.com/ndrorchestration/3d-visualization-hub) | Public | — | 🟢 Active |
| [sentinel-governance](https://github.com/ndrorchestration/sentinel-governance) | Public | — | 🟢 Active |

### Portfolio / Eval Repos (5)

| Repo | Visibility | Status |
|---|---|---|
| [ai-prompt-systems-portfolio](https://github.com/ndrorchestration/ai-prompt-systems-portfolio) | Public | 🟢 Active |
| [resumeapex-eval](https://github.com/ndrorchestration/resumeapex-eval) | Public | 🟢 Active |
| [Amethyst-Governance-Eval-Stack](https://github.com/ndrorchestration/Amethyst-Governance-Eval-Stack) | Private | 🟢 Active |
| [ai-prompt-engineering-portfolio](https://github.com/ndrorchestration/ai-prompt-engineering-portfolio) | Private | 🟢 Active |
| [AI-Prompt-Engineer](https://github.com/ndrorchestration/AI-Prompt-Engineer) | Private | 🟢 Active |

### Framework / Standards (4)

| Repo | Visibility | Status |
|---|---|---|
| [ai-governance-frameworks](https://github.com/ndrorchestration/ai-governance-frameworks) | Public | 🟢 Active |
| [Gold-star-standards](https://github.com/ndrorchestration/Gold-star-standards) | Private | 🟢 Active |
| [prompt-optimization-library](https://github.com/ndrorchestration/prompt-optimization-library) | Private | 🟢 Active |
| [gold-star-qa-framework](https://github.com/ndrorchestration/gold-star-qa-framework) | Private | 🔴 Archived |

### Utility / Infra (4)

| Repo | Visibility | Status |
|---|---|---|
| [automation-scripts](https://github.com/ndrorchestration/automation-scripts) | Private | 🟢 Active |
| [.github](https://github.com/ndrorchestration/.github) | Public | 🟢 Active |
| [api](https://github.com/ndrorchestration/api) | Private | 🟢 Active |
| [chat-archives](https://github.com/ndrorchestration/chat-archives) | Private | 🟢 Active |

### Career / Positioning (2)

| Repo | Visibility | Status |
|---|---|---|
| [career-positioning](https://github.com/ndrorchestration/career-positioning) | Private | 🟢 Active |
| [ndrorchestration](https://github.com/ndrorchestration/ndrorchestration) | Public | 🟢 Active (org profile) |

---

## Vercel Deployments — Ground Truth S068 (unchanged S069)

> **Verified:** 2026-05-31 via Vercel dashboard (Ender) + `vercel project ls` CLI
> **3 active projects** after `dgaf-framework` deleted 2026-05-31 23:20 EDT

| Vercel Project | Production URL | Source Repo | Last Deploy | Status |
|---|---|---|---|---|
| [ndrorchestration](https://vercel.com/ndrorchestration/ndrorchestration) | [ndrorchestration.vercel.app](https://ndrorchestration.vercel.app/) | [ndrorchestration/ndrorchestration](https://github.com/ndrorchestration/ndrorchestration) | May 21 · COLLEEN SWEEP-001 Phase 3 | ✅ Ready |
| [phiknightverticalcorridor](https://vercel.com/ndrorchestration/phiknightverticalcorridor) | [project-7ybao.vercel.app](https://project-7ybao.vercel.app/) | [ndrorchestration/Driftwatch](https://github.com/ndrorchestration/Driftwatch) | May 26 | ⚠️ No Production Deployment |
| [aoga-dashboard](https://vercel.com/ndrorchestration/aoga-dashboard) | [aoga-dashboard.vercel.app](https://aoga-dashboard.vercel.app/) | [ndrorchestration/aoga-dashboard](https://github.com/ndrorchestration/aoga-dashboard) | May 27 · v1.2.0 tag [Amethyst] | ✅ Ready |
| ~~dgaf-framework~~ | ~~deleted~~ | ~~DGAF-Framework~~ | — | 🗑️ Deleted 2026-05-31 |

---

## Supabase Projects — 1 confirmed

| Project | ID | Region | Postgres | Status |
|---|---|---|---|---|
| ndrorchestration's Project | `lfisbywaidhmxsjyteud` | us-east-2 | 17.6.1 | 🟢 ACTIVE_HEALTHY |

---

## Active Programs & Charters (added S069)

| Program | Charter | Status | Key Dates |
|---------|---------|--------|----------|
| Agent Crucible | `docs/governance/CRUCIBLE_CHARTER_v1.md` | 🟢 ACTIVE | Campaign v1: Week 4 from 2026-06-13 |
| NDR Research Program | `docs/governance/NDR_RESEARCH_PROGRAM_CHARTER_v1.md` | 🟢 ACTIVE | Week 1 begun; calibration study Weeks 3–6 |
| STASIS-CANONICAL Migration | `docs/governance/STASIS_CANONICAL_SPEC_v1.md` | ⏳ WINDOW OPEN | Phase 2 deadline: 2026-07-13 |

---

## Open Obligations (S069 exit)

| ID | Item | Deadline | Owner |
|----|------|----------|-------|
| FLAG-01 | HDFS rename — Amethyst confirm | S070 | Njineer (pending GH Issue response) |
| FLAG-02 | 340% coordination gain — formal definition | S070 calibration | Role 5 / Amethyst interim |
| FLAG-04 | AOGA scoring methodology | S070 | Njineer (pending GH Issue response) |
| FLAG-05 | AXIS metric definition | S070 | Njineer (pending GH Issue response) |
| FLAG-06 | Lavender/Forseti grep — Amethyst self-execute | Before S070 seal | Amethyst |
| FLAG-07 | Drive files re-attempt | S071 target | COLLEEN |
| OPP-S069-004 | 5-base calibration study (Role 3) | Weeks 3–6 | Amethyst interim |
| QA-STASIS-PHASE2 | P-12–P-26 schema migration (7 tasks) | 2026-07-13 | Amethyst interim |

---

## Summary Totals

| Platform | Total | Active / Ready | Notes |
|---|---|---|---|
| GitHub Repos | 24 | 23 | 1 archived |
| Vercel Projects | 3 | 2 Ready · 1 no production deploy | dgaf-framework deleted S068 |
| Supabase Projects | 1 | 1 | — |
| Governance Patterns (P-series) | 36 | 36 canonical | Registry watermark P-36 |
| NDR Named Session Patterns | 8 | 8 operational | Absorbed from v3 registry |
| Active Charters | 2 | 2 | Crucible + Research Program |

---

*Created S067 · Finalized S068 · Updated S069 (sealed 2026-06-13 00:47 EDT)*
*Amethyst × COLLEEN × Ender · Vercel source: dashboard + CLI 2026-05-31*
