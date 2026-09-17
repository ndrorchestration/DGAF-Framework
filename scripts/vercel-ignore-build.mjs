#!/usr/bin/env node

import { spawnSync } from 'node:child_process'

const SAFE_SKIP_PREFIXES = [
  '.github/',
  'docs/',
  'schemas/',
  'tests/',
  'scripts/prepare_track_a_',
  'scripts/validate_track_a_',
]
const FORCE_BUILD_PATHS = new Set(['.github/workflows/deploy.yml'])

function canSafelySkip(changedPaths) {
  return changedPaths.length > 0 && changedPaths.every(path => {
    if (FORCE_BUILD_PATHS.has(path)) return false
    return SAFE_SKIP_PREFIXES.some(prefix => path.startsWith(prefix))
  })
}

function isAvailableCommit(sha) {
  if (!sha) return false
  return spawnSync('git', ['cat-file', '-e', `${sha}^{commit}`], { stdio: 'ignore' }).status === 0
}

function changedPathsFromGit(base, head) {
  if (!isAvailableCommit(base) || !isAvailableCommit(head)) return null

  const diff = spawnSync(
    'git',
    ['diff', '--name-only', '-z', '--no-renames', base, head, '--'],
    { encoding: 'utf8' },
  )
  if (diff.status !== 0 || diff.error) return null
  return diff.stdout.split('\0').filter(Boolean)
}

function readOption(args, name) {
  const index = args.indexOf(name)
  return index >= 0 ? args[index + 1] ?? '' : ''
}

const args = process.argv.slice(2)
const decisionMode = args.includes('--decision')
const explicitIgnoreMode = args.includes('--vercel-ignore')
const changedIndex = args.indexOf('--changed')

let changedPaths
if (changedIndex >= 0) {
  changedPaths = args.slice(changedIndex + 1)
} else {
  const base = readOption(args, '--base') || process.env.VERCEL_GIT_PREVIOUS_SHA || ''
  const head = readOption(args, '--head') || process.env.VERCEL_GIT_COMMIT_SHA || ''
  changedPaths = changedPathsFromGit(base, head)
}

const decision = changedPaths && canSafelySkip(changedPaths) ? 'SKIP' : 'BUILD'

if (decisionMode) {
  process.stdout.write(`${decision}\n`)
  process.exit(0)
}

if (explicitIgnoreMode || !decisionMode) {
  process.exit(decision === 'SKIP' ? 0 : 1)
}
