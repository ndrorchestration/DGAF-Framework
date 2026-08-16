# Quality Next Actions — 2026-08-16

## Current order

1. **#58 Registry summary claim cleanup**
   - Correct the two registry summaries identified by the deterministic claim audit.
   - Re-run claim hygiene and reconcile the claim index.

2. **#54 Toolchain determinism**
   - `requirements-ci.txt` pins the evidence-gate tool versions observed in successful CI.
   - Next step: wire the pinned file into every relevant Python evidence workflow and record the resulting lock provenance.

3. **#47 Formatting/type debt**
   - Mechanical Black/isort remediation first.
   - Then fix the 11 concrete mypy findings with focused tests where semantics could change.

4. **#51 Runtime support policy**
   - Decide release-level support versus CI validation for Python 3.9–3.12.
   - Document deprecation/removal policy and dependency constraints.

5. **Independent evidence gates**
   - Live controlled staging execution.
   - Sentinel → dashboard end-to-end trace.
   - Real-workload efficacy evaluation.

## Evidence rule

Do not close a gate merely because adjacent infrastructure succeeds. Every closure requires the exact evidence condition recorded in the canonical claim/evidence index.
