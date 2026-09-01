# P8 / P9 / Freeze Readiness — Reconciled 2026-09-01

## Control status

- State: `PRE-FREEZE / FAIL-CLOSED`
- Current `main`: active documentation/evidence lineage; do not freeze a documentation tip into apparatus identity
- Corrected apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- Current mainline runtime candidate: `92ff830b1c67413df745e37087e6447c9c251b9a` / tree `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`
- Latest controlled completion candidate: `562753b3053b3566b0fcad1b0b1df151d7de119a`
- P2 current runtime predicate: `VERIFIED` — run `33509348174`, artifact `9800942933`
- P6a current runtime predicate: `VERIFIED` — run `33509416955`, artifact `9800972819`
- P3: `OPEN`
- P4: `OPEN`
- P5: `OPEN`
- P6: `OPEN / FAIL-CLOSED`
- P7: `ADOPTED / FINAL BINDING OPEN`
- P8: `OPEN / FAIL-CLOSED`
- P9: `SCOPED PASS / BROADER CLOSURE OPEN`
- Freeze: `NOT CREATED`
- Authorization: `NOT GRANTED`
- Empirical N: `0`

This is a readiness/control artifact. It is not evidence that every predicate has passed and it does not authorize execution.

## Dynamic control model

Every gate is a predicate with explicit scope, prerequisites, evidence requirements, freshness conditions, invalidation triggers, and closure rules. Documentation repetition does not increase epistemic strength.

## Predicate matrix

| Predicate | State | Closure requirement |
|---|---|---|
| P1 candidate identity | OPEN | Exact selected candidate/source/tree/deployment binding and retained provenance |
| P2 runtime | VERIFIED | Current evidence is bound to `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`; re-run if selected pilot candidate changes |
| P3 artifact contract | OPEN | Current selected candidate artifact-contract evidence |
| P4 blinding/security | OPEN | Operational custody, access separation, bijection, and negative-state evidence |
| P5 reproducibility | OPEN | Current selected candidate environment/topology/RNG reproduction |
| P6 durable custody | OPEN / FAIL-CLOSED | Durable write/retrieve/hash round trip for the selected candidate |
| P6a CORS | VERIFIED | Current evidence is bound to `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`; re-run if selected pilot candidate changes |
| P7 scientific target | ADOPTED / FORMALLY OPEN | Exact selected candidate/protocol/analysis/freeze binding |
| P8 analysis lock | OPEN / FAIL-CLOSED | Exact analysis/configuration/protocol/current-tree binding and required TGL/P-35 predicates |
| P9 independent verification | SCOPED PASS / BROADER CLOSURE OPEN | Complete evidence-chain verification for the selected candidate; scoped run `33567199896` verifies `562753b…` identity, alternate canonicalization/hash, and authority identity |

## P9 update

Run `33567199896` completed successfully on 2026-09-01 for candidate `562753b3053b3566b0fcad1b0b1df151d7de119a`.

Verified:

- exact checkout identity (`HEAD == GITHUB_SHA`);
- independent `jq -S -c` plus `sha256sum` canonicalization/hash path;
- authority-identity regression (`4 passed`);
- independent P9 evidence JSON plus SHA-256 sidecar upload.

Artifact: `9823570326`  
Artifact ZIP digest: `sha256:8e3435a3af0dc5de7376d970b9f1665a18db8ff04b26a2c0eaae8acf8b095d85`.

This is scoped verification evidence. It does not establish P9 closure for a different candidate, and it does not itself establish authorization, empirical execution, external archive, or efficacy.

## Candidate selection boundary

The latest P9 run targets `562753b…`, while current mainline runtime evidence targets `92ff830b…`. These identities must remain separate until a governance decision explicitly selects and rebinds the candidate for the next freeze cycle. No evidence transfers merely because the branch/repository is shared.

## Historical-priority boundary

The historical-priority review is separate from freeze readiness. Current adjudication establishes external prior art for individual governance, formation, provenance, artifact-identity, veto, escalation, and idempotency mechanisms. The remaining historical hypothesis concerns a potentially distinctive cross-domain integration, not primitive firstness.

Primary record: `docs/research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md`.

## Freeze and authorization boundary

No new immutable freeze exists. Pilot authorization remains a separate explicit governance transition after all required predicates and freeze verification close.

**No pilot execution. No unblinding. No efficacy claim. Empirical N remains 0.**
