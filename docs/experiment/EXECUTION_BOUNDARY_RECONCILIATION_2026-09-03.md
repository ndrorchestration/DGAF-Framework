# Execution Boundary Reconciliation — 2026-09-03

**Status:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / EMPIRICAL N=0

## Purpose

This record resolves the apparent candidate/deployment contradiction without transferring evidence across Git SHAs.

## Identity layers

### Immutable validation boundary

- P-35 validated boundary: `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`

### Execution candidate

- Candidate SHA with independently verified deployment identity: `48c12c6660df7decb61f9aac4d8560526a8754eb`
- Candidate branch: `candidate/p35-validated-control-state-2026-09-02`
- Vercel deployment: `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- Deployment SHA reported by Vercel: `48c12c6660df7decb61f9aac4d8560526a8754eb`
- Deployment state: `READY`
- Deployment alias: `dynamicgovernanceagenticformation-git-c-cab2e6-ndrorchestration.vercel.app`

### Documentation/control-plane successor commit

- Later PR #200 head: `fc45d95e5cdae4026e4e50e2746d48e1cc3b7389`
- This commit is a documentation/control-plane reconciliation commit. It does **not** by itself establish a new executable candidate or a new deployment identity.
- Its dispatch handoff intentionally preserves the existing `48c12c...` candidate/deployment pair.

## Evidence rule

The candidate/deployment pair `48c12c...` / `dpl_CW4...` is the strongest currently verified deployment identity. The later `fc45d95e...` commit must not be substituted for the executable candidate solely because it is the latest PR head.

Conversely, runtime evidence generated against `48c12c...` may only be promoted to closure when the workflow run itself is candidate-bound to `48c12c...`, its exact deployment, and its required authenticated inputs.

## Runtime state

- Existing deployment is live and READY.
- Direct unauthenticated access reaches the Vercel protection boundary and returns an SSO redirect; this confirms reachability/protection only and is not P2/P6a runtime evidence.
- Existing historical P2/P6a artifacts remain non-closing unless their triggering workflow identity independently binds to the same exact execution candidate and deployment.

## Required execution

1. Dispatch `.github/workflows/p2-runtime-verification.yml` with:
   - `candidate_sha=48c12c6660df7decb61f9aac4d8560526a8754eb`
   - `deployment_id=dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
   - `base_url=https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
2. Dispatch `.github/workflows/p6a-cors-verification.yml` with the same candidate/deployment plus the configured allowed origin.
3. Preserve the emitted provenance artifacts and verify their workflow/run identity.
4. Continue only with the downstream operational closures after fresh P2/P6a evidence is accepted.

## Guardrails

Do not create freeze, authorization, pilot mode, unblinding, or empirical N as part of this reconciliation. Do not transfer runtime evidence from `92ff830b...`, `48c12c...` historical runs with mismatched workflow identity, or any earlier candidate unless the complete provenance contract independently passes.
