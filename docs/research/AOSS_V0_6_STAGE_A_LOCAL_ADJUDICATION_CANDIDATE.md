# AOSS v0.6 Stage-A local adjudication candidate

This tranche binds the accepted external admission-decision intake,
cryptographic reverification packet, and reviewer-trust verification intake
into a single local adjudication candidate.

It is intentionally a **blocked candidate**, not an acceptance record.

The mechanism records:

- exact SHA-256 bindings to all three upstream evidence records;
- local adjudicator identity and timestamp;
- the requested disposition;
- the effective disposition;
- explicit blockers preventing local promotion.

Even when the external trust intake reports both reviewer attribution and
independence as `VERIFIED`, the current accepted trust intake keeps local trust
state false. Therefore the adjudication candidate remains blocked on:

```text
LOCAL_REVIEWER_ATTRIBUTION_NOT_VERIFIED
LOCAL_INDEPENDENCE_NOT_VERIFIED
```

The implementation deliberately has no unblocked acceptance path. If no blockers
are present, it fails closed with `LOCAL_ADJUDICATION_UNBLOCKED_PATH_NOT_IMPLEMENTED`
rather than silently granting authority.

Current boundary remains:

```text
REVIEWER_ATTRIBUTION_VERIFIED=false
INDEPENDENCE_VERIFIED=false
INSTALLED_ENVIRONMENT_ACCEPTANCE=NOT_ESTABLISHED
SOURCE_DRIVER_BINDING=NOT_ESTABLISHED
EXECUTABLE_ACCEPTANCE=NOT_ESTABLISHED
DESTINATION_ACCEPTANCE=NOT_ESTABLISHED
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
```

The checked-in tests use structural fixtures only and do not represent a real
local governance adjudication event.
