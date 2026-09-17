import assert from 'node:assert/strict'
import { execFileSync, spawnSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import path from 'node:path'
import test from 'node:test'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
const HELPER = path.join(ROOT, 'scripts', 'vercel-ignore-build.mjs')

function runDecision(paths: string[]) {
  return spawnSync(process.execPath, [HELPER, '--decision', '--changed', ...paths], {
    cwd: ROOT,
    encoding: 'utf8',
  })
}

function runVercelIgnore(paths: string[]) {
  return spawnSync(process.execPath, [HELPER, '--vercel-ignore', '--changed', ...paths], {
    cwd: ROOT,
    encoding: 'utf8',
  })
}

function git(cwd: string, ...args: string[]) {
  return execFileSync('git', args, { cwd, encoding: 'utf8' }).trim()
}

function createRepoWithChange(relativePath: string) {
  const repo = mkdtempSync(path.join(tmpdir(), 'dgaf-vercel-quota-'))
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
  const repo = mkdtempSync(path.join(tmpdir(), 'dgaf-vercel-quota-rename-'))
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
  git(repo, 'commit', '-m', 'move runtime file')
  const current = git(repo, 'rev-parse', 'HEAD')
  return { repo, previous, current }
}

function runGitDecision(cwd: string, previous?: string, current?: string) {
  const args = [HELPER, '--decision', '--base', previous ?? '', '--head', current ?? '']
  return spawnSync(process.execPath, args, { cwd, encoding: 'utf8' })
}

test('only proven inert surfaces are classified SKIP', () => {
  for (const changed of [
    ['docs/experiment/status.md'],
    ['schemas/example.schema.json'],
    ['tests/test_example.py'],
    ['.github/workflows/claim-hygiene.yml'],
    ['scripts/prepare_track_a_epoch_002_precollection_preflight.py'],
    ['scripts/validate_track_a_epoch_002_collection_authorization.py'],
    ['docs/status.md', 'schemas/example.json', 'tests/test_example.py'],
  ]) {
    const result = runDecision(changed)
    assert.equal(result.status, 0, result.stderr || result.stdout)
    assert.equal(result.stdout.trim(), 'SKIP')
  }
})

test('runtime, unclassified scripts, deploy control, config, unknown, mixed, and empty changes classify BUILD', () => {
  const cases = [
    ['scripts/validate_example.py'],
    ['scripts/vercel-ignore-build.mjs'],
    ['.github/workflows/deploy.yml'],
    ['app/page.tsx'],
    ['api/health.py'],
    ['public/logo.svg'],
    ['vercel.json'],
    ['package.json'],
    ['package-lock.json'],
    ['next.config.ts'],
    ['tsconfig.json'],
    ['new-runtime-surface/example.ts'],
    ['docs/status.md', 'app/page.tsx'],
    [],
  ]

  for (const changed of cases) {
    const result = runDecision(changed)
    assert.equal(result.status, 0, result.stderr || result.stdout)
    assert.equal(result.stdout.trim(), 'BUILD')
  }
})

test('Vercel ignore exit semantics are SKIP=0 and BUILD=1', () => {
  assert.equal(runVercelIgnore(['docs/status.md']).status, 0)
  assert.equal(runVercelIgnore(['app/page.tsx']).status, 1)
})

test('Git comparison classifies a documentation-only commit SKIP', () => {
  const fixture = createRepoWithChange('docs/status.md')
  try {
    const result = runGitDecision(fixture.repo, fixture.previous, fixture.current)
    assert.equal(result.status, 0, result.stderr || result.stdout)
    assert.equal(result.stdout.trim(), 'SKIP')
  } finally {
    rmSync(fixture.repo, { recursive: true, force: true })
  }
})

test('Git comparison fails closed to BUILD for invalid evidence', () => {
  const fixture = createRepoWithChange('docs/status.md')
  try {
    assert.equal(runGitDecision(fixture.repo, undefined, fixture.current).stdout.trim(), 'BUILD')
    assert.equal(runGitDecision(fixture.repo, 'not-a-commit', fixture.current).stdout.trim(), 'BUILD')
  } finally {
    rmSync(fixture.repo, { recursive: true, force: true })
  }
})

test('runtime rename into an inert surface still classifies BUILD', () => {
  const fixture = createRepoWithRuntimeRename()
  try {
    const result = runGitDecision(fixture.repo, fixture.previous, fixture.current)
    assert.equal(result.status, 0, result.stderr || result.stdout)
    assert.equal(result.stdout.trim(), 'BUILD')
  } finally {
    rmSync(fixture.repo, { recursive: true, force: true })
  }
})

test('Vercel and GitHub deploy paths are wired to the same classifier', () => {
  const config = JSON.parse(readFileSync(path.join(ROOT, 'vercel.json'), 'utf8'))
  assert.equal(config.ignoreCommand, 'node scripts/vercel-ignore-build.mjs')
  assert.equal(config.git?.deploymentEnabled?.main, false)

  const workflow = readFileSync(path.join(ROOT, '.github/workflows/deploy.yml'), 'utf8')
  assert.match(workflow, /name: Classify deploy relevance/)
  assert.match(workflow, /node scripts\/vercel-ignore-build\.mjs --decision --base/)
  assert.match(workflow, /needs: classify/)
  assert.match(workflow, /needs\.classify\.outputs\.should_deploy == 'true'/)
})