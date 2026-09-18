import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'

const globals = readFileSync('app/styles/globals.css', 'utf8')
const frontier = readFileSync('app/styles/decision-frontier.css', 'utf8')
const governance = readFileSync('app/styles/governance-map.css', 'utf8')
const stateSpace = readFileSync('app/styles/state-space.css', 'utf8')

test('motion grammar exposes bounded semantic timing tokens', () => {
  for (const token of ['--motion-fast', '--motion-standard', '--motion-slow', '--motion-flow', '--motion-focus', '--ease-control', '--ease-emphasis']) {
    assert.match(globals, new RegExp(token.replaceAll('-', '\\-') + ':'))
  }
})

test('causal motion is limited to provenance/frontier/focus interactions', () => {
  assert.match(globals, /@keyframes dgaf-provenance-flow/)
  assert.match(globals, /@keyframes dgaf-frontier-breathe/)
  assert.match(globals, /hero-filament::before[\s\S]*dgaf-provenance-flow/)
  assert.match(governance, /governance-filament[\s\S]*dgaf-provenance-flow/)
  assert.match(globals, /hero-state-frontier[\s\S]*dgaf-frontier-breathe/)
})

test('reduced-motion removes semantic animation without removing structural cues', () => {
  for (const css of [globals, frontier, governance, stateSpace]) {
    assert.match(css, /prefers-reduced-motion: reduce/)
    assert.match(css, /animation: none !important|animation:none!important/)
  }
  assert.match(frontier, /border-top: 1px dashed|border-style: dashed/)
  assert.match(governance, /border-style:double/)
  assert.match(stateSpace, /border-style: dotted/)
})

test('interaction motion never encodes authorization state by itself', () => {
  assert.doesNotMatch(globals, /animation-name:\s*(authorized|authorization|pass|approved)/i)
  assert.doesNotMatch(frontier, /animation-name:\s*(authorized|authorization|pass|approved)/i)
  assert.doesNotMatch(governance, /animation-name:\s*(authorized|authorization|pass|approved)/i)
})
