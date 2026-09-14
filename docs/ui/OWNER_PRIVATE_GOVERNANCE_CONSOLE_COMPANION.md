# Owner-private DGAF Governance Console Companion

**Status:** ACTIVE / OWNER-PRIVATE / READ-ONLY  
**Scientific-state effect:** NONE  
**Authority effect:** NONE  
**Source snapshot:** protected `main` at `b409403624181c86738113b029c4a12e42f0b318`  
**Console source commit:** `bc66767d2112392f6b780a3812c9c653ba7d7e72`

## Purpose

The owner-private DGAF Governance Console is a companion presentation surface for inspecting governance state, evidence boundaries, blockers, and admissible next actions. It provides creator and external-reader depths over one fact model, gate filtering, per-gate scope inspection, evidence-source search, and live GitHub freshness with a timestamped fallback.

The private console is not a governance authority, evidence store, authorization surface, or scientific transition mechanism. The private URL and access identifiers are intentionally omitted from this public repository.

## Truth boundary

The console must preserve the canonical High-Assurance boundary:

`PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 / CANONICAL DGAF EFFICACY NOT ESTABLISHED`

It separately represents the Track A Epoch 002 state:

- collection authorization: ACCEPTED;
- blinded collection: COMPLETE at 50 paired seed units / 2,250 observations;
- operator retained-byte admission: PENDING;
- dataset lock: NOT ESTABLISHED;
- unblinding: NOT AUTHORIZED;
- primary analysis: NOT AUTHORIZED / NOT RUN.

Track A completion counts must never be rendered as canonical High-Assurance scientific N.

## Integration contract

- `app/lib/governance.ts` is the public application's bounded presentation-state model.
- `docs/CURRENT_STATE.md` is the primary current-facing repository summary.
- `docs/PROJECT_STATUS.md` is a compatibility entrypoint only.
- The DGAF Operational Control Center in Notion is the interpreted governance mirror.
- GitHub remains authoritative for repository, commit, issue, PR, and CI identity.
- Runtime reachability remains operational evidence only.
- Missing or failed live refresh retains the last timestamped snapshot and must not promote or negate a governance predicate.

## Access and validation

The hosted companion is owner-only with no external viewers or groups. Unauthenticated access returns HTTP 401. The deployed HTML, JavaScript, and CSS assets were successfully retrieved through authenticated owner access; invariant tests preserve PRE-FREEZE, FAIL-CLOSED, NOT AUTHORIZED, canonical N=0, efficacy NOT ESTABLISHED, live-refresh/fallback separation, and read-only operation.

No public deployment or repository visibility change is authorized by this record.
