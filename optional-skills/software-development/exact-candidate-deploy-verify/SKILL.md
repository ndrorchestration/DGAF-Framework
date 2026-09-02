---
name: exact-candidate-deploy-verify
description: "Deploy exact candidate to Vercel; record P2/P6a inputs."
version: 0.1.0
author: Andrew Hensel (ndrorchestration), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [exact-candidate, vercel, deployment, P2, P6a, evidence]
    related_skills: [dgaf-pdmal-orbit, candidate-lock-verification, verification-before-claim]
---

# Exact-Candidate Deploy & Verify

Deploy a DGAF exact-candidate branch to a Vercel preview deployment and record the resulting identity (deployment ID, URL, branch, candidate SHA) so P2 and P6a can be dispatched against the right object.

**What it does:** creates the missing physical object for candidate-bound runtime evidence. **What it does not do:** verify runtime behavior, trigger P2/P6a, or claim runtime verification. Runtime verification happens in the gate workflows, not here.

## When to Use

- The current controlled candidate has a pinned deploy branch (e.g. `deploy/exact-candidate-a43219b`).
- No Vercel deployment exists yet for that candidate SHA.
- P2/P6a need an exact deployment ID + URL as inputs.
- You need a clean record of what was deployed and from what SHA.

**Do NOT use for:**
- Deploying `main` or any branch not pinned to the exact controlled candidate SHA.
- Claiming runtime verification from the deploy step alone.
- Bypassing SHA verification before P2/P6a dispatch.

## Prerequisites

- Vercel CLI authenticated (device-flow or token). This session used interactive device flow; a stored `VERCEL_TOKEN` would also work but is not present in this environment.
- Local checkout of the exact deploy branch, or ability to fetch + checkout the remote deploy branch.
- The deploy branch pinned to the exact candidate SHA (verify before deploying — see Procedure step 1).
- `vercel.json` present at repo root (this project has one).

## Hard Invariants (do not weaken)

1. **SHA is the identity.** The controlled candidate is identified by its full 40-char SHA, not by branch name. The deploy branch is a convenience pointer; the SHA is the authority.
2. **Deploy from the exact branch, not main.** Deploying main or any non-pinned branch risks creating a mainline deployment that cannot satisfy exact-candidate binding.
3. **Verify before claiming.** A deployment that is `● Ready` is a deployment object, not runtime verification. The SSO/auth boundary on preview deployments is an authentication property, not a runtime failure — record it honestly.
4. **P2/P6a inputs are separate.** This skill produces the deployment identity; the gate workflows consume it. Do not skip the dispatch step.

## How to Run

### Step 1 — Verify the deploy branch pins the exact candidate SHA

Before anything else, confirm the remote deploy branch points to the exact controlled candidate SHA.

```
git ls-remote --heads origin deploy/exact-candidate-a43219b
```

Expected: a single line with the exact candidate SHA followed by `refs/heads/deploy/exact-candidate-a43219b`. If the SHA does not match the controlled candidate, stop — do not deploy.

Also confirm the controlled completion branch points to the same SHA (consistency check, not authority):

```
git ls-remote --heads origin completion/2026-09-01-exact-candidate
```

### Step 2 — Checkout the exact deploy branch locally

Fetch and checkout the deploy branch so the local HEAD is the exact candidate SHA. This is what the Vercel CLI will build from.

```
git fetch origin deploy/exact-candidate-a43219b:deploy/exact-candidate-a43219b
git checkout deploy/exact-candidate-a43219b
git rev-parse HEAD
```

Expected local HEAD: the exact candidate SHA (e.g. `a43219b4ed91fff8615f6c655ab3d17ca871fc29`).

### Step 3 — Authenticate Vercel CLI

If no `VERCEL_TOKEN` is set, the CLI will prompt a device-flow auth. Complete it in the browser. Do not proceed without auth.

```
vercel whoami
```

Expected: a Vercel user identity, not "No existing credentials found."

### Step 4 — Deploy from the exact checkout

Use the project name and scope that match the target Vercel project. For this project the target is `dynamicgovernanceagenticformation` under scope `ndrorchestration`.

```
vercel deploy --project dynamicgovernanceagenticformation --scope ndrorchestration --yes --no-wait --format json
```

Do NOT use `--prod` unless the gate procedure explicitly requires a production deployment. For P2/P6a candidate-bound evidence, a preview deployment is the correct object.

### Step 5 — Record the deployment identity

Capture from the deploy JSON output:

- `deployment.id` — e.g. `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17`
- `deployment.url` — e.g. `https://dynamicgovernanceagenticformation-lhp3s3sv5-ndrorchestration.vercel.app`
- `deployment.target` — e.g. `preview`

Record these alongside:

- `candidate_sha` — the exact controlled candidate SHA
- `branch` — the deploy branch name
- `deployment_state` — `READY` (or whatever the inspect step returns)

### Step 6 — Wait for Ready state

A deployment may return `INITIALIZING`. Poll until `readyState` is `READY` before recording it as usable.

