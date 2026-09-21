# AOSS v0.6 Stage-A external evidence reverification

Issue #901 now has accepted machinery for exact execution candidates and for a
non-promoting external admission-decision intake. This tranche adds the next
trust-boundary layer: cryptographic custody and reverification of supplied
external bytes.

The packet binds to the exact external-decision intake and records:

- the declared external decision-record URI and SHA-256;
- the SHA-256 recomputed from supplied retrieved bytes;
- retrieved byte length and retrieval timestamp;
- one or more reviewer-attribution evidence artifacts;
- each attribution artifact's declared and recomputed SHA-256; and
- the exact intake-record SHA-256.

Digest mismatch, retrieval-URI drift, duplicate attribution artifact IDs,
missing evidence, and packet tampering fail closed.

A cryptographic match proves only that the supplied bytes match the declared
digest. It does **not** prove that the reviewer identity is authentic, that the
reviewer is independent, that the evidence is sufficient for acceptance, or
that local governance adjudication has occurred.

Therefore a passing packet retains:

```text
CRYPTOGRAPHIC_REVERIFICATION=PASS_DECLARED_BYTES_MATCH_SHA256
REVIEWER_ATTRIBUTION_VERIFIED=false
INDEPENDENCE_VERIFIED=false
LOCAL_ADJUDICATION=NOT_EXECUTED
INSTALLED_ENVIRONMENT_ACCEPTANCE=NOT_ESTABLISHED
SOURCE_DRIVER_BINDING=NOT_ESTABLISHED
EXECUTABLE_ACCEPTANCE=NOT_ESTABLISHED
DESTINATION_ACCEPTANCE=NOT_ESTABLISHED
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
```

The checked-in tests use fixture bytes only. Their PASS establishes the
reverification mechanism, not the existence or acceptance of any real external
review record.
