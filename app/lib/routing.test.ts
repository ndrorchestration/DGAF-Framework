import assert from 'node:assert/strict'
import { existsSync, readFileSync } from 'node:fs'
import test from 'node:test'

const navigation = readFileSync('app/lib/navigation.ts', 'utf8')
const shell = readFileSync('app/components/app-shell.tsx', 'utf8')
const overview = readFileSync('app/components/overview-view.tsx', 'utf8')
const provider = readFileSync('app/components/dashboard-runtime-provider.tsx', 'utf8')
const commandCenterLayout = readFileSync('app/(command-center)/layout.tsx', 'utf8')

const REQUIRED_ROUTES = [
  ['overview', '/'],
  ['control', '/control'],
  ['governance', '/governance'],
  ['agents', '/agents'],
  ['evidence', '/evidence'],
  ['tools', '/tools'],
] as const

test('required command-center views have stable public routes', () => {
  for (const [id, href] of REQUIRED_ROUTES) {
    assert.match(navigation, new RegExp(`id: ['"]${id}['"][\\s\\S]*href: ['"]${href.replace('/', '\\/')}['"]`))
  }
})

test('accepted State Space view is preserved as an addressable current-lineage route', () => {
  assert.match(navigation, /id: ['"]state-space['"][\s\S]*href: ['"]\/state-space['"]/)
  assert.equal(existsSync('app/(command-center)/state-space/page.tsx'), true)
})

test('shared shell derives navigation from pathname and semantic links', () => {
  assert.match(shell, /from 'next\/link'/)
  assert.match(shell, /usePathname/)
  assert.match(shell, /aria-current=\{activeView === id \? 'page' : undefined\}/)
  assert.doesNotMatch(shell, /onNavigate/)
  assert.doesNotMatch(shell, /<button key=\{id\} className="nav-item"/)
})

test('overview actions are real links rather than callback navigation', () => {
  assert.match(overview, /<Link className="button primary" href="\/evidence">Inspect evidence/)
  assert.match(overview, /<Link className="button ghost" href="\/control">Open control room<\/Link>/)
  assert.match(overview, /<Link className="text-button" href="\/evidence">Explore evidence/)
  assert.match(overview, /<Link className="button ghost" href="\/governance">View ordered chain/)
  assert.doesNotMatch(overview, /onNavigate/)
})

test('one shared runtime provider owns dashboard polling', () => {
  assert.match(provider, /useDashboardData\(\)/)
  assert.match(provider, /createContext/)
  assert.match(commandCenterLayout, /<DashboardRuntimeProvider>/)
  assert.match(commandCenterLayout, /<AppShell>/)

  const routeFiles = [
    'app/(command-center)/page.tsx',
    'app/(command-center)/control/page.tsx',
    'app/(command-center)/governance/page.tsx',
    'app/(command-center)/state-space/page.tsx',
    'app/(command-center)/agents/page.tsx',
    'app/(command-center)/evidence/page.tsx',
    'app/(command-center)/tools/page.tsx',
  ]
  for (const path of routeFiles) {
    const source = readFileSync(path, 'utf8')
    assert.doesNotMatch(source, /useDashboardData/)
  }
})

test('legacy local view-state page is removed', () => {
  assert.equal(existsSync('app/page.tsx'), false)
})
