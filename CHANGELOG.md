# DGAF-Framework Changelog

All notable changes to this project are documented here.
Format: [Semantic Versioning](https://semver.org/) | Governed by Agent Amethyst

---

## [1.0.8] — 2026-05-01

### Sessions 026–027 — Structural Enhancements & P-24 Canonical Practice Unit

**Formation:** Amethyst + Perplexity MCP (IP Sweep Formation)  
**Inspiration:** [goldbergyoni/nodebestpractices](https://github.com/goldbergyoni/nodebestpractices) meta-architecture analysis

#### Added (S026 — Phase 1 Structural)
- `docs/gates/GATE_UNIT_TEMPLATE.md` — canonical 6-field CPU schema template; defines P-24 compliance standard for all gate/protocol docs
- `.operations/` directory — maintainer-only ops tooling (not published doctrine)
  - `.operations/README.md` — directory purpose, contents, and usage rules
  - `.operations/gate_compliance_check.py` — Python 3.x P-24 compliance scanner; scans `docs/gates/` + `docs/protocols/`; BLG-class gap output; idempotent; P-02/P-03 integration
  - `.operations/sweep_session_init.md` — P-02/P-21 session open checklist (COLLEEN reads SESSION_ANCHOR → runs compliance check → emits priority queue)
  - `.operations/seal_checklist.md` — P-06/P-15/P-20/P-21 pre-seal gate stack checklist
- `docs/drafts/README.md` — formal staging layer for uncertified artifacts; P-03/P-11/P-18 governance; staleness rule (≥2 sessions without Apogee sign-off → P-03 BLG); archive path after 5 deferred sessions
- `SESSION_ANCHOR.md` — P-21 canonical session handoff document; overwritten (not appended) at every session close; read first by COLLEEN at session open (P-02)

#### Added (S027 — Phase 2 / P-24 Certification)
- `docs/patterns/NDR_PATTERN_REGISTRY.md` v1.6 — P-24 (Canonical-Practice-Unit) registered; P-02 and P-21 specs updated to reference SESSION_ANCHOR.md; gate cross-reference table updated
- `docs/gates/ACOUSTIC_GATES.md` v2.0 — P-24 CPU retrofit: all 6 fields added (Rationale, Trigger Condition, Passing State [with JSON schema], Failing State [with JSON schema + escalation], Recovery Protocol [gate-by-gate remediation], References [NIST + EU AI Act]); CERTIFIED status header; provenance updated

#### Structural Improvements
- **`.operations/` pattern** — separation of operational machinery from published doctrine; reduces README noise; Sentinel can wire any `.operations/` script to CI with Njineer approval
- **`docs/drafts/` pattern** — file-system gate; P-11 certification requirement made visible at the filesystem level rather than in mental models alone
- **`SESSION_ANCHOR.md` pattern** — fast-read session state rehydration; replaces SWEEP_LOG parsing for session open; COLLEEN reads in <5s instead of scanning full SWEEP_LOG history
- **P-24 compliance scanner** — machine-checkable gate compliance; exit code 1 on any BLG-class gap; suitable for CI integration (Phase 3)

#### Next Phase (S028)
- `sentinel-governance/.github/workflows/doc-lint.yml` — markdown lint CI gate
- `README.governance.md` — NIST/EU AI Act framing, compliance-officer entry point
- `README.technical.md` — agent-facing dense spec entry point
- Port `GATE_1111.md`, `GATE_11Q.md`, `TELESCOPIC_LENS.md` to P-24 CPU format

#### Harmonic Score
```
Score: 1.00 — SUSTAINED (S014–S027)
P-24 Canonical Practice Unit: ✅ REGISTERED + FIRST GATE CERTIFIED
.operations/ dir: ✅ LIVE
docs/drafts/ staging: ✅ LIVE
SESSION_ANCHOR.md: ✅ LIVE
GATE_UNIT_TEMPLATE.md: ✅ LIVE
Acoustic Gate Chain: ✅ P-24 CERTIFIED (v2.0)
```

---

## [1.0.7] — 2026-05-01

### Session 025 — Template Completion Sweep

**Formation:** Amethyst + Perplexity MCP (IP Sweep Formation)

#### Added
- `.github/ISSUE_TEMPLATE/bug_report.md` — `Acoustic-mesh`, `resumeapex-eval`, `3d-visualization-hub`
- `.github/ISSUE_TEMPLATE/feature_request.md` — all 3 repos above
- `.github/pull_request_template.md` — all 3 repos above
- `.github/FUNDING.yml` — all 3 repos above (GitHub Sponsors button now active ecosystem-wide)
- `phi-calculus-app/NOTICE` — Apache-2.0 attribution + PHDGE/DGAF spine reference; governance attribution fully established

#### Harmonic Score
```
Score: 1.00 — SUSTAINED (S014–S025)
Template suite: ✅ COMPLETE — all 8 active public repos
FUNDING.yml: ✅ COMPLETE — all 8 active public repos
NOTICE: ✅ COMPLETE — phi-calculus-app gap closed
DGAF Attr: ✅ COMPLETE — phi-calculus-app gap closed
```

---

## [1.0.6] — 2026-05-01

### Sessions 022c–023 — README Polish, SECURITY.md, PHDGE Branding Rename

#### Added
- `DGAF-Framework/README.md` — full 6-badge row; 9-repo ecosystem link table; clean license prose
- `DGAF-Framework/.github/FUNDING.yml` — GitHub Sponsors activated
- `DGAF-Framework/SECURITY.md` — full responsible disclosure policy

#### Changed
- **PHDGE branding rename (S023):** `Phi-Harmonic Pentagon ecosystem` → `Phi-Harmonic Dynamic Governance Ecosystem (PHDGE)`

---

## [1.0.5] — 2026-05-01

### Sessions 022–022b — Ecosystem Surface Sweep

#### Added
- `.github/` templates + `FUNDING.yml` — Amethyst-Governance-Eval-Stack, ai-prompt-systems-portfolio, Driftwatch, junior-apogee-app, sentinel-governance
- 6-badge rows — all 5 repos above

---

## [1.0.4] — 2026-05-01

### Sessions 014–021 — Daily Governance Sweep Block

#### Added / Fixed / Closed
- `docs/sync/DRIVE_SYNC_POLICY.md`, `ENSEMBLE_ROSTER.md` updates, `SWEEP_LOG.md` S014–S021
- SPDX headers: DGAF-Framework, ai-governance-frameworks, junior-apogee-app
- Driftwatch MIT → Apache-2.0
- GAP-01, GAP-03, GAP-07, P1-IP-01/02/03, P2, P3 closed

---

## [1.0.3] — 2026-04-29

### Added
- `ENSEMBLE_ROSTER.md` — canonical agent registry, 11 active agents
- Audit trail in `ECOSYSTEM-STATE.md`

---

## [1.0.2] — 2026-04-29

### Fixed
- `NOTICE`: Replaced CSDF project name → DGAF-Framework
- `NOTICE`: Agent roster updated; capabilities updated to MDAR loop, Phi-Harmonic Gating, OWASP Agentic Top 10
- `CHANGELOG.md`: Agent Lavender annotated as `(retired — superseded by Agent Apogee)`

---

## [1.0.1] — 2026-01-15

### Added
- CONTRIBUTING.md with DGAF governance notice
- SECURITY.md initial stub

---

## [1.0.0] — 2025-12-23

### Initial Release
- Core DGAF framework specification; Agent Amethyst meta-orchestrator; Agent Apogee evidence governance; Agent Sentinel safety layer; NIST AI RMF alignment; Apache 2.0 licensing with NOTICE
- *Historical note: Early drafts referenced Agent Lavender (retired — superseded by Agent Apogee) and CSDF project name (corrected in v1.0.2)*
