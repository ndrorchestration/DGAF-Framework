# SBCF replay rollback falsification — 2026-10-09

Research-only, fail-closed. Linked: GitHub #1338 / draft PR #1339.

## Observation
A copied pre-admission SQLite file can replace the current replay store. After restart, the previously admitted higher-sequence event is accepted again, because the restored high-water mark predates it. The new negative test records this as a strict expected failure (`xfail`), **not a successful anti-rollback defense**.

## QA
`tests/test_sbcf_adversarial_gaps.py`: modified signed payload rejection, unauthorized field rejection, normal persistent high-water test; plus rollback counterexample. The latter is known failing until an independently retained anti-rollback checkpoint is implemented and tested. Do not turn xfail into a green security claim.

## Required remediation
Use a trustworthy external sequence/checkpoint witness, verified run-policy binding and recovery behavior. Evaluate snapshot restore, device rollback, forked writers, multi-process writes, forged sources and stale counters. No production custody or identity root exists in this prototype.

Scientific efficacy, independence, high assurance, and live quarantine continue NOT ESTABLISHED. Keep protected main unchanged.
