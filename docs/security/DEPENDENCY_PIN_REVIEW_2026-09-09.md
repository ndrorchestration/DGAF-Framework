# Mutable Dependency Pin Review — 2026-09-09

**Scope:** integrity/reproducibility remediation for issue #570 only.

## Reviewed pins

| Surface | Previous | Reviewed exact pin | Rationale |
|---|---|---|---|
| Vercel CLI in production and preview workflows | `vercel@latest` | `vercel@59.11.7` | Replaces a moving npm tag with one exact reviewed release used by both deployment paths. |
| HTTPX in deployment verification and regression workflow | unpinned `httpx` | `httpx==0.28.1` | Uses the current stable HTTPX release rather than the 1.0 development series. |
| Live regression script import fallback | dynamic `pip install httpx` | removed | Missing dependencies now fail closed instead of mutating the runtime environment. |

The Vercel workflow install verifies the installed CLI reports the expected exact version before any deployment credential or deployment action is used.

## NPM transitive lock establishment

The root npm dependency graph is now represented by a real npm-generated `package-lock.json` rather than hand-authored transitive versions or inferred integrity values.

Bootstrap provenance:

- bootstrap source commit: `62a0c35db29420075e331d501fa281054ab63230`
- GitHub Actions run: `34427479869`
- retained artifact ID: `10133208552`
- artifact digest reported by GitHub: `sha256:e4120448b7cc85e95dd84dda03bdfd0d9444df09265e9616d9c4fe1fe97763d2`
- `package.json` SHA-256: `032252ce8dd07dba9f1ebb583e091fe41f70c07633dc1380c72339b6408a6204`
- retained `package-lock.json` SHA-256: `d4af9d2195f8b23975ce9389754e74ec4415c087ea633afc9a6b5146743503f6`
- Node: `v24.20.0`
- npm: `11.19.0`
- generation command: `npm install --package-lock-only --ignore-scripts --no-audit --no-fund`
- bootstrap validation: clean `npm ci --ignore-scripts --no-audit --no-fund` followed by `npm run build`
- bootstrap result: `PASS_NONEMPIRICAL_REPRODUCIBILITY_EVIDENCE`

The bootstrap lock digest above identifies the original retained bootstrap artifact only. It is historical provenance and does not constrain the SHA-256 of future reviewed lockfile updates. Each later dependency change is expected to produce new lockfile bytes and must instead be accepted only by the permanent validation gate on that exact reviewed source state.

The artifact-retention workflow then downloaded that exact artifact, independently rechecked the source/run/package/lock identities and SHA-256 values, and committed the exact retained lockfile bytes to the PR branch. The write-capable retention workflow was removed immediately afterward and is not part of the permanent repository design.

## Direct dependency scope remediation

PR #584 was presented as a PostCSS update, but its rebased exact diff also changed the root `next` dependency from `15.5.24` to `16.3.4`. That broader direct major-version change was not represented by the PR title/body. The rebased exact head `ae787820b6b6ad914df15401a6dad681e6d16e93` nevertheless passed all 18 returned workflows, including NPM Lockfile Validation, Governance CI, PPTL CI, DGAF Regression Suite, and PDMAL Pre-Freeze Runner Validation, before merge commit `0dcfe07d160eb116cfd9ef8f4d7faf17d6a51fcd`.

Because PRE-FREEZE allows reviewed implementation maintenance but hidden dependency scope is not acceptable provenance, the current direct dependency surface is now declared separately in `docs/security/npm-direct-dependency-state.json`. The repository contract requires that declaration to match `package.json` exactly. A future direct dependency or devDependency change therefore fails the permanent npm gate unless the dedicated declaration is deliberately updated in the same reviewed source state. The declaration SHA-256 is included in emitted npm validation evidence.

This remediation accepts the current Next.js/PostCSS source state as a pre-freeze implementation state after exact-head validation; it does not treat the earlier narrow PR description as sufficient review evidence, and it does not create scientific authorization.

## Permanent lock contract

`.github/workflows/npm-lockfile-validation.yml` is the permanent read-only gate. It:

1. requires `package.json`, `package-lock.json`, and the direct-dependency declaration and rejects competing npm/yarn/pnpm lockfiles;
2. executes `tests/test_npm_lockfile_contract.py` directly so the repository-level contract is itself part of the required validation path;
3. requires the declared direct dependency and devDependency maps to match `package.json` exactly;
4. uses exact Node `24.20.0` and requires bundled npm `11.19.0`;
5. checks lockfile v3 name/version identity against `package.json`;
6. runs `npm install --package-lock-only --ignore-scripts` and requires byte-for-byte lockfile stability;
7. removes `node_modules`, performs clean `npm ci --ignore-scripts`, and builds;
8. rejects obvious secret-like material in the lockfile;
9. emits SHA-256-bound validation evidence for the manifest, lockfile, and direct-dependency declaration tied to the exact workflow source/run; and
10. has only `contents: read` permission.

Any future dependency update must deliberately update the manifest/lock together, update the direct-dependency declaration whenever the root dependency surface changes, and re-pass this gate.

## Governance boundary

This remediation changes dependency reproducibility and dependency-scope disclosure only. It does not change Track A preregistration, candidate/freeze identity, custody/blinding, authorization, stopping rules, empirical results, or scientific N.

**Control state remains:** PRE-FREEZE / FAIL-CLOSED / SUCCESSOR COLLECTION NOT AUTHORIZED / N=0.
