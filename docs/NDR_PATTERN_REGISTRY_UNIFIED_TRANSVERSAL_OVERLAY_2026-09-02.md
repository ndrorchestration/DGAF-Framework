# NDR Pattern Registry Unified — Transversal Overlay — 2026-09-02

**Purpose:** Current cross-registry synchronization layer for dependency and transversal-agreement semantics.
**Status:** CANONICAL OVERLAY / NON-DESTRUCTIVE
**Source registries:** `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` and `docs/ndr_patterns_unified.json`
**Pattern entry:** `patterns/NDR_TRANSVERSAL_CANDIDATE_AGREEMENT_v1.md`

## Active registry identity

The underlying NDR registry is a historical/canonical source for the NDR pattern family. The machine-readable registry separately records the P-42 AHG identity. This overlay resolves the *current synchronization semantics* without rewriting historical registry records.

### Namespace invariants

- `P-35` = **Procluding Premise Gate**.
- `P-42` = **Adaptive Harmonic Governance (AHG)**.
- P-35 and P-42 are distinct identifiers and mechanisms.
- A registry watermark does not itself establish implementation, verification, authorization, or empirical efficacy.

## Transversal pattern definition

**NDR-TRANSVERSAL-CANDIDATE-AGREEMENT**

A governance consistency pattern requiring independent current-state projections to resolve to one scoped candidate identity before downstream evidence is promoted.

**Class:** ADVISORY as a governance pattern; BLOCKING when its agreement predicate is explicitly required by a downstream closure control.

## Required identity tuple

`apparatus/source SHA + candidate SHA/tree + deployment identity/source SHA + workflow/evidence run + artifact identity + protocol/analysis binding + freeze identity + authorization state`

## Dependency classes

`UPSTREAM_IDENTITY`
→ exact source/candidate/deployment identities.

`EXECUTION_DEPENDENCY`
→ runtime, artifact, custody, reproducibility, security.

`GOVERNANCE_DEPENDENCY`
→ P7, P8, independent P9, freeze, authorization.

`CROSS_SYSTEM_DEPENDENCY`
→ GitHub, Vercel, Notion, evidence, taxonomy, pattern registries.

`HISTORICAL_REFERENCE`
→ retained prior state; non-closing unless explicitly revalidated.

## Agreement classes

`ROLE DIFFERENCE` — intentional semantic role separation.

`HISTORICAL DIFFERENCE` — prior scoped identity retained for provenance.

`TRANSVERSAL DRIFT` — conflicting live projections without intentional role distinction.

`BLOCKING CONTRADICTION` — discrepancy capable of invalid evidence transfer or governance transition.

## Current P-35 remediation relationship

The verified engineering remediation requires an explicit `premise_check_fn` at the DGAF/TGL/ConsensusTask boundary. The dependency is therefore part of the execution/wiring contract for P-35 enforcement.

This registry overlay does **not** define a PDMAL constitutional premise policy. A PDMAL-specific premise checker remains an independently approved scientific-control prerequisite to pilot execution.

## Current candidate boundary

For PR #192 candidate `edd3b5c8266e2680b9bb94301c2623a3f1ac0cf0`:

- broad exact-head CI coverage is present;
- Pre-Authorization Security passed;
- Pre-Freeze Runner Validation is blocked by four legacy tests that omit the explicit P-35 checker now required by the implementation;
- Governance CI is blocked by a TLA+ Tools release SHA mismatch and requires independent release verification;
- no exact-candidate Vercel deployment is currently evidenced;
- freeze and authorization remain absent.

These are candidate-cycle control facts, not pattern-efficacy claims.

## Non-transfer rule

No pattern registry entry, taxonomy entry, workflow pass, deployment, or evidence artifact may transfer verification status across candidate identities merely because the mechanism or terminology appears equivalent.

**Default:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.
