# AOSS v0.6 Stage-A local trust-review packet

This tranche prepares retained review material for the two local trust blockers
that remain after the accepted blocked local-adjudication candidate:

- `LOCAL_REVIEWER_ATTRIBUTION_NOT_VERIFIED`
- `LOCAL_INDEPENDENCE_NOT_VERIFIED`

The packet binds the exact reviewer-trust intake and local-adjudication
candidate by SHA-256 and requires one retained evidence identity for each local
review role:

1. reviewer attribution;
2. reviewer independence.

Retaining an evidence URI and SHA-256 is **not** the same as authenticating the
evidence or deciding the trust question. The packet therefore fixes the review
state to:

```text
classification=NOT_EXECUTED
reviewer_identity=null
reviewed_at=null
fresh_cryptographic_verification=false
reviewer_attribution_verified=false
independence_verified=false
```

Those fields cannot be populated by this mechanism. Any attempt to prefill them
fails closed. A later, separately reviewed adjudication-result intake must carry
an actual reviewer decision and its evidence before local trust can change.

The downstream boundary remains unchanged:

```text
INSTALLED_ENVIRONMENT_ACCEPTANCE=NOT_ESTABLISHED
SOURCE_DRIVER_BINDING=NOT_ESTABLISHED
EXECUTABLE_ACCEPTANCE=NOT_ESTABLISHED
DESTINATION_ACCEPTANCE=NOT_ESTABLISHED
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
```

Checked-in evidence identities are fixtures only; this tranche performs no real
trust review and generates no ACP outcome.
