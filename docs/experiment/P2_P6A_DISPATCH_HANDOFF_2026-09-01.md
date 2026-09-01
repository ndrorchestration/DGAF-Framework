# P2 / P6a Dispatch Handoff — Verified Runtime Candidate

**Status:** VERIFIED RUNTIME EVIDENCE / PRE-FREEZE / FAIL-CLOSED / N=0

## Candidate binding

- `apparatus_source_sha`: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- `candidate_sha`: `92ff830b1c67413df745e37087e6447c9c251b9a`
- `candidate_tree_sha`: `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae`
- `deployment_id`: `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`
- `base_url`: `https://dynamicgovernanceagenticformation-3y3d8o5dp-ndrorchestration.vercel.app`
- `allowed_origin`: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`

The apparatus source and runtime candidate are deliberately distinct identities. The candidate descends from the corrected apparatus source, but runtime evidence is bound to the exact candidate commit/tree and deployment above.

## Verified P2

- Workflow: `.github/workflows/p2-runtime-verification.yml`
- Run: `33509348174`
- Artifact: `9800942933`
- Digest: `sha256:00519533edcaa4c09410b3ed29e49437a5ce8a23ea341a2b798490e110f056c2`
- Result: `VERIFIED`
- Five required cases passed.
- Required fail-closed case `valid_missing_audit`: HTTP 503, decision `BLOCKED`.

## Verified P6a

- Workflow: `.github/workflows/p6a-cors-verification.yml`
- Run: `33509416955`
- Artifact: `9800972819`
- Digest: `sha256:9e78ebef5eaa7f33027ec09c0cb922f57bc43dab2fcc694a823ac504c611fcdd`
- Result: `VERIFIED`
- Allowed-origin preflight: HTTP 204.
- Disallowed-origin preflight: HTTP 403.
- Allowed and disallowed POST cases matched expected checks.

## Evidence boundary

These P2/P6a results close only the respective runtime predicates in the recorded endpoint/deployment/environment scope. They do not establish efficacy, freeze, authorization, unblinding, or empirical execution.

## Latest downstream status

- P3: `OPEN`
- P4: `OPEN`
- P5: `OPEN`
- P6: `OPEN / FAIL-CLOSED`
- P7: `ADOPTED / FINAL BINDING OPEN`
- P8: `OPEN / FAIL-CLOSED`
- P9: `SCOPED PASS / BROADER CLOSURE OPEN` via run `33567199896` against separate completion candidate `562753b…`
- Freeze: `NOT ESTABLISHED`
- Authorization: `NOT GRANTED`
- Empirical N: `0`

The P9 result does not transfer to this mainline runtime candidate. A candidate change requires explicit rebinding and fresh affected-predicate evidence.

## Current closure sequence

`selected candidate → P3/P4/P5/P6 → P7 exact binding → P8 → broader P9 → immutable freeze → explicit authorization → blinded pilot`.

## Historical handoff rule

The prior `P2_P6A_DISPATCH_HANDOFF_2026-08-31.md` is a superseded snapshot and should be interpreted as historical evidence of the pre-verification state. Its earlier `NOT_ESTABLISHED` dispatch boundary must not override this current handoff. Historical candidate/deployment values remain non-closing and are not valid current dispatch inputs.

## Cross-references

- `../CURRENT_STATE.md`
- `../CLAIM_EVIDENCE_INDEX.md`
- `../governance/P1_TO_P9_EVIDENCE_MATRIX.md`
- `../governance/P9_LATEST_RECONCILIATION_2026-09-01.md`
