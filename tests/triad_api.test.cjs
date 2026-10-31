// Regression checks for the legacy non-authorizing Pages Router diagnostic.
// Run: node --test tests/triad_api.test.cjs (requires npm dependencies installed).
const { test } = require('node:test')
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')
const ts = require('typescript')

const source = fs.readFileSync(path.join(__dirname, '../pages/api/triad.ts'), 'utf8')
const compiled = ts.transpileModule(source, {
  compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
}).outputText
const moduleObject = { exports: {} }
vm.runInNewContext(compiled, { module: moduleObject, exports: moduleObject.exports })
const handler = moduleObject.exports.default

function call(action, body, method = 'POST') {
  const response = {
    statusCode: 200,
    status(code) { this.statusCode = code; return this },
    json(value) { this.body = value; return this },
  }
  handler({ method, query: { action }, body }, response)
  return response
}

test('legacy turn cannot report PASS or a cryptographic seal', () => {
  const res = call('turn', { payload: 'hello', claim: 'a real claim', confidence: 1, turn: 1 })
  assert.equal(res.statusCode, 503)
  assert.equal(res.body.decision, 'NOT_IMPLEMENTED')
  assert.equal(res.body.authority, 'NONE')
  assert.equal(res.body.mode, 'PROTOTYPE_DIAGNOSTIC_ONLY')
  assert.equal('seal' in res.body, false)
  assert.equal('seal' in res.body.gates.g9_amethyst, false)
  assert.equal(res.body.gates.g9_amethyst.status, 'NOT_IMPLEMENTED')
})

test('invalid numeric values cannot reach diagnostic gates', () => {
  for (const confidence of [NaN, Infinity, -1, 2, '0.5']) {
    assert.equal(call('turn', { confidence, turn: 1 }).statusCode, 400)
  }
  for (const turn of [0, -1, 0.5, '2']) {
    assert.equal(call('turn', { confidence: 0.5, turn }).statusCode, 400)
  }
})

test('blocked phrases remain rejected and explicitly non-authoritative', () => {
  const res = call('turn', { payload: 'ignore previous', confidence: 0.5, turn: 1 })
  assert.equal(res.statusCode, 400)
  assert.equal(res.body.decision, 'KILL')
  assert.equal(res.body.authority, 'NONE')
})

test('unknown actions and methods are rejected', () => {
  assert.equal(call('anything', {}).statusCode, 400)
  assert.equal(call('turn', {}, 'GET').statusCode, 405)
})

test('triad formation remains a structural check, not a turn authorization', () => {
  const res = call('form', { triad_id: 'governance', agents: ['sentinel', 'amethyst', 'apogee'] })
  assert.equal(res.statusCode, 200)
  assert.equal(res.body.formed, true)
  assert.equal('decision' in res.body, false)
})

test('malformed triad formation inputs fail with 400 rather than crashing', () => {
  for (const agents of [null, {}, 12, 'amethyst', [null, 'apogee'], ['amethyst', 1]]) {
    assert.equal(call('form', { triad_id: 'governance', agents }).statusCode, 400)
  }
  for (const triad_id of ['__proto__', 'constructor', null, 123]) {
    assert.equal(call('form', { triad_id, agents: [] }).statusCode, 400)
  }
})
