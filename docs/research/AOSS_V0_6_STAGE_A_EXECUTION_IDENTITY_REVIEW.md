# AOSS v0.6 Stage-A execution-identity external-review packet

Issue #901 requires accepted source-driver/collector executable identity and
accepted destination/attempt identity before collection readiness can be
established.

The currently accepted proposal records are intentionally insufficient for
those admissions:

- the source-driver binding is a non-collecting synthetic contract and has no
  accepted executable or destination;
- the executable identity is only source-module provenance;
- the destination identity is a synthetic fixture URI; and
- the attempt identity is a synthetic fixture attempt ID.

This tranche binds the exact proposal records by deterministic SHA-256 and
creates an external-review packet that **preserves those insufficiencies as
blockers**. It does not reinterpret fixture identities as real identities.

A successful packet validation means only:

```text
EXECUTION_IDENTITY_REVIEW_PACKET=PASS_BLOCKED_REVIEW_PACKET
SOURCE_DRIVER_BINDING=NOT_ESTABLISHED
EXECUTABLE_ACCEPTANCE=NOT_ESTABLISHED
DESTINATION_ACCEPTANCE=NOT_ESTABLISHED
REAL_EXECUTABLE_IDENTITY_REQUIRED=true
REAL_DESTINATION_IDENTITY_REQUIRED=true
REAL_ATTEMPT_IDENTITY_REQUIRED=true
EXTERNAL_ADJUDICATION=NOT_EXECUTED
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
```

A later admission candidate must supply real executable, destination, and
attempt identities under a separate review. This module cannot create or
accept those identities and cannot enable collection.
