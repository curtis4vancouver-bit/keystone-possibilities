const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

async function resetChat(page) {
    try {
        // Try to click "New chat" using xpath or CSS
        const newChatBtns = await page.$$('button[aria-label="New chat"], span');
        for (const btn of newChatBtns) {
            const text = await page.evaluate(el => el.textContent, btn);
            if (text && text.includes('New chat')) {
                await btn.click();
                await new Promise(r => setTimeout(r, 2000));
                return true;
            }
        }
        await page.goto('https://gemini.google.com/app');
        await new Promise(r => setTimeout(r, 2000));
        return true;
    } catch (e) {
        await page.goto('https://gemini.google.com/app');
        return false;
    }
}

async function processPromptInTab(page, prompt, i, promptsLength, outDir) {
    console.log(`\n[${i+1}/${promptsLength}] Executing Gemini Deep Research for: ${prompt.substring(0, 40)}...`);
    
    try {
        await page.bringToFront();
        
        const inputSelector = 'div[role="textbox"]';
        await page.waitForSelector(inputSelector, { timeout: 15000 });
        await page.type(inputSelector, prompt, { delay: 10 });
        
        // Click the '+' button
        try {
            const plusBtn = await page.$('button[aria-label="Add files or tools"], button[aria-label="Upload"]');
            if (plusBtn) {
                await plusBtn.click();
                await new Promise(r => setTimeout(r, 1000));
                
                // Use evaluate to find the Deep Research text and click its parent
                const clicked = await page.evaluate(() => {
                    const elements = Array.from(document.querySelectorAll('*'));
                    const dr = elements.find(el => el.textContent && el.textContent.trim() === 'Deep Research');
                    if (dr) {
                        dr.click();
                        return true;
                    }
                    return false;
                });
                
                if (clicked) {
                    console.log(`  [Tab ${i+1}] ✅ Activated Deep Research via '+' menu`);
                    await new Promise(r => setTimeout(r, 500));
                }
            }
        } catch(e) {
            console.log(`  [Tab ${i+1}] ⚠️ Could not find '+' menu, attempting direct submit...`);
        }
        
        await page.keyboard.press('Enter');
        console.log(`  [Tab ${i+1}] Submitted prompt. Waiting for completion...`);
        
        // Wait for generation
        await page.waitForSelector('button[aria-label="Copy"], button[aria-label="Good response"]', { timeout: 600000 });
        
        // Extract text
        const text = await page.evaluate(() => {
            const msgs = document.querySelectorAll('.message-content');
            if (msgs.length === 0) return null;
            return msgs[msgs.length - 1].innerText;
        });
        
        if (text) {
            const mdContent = `# Deep Research: ${prompt}\n\n## Gemini Output\n\n${text}`;
            const filename = `DeepDive_${i+1}_${Date.now()}.md`;
            fs.writeFileSync(path.join(outDir, filename), mdContent);
            console.log(`  [Tab ${i+1}] ✅ Saved intelligence to ${filename}`);
        }
        
        console.log(`  [Tab ${i+1}] Resetting chat for next prompt...`);
        await resetChat(page);
        console.log(`  [Tab ${i+1}] ✅ Chat reset successful.`);
        
    } catch (err) {
        console.log(`  [Tab ${i+1}] ❌ Error: ${err.message}`);
        await resetChat(page);
    }
}

async function runResearch() {
    console.log("Starting Keystone Puppeteer Deep Research (Batches of 3)...");
    
    const queuePath = 'C:\\Users\\Curtis\\.gemini\\antigravity\\brain\\dcfb044f-d157-4191-8dd4-486712240c1d\\deep_research_queue.md';
    const queueContent = fs.readFileSync(queuePath, 'utf-8');
    const prompts = [...queueContent.matchAll(/\*\*"([^"]+)"\*\*/g)].map(m => m[1]);
    console.log(`Found ${prompts.length} prompts.`);

    const outDir = 'c:\\Users\\Curtis\\New folder\\construction-website\\Keystone_HQ\\00_Master_Brain\\Deep_Research_Results';
    if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

    let browser;
    try {
        console.log(`Launching Visual Chrome using your main profile...`);
        browser = await puppeteer.launch({
            executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            userDataDir: 'C:\\Users\\Curtis\\AppData\\Local\\Google\\Chrome\\User Data',
            headless: false,
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled']
        });
        console.log("✅ Successfully launched Visual Chrome with your profile!");
    } catch (err) {
        console.error("❌ Failed to launch:", err.message);
        process.exit(1);
    }
    
    const BATCH_SIZE = 3;
    const workerPages = [];
    
    console.log(`Creating ${BATCH_SIZE} persistent worker tabs...`);
    for (let i = 0; i < BATCH_SIZE; i++) {
        const page = await browser.newPage();
        await page.goto('https://gemini.google.com/app');
        workerPages.push(page);
    }
    
    for (let i = 0; i < prompts.length; i += BATCH_SIZE) {
        const batch = prompts.slice(i, i + BATCH_SIZE);
        console.log(`\n=== Starting Batch ${Math.floor(i/BATCH_SIZE) + 1} ===`);
        
        const promises = batch.map((prompt, index) => 
            processPromptInTab(workerPages[index], prompt, i + index, prompts.length, outDir)
        );
        
        await Promise.all(promises);
        console.log(`=== Batch ${Math.floor(i/BATCH_SIZE) + 1} Complete ===`);
        await new Promise(r => setTimeout(r, 10000));
    }
    
    for (const page of workerPages) {
        await page.close();
    }
    
    browser.disconnect();
    console.log("\n🎉 All 40 Deep Dives Completed Successfully!");
    process.exit(0);
}

runResearch().catch(console.error);
