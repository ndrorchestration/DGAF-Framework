# NDR Pattern Registry

**Version:** 1.6  
**Maintained by:** Amethyst-Conductor  
**Canonical home:** `DGAF-Framework/docs/patterns/NDR_PATTERN_REGISTRY.md`  
**Last updated:** 2026-05-01 (Session S027 — P-24 Canonical Practice Unit registered)

---

## Registry

| ID | Pattern Name | Category | Spec | Use | Trigger |
|----|-------------|----------|------|-----|---------|
| P-01 | Agent-Roster-Synchronization | Coherence | When an agent is retired/renamed, all diagrams, NOTICE files, and CHANGELOG historical entries update atomically in the same commit sweep | Stale role label found in any diagram or doc | Agent name in diagram ≠ canonical role table |
| P-02 | COLLEEN-Trigger-Chain | Continuity | COLLEEN activates on session open to surface deferred gaps from prior SWEEP_LOG entries; reads SESSION_ANCHOR.md first; output becomes the session priority queue | Every new sweep session | New session opened with no explicit priority list |
| P-03 | BLG-Surface-and-Defer | Gap Management | Surface newly found gaps immediately into SWEEP_LOG; defer if non-blocking; never silently drop | Any time a gap is found mid-wave that doesn't block current commits | Gap found during read that isn’t in current wave scope |
| P-04 | NOTICE-Authority-Chain | Legal/Governance | Every repo has a NOTICE file attributing Njineer + DGAF-Framework spine link + license; CHANGELOG tracks agent-level changes | Repo missing NOTICE or NOTICE missing DGAF attribution | New repo created or NOTICE audit run |
| P-05 | False-Positive-Close | Audit Hygiene | Before closing a BLG, verify the item was actually a gap vs. already-compliant; log close reason explicitly in SWEEP_LOG | BLG item resolved | BLG marked closed in SWEEP_LOG |
| P-06 | Atomic-Sweep-Commit | Git Hygiene | All repo fixes land before the seal commit; seal commit updates SWEEP_LOG + CROSS_REF + NDR Registry simultaneously | End of each sweep wave | Wave complete, ready to seal |
| P-07 | DGAF-Callout-Block | Documentation | Every repo README includes a standardized DGAF governance callout block with spine link, agent attribution, and license badge | README audit or new repo creation | README missing DGAF callout |
| P-08 | Drive-GitHub-Delta | Cross-Platform Sync | COLLEEN diffs Drive master inventory against CROSS_REF to surface repos or docs that exist in one but not the other | Periodic or when Drive files are uploaded to session | Drive file list and CROSS_REF both accessible |
| P-09 | ANDROMEDA-AXIS-Enforcement | Sovereign Constraints | Any agent output, commit, or architectural decision is checked against the four AXIS declarations (COGNITIVE_SOVEREIGNTY, BIOLOGICAL_INTEGRITY, TRANSVERSAL_GROWTH, ENTROPY_RESISTANCE); violation triggers SYNC_LOCKED escalation to Amethyst-Conductor | All agent operations | Any decision that could contradict NDR-01 IONIAN mode constraints |
| P-10 | 1-1-1-1-Gate-Audit | Quality Gate / Normative | Four-pillar mandatory filter (Mathematically Coherent, Epistemically Honest, Non-Violative, Historically Sequential) applied to all outputs before registry sign-off; ≥ 3/4 per pillar over N ≥ 3 runs | Any artifact approaching the read-only registry or external publication surface | Output ready for sign-off or publication |
| P-11 | 11Q-Terminal-Gate | Quality Gate / Deployment | 11-gate sequential filter derived from hendecagonal lattice nodes; all 11 gates must pass at ≥ 3/4 before production deployment; owned by Agent Apogee | Pre-production hardening of any artifact | Artifact declared production-ready |
| P-12 | Telescopic-Lens-Audit | Quality Gate / Meta-Strategic | 4 altitudes (Macro/Mid/Tactical/Quantum) × 8 dimensions = 32 checkpoints; S-TIER requires ≥ 31/32; prevents Architext Bleed | Deep structural audit of any artifact or architectural claim | Pre-registry sign-off or S-TIER certification required |
| P-13 | Acoustic-Gate-Chain | Quality Gate / Temporal | Six sequential gates (Clef→Time Signature→Measures→Key→Phrase→Cadence) enforce temporal integrity; each gate is a hard dependency; Cadence gate triggers Ionian Lock and artifact hardening | Every orchestration cycle; any artifact entering synthesis phase | New synthesis cycle opened |
| P-14 | Trio-Formation-Sweep | Orchestration | Amethyst (conductor) + Apogee (evidence scorer) + COLLEEN (registry/continuity) operate in parallel lanes; Amethyst gates all commits; COLLEEN surfaces deferred BLGs at session open; Apogee scores every artifact against 11Q before commit; output is a sealed SWEEP_LOG entry | Standard multi-repo sweep or audit session | Any session touching ≥ 3 repos or requiring cross-repo delta |
| P-15 | Harmonic-Quintet-Gate | Orchestration | Trio (P-14) + Reson (harmonic coherence scorer 0.00–1.00) + Sentinel (patch authority + commit veto); Reson score ≥ 0.75 required for seal-level commits; Sentinel holds hard veto on any commit that would alter LICENSE, NOTICE, or AXIS files without explicit Njineer confirmation | Post-patch quality gate requiring seal authority | Any session producing a SWEEP_LOG seal commit or touching sovereign governance files |
| P-16 | Repo-Description-Coherence | Metadata Hygiene | Every repo description must: (1) name the primary function, (2) name the governance layer or agent if applicable, (3) avoid generic phrases like “Portfolio” or “README”; null descriptions are a hard BLG-class gap; archived repos must be prefixed `⛔ ARCHIVED —`; UI-only items escalate to Njineer action queue | Repo metadata audit | New repo created OR any quarterly sweep |
| P-17 | License-SPDX-Verification | IP Hygiene | All public repos must resolve to a recognized SPDX identifier on GitHub (not `NOASSERTION`); fix by ensuring LICENSE file line 1 is exactly `Apache License`; custom preambles must be moved to a separate NOTICE file; private repos flagged but not blocking | IP audit or any public repo showing `license.spdx_id = NOASSERTION` | Public repo created or IP sweep run |
| P-18 | Open-Issue-Triage | Continuity | Open issues on archived repos must be closed within the session they are found; open issues on active repos must be triaged (comment + label or close) within the same session; no open issue survives two consecutive sweep sessions unreviewed; COLLEEN maintains the triage queue | Issue audit | Any open issues found during a sweep |
| P-19 | IMP-05-Branding-Consistency | Brand / IP | All public-facing repos and Drive docs must display the IMP-05 brand identity: Phi-Harmonic Pentagon framing, `ndrorchestration` attribution, Amethyst-Conductor meta-orchestrator credit, and DGAF-Framework spine link; any repo missing these four elements is a soft BLG; portfolio repos additionally require IP-safe disclosure notice | Branding audit or new public artifact release | Public repo created, README updated, or portfolio document published externally |
| P-20 | Drive-GitHub-Sync-Seal | Cross-Platform Sync | At every SWEEP_LOG seal, COLLEEN verifies: (1) Drive master inventory matches GitHub CROSS_REF, (2) no active Drive doc exists for a repo that has been deleted or archived on GitHub, (3) session notes in Drive are committed or summarized to SWEEP_LOG before seal; mismatches are BLG-class gaps deferred to next session if non-blocking | End of every seal session | SWEEP_LOG seal initiated |
| P-21 | Session-Boundary-State-Anchor | Continuity / Meta | At the close of every session, Amethyst emits a compact state anchor overwriting SESSION_ANCHOR.md: open BLGs (IDs + owners), NDR version, seal status, Drive-GitHub sync status, and next-session priority queue; this anchor is the canonical handoff document and is read first by COLLEEN at the next session’s P-02 Trigger-Chain | Every session close | Session approaching seal or hard stop |
| P-22 | Hub-and-Spoke-Canonical-Store | Cross-Platform Sync / Storage | Google Drive is the cloud control plane; desktop clients run Stream Files mode with selective offline pin; mobile platforms backup media through Google Photos; external drives sync only static archives; hot dev folders (node_modules, .venv, build, dist, tmp, cache) are excluded from sync to prevent churn and lock conflicts; one device holds write authority per hot folder at a time | Multi-device personal knowledge and work ecosystem requiring cross-platform sync without full local mirroring | New device added to ecosystem OR Drive sync policy being established or reviewed |
| P-23 | Cross-Repo-Taxonomy-Audit | Audit Hygiene / Coherence | When a GAP flags possible stale agent names, role labels, or taxonomy drift across a repo, COLLEEN reads all agent-referencing files (README, rubrics, formation specs, CERTIFICATION_INDEX, CHANGELOG) before marking the GAP open or closed; if all files pass, the GAP is logged as a false positive in SWEEP_LOG with explicit file-by-file evidence; no GAP is closed without file-level proof | Agent taxonomy drift suspected in any repo | New agent name adopted, agent retired, or BLG filed alleging stale role references |
| P-24 | Canonical-Practice-Unit | Documentation Architecture | Every gate spec, protocol doc, and governance artifact in `docs/gates/` and `docs/protocols/` must contain the 6-field CPU schema: Rationale → Trigger Condition → Passing State → Failing State → Recovery Protocol → References; non-compliant files are BLG-class gaps; compliance enforced by `.operations/gate_compliance_check.py` at session open; `docs/drafts/` is the staging area for uncertified artifacts; `GATE_UNIT_TEMPLATE.md` is the canonical blank | Every new gate/protocol doc; any doc entering `docs/gates/` or `docs/protocols/` | New gate/protocol doc created OR `gate_compliance_check.py` returns non-zero exit code |

