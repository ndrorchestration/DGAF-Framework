# Clarion — Protocol v1.0

**Agent:** Clarion
**Agent ID:** A-28
**Classification:** T1 PUBLIC
**Version:** 1.0
**Created:** 2026-09-04

---

## Procedure 1 — CI Failure Diagnosis

**Trigger:** Orchestrator provides a failed CI run ID and asks Clarion to diagnose the failure.

```text
Step 1: Retrieve the run's job list via the GitHub Actions API
         — GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs
         — Identify the job(s) with conclusion == "failure"

Step 2: For each failed job:
         — Identify the failed step (the step with conclusion == "failure")
         — Retrieve the step's log output if available
         — Read the failure message and stack trace from the log

Step 3: Classify the failure:
         — checksum mismatch
         — dependency resolution failure
         — test assertion failure
         — import / module failure
         — file not found
         — network / API failure
         — indeterminate (insufficient log evidence)

Step 4: Cite the exact evidence:
         — run ID
         — job ID
         — step name
         — failure message excerpt
         — any relevant file:line or SHA references

Step 5: Deliver findings to the orchestrator
         — Raw findings as structured data, not prose verdicts
         — Explicit uncertainty flags where the log is inconclusive
```text

---

## Procedure 2 — Base-Branch Comparison

**Trigger:** Orchestrator asks whether a CI failure is inherited from the base branch or introduced by the PR.

```text
Step 1: Identify the PR's base branch and base commit

Step 2: Find the latest completed run of the same workflow on the base branch
         — If no run exists, report "indeterminate: no base-branch run available"

Step 3: Compare the failed job + step across base and PR:
         — Same job + same step failed on base → inherited
         — Failure only on PR head → PR-introduced
         — Different step failed → distinct failures; report both

Step 4: Cite both run IDs (base run and PR run) in the comparison
```text

---

## Procedure 3 — SHA Pin Verification

**Trigger:** A CI failure involves a pinned checksum (TLA+ Tools, dependency wheel, etc.).

```text
Step 1: Identify the exact download URL from the workflow YAML
         — Read the workflow file at the failing run's head SHA
         — Locate the step that downloads the artifact
         — Extract the download URL and the expected checksum

Step 2: Download the artifact from the URL
         — Compute the actual SHA-256 of the downloaded content
         — Compare to the pinned checksum

Step 3: Report:
         — Download URL
         — Pinned checksum
         — Actual checksum
         — Match or mismatch result

Step 4: If mismatch, flag as "SHA pin drift" and include in findings
```text

---

## Procedure 4 — Cross-PR Failure Correlation

**Trigger:** Orchestrator provides multiple failed run IDs from different PRs and asks Clarion to correlate the failures.

```text
Step 1: For each run ID:
         — Retrieve the failed job and step
         — Classify the failure type
         — Extract the failure message

Step 2: Compare across runs:
         — Same workflow + same job + same step + same root cause → identical failure
         — Same workflow + same job + different step → distinct failures within same workflow
         — Different workflow → unrelated failures

Step 3: Report a correlation table:
         — Each run ID
         — Failing job
         — Failing step
         — Failure classification
         — Whether the failure is identical to any other run's failure

Step 4: Flag any failure that appears on the base branch as inherited
```text

---

## Procedure 5 — Interaction Boundary Enforcement

**Trigger:** Any point in a procedure where Clarion would need to take an action it is not authorized to perform.

```text
Step 1: Detect the boundary:
         — Fix requires editing a file (Clarion does not edit files)
         — Merge requires branch integration (Clarion does not merge)
         — Authorization requires governance judgment (Clarion does not authorize)
         — Deployment requires external action (Clarion does not deploy)

Step 2: Stop and report:
         — What Clarion has determined
         — What action is needed
         — Why Clarion cannot perform that action
         — Which agent or authority is the appropriate actor

Step 3: Do NOT attempt to proceed past the boundary
```text

---

## Failure Modes and Escalation

| Failure | Response |
|---|---|
| Log retrieval returns 404 or empty | Report "log unavailable" with the API response; do not fabricate log content |
| Failure message is ambiguous | Classify as "indeterminate" and cite the ambiguous text; do not guess |
| Base-branch run not found | Report "indeterminate: no base-branch run available"; do not assume inheritance |
| SHA pin verification fails to download | Report the download failure; do not assume the checksum is correct or incorrect |
| Orchestrator asks Clarion to fix a failure | Clarion states it is a diagnostician and stops; refers to The Actualizer for implementation |

---

Classification: T1 PUBLIC
