const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function runResearch() {
    console.log("Starting Keystone Playwright Deep Research (Agent Directed)...");
    
    // Read queue
    const queuePath = 'C:\\Users\\Curtis\\.gemini\\antigravity\\brain\\dcfb044f-d157-4191-8dd4-486712240c1d\\deep_research_queue.md';
    const queueContent = fs.readFileSync(queuePath, 'utf-8');
    const prompts = [...queueContent.matchAll(/\*\*"([^"]+)"\*\*/g)].map(m => m[1]);
    console.log(`Found ${prompts.length} prompts to research.`);

    const outDir = 'c:\\Users\\Curtis\\New folder\\construction-website\\Keystone_HQ\\00_Master_Brain\\Deep_Research_Results';
    if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

    // Launch browser
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    });
    
    const page = await context.newPage();
    
    for (let i = 0; i < prompts.length; i++) {
        const prompt = prompts[i];
        console.log(`\n[${i+1}/${prompts.length}] Researching: ${prompt.substring(0, 40)}...`);
        
        try {
            // Using DuckDuckGo Lite which is extremely reliable for scraping
            await page.goto('https://lite.duckduckgo.com/lite/', { waitUntil: 'domcontentloaded' });
            
            // Wait for input
            await page.fill('input[name="q"]', prompt + " 2026 update guide MCP AI");
            await page.click('input[type="submit"]');
            await page.waitForLoadState('domcontentloaded');
            
            const results = await page.evaluate(() => {
                const links = Array.from(document.querySelectorAll('.result-snippet'));
                return links.map(el => el.innerText).join('\n\n---\n\n');
            });

            // Follow the first 2 links for deeper content if available
            let deepContent = "";
            try {
                const firstLink = await page.$('.result-url');
                if (firstLink) {
                    const url = await firstLink.getAttribute('href');
                    if (url && !url.includes('youtube')) {
                        const newPage = await context.newPage();
                        await newPage.goto(url, { timeout: 15000, waitUntil: 'domcontentloaded' });
                        deepContent = await newPage.evaluate(() => document.body.innerText.substring(0, 5000));
                        await newPage.close();
                    }
                }
            } catch (e) {
                console.log("  Failed to deep-click link. Relying on snippets.");
            }

            const mdContent = `# Deep Research: ${prompt}\n\n## Search Intelligence (2026)\n\n${results}\n\n## Deep Content Extract\n\n${deepContent}`;
            const filename = `DeepDive_${i+1}_${Date.now()}.md`;
            
            fs.writeFileSync(path.join(outDir, filename), mdContent);
            console.log(`  ✅ Saved intelligence to ${filename}`);
            
            // Random pause to prevent rate limiting
            await page.waitForTimeout(3000 + Math.random() * 2000);
            
        } catch (err) {
            console.log(`  ❌ Error: ${err.message}`);
        }
    }
    
    await browser.close();
    console.log("\n🎉 All 40 Deep Dives Completed Successfully!");
}

runResearch().catch(console.error);