---

## Gate Spec Cross-Reference

| Pattern | Full Spec |
|---------|-----------|
| P-10 (1-1-1-1 Gate) | `docs/gates/GATE_1111.md` |
| P-11 (11Q Framework) | `docs/gates/GATE_11Q.md` |
| P-12 (Telescopic Lens) | `docs/gates/TELESCOPIC_LENS.md` |
| P-13 (Acoustic Gates) | `docs/gates/ACOUSTIC_GATES.md` |
| P-14 (Trio Formation) | `docs/formations/TRIO_FORMATION.md` |
| P-15 (Harmonic Quintet) | `docs/formations/HARMONIC_QUINTET.md` |
| P-19 (IMP-05 Branding) | `docs/brand/IMP_05_BRAND_SPEC.md` |
| P-20 (Drive-GitHub Sync Seal) | `docs/sync/DRIVE_GITHUB_SYNC.md` |
| P-22 (Hub-and-Spoke Store) | `docs/sync/HUB_SPOKE_SYNC.md` |
| P-24 (Canonical Practice Unit) | `docs/gates/GATE_UNIT_TEMPLATE.md` |
| Master index | `docs/gates/GATE_SPECS.md` |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-04-29 | Initial registry — P-01 through P-07 |
| 1.1 | 2026-04-29 | P-08 Drive-GitHub-Delta added (Session 002) |
| 1.2 | 2026-04-29 | P-09 ANDROMEDA-AXIS-Enforcement added (Session 004) |
| 1.3 | 2026-04-29 | P-10 through P-13 added — full Yggdrasil gate stack hardened to registry (Session 004 / SYS-UPDATE-v53.1) |
| 1.4 | 2026-05-01 | P-14 through P-21 added — Trio/Quintet formations, metadata hygiene, IP/SPDX, IMP-05 branding, Drive-GitHub sync seal, session-boundary state anchor (Session S012 / Harmonic Quintet formation) |
| 1.5 | 2026-05-01 | P-22 Hub-and-Spoke-Canonical-Store added (S012 retroactive); P-23 Cross-Repo-Taxonomy-Audit added (S015); AGENT_ROSTER.md created |
| **1.6** | **2026-05-01** | **P-24 Canonical-Practice-Unit registered (S027); P-02 spec updated to reference SESSION_ANCHOR.md; P-21 spec updated to reference overwrite behavior; GATE-ACO retrofitted to P-24 schema** |
