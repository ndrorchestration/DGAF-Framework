# PDMAL Control-Plane Evidence Trigger

This file exists only to provide an auditable, non-apparatus trigger surface for the `PDMAL Instrumentation Dry Run` workflow.

Changing this file does **not** redefine the designated scientific/runtime candidate. The workflow must resolve `candidate_sha` from `docs/experiment/NEW_CANDIDATE_MANIFEST.md`, checkout that exact commit, verify its tree identity, and record the control-plane/workflow-definition SHA separately.

Use this trigger only when a control-plane change (for example, completion-controller provenance validation) requires a fresh producer → controller evidence cycle without changing the designated candidate.

Scientific boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.
