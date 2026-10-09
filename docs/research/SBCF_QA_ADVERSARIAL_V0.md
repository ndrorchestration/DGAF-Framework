# SBCF checkpoint QA and adversarial workplan — draft

Related: issue #1338, draft PR #1339. Status: PRE-FREEZE, synthetic-only, NOT AUTHORIZED.

## Control limitations
The in-memory SimulatedGate is a Python object only, not an OS syscall interceptor, sandbox, egress filter, credential broker, worker registry, or an independent policy enforcement point. It is deliberately not connected to production infrastructure. The local hash chain detects accidental modification only when its trusted digest or checkpoint exists elsewhere; malicious replacement of the entire chain remains possible. No independent attestation implemented.

## Parallel tracks (uncompleted unless separately evidenced)
- C1 verify primary sources and bibliographic provenance; prioritize actual executable baselines and avoid fabricated parity claims.
- C2 adversarial threat matrix: hidden worker, forged observation, stale log, tampered queue, stolen credential, out-of-band egress, tool-call replay, racing revocation, cooperative text plus continued violation.
- C3 policy enforceability: separate PDP / PEP / broker, revoke tokens and workers without trusting the agent; require clean distinct release adjudication.
- C4 formal assumptions: define controlled state, measurement coverage and counterexamples to monotonic convergence; don't conflate increasing restriction state with actual risk reduction.
- C5 matched four-arm trials with seeded holdouts; dialogue changes candidate actions, never hard permission boundaries.
- C6 preregistration and power analysis before measuring outcome efficacy.
- C7 typed evidence to Structural Epistemics, ACP boundary, AOSS metrics and Tektite status projection.
- C8 independent reviewer and outside-operator falsification; preserve raw first-run evidence.
- C9 publish only bounded, exact-head evidence, subject to explicit authorization.

## Follow-up acceptance
Each checkpoint: source SHA, expected/actual, first failure, negative control, PASS/FAIL/BLOCKED, reviewer eligibility, retained hash, operational/synthetic scope, remediation. Hard block on any missing externally attested execution evidence. Existing scientific N=0 and independent/high assurance NOT ESTABLISHED.
