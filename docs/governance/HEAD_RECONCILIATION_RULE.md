# Control-State HEAD Reconciliation Rule

`last_reconciled_main_tip` records the main-branch commit whose control state was last reconciled; it is not a self-referential assertion that the field must equal the commit containing the field.

For a control-state change committed to `main`, the new commit should record the immediately preceding main tip as the reconciled source. A post-merge validation may therefore compare `last_reconciled_main_tip` with the push event's `before` SHA. A workflow validating an unchanged control-state commit may instead compare the recorded tip with the commit being validated.

The validator must never require a control-state file to contain its own commit SHA, because that creates an impossible self-referential invariant.
