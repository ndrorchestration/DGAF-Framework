import test from 'node:test'
import assert from 'node:assert/strict'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
const HELPER = path.join(ROOT, 'scripts', 'vercel-ignore-build.mjs')

function runChanged(paths: string[]) {
  return spawnSync(process.execPath, [HELPER, '--changed', ...paths], {
    cwd: ROOT,
    encoding: 'utf8',
  })
}

test('documentation-only changes are safely ignored by automatic Vercel preview builds', () => {
  const result = runChanged(['docs/experiment/example.md'])
  assert.equal(result.status, 0, result.stderr || result.stdout)
})

test('known non-deploy governance and tooling surfaces can share one skipped preview', () => {
  const result = runChanged([
    '.github/workflows/example.yml',
    'scripts/validate_example.py',
    'schemas/example.schema.json',
    'tests/test_example.py',
  ])
  assert.equal(result.status, 0, result.stderr || result.stdout)
})

test('a mixed change set builds when any deploy-relevant surface is present', () => {
  const result = runChanged(['docs/experiment/example.md', 'app/page.tsx'])
  assert.equal(result.status, 1, result.stderr || result.stdout)
})

test('an unknown path builds rather than being optimistically skipped', () => {
  const result = runChanged(['new-runtime-surface/example.ts'])
  assert.equal(result.status, 1, result.stderr || result.stdout)
})
