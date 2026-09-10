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

## Permanent lock contract

`.github/workflows/npm-lockfile-validation.yml` is the permanent read-only gate. It:

1. requires `package.json` and `package-lock.json` and rejects competing npm/yarn/pnpm lockfiles;
2. executes `tests/test_npm_lockfile_contract.py` directly so the repository-level contract is itself part of the required validation path;
3. uses exact Node `24.20.0` and requires bundled npm `11.19.0`;
4. checks lockfile v3 name/version identity against `package.json`;
5. runs `npm install --package-lock-only --ignore-scripts` and requires byte-for-byte lockfile stability;
6. removes `node_modules`, performs clean `npm ci --ignore-scripts`, and builds;
7. rejects obvious secret-like material in the lockfile;
8. emits SHA-256-bound validation evidence tied to the exact workflow source/run; and
9. has only `contents: read` permission.

Any future dependency update must deliberately update the manifest/lock together and re-pass this gate. The original **NOT REPOSITORY-LOCKED** state is superseded only when this PR's final exact-head validation passes and the change is merged.

## Governance boundary

This remediation changes dependency reproducibility only. It does not change Track A preregistration, candidate/freeze identity, custody/blinding, authorization, stopping rules, empirical results, or scientific N.

**Control state remains:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.
