---
name: audit-epistemic-discipline
description: "Apply 10 meta/verification reflexes to every DGAF audit/claim before asserting anything."
version: 0.1.0
author: Andrew Hensel (ndrorchestration), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [epistemic, audit, verification, DGAF, closure, no-transfer, green-is-not-closure]
    related_skills: [dgaf-pdmal-orbit, verification-before-claim, candidate-lock-verification]
---

# Audit Epistemic Discipline — 10 Meta-Verification Reflexes

A meta/hybrid skill that bundles 10 tested reflexes for honest DGAF audit work. Each reflex is a detection signature plus a concrete check. Apply them in sequence before finalizing any audit claim, evidence summary, or closure statement.

These are not standalone ceremonies. They are reflexes that fire when their detection signature appears. When a reflex is not triggered, skip it — do not force it into every message.

## When to Use

- Before asserting any empirical claim about a DGAF candidate, workflow run, artifact, deployment, or gate state.
- Before summarizing an audit, reporting verification, or closing a task.
- When a context-compaction block is present and you are about to act on its claims.
- When you feel the urge to "fill in" a gap with plausible inference.
- When CI green is in front of you and you feel closure pressure.

**Do NOT use to:**
- Override the standing DGAF governance boundary (`PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`).
- Add ceremony to simple, low-stakes statements.
- Replace `dgaf-pdmal-orbit` — this skill is the operational habit layer inside that boundary.

## Standing Boundary

This skill does not grant authority, close gates, authorize freeze/pilot, or claim efficacy. It is a verification-discipline skill. The standing posture remains authoritative.

---

## Reflex 1 — Triple-Source Verification

**Detection signature**: You are about to assert an empirical claim that you would be uncomfortable retracting.

**What to do**: Before asserting, name at least two independent concrete sources. If only one source is available, label the claim single-sourced and flag it as weaker.

**Independent sources are not**: two fields from the same run object, two views of the same artifact, two paraphrases of the same source. Independent means different retrieval paths that could disagree.

**What to avoid**: citing one run object and calling it "verified" without a second source that could have disagreed.

**Test this session**: the claim "run 33579935848 is success" — first source is the run object conclusion; second source is the headSha/event fields that disambiguate whether it's a PR-gated or push-triggered run. Both are from the same API call, which is weaker than two truly independent paths, so the honest label is "single-sourced from the run object, corroborated by its own metadata fields."

---

## Reflex 2 — Epistemic-Class Tagging

**Detection signature**: You are making a factual statement whose basis you could misremember later.

**What to do**: Tag the statement's epistemic class in your own drafting:
- `observed:` — tool returned this directly this turn.
- `deduced:` — follows from observed plus a stated inference.
- `restated:` — from prior context, not re-verified this turn.
- `uncertain:` — you do not actually know and are not asserting.

When you tag, also tag the source for observed/deduced.

**What to avoid**: letting "restated" claims silently become "observed" claims by the time they reach the user.

**Test this session**: every claim in the audit summary should carry a tag. If you cannot tag it, you are either deducing without stating it, or asserting from memory — both are flags.

---

## Reflex 3 — No-Transfer-Between-Candidates Gate

**Detection signature**: You are about to say evidence from candidate/branch/session A applies to candidate/branch/session B.

**What to do**: Stop. Name the exact identity each piece of evidence binds to (SHA, branch, run ID, artifact ID). If the evidence did not execute against the target identity, label it historical-only and flag the transfer risk. Do not silently relabel.

**What to avoid**: "P9 passed" without naming which candidate's P9. "CI passed" without naming which branch's CI. "Deployment verified" without naming which SHA the deployment was built from.

**Test this session**: the audit report separates the completion candidate's scoped PASS from any remediation-branch P9 result. That separation is the reflex in action. If any sentence in the audit blurs them, flag it.

---

## Reflex 4 — Green-CI-Is-Not-Closure

**Detection signature**: You see a CI pass and feel closure pressure.

**What to do**: Name, explicitly, what the CI run establishes and what it does not establish. Then name the gap. Prefer: "CI passed for X, which does not establish Y, and the Y-relevant workflow has not run on X yet."

**What to avoid**: letting "green" become a closure sentence.

**Test this session**: "Truth Layer Tests passed on the remediation head" is a green-CI finding. The reflex forces the gap clause: "which does not establish that the PDMAL Pre-Freeze Runner workflow has run on this head." That gap clause is the actual finding.

---

## Reflex 5 — Standing-Posture Inventory

**Detection signature**: You are starting a DGAF verification task, or you are about to make a closure/advancement/state-change claim.

**What to do**: State the standing posture before anything else:
- PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0
- What would actually move each
- Whether the current task is compatible with that posture

Then check whether any assertion in the task invades those gates.

**What to avoid**: letting a verification task silently become a closure claim.

**Test this session**: the audit's first move should be the posture inventory. If the audit does not open with it, flag the audit.

---

## Reflex 6 — Authorization-Boundary Check

**Detection signature**: You are about to mention authorization, freeze, pilot, efficacy, or demonstration of effectiveness.

**What to do**: Check: was explicit authorization actually granted for this? If not, flag the claim as unverified and do not promote it. This is a hard gate, not a soft preference.

