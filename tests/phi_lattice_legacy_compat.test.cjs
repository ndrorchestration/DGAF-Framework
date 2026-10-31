// Combined non-authorizing characterization drawn from draft PR #1554.
// This test asserts *current* divergence, not correctness or release authority.
const { test } = require('node:test')
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')
const ts = require('typescript')

function loadRoute(name) {
  const source = fs.readFileSync(path.join(__dirname, '../pages/api', name), 'utf8')
  const js = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
  }).outputText
  const mod = { exports: {} }
  function requireStub(id) {
    if (id === '../../lib/evidence') return { evidenceEnvelope: fields => fields }
    throw Error('Unexpected runtime import: ' + id)
  }
  vm.runInNewContext(js, { module: mod, exports: mod.exports, require: requireStub, Buffer })
  return mod.exports.default
}

function post(handler, body, action) {
  const res = {
    statusCode: 200,
    status(value) { this.statusCode = value; return this },
    json(body) { this.body = body; return this },
  }
  handler({ method: 'POST', query: action ? { action } : {}, body }, res)
  return res
}

const orchestrate = loadRoute('orchestrate.ts')
const triad = loadRoute('triad.ts')

test('confidence=1 remains divergent, and legacy endpoint is explicitly non-authorizing', () => {
  const input = { payload: 'ordinary', claim: 'sample', confidence: 1, turn: 1 }
  const a = post(orchestrate, input)
  const b = post(triad, input, 'turn')
  assert.equal(a.statusCode, 200)
  assert.equal(a.body.effective_confidence, 0.618034)
  assert.equal(a.body.evidence.status, 'PARTIAL')
  assert.equal(b.statusCode, 503)
  assert.equal(b.body.decision, 'NOT_IMPLEMENTED')
  assert.equal(b.body.authority, 'NONE')
  assert.equal(b.body.effective_confidence, 1)
  assert.equal('seal' in b.body, false)
})

test('orchestration checkpoint remains blocked and numeric input stays bounded', () => {
  for (const turn of [13, 21, 34, 55]) {
    const result = post(orchestrate, { confidence: 1, turn })
    assert.equal(result.statusCode, 503)
    assert.equal(result.body.decision, 'BLOCKED')
  }
  for (const confidence of [NaN, Infinity, -0.01, 1.01]) {
    const result = post(orchestrate, { confidence, turn: 1 })
    assert.equal(result.statusCode, 400)
    assert.equal(result.body.decision, 'REJECT')
  }
})
