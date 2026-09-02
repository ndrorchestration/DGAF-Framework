# Current-Candidate P4/P5/P6 Evidence Checklist — 2026-09-01

## Scope

Non-authorizing evidence-planning/control record for the selected experimental candidate. This document does not create empirical observations, freeze the apparatus, grant authorization, unblind any condition, or change empirical N.

## Exact identity boundary

- Corrected apparatus provenance anchor: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- Selected experimental candidate: `58ba9a072f40e94638b0332eeec19dd882a7ff95`
- Selected candidate tree: `abdbc9b33c0fe3341280dfbc1c4a7c0f41df4deb`
- Candidate PR: `#192` (`candidate/p35-integrated-current-20260902`)
- Exact candidate deployment: **NOT ESTABLISHED**

## P4 — Security / blinding

- [ ] Exact candidate-bound execution demonstrating the blinding procedure.
- [ ] Operational key custody and access separation evidence.
- [ ] Independent blinded-condition bijection verification without key disclosure.
- [ ] Evidence that no premature unblinding occurred.
- [ ] Exact candidate/deployment/protocol identity attached to retained evidence.

## P5 — Provenance / reproducibility

- [x] Exact candidate-bound pre-freeze workflow execution: run `33616403754` on `58ba9a…`.
- [x] Candidate CI verification wave completed 18/18 successfully.
- [x] Candidate-bound instrumentation, harness, truth-layer, and toolchain checks passed.
- [ ] Independent environment fingerprint recomputation.
- [ ] Independent topology/failure stream separation check.
- [ ] Deterministic rerun comparison retained for final candidate state.
- [ ] Exact protocol/environment/dependency identity captured without secret disclosure.

## P6 — Durable Evidence Custody

- [ ] Current-candidate evidence artifact placed into configured durable archive.
- [ ] Independent retrieval from that archive.
- [ ] Independent SHA-256 equality across source/archive/retrieved bytes.
- [ ] Retention manifest bound to exact applicable freeze/candidate identity.
- [ ] No secret values included in retained evidence.

## Promotion rule

No P4/P5/P6 gate may be promoted from `OPEN` merely because implementation exists, a historical artifact exists, a documentation commit succeeds, a deployment is healthy, or a related prior candidate passed the same conceptual check.

## Current boundary

**P4 OPEN · P5 ENGINEERING/WORKFLOW EVIDENCE COMPLETE; FINAL CLOSURE OPEN · P6 OPEN / FAIL-CLOSED**  
**PRE-FREEZE · NOT AUTHORIZED · empirical N = 0**
