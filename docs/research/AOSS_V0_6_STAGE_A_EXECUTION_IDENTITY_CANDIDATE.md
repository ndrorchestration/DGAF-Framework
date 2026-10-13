# AOSS v0.6 Stage-A exact driver execution identity candidate

Issue #901 has three coupled execution-readiness predicates still open:
accepted installed environment, accepted source-driver/collector executable
identity, and accepted destination/attempt identity. Issue #1348 tracks the
remaining driver/executable identity gap.

PR #918 established that source-module provenance plus fixture-only
destination/attempt identities are not sufficient admission evidence. The
later prospective candidate mechanism added real environment/destination
shapes, but its arbitrary nonempty `argv` field did not prove that the named
driver target existed.

This candidate hardens that boundary without admitting execution. It binds:

- the frozen ACP repository, commit, source-module path, and source blob;
- the corrected Stage-A recipe-catalog SHA-256 from the #1350 candidate;
- an exact tracked DGAF source-driver path, Git blob, raw SHA-256, status, and
  callable entrypoint;
- the installed-environment evidence-candidate record digest;
- exact interpreter path and interpreter SHA-256;
- the exact driver callable plus working directory;
- a non-fixture destination URI; and
- a prospective attempt identity created before execution and before any
  outcome inspection.

The bound driver candidate is
`scripts/aoss_stage_a/source_driver.py` with:

- introduction commit `838ecf26519d4d4cfcd836793a4bdc13b2be24cc`;
- Git blob `2db1146f2d1caa32445d79fdf75357833107802a`;
- raw SHA-256
  `0ce16a2f60a17502c397ded13e8eb612b6cc8fa8ede5a9ec26103d9e0f151bd9`;
- entrypoint
  `scripts.aoss_stage_a.source_driver:generate_source_episode`; and
- status `IMPLEMENTED_NOT_ADMITTED`.

The driver implementation is deliberately separated from authorization. Its
source defines the frozen native ACP workloads and explicit post-export
transformations, but current verification is source/static only. The current
work does not import the driver, import ACP through the driver, execute an ACP
episode, reserve a study attempt, or create outcomes.

The validator rejects fixture destinations, fixture/synthetic attempt IDs,
source drift, stale recipe-catalog identity, malformed digests, substituted
driver path/blob/SHA/entrypoint, post-inspection attempts, pre-populated
adjudication, or any readiness promotion.

A successful candidate validation means only:

```text
EXECUTION_IDENTITY_CANDIDATE=PASS_EXACT_DRIVER_IDENTITY_CANDIDATE
DRIVER_STATUS=IMPLEMENTED_NOT_ADMITTED
INSTALLED_ENVIRONMENT_ACCEPTANCE=NOT_ESTABLISHED
SOURCE_DRIVER_BINDING=NOT_ESTABLISHED
EXECUTABLE_ACCEPTANCE=NOT_ESTABLISHED
DESTINATION_ACCEPTANCE=NOT_ESTABLISHED
EXTERNAL_ADJUDICATION=NOT_EXECUTED
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

A structurally valid identity candidate is review material, not an acceptance
event and not permission to import the driver or run an ACP study episode.
