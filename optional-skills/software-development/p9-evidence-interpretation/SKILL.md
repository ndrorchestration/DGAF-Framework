---
name: p9-evidence-interpretation
description: "Read P9 evidence honestly: scoped pass vs broader closure."
version: 0.1.0
author: Andrew Hensel (ndrororch. — placeholder)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [P9, evidence, verification, scope, no-transfer]
    related_skills: [dgaf-pdmal-orbit, verification-before-claim, exact-candidate-deploy-verify]
---

# P9 Evidence Interpretation

Read P9 independent-verification output without overclaiming. Distinguish scoped PASS from broader closure. Preserve the no-transfer boundary between candidates. Record the independence limitation honestly.

## When to Use

- A P9 independent-verification workflow has completed successfully.
- You need to decide whether the result supports P9 VERIFIED, scoped PASS, or broader closure OPEN.
- You need to confirm the exact candidate identity and artifact custody before promoting any gate.
- You need to record what the P9 run actually verified, including what it did not verify.

**Do NOT use to:**
- Promote P9 to full closure when only scoped verification executed.
- Transfer P9 evidence from one candidate to another.
- Relabel a scoped PASS as full P9 closure.

## Hard Invariants (do not weaken)

1. **Exact candidate identity first.** A P9 result is evidence only for the exact candidate SHA it ran against. If `HEAD != GITHUB_SHA` in the run, or if the run's head SHA does not match the controlled candidate, the result is NOT evidence for the controlled candidate.
2. **Scoped PASS ≠ broader closure.** Independent canonicalization of one artifact, one checkout identity check, and one authority regression is scoped verification. It does not by itself close broader P9 until the full evidence chain for the candidate is in place.
3. **No transfer between candidates.** Evidence established for candidate X is historical only for candidate Y. Each candidate must establish its own P9 evidence chain.
4. **Independence has a limit.** Breaking the canonicalization-method monoculture (e.g. `jq -S -c` + `sha256sum` independent of the Python path) is real, but the execution substrate (GitHub Actions, same repo, same account) remains shared. Record that limitation honestly.
5. **Artifact custody is part of the evidence.** A P9 result without a retained artifact and a verified digest is not durable evidence. Record artifact ID, ZIP digest, and the canonical digest.

## What a P9 Scoped PASS Verifies

A scoped PASS typically confirms:

- Exact `HEAD == GITHUB_SHA` for the run.
- Independent canonicalization path produces a deterministic digest.
- The independent digest matches the expected canonical digest for that artifact.
- Authority-identity regression tests pass (e.g. 4 passed).
- Artifact retained (artifact ID, ZIP digest).

A scoped PASS does NOT by itself verify:

- The broader P9 evidence chain for the candidate (other artifacts, other workflows, other candidates' evidence).
- Runtime behavior, deployment health, or gate P2/P6a.
- Anything about a different candidate.

## How to Read P9 Output

### Step 1 — Confirm the exact candidate SHA

Before interpreting the result, confirm the run's `headSha` matches the controlled candidate SHA. If it does not, the result is historical for a different candidate.

Sources:
- `gh run view <run-id> --json headSha,conclusion,status`
- Workflow run logs if the identity check is logged in-step.

### Step 2 — Confirm the conclusion and status

A P9 result is usable only if the run completed successfully. A failed or cancelled P9 run is not evidence for anything.

### Step 3 — Identify the artifacts

Identify the P9 evidence artifact(s): artifact ID, name, ZIP digest if available. Record:

```
run_id            = <workflow run id>
head_sha          = <exact SHA the run executed against>
artifact_id       = <dgaf-p9-independent-evidence or equivalent>
artifact_zip_digest = <sha256:...>
canonical_digest   = <the deterministic digest produced by the independent path>
```

### Step 4 — Confirm the independent canonicalization path

A real P9 result uses an independent path from the primary implementation. For this project that is `jq -S -c` plus `sha256sum`, separate from the Python-based canonicalization. Confirm:

- The independent path is actually different from the path under test.
- The digest produced by the independent path matches the expected canonical digest.

### Step 5 — Confirm the authority-identity regression

Confirm the authority-identity regression tests passed. For this project that is typically 4 passed tests. Record the count and the fact of passage, not just the word "PASS."

### Step 6 — Record the independence limitation

Record honestly that the execution substrate remains shared (GitHub Actions, same repo, same account). Breaking the canonicalization-method monoculture is a real improvement, but it is not full substrate independence. If the project later requires stronger independence, that is a separate step.

### Step 7 — Decide the closure state

Use these distinctions:

- **Scoped PASS:** the run verified exact identity, independent canonicalization, matching digest, and authority regression for the exact candidate SHA. Record as scoped PASS.
- **Broader closure OPEN:** the scoped PASS exists, but the full candidate P9 evidence chain (other artifacts, other workflows, other candidates' evidence) is not yet complete.
- **P9 VERIFIED:** only when the broader P9 evidence chain for the exact candidate is complete and reconciled. Do not promote from scoped PASS to VERIFIED solely because the scoped run passed.

### Step 8 — Preserve the no-transfer boundary

If the P9 result is for a candidate that is not the current controlled candidate, record it as historical evidence only. Do not promote it as evidence for the controlled candidate.

### Step 9 — Update the evidence record

Update the P9 reconciliation record and the P1–P9 matrix. For a scoped PASS, the correct entry is:

```
P9: SCOPED PASS / BROADER CLOSURE OPEN
```

Not:

```
P9: VERIFIED
```

unless the broader chain is complete.

## What This Skill Cannot Do

- It cannot promote P9 to VERIFIED. That requires the broader evidence chain and controller reconciliation.
- It cannot transfer evidence across candidates. That is prohibited by the no-transfer rule.
- It cannot create P9 evidence that does not exist. If the P9 run has not executed for the exact candidate, the result is OPEN, not PASS.

## Pitfalls

- **Relabeling scoped PASS as VERIFIED.** A single successful scoped run is not full P9 closure.
- **Transferring evidence across candidates.** Each candidate needs its own P9 evidence.
- **Ignoring the independence limit.** Claiming full independence when only the canonicalization method changed is overclaiming.
- **Skipping artifact custody.** A P9 result without a retained artifact and verified digest is not durable evidence.
- **Overclaiming from a failed run.** A failed P9 run is not evidence, positive or negative.

## Verification

- [ ] Run head SHA confirmed against controlled candidate SHA
- [ ] Run conclusion is success
- [ ] Artifact ID and digest recorded
- [ ] Independent canonicalization path confirmed different from primary path
- [ ] Authority-identity regression count recorded
- [ ] Independence limitation recorded honestly
- [ ] Closure state labeled correctly (scoped PASS vs broader closure vs VERIFIED)
- [ ] No-transfer boundary preserved if candidate differs

## Companion Skills

- `exact-candidate-deploy-verify` — produces the deployment identity P9 may later verify against.
- `dgaf-pdmal-orbit` — the standing governance boundary; P9 is one predicate in that framework.
- `verification-before-claim` — closed-loop verify discipline; apply before stating P9 status.

## Relationship to Existing Documentation

This skill encodes the interpretation procedure. The authoritative record is:

- `docs/governance/P9_LATEST_RECONCILIATION_2026-09-01.md` or the current P9 reconciliation record
- `docs/governance/P1_TO_P9_EVIDENCE_MATRIX.md`
- `docs/evidence/PDMAL_EVIDENCE_INDEX.md`

Do not let the skill output replace the documentation.
