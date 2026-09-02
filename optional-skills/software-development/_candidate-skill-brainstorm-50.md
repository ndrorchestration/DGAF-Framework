# 50 Candidate Meta/Combination/Hybrid Skills — Raw Brainstorm

Context: DGAF-Framework project (ndrorchestration). Standing posture PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. Current work: completion-cycle evidence closure (P2–P9), remediation branch P-35, Vercel deployment for exact candidate a43219b4… . Already-authored skills in optional-skills/software-development/.

Each candidate below is a skill idea. Categories: truth-anchoring (what is actually verified vs. claimed), governance-hygiene (standing-posture discipline), cross-candidate-evidence (no-transfer + binding map), deployment-evidence (Vercel side), audit-procedure (how to run a good audit), reproduction/repeatability (next-cycle reuse), and self-critique (detect own drift).

---

## A. Truth-anchoring (what is actually verified vs. claimed)

1. verification-status-table-extractor: read a doc section and produce a table: each claim, its evidence sourcing (CI run id, artifact id, SHA, or none), and a one-word status flag (VERIFIED / OPEN / CLAIM-ONLY / STALE).
2. run-id-cross-reference-checker: given a set of claim statements, locate the actual workflow runs that mention those run IDs / artifact IDs and confirm they exist and match the stated conclusion.
3. sha-binding-verifier: for each claim mentioning a SHA, pull the branch/ref/when and confirm the SHA actually exists and is reachable (not just pasted).
4. artifact-digest-recompute-lite: given an artifact ID known to be JSON/text, recompute its SHA-256 and compare with a stated digest without downloading a ZIP (preferred path when available).
5. conclusion-mismatch-finder: for each run ID cited as evidence, fetch run conclusion and status and flag mismatches (claimed success but run is failure/cancelled; claimed failure but run is success).
6. event-type-classifier: classify each run as push / workflow_dispatch / pull_request / workflow_run and flag where a claim treats a push-triggered run as if it were a PR-gated or dispatch-gated execution.
7. freshness-anchor-checker: check whether the cited evidence is newer or older than the claim's stated cutoff; flag stale evidence used for a current-state claim.
8. artifact-availability-probe: for a cited artifact ID, check whether it is downloadable at all (exists, size, name) before asserting custody.
9. artifact-deprecation-checker: check artifact retention window vs. current date; flag artifacts that may be past retention if retention-days is known.
10. dual-evidence-consistency-checker: when two sources are cited for one claim, check whether they actually agree (run id, conclusion, SHA) or silently contradict.

## B. Governance-hygiene (standing-posture discipline)

11. standing-posture-reminder: at top of any evidence/closure discussion, restate PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0 and list what would actually move each, then check whether the current discussion invades those gates.
12. authorization-boundary-linter: scan text for any language that implies authorization, freeze, pilot approval, or efficacy; tag each occurrence as OK / overclaim / candidate for retraction.
13. gate-state-table-canonicalizer: given a gate list (P2–P9, freeze, authorization, empirical N) in prose, produce a canonical table with explicit state per gate and a one-line "from what evidence" column.
14. snapshot-vs-live-distinguisher: distinguish historical snapshot documents from live control-plane documents in a doc list; flag any live claim that relies on a snapshot as if it were current.
15. no-efficacy-claim-filter: flag any sentence that asserts DGAF efficacy, validation, demonstration of effectiveness, or N>0 without explicit explicit authorization + empirical evidence.
16. inhibitor-flag-set: given a closure state, enumerate the inhibitors still present (per gate) and refuse to closes those gates in any summary.
17. proof-state-per-gate-regenerator: for each gate, regenerate the proof state from first principles (not from chat memory) and compare to the asserted state.
18. authority-attribution-linter: flag sentences attributing authority to an agent or tool that does not hold it (e.g., completion controller self-authorizing).
19. irrevocable-op-gate-checker: before any irreversible-op language (merge, pilot, freeze), require explicit operator go-ahead evidence; flag absence.
20. ephemeral-vs-durable-evidence-classifier: classify each cited piece of evidence as ephemeral (CI log, one-time run) vs. durable (artifact with digest + custody) and flag when a durable-sounding claim rests on ephemeral evidence.

## C. Cross-candidate-evidence (no-transfer + binding map)