**What to avoid**: any language that implies authorization without authorization. "Ready to freeze" is a claim of readiness, not authorization — but if it reads as anticipatory authorization, flag it.

**Test this session**: any sentence in the audit that could read as "we are getting close to freeze/pilot" must be checked against this reflex. If the sentence implies progress toward authorization without stating the explicit gap, rename it.

---

## Reflex 7 — Event-Type Disambiguation

**Detection signature**: A workflow run is cited as evidence for a candidate or gate.

**What to do**: Name the event type: push / workflow_dispatch / pull_request / workflow_run. Then name what that means for the evidence: did the run actually evaluate the candidate under the intended trigger condition?

**What to avoid**: treating push-triggered runs as if they were PR-gated runs, or PR-triggered runs as if they were dispatch-triggered.

**Test this session**: run 33579935848 is push-triggered. The reflex forces the clarification: "this was a push-triggered run, not a PR-gated execution." That clarification is itself a finding.

---

## Reflex 8 — Deployment-Binding Check

**Detection signature**: A Vercel deployment is cited as evidence.

**What to do**: Separate four layers and name what is established at each:
1. Object exists and is Ready.
2. Built from which commit SHA (via branch pin or Vercel metadata if retrievable).
3. Endpoints reachable without SSO/auth wrapping.
4. Runtime behavior actually verified.

If any layer is missing, name it as pending rather than folding it into the previous layer.

**What to avoid**: conflating "deployment Ready" with "runtime verified," or "branch pins SHA" with "deployment was built from SHA."

**Test this session**: the deployment record should separate object-Ready from built-from-SHA from endpoint-reachable from runtime-verified. If the record collapses them, flag it.

---

## Reflex 9 — Claim-Scope Anchor

**Detection signature**: You are about to make a claim whose scope could drift.

**What to do**: Anchor the claim's scope before stating it: what candidate, what branch, what run, what time window, what evidence identity. If the scope is not nameable, the claim is not yet ready.

**What to avoid**: scope drift — citing evidence that binds to one scope while the sentence is about another scope.

**Test this session**: each audit sentence should be anchorable. If you cannot anchor a sentence to a candidate/branch/run/time/evidence, flag it as scope-ungrounded.

---

## Reflex 10 — Retraction-Readiness Check

**Detection signature**: You are about to finalize a claim or send a summary.

**What to do**: Ask: if I were wrong about this, would I retract it cleanly? If the answer is no — because the claim is vague, built on inference, entangled with other claims, or resting on a single source you cannot re-fetch — flag it before sending.

**What to avoid**: sending claims that are hard to retract because they are hedged, interpretive, or built on memory.

**Test this session**: for each claim in the audit summary, run the retraction test. Claims that fail go back for sharpening or downgrade.

---

## How the 10 Compose

These are not independent tools. They compose as a spine:

1. Standing-posture inventory sets the frame.
2. Claim-scope anchor names what you're talking about.
3. No-transfer gate checks identity.
4. Triple-source verification checks evidence.
5. Event-type disambiguation checks the trigger condition.
6. Green-CI-is-not-closure checks the CI temptation.
7. Deployment-binding check checks the deployment layer.
8. Authorization-boundary check checks the authority layer.
9. Epistemic-class tagging names how you know each claim.
10. Retraction-readiness check is the pre-send gate.

Apply them in that order when their detection signatures fire. When a reflex does not fire, skip it. When several fire, apply all of them.

## How to Test This Skill

To test whether this skill is working, apply it to a real state and check for false negatives:

1. Pick a stale or incomplete claim.
2. Run all 10 reflexes.
3. Check whether any reflex failed to flag the problem.
4. If a reflex missed it, the skill needs a detection-signature refinement, not a ceremony addition.

## Pitfalls

- **Ceremony overload**: applying all 10 to every sentence is not the point. Apply the reflexes whose detection signatures fire.
- **Tagging without checking**: epistemic-class tagging is not a substitute for verification; it is a label on whether you actually verified.
- **No-transfer as blocking only**: no-transfer is also a labeling skill — historical-only evidence is fine if labeled, bad if relabeled.
- **Green-is-not-closure as pessimism**: it is not pessimism; it is precision about what green means.
- **Deployment-binding as one claim**: it is four layers; collapsing them is the error mode.

## Verification

- [ ] Each reflex has a detection signature and a concrete check.
- [ ] The 10 compose as a spine, not as 10 ceremonies.
- [ ] The skill does not overlap dgaf-pdmal-orbit's standing-boundary content; it operationalizes it.
- [ ] The skill names what to avoid for each reflex.
- [ ] The skill includes a live test procedure.

## Companion Skills

- `dgaf-pdmal-orbit` — the standing governance boundary this skill operates inside.
- `verification-before-claim` — the existing verification habit this skill refines and hardens.
- `candidate-lock-verification` — the exact-identity discipline this skill enforces at claim time.
- `exact-candidate-deploy-verify` — the deployment-binding subprocedure this skill references.

## Relationship to Existing Documentation

This skill encodes the verification reflexes; the authoritative record of what was verified remains the documentation (`docs/governance/...`, `docs/evidence/...`). The skill is the habit layer; the docs are the record.
