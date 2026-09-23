import fs from 'node:fs'
import path from 'node:path'
import test from 'node:test'
import assert from 'node:assert/strict'

const routePath = path.join(process.cwd(), 'pages', 'api', 'mandate.ts')
const source = fs.readFileSync(routePath, 'utf8')

test('legacy mandate API is explicitly quarantined as non-authoritative', () => {
  assert.match(source, /NON_AUTHORITATIVE_LEGACY_SURFACE/)
  assert.match(source, /status\(410\)/)
  assert.doesNotMatch(source, /mandates\.set\(/)
  assert.doesNotMatch(source, /m\.status\s*=\s*status/)
})

test('legacy mandate API cannot advertise itself as governance authority', () => {
  assert.doesNotMatch(source, /Implements Triumvirate Governance Contract/)
  assert.doesNotMatch(source, /Mandate may only be issued by Prime/)
})
