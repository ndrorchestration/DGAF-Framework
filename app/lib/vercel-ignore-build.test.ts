import test from 'node:test'
import assert from 'node:assert/strict'
import { execFileSync, spawnSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
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

function createRepoWithChange(relativePath: string) {
  const repo = mkdtempSync(path.join(tmpdir(), 'dgaf-vercel-ignore-'))
  git(repo, 'init')
  git(repo, 'config', 'user.email', 'test@example.invalid')
  git(repo, 'config', 'user.name', 'DGAF test')
  writeFileSync(path.join(repo, 'README.md'), 'baseline\n')
  git(repo, 'add', 'README.md')
  git(repo, 'commit', '-m', 'baseline')
  const previous = git(repo, 'rev-parse', 'HEAD')

  const target = path.join(repo, relativePath)
  mkdirSync(path.dirname(target), { recursive: true })
  writeFileSync(target, 'changed\n')
  git(repo, 'add', relativePath)
  git(repo, 'commit', '-m', 'change')
  const current = git(repo, 'rev-parse', 'HEAD')
  return { repo, previous, current }
}

function createRepoWithRuntimeRename() {
  const repo = mkdtempSync(path.join(tmpdir(), 'dgaf-vercel-ignore-rename-'))
  git(repo, 'init')
  git(repo, 'config', 'user.email', 'test@example.invalid')
  git(repo, 'config', 'user.name', 'DGAF test')
  mkdirSync(path.join(repo, 'app'), { recursive: true })
  writeFileSync(path.join(repo, 'app/page.tsx'), 'export default function Page() { return null }\n')
  git(repo, 'add', 'app/page.tsx')
  git(repo, 'commit', '-m', 'runtime baseline')
  const previous = git(repo, 'rev-parse', 'HEAD')

  mkdirSync(path.join(repo, 'docs'), { recursive: true })
  git(repo, 'mv', 'app/page.tsx', 'docs/page.tsx')
  git(repo, 'commit', '-m', 'move runtime file to docs')
  const current = git(repo, 'rev-parse', 'HEAD')
  return { repo, previous, current }
}

function runGitMode(cwd: string, previous?: string, current?: string) {
  return spawnSync(process.execPath, [HELPER], {
    cwd,
    encoding: 'utf8',
    env: {
      ...process.env,
      VERCEL_GIT_PREVIOUS_SHA: previous ?? '',
      VERCEL_GIT_COMMIT_SHA: current ?? '',
    },
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

test('Vercel Git SHA comparison skips a proven documentation-only commit', () => {
  const fixture = createRepoWithChange('docs/status.md')
  try {
    const result = runGitMode(fixture.repo, fixture.previous, fixture.current)
    assert.equal(result.status, 0, result.stderr || result.stdout)
  } finally {
    rmSync(fixture.repo, { recursive: true, force: true })
  }
})

test('Vercel Git SHA comparison builds for a deploy-relevant commit', () => {
  const fixture = createRepoWithChange('app/page.tsx')
  try {
    const result = runGitMode(fixture.repo, fixture.previous, fixture.current)
    assert.equal(result.status, 1, result.stderr || result.stdout)
  } finally {
    rmSync(fixture.repo, { recursive: true, force: true })
  }
})

test('runtime file moved into a non-deploy surface still forces a build', () => {
  const fixture = createRepoWithRuntimeRename()
  try {
    const result = runGitMode(fixture.repo, fixture.previous, fixture.current)
    assert.equal(result.status, 1, result.stderr || result.stdout)
  } finally {
    rmSync(fixture.repo, { recursive: true, force: true })
  }
})

test('missing or invalid comparison evidence fails open toward building', () => {
  const fixture = createRepoWithChange('docs/status.md')
  try {
    assert.equal(runGitMode(fixture.repo, undefined, fixture.current).status, 1)
    assert.equal(runGitMode(fixture.repo, 'not-a-commit', fixture.current).status, 1)
  } finally {
    rmSync(fixture.repo, { recursive: true, force: true })
  }
})

test('vercel.json binds the tested ignored-build helper without re-enabling main auto-deploys', () => {
  const config = JSON.parse(readFileSync(path.join(ROOT, 'vercel.json'), 'utf8'))
  assert.equal(config.ignoreCommand, 'node scripts/vercel-ignore-build.mjs')
  assert.equal(config.git?.deploymentEnabled?.main, false)
})
