import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'

const globals = readFileSync('app/styles/globals.css', 'utf8')
const frontier = readFileSync('app/styles/decision-frontier.css', 'utf8')
const governanceMap = readFileSync('app/styles/governance-map.css', 'utf8')
const stateSpace = readFileSync('app/styles/state-space.css', 'utf8')
const overview = readFileSync('app/components/overview-view.tsx', 'utf8')
const appShell = readFileSync('app/components/app-shell.tsx', 'utf8')
const evidenceView = readFileSync('app/components/evidence-view.tsx', 'utf8')
const dashboardPage = readFileSync('app/page.tsx', 'utf8')

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
  assert.match(globals, /data-tone="warning"[\s\S]*status-dot[\s\S]*rotate\(45deg\)/)
  assert.match(globals, /data-tone="danger"[\s\S]*background:transparent/)
  assert.match(globals, /data-tone="neutral"[\s\S]*border-style:dotted/)
})

test('reduced-motion equivalence remains explicit across semantic views', () => {
  for (const css of [frontier, governanceMap, stateSpace]) assert.match(css, /prefers-reduced-motion: ?reduce/)
})


test('forced colors preserve structural semantics and focus visibility', () => {
  assert.match(globals, /@media \(forced-colors: active\)/)
  assert.match(globals, /outline: 2px solid Highlight/)
  assert.match(globals, /truth-boundary[\s\S]*border-left: 3px solid CanvasText/)
  assert.match(globals, /status-chip\[data-tone="warning"\][\s\S]*status-dot/)
})


test('Overview hero remains a semantic control field rather than decorative-only futurism', () => {
  assert.match(overview, /SEMANTIC CONTROL FIELD/)
  assert.match(overview, /CURRENT STATE/)
  assert.match(overview, /AUTHORIZATION BOUNDARY/)
  assert.match(overview, /NEXT ADMISSIBLE/)
  assert.doesNotMatch(overview, /hero-orbit/)
})


test('mobile does not hide the semantic hero field', () => {
  assert.doesNotMatch(globals, /\.hero-field\{display:none\}/)
  assert.match(globals, /\.hero-field\{width:100%;justify-self:stretch/)
})


test('operator journey verifies evidence before governance', () => {
  const evidenceNav = appShell.indexOf("id: 'evidence'")
  const governanceNav = appShell.indexOf("id: 'governance'")

  assert.ok(evidenceNav >= 0, 'Evidence navigation entry must exist')
  assert.ok(governanceNav >= 0, 'Governance navigation entry must exist')
  assert.ok(evidenceNav < governanceNav, 'Evidence must appear before Governance in the primary operator journey')
  assert.match(
    overview,
    /className="button primary" onClick=\{\(\) => onNavigate\('evidence'\)\}>Inspect evidence/,
  )
})


test('Evidence view exposes provenance boundaries before governance handoff', () => {
  assert.match(evidenceView, /GOVERNANCE_STAGES/)
  assert.match(evidenceView, /EVIDENCE SPINE/)
  assert.match(evidenceView, /EVIDENCE BOUNDARY/)
  assert.match(evidenceView, /DOES NOT ESTABLISH/)
  assert.match(evidenceView, /establishes—or still leaves open/)
  assert.doesNotMatch(evidenceView, /each accepted state establishes/)
  assert.match(
    evidenceView,
    /onClick=\{\(\) => onNavigate\('governance'\)\}>Inspect governance context/,
  )
  assert.match(dashboardPage, /<EvidenceView onNavigate=\{setView\} \/>/)
})
