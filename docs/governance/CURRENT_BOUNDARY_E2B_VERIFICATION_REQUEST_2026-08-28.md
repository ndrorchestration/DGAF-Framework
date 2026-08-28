# Current-Boundary E2b Verification Request — 2026-08-28

**Purpose:** Trigger the normal push-path Governance CI/E2b verifier against the post-PR-#121 `main` tree without changing the PDMAL experimental apparatus.

## Scope

This is a governance/provenance marker only. It does not alter the PDMAL runner, analysis implementation, artifact schema, protocol, candidate apparatus, freeze state, authorization state, or empirical data.

## Predecessor boundary

- Experimental candidate remains: `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`
- PR #121 exact verification head: `7475fda1aa39edabb19653b2302b8bba42badead`
- PR #121 merge commit: `ba5a2fdfa2d137cbddae20aa84f7d31d0097f960`

## Verification objective

Use the push-triggered Governance CI path to produce current-tree E2b evidence against the exact commit created by this marker. The resulting evidence must remain scoped to that exact executed tree and must not be retroactively transferred to the experimental candidate.

## Acceptance boundary

A successful E2b run establishes verifier-toolchain/provenance properties for the exact executed tree only. It does not close P8, create a freeze, grant authorization, or establish empirical efficacy.

**Pilot authorization:** NOT GRANTED  
**Empirical N:** 0  
**Freeze:** NOT CREATED
