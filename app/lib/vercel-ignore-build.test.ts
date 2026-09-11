import test from 'node:test'
import assert from 'node:assert/strict'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
const HELPER = path.join(ROOT, 'scripts', 'vercel-ignore-build.mjs')

test('documentation-only changes are safely ignored by automatic Vercel preview builds', () => {
  const result = spawnSync(process.execPath, [HELPER, '--changed', 'docs/experiment/example.md'], {
    cwd: ROOT,
    encoding: 'utf8',
  })

  assert.equal(result.status, 0, result.stderr || result.stdout)
})
