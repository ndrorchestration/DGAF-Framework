# Minimal DGAF Construct Decision — 2026-08-30

**Status:** DECIDED / PRE-N=1 BOUNDARY
**Empirical N:** 0
**Pilot authorization:** NOT GRANTED

## Decision

The current PDMAL experiment SHALL test the **minimal DGAF/TGL construct actually defined by the canonical TGL execution contract**, not the entire historical DGAF governance ecosystem.

The historical gates that the canonical TGL marks as required are **constitutive of the tested treatment** and therefore cannot be declared out-of-scope merely to reach N=1.

The remaining historical governance mechanisms that are not required by the selected TGL treatment are **outside the minimal construct** and shall remain FAIL-CLOSED unless and until a future experiment explicitly incorporates them.

## Basis

The canonical `TriadicGovernanceLoop.REQUIRED_STEPS` is `{1, 2, 3, 4, 5, 6, 8}`. These correspond to:

| TGL step | Pattern | Gate | Minimal-construct disposition |
|---|---|---|---|
| 1 | P-31 | `SCPE_Prune` | **A — required** |
| 2 | P-33 | `PDMAL_ConvergenceMonitor` | **A — required** |
| 3 | N/A | `DemiJoule_SafetyGate` | **A — required** |
| 4 | P-27 | `KAPPA_Router` | **A — required** |
| 5 | P-29 | `Sentinel_RiskPass` | **A — required** |
| 6 | P-32 | `PhiClosure_Gate` | **A — required** |
| 8 | P-30 | `Apogee_AttestationGate` | **A — required** |

The TGL source defines an absent hook as `SKIP`; required `SKIP` transitions the turn to `ESCALATE`. The PDMAL adapter additionally converts a required skipped gate into `FAIL_CLOSED`, preventing an unwired required gate from becoming a treatment outcome.

## Out-of-scope boundary

The following are **not** required steps in the canonical TGL treatment contract and therefore are not pre-N=1 historical-recovery obligations merely because they exist in the wider governance architecture:

- HPG / `HPG_OctaveGate` (step 7), conditional on P-32 PASS;
- Herald / `Herald_FanOut` (step 9), an evidence/fan-out operation rather than a treatment-defining control decision;
- other historical governance mechanisms not present in the selected canonical TGL treatment path.

They remain operationally fail-closed or observational infrastructure as implemented. They may be incorporated in a later explicitly governed construct, but their absence does not by itself redefine the minimal DGAF treatment.

## Consequence for Issue #152

Issue #152 has completed its R1–R4 recovery determination for the current evidence epoch:

- **A for P-31, P-33, DemiJoule, P-27, P-29, P-32, and P-30.** These are required treatment components under the canonical TGL contract.
- **B for non-required historical governance capabilities outside the selected minimal treatment.** They remain FAIL-CLOSED and deferred.
- **No invented adapters.** A historical gate may only be adapted if genuinely new authoritative semantic evidence or an explicitly adopted new governed specification establishes a defensible translation to the current `ConsensusState`.
- **Unresolved semantics remain a genuine treatment-integrity blocker.** If a required gate cannot satisfy restoration or governed adaptation without changing its meaning, the defined full treatment remains FAIL-CLOSED and N=1 cannot claim execution of that treatment.

## R1–R4 semantic-recovery result

The bounded read-only semantic-recovery map is recorded in `docs/experiment/R5_R7_GATE_SEMANTIC_RECOVERY_MAP_2026-08-30.md`.

Current result: **no seven-gate adapter is justified from the available evidence epoch**. The current `ConsensusState` supplies useful fields, but field presence does not establish historical semantic equivalence. The recovery determination is therefore **CLOSED / FAIL-CLOSED for this evidence epoch**, not an invitation to repeat the same investigation.

Reopening the recovery determination requires a genuine state change: newly recovered authoritative historical contract material or an explicitly adopted new governed treatment specification. Documentation churn, CI fan-out, deployment-health success, or repeated review of the same evidence does not reopen R1–R4.

## Anti-trap constraint

This decision does **not** authorize reconstruction of every historical DGAF component.

For each required gate, only the minimum information necessary to establish a semantically faithful executable contract is relevant. Any historical capability outside the minimal construct is explicitly deferred.

The existence of further possible governance refinement is not a blocker.

## Candidate and N=1 boundary

The post-#151 apparatus candidate is designated separately as:

`05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`

Candidate designation is **not** a freeze and does not itself constitute candidate-scoped experimental verification. The apparatus identity remains stable across documentation-only commits; only an executable apparatus change or an explicitly governed treatment-specification change creates a new candidate cycle.

The first N=1 observation may begin only after the seven required treatment components have either:

1. been restored without semantic change; or
2. been adapted through an explicit, loss-accounted, governed translation that preserves the treatment definition.

If a required gate cannot satisfy either condition, the experiment remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**.

## Epistemic classification

- Historical gate existence: **RECOVERED** where documented by Issue #152.
- Required status: **VERIFIED FROM CANONICAL TGL CONTRACT**.
- R1–R4 recovery determination: **CLOSED / FAIL-CLOSED FOR CURRENT EVIDENCE EPOCH**.
- Current semantic adapter suitability: **NOT ESTABLISHED** for the seven required gates.
- Candidate designation: **ESTABLISHED** for `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37`.
- Candidate-scoped experimental execution: **NOT YET VERIFIED**.
- Scientific efficacy: **NOT ESTABLISHED**.

## Source boundary

This decision is derived from the canonical TGL implementation, PDMAL protocol, and governed recovery taxonomy in Issue #152. It does not promote historical claims of validation into current evidence and does not authorize experimental execution.
