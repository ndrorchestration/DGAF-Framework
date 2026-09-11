#!/usr/bin/env node

import { spawnSync } from 'node:child_process'

const SAFE_NON_DEPLOY_PREFIXES = [
  '.github/',
  'docs/',
  'schemas/',
  'scripts/',
  'tests/',
]

function canSafelySkip(changedPaths) {
  return changedPaths.length > 0 && changedPaths.every(file =>
    SAFE_NON_DEPLOY_PREFIXES.some(prefix => file.startsWith(prefix)),
  )
}

function isAvailableCommit(sha) {
  if (!sha) return false
  return spawnSync('git', ['cat-file', '-e', `${sha}^{commit}`], { stdio: 'ignore' }).status === 0
}

function changedPathsFromVercelGit() {
  const previous = process.env.VERCEL_GIT_PREVIOUS_SHA
  const current = process.env.VERCEL_GIT_COMMIT_SHA

  if (!isAvailableCommit(previous) || !isAvailableCommit(current)) return null

  const diff = spawnSync('git', ['diff', '--name-only', '-z', previous, current, '--'], {
    encoding: 'utf8',
  })
  if (diff.status !== 0 || diff.error) return null

  return diff.stdout.split('\0').filter(Boolean)
}

const args = process.argv.slice(2)

if (args[0] === '--changed') {
  const changedPaths = args.slice(1)
  process.exit(canSafelySkip(changedPaths) ? 0 : 1)
}

const changedPaths = changedPathsFromVercelGit()
// Missing/invalid comparison evidence fails open toward building.
process.exit(changedPaths && canSafelySkip(changedPaths) ? 0 : 1)
