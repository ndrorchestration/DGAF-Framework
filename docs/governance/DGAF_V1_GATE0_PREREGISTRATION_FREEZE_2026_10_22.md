# DGAF v1 Gate 0 — owner/operator preregistration freeze record

**Effective date:** 2026-10-22
**Controller:** <https://github.com/ndrorchestration/DGAF-Framework/issues/1421>
**Protected-main baseline at freeze:** `1a95b94332dffb404c5a3ce026d70781a8c10b90`
**Freeze class:** OWNER_OPERATOR_PREREGISTRATION / SAME_SYSTEM_NONINDEPENDENT
**Independent Gate 0 acceptance:** NOT_ESTABLISHED

This record freezes the release **acceptance oracles and review taxonomy** prospectively.
It does not mark Gate 0 complete and does not retroactively turn pre-freeze tests,
audits or operator classifications into accepted evidence.

## Frozen source documents

| Document | SHA-256 | Role |
| --- | --- | --- |
| DGAF v1 bounded release completion and epistemic assurance | `106d359e4b2a82e6a51a1b05d48e044b24c64bd6b61605c64587ed75cf9f8477` | release scope/oracles, non-goals, reviewer eligibility and change control |
| claims-and-evidence register seed | `a95edc10535ab23989e9af7304fd823cdcc42013545495f71435d01107cd222b` | claim vocabulary and evidence-binding schema |
| gate evidence/exclusion template | `257946af2196ab2c018245380edb93d025419653e362adced509fecad294226b` | evidence, severity, reachability and threat-model schema |
| preliminary source reachability inventory | `b942662ccdeb781a64573a336b88a5da4e8e8d466d89d6116e7f114b89ca45e4` | pre-freeze inventory only; not accepted gate evidence |

## Freeze semantics

- `GATE_0_ORACLES=FROZEN_V1`
- `GATE_0_SCOPE_BINDING=BLOCKED`
- `GATE_0_ACCEPTANCE=NOT_INDEPENDENTLY_CONFIRMED`
- `G1..G7=BLOCKED`
- `DGAF_V1_RELEASE=HOLD`
- `SCIENTIFIC_N_INCREMENT=0`
- `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`
- `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`
- `HIGH_ASSURANCE=NOT_AUTHORIZED`

The inventory work performed before this freeze may be re-used only after it is
rebound to the frozen oracle version and exact evidence/source identities.
A later oracle change requires a new version and digest, a rationale, an affected-
evidence list, and re-opening any dependent disposition.

## Remaining Gate 0 completion requirements

1. Bind exact v1 supported action classes and excluded/unreachable capabilities.
2. Re-adjudicate current blockers under these frozen oracles.
3. Obtain eligible independent reviewer conflict disclosure and written sign-off.
4. Bind accepted evidence to an immutable final candidate and signed release identity.
5. Keep any missing, conflicting or non-independent evidence BLOCKED.

The workstation used for this preregistration does not currently expose a configured
commit-signing key. Repository publication of this record may therefore be unsigned;
that is an explicit release-admission limitation, not evidence of signing.

## Formatting-only source rehash candidate

The parent commit `ded5cf5e99b5f56f0e31bad60e234edcdd43fe1e` retains the original Gate 0 source
bytes and hashes. This isolated candidate repairs Markdown heading/list spacing
and bare URL markup without changing the wording of acceptance oracles,
gate statuses, or eligibility requirements. Updated hashes in the table above
supersede parent hashes only if this candidate is explicitly re-preregistered
under a recorded new digest and eligible review; no retrospective gate PASS
or release authority is implied.
