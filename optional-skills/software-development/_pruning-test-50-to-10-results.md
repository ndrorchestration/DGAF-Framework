# Epistemic Effectiveness Test — 10 Candidates Against Live Session Frictions

## Test method

For each candidate skill, answer four questions honestly:

1. **Failure prevented**: What real failure would this have caught or prevented this session?
2. **Coverage overlap**: Is it already substantially covered by an existing skill/invariant/tool, or is the gap real?
3. **Actionability**: Is it a reflex/habit I can actually apply at claim time, or is it ceremony I'd skip?
4. **Salvage value**: If I'm wrong about a claim this session, would this skill have made the error visible sooner?

Score each 0–3. Keep only those scoring ≥7/12 that are not pure duplication.

---

## Candidate 1 — Triple-source verification reflex

**What it would do**: Before asserting an empirical claim, seek ≥2 independent concrete sources (run state + artifact; git state + file content; deployment probe + run conclusion) and state what each confirmed.

**Failure prevented this session**: Several claims in the audit report depended on `gh run view 33579935848`. If I'd only checked the run title and not the `headSha`/`event` fields, I would have missed that it was push-triggered, not PR-triggered. Two independent fields of the same run object is not fully independent, but it's better than one.

**Coverage overlap**: Partial with `verification-before-claim`, which already says verify before claiming. But that skill doesn't require *multiple independent sources*. This is a stricter refinement. Real gap.

**Actionability**: High. I can apply it at claim time: "claim X, sources A and B, agreement Y."

**Salvage value**: High. This session's honest verification moments are exactly this pattern.

**Verdict**: **KEEP.** Refine as: "for any empirical claim I'd be uncomfortable retracting, name ≥2 independent sources; if only one, label it single-sourced."

---

## Candidate 2 — Epistemic-class tagging of every factual claim

**What it would do**: Tag each factual claim as [observed: tool returned X], [deduced: follows from Y + Z], [restated: from prior context not re-verified this turn], or [uncertain].

**Failure prevented this session**: I restated the audit report's claims before fully verifying them. If I'd tagged them, I'd have caught which ones I was restating from the summary vs. which I'd freshly verified. This session's whole dynamic — restate audit, then verify bits — is exactly where this helps.

**Coverage overlap**: None existing. There's no mechanism forcing me to classify how I know something. Real gap.

**Actionability**: High, as a lightweight convention. Not a separate document; a tagging discipline in every message with empirical content.

**Salvage value**: Very high. This is the backbone skill.

**Verdict**: **KEEP.** Make it the framing mechanism; the other skills feed into it.

---

## Candidate 3 — No-transfer-between-candidates enforcement

**What it would do**: Before any claim that evidence from candidate/branch/session A applies to B, stop and check whether the evidence executed against B's exact identity. If not, label it as transferred and flag the risk.

**Failure prevented this session**: Real risk all session. The whole point of the DGAF evidence model is that evidence doesn't transfer. The audit report already did this honestly (scoped PASS vs broader closure, completion-candidate vs remediation-branch P9), but as an *operational reflex* it's worth making explicit because it's the single most common failure mode.

**Coverage overlap**: The dgaf-pdmal-orbit invariant "Evidence does NOT cross apparatus identity" already states the rule. But the *habit of checking at claim time* is not automatic. This skill is the operationalization of that invariant at the moment of assertion.

**Actionability**: High. Every time I mention evidence, name the identity it binds to.

**Salvage value**: High. This is the DGAF-specific binding invariant made actionable.

