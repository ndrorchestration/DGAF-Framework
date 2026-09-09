# Current-Facing Documentation Recency Audit — 2026-09-09

Status: **OPEN FINDINGS / NON-SCIENTIFIC**

Audit anchor: `8434a66f47ef9256c5f608b839886624e6d0d6e2` (merged PR #521)

## Purpose

Distinguish repository-wide tracked-file coverage from the stronger question of whether every document presented as current-facing still reflects the latest accepted implementation, governance, vocabulary, and evidence boundary.

This audit does not authorize execution, alter Track A, change scientific N, resolve agent identity conflicts, establish efficacy, or authorize High-Assurance.

## Current-facing surfaces reviewed

- `README.md`
- `docs/CURRENT_STATE.md`
- `docs/PROJECT_STATUS.md`
- `docs/PUBLIC_TRANSLATION_LAYER.md`
- `docs/VOCABULARY_TRANSLATION_MATRIX.json`
- `docs/VOCABULARY_GOVERNANCE.md`
- `ENSEMBLE_ROSTER.md`
- `docs/architecture/DGAF_V1_AGENT_ROLE_MAPPING.md`
- Notion `DGAF-Framework — Operational Control Center` as the governance/control-plane mirror

Historical dated records are not required to match current state when they are clearly classified as historical.

## Findings

### F-01 — `docs/CURRENT_STATE.md` recency metadata is stale

The live scientific boundary remains materially correct, but the front matter still records `last_verified: 2026-09-08` while current signed `main` is the 2026-09-09 PR #521 merge.

Classification: **RECENCY / METADATA**

Scientific effect: **NONE**

### F-02 — stale moving-main wording remains in `docs/CURRENT_STATE.md`

The Track A identity section describes the primary-analysis authorization tooling merge as `current accepted main`. That SHA is a valid historical tooling merge identity, but it is no longer repository `main` after subsequent security, custody, identity, research, runtime, and vocabulary merges.

Required correction: retain the immutable tooling merge identity, remove the moving `current accepted main` characterization.

Classification: **CURRENT-FACING WORDING**

Scientific effect: **NONE**

### F-03 — recent engineering/control-plane completions are not summarized in the live state narrative

The current scientific boundary did not change, but the live ecosystem summary does not yet surface the following merged developments:

- #503 — Next.js security dependency refresh;
- #507 — Track A custody handoff runbook;
- #511 — identity/scientific-state decoupling;
- #513 — non-destructive branch-disposition inventory;
- #514 — prospective weighted Forman–Ricci replication lane;
- #517 — Task-4 corpus-intake lock;
- #520 — exact-source live staging-breaker evidence capped at `PASS_STRUCTURAL_LIVE_STAGING_ONLY`;
- #521 — Vocabulary Translation Matrix v2 and vocabulary governance.

These are engineering, governance, research, runtime, and documentation developments. They do not promote Track A or High-Assurance scientific state.

Classification: **SUMMARY COVERAGE**

### F-04 — identity ontology remains intentionally unresolved

Issue #522 is the controlling follow-up for:

- Sentinel / Sentinel-Phi lineage;
- Ionia agent-vs-state ontology;
- A-09/A-10/A-11/A-12 designation collisions involving Zenith / Reson / Lyra / Echolette;
- COLLEEN / Librarian designation drift.

Vocabulary translation must preserve these conflicts rather than silently adjudicating them.

Classification: **OPEN GOVERNANCE DEPENDENCY**

### F-05 — full repository coverage is not equivalent to documentation recency

`Full Repository Coverage Audit` inventories and hashes every tracked file and scans defined provenance/consistency patterns. It does not establish that every current-facing narrative is semantically current. A dedicated recency/adjudication pass is therefore required after material state-model, vocabulary, architecture, or public-documentation transitions.

Classification: **PROCESS GAP**

## Fresh audit evidence already present on PR #521 / merged main

The PR #521 exact-head validation and post-merge main workflows provide fresh evidence for ordinary automated governance classes, including vocabulary validation, claim/IP hygiene, control-state consistency, provenance, ecosystem registry auditing, Python quality, and the normal repository CI suite.

Those passes establish their defined predicates only; they are not a substitute for the findings above.

## Audit classes requiring explicit refresh or adjudication

Priority order:

1. current-facing documentation recency/adjudication;
2. cross-authority agent identity ontology adjudication under #522;
3. GitHub ↔ Notion control-plane reconciliation after #521/#522 changes;
4. cross-repository ecosystem architecture/documentation audit;
5. security/dependency/provenance audit across satellite repositories;
6. P4-B / Mode-T strict-chain readiness refresh before relying on the 2026-09-05 record as current;
7. external portfolio / resume / public-claims evidence reconciliation.

The seven-gate treatment-fidelity audit dated 2026-09-08 remains recent and scope-specific; it does not require rerun solely because vocabulary/documentation changed unless its bound treatment or implementation identities change.

## Current scientific boundary preserved by this audit

- Track A prospective collection: **COMPLETE / BLINDED / RETAINED**
- inferential seed units: **50**
- blinded raw observations: **2,250**
- dataset lock: **ESTABLISHED**
- unblinding authorization: **ESTABLISHED — mapping release/decryption scope only**
- matching custody-key handoff: **NOT ESTABLISHED**
- unblinded analysis input: **NOT YET MATERIALIZED**
- primary analysis: **NOT AUTHORIZED / NOT RUN**
- canonical DGAF efficacy: **NOT ESTABLISHED**
- canonical High-Assurance: **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**

## Completion condition

This audit may be closed only after:

1. F-01/F-02/F-03 are reconciled on current-facing repository documentation;
2. Notion is read back and reconciled to the same GitHub authority boundary;
3. #522 remains visibly open or is replaced by an explicit accepted ontology adjudication;
4. the exact audit-repair PR head completes a fresh full CI wave, including Full Repository Coverage Audit, with zero failures and zero active checks.
