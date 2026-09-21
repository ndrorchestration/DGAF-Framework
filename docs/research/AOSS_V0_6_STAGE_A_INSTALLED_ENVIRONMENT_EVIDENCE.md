# AOSS v0.6 Stage-A installed-environment evidence candidate

Issue #901 requires an accepted installed environment before executable
collection readiness can be considered.

This tranche creates a **reviewable candidate evidence envelope**, not an
acceptance event. It captures the exact interpreter implementation/version,
dependency-lock digest, platform, executable path, prefix/base-prefix, and an
offset-aware observation timestamp. The evidence payload is canonically
serialized and bound to a deterministic SHA-256.

Validation fails closed on runtime/lock drift, malformed or missing runtime
facts, digest tampering, or any attempt to promote acceptance, source-driver
binding, execution permission, collection readiness, outcomes, or scientific N.

A successful candidate validation means only:

```text
INSTALLED_ENVIRONMENT_EVIDENCE_CANDIDATE=PASS_OBSERVED_CANDIDATE_NOT_ACCEPTED
INSTALLED_ENVIRONMENT_ACCEPTANCE=NOT_ESTABLISHED
SOURCE_DRIVER_BINDING=NOT_ESTABLISHED
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
```

The actual collection host must generate its own evidence candidate and that
exact evidence must undergo a separate acceptance review. CI observations do
not automatically become accepted collection-host evidence.
