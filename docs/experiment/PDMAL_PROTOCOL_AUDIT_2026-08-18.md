# PDMAL Protocol Audit — 2026-08-18

## Audit status

**PRE-FREEZE / AUDIT COMPLETED / FREEZE NOT AUTHORIZED**

This audit checks the current protocol text against the implementation visible on `epistemic/evidence-architecture-v1`. It does not promote unresolved controls to final status.

## Protocol identity

- Protocol file: `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md`
- Current protocol content SHA: `f367328fdf0854a12b22bd94a25a58973923c5c7`
- Protocol status: `PRE-FREEZE / PANEL-ADJUDICATED / NO DATA COLLECTION AUTHORIZED`
- Freeze commit SHA: not yet assigned
- Freeze timestamp: not yet assigned

The protocol itself therefore remains the authoritative pre-freeze document and must not be rewritten as `FROZEN` merely to remove open-control language.

## Cross-reference verification

| Control | Result | Evidence |
|---|---|---|
| Primary endpoint FFCR | MATCH | Protocol defines raw FFCR and mean paired seed-level difference; runner/task engine exposes `ffcr_success`. |
| Sample-size equation | MATCH | Protocol uses paired-difference normal approximation with alpha 0.05, power 0.80, MDD 0.15, `math.ceil`; `sample_size.py` implements the same equation. |
| Timeout | MATCH | Protocol states 60 seconds; `task_engine.py` sets `TRIAL_TIMEOUT_SECONDS = 60.0`. |
| Retry budget | MATCH | Protocol states 3 attempts; `task_engine.py` sets `MAX_ATTEMPTS = 3`. |
| Recovery window | MATCH | Protocol states 30 seconds; `task_engine.py` sets `RECOVERY_WINDOW_SECONDS = 30.0`. |
| Seed runtime ceiling | MATCH IN CODE / NOT YET CHARACTERIZED | Protocol states 300 seconds; `task_engine.py` sets `SEED_RUNTIME_CEILING_SECONDS = 300.0`, but required freeze characterization remains open. |
| RNG | MATCH | Protocol specifies `SeedSequence.spawn()` + `Generator(PCG64)`; `harness_contract.py` implements those controls. |
| Blinding | PARTIAL | HMAC-SHA256 primitive exists and is CI-tested with test-only keys; operational protected mapping custody is not yet verified. |
| Artifact schema | PARTIAL | Machine-readable schema validator now requires `schema_version=1.0`; retention is currently 30 days; long-term retention decision remains open. |
| Topology provenance | IMPLEMENTED / CI PENDING | Generator parameters and graph fingerprinting are now represented in the implementation; fresh CI verification is still required. |
| Experimental execution | NOT IMPLEMENTED | `run_pilot.py` explicitly refuses real pilot execution because the real experimental task executor is not implemented. |

## Non-final language that must remain

The protocol currently contains genuine unresolved-control language, including:

- `PROVENANCE REQUIRED`
- `ENVIRONMENT RECORD REQUIRED`
- `VALUES PENDING IMPLEMENTATION PIN`
- `IMPLEMENTATION VERIFICATION REQUIRED`
- `CUSTODY VERIFICATION REQUIRED`
- `RUNTIME CEILING PENDING`
- `PENDING IMPLEMENTATION VERIFICATION`
- `NOT YET ASSIGNED`

These phrases are not documentation defects by themselves. They accurately identify controls that have not yet crossed the evidence boundary. They must remain until the corresponding evidence exists.

## Audit finding

The protocol is internally consistent on the principal numeric mechanics currently implemented, but it is **not yet a freeze-ready document** because several prerequisite controls remain genuinely open:

1. hash-complete environment lock;
2. topology CI verification and final topology fingerprints/provenance evidence;
3. operational protected blinding mapping and unblinding procedure test;
4. long-term artifact retention decision/configuration;
5. exact freeze-time environment/RNG manifest;
6. runtime-ceiling characterization;
7. final analysis implementation verification;
8. operational protocol-deviation evidence;
9. real experimental task adapter.

## Freeze rule

No protocol SHA should be recorded as a freeze SHA, and no pilot authorization should be inferred from this audit. The current protocol content SHA is recorded above only as an audit reference.

## Evidence boundary

This audit establishes documentation/implementation consistency only. It does not establish PDMAL efficacy, superiority, convergence, robustness, or real-world benefit.
