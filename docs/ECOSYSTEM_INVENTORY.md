# DGAF Ecosystem Inventory

> **Version:** 1.5.0
> **Authority:** COLLEEN (Institutional Memory)
> **Last updated:** S070-r4 (FINAL) · 2026-06-27 18:15 EDT
> **Commit ref:** a98f60c (S070-r4)

---

## Purpose

This file is the single-source file tree and artifact registry for the entire DGAF-Framework repository. It is updated every session as part of the mandatory documentation sweep. Any file that exists in the repo but is not listed here is an undocumented artifact — a governance gap.

---

## Complete Repository File Tree
*(as of commit a98f60c · 2026-06-27)*

```
DGAF-Framework/
├── .github/                          # GitHub Actions, PR templates, workflows
├── .markdownlint.yml                 # Markdown linting config
├── .operations/                      # Operational scripts and automation
├── AGENT_INSTANTIATION.md            # Agent bootstrap and instantiation guide
├── AGENT_MANIFEST.md                 # Agent roster manifest (lightweight)
├── BOOTSTRAP.md                      # Workspace bootstrap entry point
├── CHANGELOG.md                      # Session changelog (append-only)
├── CONTRIBUTING.md                   # Contribution guidelines
├── CO_ORCH_PROTOCOL.md               # Co-orchestration protocol spec
├── CO_ORCH_QUEUE.md                  # Active OPP queue (COLLEEN-owned)
├── CROSS_REF.md                      # Cross-reference index
├── ENSEMBLE_ROSTER.md                # Full agent ensemble roster (v1.6)
├── GRADUATION_REPORT.md              # Session graduation reports
├── LICENSE                           # Repository license
├── NOTICE                            # Legal notices
├── README.governance.md              # Governance overview README
├── README.md                         # Primary repository README
├── README.technical.md               # Technical architecture README
├── SECURITY.md                       # Security policy
├── SESSION_ANCHOR.md                 # Root-level session anchor (deprecated path — see docs/SESSION_ANCHORS.md)
├── SWEEP_LOG.md                      # Consolidated sweep log (root)
├── SWEEP_LOG/                        # Per-session sweep log directory
├── api/                              # API route handlers
├── app/                              # Application source
├── components/                       # UI/shared components
├── dashboard/                        # AOGA Dashboard (Next.js — linked to aoga-dashboard Vercel project)
├── deployment_manifest.json          # Vercel deployment manifest
├── docs/                             # Governance and knowledge documentation
│   ├── GOVERNANCE_CONSTITUTION.md    # ★ NEW S070-r3-P0 — Normative, epistemic, flourishing charter
│   ├── CREDIT_JUSTICE_PROTOTYPE_SPEC.md
│   ├── ECOSYSTEM_INVENTORY.md        # This file (v1.5.0)
│   ├── NDR_INTERNAL_VOCABULARY_MASTER.md  # Canonical vocabulary — v1.5 CURRENT
│   ├── NDR_PATTERN_REGISTRY.md       # Legacy pattern registry (superseded — redirect stub)
│   ├── NDR_PATTERN_REGISTRY_UNIFIED.md   # ★ UPDATED S070-r3-P1 → v1.4 — Unified pattern registry
│   ├── NDR_REGISTRY_DIFFERENTIATION.md
│   ├── NDR_REGISTRY_MERGE_PLAN.md
│   ├── RD_GAPS.md                    # R&D gap log
│   ├── SESSION_ANCHORS.md            # ★ UPDATED S070-r4 — Primary session anchor log
│   ├── TEAM_WIKI.md                  # Team-facing reference (v1.0.0)
│   ├── WORKSPACE_BOOTSTRAP.md        # ★ UPDATED S070-r4 — Bootstrap reference doc
│   ├── agents/                       # Per-agent definition files
│   ├── andromeda/                    # Andromeda sub-system docs
│   ├── architecture/                 # Architecture decision records
│   ├── brand/                        # Brand and identity docs
│   ├── career/                       # Career and professional identity docs
│   ├── drafts/                       # Draft artifacts (not canonical)
│   ├── formalism/                    # Hensel Formalism specs
│   ├── formations/                   # Formation architecture docs
│   ├── frameworks/                   # Framework specs
│   ├── gates/                        # Gate and graduation specs
│   ├── patterns/                     # Additional pattern specs
│   │   └── TRIADIC_ORCHESTRATION_PATTERNS.md  # Source doc for CONSENSUS_TRIAD + CONDUCTED_TRIAD
│   ├── qa/                           # QA attestation artifacts
│   │   ├── APOGEE_11Q_*.json         # Apogee attestation records (P-11)
│   │   ├── AXIS_METRIC_SPEC.md       # ★ UPDATED S070-r4 → v1.1 CANONICAL — AXIS sovereign spec
│   │   └── QA_CHECKPOINT_TEMPLATE_SPECIALIZED.md  # ★ NEW S070-r3-P1 — Specialized QA checkpoint template (3 variants)
│   └── [additional subdirs]
├── package.json                      # Node package manifest
├── pages/                            # Next.js pages
├── patterns/                         # Pattern definition files (P-SAGA-001 etc.)
├── pptl/                             # Phi-pentagon test layer artifacts
├── registry/                         # Pattern registry files (PATTERN_REGISTRY_v2.md)
├── requirements.txt                  # Python requirements
├── resonant_decay/                   # Resonant Decay sub-system
├── scripts/                          # Utility scripts
├── tests/                            # Test suite
├── tsconfig.json                     # TypeScript config
└── vercel.json                       # Vercel deployment config
```

