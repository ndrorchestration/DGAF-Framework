# Candidate Identity Reconciliation — 2026-08-30

**Status:** RECONCILED / PRE-FREEZE / NON-AUTHORIZING
**Purpose:** Resolve the apparent mismatch among `2a80f819…`, `303f4424…`, and the `main` lineage, then record the explicit designation of the next pre-freeze candidate without promoting it to a freeze.

## Finding

The apparent candidate conflict is not two incompatible mainline trees.

- `2a80f8193f4222658c01b1bfe8a94e3ecae8af9f` is the P8 checklist ancestor.
- `303f4424d2198f0d0cf76305c589263dd1e417dc` is a descendant of `2a80f819…` and contains the integrated DGAF v1 engineering/production control-plane work.
- `255d76f6775caf40e758de4d41920f9ce40fda0c` was the `main` tip at the time of the original reconciliation and is a descendant of `303f4424…`.
- Git comparison from `303f4424…` to `255d76f6…` reported 12 additional commits and documentation/evidence-surface changes only; no executable apparatus files were changed in that interval.
- Therefore the earlier statement that `303f4424…` was “not on main” was incorrect: it is an ancestor of the reconciled mainline.

## Role separation

| Identity | Role | Experimental authority |
|---|---|---|
| `2a80f819…` | P8 checklist ancestor | Historical lineage only |
| `303f4424…` | Integrated DGAF v1 engineering/production source; exact production runtime source for prior P2/P6a evidence | Verified engineering/runtime boundary; not itself a new freeze |
| `ac8ea267…` | Prior experimental verification boundary | Historical/candidate-scoped provenance |
| `255d76f6…` | Mainline documentation/evidence tip at original reconciliation time | Documentation lineage only; not independently treated as an experimental freeze |
| `c6157158bf0ee4840e99a381a4b99bd2febe2302` | **Current designated pre-freeze candidate** on `experimental-candidate/2026-08-30-reconciled` | **Designated for fresh verification; NOT FROZEN** |

## Candidate designation disposition

The next evidence cycle has been explicitly designated to candidate `c6157158bf0ee4840e99a381a4b99bd2febe2302`.

Its candidate ref is `experimental-candidate/2026-08-30-reconciled`.

Its exact Vercel production deployment is `dpl_8iYrzqsf729RSZRXj698pa4ptbWZ`, whose recorded Git source SHA is an exact match to `c6157158…` and whose deployment state is `READY`.

This designation establishes the target for candidate-scoped verification. It does **not** create a freeze, grant authorization, or transfer historical P2/P6a evidence from `303f4424…`.

## P2/P6a evidence disposition

P2 run `33300481208` and P6a run `33302495240` remain valid exact evidence for the `303f4424…` production/runtime boundary. They are retained as historical candidate-scoped evidence and are not rewritten as evidence for `c6157158…`.

Fresh exact-candidate P2 and P6a execution is required for `c6157158…` before those predicates may be treated as current-candidate verified.

## Downstream binding rule

P3–P9 must bind to `c6157158…` or to a later explicitly designated candidate if a substantive apparatus change occurs. No gate may be closed by silently substituting `303f4424…`, `255d76f6…`, `2a80f819…`, or `ac8ea267…` for the current designated candidate.

If a substantive protocol, runner, analysis, artifact, security/custody, retention, or executable control change occurs, the candidate cycle must be re-identified and affected predicates re-verified.

## Non-authorizing conclusion

The identity discrepancy is reconciled and the next pre-freeze candidate is explicitly designated. The repository remains PRE-FREEZE / FAIL-CLOSED until candidate-scoped evidence, P8 closure, independent P9 verification, and a new immutable freeze are completed.

**Current designated candidate:** `c6157158…`
**Freeze:** NOT CREATED
**Pilot authorization:** NOT GRANTED
**Empirical N:** 0
