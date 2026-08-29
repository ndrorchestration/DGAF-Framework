# DGAF/PDMAL Candidate Boundary Binding Record

**Record date:** 2026-08-28  
**Purpose:** Exact identity reconciliation for the current experimental verification candidate before P7/P8 closure.  
**Status:** PRE-FREEZE / BINDING PREPARATION ONLY  
**Experimental candidate:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`  
**Pilot authorization:** NOT GRANTED  
**Freeze:** NOT CREATED  
**Empirical N:** 0

## Current control-plane blocker

The pre-freeze TGL contract suite exposed a substantive regression associated with PR #132: 41 tests passed and 2 failed at the PDMAL → TGL → P-35 boundary. The failure is treated as a contract signal, not as transient test noise.

PR #132 remains **BLOCKED / DRAFT / UNMERGED**. PR #133 is the isolated remediation candidate. It is intended to restore the established TGL/P-35 contract and related fail-closed semantics; it does not authorize execution, create a freeze, or redefine the experimental apparatus.

The current experimental verification boundary remains `ac8ea267…` until a separately governed candidate identity is created and affected predicates are re-verified after any substantive apparatus change.

## Exact candidate identity

The candidate was resolved directly from the Git tree at `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. This record is an identity/binding aid; it is **not** a freeze manifest and does not authorize execution.

## Candidate component fingerprints

The previously recorded candidate component fingerprints remain historical evidence for this binding record. They must be re-derived from the exact final candidate before freeze rather than assumed to remain valid after substantive changes.

## Binding discrepancies requiring resolution

### 1. Protocol applicability metadata is stale
The candidate copy of `PDMAL_EXPERIMENT_PROTOCOL.md` has an older `applies_to_sha`. The current experimental verification boundary is `ac8ea267…`. This remains a P7/P8 binding defect and must be corrected in a new candidate-bound revision before final freeze.

### 2. Candidate manifest is historical
`CANDIDATE_MANIFEST_2026-08-21.json` records older candidate identities. It remains provenance and must not be rewritten into a false current history. A new candidate-bound manifest must supersede it for freeze preparation.

### 3. Historical P8 identities remain historical
Historical P8 material naming superseded candidates remains provenance. Current planning records must use the active verification boundary or explicitly label historical scope.

### 4. TGL remediation boundary
TGL/P-35 contract repair is a prerequisite to candidate verification, not an authorization transition. Any resulting executable change to the experimental apparatus requires a new candidate identity and affected-predicate re-verification rather than silently inheriting `ac8ea267…` evidence.

## P7/P8 implication

P7/P8 cannot be declared closed until the protocol applicability, analysis configuration identity, runner/schema identity, TGL control-plane contract, freeze manifest, and remaining predicate evidence are cryptographically bound to one final immutable candidate.

## Evidence-surface rule

This record is an **internal governance** artifact. It must not be copied verbatim into the public-facing project surface. Public-facing documentation may state scoped implementation/verification facts but must not expose internal custody/credential mechanics or imply experimental efficacy.

## Non-authorizing conclusion

This record documents identity reconciliation and the current TGL blocker. It does not create a freeze, grant authorization, produce empirical observations, or increase empirical N.
