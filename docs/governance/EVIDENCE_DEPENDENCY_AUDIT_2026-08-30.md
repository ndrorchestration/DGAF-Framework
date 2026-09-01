# Evidence Dependency Audit — Reconciled 2026-09-01

**Status:** CURRENT / NON-AUTHORIZING

## Canonical identity graph

| Node | Identity / role |
|---|---|
| Corrected apparatus source | `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` |
| Mainline runtime candidate | `92ff830b1c67413df745e37087e6447c9c251b9a` |
| Mainline runtime candidate tree | `73cf3adcc2fd600eda83b818a681c83a7bb1c2ae` |
| Mainline production deployment | `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` |
| Latest completion candidate | `562753b3053b3566b0fcad1b0b1df151d7de119a` |
| Latest completion branch | `completion/2026-09-01-exact-candidate` |
| Current main documentation lineage | `main` — resolve live rather than embedding a mutable tip |
| Prior production/runtime evidence source | `303f4424d2198f0d0cf76305c589263dd1e417dc` |
| Prior pre-remediation candidate | `c6157158bf0ee4840e99a381a4b99bd2febe2302` |
| Superseded post-#151 candidate | `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37` |

## Dependency conditions

Current-candidate evidence may close a predicate only when all upstream identities required by that predicate resolve to the same current candidate cycle.

Historical evidence remains valid only at its exact candidate/source/deployment/run/artifact boundary.

The mainline runtime candidate `92ff830b…` and the completion candidate `562753b…` are distinct identities. The scoped P9 result for `562753b…` does not qualify `92ff830b…`.

No evidence is transferred merely by ancestry, shared repository, deployment URL, workflow name, documentation lineage, or apparent behavioral equivalence.

## Gate dependencies

P1 → exact selected candidate/source/tree/deployment binding.

P2/P6a → require exact candidate deployment and fresh runtime execution when the selected candidate changes.

P3 → requires current selected-candidate artifact execution and schema/integrity evidence.

P4 → requires current operational custody and blinding separation.

P5 → requires current environment/topology/RNG/provenance evidence.

P6 → requires durable archive/retrieval/hash evidence for current selected-candidate artifacts.

P7 → requires exact scientific binding to the selected candidate/protocol/analysis/final freeze identity.

P8 → requires selected-candidate analysis/runner/protocol binding and applicable predicate closure.

P9 → requires independent verification of the complete selected-candidate evidence graph. Scoped run `33567199896` is a verified P9 component for completion candidate `562753b…`.

Freeze → requires current selected-candidate P1–P8 plus broader P9 closure and independent freeze verification.

Authorization → separate governance transition after freeze verification.

N>0 → authorized execution only.

## Non-equivalence invariants

`apparatus SHA != candidate SHA != designation/control commit != documentation lineage != workflow head SHA != deployment ID != freeze SHA`

`implemented != wired != candidate-bound != verified != authorized`

`historical evidence != current evidence`

`deployment READY != runtime verified`

`scoped P9 PASS != full P9 closure`

`P9 evidence for candidate A != P9 evidence for candidate B`

## Latest scoped P9 evidence

Run `33567199896` successfully verified candidate `562753b3053b3566b0fcad1b0b1df151d7de119a` by:

- checking exact checkout identity (`HEAD == GITHUB_SHA`);
- independently canonicalizing the deterministic case with `jq -S -c`;
- independently hashing with `sha256sum` and matching the DGAF/Python digest;
- passing the authority identity regression (`4 passed`);
- uploading evidence artifact `9823570326` with ZIP digest `sha256:8e3435a3af0dc5de7376d970b9f1665a18db8ff04b26a2c0eaae8acf8b095d85`.

This resolves the previously identified canonicalization-method and authority-identity checks at that completion-candidate boundary, but does not establish all P1–P8 evidence for the same candidate and therefore does not create a freeze or authorization state.

## Current disposition

- Mainline runtime predicates P2/P6a are verified for `92ff830b…` / `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc`.
- P3/P4/P5/P6 remain open for the selected pilot candidate.
- P7 is adopted with final exact binding open.
- P8 remains open/fail-closed.
- P9 has a scoped PASS for `562753b…`; broader closure is open.
- Freeze is not established.
- Pilot authorization is not granted.
- Empirical N remains 0.

**PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0**

## Cross-references

- `../CURRENT_STATE.md`
- `P1_TO_P9_EVIDENCE_MATRIX.md`
- `P8_VERIFICATION_CHECKLIST.md`
- `P9_LATEST_RECONCILIATION_2026-09-01.md`
- `../CLAIM_EVIDENCE_INDEX.md`
- `../evidence/PDMAL_EVIDENCE_INDEX.md`
