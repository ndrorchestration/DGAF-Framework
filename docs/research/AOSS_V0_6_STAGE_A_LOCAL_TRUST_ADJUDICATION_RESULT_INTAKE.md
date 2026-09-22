# AOSS v0.6 Stage-A local trust adjudication-result intake

This tranche provides a custody boundary for an eventual local trust-review
result. It is deliberately separate from trust promotion.

The intake records:

- exact SHA-256 binding to the accepted local trust-review packet;
- reviewer identity and offset-aware review timestamp;
- decision-record URI and SHA-256;
- whether fresh cryptographic verification was reported;
- reviewer-attribution finding;
- independence finding.

Allowed findings are `VERIFIED`, `NOT_VERIFIED`, and `BLOCKED`.

A structurally positive result is represented only as
`POSITIVE_REVIEW_REPORTED`. It does **not** set either local trust predicate
true. This prevents an intake mechanism from self-authorizing merely because a
record says the review succeeded.

The fixed boundary is:

```text
trust_promotion=NOT_EXECUTED
reviewer_attribution_verified=false
independence_verified=false
INSTALLED_ENVIRONMENT_ACCEPTANCE=NOT_ESTABLISHED
SOURCE_DRIVER_BINDING=NOT_ESTABLISHED
EXECUTABLE_ACCEPTANCE=NOT_ESTABLISHED
DESTINATION_ACCEPTANCE=NOT_ESTABLISHED
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
```

A later acceptance mechanism must independently verify the result record and
authorize any trust-state transition. Checked-in test inputs are fixtures only;
this tranche does not perform a real review, accept identities, execute ACP
episodes, or generate study outcomes.
