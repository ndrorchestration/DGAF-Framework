# Temporal / Historical Document Catalog — 2026-09-02

**Status:** CANONICAL RECONCILIATION INDEX / NON-AUTHORIZING

## Live overlays

- `docs/governance/TEMPORAL_SSOT_RECONCILIATION_2026-09-02.md` — canonical temporal interpretation.
- `docs/taxonomy/TRANSVERSAL_AGREEMENT_AND_DEPENDENCY_TAXONOMY_2026-09-02.md` — transversal dependency/agreement vocabulary.
- `docs/NDR_PATTERN_REGISTRY_UNIFIED_TRANSVERSAL_OVERLAY_2026-09-02.md` — pattern-registry transversal overlay.

## Historical/role-scoped repository documents

The following classes are historical or role-scoped records and must not be treated as the sole live candidate authority merely because they contain current-looking terminology:

- `README.md`, `docs/CURRENT_STATE.md`, `docs/PROJECT_STATUS.md` — primary project/status surfaces; current candidate identity must be resolved through the temporal overlay and live GitHub objects.
- `docs/governance/P1_TO_P9_EVIDENCE_MATRIX.md`, `docs/evidence/PDMAL_EVIDENCE_INDEX.md` — evidence indexes; candidate/deployment/run/artifact identities remain exact-scoped.
- `docs/experiment/*` — experimental handoffs, freeze manifests, deployment closure, custody, and protocol records; each record retains the identity it was created against.
- `docs/governance/*` — governance decisions, readiness, audits, and reconciliation records; dated records remain historical unless explicitly designated as live overlays.
- `docs/architecture/*` — architecture plans and readiness snapshots; their stated PR/commit identities are historical/role-scoped unless rebound by a later control record.
- `SWEEP_LOG/*`, historical analyses, progress showcases, and completion records — chronological provenance; do not rewrite history to reflect later knowledge.

## Interpretation rule

A historical document is considered **reconciled** when its original content remains intact and a current temporal overlay identifies its present status, role, and non-substitution boundary.

A document is not required to be rewritten merely because a later candidate exists. Rewriting a historical record can destroy chronology and provenance.

## Current state reference

As of 2026-09-02:

- `main` documentation/control-plane lineage: `275756fd81c975f17ae3d16d24e599db0617cf85`.
- Active experimental candidate: PR #192 head `58ba9a072f40e94638b0332eeec19dd882a7ff95`.
- Candidate tree: `abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb`.
- Corrected apparatus/source anchor: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`.
- Exact candidate Vercel deployment: not evidenced; current provider status is rate-limited.
- Experimental boundary: `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`.
- Fresh exact-head CI wave: all reported workflows PASS, including Pre-Freeze Runner Validation and Pre-Authorization Security.

## Temporal integrity principle

`engineering progress != documentation progress != evidence closure != freeze != authorization != empirical progress`.

This catalog does not change any gate state, create a freeze, grant authorization, or establish empirical evidence.
