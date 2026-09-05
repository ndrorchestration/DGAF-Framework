# P4 Human / Key Custody Procedure — Compatibility Path

**Status:** SUPERSEDED AS CANONICAL PROCEDURE / HUMAN MODE REMAINS VALID  
**Canonical procedure:** `docs/governance/P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md`  
**Related issue:** #285

This path is retained for provenance and backward references. The human-custody design previously defined here is now **Mode H** of the canonical P4 Independent Blinding Custody Procedure.

The scientific invariant has been generalized from a mandatory two-human topology to **independently enforceable custody**:

> Before the predeclared release condition, the execution/analysis principal must be unable to obtain the raw blinding key, cleartext mapping, commitment nonces, or functionally equivalent recovery material by unilateral action through ordinary, administrative, recovery, backup, policy-edit, credential-reset, export, or break-glass paths.

A genuinely distinct human Key Custodian remains an acceptable and strong way to satisfy that invariant, but it is no longer the only permitted topology. Institutional/third-party custody and independently enforced technical custody may also qualify when the evidence demonstrates that the analyst lacks every unilateral path capable of defeating the blind.

The following remain non-substitutes: alternate accounts controlled by the same person, AI agents/personas, ordinary repository secrets, analyst-recoverable password vaults, analyst-administered KMS/HSM configurations, ordinary encryption with analyst-held recovery material, and preregistration alone.

The P4-A/P4-B lifecycle split remains unchanged: P4-A is pre-execution custody closure; P4-B is the post-unblinding continuity audit.

No custody instance has been executed by this governance correction.

**P4-A: OPEN / NOT EXECUTED.**  
**Freeze: NOT ESTABLISHED.**  
**Pilot authorization: NOT GRANTED.**  
**Empirical N: 0.**
