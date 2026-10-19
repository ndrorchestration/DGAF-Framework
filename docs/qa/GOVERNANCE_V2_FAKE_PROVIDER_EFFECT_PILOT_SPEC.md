# DGAF V2 — Fake-Provider Effect Pilot

## Scope and prior work

This is a provisional and separately scoped engineering pilot under comparative
controller #1061. The earlier 11-case recovery/composition and 8-case receipt
mutation comparisons chiefly validate statuses, recovery functions, and linked
artifacts. The new pilot additionally observes writes recorded by a separate
in-process fake-provider event log. It still does not connect a real provider,
real distributed custody, or a real human operator.

The fixed operator-local expected-outcomes file is
experiments/governance_benchmark/effect_pilot/pilot_v1.json.
Its SHA-256 is
1d4312938a5847c6e000faa73a10c0660108044aebc84319b45be414bd4f34d0.
This is an operator-authored candidate oracle, not independent ground truth.

## Four reproducible cases

- GOV2-01: valid request and cached idempotent replay; one fake effect.
- GOV2-04: fake write succeeds before its acknowledgement is lost;
  blind retry is blocked pending reconciliation; one fake effect.
- GOV2-05: deterministic interleaving of two in-flight callers;
  the second is blocked, the first completes; one fake effect.
- GOV2-06: first simulated attempt produces no effect; the in-process
  fake-provider log confirms no effect; after simulated fresh authorization,
  a new attempt completes. This does not verify actual authorization.

Both arms receive the same action identity, digest, interleaving schedule,
fault, fake provider interface, and provisional oracle. DGAF uses its merged
InMemoryIdempotencyLedger reference class. The conventional arm independently
implements an equally capable ledger with reserved, unknown, and completed
states; no intentionally disabled features.

Fake-provider append records, not arm-returned status, are the independent
observed event count inside the toy harness. However the storage and verifier
are part of this same operator-controlled process, not an independently owned
trust domain.

## Error detection and acceptance boundary

Fail the same-system test if the oracle byte digest differs; fixtures
unexpectedly change; a fake provider writes twice under one identity;
an in-flight duplicate is dispatched; an unknown outcome is blindly retried;
or either policy arm differs from the provisional expectation. A negative test
deliberately injects duplicate writes and demands detection.

Recorded event counts and decision sequences can be reported only as
synthetic implementation observations, not scientific efficacy,
operator workload, production reliability, or an externally sampled result.
The deterministic interleaving is not a threaded or distributed concurrency
test. No random sample or statistical N is claimed.

## Next admission step

Create a signed, isolated draft PR for this pilot and obtain exact-head
CI plus an eligible non-author assessment of fairness, oracle independence,
provider-state visibility, and scenario controls. Do not merge or promote
research claims solely from these tests. Do not alter PR #1362, frozen #1067,
protected main, driver/provider admission, or scientific authorization.

SCIENTIFIC_N_INCREMENT=0.
INDEPENDENT_VALIDATION=NOT_ESTABLISHED.
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED.
HIGH_ASSURANCE=NOT_AUTHORIZED.
STATE_OF_THE_ART=NOT_ESTABLISHED.
