// Characterization only: preserves existing divergent route behavior pending #1552.
// This is NOT acceptance of either numeric contract and does not exercise live authorization.
const { test } = require('node:test')
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')
const ts = require('typescript')

function loadRoute(filename) {
  const source = fs.readFileSync(path.join(__dirname, '../pages/api', filename), 'utf8')
  const js = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
  }).outputText
  const moduleObject = { exports: {} }
  const requireStub = (name) => {
    if (name === '../../lib/evidence') {
      return { evidenceEnvelope: (record) => ({ ...record, characterization_only: true }) }
    }
    throw new Error('Unexpected runtime import: ' + name)
  }
  vm.runInNewContext(js, { module: moduleObject, exports: moduleObject.exports, require: requireStub }, {
    filename,
  })
  return moduleObject.exports.default
}

function post(handler, body, action) {
  const res = {
    statusCode: 200,
    status(code) { this.statusCode = code; return this },
    json(value) { this.body = value; return this },
  }
  handler({ method: 'POST', query: action ? { action } : {}, body }, res)
  return res
}

const orchestrate = loadRoute('orchestrate.ts')
const triad = loadRoute('triad.ts')

// Historical baseline at main 1a95b94332dffb404c5a3ce026d70781a8c10b90.
test('current non-checkpoint route outputs diverge at confidence 1', () => {
  const a = post(orchestrate, { payload: 'ordinary', claim: 'sample', confidence: 1, turn: 1 })
  const b = post(triad, { payload: 'ordinary', claim: 'sample', confidence: 1, turn: 1 }, 'turn')
  assert.equal(a.statusCode, 200)
  assert.equal(a.body.evidence.status, 'PARTIAL')
  assert.equal(a.body.effective_confidence, 0.618034)
  assert.equal(b.statusCode, 200)
  assert.equal(b.body.effective_confidence, 1)
  assert.notEqual(a.body.effective_confidence, b.body.effective_confidence)
})

test('existing input edge cases are characterized without endorsing semantics', () => {
  const cases = [
    [0, 0],
    [0.5, 0.618034],
    [0.8, 0.618034],
    [1, 0.618034],
  ]
  for (const [confidence, expected] of cases) {
    const res = post(orchestrate, { confidence, turn: 1 })
    assert.equal(res.statusCode, 200)
    assert.equal(res.body.effective_confidence, expected)
  }
  for (const confidence of [NaN, Infinity, -0.01, 1.01]) {
    const res = post(orchestrate, { confidence, turn: 1 })
    assert.equal(res.statusCode, 400)
    assert.equal(res.body.decision, 'REJECT')
  }
})

test('checkpoint remains fail-closed without live audit state', () => {
  for (const turn of [13, 21, 34, 55]) {
    const res = post(orchestrate, { confidence: 1, turn })
    assert.equal(res.statusCode, 503)
    assert.equal(res.body.decision, 'BLOCKED')
    assert.equal(res.body.evidence.status, 'BLOCKED')
  }
})
