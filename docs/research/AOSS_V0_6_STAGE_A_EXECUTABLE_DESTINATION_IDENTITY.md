# AOSS v0.6 Stage-A executable/destination identity boundary

This is a proposed, non-collecting identity contract for Issue #901. It records
exact provenance for the ACP source module at the frozen source commit and
explicitly labels destination and attempt identifiers as synthetic fixtures.

The contract does **not** accept a DGAF source-driver executable or collector,
does not import or execute ACP, and does not establish collection readiness.
The fixture identities are test apparatus only and must not be relabeled as
study destinations, attempts, episodes, or outcomes.

The exact source-module evidence is:

- repository: `ndrorchestration/agent-control-plane`;
- commit: `dbab7c1afafec524ce7c18157de2089cafe79c87`;
- path: `src/agent_control_plane/core.py`;
- Git blob identity: `1341df7296a426b336b76ac6b1e4df67611ec931`.

The next separate gate remains an independently reviewed DGAF source-driver
executable and accepted destination/attempt binding. Until that gate is
accepted, `COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED`.

State boundary:

- `OUTCOME_COLLECTION_AUTHORIZED=TRUE` remains bounded and unchanged;
- `SCIENTIFIC_N_INCREMENT=0`;
- canonical DGAF efficacy and independent validation remain
  `NOT_ESTABLISHED`;
- High-Assurance remains `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`;
- no ACP episodes, outcomes, or analysis are generated.
