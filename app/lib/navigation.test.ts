import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'

const shell = readFileSync(new URL('../components/app-shell.tsx', import.meta.url), 'utf8')

function position(label: string) {
  const index = shell.indexOf(label)
  assert.notEqual(index, -1, `expected shell to contain ${label}`)
  return index
}

test('primary navigation follows understand verify inspect operate journey', () => {
  const understand = position("label: 'UNDERSTAND'")
  const verify = position("label: 'VERIFY'")
  const inspect = position("label: 'INSPECT'")
  const operate = position("label: 'OPERATE'")

  assert.ok(understand < verify)
  assert.ok(verify < inspect)
  assert.ok(inspect < operate)

  assert.ok(position("label: 'Overview'") < position("label: 'Evidence & Research'"))
  assert.ok(position("label: 'Evidence & Research'") < position("label: 'Agents & Formations'"))
  assert.ok(position("label: 'Agents & Formations'") < position("label: 'Control Room'"))
})

test('control room is framed as an operator surface rather than generic telemetry', () => {
  assert.match(shell, /label: 'Control Room', sub: 'Operator actions & runtime'/)
})

test('mobile navigation exposes expansion state and controlled region', () => {
  assert.match(shell, /id="primary-navigation"/)
  assert.match(shell, /aria-controls="primary-navigation"/)
  assert.match(shell, /aria-expanded=\{mobileOpen\}/)
  assert.match(shell, /aria-label=\{mobileOpen \? 'Close navigation' : 'Open navigation'\}/)
})