21. candidate-bindings-index-builder: build an index of (SHA → branch → workflow runs → artifacts) from gh api, one row per SHA, used as the substrate for no-transfer checks.
22. no-transfer-violation-detector: given a claim about candidate X that cites evidence from candidate Y, flag it; require explicit "historical only" label.
23. evidence-scoped-labeling-assistant: when a P9 or other evidence result is scoped (e.g., scoped PASS vs broader closure), help label it correctly rather than overpromoting.
24. candidate-identity-triple-checker: for any candidate discussion, restate the three identities (apparatus SHA, designation commit SHA, freeze commit SHA if any) and confirm not conflated.
25. evidence-transfer-graph: draw (in text) the transfer edges implied by the current evidence discussion and flag any cross-candidate edge.
26. branch-candidate-lifecycle-tracker: track branch head SHA changes over time and flag where a verification result predates a head change on the same branch, so it may be stale for the new head.
27. same-branch-different-head-evidence-validator: when the same branch has multiple heads over time, check whether cited evidence is for the current head or a prior head.
28. run-ownership-attribution-checker: for a run cited as "the verification for X", confirm the run's head branch / head SHA actually points to X.
29. cross-branch-evidence-reader: read the evidence for each branch involved in the current state (completion, remediation, deploy, main) and produce one line per branch of what is actually established there.
30. workflow-run-subset-classifier: classify which subset of available workflows is relevant to a given candidate state and which are noise for that candidate.

## D. Deployment-evidence (Vercel side)

31. vercel-deployment-identity-verifier: for a Vercel deployment ID, confirm object exists, target env, status, URL, and (if retrievable) git source SHA; produce a binding table vs. candidate SHA.
32. vercel-vs-candidate-sha-binder: given a deployment and a candidate SHA, check whether deployment was built from that SHA via Vercel metadata or deploy-branch pin; flag mismatch.
33. vercel-sso-boundary-annotator: for a Vercel preview/production deployment, probe endpoints and annotate which are SSO-wrapped vs. reachable; do not relabel auth as runtime failure.
34. deployment-runtime-probing-honest: for a deployment URL, attempt a small set of health probes and record actual responses honestly, including redirects/SSO, without overclaiming.
35. deployment-reuse-prohibition-checker: flag any attempt to reuse an existing mainline deployment as exact-candidate evidence; enforce deploy-from-exact-branch rule.
36. vercel-env-bound-probe-canonicalizer: pick the right probe path for candidate-bound evidence depending on deployment env (preview vs production) and auth properties.
37. vercel-deployment-vs-branch-liveness-checker: check whether a deployment's associated branch is still the exact candidate branch or has moved; flag drift.
38. vercel-deployment-handoff-record-template: generate the handoff record template for P2/P6a with exact fields.
39. deployment-runtime-vs-deployment-object-distinguisher: separate "deployment object Ready" from "runtime behavior verified" in any summary.
40. vercel-storage-availability-checker: check whether Vercel API token or CLI auth is available in the current environment before attempting deployment/API ops; fail closed if not.

## E. Audit-procedure (how to run a good audit)

41. audit-claim-verification-loop: for an audit summary, re-fetch each cited run/artifact/SHA/branch, confirm, and produce a revised summary with verified vs. unverified sections.
42. audit-finding-to-evidence-binder: for each audit finding, attach the exact evidence anchor (run id / artifact id / SHA / file path) or mark as no-evidence.
43. audit-gap-decomposition: take a high-level gap ("P-35 not verified") and decompose into the smallest missing evidence pieces (which workflow, which run, which file, which artifact).
44. audit-to-procedure-converter: take an audit finding and convert it into the concrete steps that would close it, including what is in-environment vs. out-of-environment.
45. audit-doc-refresh-checker: check whether the cited documentation files actually exist at the stated commit shas and are reachable.
46. audit-truth-source-ranker: for each claim, rank available sources by trustworthiness (live repo/git > CI run artifact > PR prose > chat memory) and flag low-source claims.
47. audit-filling-guard: during an audit, flag when the assistant fills gaps with plausible inference rather than retrieved evidence.
48. audit-recusal-checker: detect when the assistant is asked to assert something outside its verified reach and recommend the honest "not verifiable from here" posture.
49. adversarial-audit-prompt-generator: generate adversarial questions for a claim set (what would disprove it, what alternative explanation fits, what boundary would break it).
50. audit-freshness-window-computation: compute, for each cited run, the time delta from now and from the claim's stated context; flag evidence older than a sensible freshness window.

---

End of raw brainstorm. Next phase: test each for epistemic effectiveness against this session's actual frictions, then prune to 10.
