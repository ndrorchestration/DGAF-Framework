# Execution Boundary Reconciliation — 2026-09-03

**Status:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / EMPIRICAL N=0

## Purpose

This record is the current documentation authority for the execution boundary. It distinguishes the verified executable candidate from later documentation/control-plane commits and records runtime observations without promoting non-provenance-bound observations to gate closure.

## Identity

- **Immutable P-35 validation boundary:** `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`
- **Verified executable candidate:** `48c12c6660df7decb61f9aac4d8560526a8754eb`
- **Candidate branch:** `candidate/p35-validated-control-state-2026-09-02`
- **Verified Vercel deployment:** `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`
- **Verified deployment SHA:** `48c12c6660df7decb61f9aac4d8560526a8754eb`
- **Verified deployment state:** `READY`
- **Verified deployment alias:** `dynamicgovernanceagenticformation-git-c-cab2e6-ndrorchestration.vercel.app`
- **Later PR #200 documentation/control-plane head:** `fc45d95e5cdae4026e4e50e2746d48e1cc3b7389`

The later `fc45d95e...` commit is not promoted to a deployment-bound runtime candidate merely because it is the latest PR head. Its own dispatch handoff preserves the `48c12c...` execution candidate/deployment pair.

## Runtime verification boundary

The Vercel deployment is independently identified as a Git deployment of `48c12c...`. Direct unauthenticated access reaches the Vercel SSO protection boundary. This establishes reachability/protection only and is not P2/P6a workflow evidence.

A live observation on the verified deployment exercised the four P6a request classes and matched the P6a workflow predicates: allowed-origin POST returned `503` with the expected allow-origin header; disallowed-origin POST returned `503` without the allow-origin header; allowed-origin preflight returned `204` with required method/header allowances; disallowed-origin preflight returned `403` without the allow-origin header. This is a runtime observation for the exact deployment, but it does not close P6a because the preserved workflow artifact must itself be produced by the exact-candidate workflow execution.

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

Historical P2/P6a artifacts do not transfer across candidate, deployment, or triggering-workflow identity. The exact deployment identity is established, but closing evidence still requires the designated workflow run to execute against that exact candidate/deployment pair and preserve its artifact.

Runtime observations, deployment health, CI success, dry runs, and documentation reconciliation are non-closing unless the governing predicate explicitly identifies them as sufficient evidence.

The protected Vercel automation bypass secret is required by both runtime workflows and is never recorded in documentation.

No freeze, authorization, pilot execution, unblinding, or empirical N is established by this document.

## Current closure sequence

`P2 + P6a exact workflow execution → operational P3/P4/P5/P6 closure → exact P7 binding → P8 → independent P9 → immutable freeze → explicit authorization → blinded pilot`