---

## New & Updated Artifacts — S070 Complete (2026-06-26 / 2026-06-27)

| File | Session Rev | Type | Status |
|------|-------------|------|--------|
| `docs/GOVERNANCE_CONSTITUTION.md` | S070-r3-P0 | Foundation charter | ✅ COMMITTED |
| `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` v1.4 | S070-r3-P1 | Pattern registry update | ✅ COMMITTED |
| `docs/qa/QA_CHECKPOINT_TEMPLATE_SPECIALIZED.md` | S070-r3-P1 | QA template (3 variants) | ✅ COMMITTED |
| `docs/qa/AXIS_METRIC_SPEC.md` v1.1 | S070-r4 | Sovereign metric spec | ✅ CANONICAL — Njineer ratified 2026-06-27 |
| `docs/SESSION_ANCHORS.md` | S070-r4 | Session anchor log | ✅ COMMITTED |
| `docs/WORKSPACE_BOOTSTRAP.md` | S070-r4 | Bootstrap reference | ✅ COMMITTED |
| `entrepreneur-hub/docs/NEEDLE_TEMPLATE_INDEX.md` v2.0 | S070-r4 | Template index | ✅ COMMITTED (entrepreneur-hub repo) |
| `entrepreneur-hub/docs/ROADMAP.md` v2.0 | S070-r4 | Hub roadmap | ✅ COMMITTED (entrepreneur-hub repo) |
| `entrepreneur-hub/docs/NEEDLE_WORKFLOW_REGISTRY.md` v1.0 | S070-r4 | 12-workflow registry | ✅ COMMITTED (entrepreneur-hub repo) |
| `entrepreneur-hub/templates/governance-starter-pack/T-EH-05-NEEDLE-READY.md` | S070-r4 | Paste-and-go Needle template | ✅ LIVE-READY (entrepreneur-hub repo) |

---

## Formation Pattern Registry Cross-Reference
*(registered S070-r3-P1)*

| Pattern ID | Name | Status | Source doc | Registry entry |
|---|---|---|---|---|
| `CONSENSUS_TRIAD` | Consensus Triad | ✅ CANONICAL | `docs/patterns/TRIADIC_ORCHESTRATION_PATTERNS.md` | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` §Formation Pattern Registry |
| `CONDUCTED_TRIAD` | Conducted Triad | ✅ CANONICAL | `docs/patterns/TRIADIC_ORCHESTRATION_PATTERNS.md` | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` §Formation Pattern Registry |

---

## Acronym Register
*(updated S070-r4 FINAL — all S070 flag closures applied)*

