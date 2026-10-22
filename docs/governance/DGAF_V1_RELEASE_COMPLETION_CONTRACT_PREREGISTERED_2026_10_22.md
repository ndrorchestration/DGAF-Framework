# DGAF v1: Bounded Release Completion and Epistemic Assurance — Preregistered Oracles v1

**Disposition:** ORACLES PREREGISTERED / OWNER-OPERATOR FROZEN / INDEPENDENT GATE ACCEPTANCE NOT ESTABLISHED / RELEASE HOLD. 2026-10-22.
**Controller:** <https://github.com/ndrorchestration/DGAF-Framework/issues/1421>
**Proposed Notion source:** <https://app.notion.com/p/401f5bad238b8140bcc2d19ec3c82b28>
**Source baseline:** protected main `1a95b94332dffb404c5a3ce026d70781a8c10b90` (revalidate before decisions).

## Bounded meaning of finished

DGAF v1 completion is bounded software product/release evidence, not scientific certification.
The release must be reviewed against criteria frozen **before** classifying issues or
claims, by independent and eligible reviewers with written conflict-of-interest
disclosures and reproducible source/evidence identities. Every supported action
class must demonstrate denial on its enumerated failure modes, including
unavailable authority and fallback-to-allow attempts, without extrapolating
from those tests to global safety.

## Gate 0: mandatory prior preregistration

Freeze before audit: release scope, supported action classes, excluded and
unreachable execution paths, exact candidate SHA, public-claim vocabulary,
seven gate oracles, threat model, severity taxonomy, reviewer eligibility,
evidence custody rules and the change-control process. Amendment requires
explicit rationale, affected evidence, and fresh eligible review. Existing
CI success cannot retroactively satisfy an unregistered oracle.

## Frozen release-gate oracles

- **G1 Scope freeze:** action-class matrix, versions, assumptions, boundaries,
  user-facing interfaces, supported/unsupported deployment topology.
- **G2 Release safety:** independently adjudicated P0/critical problems;
  inaccessible or hard-disabled excluded functionality; negative reachability controls.
- **G3 Source reconciliation:** exact SHA aligns implementation, documentation,
  capability registry, authority rules and public claims.
- **G4 Bounded runtime verification:** predefined fault classes, invalid inputs,
  authority outage, stale data, revocation, replay/race, conflicts and no fallback-to-allow.
- **G5 Independent review:** eligible reviewer conflicts disclosed, clean
  reproduction, retained negative findings, separate independent sign-off.
- **G6 Reproducible distribution:** version locks, clean install, build provenance,
  artifact hashes, SBOM, independent source/driver rerun and supported platforms.
- **G7 Release admission:** source- and artifact-bound adjudication, immutable
  signed candidate, residual risk, no unresolved release-critical blockers.

Each gate needs `gate_id`, `owner`, `verifier`, `COI`, `date`,
`evaluated_commit`, `frozen_oracle_version`, `artifact_url`, `sha256`,
`observation`, `negative_cases`, `residual_risk`, `disposition`
(PASS, FAIL or BLOCKED), and attributed `signoff`. Missing = BLOCKED.

## Frozen reviewer eligibility and change control

An eligible independent release reviewer must not be an author or contributor to
the evaluated change, must not hold direct commit/write authority for the
evaluated repository during the review, must disclose employment, funding,
personal and other material conflicts, must be able to reproduce the evidence
from a clean environment, and must return a written source-bound disposition.
Reviewer eligibility is itself subject to recorded adjudication.

These oracles are frozen prospectively. Earlier inventories and tests remain
useful evidence but cannot retroactively become PASS decisions. Any amendment
must create a new criteria version and digest, state the rationale and affected
evidence, and re-open any disposition that depends on the changed oracle.
Owner/operator preregistration is not independent acceptance.

## Public claims and evidence

Every claim must bind claim text, capability/action class, code commit, evidence
digest, verifier, independence level, test/protocol, assumptions and limitations.
Allowed statuses: SUPPORTED / TESTED_ONLY / ASPIRATIONAL / EXPLICITLY_NOT_CLAIMED.
A test success does not prove general correctness or efficacy.

## Threat, reachability and reviewer assumptions

Identify authorization/evidence assets, issuer/request/execution boundaries,
source-aware adversaries, key compromise, replay/concurrency, service outage,
potential artifact recipients and excluded deployment environments. An exclusion
is valid only with an evidence-backed removal, hard disablement or execution-path
unreachability test. Independently adjudicate reviewer conflicts, not just
non-authorship; P0/critical defects may not be self-approved.

## Open release classification candidates (not decisions)

- #1399 / draft PR #1414: possible P0 public artifact producer; resolve guard or
  prove the producer unreachable before release.
- #758 / draft #1416: trust lifecycle **design only**, not live issuer admission.
- #756, #757, #770: replay/revocation/provider capabilities do not exist merely
  because contract tests pass. Either bound them into release obligations or
  prove dependent v1 capabilities excluded and unreachable.
- #929: independent scientific AOSS review remains separate from bounded
  engineering-release review; no automatic scientific promotion.

## Epistemic non-goals and state

SemVer 1.0.0 defines a public API, not validated scientific superiority, global
security, universal agent correctness, certification or high assurance.
Until independently accepted evidence and release authorization:
`GATE_0_ORACLES=FROZEN_V1`; `GATE_0_SCOPE_BINDING=BLOCKED`; `GATE_0_ACCEPTANCE=NOT_INDEPENDENTLY_CONFIRMED`; `G1..G7=BLOCKED`;
`DGAF_V1_RELEASE=HOLD`; `SCIENTIFIC_N_INCREMENT=0`;
`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`;
`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`;
`HIGH_ASSURANCE=NOT_AUTHORIZED`.
