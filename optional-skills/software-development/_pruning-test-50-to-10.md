# Pruning Test — 50 → 10

## Evaluation criteria (applied to this session's frictions)

Each candidate scored 0–3 on:

- **friction-fit**: how directly it addresses a real friction from this session
- **epistemic-leverage**: would it have changed what could be honestly claimed this session
- **fail-closed posture**: does it refuse to assert when evidence is absent, or does it paper over gaps
- **durability**: does it produce a reusable artifact or only a one-time correction
- **deduplication**: does it overlap an already-authored skill or a stronger combination

Then ranked. Top 10 kept. The rest are folded into those 10 or discarded.

---

## Phase 1 — quick triage (friction-fit first)

### Tier 1 — directly addresses real frictions (strong candidates)

1. **run-id-cross-reference-checker** — this session cited run 33579935848; re-fetching it confirmed headSha, conclusion, event. A skill that does this for every cited run ID would have made the audit mechanically tighter.
2. **candidate-evidence-binding-map** (this is #21–#30 folded into one) — the core detection pattern: for a given SHA, which workflows actually ran, which artifacts exist, which gaps remain. This is the single most leveraged skill from this session.
3. **conclusion-mismatch-finder** — citation can say success; run object can say failure. This session avoided that by re-fetching; a dedicated check would harden it.
4. **no-transfer-violation-detector** — completion candidate vs remediation branch vs deploy branch vs main; this session's P9 scoped PASS is exactly the kind of thing that gets mislabeled without this check.
5. **event-type-classifier** — the audit correctly noted the Truth Layer run was push-triggered, not PR-triggered. A dedicated classifier makes that distinction explicit and reusable.
6. **artifact-availability-probe + artifact-digest-recompute-lite** — custody is part of evidence; this session's P9 artifact ID + ZIP digest + canonical digest is exactly the pattern. Combine into one custody-checker.
7. **standing-posture-reminder + no-efficacy-claim-filter + authorization-boundary-linter** — fold into one governance-hygiene skill; this session's posture discipline is the backbone.
8. **audit-claim-verification-loop** — the meta-skill that would have re-fetched every cited item in the audit summary and produced a verified/unverified split. This is the highest-leverage combination.

### Tier 2 — worth including but subsumed or narrow

9. **vercel-deployment-identity-verifier + vercel-vs-candidate-sha-binder + vercel-sso-boundary-annotator + deployment-runtime-vs-deployment-object-distinguisher** — fold into one deployment-binding-checker. The deployment-side work this session did is exactly this multi-layer check.
10. **gate-state-table-canonicalizer** — the audit already produced a gate-state table; this skill formalizes the canonical form rather than re-deriving prose.

### Tier 3 — fold into stronger skills or discard

- #3, #5, #9, #10 (SHA-binding-verifier, freshness-anchor-checker, artifact-deprecation-checker, dual-evidence-consistency-checker): fold into the binding-map or verification-loop; not strong enough alone.
- #4 (sha-binding-verifier), #6 (event-type-classifier as standalone), #8 (artifact-availability-probe standalone): subsumed.
- #11–#20 (governance hygiene cluster): fold into one hygiene skill; individual ones are too granular.
- #22–#30 (cross-candidate cluster): fold into the binding-map + no-transfer detector.
- #31–#40 (deployment cluster): fold into one deployment-binding-checker.
- #41–#50 (audit-procedure cluster): the verification-loop is the strongest; the rest are either too meta (#49 adversarial prompt generator — not this project's lane), too generic (#45 doc-refresh-checker), or too easy to over-engineer (#50 freshness-window — better as a column in the binding map).

## Phase 2 — the 10

| # | Skill | What it does | Why it survived |
|---|---|---|---|
| 1 | audit-claim-verification-loop | Re-fetch every cited run/artifact/SHA/branch in an audit summary; produce verified vs. unverified split | Highest leveraged; this session's verification moments are exactly this |
| 2 | candidate-evidence-binding-map | For a given SHA, enumerate workflows that ran against it, artifacts produced, gaps remaining | Core detection pattern; prevents "CI green on wrong thing" error |
| 3 | no-transfer-evidence-guard | Flag cross-candidate evidence use; require explicit historical-only labeling | Prevents the scoped-PASS-vs-broader-closure confusion |
| 4 | gate-state-canonicalizer | Produce canonical gate-state table (P2–P9, freeze, authorization, empirical N) with one-line evidence source per gate | Formalizes what the audit already does in prose |
| 5 | governance-hygiene-checker | Standing-posture restatement + no-efficacy-claim filter + authorization-boundary linter in one skill | Backbone discipline; one skill instead of three |
| 6 | deployment-binding-checker | For a Vercel deployment: object exists / target env / status / URL / git-source SHA / SSO-boundary / reuse-prohibition | Multi-layer distinction this session lived through |
| 7 | artifact-custody-checker | For a cited artifact: existence, size, name, SHA-256 recompute (when retrievable), digest match, retention caveat | Custody is real evidence; the P9 ZIP digest + canonical digest pattern is exactly this |
| 8 | run-event-classifier | Classify each cited run as push / workflow_dispatch / pull_request / workflow_run; flag where that matters | The push-vs-PR distinction was a real finding this session |
| 9 | conclusion-verifier | Fetch run conclusion/status and flag mismatch with claimed conclusion; fail closed on missing | Prevents "citation says success, run is failure" error class |
| 10 | audit-gap-decomposer | Take a high-level gap and decompose into smallest missing evidence pieces (which workflow, which run, which file, which artifact, which is in-env vs out-of-env) | This session's core move: "pre-freeze P-35 hasn't run on new code" → "which workflow, which run, which is missing" |

## Phase 3 — what got folded or cut

**Folded into #2 (binding-map):**
- #3 SHA-binding-verifier (becomes a column in the map)
- #5 freshness-anchor-checker (becomes a freshness column)
- #9 dual-evidence-consistency-checker (becomes a consistency check within the map)
- #10 artifact-deprecation-checker (becomes a retention caveat)
- #21–#30 cross-candidate cluster (the binding map is the substrate)
- #25 evidence-transfer-graph (becomes a derived view from the map)
- #26 branch-candidate-lifecycle-tracker (becomes part of the map)
- #27 same-branch-different-head-evidence-validator (becomes a head-vs-evidence check in the map)

**Folded into #7 (custody-checker):**
- #4 artifact-digest-recompute-lite
- #8 artifact-availability-probe
- #6 artifact-deprecation-checker (retention caveat)

**Folded into #6 (deployment-binding-checker):**
- #31 vercel-deployment-identity-verifier
- #32 vercel-vs-candidate-sha-binder
- #33 vercel-sso-boundary-annotator
- #34 deployment-runtime-probing-honest
- #35 deployment-reuse-prohibition-checker
- #36 vercel-env-bound-probe-canonicalizer
- #37 vercel-deployment-vs-branch-liveness-checker
- #38 vercel-deployment-handoff-record-template
- #39 deployment-runtime-vs-deployment-object-distinguisher
- #40 vercel-storage-availability-checker

**Folded into #5 (governance-hygiene-checker):**
- #11 standing-posture-reminder
- #12 authorization-boundary-linter
- #13 gate-state-table-canonicalizer (moved to #4 as the stronger form)
- #14 snapshot-vs-live-distinguisher
- #15 no-efficacy-claim-filter
- #16 inhibitor-flag-set
- #17 proof-state-per-gate-regenerator
- #18 authority-attribution-linter
- #19 irrevocable-op-gate-checker
- #20 ephemeral-vs-durable-evidence-classifier

**Folded into #1 or #8 or #9:**
- #1 SHA-binding-verifier → #1 verification loop
- #2 run-id-cross-reference-checker → #1 verification loop (this is basically the loop body)
- #7 conclusion-mismatch-finder → #9 conclusion-verifier
- #10 event-type-classifier → #8 run-event-classifier

**Folded into #10 (gap-decomposer):**
- #41 audit-claim-verification-loop is #1 (stronger form)
- #42 audit-finding-to-evidence-binder → part of the verification loop
- #43 audit-gap-decomposition → #10
- #46 audit-truth-source-ranker → part of the verification loop
- #47 audit-filling-guard → part of the loop's self-check
- #48 audit-recusal-checker → part of the loop's fail-closed posture

**Cut:**
- #44 audit-to-procedure-converter — better as the loop's output format, not a separate skill
- #45 audit-doc-refresh-checker — too specific; fold into the loop's doc-check
- #49 adversarial-audit-prompt-generator — not this project's lane; generates noise
- #50 audit-freshness-window-computation — better as a column in the binding map

## Phase 4 — remaining concern

The 10 are not 10 independent tools. Several are layers on the same substrate (binding-map + verification-loop + no-transfer-guard + gate-state-canonicalizer together form the audit spine). That's intentional — the project needs an audit spine, not 10 random procedures. The deployment-binding-checker and artifact-custody-checker are the two side-spines for the evidence types this project actually uses.

Next: write all 10 with verification criteria, then run each detection procedure on live repo state to confirm they fire correctly.
