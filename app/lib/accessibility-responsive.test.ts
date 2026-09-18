import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'

const shell = readFileSync('app/components/app-shell.tsx', 'utf8')
const globals = readFileSync('app/styles/globals.css', 'utf8')

test('shell provides direct keyboard access to main content', () => {
  assert.match(shell, /className="skip-link" href="#main-content"/)
  assert.match(shell, /id="main-content"[\s\S]*tabIndex=\{-1\}/)
  assert.match(globals, /\.skip-link:focus[\s\S]*translateY\(0\)/)
})

test('mobile navigation exposes state and keyboard dismissal', () => {
  assert.match(shell, /aria-expanded=\{mobileOpen\}/)
  assert.match(shell, /aria-controls="primary-navigation"/)
  assert.match(shell, /event\.key !== 'Escape'/)
  assert.match(shell, /menuButtonRef\.current\?\.focus\(\)/)
  assert.match(shell, /querySelector<HTMLButtonElement>\('button'\)\?\.focus\(\)/)
})

test('interactive controls retain minimum touch target sizing', () => {
  assert.match(globals, /\.nav-item,[\s\S]*\.severity-filter button[\s\S]*min-height: 44px/)
  assert.match(globals, /@media \(max-width: 760px\)[\s\S]*\.nav-item[\s\S]*min-height: 48px/)
})

test('technical identities can wrap on narrow surfaces', () => {
  assert.match(globals, /\.source-stamp,[\s\S]*\.tool-contract strong[\s\S]*overflow-wrap: anywhere/)
  assert.match(globals, /word-break: break-word/)
})

test('forced colors and reduced motion preserve accessibility affordances', () => {
  assert.match(globals, /@media \(forced-colors: active\)[\s\S]*\.skip-link/)
  assert.match(globals, /@media \(prefers-reduced-motion: reduce\)[\s\S]*\.skip-link/)
})
