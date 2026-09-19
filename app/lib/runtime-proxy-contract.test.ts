import test from 'node:test'
import assert from 'node:assert/strict'
import { existsSync, readFileSync } from 'node:fs'

const proxy = readFileSync('proxy.ts', 'utf8')
const pyproject = readFileSync('pyproject.toml', 'utf8')

test('Next.js 16 proxy migration preserves the API-only CORS boundary', () => {
  assert.equal(existsSync('middleware.ts'), false)
  assert.match(proxy, /export function proxy\(request: NextRequest\)/)
  assert.match(proxy, /matcher: "\/api\/:path\*"/)
  assert.match(proxy, /if \(!request\.nextUrl\.pathname\.startsWith\("\/api\/"\)\)/)
})

test('proxy preserves exact allowlist and fail-closed preflight behavior', () => {
  for (const origin of [
    'https://dynamicgovernanceagenticformation.vercel.app',
    'https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app',
    'https://dynamicgovernanceagenticformation-git-main-ndrorchestration.vercel.app',
  ]) {
    assert.match(proxy, new RegExp(origin.replaceAll('.', '\\.') ))
  }
  assert.match(proxy, /status: allowed \? 204 : 403/)
  assert.match(proxy, /Access-Control-Allow-Methods", "GET,POST,OPTIONS"/)
  assert.match(proxy, /Access-Control-Allow-Headers", "Content-Type,Authorization,X-AHG-Session,X-AHG-Turn"/)
  assert.match(proxy, /Access-Control-Max-Age", "600"/)
  assert.match(proxy, /Vary", "Origin"/)
})

test('Vercel Python runtime remains pinned to the Python 3.12 series', () => {
  assert.match(pyproject, /requires-python = "~=3\.12\.0"/)
})
