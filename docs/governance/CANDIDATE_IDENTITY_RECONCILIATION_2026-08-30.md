# Candidate Identity Reconciliation — 2026-08-30

**Status:** RECONCILED / PRE-FREEZE / NON-AUTHORIZING
**Purpose:** Resolve the apparent mismatch among `2a80f819…`, `303f4424…`, and the current `main` lineage before any P3–P9 closure.

## Finding

The apparent candidate conflict is not two incompatible mainline trees.

- `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` is the P8 checklist ancestor.
- `303f4424d2198f0d0cf76305c589263dd1e417dc` is a descendant of `2a80f819…` and contains the integrated DGAF v1 engineering/production control-plane work.
- Current `main` at the time of reconciliation was `255d76f6775caf40e758de4d41920f9ce40fda0c`, which is a descendant of `303f4424…`.
- Git comparison from `303f4424…` to `255d76f6…` reports 12 additional commits and only documentation/evidence-surface file changes; no executable apparatus files are changed in that interval.
- Therefore the statement that `303f4424…` is “not on main” is false for the current repository state: it is an ancestor of `main`.

## Role separation

| Identity | Role | Experimental authority |
|---|---|---|
| `2a80f819…` | P8 checklist ancestor | Historical lineage only |
| `303f4424…` | Integrated DGAF v1 engineering/production source; exact production runtime source for P2/P6a evidence | Verified engineering/runtime boundary; not a new experimental freeze |
| `ac8ea267…` | Prior experimental verification boundary | Historical/candidate-scoped provenance |
| `255d76f6…` | Mainline documentation/evidence tip at reconciliation time | Not independently verified as a new experimental candidate |
| **Future freeze candidate** | Explicit new immutable candidate after candidate designation | **Not yet designated** |

## P2/P6a evidence disposition

P2 run `33300481208` and P6a run `33302495240` remain valid exact evidence for the `303f4424…` production/runtime boundary. They are not rewritten as evidence for another SHA.

A future experimental candidate may inherit the underlying executable apparatus only after the candidate-binding procedure explicitly establishes equivalence and/or fresh exact-SHA runtime verification where required. No downstream predicate is to be closed by silently substituting `303f4424…`, `255d76f6…`, or `2a80f819…` for a newly designated freeze candidate.

## Decision rule

The next step is to create an explicit candidate identity from the current reconciled tree, without declaring it frozen. P3–P9 then bind to that exact candidate. The candidate remains PRE-FREEZE until all required evidence, independent verification, and freeze checks succeed.

This record does not authorize execution, create a freeze, or increase empirical N.

**Pilot authorization: NOT GRANTED. Empirical N = 0.**
