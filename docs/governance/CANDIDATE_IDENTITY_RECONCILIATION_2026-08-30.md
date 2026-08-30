# Candidate Identity Reconciliation — 2026-08-30

**Status:** RECONCILED / PRE-FREEZE / NON-AUTHORIZING
**Purpose:** Record the current post-#151 candidate boundary and preserve historical identities without conflation.

## Current role separation

| Identity | Role | Experimental authority |
|---|---|---|
| `2a80f819…` | Historical P8 checklist ancestor | Historical lineage only |
| `303f4424…` | Prior integrated engineering/production source; exact source for prior P2/P6a evidence | Verified historical runtime boundary; not current candidate |
| `ac8ea267…` | Prior experimental verification boundary | Historical/candidate-scoped provenance |
| `c6157158…` | Prior pre-remediation candidate | Superseded / historical only |
| `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37` | **Post-#151 apparatus candidate/source identity** | **Designated for the new evidence cycle; NOT FROZEN** |
| `02c146d1…` | Candidate-designation/control commit | Control record only; not apparatus identity |
| `main` | Documentation/evidence lineage | Does not itself define apparatus identity |

## Candidate designation

PR #151 introduced substantive apparatus changes and merged as `05fa286…`. That merge establishes the new candidate-cycle apparatus boundary. The subsequent `02c146d1…` commit records explicit designation of that apparatus identity and is not itself the apparatus source.

The designated post-#151 candidate is:

`05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`

The designation does **not** create a freeze, grant authorization, or transfer historical evidence.

## Historical evidence boundary

P2 run `33300481208` and P6a run `33302495240` remain exact verified evidence for `303f4424…` and its associated deployment. They are not current-candidate evidence for `05fa286…` and require fresh execution against the exact current candidate/deployment before current-candidate verification.

Likewise, all pre-#151 P3–P9 records remain historical/pre-remediation evidence and do not transfer automatically to the post-#151 apparatus.

## Downstream binding rule

P1–P9 evidence for the current cycle MUST bind to `05fa286…` or to a later explicitly designated candidate if substantive apparatus changes occur.

The following are non-equivalent and MUST NOT be silently substituted for one another:

`apparatus SHA != designation/control commit != documentation lineage != workflow head SHA != deployment identity != freeze SHA`

A substantive change to protocol, runner, analysis, artifact schema, security/custody, retention, or executable governance requires candidate re-identification and affected-predicate re-verification.

## Current boundary

**Current apparatus candidate:** `05fa286…`
**Freeze:** NOT CREATED
**Pilot authorization:** NOT GRANTED
**Empirical N:** 0
**Experimental state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
