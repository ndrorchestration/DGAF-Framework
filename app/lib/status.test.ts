import test from 'node:test'
import assert from 'node:assert/strict'
import { STATUS_META, normalizeRuntimeStatus, statusMeta } from './status.ts'

test('loading is neutral rather than destructive', () => {
  const loading = statusMeta('loading')
  assert.equal(loading.tone, 'neutral')
  assert.notEqual(loading.label, 'Failed')
  assert.notEqual(loading.label, 'Denied')
})

test('pass and verified remain distinct evidence states', () => {
  assert.equal(STATUS_META.pass.label, 'Pass')
  assert.equal(STATUS_META.verified.label, 'Verified')
  assert.notEqual(STATUS_META.pass.label, STATUS_META.verified.label)
})

test('not authorized and not established remain distinct', () => {
  assert.equal(STATUS_META.not_authorized.label, 'Not authorized')
  assert.equal(STATUS_META.not_established.label, 'Not established')
  assert.notEqual(STATUS_META.not_authorized.description, STATUS_META.not_established.description)
})

test('unknown runtime input remains unknown', () => {
  assert.equal(normalizeRuntimeStatus('mystery'), 'unknown')
  assert.equal(normalizeRuntimeStatus(undefined), 'unknown')
})

test('runtime ok maps to pass, never verified', () => {
  assert.equal(normalizeRuntimeStatus('ok'), 'pass')
  assert.notEqual(normalizeRuntimeStatus('ok'), 'verified')
})