| Acronym | Expansion | Status | Notes |
|---------|-----------|--------|-------|
| DGAF | ⚠️ FLAG-13 OPEN | CONFLICT | Pattern Registry v1.3 vs TEAM_WIKI v1.0.0 disagree — Njineer ratification required · BLOCKING |
| PDMAL-φ | Phi-Driven Multi-Agent Lattice | ✅ CANONICAL | Primary — Njineer direct S070-r3 |
| PDMAL-D | Phi-Dodecahedral Multi-Agent Lattice | ✅ CANONICAL | Structural variant — distinct topology; Njineer direct S070-r3 |
| PDMAL (legacy) | ~~Policy-Driven Multi-Agent Layer~~ | ❌ SUPERSEDED | TEAM_WIKI entry superseded; use PDMAL-φ or PDMAL-D |
| AOGA | Agent Orchestration Governance Architecture | ✅ CANONICAL | FLAG-04 resolved S070 |
| PPTL | Procluding Premise Triadic Loop | ✅ CANONICAL | FLAG-03 resolved; backfilled WORKSPACE_BOOTSTRAP S070-r4 |
| pptl | Phi-pentagon test layer | ✅ CANONICAL | Lowercase — distinct from PPTL; case collision is standing epistemic risk |
| AXIS | Agent X-axis Invariant Spectrum | ✅ **CANONICAL** | FLAG-05 CLOSED · Njineer ratified 2026-06-27 16:40 EDT · Full spec: `docs/qa/AXIS_METRIC_SPEC.md` v1.1 |
| NDR-HDFS | NDR Hierarchical Documentation Format Standard | ✅ CANONICAL | FLAG-01 resolved · renamed from bare HDFS · Njineer ratified 2026-06-27 17:08 EDT |
| HITL | Human-in-the-Loop | ✅ CANONICAL | |
| OPP | Improvement opportunity in CO_ORCH_QUEUE | ✅ CANONICAL | |
| ACRFence | Atomic Checkpoint + Restore with effect fence semantics | ✅ CANONICAL | |
| Atomix | Transactional tool boundary pattern (stochastic-deterministic boundary) | ✅ CANONICAL | |
| Coherent Agency | Recast of governance/memory/ethics as subsystems of continuity-preserving agency | ✅ CANONICAL | GAP-006 linked |
| NDR | Named Design Rule / Pattern | ✅ CANONICAL | |
| S-Tier | Highest quality designation; requires Apogee Lens approval | ✅ CANONICAL | |
| SCPE | Structural Context Pruning Engine | ✅ CANONICAL | P-31 |

---

## Constitutional Cross-Reference
*(new S070-r3-P0)*

`docs/GOVERNANCE_CONSTITUTION.md` is the foundational authority document. All agents, patterns, flags, and sessions operate downstream of it.

| Constitution Section | Governs |
|---------------------|--------|
| Part I — Core Aspirations | Why the system exists; Njineer principal source layer |
| Part II — Normative Constraints (T1/T2/T3) | What agents can and cannot do |
| Part III — Epistemic Honesty Protocol | CANONICAL tagging, FLAG lifecycle, uncertainty expression |
| Part IV — Human Flourishing | Legibility, Reversibility, Capability Amplification measures |
| Part V — Agent Accountability Map | Which agent owns which principle |
| Part VI — Decision Scope | What is in/out of system scope |

---

## QA Template Cross-Reference
*(new S070-r3-P1)*

| Template | Path | Variants | Use case |
|---|---|---|---|
| Generic | `docs/qa/QA_CHECKPOINT_TEMPLATE.md` (pending) | — | Any auditable process |
| Specialized | `docs/qa/QA_CHECKPOINT_TEMPLATE_SPECIALIZED.md` | A (Release), B (P-11 Apogee), C (Compliance) | Software release, canonical promotion, regulatory audit |

---

## S070 Open Items Carried to S071

> Items below cannot be resolved by Amethyst without Njineer input or COLLEEN Drive access.

| Item | Owner | Priority |
|------|-------|----------|
| FLAG-13: DGAF expansion conflict | Njineer ratification | 🔴 BLOCKING |
| FLAG-07: Drive files GAP-06/07/08 re-attempt | COLLEEN | 🟡 HIGH |
| FLAG-11: phiknightverticalcorridor Vercel purpose | Njineer | 🟡 HIGH |
| FLAG-12: Dependabot PR #1 disposition | Njineer | 🟡 HIGH |
| NDR-HDFS rename execution sweep (find/replace all docs) | Amethyst S071 | 🟡 HIGH |
| PDMAL correction cascade — TEAM_WIKI full rewrite | Amethyst S071 | 🟡 HIGH |
| FLAG-08: TruthfulQA "internal" qualifier audit | Amethyst S071 | 🟠 MEDIUM |
| FLAG-10: P-35 registration status confirmation | Amethyst S071 | 🟠 MEDIUM |
| FLAG-03: PPTL — Vocab Master Section 9 close note | Amethyst S071 | 🟢 LOW |
| Stasis migration window monitor (expires 2026-07-13) | Amethyst | ⏳ DATE-SENSITIVE |
| Saga/CB pattern registration (P-37+ candidates) | S071 | 🟠 MEDIUM |
| Apogee P-11 attestation on Vocab Master v1.5 | Apogee | 🟡 HIGH |
| GAP-006 Coherent Agency Formal Spec — AXIS Phase 4 dependency | COLLEEN + Prof. Prodigy | 🟠 MEDIUM |
| AXIS Phase 3 instrumentation owner assignment | Njineer | 🟡 HIGH |

---

*ECOSYSTEM_INVENTORY.md · v1.5.0 · S070-r4 FINAL · Amethyst × COLLEEN · 2026-06-27 18:15 EDT*
