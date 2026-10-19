# v1.6 DemiJoule safety validation — bounded falsification and repair

**State: OPERATOR-LOCAL SOURCE QA / NOT CANONICAL ADMISSION.**
Controller: GitHub issue #1379. Investigation #1374 separately concerns
whether the v1.6 dgaf_decision placeholder is misunderstood as final
authorization.

## Protected-main first failures

Protected main 0e09ae555136fb9d433c7294f445e0b656c7e705 accepted invalid
six-axis scores without type and finiteness checks. The first same-system
Python source probe observed:

- Normal six finite 0.9 scores: PASS (positive control).
- Consent NaN: **PASS** (incorrect acceptance).
- Consent positive infinity: **PASS** (incorrect acceptance).
- Consent boolean True: **PASS** (non-numeric Boolean accepted).
- Consent string, null score or null safety mapping: uncaught TypeError.
- Consent negative infinity or missing axes: ESCALATE.

This is confirmed reference-module input-validation behavior, **not**
proof that live ACP, TGL, a production provider, or the Next.js app
calls this legacy reference gate.

## Narrow remediation

Require six named axes from a mapping, each a real numeric scalar rather
than bool or a coercible string, all finite and within normalized
[0.0, 1.0]. Malformed inputs return the existing ESCALATE result shape,
without throwing. Valid finite values at and above the historical 0.5
threshold still pass; finite values below it still escalate.

Only the DemiJouleGate.safety_gate implementation changes.
No AgentAmethyst orchestration ordering, audit field names, DGAF/C3/OPA
comparator, empirical analysis, protected data, artifact, or permission
admission logic is modified. The ambiguity that dgaf_decision=PASS
can coexist with apogee_grade=ESCALATE remains a separate issue.
Never use that early schema-placeholder as standalone authorization.

## Consumer limits

Source search found components.ensemble_v16 imported by the historical
PDMAL adapter and associated parity tests, for SCPE and convergence.
It did not establish that the current TypeScript /api/orchestrate
endpoint or runtime-action admission stack invokes this legacy gate.
No independent review or live browser/provider test has occurred.

## Admission

- Retain first failures in the issue and original Git history.
- Reproduce corrected positive/negative controls on exact new source.
- Require eligible non-author code review before any protected-main merge.
- SCIENTIFIC_N_INCREMENT=0.
- INDEPENDENT_VALIDATION=NOT_ESTABLISHED.
- CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED.
- HIGH_ASSURANCE=NOT_AUTHORIZED.
