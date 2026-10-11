# SDD ledger — plan: docs/superpowers/plans/2026-10-11-containment-admission.md

Ruling: continue native execution without intermediate approval questions — user's explicit continuous-execution instruction overrides skill checkpoints — cost if wrong: candidate scope may require revision before merge.
Ruling: materialize a selected immutable source snapshot and use GitHub tree API for candidate admission — git mirror clone lacks credentials — cost if wrong: local full-repository checks remain unavailable; hosted checks must establish admission readiness.
Ruling: implement exact-byte integrity binding, with source authenticity NOT_ESTABLISHED — production trust-anchor provisioning is unresolved and existing SBCF prototypes are unmerged — cost if wrong: live producer admission remains blocked.
Pre-flight: assessment produces a non-authorizing record; intake adds digest binding without changing disposition. Projection consumes those exact records and PEP refusal; browser consumes only static generated records. Synthetic claims remain fixed-time replay.
Task 1 port: 26 unittest tests PASS using unchanged immutable source modules. New intake tests pending.

Task 1 complete: bound intake RED (missing module) → GREEN; 31 tests PASS.
Task 2 generator complete: RED (missing module) → GREEN; 36 tests PASS; SC-28 consumes the actual SC-01 assessment, records refusal and zero callbacks.
Task 2 parser: RED (missing module) → GREEN; four Node tests PASS for case coverage, authority ceiling, semantic consistency and receipt linkage. Browser validation pending.

The direct public GitHub transport succeeded after the mirror failed; full checkout at the exact baseline is available. A sibling git worktree on codex/containment-assessment-20261011 now isolates the candidate. The earlier local-source limitation is resolved. Baseline Python and UI checks started before transfer. Browser runtime download returned a truncated non-ZIP response; DOM evidence will be used, with the missing browser check retained.

Task 2 complete: 36 new/ported containment tests plus existing PEP and surface tests: 50 PASS, 82 subtests. Node suite: 121 PASS (117 existing, 4 new). TypeScript noEmit: PASS after explicit readonly tuple typing. Changed Python flake8/Black/isort/mypy checks: PASS with CI-pinned toolchain. Generator output includes exact implementation SHA256 values.
DOM verification: five rendered cases; injected markup produces zero image nodes; promoted authority produces zero case articles and Evidence unavailable. Chromium installation returned a truncated archive, so browser visual QA remains NOT_RUN.
Baseline broad run limitation: shallow history prevented immutable git-show source checks. Full Git history fetched before candidate broad rerun; initial failed log retained outside candidate.

Broad verification at candidate a56a91ef7ddff05d241541a8fe2cdffbbc08197a: 2058 Python tests PASS, 4 skipped, 146 subtests PASS (31.14s); npm test:ui 121 PASS; npm build PASS; TypeScript noEmit PASS. Next generated tsconfig changes were restored; they are not candidate changes. CI-pinned changed-file quality tools PASS. Fresh reviewer in progress.

Final review: no Critical. Important content-digest coherence issue retained for fix; reviewer Minor integer parser exception regraded Important because callers implementing the documented failure path can crash on an unhandled parser exception. Ruling: normalize parser ValueError within AssessmentInputError — preserve a reliable malformed-input boundary — cost if wrong: parser detail is carried only as exception cause.
Final: minor (deferred): module-request failure leaves the Loading message; authority ceiling remains visible and conservative. No module-failure recovery claim is made.
Reviewer declined to judge browser behavior, producer authenticity/custody, live containment, independent science, SBCF remote preservation and broad checks. Ruling: substantiate browser and broad checks with author-executed evidence; leave authenticity/custody, live containment and independent science unestablished; preserve SBCF by making no branch changes — these are the candidate's declared boundaries — cost if wrong: external acceptance and live integration remain required.
Fix RED evidence: matching-pin 5000-digit integer raised plain ValueError; edited retained assessment accepted unchanged digest. Tests failed before fixes. Async WebCrypto SHA256 now checks canonical assessment bytes before rendering; separate producer-authentication ceiling unchanged.

Final fixes verified: content-digest mutation test RED→GREEN (both binding fields and evidence IDs); large-integer parser test RED→GREEN. Full tests/: 2059 PASS, 4 skipped, 146 subtests PASS (29.88s). UI suite: 122 PASS. TypeScript noEmit, Next production build and changed-Python quality gates PASS.
Chromium 153 rendering completed using an alternate locally extracted browser: desktop five cases, mobile no horizontal overflow, edited assessment rejected, zero execution buttons. Desktop/mobile screenshots visually inspected by author; no user acceptance inferred. Earlier browser-download/runtime limitations are resolved for the successful local check.
Task 3 code/review/verification complete. Fresh reviewer findings are addressed by one author TDD fix pass; no second review or independent scientific validation claimed. Draft remote admission and hosted status recorded in completion receipt.
