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

The artifact-retention workflow then downloaded that exact artifact, independently rechecked the source/run/package/lock identities and SHA-256 values, and committed the exact retained lockfile bytes to the PR branch. The write-capable retention workflow was removed immediately afterward and is not part of the permanent repository design.

## Permanent lock contract

`.github/workflows/npm-lockfile-validation.yml` is the permanent read-only gate. It:

1. requires `package.json` and `package-lock.json` and rejects competing npm/yarn/pnpm lockfiles;
2. uses exact Node `24.20.0` and requires bundled npm `11.19.0`;
3. checks lockfile v3 name/version identity against `package.json`;
4. runs `npm install --package-lock-only --ignore-scripts` and requires byte-for-byte lockfile stability;
5. removes `node_modules`, performs clean `npm ci --ignore-scripts`, and builds;
6. rejects obvious secret-like material in the lockfile;
7. emits SHA-256-bound validation evidence tied to the exact workflow source/run; and
8. has only `contents: read` permission.

Any future dependency update must deliberately update the manifest/lock together and re-pass this gate. The original **NOT REPOSITORY-LOCKED** state is superseded only when this PR's final exact-head validation passes and the change is merged.

## Governance boundary

This remediation changes dependency reproducibility only. It does not change Track A preregistration, candidate/freeze identity, custody/blinding, authorization, stopping rules, empirical results, or scientific N.

**Control state remains:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.


## Reviewed update lifecycle — 2026-09-10

The bootstrap lock digest above remains historical evidence for commit
`c147df1ac226b641e5a85cd08fb45e9a838ac825`. Contract tests verify that immutable
Git object rather than requiring every later lockfile to retain its bytes.
The npm workflow now explicitly runs the standard-library unittest contract
suite, with full checkout history so missing provenance fails visibly.
Current manifest/lock consistency, clean npm ci/build, and exact-source
validation receipts remain required for every reviewed update.

The PostCSS manifest and lock changes are taken byte-for-byte from Dependabot
PR #584, head `0c5ec61212a255366b5f359f32922388676087f5` (8.4.31 to 8.5.23).
This change must receive fresh CI with the repaired contract; earlier PR checks
are not transferred to this combined change. Historical bootstrap provenance
is preserved and current dependency versions may evolve through reviewed PRs.

Local contract checks accept both consistent original and updated pairs and
reject a mismatched manifest/lock pair. This is structural engineering evidence,
not empirical efficacy, freeze, custody acceptance, or collection authorization.
