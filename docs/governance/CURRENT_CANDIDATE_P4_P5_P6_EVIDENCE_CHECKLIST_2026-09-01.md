# Current-Candidate P4/P5/P6 Evidence Checklist — 2026-09-01

## Scope
Non-authorizing control record for selected experimental candidate `58ba9a072f40e94638b0332eeec19dd882a7ff95`.

## P4
- [ ] Exact candidate-bound blinding execution.
- [ ] Operational key custody/access separation.
- [ ] Independent blinded-condition bijection verification.
- [ ] No-premature-unblinding evidence.
- [ ] Exact candidate/deployment/protocol binding on retained evidence.

## P5
- [x] Exact candidate-bound pre-freeze run `33616403754`.
- [x] 18/18 candidate GitHub Actions workflows successful.
- [x] Candidate instrumentation/harness/truth/toolchain checks successful.
- [ ] Independent environment fingerprint recomputation.
- [ ] Independent topology/failure RNG stream check.
- [ ] Deterministic rerun comparison for final candidate state.
- [ ] Exact protocol/environment/dependency identity captured without secrets.

## P6
- [ ] Candidate evidence placed into configured durable archive.
- [ ] Independent retrieval from archive.
- [ ] Independent source/archive/retrieved SHA-256 equality.
- [ ] Retention manifest bound to exact freeze/candidate identity.
- [ ] No secrets in retained evidence.

## Promotion rule
No P4/P5/P6 gate may be promoted from open merely from implementation, historical evidence, successful documentation deployment, or related-candidate results.

**Current boundary: P4 OPEN · P5 FINAL CLOSURE OPEN · P6 OPEN / FAIL-CLOSED · PRE-FREEZE · NOT AUTHORIZED · N=0.**
