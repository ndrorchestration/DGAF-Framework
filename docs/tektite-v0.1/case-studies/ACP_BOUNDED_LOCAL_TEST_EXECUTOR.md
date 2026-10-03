# ACP bounded local-test executor

## What is established

ACP PR #156 establishes the mutation executor only for the tested `BOUNDED_LOCAL_TEST` disposable-repository scope. ACP PR #159 adds durable local mutation lineage for that same bounded scope.

The tested path requires explicit experimental opt-in, an exact repository-root allowlist, the disposable-test marker, bounded mutation capabilities, current authorization/journal/evidence/postcondition controls, and fresh adjudication for consequential follow-on effects.

## What is not established

This evidence does not establish:

- mutation authority for real projects;
- rollback execution;
- production execution;
- trusted process identity;
- hostile-local-actor or peer-process tamper resistance;
- elimination of all final-path TOCTOU risk;
- distributed/global effect lineage;
- independent validation;
- High-Assurance.

## Authority boundary

A terminal execution record is evidence of the bounded event, not permission for another event. The receipt authority effect is `NONE`; consequential follow-on work requires fresh adjudication and fresh authorization.

## Public sources

- [ACP PR #156](https://github.com/ndrorchestration/agent-control-plane/pull/156)
- [ACP PR #159](https://github.com/ndrorchestration/agent-control-plane/pull/159)
- [DGAF PR #1257](https://github.com/ndrorchestration/DGAF-Framework/pull/1257)
- [Tektite PR #1270](https://github.com/ndrorchestration/DGAF-Framework/pull/1270)
