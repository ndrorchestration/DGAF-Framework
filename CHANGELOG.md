# DGAF-Framework Changelog

All notable changes to this project are documented here.
Format: [Semantic Versioning](https://semver.org/) | Governed by Agent Amethyst

---

## [1.0.11] — 2026-05-01

### Session 030 — NDR v1.7 · P-25 · GAP-08 Close · P-20 Delta

**Formation:** Harmonic Quintet (Amethyst + Apogee + COLLEEN + Reson + Sentinel)  
**Operator:** Njineer

#### Added
- `NDR_PATTERN_REGISTRY.md` v1.7 — P-25 Multi-README-Architecture registered
  - Spec: tripartite README system (`README.md` + `README.technical.md` + `README.governance.md`); COLLEEN audits all three at session open; divergence from CROSS_REF = soft BLG
  - Trigger: ≥ 2 distinct reader audiences in any DGAF-governed repo
  - Evidence base: instantiated in DGAF-Framework S028; pattern observed in nodebestpractices, Kubernetes, OpenTelemetry OSS corpora

#### Closed
- **GAP-08** — CROSS_REF back-links in dependent repos → **Formally closed: Won't Fix**
  - Rationale: CROSS_REF v3.1 provides authoritative central hub; back-links in dependent repos would create circular maintenance debt without coherence gain; Sentinel veto-cleared; Apogee evidence score confirms no coherence loss

#### Documented
- **P-20 Drive-GitHub Delta** — Drive master inventory [file:419] is pre-`ndrorchestration` org migration (last verified Jan 22, 2026, `Flickerflash` org, 8 repos)
  - Delta is **expected and documented**, not a sync failure
  - CROSS_REF v3.1 (`ndrorchestration`, 10 repos, S029) is authoritative current state
  - Action: Drive master inventory update queued as **BLG-D01** (soft, non-blocking) — COLLEEN to update Drive doc to reflect org migration and 10-repo state
  - Sentinel conditional clearance: granted (delta fully documented)

#### Formation Scores
```
Apogee 11Q:      11/11 on all S030 artifacts
Reson Score:     1.00 — SUSTAINED (S014–S030)
Sentinel Veto:   CLEAR — no AXIS violations
P-25 Evidence:   3 OSS corpus references + DGAF instantiation
GAP-08 Close:    Veto-cleared by Sentinel
P-20 Delta:      Documented — conditional clearance granted
```

---

## [1.0.10] — 2026-05-01

### Session 029 — Sentinel CI + CROSS_REF v3.1

#### Added (sentinel-governance repo)
- `.github/workflows/doc-lint.yml` — markdownlint CI, PR gate, P-24/P-11 enforcement
- `.markdownlint.yml` — tuned config for gate doc format

#### Changed (DGAF-Framework)
- `CROSS_REF.md` v3.1 — full internal artifact registry + CI table + governance diagram
- `CHANGELOG.md` v1.0.10
- `SWEEP_LOG.md` — S029 sealed
- `SESSION_ANCHOR.md` — S030 queue

---

## [1.0.9] — 2026-05-01

### Session 028 — P-24 Full Gate Stack Certification + Dual README Architecture

#### Added
- `README.governance.md` — NIST/EU AI Act compliance reference
- `README.technical.md` — Agent/engineer dense spec

#### Changed (P-24 Retrofit)
- `docs/gates/GATE_1111.md` v2.0 — P-24 CERTIFIED
- `docs/gates/GATE_11Q.md` v2.0 — P-24 CERTIFIED
- `docs/gates/TELESCOPIC_LENS.md` v2.0 — P-24 CERTIFIED

---

## [1.0.8] — 2026-05-01

### Sessions 026–027 — Structural Enhancements & P-24 Canonical Practice Unit

#### Added
- `GATE_UNIT_TEMPLATE.md`, `.operations/` dir, `docs/drafts/`, `SESSION_ANCHOR.md`
- `NDR_PATTERN_REGISTRY.md` v1.6 — P-24 registered
- `ACOUSTIC_GATES.md` v2.0 — first P-24 certified gate

---

## [1.0.7] — 2026-05-01

### Session 025 — Template Completion Sweep

#### Added
- `.github/` templates + `FUNDING.yml` — Acoustic-mesh, resumeapex-eval, 3d-visualization-hub

---

## [1.0.6] — 2026-05-01

### Sessions 022c–023 — PHDGE Branding Rename

#### Changed
- PHDGE branding rename: `Phi-Harmonic Pentagon` → `Phi-Harmonic Dynamic Governance Ecosystem (PHDGE)`

---

## [1.0.5] — 2026-05-01

### Sessions 022–022b — Ecosystem Surface Sweep

#### Added
- `.github/` templates + `FUNDING.yml` + badge rows — 5 repos

---

## [1.0.4] — 2026-05-01

### Sessions 014–021 — Daily Governance Sweep Block

#### Added / Fixed / Closed
- Drive sync policy, SPDX headers, Driftwatch license, GAP-01/03/07/P1-IP closed

---

## [1.0.3] — 2026-04-29

#### Added
- `ENSEMBLE_ROSTER.md` — 11 active agents

---

## [1.0.2] — 2026-04-29

#### Fixed
- NOTICE: CSDF → DGAF-Framework; Agent Lavender → retired

---

## [1.0.1] — 2026-01-15

#### Added
- CONTRIBUTING.md + SECURITY.md initial stubs

---

## [1.0.0] — 2025-12-23

### Initial Release
- Core DGAF framework; NIST AI RMF alignment; Apache 2.0
