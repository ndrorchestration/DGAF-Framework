# Stale Document Sweep — 2026-08-25

## Classification
Historical SHAs are retained when they document historical evidence, prior freezes, or superseded apparatus. They are stale only when presented as current authority without historical qualification.

## References identified
Prior candidates include `4983f44`, `94fb6fd`, `b098e644`, `3510b868`, and earlier P7/P8 states. These are not automatically errors because they serve as historical evidence.

## Current lineage
Later corrections include `0d207ff87b2773ec5a06f7b2fadf6c67138b65ec` and `fcff79c20185115297a93b6bd97d3b4b5f05383e`. Current-state documents must identify their actual candidate.

## Remediation rules
1. Preserve historical evidence with explicit historical labels.
2. Correct historical SHAs presented as current authority.
3. Distinguish implementation, execution, verification, authorization, and empirical evidence.
4. Keep expert-panel findings linked to the current gate state.
5. Repeat this sweep before authoritative freeze and after candidate changes.

## Expert-panel cross-check
Panel-derived controls remain prerequisites: P7 traceability, parameter-boundary classification, operational blinding, infrastructure-unavailable policy, adversarial preflight, formal unblinding, and comparative-baseline scheduling.

## Current state
- P2: PASS
- P6a: PASS
- PDMAL instrumentation dry run: PASS
- Governance CI current-candidate PASS: NOT ESTABLISHED
- P8: OPEN
- Protocol freeze: NO-GO
- Pilot authorization: NOT GRANTED
- Empirical N: 0
