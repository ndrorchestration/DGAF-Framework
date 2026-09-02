# P-35 Remediation Audit — 2026-09-02

## Scope

This record audits the current remediation branch for the P-35 premise-hook integration boundary. It is engineering/pre-freeze evidence only and does not establish protocol freeze, pilot authorization, unblinding, or empirical execution.

## Current head

- PR: #188
- Branch: `remediation/p35-premise-hook-2026-09-01`
- Current head: `df307e8e9f36062923e92c826b0a7ae06b870e58`
- Historical completion candidate that motivated remediation: `a43219b4ed91fff8615f6c655ab3d17ca871fc29`

## Verified P-35 boundary

The current implementation requires an explicit callable checker for `ConsensusTask(condition="dgaf")` and `DGAF_TGLAdapter`. `run_pilot()` loads `PDMAL_PREMISE_CHECKER` before any pilot task construction and passes the resulting callable into DGAF tasks.

The direct runner regression in `experiments/pdmal_pilot/test_run_pilot_p35.py` verifies both missing-checker refusal before task construction and propagation of an explicitly loaded checker into a DGAF task.

The canonical TGL tests verify that P-35 violations and unexpected checker exceptions return sealed KILL audits rather than bypassable exceptions.

## Additional defect found and remediated

The non-empirical runtime characterization harness still constructed DGAF tasks without a P-35 checker after the `ConsensusTask` boundary was tightened. That path has now been corrected.

- Default runtime characterization conditions are now `null`, `simple`, and `static`.
- A DGAF characterization may only be requested when `PDMAL_PREMISE_CHECKER=module:attribute` is explicitly supplied.
- No permissive or synthetic checker is inserted.
- Runtime characterization workflow now runs on the remediation branch and asserts that its default artifact contains no DGAF condition and no configured P-35 checker.
- Added `test_runtime_characterization_p35.py` covering the missing-checker refusal and explicit-checker propagation boundary without empirical execution.

## Evidence status

The previously successful exact-head pre-freeze run `33592005918` and artifact `9832129713` are bound to `d460dea0e920a616269a1a929be42e0bd2535c13`. Because subsequent commits changed the remediation branch, that evidence does not transfer to `df307e8e9f36062923e92c826b0a7ae06b870e58`.

A fresh aggregate verification is therefore required for the current head.

## Control boundary

P-35 remediation is treated as an engineering finding under active verification. P8 remains open/fail-closed. Freeze and pilot authorization remain absent. Empirical N remains zero.
