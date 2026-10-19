# SBCF matched receiver custody contract v0

Status: CANDIDATE / NOT FROZEN / OPERATOR UNASSIGNED.

This contract is a prospective dependency of the matched HTTP effect v1
candidate. It does not assign an operator or create independent validation.

The contract reuses existing DGAF custody and retention doctrine:

- transient CI artifacts are not the durable research record;
- durable evidence must have a declared archive location, identifier, retention
  period, access-control owner, and integrity record;
- retrieval and independently recomputed SHA-256 verification are required;
- private keys are excluded from the evidence packet;
- custody does not authorize analysis or adjudication.

## Exact v1 binding

The candidate is bound to matched HTTP v1 digest:

`sha256:0540ca3b11e82da563208afb4164da9b00c260779832b462dc6824e7dfebadff`

A later v1 contract change therefore requires an explicit custody-contract
revision rather than silently reusing a receipt regime against different trial
semantics.

## Receiver operator

Structural readiness requires one assigned receiver operator whose role is:

- outside implementation of every system under test;
- uncoached for the receiver-observation task;
- not same-owner automation;
- scoped to SBCF, ACS, and OpenShell matched evidence.

The current candidate leaves `operator_id = null` and status `UNASSIGNED`.

This is deliberate. ChatGPT, the implementation author, same-owner automation,
or another process controlled by the implementation operator cannot be inserted
into the fixture merely to make the structural gate green.

## Raw receiver receipt

Each raw receipt must retain raw bytes and bind at least:

- `trial_id`;
- exact effect-identity SHA-256;
- observed effect;
- raw-record SHA-256;
- byte count.

Private keys are prohibited from the receipt. Analysis/scoring fields are also
prohibited so raw observation custody does not become an analysis channel.

## Durable retention

The candidate leaves durable retention `UNRESOLVED`.

A future freeze requires non-null:

- archive location;
- archive identifier;
- explicit retention period;
- access-control owner.

The retained object must later be retrieved and its hash independently
recomputed. Merely naming an archive or documenting this policy does not close
the gate.

## Separation of authority

A structurally ready custody contract still does not authorize:

- primary analysis;
- adjudication;
- scientific-N increment;
- independent-validation claims.

Those authorities remain separate. This preserves the existing DGAF rule that
custody of evidence and authority to interpret or admit it are distinct events.

## Current blockers

The candidate is intentionally blocked on:

- `custody_contract_not_frozen`;
- `receiver_operator_unassigned`;
- `durable_retention_unfrozen`.

No operator is assigned, no archive is configured, and no real receiver receipt
has been collected.

No trial, freeze, merge, release, analysis, adjudication, scientific-N increment
or authority expansion is authorized.

`SCIENTIFIC_N_INCREMENT=0`

`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`

`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`

`HIGH_ASSURANCE=NOT_AUTHORIZED`
