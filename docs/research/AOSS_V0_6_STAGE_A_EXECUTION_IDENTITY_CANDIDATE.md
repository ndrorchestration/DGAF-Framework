# AOSS v0.6 Stage-A non-fixture execution identity candidate

Issue #901 has three coupled execution-readiness predicates still open:
accepted installed environment, accepted source-driver/collector executable
identity, and accepted destination/attempt identity.

PR #918 established that the current source-module provenance plus fixture-only
destination/attempt identities are not sufficient admission evidence.

This tranche adds the next non-authorizing structure: a **prospective
non-fixture identity candidate** for external review. A candidate binds:

- the frozen ACP repository, commit, source-module path, and source blob;
- the frozen Stage-A recipe-catalog digest;
- the installed-environment evidence-candidate record digest;
- exact interpreter path and interpreter SHA-256;
- exact argv and working directory;
- a non-fixture destination URI; and
- a prospective attempt identity created before execution and before any outcome
  inspection.

The validator rejects fixture destinations, fixture/synthetic attempt IDs,
source drift, malformed digests, post-inspection attempts, pre-populated
adjudication, or any readiness promotion.

A successful validation means only:

```text
EXECUTION_IDENTITY_CANDIDATE=PASS_NON_FIXTURE_IDENTITY_CANDIDATE
INSTALLED_ENVIRONMENT_ACCEPTANCE=NOT_ESTABLISHED
SOURCE_DRIVER_BINDING=NOT_ESTABLISHED
EXECUTABLE_ACCEPTANCE=NOT_ESTABLISHED
DESTINATION_ACCEPTANCE=NOT_ESTABLISHED
EXTERNAL_ADJUDICATION=NOT_EXECUTED
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
```

The candidate is review material, not an acceptance event and not permission to
run an ACP study episode.
