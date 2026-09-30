# Tektite v0.1 Release Checklist

## Scope checks

- [ ] Five public pages exist: Home, Governance Console, Evidence Ledger, Case Studies, Services/About.
- [ ] Static JSON or Markdown data seed exists.
- [ ] No live integrations are required for v0.1.
- [ ] No live executor, rollback control, mutation control, or private operations surface is exposed.

## Claim checks

- [ ] Every public claim has a source.
- [ ] Every public claim has a status.
- [ ] Every public claim has a scope.
- [ ] Every public claim has a limitation.
- [ ] Every public claim has an authorization effect.

## Boundary checks

- [ ] No page implies independent validation.
- [ ] No page implies canonical DGAF efficacy.
- [ ] No page implies High-Assurance.
- [ ] No page implies production executor status.
- [ ] No page implies live repository mutation authorization.
- [ ] No page implies rollback execution authorization.
- [ ] No page claims certification or compliance.

## Public/private checks

- [ ] No raw Notion content is exposed.
- [ ] No local file paths are exposed.
- [ ] No RDC internals are exposed.
- [ ] No credentials, tokens, or machine details are exposed.
- [ ] No personal logistics are exposed.
- [ ] No unsafe executor internals are exposed.

## Required release-state ceiling

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
LIVE_REPOSITORY_MUTATION=NOT_AUTHORIZED
ROLLBACK_EXECUTION=NOT_AUTHORIZED
PRODUCTION_EXECUTOR=NOT_ESTABLISHED
```

## Release rule

Publish only if Tektite remains a public projection and explanation layer. Do not publish if any wording or UI implies that Tektite is a governance authority, production executor, independent validator, or compliance-certified product.