```
vercel inspect <deployment-url> --scope ndrorchestration --format json
```

Check `deployment.readyState == "READY"` and `deployment.status == "● Ready"`. Do not record an INITIALIZING deployment as complete.

### Step 7 — Honest verification of what was deployed

The Vercel CLI inspect shows the deployment object. Confirm:

- id matches the recorded deployment ID
- url matches the recorded URL
- target is the intended environment (preview or production)
- status is Ready

**Do not claim runtime verification from this step.** The deployment being Ready means the build succeeded and the object exists. Runtime behavior is verified by the gate workflows (P2, P6a) that consume the deployment identity.

### Step 8 — Record the SSO/auth boundary honestly

If health-probe endpoints return `302 → Vercel SSO` instead of a clean response, record that as an **authentication boundary**, not a runtime failure. Do not relabel authentication wrapping as "deployment unhealthy."

If runtime health verification is required for the evidence chain, the gate workflows or an authenticated probe path must be used — not the unauthenticated curl from this skill.

### Step 9 — Produce the handoff record

The output of this skill is a handoff record for P2/P6a. Format:

```
candidate_sha        = <exact candidate SHA>
deployment_id        = <dpl_...>
base_url             = <deployment URL>
branch               = <deploy branch name>
deployment_state    = READY
deployment_target   = preview (or production if that was the intent)
deployed_at_utc      = <timestamp>
deployer             = <who/what triggered the deploy>
sso_boundary         = <true if preview deployment wraps endpoints in Vercel SSO; record honestly>
```

Write this to a file in the repo (e.g. `docs/evidence/exact-candidate-deployment-<candidate-sha>.md` or the existing evidence index) so the next step has the exact inputs without relying on chat history.

## P2/P6a Dispatch Inputs

Once this skill completes, the P2 and P6a workflow_dispatch forms should be filled with:

- `candidate_sha` = exact candidate SHA
- `deployment_id` = the dpl_... ID
- `base_url` = the deployment URL
- P6a additionally needs `expected_allowed_origin` = the origin served by that deployment

**Do not reuse an existing mainline deployment.** The existing production deployment (`dpl_AFndnDtWjovVQ7jhBXczcbtSU3AM`, SHA `aa9dc883…`) is a mainline deployment and cannot satisfy exact-candidate binding for `a43219b…`.

## What This Skill Cannot Do

- It cannot trigger GitHub workflow_dispatch. If the environment lacks workflow_dispatch write access, the handoff record stays on disk and the dispatch must be done through whatever surface has that capability.
- It cannot read Vercel REST API `gitSource` directly without a `VERCEL_TOKEN`. The CLI inspect path is the available verification.
- It cannot authenticate to the deployment's runtime endpoints if they are wrapped in Vercel SSO. That is an auth-property of the deployment environment, not a defect in the deploy step.

## Pitfalls

- **Deploying from the wrong branch.** Always checkout and verify the exact deploy branch before `vercel deploy`. The CLI builds from the local checkout, not from a remote ref you didn't fetch.
- **Skipping the Ready wait.** Recording an INITIALIZING deployment as usable will cause P2/P6a to dispatch against a deployment that is not yet built.
- **Overclaiming runtime verification.** `● Ready` is a deployment object state. Runtime verification is a separate gate.
- **Reusing the production deployment.** The production deployment is mainline; candidate-bound evidence requires the exact-candidate deployment.
- **Silent auth failures.** If the deployment endpoints are SSO-wrapped, record that honestly. Don't retry curl until it "works" — it won't, because the redirect is intentional.

## Verification

- [ ] Remote deploy branch pins exact candidate SHA (ls-remote confirmed)
- [ ] Local HEAD after checkout == exact candidate SHA
- [ ] Vercel CLI authenticated (whoami returned identity)
- [ ] Deploy output recorded: deployment ID, URL, target
- [ ] Deployment state confirmed Ready via inspect
- [ ] Handoff record written to disk with all P2/P6a inputs
- [ ] SSO/auth boundary recorded honestly (if applicable)
- [ ] No claim of runtime verification made from the deploy step alone

## Companion Skills

- `dgaf-pdmal-orbit` — the standing governance boundary and ORBIT-N1 state machine; this skill executes one transition within that framework.
- `candidate-lock-verification` — verify the locked apparatus candidate SHA and examine P-gates.
- `verification-before-claim` — the closed-loop verify discipline; apply before stating anything this skill produced is "verified."

## Relationship to Existing Documentation

This skill encodes the procedure; the authoritative record is the documentation. After running, update:

- `docs/evidence/PDMAL_EVIDENCE_INDEX.md` or the current evidence index
- `docs/governance/CURRENT_CANDIDATE_EVIDENCE_READINESS_2026-09-01.md` or the current-candidate readiness record
- `docs/governance/P1_TO_P9_EVIDENCE_MATRIX.md` — once the deployment is confirmed and P2/P6a dispatched

Do not let the skill output replace the documentation. The skill is the procedure; the docs are the record.
