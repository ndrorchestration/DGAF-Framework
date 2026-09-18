import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'

const overview = readFileSync('app/components/overview-view.tsx', 'utf8')
const globals = readFileSync('app/styles/globals.css', 'utf8')

test('external summary explains product value in plain operational language', () => {
  assert.match(overview, /EXTERNAL SUMMARY/)
  assert.match(overview, /What DGAF is for/)
  assert.match(overview, /Govern actions/)
  assert.match(overview, /Bind evidence/)
  assert.match(overview, /Expose limits/)
})

test('external summary keeps canonical efficacy claim ceiling visible', () => {
  assert.match(overview, /Current claim ceiling/)
  assert.match(overview, /TRUTH_BOUNDARY\.efficacy/)
  assert.match(overview, /not presented as established canonical efficacy/)
})

test('public summary remains responsive rather than hidden', () => {
  assert.match(globals, /\.public-summary \{/)
  assert.match(globals, /@media \(max-width: 980px\)[\s\S]*\.public-summary[\s\S]*grid-template-columns: 1fr/)
  assert.doesNotMatch(globals, /\.public-summary\s*\{[^}]*display:\s*none/)
})

test('claim ceiling has structural boundary treatment', () => {
  assert.match(globals, /\.public-claim-ceiling[\s\S]*border-left: 3px solid var\(--boundary-authorization\)/)
  assert.match(globals, /background: var\(--boundary-authorization-soft\)/)
})
