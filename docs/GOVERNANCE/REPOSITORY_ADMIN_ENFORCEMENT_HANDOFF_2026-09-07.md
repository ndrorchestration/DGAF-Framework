# Repository Administrator Enforcement Handoff — Issue #277

> **Status:** READY FOR REPOSITORY-ADMIN ACTION / PREVENTIVE ENFORCEMENT NOT ESTABLISHED  
> **Prepared against checkpoint:** `d01fa13d40b60a1e0bd661756fd60e8550107d9d`  
> **Scientific effect:** NONE

## Current readable enforcement

At preparation time:

- protected `main` requires only status context `PPTL CI`;
- enforcement level is `non_admins`;
- active branch ruleset ID `16909314` targets the default branch and contains deletion + non-fast-forward protection;
- no required-pull-request rule is established by the readable ruleset;
- no unintended bypass actor has been identified in the readable ruleset;
- Main Push Provenance Audit has repeatedly detected non-PR writes after they reached `main`, proving the compensating control is detective rather than preventive.

This handoff intentionally does **not** include ready-to-import ruleset JSON. Rule IDs, workflow identities, and repository settings can drift; copying stale JSON would be less safe than applying the semantic requirements below and reading them back.

## Required semantic outcome

A repository administrator should configure protected `main` so that:

1. ordinary changes require a pull request or an equivalent control with the same effective semantics;
2. no unintended actor can bypass the protected-main policy;
3. merge-critical checks cannot be skipped merely because a change is documentation-only;
4. the required set remains small, stable, explicit, and maintainable rather than mechanically requiring every advisory workflow;
5. direct ordinary contents writes to protected `main` are rejected by policy rather than merely detected afterward.

## Recommended merge-critical control set

The administrator should deliberately choose the exact repository contexts/workflows that implement these semantic categories:

- `PPTL CI`;
- governance/control-state consistency and HEAD binding;
- truth/evidence/claim integrity;
- Python quality for executable-code changes, through a required workflow design that cannot disappear on a path filter;
- PDMAL pre-freeze/pre-authorization safety for governed experiment changes;
- Mode-T security/lifecycle checks when Mode-T-governed surfaces change.

If a required status can be absent because of path filters, do not require that raw context directly. Prefer a stable always-reported aggregate or a ruleset `required_workflows` design whose behavior has been tested for documentation and code changes.

## Administrator action checklist

- [ ] Confirm current default branch and existing protection/rulesets.
- [ ] Add/enable required pull-request semantics for `main`.
- [ ] Select exact merge-critical required workflows/statuses.
- [ ] Confirm no accidental bypass actors.
- [ ] Preserve deletion and non-fast-forward protections.
- [ ] Save configuration.

## Mandatory post-change proof

Do not close #277 from a screenshot or configuration claim alone. Record evidence for all of the following:

1. fresh branch-protection/ruleset readback showing required-PR semantics;
2. exact required contexts/workflows in the saved configuration;
3. bypass-actor readback;
4. a controlled PR whose required check fails and whose merge is actually blocked;
5. a normal green PR whose merge succeeds;
6. a controlled attempt at an ordinary direct contents write to protected `main` that is rejected, if practical and safe;
7. Main Push Provenance Audit remains useful as a detective backstop but is no longer the primary control.

## Acceptance outcome

Issue #277 may move from OPEN only after preventive behavior is independently observable from repository configuration and negative/positive controls. This handoff, CI, or a planned configuration does not itself establish enforcement.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0 remains controlling.**