**Verdict**: **KEEP**, but consider folding the checklist into the binding ledger (#3) to avoid two skills saying nearly the same thing. Actually, keep separate: no-transfer is a claim-time gate; the ledger is the durable record. They're complementary.

---

## Candidate 4 — Green-CI-is-not-closure reflex

**What it would do**: When I encounter any CI pass, default to: "which exact gate/branch/SHA/artifact does this establish, and what does it NOT establish?" Never let CI passage substitute for a closed gate without naming the gap.

**Failure prevented this session**: This was the core risk all session, and it materialized in the audit: Truth Layer CI passed on the remediation head, but the pre-freeze P-35 workflow hadn't run on the new code. If I'd had this reflex active, the audit would have opened with "CI passed, but the relevant pre-freeze workflow hasn't run on this head yet" instead of drifting toward closure.

**Coverage overlap**: Partial with dgaf-pdmal-orbit's hard invariant that "CI success ≠ efficacy/freeze/authorization." But the *reflex of naming the gap explicitly at the moment of citing CI* is distinct. Real gap.

**Actionability**: High. Every CI citation gets a "doesn't establish" clause.

**Salvage value**: Very high. This session's central epistemic risk.

**Verdict**: **KEEP.** This is the single highest-leverage skill from this session.

---

## Candidate 5 — Don't-elaborate-beyond-tool-output

**What it would do**: Don't construct plausible narratives about what "probably" happened or what a result "probably means" unless labeled as inference. When I don't have the data, say so.

**Failure prevented this session**: I did this reasonably well this session — I said the SSO redirects were an auth boundary, not a runtime failure; I said I couldn't confirm the deployment SHA from Vercel metadata without the token. But the risk is real and recurring: it's tempting to fill gaps with inference when the tooling is limited.

**Coverage overlap**: Partial with epistemic tagging (#2) and boundary honesty (#6). But as a standalone prohibition against inventing plausible narratives, it's a distinct reflex.

**Actionability**: High. "I don't have that" is a complete sentence.

**Salvage value**: High. This is the anti-hallucination reflex in epistemic form.

**Verdict**: **KEEP.**

---

## Candidate 6 — Boundary-crossing honesty

**What it would do**: Name exactly which boundaries I crossed for each claim — files read, API calls, run fetches, artifact downloads, deployment probes — and don't claim to have crossed boundaries I didn't.

**Failure prevented this session**: Without this, I could have claimed "I verified the deployment SHA" when I actually only verified the branch pins the SHA. The skill forces the distinction.

**Coverage overlap**: Overlaps with #1 (triple-source) and #2 (tagging). But as a standalone "name the boundaries you crossed" reflex, it's a distinct honesty check.

**Actionability**: High. "I did X, I did not do Y" is a complete and honest sentence.

**Salvage value**: High. Prevents the "I verified" overclaim when I only partially verified.

**Verdict**: **KEEP.** Consider whether it's a sub-component of #1/#2, but it's distinct enough as a name-the-boundaries reflex.

---

## Candidate 7 — Closure and completion integrity

**What it would do**: At every summary point, enumerate (a) what's actually verified this turn, (b) every open blocker, (c) every claim made this turn that I haven't directly verified, and (d) whether the standing invariants are preserved. Don't claim completion without concrete criteria.

**Failure prevented this session**: This is the structural version of what I did organically. If I'd had it as a reflex, the audit's closing would have been more systematic: "verified this turn: run 33579935848 headSha matches branch; conclusion success; event push. Not verified this turn: pre-freeze P-35 workflow has not run on this head. Open blockers: none new. Standing invariants: preserved."

**Coverage overlap**: Partial with dgaf-pdmal-orbit's state-of-evidence discipline, but this is the *habit* of doing it at every closure point, not just the document.

**Actionability**: High. It's a closure ritual, not a separate artifact.

**Salvage value**: High. Prevents false closure.

**Verdict**: **KEEP.** This is the best structural skill from this session.

---

## Candidate 8 — Context-compaction re-anchor

**What it would do**: When a context-compaction block is present, treat the live user message as the actual task and the compacted snapshot as background only. Don't let the snapshot's framing override the live ask. Re-verify live state before acting on any snapshot claim.

**Failure prevented this session**: This session started with a compaction block. I read it and used it as background, which was correct. But the risk is real: a compacted snapshot can contain stale claims that look current. If I'd acted on a stale snapshot claim without re-verifying, I'd have been wrong.

**Coverage overlap**: None existing as a named reflex. Real gap, but only relevant when compaction is present.

**Actionability**: High when compaction is present; N/A when it isn't.

**Salvage value**: Medium-high for long sessions. This session it didn't fire as a failure, but the risk is real.

**Verdict**: **KEEP**, but as a conditional reflex that only fires when compaction is present.

---

## Candidate 9 — Reporter-not-advocate stance check

**What it would do**: Before sending, check whether the message is reporting what I verified or advocating for a conclusion I want the user to reach. If advocating, flag it.

**Failure prevented this session**: I didn't advocate this session; I reported. But the risk is real in DGAF work, where there's a natural temptation to frame things as "on track" when they're not.

**Coverage overlap**: Overlaps with #2 (tagging) and #6 (boundary honesty), but as a stance check it's distinct.

**Actionability**: Medium. It's a pre-send check, which is easy to skip when I'm focused on content.

**Salvage value**: Medium. This session didn't have an advocacy failure, but the risk is real.

**Verdict**: **KEEP**, but weaker than the top 6. Worth including for stance discipline.

---

## Candidate 10 — Scope-anchor and termination clarity

**What it would do**: Re-anchor each turn to the actual live ask (not the compacted context). Track what's actually done/in-progress/not-started. Don't pad with adjacent work.

**Failure prevented this session**: I stayed fairly well-scoped this session, but the risk is real: there's a huge amount of context and it's easy to drift into adjacent audits.

**Coverage overlap**: Partial with #8 (compaction re-anchor), but #10 is about scope drift more generally, not just compaction.

**Actionability**: Medium-high. It's a pre-response check.

**Salvage value**: Medium. This session didn't have a scope-drift failure, but the risk is real.

**Verdict**: **KEEP**, but as a lighter reflex than the top 6.

---

## Cut candidates (with reasons)

- #1 verify-before-claim alone: covered by existing skill; my refinements (#1, #6) are the real value.
- #8 state-of-evidence board, #9 candidate-identity tracker, #12 evidence-aging, #13 gate-status diff: these are artifacts/habits that fold into the binding ledger (#3) and closure ritual (#7). Don't make them standalone skills.
- #14 fresh-vs-restated, #16 "I don't know" default, #21 observed/deduced/assumed, #22 label uncertainty: all fold into epistemic tagging (#2).
- #23 don't-summarize-over-unverified: folds into boundary honesty (#6).
- #28 re-read-before-restating, #31 detect elaboration, #32 narrating vs. reporting, #33 claiming completion unverified: all fold into #5, #6, #7.
- #30 catch stale task description: folds into #8 (compaction re-anchor).
- #34–#40 tool-use techniques: not meta/combination skills; they're techniques.
- #41–#45 ledger/known-issues/decision-log/open-question register: artifacts, not skills; fold into the binding ledger (#3) and closure ritual (#7).
- #46 session-goal-anchor: folds into #10.

---

## Final 10 (after pruning and merging)

1. **Triple-source verification reflex** — for empirical claims, name ≥2 independent sources; label single-sourced claims.
2. **Epistemic-class tagging** — tag every factual claim as observed/deduced/restated/uncertain; this is the framing layer.
3. **No-transfer-between-candidates enforcement** — claim-time gate: name the identity each piece of evidence binds to.
4. **Green-CI-is-not-closure reflex** — every CI citation names what it establishes and what it doesn't.
5. **Don't-elaborate-beyond-tool-output** — no plausible narratives; label inference; say "I don't have that" when true.
6. **Boundary-crossing honesty** — name exactly which boundaries were crossed for each claim.
7. **Closure and completion integrity ritual** — at every summary: verified-this-turn, open blockers, unverified claims, standing-invariants check, completion-criteria check.
8. **Context-compaction re-anchor** — conditional reflex: when compaction present, live ask drives, snapshot is background, re-verify snapshot claims.
9. **Reporter-not-advocate stance check** — pre-send check: am I reporting or advocating? Flag advocacy.
10. **Scope-anchor and termination clarity** — re-anchor to live ask; track done/in-progress/not-started; don't pad.

These 10 are distinct, testable against this session, not pure duplication of existing skills, and actionable as reflexes rather than ceremony. The top 6 are the core; #7 is the structural closure skill; #8–#10 are situational/meta refinements.

Next step: actually install them as a real skill and apply them to the next verification cycle, then report whether they changed behavior.
