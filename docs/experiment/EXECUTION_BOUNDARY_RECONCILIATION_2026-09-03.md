# Execution Boundary Reconciliation — 2026-09-03

**Status:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / EMPIRICAL N=0

## Purpose

This record distinguishes the verified executable candidate from later documentation/control-plane commits. It does not transfer any deployment-bound evidence across Git SHAs.

## Identity

- **Immutable P-35 validation boundary:** `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`
- **Verified executable candidate:** `48c12c6660df7decb61f9aac4d8560526a8754eb`
- **Candidate branch:** `candidate/p35-validated-control-state-2026-09-02`
- **Verified Vercel deployment:** `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- **Verified deployment SHA:** `48c12c6660df7decb61f9aac4d8560526a8754eb`
- **Verified deployment state:** `READY`
- **Verified deployment alias:** `dynamicgovernanceagenticformation-git-c-cab2e6-ndrorchestration.vercel.app`
- **Later PR #200 documentation/control-plane head:** `fc45d95e5cdae4026e4e50e2746d48e1cc3b7389`

The later `fc45d95e...` commit must not be treated as a deployment-bound runtime candidate merely because it is the latest PR head. Its own dispatch handoff preserves the `48c12c...` candidate/deployment pair.

## Runtime verification boundary

The existing Vercel deployment is independently identified as a Git deployment of `48c12c...`. Direct unauthenticated access reaches Vercel's SSO protection boundary; that confirms reachability/protection only and is not P2/P6a runtime evidence.

P2/P6a closure still requires successful candidate-bound workflow execution, including the required Vercel automation bypass secret and preservation of the resulting provenance artifacts.

## Required dispatch inputs

### P2

- `candidate_sha=48c12c6660df7decb61f9aac4d8560526a8754eb`
- `deployment_id=dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- `base_url=https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`

### P6a

- `candidate_sha=48c12c6660df7decb61f9aac4d8560526a8754eb`
- `deployment_id=dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- `base_url=https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`
- `allowed_origin=https://dynamicgovernanceagenticformation-7avhglp61-ndrorchestration.vercel.app`

## Evidence rules

Historical P2/P6a artifacts do not transfer across candidate, deployment, or triggering-workflow identity. The exact deployment identity is established, but runtime closure remains pending until the workflow run itself is bound to the same candidate/deployment pair.

No freeze, authorization, pilot execution, unblinding, or empirical N is established by this document.
