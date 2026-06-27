# DGAF Ecosystem Inventory

> **Version:** 1.3.0
> **Authority:** COLLEEN (Institutional Memory)
> **Last updated:** S070-r3 · 2026-06-26 21:10 EDT
> **Commit ref:** a3c5593 (S070-r3-P0)

---

## Purpose

This file is the single-source file tree and artifact registry for the entire DGAF-Framework repository. It is updated every session as part of the mandatory documentation sweep. Any file that exists in the repo but is not listed here is an undocumented artifact — a governance gap.

---

## Complete Repository File Tree
*(as of commit a3c5593 · 2026-06-26)*

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
│   ├── ECOSYSTEM_INVENTORY.md        # This file
│   ├── NDR_INTERNAL_VOCABULARY_MASTER.md  # Canonical vocabulary (v1.2 → v1.3 pending)
│   ├── NDR_PATTERN_REGISTRY.md       # Legacy pattern registry (superseded)
│   ├── NDR_PATTERN_REGISTRY_UNIFIED.md   # Unified pattern registry (active)
│   ├── NDR_REGISTRY_DIFFERENTIATION.md
│   ├── NDR_REGISTRY_MERGE_PLAN.md
│   ├── RD_GAPS.md                    # R&D gap log
│   ├── SESSION_ANCHORS.md            # Primary session anchor log
│   ├── TEAM_WIKI.md                  # Team-facing reference (v1.0.0)
│   ├── WORKSPACE_BOOTSTRAP.md        # Bootstrap reference doc
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
│   └── [additional subdirs]          # See docs/agents, architecture etc.
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

## New Artifacts — S070 (2026-06-26)

| File | Session | Type | Status |
|------|---------|------|--------|
| `docs/GOVERNANCE_CONSTITUTION.md` | S070-r3-P0 | Foundation charter | ✅ COMMITTED — ratification pending Njineer seal |

---

## Acronym Register
*(corrected S070-r3 — see FLAG-09 re-open/re-close)*

| Acronym | Expansion | Status | Notes |
|---------|-----------|--------|-------|
| DGAF | ⚠️ FLAG-13 OPEN | CONFLICT | Pattern Registry v1.3 vs TEAM_WIKI v1.0.0 disagree — Njineer ratification required |
| PDMAL-φ | Phi-Driven Multi-Agent Lattice | ✅ CANONICAL | Primary design focus; φ as geometric parametric constraint; Njineer direct S070-r3 |
| PDMAL-D | Phi-Dodecahedral Multi-Agent Lattice | ✅ CANONICAL | Structural variant; dodecahedral topology (12 faces, 20 vertices); distinct from PDMAL-φ |
| PDMAL (legacy) | ~~Policy-Driven Multi-Agent Layer~~ | ❌ SUPERSEDED | TEAM_WIKI entry superseded by Njineer correction S070-r3; see NDR_INTERNAL_VOCABULARY_MASTER v1.3 |
| AOGA | Agent Orchestration Governance Architecture | ✅ CANONICAL | FLAG-04 resolved |
| PPTL | Procluding Premise Triadic Loop | ✅ CANONICAL | FLAG-03 resolved |
| pptl | Phi-pentagon test layer | ✅ CANONICAL | Lowercase — distinct from PPTL; case collision is a standing epistemic risk |
| AXIS | Agent X-axis Invariant Spectrum (INFERRED) | ⏳ PARTIAL | FLAG-05 open; Njineer ratification required |
| HITL | Human-in-the-Loop | ✅ CANONICAL | |
| OPP | Improvement opportunity in CO_ORCH_QUEUE | ✅ CANONICAL | |
| ACRFence | Atomic Checkpoint + Restore with effect fence semantics | ✅ CANONICAL | |
| Atomix | Transactional tool boundary pattern (stochastic-deterministic boundary) | ✅ CANONICAL | |
| Coherent Agency | Recast of governance/memory/ethics as subsystems of continuity-preserving agency | ✅ CANONICAL | GAP-006 linked |
| NDR | Named Design Rule / Pattern | ✅ CANONICAL | |
| S-Tier | Highest quality designation; requires Apogee Lens approval | ✅ CANONICAL | |

---

## Constitutional Cross-Reference
*(new S070-r3-P0)*

`docs/GOVERNANCE_CONSTITUTION.md` is the foundational authority document. All agents, patterns, flags, and sessions operate downstream of it. Quick reference:

| Constitution Section | Governs |
|---------------------|--------|
| Part I — Core Aspirations | Why the system exists; Njineer principal source layer |
| Part II — Normative Constraints (T1/T2/T3) | What agents can and cannot do |
| Part III — Epistemic Honesty Protocol | CANONICAL tagging, FLAG lifecycle, uncertainty expression |
| Part IV — Human Flourishing | Legibility, Reversibility, Capability Amplification measures |
| Part V — Agent Accountability Map | Which agent owns which principle |
| Part VI — Decision Scope | What is in/out of system scope |
