#!/usr/bin/env node

const args = process.argv.slice(2)

if (args[0] === '--changed') {
  const changedPaths = args.slice(1)
  const docsOnly = changedPaths.length > 0 && changedPaths.every(file => file.startsWith('docs/'))
  process.exit(docsOnly ? 0 : 1)
}

// Until a trustworthy Git comparison is available, fail open toward building.
process.exit(1)
