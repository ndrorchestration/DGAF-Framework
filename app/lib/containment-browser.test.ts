import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { createServer } from 'node:http'
import test from 'node:test'

const browserModule = process.env.DGAF_PLAYWRIGHT_MODULE
const browserExecutable = process.env.DGAF_CHROMIUM_EXECUTABLE
const browserUnavailable = !browserModule || !browserExecutable

async function withPage(blockModule: boolean, check: (page: any) => Promise<void>) {
  const server = createServer((request, response) => {
    const path = request.url?.split('?')[0]
    if (blockModule && path === '/evidence/tektite-containment-view.mjs') {
      response.writeHead(503).end('Module deliberately unavailable')
      return
    }
    if (!['/evidence/tektite-containment-v0.html', '/evidence/tektite-containment-view.mjs'].includes(path ?? '')) {
      response.writeHead(404).end()
      return
    }
    response.setHeader('Content-Type', path?.endsWith('.mjs') ? 'text/javascript' : 'text/html')
    response.end(readFileSync(new URL(`../../public${path}`, import.meta.url)))
  })
  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', resolve))
  let browser: any
  try {
    const module = await import(browserModule!)
    browser = await module.chromium.launch({
      executablePath: browserExecutable,
      args: ['--no-sandbox', '--disable-gpu', '--disable-software-rasterizer', '--disable-dev-shm-usage', '--no-zygote'],
      headless: true,
    })
    const page = await browser.newPage()
    const address = server.address()
    assert.ok(address && typeof address === 'object')
    await page.goto(`http://127.0.0.1:${address.port}/evidence/tektite-containment-v0.html`)
    await check(page)
  } finally {
    try {
      if (browser) await browser.close()
    } finally {
      await new Promise<void>((resolve, reject) => server.close((error) => error ? reject(error) : resolve()))
    }
  }
}

test('containment replay stays unavailable when its module request fails', { skip: browserUnavailable }, async () => {
  await withPage(true, async (page) => {
    const text = await page.locator('#cases').innerText()
    assert.match(text, /Evidence unavailable/)
    assert.doesNotMatch(text, /Loading/)
    assert.equal(await page.locator('article').count(), 0)
    assert.match(await page.locator('.boundary').innerText(), /Live containment: NOT_ESTABLISHED/)
  })
})

test('containment replay replaces the fallback only with validated cases', { skip: browserUnavailable }, async () => {
  await withPage(false, async (page) => {
    await page.waitForSelector('article')
    assert.equal(await page.locator('article').count(), 5)
    assert.doesNotMatch(await page.locator('#cases').innerText(), /Evidence unavailable/)
  })
})
