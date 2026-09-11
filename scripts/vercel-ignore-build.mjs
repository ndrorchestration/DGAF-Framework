#!/usr/bin/env node

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

const args = process.argv.slice(2)

if (args[0] === '--changed') {
  const changedPaths = args.slice(1)
  process.exit(canSafelySkip(changedPaths) ? 0 : 1)
}

// Until a trustworthy Git comparison is available, fail open toward building.
process.exit(1)
