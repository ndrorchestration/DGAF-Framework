# DGAF-Framework Changelog

All notable changes to this project are documented here.
Format: [Semantic Versioning](https://semver.org/) | Governed by Agent Amethyst

---

## [1.0.6] — 2026-05-01

### Sessions 022c–023 — README Polish, SECURITY.md, PHDGE Branding Rename

**Formation:** Amethyst + Perplexity MCP (IP Sweep Formation)

#### Added
- `DGAF-Framework/README.md` — full 6-badge flat-square row (gold/teal/blue/purple/teal/green); full ecosystem link table (9 repos); clean license + provenance prose (S022c)
- `DGAF-Framework/.github/FUNDING.yml` — GitHub Sponsors button activated for governance spine (S022c)
- `DGAF-Framework/SECURITY.md` — expanded from 211-byte stub to full responsible disclosure policy: scope table, 48hr/5-day SLA, Sentinel escalation path, in/out-of-scope matrix (S022c)

#### Changed
- **PHDGE branding rename (S023):** `Phi-Harmonic Pentagon ecosystem` → `Phi-Harmonic Dynamic Governance Ecosystem (PHDGE)` ecosystem-wide
  - `Driftwatch/README.md` — 2 instances replaced: Core Capabilities bullet + How It Works diagram
  - Rationale: "Pentagon" implied 5-node limit (ensemble is 11+ agents); "Dynamic" mirrors DGAF's own name; PHD branding hook for external recognition
  - Retired term: `Phi-Harmonic Pentagon ecosystem` — 0 instances remain in org

#### Orchestration Patterns Applied
- Atomic Batch Push (push_files) — S022c 4-file push
- Pre-patch audit: code search + manual read of all governance docs before write
- Gap detection: 2 Pentagon instances found in Driftwatch README on full read (search index had 1); both patched

#### Harmonic Score
```
Score: 1.00 — SUSTAINED (S014–S023)
PHDGE rename: COMPLETE — 0 Pentagon instances remaining
README posture: COMPLETE — spine README fully polished
SECURITY.md: COMPLETE — full policy live
FUNDING.yml: COMPLETE — all 6 public repos
```

---

## [1.0.5] — 2026-05-01

### Sessions 022–022b — Ecosystem Surface Sweep

**Formation:** Amethyst + Perplexity MCP (IP Sweep Formation)

#### Added
- `.github/ISSUE_TEMPLATE/bug_report.md` — Amethyst-Governance-Eval-Stack, ai-prompt-systems-portfolio, Driftwatch, junior-apogee-app, sentinel-governance
- `.github/ISSUE_TEMPLATE/feature_request.md` — all 5 repos above
- `.github/pull_request_template.md` — all 5 repos above
- `.github/FUNDING.yml` — all 5 repos above (GitHub Sponsors button activated)
- 6 shields.io badges added to Amethyst-Governance-Eval-Stack, ai-prompt-systems-portfolio, Driftwatch, junior-apogee-app READMEs

#### Fixed
- `ai-prompt-systems-portfolio/README.md` — Language:Python badge omitted in S022; patched in S022b
- `Driftwatch/README.md` — license badge corrected MIT → Apache 2.0
- `sentinel-governance/.github/` — missed in S022 batch; full template suite added in S022b

#### Harmonic Score
```
Score: 1.00 — SUSTAINED (S014–S022b)
Template suite: complete across all 5 active public repos
FUNDING.yml: ecosystem-wide
Badge posture: 6-badge standard on all repos
```

---

## [1.0.4] — 2026-05-01

### Sessions 014–021 — Daily Governance Sweep Block

**Formation:** Amethyst + COLLEEN + Apogee + Sentinel + Perplexity MCP (IP Sweep Formation for S018–S021)

#### Added
- `docs/sync/DRIVE_SYNC_POLICY.md` — canonical cross-platform Google Drive sync specification (S019)
- `ENSEMBLE_ROSTER.md` — IP Sweep Formation added as recognized working triad; S021 session notes block
- `SWEEP_LOG.md` — Sessions 014–021 sealed; full day audit chain complete

#### Fixed / Upgraded
- `DGAF-Framework/LICENSE` — SPDX-License-Identifier: Apache-2.0 prepended (S019 P1-IP-01)
- `ai-governance-frameworks/LICENSE` — SPDX-License-Identifier: Apache-2.0 prepended (S019 P1-IP-02)
- `junior-apogee-app/LICENSE` — SPDX header added; `Ndr (Flickerflash)` → `Ndr (ndrorchestration)` (S019 P1-IP-03)
- `Driftwatch/LICENSE` — MIT → Apache-2.0 with SPDX; patent grant clause active (S020 P2)

#### Closed
- GAP-01: Gold-star-standards agent taxonomy (S015)
- GAP-03: ai-prompt-systems-portfolio DGAF vocabulary alignment (S016)
- GAP-07: Amethyst-Governance-Eval-Stack — all 4 dirs populated, 8 files, Tier 1 operational (S017)
- P1-IP-01/02/03: SPDX license headers (S019)
- P2: Driftwatch MIT → Apache-2.0 upgrade (S020)
- P3: gold-star-qa-framework deprecation — resolved via archive status (S020)

#### Deferred (no coherence risk)
- GAP-08: CROSS_REF back-links in dependent repos — COLLEEN async 🟡
- P3: Topic metadata on 5 repos — Njineer UI-only 🟡

#### Harmonic Score
```
Score: 1.00 — SUSTAINED ALL DAY (S014–S021)
All P1 and P2 items closed.
Flickerflash purge: COMPLETE.
License posture (all public repos): COMPLETE.
AGES eval stack: COMPLETE.
Drive sync policy: COMPLETE.
```

---

## [1.0.3] — 2026-04-29

### Added
- `ENSEMBLE_ROSTER.md` — canonical agent registry for all 11 active DGAF agents; retired agent log; triad configurations; cross-repo reference table
- Audit trail entry in `ECOSYSTEM-STATE.md` (Amethyst-Governance-Eval-Stack)

### Fixed
- `NOTICE` in `ai-prompt-engineering-portfolio`: Agent Lavender attribution retired; authority transferred to Agent Amethyst + DGAF stack

### Meta-Strategic Gaps Identified (COLLEEN × Apogee — April 29 session)

| ID | Gap | Agent Lead | Priority |
|----|-----|------------|----------|
| GAP-01 | Gold-star-standards agent taxonomy | COLLEEN | 🔴 High |
| GAP-02 | junior-apogee-app missing NOTICE | Sentinel | 🟠 Medium |
| GAP-03 | ai-prompt-systems-portfolio DGAF vocab | COLLEEN | 🟡 Medium |
| GAP-04 | No SWEEP_LOG.md | Amethyst | 🟡 Medium |
| GAP-05 | Driftwatch/AGENTS.md stale agent roles | Apogee | 🟡 Medium |
| GAP-06 | Drive ↔ GitHub sync unverified | Amethyst + COLLEEN | 🟡 Medium |
| GAP-07 | Amethyst-Governance-Eval-Stack subdirs unaudited | Apogee | 🟠 Medium |
| GAP-08 | No inter-repo CROSS_REF back-links | COLLEEN | 🟡 Low-med |

---

## [1.0.2] — 2026-04-29

### Fixed
- `NOTICE`: Replaced stale `CyberShield Defense Framework (CSDF)` project name with `DGAF-Framework`
- `NOTICE`: Updated agent roster to canonical Amethyst/Apogee/Sentinel/Reciprocity/Prodigy/DemiJoule/COLLEEN/Herald/Reson/Echolette/Lyra taxonomy
- `NOTICE`: Corrected capabilities section to reflect MDAR loop, Phi-Harmonic Gating, and OWASP Agentic Top 10 alignment
- `CHANGELOG.md`: Added v1.0.2 entry; annotated Agent Lavender as `(retired — superseded by Agent Apogee)`

---

## [1.0.1] — 2026-01-15

### Added
- Initial CONTRIBUTING.md with DGAF governance notice
- SECURITY.md with vulnerability reporting process

### Changed
- README: Updated agent attribution

---

## [1.0.0] — 2025-12-23

### Initial Release
- Core DGAF framework specification
- Agent Amethyst meta-orchestrator definition
- Agent Apogee evidence governance protocols
- Agent Sentinel safety layer specification
- NIST AI RMF alignment documentation
- Apache 2.0 licensing with NOTICE
- *Historical note: Early drafts referenced Agent Lavender (retired — superseded by Agent Apogee) and CSDF project name (corrected in v1.0.2)*
