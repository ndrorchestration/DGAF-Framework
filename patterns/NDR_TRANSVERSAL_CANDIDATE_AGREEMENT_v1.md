# NDR Transversal Candidate Agreement Pattern v1

**Namespace:** NDR runtime-governance pattern
**Class:** ADVISORY governance-control pattern; blocking when used as a prerequisite for evidence closure
**Status:** REGISTERED — 2026-09-02
**Related:** P-35 Procluding Premise Gate; P-36 Gate Priority Schema; P-42 Adaptive Harmonic Governance

## Intent

Maintain agreement among independent control-plane projections of a candidate so that a valid state in one system cannot be mistaken for a valid state in another.

## Required identity tuple

`apparatus/source SHA + candidate SHA/tree + deployment identity/source SHA + workflow/evidence run + artifact identity + protocol/analysis binding + freeze identity + authorization state`

## Pattern

`discover → classify identity roles → compare projections → quarantine historical references → resolve contradictions → retain exact provenance → permit downstream closure only after agreement`

## Cross-system projections

- GitHub source, candidate manifest, control state, workflow runs, and artifacts
- Vercel deployment source SHA, target/state, and runtime evidence when deployment is applicable
- Notion operational control state
- taxonomy/vocabulary registries
- pattern registries and cross-reference indexes
- public/current documentation

## Non-substitution

The following do not establish candidate equivalence:

- shared ancestry;
- same repository;
- same branch name;
- same workflow name;
- same deployment URL/domain;
- behavioral similarity;
- prior PASS on another SHA.

## Failure classes

`BENIGN HISTORICAL DIFFERENCE` → preserve and label.

`ROLE DIFFERENCE` → preserve distinct identities and their scopes.

`UNRESOLVED TRANSVERSAL DRIFT` → block promotion until reconciled.

`BLOCKING CONTRADICTION` → fail closed; do not transfer evidence.

## P-35 boundary note

Where P-35 enforcement requires an explicit premise checker, the checker is an upstream dependency of the DGAF/TGL/ConsensusTask boundary. The pattern does not define a PDMAL-specific premise policy. An approved experimental-control checker is required separately before pilot execution.

## Evidence semantics

`DEFINED`, `IMPLEMENTED`, `TESTED`, `CANDIDATE-BOUND`, `VERIFIED`, `FROZEN`, `AUTHORIZED`, and `EMPIRICAL` are distinct states.

A successful transversal check does not itself authorize execution or create empirical evidence.

## Audit test

A current candidate is not promotion-eligible when any live projection names a different candidate, deployment, or evidence boundary without an explicit historical/role qualification.

**Default posture:** fail closed.
