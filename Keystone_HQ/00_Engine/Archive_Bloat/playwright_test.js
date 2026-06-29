/**
 * Keystone Playwright Smoke Test
 * Tests: headless browsing, screenshots, network monitoring, multi-tab
 */
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('=== KEYSTONE PLAYWRIGHT SMOKE TEST ===\n');

  // 1. Launch browser
  console.log('[1/6] Launching headless Chromium...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'KeystoneMasterBrain/1.0'
  });
  console.log('  ✅ Browser launched\n');

  // 2. Navigate & get page info
  console.log('[2/6] Navigating to Google...');
  const page = await context.newPage();
  await page.goto('https://www.google.com');
  const title = await page.title();
  const url = page.url();
  console.log(`  ✅ Page title: "${title}"`);
  console.log(`  ✅ URL: ${url}\n`);

  // 3. Screenshot capability
  console.log('[3/6] Taking screenshot...');
  const screenshotDir = path.join(__dirname, 'playwright_screenshots');
  const fs = require('fs');
  if (!fs.existsSync(screenshotDir)) fs.mkdirSync(screenshotDir, { recursive: true });
  const screenshotPath = path.join(screenshotDir, 'smoke_test.png');
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`  ✅ Screenshot saved: ${screenshotPath}\n`);

  // 4. Network request monitoring
  console.log('[4/6] Testing network monitoring...');
  const requests = [];
  page.on('request', req => requests.push({ method: req.method(), url: req.url().substring(0, 80) }));
  await page.goto('https://playwright.dev');
  const pwTitle = await page.title();
  console.log(`  ✅ Playwright.dev title: "${pwTitle}"`);
  console.log(`  ✅ Captured ${requests.length} network requests\n`);

  // 5. Multi-tab test
  console.log('[5/6] Testing multi-tab...');
  const page2 = await context.newPage();
  await page2.goto('https://github.com');
  const ghTitle = await page2.title();
  const pages = context.pages();
  console.log(`  ✅ GitHub title: "${ghTitle}"`);
  console.log(`  ✅ Total open tabs: ${pages.length}\n`);

  // 6. JavaScript execution
  console.log('[6/6] Testing JS execution in page...');
  const result = await page.evaluate(() => {
    return {
      innerWidth: window.innerWidth,
      innerHeight: window.innerHeight,
      userAgent: navigator.userAgent.substring(0, 50),
      timestamp: new Date().toISOString()
    };
  });
  console.log(`  ✅ Window: ${result.innerWidth}x${result.innerHeight}`);
  console.log(`  ✅ UA: ${result.userAgent}...`);
  console.log(`  ✅ Time: ${result.timestamp}\n`);

  // Cleanup
  await browser.close();
  console.log('=== ALL TESTS PASSED ✅ ===');
  console.log('\nPlaywright is fully operational for the Keystone Master Brain!');
})().catch(err => {
  console.error('❌ TEST FAILED:', err.message);
  process.exit(1);
});
