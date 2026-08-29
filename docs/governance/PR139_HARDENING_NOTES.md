# PR #139 Hardening Notes

## Closed engineering findings

### Active-resource release
Escalated tasks now release their active concurrency slot immediately. This applies to recursion-depth refusal, lineage concurrency refusal, TGL escalation, explicit veto, and budget-overrun escalation.

### TGL boundary
TGL evaluation is callable only from `EVALUATING`. Terminal TGL failure maps to control-plane escalation; the control plane does not reinterpret a terminal governance result as permission to continue recursion.

### CI completeness
The v1 control-plane CI lane executes core, TGL integration, and adversarial contract suites. Missing test files are treated as repository errors rather than silently skipped.

## Remaining verification-only items

These cannot be truthfully closed by source inspection alone:

- GitHub Actions execution on the exact candidate head;
- observed test results and logs;
- independent adversarial review disposition;
- current-main → production exact deployment binding under Issue #137.

## Boundary
No experimental execution or PDMAL state transition is permitted by this document.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**
