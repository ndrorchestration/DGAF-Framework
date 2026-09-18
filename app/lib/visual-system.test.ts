import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'

const globals = readFileSync('app/styles/globals.css', 'utf8')
const frontier = readFileSync('app/styles/decision-frontier.css', 'utf8')
const governanceMap = readFileSync('app/styles/governance-map.css', 'utf8')
const stateSpace = readFileSync('app/styles/state-space.css', 'utf8')

const REQUIRED_TOKENS = [
  '--state-established',
  '--state-frontier',
  '--state-unreachable',
  '--boundary-authorization',
  '--boundary-global',
  '--provenance',
  '--coupling-authority',
  '--coupling-dependency',
  '--evidence',
  '--consequence',
  '--execution-receipt',
  '--focus-ring',
  '--surface-raised',
  '--text-primary',
  '--type-display-size',
  '--motion-standard',
  '--ease-control',
]

test('DGAF defines meaning-bearing visual tokens above palette primitives', () => {
  for (const token of REQUIRED_TOKENS) assert.match(globals, new RegExp(token.replaceAll('-', '\\-') + ':'))
})

test('flagship Semantic Control Field surfaces consume semantic roles', () => {
  assert.match(frontier, /var\(--state-established\)/)
  assert.match(frontier, /var\(--boundary-authorization\)/)
  assert.match(frontier, /var\(--provenance\)/)
  assert.match(frontier, /var\(--execution-receipt\)/)

  assert.match(governanceMap, /var\(--boundary-global\)/)
  assert.match(governanceMap, /var\(--coupling-authority\)/)
  assert.match(governanceMap, /var\(--provenance\)/)

  assert.match(stateSpace, /var\(--state-frontier\)/)
  assert.match(stateSpace, /var\(--state-unreachable\)/)
})

test('non-color structural semantics remain present', () => {
  assert.match(frontier, /repeating-linear-gradient/)
  assert.match(governanceMap, /border-style:double/)
  assert.match(governanceMap, /border-style:dashed/)
  assert.match(stateSpace, /border-style: dashed/)
  assert.match(stateSpace, /border-style: dotted/)
  assert.match(globals, /data-tone="warning".*status-dot.*rotate\(45deg\)/s)
  assert.match(globals, /data-tone="danger".*background:transparent/s)
  assert.match(globals, /data-tone="neutral".*border-style:dotted/s)
})

test('reduced-motion equivalence remains explicit across semantic views', () => {
  for (const css of [frontier, governanceMap, stateSpace]) assert.match(css, /prefers-reduced-motion: ?reduce/)
})
