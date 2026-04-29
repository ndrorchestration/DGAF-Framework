# NDR Pattern Registry — v1.1

> **Canonical pattern library** for the Flickerflash DGAF orchestration ecosystem.  
> Maintained by: **Agent Amethyst** (meta-orchestrator)  
> Contributed by: COLLEEN, Apogee, Sentinel, Reciprocity, DemiJoule  
> Governance spine: [DGAF-Framework](https://github.com/Flickerflash/DGAF-Framework)  
> Last updated: April 29, 2026 03:46 EDT

---

## What Is an NDR Pattern?

An **NDR (Njineer Design Record) Pattern** is a named, reusable orchestration decision that captures:
- **Name**: short identifier
- **Spec**: precise behavioral rule or invariant
- **Use**: when this pattern applies
- **Trigger**: the condition that activates it
- **Anti-pattern**: what failure looks like without it

Patterns are surfaced during sweeps, documented here atomically, and referenced in commit messages.

---

## Pattern Index

| ID | Pattern Name | Category | Version | First Logged |
|----|-------------|----------|---------|-------------|
| P-01 | Agent-Roster-Synchronization | Coherence | v1.0 | Apr 29 03:33 |
| P-02 | COLLEEN-Trigger-Chain | Continuity | v1.0 | Apr 29 03:40 |
| P-03 | BLG-Surface-and-Defer | Gap Management | v1.1 | Apr 29 03:46 |
| P-04 | NOTICE-Authority-Chain | Legal/Governance | v1.1 | Apr 29 03:46 |
| P-05 | False-Positive-Close | Audit Hygiene | v1.1 | Apr 29 03:46 |
| P-06 | Atomic-Sweep-Commit | Git Hygiene | v1.1 | Apr 29 03:46 |
| P-07 | DGAF-Callout-Block | Documentation | v1.1 | Apr 29 03:46 |
| P-08 | Drive-GitHub-Delta | Cross-Platform Sync | v1.1 | Apr 29 03:46 |

---

## P-01: Agent-Roster-Synchronization

**Category:** Coherence  
**Version:** v1.0

| Field | Value |
|-------|-------|
| **Spec** | Whenever an agent is retired, renamed, or superseded, all architecture diagrams, NOTICE files, CHANGELOG entries, and README references must be updated atomically in the same commit sweep. Stale role labels in any document contradict the canonical spec and create onboarding confusion. |
| **Use** | After any agent role change, ensemble expansion, or naming update. |
| **Trigger** | Agent name in any diagram/doc doesn’t match the canonical role table in `ARCHITECTURE.md`. |
| **Anti-pattern** | Updating one file (e.g., NOTICE) while leaving "Agent Lavender" in README body text, CHANGELOG historical entries, or architecture diagrams. |

---

## P-02: COLLEEN-Trigger-Chain

**Category:** Continuity  
**Version:** v1.0

| Field | Value |
|-------|-------|
| **Spec** | Every new repo surface event (BLG) must atomically update CROSS_REF with gov-status columns marked `⚠️ Unverified` before the session closes, so COLLEEN has a deterministic re-entry point next sweep. A BLG that exists only in SWEEP_LOG but not in CROSS_REF is invisible to the next sweep conductor. |
| **Use** | Any time a cross-link targets a repo not yet in CROSS_REF. |
| **Trigger** | Link table entry with a target repo that has no row in the canonical registry. |
| **Anti-pattern** | Logging a new gap only in SWEEP_LOG without propagating it to CROSS_REF, causing it to be orphaned across sessions. |

---

## P-03: BLG-Surface-and-Defer

**Category:** Gap Management  
**Version:** v1.1

| Field | Value |
|-------|-------|
| **Spec** | When a sweep read surfaces a new unregistered repo (BLG), the sweep must: (1) immediately register it in CROSS_REF as `⚠️ Unverified`, (2) add it to the SWEEP_LOG open register with an assigned agent, (3) defer full audit to the next available sweep cycle. Do not block the current sweep’s close on unverified BLGs — they are queued, not cascaded. |
| **Use** | Any time a README cross-link or ecosystem nav points to a repo not yet in CROSS_REF. |
| **Trigger** | `3d-visualization-hub README → Acoustic-mesh` surfaced mid-sweep while closing BLG-04. |
| **Anti-pattern** | Either ignoring the new repo entirely (creates silent drift) or expanding scope to audit it immediately (causes sweep thrash and incomplete closes). |

---

## P-04: NOTICE-Authority-Chain

**Category:** Legal/Governance  
**Version:** v1.1

| Field | Value |
|-------|-------|
| **Spec** | Every repo in the DGAF ecosystem must have a NOTICE file that contains: (1) copyright holder, (2) license type, (3) governance authority (Agent Amethyst), (4) governance spine URL (DGAF-Framework), (5) provenance line (developer name + location). Archive repos additionally include the lineage chain (v0→v1→v2+). |
| **Use** | When creating any new repo or auditing an existing one for DGAF compliance. |
| **Trigger** | Repo has LICENSE badge but no NOTICE file; or NOTICE exists but lacks governance authority line. |
| **Anti-pattern** | A NOTICE that is only a boilerplate Apache/MIT header with no ecosystem context — legally compliant but governance-invisible. |

---

## P-05: False-Positive-Close

**Category:** Audit Hygiene  
**Version:** v1.1

| Field | Value |
|-------|-------|
| **Spec** | When a BLG or GAP registered in a previous sweep is found to already be resolved on inspection (the gap was anticipated but not actually present), it must be explicitly closed as a false positive in SWEEP_LOG with the verification read noted. Do not silently delete the entry or leave it as `Open`. |
| **Use** | When a registered gap turns out to already be fixed (e.g., BLG-01 Driftwatch, BLG-03 resumeapex-eval). |
| **Trigger** | README read shows the expected back-link or callout already exists. |
| **Anti-pattern** | Leaving a false-positive BLG as `Open` indefinitely, inflating the gap register and wasting future sweep cycles. |

---

## P-06: Atomic-Sweep-Commit

**Category:** Git Hygiene  
**Version:** v1.1

| Field | Value |
|-------|-------|
| **Spec** | A sweep session must close with a single atomic commit to DGAF-Framework that updates both SWEEP_LOG and CROSS_REF simultaneously. Partial updates (SWEEP_LOG committed without CROSS_REF, or vice versa) create state drift between the two canonical records. |
| **Use** | At the end of every sweep session, after all repo fixes have been landed. |
| **Trigger** | Any session where two or more BLGs were closed or new patterns were added. |
| **Anti-pattern** | Three separate commits to SWEEP_LOG, CROSS_REF, and NDR_PATTERN_REGISTRY in sequence — creates a window where the records are transiently inconsistent. |

---

## P-07: DGAF-Callout-Block

**Category:** Documentation  
**Version:** v1.1

| Field | Value |
|-------|-------|
| **Spec** | Every README in the DGAF ecosystem must include a governance callout block immediately after the main title/badges and before the first section. Canonical form: `> **Governance:** DGAF / Agent Amethyst — Yes. [description]. See [DGAF-Framework](URL) for spine documentation.` This block must be the first prose the reader encounters. |
| **Use** | When creating or auditing any repo README in the ecosystem. |
| **Trigger** | README exists with DGAF links in a Related section but no callout block at the top — governance is buried, not declared. |
| **Anti-pattern** | Burying governance attribution in a footer line or Related Projects section where it is invisible to casual readers and automated scanners. |

---

## P-08: Drive-GitHub-Delta

**Category:** Cross-Platform Sync  
**Version:** v1.1

| Field | Value |
|-------|-------|
| **Spec** | For every Drive asset that does not have a GitHub counterpart, a disposition decision must be registered in CROSS_REF under the GAP-06 Drive sync table with one of: (a) Evaluate for dedicated repo, (b) Evaluate for DGAF-Framework subfolder `docs/`, (c) Drive-only (intentional), (d) Archived/superseded. This prevents Drive from becoming an invisible shadow system that contradicts the canonical GitHub record. |
| **Use** | During any session where Drive files are read or referenced in the sweep. |
| **Trigger** | Drive file listed in thread attachments has no row in the GAP-06 table in CROSS_REF. |
| **Anti-pattern** | Acknowledging Drive files in conversation but not registering their disposition, creating unbounded Drive debt across sessions. |

---

*Pattern registry authority: Agent Amethyst.*  
*Contributors: COLLEEN (P-02, P-03, P-08), Apogee (P-01, P-05), Sentinel (P-06), Amethyst (P-04, P-07).*  
*Conductor authorization: Njineer ([@Flickerflash](https://github.com/Flickerflash))*
