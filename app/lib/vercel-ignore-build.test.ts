import test from 'node:test'
import assert from 'node:assert/strict'
import { execFileSync, spawnSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
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

function git(cwd: string, ...args: string[]) {
  return execFileSync('git', args, { cwd, encoding: 'utf8' }).trim()
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

test('Vercel Git SHA comparison skips a proven documentation-only commit', () => {
  const repo = mkdtempSync(path.join(tmpdir(), 'dgaf-vercel-ignore-'))
  try {
    git(repo, 'init')
    git(repo, 'config', 'user.email', 'test@example.invalid')
    git(repo, 'config', 'user.name', 'DGAF test')
    writeFileSync(path.join(repo, 'README.md'), 'baseline\n')
    git(repo, 'add', 'README.md')
    git(repo, 'commit', '-m', 'baseline')
    const previous = git(repo, 'rev-parse', 'HEAD')

    mkdirSync(path.join(repo, 'docs'), { recursive: true })
    writeFileSync(path.join(repo, 'docs', 'status.md'), 'presentation-only update\n')
    git(repo, 'add', 'docs/status.md')
    git(repo, 'commit', '-m', 'docs update')
    const current = git(repo, 'rev-parse', 'HEAD')

    const result = spawnSync(process.execPath, [HELPER], {
      cwd: repo,
      encoding: 'utf8',
      env: {
        ...process.env,
        VERCEL_GIT_PREVIOUS_SHA: previous,
        VERCEL_GIT_COMMIT_SHA: current,
      },
    })

    assert.equal(result.status, 0, result.stderr || result.stdout)
  } finally {
    rmSync(repo, { recursive: true, force: true })
  }
})
